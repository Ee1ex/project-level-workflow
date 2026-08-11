import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import workflow


ROOT = Path(__file__).resolve().parents[1]


class PackageValidationTests(unittest.TestCase):
    def test_current_package_passes_deterministic_validation(self) -> None:
        self.assertEqual(workflow.validate_package(ROOT), [])

    def test_validation_reports_missing_required_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            errors = workflow.validate_package(Path(directory))
        self.assertTrue(errors)
        self.assertIn("缺少", " ".join(errors))

    def test_cli_validate_package_returns_zero(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "workflow.py"),
                "validate-package",
                "--package-root",
                str(ROOT),
            ],
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("包验证通过", result.stdout)

    def test_version_is_consistent_across_public_contracts(self) -> None:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        schema = json.loads(
            (ROOT / "schemas" / "workflow-state.schema.json").read_text(encoding="utf-8")
        )
        evals = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertEqual(schema["properties"]["workflow_version"]["const"], version)
        self.assertEqual(evals["version"], version)
        self.assertIn(f"## [{version}]", changelog)

    def test_package_contract_exposes_four_active_levels(self) -> None:
        self.assertEqual(
            workflow.LEVEL_SOPS,
            {
                1: "LEVEL1-快速验证与轻量交付流程.md",
                2: "LEVEL2-可持续运营项目开发流程.md",
                3: "LEVEL3-已有与开源项目改进流程.md",
                4: "LEVEL4-复杂项目需求分析流程.md",
            },
        )
        self.assertTrue((ROOT / "references" / "project-vibe-spec-bridge.md").is_file())


if __name__ == "__main__":
    unittest.main()
