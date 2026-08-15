import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core" / "project-vibe-spec"

PVS_TEMPLATES = (
    "AGENTS.md.template",
    "DOCUMENT_MAP.md.template",
    "Decisions/DEC-YYYYMMDD-NNN.md.template",
    "Decisions/LEDGER.md.template",
    "Decisions/README.md.template",
    "Progress/LEDGER.md.template",
    "Progress/PROG-REQ-YYYYMMDD-NNN-slug.md.template",
    "Progress/README.md.template",
    "Requirements/LEDGER.md.template",
    "Requirements/README.md.template",
    "Requirements/REQ-YYYYMMDD-NNN.md.template",
    "docs/BUG_TRACKER.md.template",
    "docs/BUSINESS_FLOW.md.template",
    "docs/PDD.md.template",
    "docs/PRD.md.template",
    "docs/PROGRESS.md.template",
    "docs/UI_GUIDE.md.template",
)


class EmbeddedPvsTests(unittest.TestCase):
    def test_core_is_complete_and_not_discoverable_as_a_second_skill(self) -> None:
        self.assertTrue((CORE / "PVS.md").is_file())
        self.assertFalse((CORE / "SKILL.md").exists())
        self.assertTrue((CORE / "references" / "decision-gates.md").is_file())
        self.assertTrue((CORE / "references" / "document-maintenance.md").is_file())
        starter = CORE / "assets" / "governance-starter"
        for relative in PVS_TEMPLATES:
            with self.subTest(template=relative):
                self.assertTrue((starter / relative).is_file(), relative)

    def test_source_records_authorized_commit_and_root_mit_license(self) -> None:
        source_path = CORE / "SOURCE.md"
        self.assertTrue(source_path.is_file())
        source = source_path.read_text(encoding="utf-8")
        self.assertIn("https://github.com/dnwwdwd/project-vibe-spec.git", source)
        self.assertIn("dae5315", source)
        self.assertIn("MIT", source)
        self.assertIn("PVS.md", source)

    def test_template_map_has_one_default_per_role(self) -> None:
        map_path = ROOT / "templates" / "template-map.json"
        self.assertTrue(map_path.is_file())
        data = json.loads(map_path.read_text(encoding="utf-8"))
        self.assertEqual(data["version"], 1)
        names = [entry["name"] for entry in data["roles"]]
        defaults = [entry["default"] for entry in data["roles"]]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(defaults), len(set(defaults)))
        for entry in data["roles"]:
            self.assertTrue((ROOT / entry["default"]).is_file(), entry["default"])
            for compatibility in entry.get("compatibility", []):
                self.assertTrue((ROOT / compatibility).is_file(), compatibility)


if __name__ == "__main__":
    unittest.main()
