import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_level_md_is_the_only_root_level_document(self):
        level_doc = ROOT / "LEVEL.md"
        self.assertTrue(level_doc.is_file())
        self.assertEqual(
            [path.name for path in ROOT.glob("LEVEL*.md")],
            ["LEVEL.md"],
        )

    def test_level_md_defines_all_four_current_levels(self):
        text = (ROOT / "LEVEL.md").read_text(encoding="utf-8")
        for heading in (
            "## LEVEL 1：快速验证与轻量交付",
            "## LEVEL 2：可持续运营项目",
            "## LEVEL 3：已有、团队与开源项目改进",
            "## LEVEL 4：复杂项目需求分析",
        ):
            self.assertIn(heading, text)
        self.assertIn("持续更新不等于持续运营", text)
        self.assertIn("旧 LEVEL 2 → 新 LEVEL 3", text)
        self.assertIn("旧 LEVEL 3 → 新 LEVEL 4", text)

    def test_public_metadata_exists(self):
        for relative in ["README.md", "LEVEL.md", "VERSION", "CHANGELOG.md", "LICENSE"]:
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

    def test_only_root_skill_is_discoverable(self):
        skill_files = sorted(
            path.relative_to(ROOT).as_posix() for path in ROOT.rglob("SKILL.md")
        )
        self.assertEqual(skill_files, ["SKILL.md"])

    def test_public_workflow_routes_to_embedded_pvs(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        bridge = (ROOT / "references" / "project-vibe-spec-bridge.md").read_text(
            encoding="utf-8"
        )
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for text in (skill, bridge, readme):
            self.assertIn("core/project-vibe-spec/PVS.md", text)
            self.assertNotIn("另行安装 `project-vibe-spec`", text)
        self.assertIn("templates/template-map.json", bridge)
        self.assertIn("LEVEL.md", bridge)


if __name__ == "__main__":
    unittest.main()
