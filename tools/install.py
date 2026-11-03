"""Install selected skills from an extracted Skill Base Codex bundle (stdlib only)."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path, PurePosixPath


def load_bundle(source: Path) -> dict:
    manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1 or manifest.get("agent") != "codex":
        raise ValueError("Manifesto incompatível")
    names = manifest.get("skills")
    if not isinstance(names, list) or not names or any(
        not isinstance(name, str) or not re.fullmatch(r"skill-base-[a-z0-9]+(?:-[a-z0-9]+)*", name)
        for name in names
    ) or len(set(names)) != len(names):
        raise ValueError("Lista de skills inválida")
    files = manifest.get("files_sha256")
    if not isinstance(files, dict) or not files:
        raise ValueError("Manifesto sem arquivos")
    if "LICENSE" not in files:
        raise ValueError("Pacote sem licença")
    for relative, expected in files.items():
        path = PurePosixPath(relative)
        if path.is_absolute() or ".." in path.parts or "\\" in relative or ":" in relative:
            raise ValueError(f"Caminho inválido no manifesto: {relative}")
        local = source.joinpath(*path.parts)
        if not local.resolve().is_relative_to(source.resolve()) or not local.is_file():
            raise ValueError(f"Arquivo ausente ou fora do pacote: {relative}")
        if hashlib.sha256(local.read_bytes()).hexdigest() != expected:
            raise ValueError(f"Checksum divergente: {relative}")
    for local in source.rglob("*"):
        if local.is_symlink():
            raise ValueError(f"Symlink não permitido no pacote: {local}")
        if local.is_file() and local.relative_to(source).as_posix() not in {*files, "manifest.json"}:
            raise ValueError(f"Arquivo fora do manifesto: {local}")
    for name in names:
        if f"skills/{name}/SKILL.md" not in files or f"skills/{name}/agents/openai.yaml" not in files:
            raise ValueError(f"Skill incompleta: {name}")
    return manifest


def install(source: Path, destination: Path, selected: list[str] | None = None, replace: bool = False) -> list[str]:
    source = source.resolve()
    manifest = load_bundle(source)
    names = list(dict.fromkeys(selected if selected is not None else manifest["skills"]))
    if not names or set(names) - set(manifest["skills"]):
        raise ValueError("Seleção vazia ou skill ausente no pacote")
    # Inspect before resolving so a symlink destination cannot silently redirect a replacement.
    destination = destination.absolute()
    if any(path.is_symlink() for path in [destination, *destination.parents]):
        raise ValueError("Destino de instalação não pode atravessar symlinks")
    destination = destination.resolve()
    if destination.is_relative_to(source) or source.is_relative_to(destination):
        raise ValueError("Origem e destino de instalação não podem se sobrepor")
    for name in names:
        target = destination / name
        if target.is_symlink():
            raise ValueError(f"Destino é symlink: {target}")
        if target.exists():
            if not replace:
                raise ValueError(f"Skill já existe: {name}; use --replace para substituí-la")
            if not target.is_dir() or not (target / "SKILL.md").is_file():
                raise ValueError(f"Destino não é uma skill substituível: {name}")
    destination.mkdir(parents=True, exist_ok=True)
    # Stage the entire selection before replacing anything. Backups permit rollback on failure.
    staging = Path(tempfile.mkdtemp(prefix=".skill-base-", dir=destination))
    cleanup = True
    try:
        for name in names:
            shutil.copytree(source / "skills" / name, staging / "new" / name)
            shutil.copy2(source / "LICENSE", staging / "new" / name / "LICENSE")
        installed, backed_up = [], []
        try:
            for name in names:
                target = destination / name
                if target.exists():
                    backup = staging / "old" / name
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    target.rename(backup)
                    backed_up.append(name)
                (staging / "new" / name).rename(target)
                installed.append(name)
        except BaseException:
            try:
                for name in reversed(installed):
                    shutil.rmtree(destination / name)
                for name in reversed(backed_up):
                    (staging / "old" / name).rename(destination / name)
            except BaseException as error:
                cleanup = False
                raise RuntimeError(f"Restauração interrompida; backups preservados em {staging}") from error
            raise
    finally:
        if cleanup:
            shutil.rmtree(staging)
    return names


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent,
                        help="Pasta extraída que contém manifest.json (padrão: pasta deste script)")
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--project", type=Path, help="Raiz explícita de um projeto existente")
    scope.add_argument("--global", dest="global_scope", action="store_true", help="Instalar em ~/.agents/skills")
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--all", action="store_true", help="Instalar todas as skills deste pacote")
    selection.add_argument("--skill", action="append", help="Nome completo; repetir para selecionar várias")
    parser.add_argument("--replace", action="store_true", help="Substituir somente as skills selecionadas")
    args = parser.parse_args(argv)
    if args.project is not None and not args.project.is_dir():
        parser.error("--project deve apontar para um diretório existente")
    destination = (Path.home() if args.global_scope else args.project) / ".agents" / "skills"
    try:
        names = install(args.source, destination, args.skill, args.replace)
    except (ValueError, OSError, RuntimeError) as error:
        parser.exit(1, f"Erro: {error}\n")
    print(f"Instaladas {len(names)} skills em {destination.resolve()}")
    print("O Codex detecta as skills automaticamente; reinicie se elas não aparecerem.")


if __name__ == "__main__":
    main()
