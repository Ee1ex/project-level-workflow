from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_NAMES = (
    "install.ps1",
    "install.sh",
    "update.ps1",
    "update.sh",
    "uninstall.ps1",
    "uninstall.sh",
)


class LifecycleScriptTests(unittest.TestCase):
    def _read(self, name: str) -> str:
        return (ROOT / "scripts" / name).read_text(encoding="utf-8")

    def test_all_lifecycle_scripts_exist_and_support_dry_run(self) -> None:
        for name in SCRIPT_NAMES:
            with self.subTest(script=name):
                path = ROOT / "scripts" / name
                self.assertTrue(path.is_file(), f"缺少生命周期脚本：{name}")
                content = self._read(name).lower()
                self.assertIn("dryrun" if name.endswith(".ps1") else "dry-run", content)

    def test_scripts_include_path_safety_and_chinese_errors(self) -> None:
        for name in SCRIPT_NAMES:
            with self.subTest(script=name):
                content = self._read(name)
                self.assertIn("错误", content)
                self.assertIn("project-level-workflow", content)
                if name.endswith(".ps1"):
                    self.assertIn("GetFullPath", content)
                    self.assertIn("-LiteralPath", content)
                else:
                    self.assertIn("set -euo pipefail", content)
                    self.assertIn('"$target"', content)

    def test_install_and_update_have_version_and_conflict_backup_policy(self) -> None:
        for name in ("install.ps1", "install.sh", "update.ps1", "update.sh"):
            with self.subTest(script=name):
                content = self._read(name).lower()
                self.assertIn("version", content)
                self.assertIn("backup", content)
                self.assertIn("conflict", content)

    def test_installers_include_all_active_sops_and_compatibility_entries(self) -> None:
        expected = (
            "LEVEL1-快速验证与轻量交付流程",
            "LEVEL2-可持续运营项目开发流程",
            "LEVEL3-已有与开源项目改进流程",
            "LEVEL4-复杂项目需求分析流程",
        )
        for name in ("install.ps1", "install.sh"):
            content = self._read(name)
            for item in expected:
                with self.subTest(script=name, item=item):
                    self.assertIn(item, content)

    def test_update_runs_doctor_and_state_migration_before_replacement(self) -> None:
        for name in ("update.ps1", "update.sh"):
            with self.subTest(script=name):
                content = self._read(name).lower()
                self.assertIn("doctor", content)
                self.assertIn("migrate", content)

    def test_uninstall_preserves_project_state_and_project_docs(self) -> None:
        for name in ("uninstall.ps1", "uninstall.sh"):
            with self.subTest(script=name):
                content = self._read(name)
                self.assertIn(".project-workflow", content)
                self.assertIn("docs/project-workflow", content)
                self.assertIn("保留", content)

    def test_powershell_avoids_cross_shell_and_string_execution(self) -> None:
        forbidden = ("cmd /c", "bash -c", "sh -c", "Invoke-Expression", "iex ", "Start-Process")
        for name in ("install.ps1", "update.ps1", "uninstall.ps1"):
            with self.subTest(script=name):
                content = self._read(name)
                self.assertIn("Set-StrictMode -Version Latest", content)
                self.assertIn("$ErrorActionPreference = 'Stop'", content)
                for item in forbidden:
                    self.assertNotIn(item, content)

    def test_shell_scripts_quote_copy_move_and_remove_targets(self) -> None:
        for name in ("install.sh", "update.sh", "uninstall.sh"):
            with self.subTest(script=name):
                content = self._read(name)
                self.assertNotIn("eval ", content)
                self.assertNotIn("rm -rf $target", content)
                self.assertNotIn("cp -R $", content)
                self.assertNotIn("mv $", content)


if __name__ == "__main__":
    unittest.main()
