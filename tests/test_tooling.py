"""Observable packaging, validation and installation behavior; all writes are isolated."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TEMP_ROOT = ROOT / "dist" / "test-workspaces"
TEMP_ROOT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / "tools"))
import catalog

spec = importlib.util.spec_from_file_location("installer", ROOT / "tools/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class PackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workspace = tempfile.TemporaryDirectory(prefix="skill-base-tests-", dir=TEMP_ROOT)
        cls.base = Path(cls.workspace.name)
        cls.output = cls.base / "packages"
        cls.version = catalog.read_version(ROOT)
        cls.paths = catalog.build(ROOT, cls.output)
        cls.archive = cls.output / f"skill-base-codex-v{cls.version}.zip"

    @classmethod
    def tearDownClass(cls):
        cls.workspace.cleanup()

    def setUp(self):
        self.work = tempfile.TemporaryDirectory(prefix="case-", dir=self.base)
        self.addCleanup(self.work.cleanup)
        self.folder = Path(self.work.name)
        with zipfile.ZipFile(self.archive) as archive:
            archive.extractall(self.folder)
        self.source = self.folder / self.archive.stem
        self.project = self.folder / "projeto com espaços"
        self.project.mkdir()
        self.destination = self.project / ".agents/skills"
        self.manifest = installer.load_bundle(self.source)
        self.names = self.manifest["skills"]

    def test_complete_and_individual_archives_are_self_contained(self):
        archives = [p for p in self.paths if p.suffix == ".zip"]
        self.assertEqual(len(archives), 7)
        for path in archives:
            with self.subTest(archive=path.name), zipfile.ZipFile(path) as archive:
                members = archive.namelist()
                prefix = path.stem + "/"
                self.assertTrue(all(name.startswith(prefix) for name in members))
                manifest = json.loads(archive.read(prefix + "manifest.json"))
                self.assertEqual(manifest["version"], self.version)
                self.assertEqual(len(manifest["skills"]), 6 if path == self.archive else 1)
                self.assertEqual(set(members), {prefix + p for p in manifest["files_sha256"]} | {prefix + "manifest.json"})
                self.assertIn(prefix + "LICENSE", members)
                self.assertIn(prefix + "install.py", members)
                self.assertIn("source_commit", manifest)
                self.assertTrue(manifest["adapted_from"]["source_files_sha256"])
                self.assertFalse(any("/claude/" in p or "/github-copilot/" in p for p in members))
                for filename, expected in manifest["files_sha256"].items():
                    self.assertEqual(hashlib.sha256(archive.read(prefix + filename)).hexdigest(), expected)

    def test_checksums_cover_all_artifacts_except_checksum_file(self):
        lines = (self.output / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 8)
        for line in lines:
            expected, name = line.split("  ", 1)
            self.assertEqual(hashlib.sha256((self.output / name).read_bytes()).hexdigest(), expected)

    def test_repeated_build_is_identical(self):
        second = catalog.build(ROOT, self.folder / "second")
        self.assertEqual({p.name: p.read_bytes() for p in self.paths}, {p.name: p.read_bytes() for p in second})

    def test_install_all_and_selected_preserve_other_files(self):
        marker = self.project / "arquivo.txt"
        marker.write_text("preservar", encoding="utf-8")
        installed = installer.install(self.source, self.destination, [self.names[0]])
        self.assertEqual(installed, [self.names[0]])
        self.assertEqual((self.destination / self.names[0] / "LICENSE").read_bytes(), (self.source / "LICENSE").read_bytes())
        self.assertEqual([p.name for p in self.destination.iterdir()], [self.names[0]])
        installer.install(self.source, self.destination, self.names[1:])
        self.assertEqual(sorted(p.name for p in self.destination.iterdir()), sorted(self.names))
        self.assertEqual(marker.read_text(encoding="utf-8"), "preservar")

    def test_collisions_are_preflighted_before_any_copy(self):
        installer.install(self.source, self.destination, [self.names[-1]])
        with self.assertRaisesRegex(ValueError, "já existe"):
            installer.install(self.source, self.destination)
        self.assertEqual([p.name for p in self.destination.iterdir()], [self.names[-1]])

    def test_replace_selected_removes_stale_resources_only_in_selection(self):
        installer.install(self.source, self.destination)
        old = self.destination / self.names[0] / "recurso-antigo.txt"
        old.write_text("antigo", encoding="utf-8")
        preserved = self.destination / self.names[1] / "personalizado.txt"
        preserved.write_text("manter", encoding="utf-8")
        unrelated = self.destination / "outra-skill"
        unrelated.mkdir()
        installer.install(self.source, self.destination, [self.names[0]], replace=True)
        self.assertFalse(old.exists())
        self.assertTrue(preserved.exists())
        self.assertTrue(unrelated.exists())

    def test_unknown_skill_and_tampering_do_not_create_destination(self):
        with self.assertRaisesRegex(ValueError, "ausente"):
            installer.install(self.source, self.destination, ["../../fora"])
        (self.source / "skills" / self.names[0] / "SKILL.md").write_text("alterado", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Checksum"):
            installer.install(self.source, self.destination)
        self.assertFalse(self.destination.exists())

    def test_unlisted_resources_and_manifest_traversal_are_rejected(self):
        extra = self.source / "skills" / self.names[0] / "extra.txt"
        extra.write_text("não listado", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "fora do manifesto"):
            installer.install(self.source, self.destination)
        extra.unlink()
        self.manifest["files_sha256"]["../fora"] = "0" * 64
        (self.source / "manifest.json").write_text(json.dumps(self.manifest), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Caminho inválido"):
            installer.install(self.source, self.destination)
        self.assertFalse(self.destination.exists())

    def test_non_skill_destination_is_not_replaceable(self):
        (self.destination / self.names[0]).mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "não é uma skill"):
            installer.install(self.source, self.destination, [self.names[0]], replace=True)

    def test_failed_replacement_restores_entire_selection(self):
        installer.install(self.source, self.destination)
        marker = self.destination / self.names[0] / "local.txt"
        marker.write_text("original", encoding="utf-8")
        original_rename = Path.rename

        def fail_second_install(path, target):
            if path.parent.name == "new" and path.name == self.names[1]:
                raise OSError("falha simulada")
            return original_rename(path, target)

        with patch.object(Path, "rename", fail_second_install):
            with self.assertRaisesRegex(OSError, "simulada"):
                installer.install(self.source, self.destination, self.names[:2], replace=True)
        self.assertEqual(marker.read_text(encoding="utf-8"), "original")
        self.assertEqual(sorted(p.name for p in self.destination.iterdir()), sorted(self.names))

    def test_project_cli_and_global_scope_with_isolated_home(self):
        result = subprocess.run([sys.executable, str(self.source / "install.py"), "--project", str(self.project), "--all"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(list(self.destination.iterdir())), 6)
        fake_home = self.folder / "usuario"
        with patch.object(installer.Path, "home", return_value=fake_home):
            installer.main(["--source", str(self.source), "--global", "--skill", self.names[0]])
        self.assertTrue((fake_home / ".agents/skills" / self.names[0] / "SKILL.md").is_file())

    def test_failed_rollback_preserves_backups_for_recovery(self):
        installer.install(self.source, self.destination)
        marker = self.destination / self.names[0] / "local.txt"
        marker.write_text("preservar mesmo na falha", encoding="utf-8")
        original_rename = Path.rename

        def fail_install_and_restore(path, target):
            if path.parent.name == "new" and path.name == self.names[1]:
                raise OSError("falha na instalação")
            if path.parent.name == "old":
                raise OSError("falha ao restaurar")
            return original_rename(path, target)

        with patch.object(Path, "rename", fail_install_and_restore):
            with self.assertRaisesRegex(RuntimeError, "backups preservados"):
                installer.install(self.source, self.destination, self.names[:2], replace=True)
        backups = list(self.destination.glob(".skill-base-*/old/*/local.txt"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), "preservar mesmo na falha")

    def test_individual_zip_installs_without_other_skills(self):
        individual = next(p for p in self.paths if p.suffix == ".zip" and p != self.archive)
        directory = self.folder / "individual"
        with zipfile.ZipFile(individual) as archive:
            archive.extractall(directory)
        source = directory / individual.stem
        names = installer.install(source, self.destination)
        self.assertEqual(len(names), 1)
        self.assertTrue((self.destination / names[0] / "SKILL.md").is_file())


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory(prefix="skill-base-validation-", dir=TEMP_ROOT)
        self.addCleanup(self.work.cleanup)
        self.root = Path(self.work.name)
        shutil.copytree(ROOT / "codex", self.root / "codex")
        (self.root / "VERSION").write_text("0.1.0\n", encoding="utf-8")

    def test_catalog_without_tag(self):
        self.assertEqual(len(catalog.validate(self.root)), 6)

    def test_invalid_version_is_rejected(self):
        (self.root / "VERSION").write_text("01.0.0", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "VERSION"):
            catalog.validate(self.root)

    def test_frontmatter_name_and_missing_resource_are_rejected(self):
        skill = self.root / "codex/skills/skill-base-escrever-us"
        path = skill / "SKILL.md"
        original = path.read_text(encoding="utf-8")
        path.write_text(original.replace("name: skill-base-escrever-us", "name: outro"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "frontmatter"):
            catalog.validate(self.root)
        path.write_text(original, encoding="utf-8")
        (skill / "assets/modelo-us.md").unlink()
        with self.assertRaisesRegex(ValueError, "Link ausente"):
            catalog.validate(self.root)

    def test_links_cannot_depend_on_another_skill(self):
        path = self.root / "codex/skills/skill-base-escrever-us/SKILL.md"
        with path.open("a", encoding="utf-8") as file:
            file.write("\n[Dependência externa](../skill-base-escrever-task/SKILL.md)\n")
        with self.assertRaisesRegex(ValueError, "externo à skill"):
            catalog.validate(self.root)

    def test_yaml_duplicate_keys_and_discovery_disabled_are_rejected(self):
        path = self.root / "codex/skills/skill-base-escrever-us/agents/openai.yaml"
        original = path.read_text(encoding="utf-8")
        path.write_text(original + "policy: {}\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicada"):
            catalog.validate(self.root)
        path.write_text(original.replace("allow_implicit_invocation: true", "allow_implicit_invocation: false"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "automática"):
            catalog.validate(self.root)


if __name__ == "__main__":
    unittest.main()
