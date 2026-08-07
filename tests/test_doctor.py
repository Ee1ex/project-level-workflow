import subprocess
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
        self.assertIn("三份 LEVEL SOP", result.stdout)

    def test_doctor_fails_when_required_files_are_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            result = run_cli("doctor", "--package-root", temp)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FAIL", result.stdout)


if __name__ == "__main__":
    unittest.main()
