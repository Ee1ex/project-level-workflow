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
            "## LEVEL 1：快速开发与完整项目记忆",
            "## LEVEL 2：完整 PVS 持续运营",
            "## LEVEL 3：已有、团队与开源项目改进",
            "## LEVEL 4：复杂自动化参考与路由",
        ):
            self.assertIn(heading, text)
        self.assertIn("持续更新不等于持续运营", text)
        self.assertIn("旧 LEVEL 2 → 新 LEVEL 3", text)
        self.assertIn("旧 LEVEL 3 → 新 LEVEL 4", text)

    def test_public_metadata_exists(self):
        for relative in ["README.md", "LEVEL.md", "VERSION", "CHANGELOG.md", "LICENSE"]:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_version_uses_two_numeric_segments(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, re.compile(r"^\d+\.\d+$"))
        self.assertEqual(version, "1.0")

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
            "references/documentation-contract.md",
            "references/personal-execution-loop.md",
        ]:
            self.assertTrue((ROOT / relative).is_file(), relative)
            self.assertIn(relative, skill)
        self.assertIn("用户明确确认前", skill)
        for policy in ("AUTO", "CONFIRM", "MANUAL_ONLY"):
            self.assertIn(policy, skill)

    def test_level_four_allows_confirmed_execution_without_embedding_capabilities(self):
        level = (ROOT / "LEVEL.md").read_text(encoding="utf-8")
        bridge = (ROOT / "references" / "project-vibe-spec-bridge.md").read_text(
            encoding="utf-8"
        )
        for text in (level, bridge):
            self.assertIn("负责人确认后可实施", text)
            self.assertNotIn("LEVEL 4 永久只分析", text)
        self.assertIn("外部", level)
        self.assertIn("不得内嵌", level)

    def test_level_four_and_github_plugin_routing_contracts(self):
        level4_path = ROOT / "references" / "level4-capability-routing.md"
        github_path = ROOT / "references" / "github-plugin-routing.md"
        self.assertTrue(level4_path.is_file())
        self.assertTrue(github_path.is_file())
        level4 = level4_path.read_text(encoding="utf-8")
        github_routing = github_path.read_text(encoding="utf-8")
        for action in ("push", "Draft PR", "Merge", "Tag", "Release"):
            self.assertIn(action, github_routing)
        self.assertIn("GitHub 插件", github_routing)
        self.assertIn("执行前确认", github_routing)
        self.assertIn("远端验证", github_routing)
        for node in (
            "需求判断",
            "原型",
            "技术方案",
            "任务拆解",
            "实现",
            "测试联调",
            "代码 Review",
            "部署准备",
            "日志排查",
            "复盘",
        ):
            self.assertIn(node, level4)
        for phrase in ("已安装则路由", "缺失时提醒安装", "拒绝安装时降级", "不得内嵌"):
            self.assertIn(phrase, level4)

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
