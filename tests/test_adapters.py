import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "workflow.py"
START = "<!-- project-level-workflow:start -->"
END = "<!-- project-level-workflow:end -->"


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )


class AdapterTests(unittest.TestCase):
    def _initialized_project(self, temp: str, level: str = "2") -> Path:
        result = run_cli("init", "--project", temp, "--level", level)
        self.assertEqual(result.returncode, 0, result.stderr)
        return Path(temp)

    def test_codex_preserves_user_content_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self._initialized_project(temp)
            target = project / "AGENTS.md"
            target.write_text("# 用户规则\n\n保留此内容。\n", encoding="utf-8")
            for _ in range(2):
                result = run_cli("render-adapter", "--platform", "codex", "--project", temp)
                self.assertEqual(result.returncode, 0, result.stderr)
            text = target.read_text(encoding="utf-8")
            self.assertIn("保留此内容", text)
            self.assertIn("LEVEL2-已有与开源项目改进流程.md", text)
            self.assertEqual(text.count(START), 1)
            self.assertEqual(text.count(END), 1)

    def test_claude_code_renders_managed_block(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self._initialized_project(temp, "1")
            result = run_cli("render-adapter", "--platform", "claude-code", "--project", temp)
            self.assertEqual(result.returncode, 0, result.stderr)
            text = (project / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertIn("LEVEL1-小型项目开发流程.md", text)
            self.assertIn(".project-workflow/state.json", text)
            self.assertEqual(text.count(START), 1)

    def test_cursor_renders_mdc_frontmatter(self):
        with tempfile.TemporaryDirectory() as temp:
            project = self._initialized_project(temp, "3")
            result = run_cli("render-adapter", "--platform", "cursor", "--project", temp)
            self.assertEqual(result.returncode, 0, result.stderr)
            target = project / ".cursor" / "rules" / "project-level-workflow.mdc"
            text = target.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"))
            self.assertIn("alwaysApply: false", text)
            self.assertIn("description:", text)
            self.assertIn("LEVEL3-持续运营产品开发流程.md", text)

    def test_unknown_platform_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            self._initialized_project(temp)
            result = run_cli("render-adapter", "--platform", "unknown", "--project", temp)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
