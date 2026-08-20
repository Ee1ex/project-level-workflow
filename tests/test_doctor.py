import subprocess
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "workflow.py"


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


class DoctorTests(unittest.TestCase):
    def test_doctor_passes_for_package(self):
        result = run_cli("doctor", "--package-root", str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)
        self.assertIn("统一 LEVEL.md", result.stdout)

    def test_doctor_fails_when_required_files_are_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            result = run_cli("doctor", "--package-root", temp)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FAIL", result.stdout)

    def test_doctor_warns_but_passes_for_independent_pvs(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            package = parent / "project-level-workflow"
            shutil.copytree(ROOT, package)
            (parent / "project-vibe-spec").mkdir()
            result = run_cli("doctor", "--package-root", str(package))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("WARN 独立 project-vibe-spec", result.stdout)

    def test_doctor_reports_embedded_pvs(self):
        result = run_cli("doctor", "--package-root", str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PVS 包内内核", result.stdout)
        self.assertIn("PVS 模板职责映射", result.stdout)

    def test_doctor_requires_elx_level_cursor_adapter(self):
        self.assertTrue((ROOT / "adapters" / "cursor" / "elx-level.mdc").is_file())
        self.assertFalse(
            (ROOT / "adapters" / "cursor" / "project-level-workflow.mdc").exists()
        )


if __name__ == "__main__":
    unittest.main()
