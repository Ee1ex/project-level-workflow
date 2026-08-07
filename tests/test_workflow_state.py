import json
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


class WorkflowStateTests(unittest.TestCase):
    def test_init_creates_state_backup_and_status(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            result = run_cli("init", "--project", temp, "--level", "1")
            self.assertEqual(result.returncode, 0, result.stderr)
            state_path = project / ".project-workflow" / "state.json"
            backup_path = project / ".project-workflow" / "state.backup.json"
            status_path = project / "docs" / "project-workflow" / "STATUS.md"
            self.assertTrue(state_path.is_file())
            self.assertTrue(backup_path.is_file())
            self.assertTrue(status_path.is_file())
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["level"], 1)
            self.assertFalse(state["permissions"]["allow_push_own_branch"])
            self.assertFalse(state["permissions"]["allow_create_draft_pr"])

    def test_validate_accepts_valid_state(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(run_cli("init", "--project", temp, "--level", "2").returncode, 0)
            result = run_cli("validate", "--project", temp)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("状态有效", result.stdout)

    def test_validate_rejects_missing_field_invalid_level_and_absolute_path(self):
        cases = [
            lambda state: state.pop("stage"),
            lambda state: state.__setitem__("level", 9),
            lambda state: state.__setitem__("artifacts", [{"path": "C:\\private\\file.md"}]),
        ]
        for mutate in cases:
            with self.subTest(mutate=mutate), tempfile.TemporaryDirectory() as temp:
                self.assertEqual(run_cli("init", "--project", temp, "--level", "1").returncode, 0)
                state_path = Path(temp) / ".project-workflow" / "state.json"
                state = json.loads(state_path.read_text(encoding="utf-8"))
                mutate(state)
                state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
                result = run_cli("validate", "--project", temp)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("状态无效", result.stderr)

    def test_init_does_not_overwrite_without_force(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            self.assertEqual(run_cli("init", "--project", temp, "--level", "1").returncode, 0)
            state_path = project / ".project-workflow" / "state.json"
            original = json.loads(state_path.read_text(encoding="utf-8"))
            original["project_id"] = "keep-me"
            state_path.write_text(json.dumps(original, ensure_ascii=False), encoding="utf-8")
            blocked = run_cli("init", "--project", temp, "--level", "2")
            self.assertEqual(blocked.returncode, 2)
            self.assertEqual(json.loads(state_path.read_text(encoding="utf-8"))["project_id"], "keep-me")
            forced = run_cli("init", "--project", temp, "--level", "2", "--force")
            self.assertEqual(forced.returncode, 0, forced.stderr)
            backup = json.loads(
                (project / ".project-workflow" / "state.backup.json").read_text(encoding="utf-8")
            )
            self.assertEqual(backup["project_id"], "keep-me")
            self.assertEqual(json.loads(state_path.read_text(encoding="utf-8"))["level"], 2)

    def test_status_renders_fixed_sections(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(run_cli("init", "--project", temp, "--level", "3").returncode, 0)
            result = run_cli("status", "--project", temp)
            self.assertEqual(result.returncode, 0, result.stderr)
            status = (Path(temp) / "docs" / "project-workflow" / "STATUS.md").read_text(
                encoding="utf-8"
            )
            for section in [
                "当前 LEVEL、阶段与任务",
                "本轮目标与不做范围",
                "已完成内容",
                "验证命令与结果摘要",
                "当前风险与未决事项",
                "当前人工 Gate",
                "推荐选择与下一步",
            ]:
                self.assertIn(section, status)

    def test_transition_requires_matching_gate_and_approval(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            self.assertEqual(run_cli("init", "--project", temp, "--level", "1").returncode, 0)
            mismatch = run_cli(
                "transition",
                "--project",
                temp,
                "--approve-gate",
                "wrong-gate",
                "--to-stage",
                "requirements",
                "--approved-by",
                "owner",
            )
            self.assertEqual(mismatch.returncode, 2)
            success = run_cli(
                "transition",
                "--project",
                temp,
                "--approve-gate",
                "level-confirmed",
                "--to-stage",
                "requirements",
                "--approved-by",
                "owner",
            )
            self.assertEqual(success.returncode, 0, success.stderr)
            state = json.loads(
                (project / ".project-workflow" / "state.json").read_text(encoding="utf-8")
            )
            self.assertEqual(state["stage"], "requirements")
            self.assertIsNone(state["gate"])
            self.assertEqual(state["history"][-1]["approved_by"], "owner")

    def test_migrate_supported_state_and_rejects_future_schema(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            self.assertEqual(run_cli("init", "--project", temp, "--level", "2").returncode, 0)
            state_path = project / ".project-workflow" / "state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["schema_version"] = "0.9.0"
            state.pop("permissions")
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            migrated = run_cli("migrate", "--project", temp)
            self.assertEqual(migrated.returncode, 0, migrated.stderr)
            current = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(current["schema_version"], "1.0.0")
            self.assertFalse(current["permissions"]["allow_push_own_branch"])
            current["schema_version"] = "9.0.0"
            state_path.write_text(json.dumps(current, ensure_ascii=False), encoding="utf-8")
            rejected = run_cli("migrate", "--project", temp)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("不支持", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
