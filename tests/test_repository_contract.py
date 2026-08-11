import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_canonical_level_docs_exist(self):
        expected = [
            "LEVEL1-快速验证与轻量交付流程.md",
            "LEVEL2-可持续运营项目开发流程.md",
            "LEVEL3-已有与开源项目改进流程.md",
            "LEVEL4-复杂项目需求分析流程.md",
        ]
        for relative in expected:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_legacy_level_docs_are_explicit_compatibility_entries(self):
        expected_targets = {
            "LEVEL1-小型项目开发流程.md": "LEVEL1-快速验证与轻量交付流程.md",
            "LEVEL2-已有与开源项目改进流程.md": "LEVEL3-已有与开源项目改进流程.md",
            "LEVEL3-持续运营产品开发流程.md": "LEVEL2-可持续运营项目开发流程.md",
        }
        for relative, target in expected_targets.items():
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("兼容", text, relative)
            self.assertIn(target, text, relative)

    def test_public_metadata_exists(self):
        for relative in ["README.md", "VERSION", "CHANGELOG.md", "LICENSE"]:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_version_is_semver(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, re.compile(r"^\d+\.\d+\.\d+$"))

    def test_public_text_has_no_private_absolute_paths(self):
        public_files = list(ROOT.glob("*.md")) + list(ROOT.glob("references/*.md"))
        forbidden = ("C:\\Users\\", "D:\\VibeCodingFiles", "/Users/")
        for path in public_files:
            text = path.read_text(encoding="utf-8")
            for value in forbidden:
                self.assertNotIn(value, text, f"{path}: {value}")

    def test_skill_frontmatter_and_references(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        self.assertIn("name: project-level-workflow", skill)
        self.assertIn("description:", skill)
        for relative in [
            "references/level-selection.md",
            "references/risk-and-permissions.md",
            "references/state-protocol.md",
            "references/tool-routing.md",
            "references/platform-compatibility.md",
            "references/project-vibe-spec-bridge.md",
        ]:
            self.assertTrue((ROOT / relative).is_file(), relative)
            self.assertIn(relative, skill)

    def test_qima_is_reminder_only(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Qima", skill)
        self.assertIn("不得直接调用", skill)


if __name__ == "__main__":
    unittest.main()
