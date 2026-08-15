import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallIntegrationTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell"), "PowerShell integration test")
    def test_project_install_is_single_skill_and_preserves_independent_pvs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            skills = project / ".codex" / "skills"
            independent = skills / "project-vibe-spec"
            independent.mkdir(parents=True)
            marker = independent / "keep.txt"
            marker.write_text("keep", encoding="utf-8")
            result = subprocess.run(
                [
                    "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                    "-File", str(ROOT / "scripts" / "install.ps1"),
                    "-Platform", "codex", "-Scope", "project", "-ProjectPath", str(project),
                ],
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
                check=False,
                env={
                    **os.environ,
                    "PATH": str(Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", ""),
                },
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            installed = skills / "project-level-workflow"
            skill_files = sorted(path.relative_to(installed).as_posix() for path in installed.rglob("SKILL.md"))
            self.assertEqual(skill_files, ["SKILL.md"])
            self.assertTrue((installed / "core" / "project-vibe-spec" / "PVS.md").is_file())
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")
            self.assertIn("独立 project-vibe-spec", result.stdout)


if __name__ == "__main__":
    unittest.main()
