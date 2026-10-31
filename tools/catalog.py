"""Validation and reproducible release bundles for the Codex catalog."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SEMVER = r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
NAME = re.compile(r"skill-base-[a-z0-9]+(?:-[a-z0-9]+)*")


def read_version(root: Path = ROOT, tag: str | None = None) -> str:
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(SEMVER, version):
        raise ValueError(f"VERSION inválida: {version!r}")
    if tag is not None and (not re.fullmatch("v" + SEMVER, tag) or tag != "v" + version):
        raise ValueError(f"Tag {tag!r} deve ser exatamente v{version}")
    return version


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_yaml(text: str):
    import yaml

    # Duplicate keys usually indicate a mistaken metadata edit.
    class UniqueLoader(yaml.SafeLoader):
        pass

    def mapping(loader, node):
        result = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node)
            if key in result:
                raise ValueError(f"Chave YAML duplicada: {key}")
            result[key] = loader.construct_object(value_node)
        return result

    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    try:
        return yaml.load(text, Loader=UniqueLoader)
    except yaml.YAMLError as error:
        raise ValueError(f"YAML inválido: {error}") from error


def validate(root: Path = ROOT, tag: str | None = None) -> list[Path]:
    read_version(root, tag)
    skills_root = root / "codex" / "skills"
    skills = sorted(p for p in skills_root.iterdir() if p.is_dir())
    if not skills:
        raise ValueError("Catálogo vazio")
    names = set()
    for skill in skills:
        if not NAME.fullmatch(skill.name) or len(skill.name) >= 64:
            raise ValueError(f"Nome inválido: {skill.name}")
        for path in [skill, *skill.rglob("*")]:
            if path.is_symlink():
                raise ValueError(f"Symlink não permitido no pacote: {path}")
            if path.is_file() and (path.name.startswith(".") or path.suffix == ".pyc"):
                raise ValueError(f"Arquivo transitório no catálogo: {path}")
        text = (skill / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.+)\Z", text, re.S)
        if not match:
            raise ValueError(f"Frontmatter ausente ou corpo vazio: {skill.name}")
        metadata = load_yaml(match[1])
        if not isinstance(metadata, dict) or metadata.get("name") != skill.name:
            raise ValueError(f"Nome do frontmatter diverge da pasta: {skill.name}")
        if metadata["name"] in names:
            raise ValueError(f"Nome duplicado: {skill.name}")
        names.add(metadata["name"])
        if not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
            raise ValueError(f"Descrição ausente: {skill.name}")
        ui = load_yaml((skill / "agents/openai.yaml").read_text(encoding="utf-8"))
        if not isinstance(ui, dict) or "model" in ui:
            raise ValueError(f"Metadados inválidos: {skill.name}")
        interface = ui.get("interface", {})
        if not isinstance(interface, dict):
            raise ValueError(f"Interface inválida: {skill.name}")
        for key in ("display_name", "short_description", "default_prompt"):
            if not isinstance(interface.get(key), str) or not interface[key].strip():
                raise ValueError(f"Metadado ausente {key}: {skill.name}")
        if not 25 <= len(interface["short_description"]) <= 64:
            raise ValueError(f"Descrição de interface deve ter 25–64 caracteres: {skill.name}")
        if "$" + skill.name not in interface["default_prompt"]:
            raise ValueError(f"Prompt não invoca a skill: {skill.name}")
        policy = ui.get("policy")
        if not isinstance(policy, dict) or policy.get("allow_implicit_invocation") is not True:
            raise ValueError(f"Descoberta automática deve estar habilitada: {skill.name}")
        for document in skill.rglob("*.md"):
            content = document.read_text(encoding="utf-8")
            if re.search(r"\b(?:TODO|TBD|FIXME)\b", content):
                raise ValueError(f"Scaffold inacabado: {document}")
            # Templates intentionally have fill-in fields. Markdown links must be real.
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
                target = target.strip().strip("<>")
                parsed = urlsplit(target)
                if parsed.scheme or target.startswith("#"):
                    continue
                linked = (document.parent / unquote(parsed.path)).resolve()
                if not linked.is_relative_to(skill.resolve()) or not linked.is_file():
                    raise ValueError(f"Link ausente ou externo à skill: {document}: {target}")
        for key in ("icon_small", "icon_large"):
            if key in interface:
                icon = (skill / interface[key]).resolve()
                if not icon.is_relative_to(skill.resolve()) or not icon.is_file():
                    raise ValueError(f"Recurso de interface ausente: {skill.name}: {key}")
    return skills


def source_commit(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else "uncommitted"


def build(root: Path = ROOT, output: Path | None = None, tag: str | None = None) -> list[Path]:
    skills = validate(root, tag)
    version = read_version(root, tag)
    output = (output or root / "dist").resolve()
    if output.is_relative_to((root / "codex/skills").resolve()):
        raise ValueError("Saída não pode estar dentro do catálogo")
    output.mkdir(parents=True, exist_ok=True)
    provenance = json.loads((root / "provenance.json").read_text(encoding="utf-8"))
    paths = []
    for selection in [skills, *[[skill] for skill in skills]]:
        suffix = "" if selection == skills else "-" + selection[0].name
        stem = f"skill-base-codex{suffix}-v{version}"
        payload = {}
        for filename in ("LICENSE", "README.md", "PROVENANCE.md", "provenance.json", "VERSION",
                         "CONTRIBUTING.md", "CHANGELOG.md", "tests/skill-scenarios.md"):
            payload[filename] = (root / filename).read_bytes()
        payload["install.py"] = (root / "tools/install.py").read_bytes()
        for skill in selection:
            for path in sorted(skill.rglob("*")):
                if path.is_file():
                    payload["skills/" + path.relative_to(skill.parent).as_posix()] = path.read_bytes()
        manifest = {
            "schema_version": 1,
            "name": "skill-base",
            "agent": "codex",
            "version": version,
            "source_commit": source_commit(root),
            "adapted_from": provenance,
            "skills": [skill.name for skill in selection],
            "files_sha256": {name: digest(data) for name, data in sorted(payload.items())},
        }
        payload["manifest.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        archive = output / (stem + ".zip")
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zipped:
            for filename, data in sorted(payload.items()):
                entry = zipfile.ZipInfo(stem + "/" + filename, date_time=(1980, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                zipped.writestr(entry, data)
        paths.append(archive)
        if selection == skills:
            manifest_path = output / f"skill-base-codex-v{version}-manifest.json"
            manifest_path.write_bytes(payload["manifest.json"])
            paths.append(manifest_path)
    checksums = output / "SHA256SUMS"
    checksums.write_text("".join(f"{digest(path.read_bytes())}  {path.name}\n" for path in sorted(paths)), encoding="utf-8")
    return [*paths, checksums]
