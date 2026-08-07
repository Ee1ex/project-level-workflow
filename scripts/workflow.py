#!/usr/bin/env python3
"""Project Level Workflow 的确定性状态管理 CLI。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any
from urllib.parse import unquote


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "1.0.0"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
REQUIRED_FIELDS = (
    "schema_version",
    "workflow_version",
    "project_id",
    "level",
    "stage",
    "gate",
    "status",
    "risk",
    "permissions",
    "current_task",
    "artifacts",
    "verifications",
    "git",
    "remote",
    "history",
    "updated_at",
)
SENSITIVE_KEY_PARTS = ("password", "secret", "token", "api_key", "private_key")
MANAGED_START = "<!-- project-level-workflow:start -->"
MANAGED_END = "<!-- project-level-workflow:end -->"
LEVEL_SOPS = {
    1: "LEVEL1-小型项目开发流程.md",
    2: "LEVEL2-已有与开源项目改进流程.md",
    3: "LEVEL3-持续运营产品开发流程.md",
}


def configure_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_version() -> str:
    version_path = PACKAGE_ROOT / "VERSION"
    if not version_path.is_file():
        raise ValueError("缺少 VERSION 文件")
    version = version_path.read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(version):
        raise ValueError(f"VERSION 不是合法 SemVer：{version}")
    return version


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    content = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    temporary.write_text(content, encoding="utf-8", newline="\n")
    json.loads(temporary.read_text(encoding="utf-8"))
    temporary.replace(path)


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    normalized = content.rstrip() + "\n"
    temporary.write_text(normalized, encoding="utf-8", newline="\n")
    temporary.replace(path)


def build_initial_state(project: Path, level: int) -> dict[str, Any]:
    project_name = project.name or "project"
    digest = hashlib.sha256(str(project).encode("utf-8")).hexdigest()[:8]
    now = utc_now()
    return {
        "schema_version": SCHEMA_VERSION,
        "workflow_version": load_version(),
        "project_id": f"{project_name}-{digest}",
        "level": level,
        "stage": "initialization",
        "gate": "level-confirmed",
        "status": "in_progress",
        "risk": "R1",
        "permissions": {
            "allow_push_own_branch": False,
            "allow_create_draft_pr": False,
        },
        "current_task": None,
        "artifacts": [],
        "verifications": [],
        "git": {
            "repository": False,
            "branch": None,
            "skill_created_branch": False,
            "last_commit": None,
        },
        "remote": {
            "name": None,
            "url": None,
            "draft_pr": None,
        },
        "history": [
            {
                "event": "workflow_initialized",
                "stage": "initialization",
                "at": now,
            }
        ],
        "updated_at": now,
    }


def _iter_values(value: Any, path: str = ""):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            yield child_path, key, child
            yield from _iter_values(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = f"{path}[{index}]"
            yield child_path, str(index), child
            yield from _iter_values(child, child_path)


def _is_absolute_file_path(value: str) -> bool:
    if value.startswith(("http://", "https://")):
        return False
    return PureWindowsPath(value).is_absolute() or PurePosixPath(value).is_absolute()


def validate_state(data: dict[str, Any], project: Path) -> list[str]:
    del project
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["状态根节点必须是对象"]
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"缺少必填字段：{field}")

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"不支持的 schema_version：{data.get('schema_version')}")
    if not isinstance(data.get("workflow_version"), str) or not SEMVER.fullmatch(
        data.get("workflow_version", "")
    ):
        errors.append("workflow_version 必须是 SemVer")
    if data.get("level") not in (1, 2, 3):
        errors.append("level 只允许 1、2 或 3")
    if data.get("risk") not in ("R1", "R2", "R3", "R4"):
        errors.append("risk 只允许 R1、R2、R3 或 R4")
    if data.get("status") not in ("in_progress", "waiting_approval", "completed", "blocked"):
        errors.append("status 值无效")

    permissions = data.get("permissions")
    if not isinstance(permissions, dict):
        errors.append("permissions 必须是对象")
    else:
        for name in ("allow_push_own_branch", "allow_create_draft_pr"):
            if not isinstance(permissions.get(name), bool):
                errors.append(f"permissions.{name} 必须是布尔值")

    for field in ("artifacts", "verifications", "history"):
        if field in data and not isinstance(data[field], list):
            errors.append(f"{field} 必须是数组")
    for field in ("git", "remote"):
        if field in data and not isinstance(data[field], dict):
            errors.append(f"{field} 必须是对象")

    for value_path, key, value in _iter_values(data):
        lowered = key.lower()
        if any(part in lowered for part in SENSITIVE_KEY_PARTS):
            errors.append(f"状态禁止保存敏感字段：{value_path}")
        if isinstance(value, str) and _is_absolute_file_path(value):
            errors.append(f"状态路径必须相对项目根目录：{value_path}")
    return errors


def _initial_status(state: dict[str, Any]) -> str:
    return f"""# 项目流程状态

- 状态：进行中
- 负责人：待项目负责人确认
- 关联 Gate：{state['gate']}
- 最后更新时间：{state['updated_at']}

## 当前 LEVEL、阶段与任务

LEVEL {state['level']} / {state['stage']} / 尚未创建任务。

## 本轮目标与不做范围

初始化项目流程；尚未批准的实现不在本轮范围。

## 已完成内容

- 创建项目状态和目录。

## 验证命令与结果摘要

- 状态初始化校验通过。

## 当前风险与未决事项

- 需要按对应 LEVEL SOP 创建最小文档包。

## 当前人工 Gate

LEVEL 已确认，等待初始化文档和首个任务。

## 推荐选择与下一步

读取对应 LEVEL SOP，创建最小文档并定义首个可验收任务。
"""


def _format_items(items: list[Any], empty_message: str) -> str:
    if not items:
        return f"- {empty_message}"
    lines: list[str] = []
    for item in items:
        if isinstance(item, dict):
            summary = item.get("summary") or item.get("path") or item.get("command")
            lines.append(f"- {summary or json.dumps(item, ensure_ascii=False)}")
        else:
            lines.append(f"- {item}")
    return "\n".join(lines)


def render_status(data: dict[str, Any]) -> str:
    task = data.get("current_task") or {}
    task_summary = task.get("summary") or task.get("title") or "尚未创建任务"
    scope = task.get("scope") or "当前任务范围尚未写入状态。"
    exclusions = task.get("out_of_scope") or "未记录额外排除项。"
    gate = data.get("gate") or "当前没有等待批准的 Gate。"
    artifacts = _format_items(data.get("artifacts", []), "尚无已记录产物。")
    verifications = _format_items(data.get("verifications", []), "尚无已记录验证。")
    return f"""# 项目流程状态

- 状态：{data['status']}
- 负责人：{task.get('owner') or '待项目负责人确认'}
- 关联 Gate：{gate}
- 最后更新时间：{data['updated_at']}

## 当前 LEVEL、阶段与任务

LEVEL {data['level']} / {data['stage']} / {task_summary}

## 本轮目标与不做范围

- 范围：{scope}
- 本次不做：{exclusions}

## 已完成内容

{artifacts}

## 验证命令与结果摘要

{verifications}

## 当前风险与未决事项

- 风险等级：{data['risk']}
- 未决事项：{task.get('open_questions') or '无已记录未决事项。'}

## 当前人工 Gate

{gate}

## 推荐选择与下一步

{task.get('next_step') or '读取对应 LEVEL SOP，选择下一个最小可验收任务。'}
"""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"状态文件不存在：{path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"状态 JSON 无法解析：第 {exc.lineno} 行第 {exc.colno} 列") from exc


def command_init(args: argparse.Namespace) -> int:
    project = Path(args.project).expanduser().resolve()
    if not project.is_dir():
        print(f"项目目录不存在：{project}", file=sys.stderr)
        return 1
    state_dir = project / ".project-workflow"
    state_path = state_dir / "state.json"
    backup_path = state_dir / "state.backup.json"
    status_path = project / "docs" / "project-workflow" / "STATUS.md"

    previous: dict[str, Any] | None = None
    if state_path.exists():
        if not args.force:
            print("状态已经存在；如需重新初始化，请显式使用 --force", file=sys.stderr)
            return 2
        try:
            previous = _load_json(state_path)
        except ValueError as exc:
            print(f"无法备份现有状态：{exc}", file=sys.stderr)
            return 1

    state = build_initial_state(project, args.level)
    errors = validate_state(state, project)
    if errors:
        print("初始化状态无效：\n- " + "\n- ".join(errors), file=sys.stderr)
        return 1

    if previous is not None:
        atomic_write_json(backup_path, previous)
    else:
        atomic_write_json(backup_path, state)
    atomic_write_json(state_path, state)
    atomic_write_text(status_path, _initial_status(state))
    print(f"已初始化 LEVEL {args.level} 项目流程：{project}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    project = Path(args.project).expanduser().resolve()
    state_path = project / ".project-workflow" / "state.json"
    try:
        state = _load_json(state_path)
    except ValueError as exc:
        print(f"状态无效：\n- {exc}", file=sys.stderr)
        return 1
    errors = validate_state(state, project)
    if errors:
        print("状态无效：\n- " + "\n- ".join(errors), file=sys.stderr)
        return 1
    print(f"状态有效：LEVEL {state['level']} / {state['stage']} / {state['status']}")
    return 0


def _state_paths(project: Path) -> tuple[Path, Path, Path]:
    state_dir = project / ".project-workflow"
    return (
        state_dir / "state.json",
        state_dir / "state.backup.json",
        project / "docs" / "project-workflow" / "STATUS.md",
    )


def command_status(args: argparse.Namespace) -> int:
    project = Path(args.project).expanduser().resolve()
    state_path, _, status_path = _state_paths(project)
    try:
        state = _load_json(state_path)
    except ValueError as exc:
        print(f"状态无效：\n- {exc}", file=sys.stderr)
        return 1
    errors = validate_state(state, project)
    if errors:
        print("状态无效：\n- " + "\n- ".join(errors), file=sys.stderr)
        return 1
    atomic_write_text(status_path, render_status(state))
    print(f"已刷新状态摘要：{status_path}")
    return 0


def command_transition(args: argparse.Namespace) -> int:
    project = Path(args.project).expanduser().resolve()
    state_path, backup_path, status_path = _state_paths(project)
    try:
        state = _load_json(state_path)
    except ValueError as exc:
        print(f"状态无效：\n- {exc}", file=sys.stderr)
        return 1
    errors = validate_state(state, project)
    if errors:
        print("状态无效：\n- " + "\n- ".join(errors), file=sys.stderr)
        return 1
    if state.get("gate") != args.approve_gate:
        print(
            f"Gate 不匹配：当前为 {state.get('gate')}，请求批准 {args.approve_gate}",
            file=sys.stderr,
        )
        return 2
    approved_by = args.approved_by.strip()
    if not approved_by:
        print("approved-by 不能为空", file=sys.stderr)
        return 1

    previous = json.loads(json.dumps(state, ensure_ascii=False))
    now = utc_now()
    state["stage"] = args.to_stage
    state["gate"] = args.next_gate
    state["status"] = "waiting_approval" if args.next_gate else "in_progress"
    state["updated_at"] = now
    state["history"].append(
        {
            "event": "gate_approved",
            "gate": args.approve_gate,
            "to_stage": args.to_stage,
            "approved_by": approved_by,
            "at": now,
        }
    )
    errors = validate_state(state, project)
    if errors:
        print("转换后状态无效：\n- " + "\n- ".join(errors), file=sys.stderr)
        return 1
    atomic_write_json(backup_path, previous)
    atomic_write_json(state_path, state)
    atomic_write_text(status_path, render_status(state))
    print(f"已批准 {args.approve_gate}，进入阶段 {args.to_stage}")
    return 0


def command_migrate(args: argparse.Namespace) -> int:
    project = Path(args.project).expanduser().resolve()
    state_path, backup_path, status_path = _state_paths(project)
    try:
        state = _load_json(state_path)
    except ValueError as exc:
        print(f"状态无效：\n- {exc}", file=sys.stderr)
        return 1
    source_version = state.get("schema_version")
    if source_version == SCHEMA_VERSION:
        errors = validate_state(state, project)
        if errors:
            print("状态无效：\n- " + "\n- ".join(errors), file=sys.stderr)
            return 1
        print("状态 Schema 已是最新版本")
        return 0
    if source_version != "0.9.0":
        print(f"不支持从 Schema {source_version} 迁移", file=sys.stderr)
        return 1

    previous = json.loads(json.dumps(state, ensure_ascii=False))
    now = utc_now()
    state["schema_version"] = SCHEMA_VERSION
    state["workflow_version"] = load_version()
    state.setdefault(
        "permissions",
        {
            "allow_push_own_branch": False,
            "allow_create_draft_pr": False,
        },
    )
    state.setdefault("history", []).append(
        {
            "event": "schema_migrated",
            "from": source_version,
            "to": SCHEMA_VERSION,
            "at": now,
        }
    )
    state["updated_at"] = now
    errors = validate_state(state, project)
    if errors:
        print("迁移后状态无效：\n- " + "\n- ".join(errors), file=sys.stderr)
        return 1
    atomic_write_json(backup_path, previous)
    atomic_write_json(state_path, state)
    atomic_write_text(status_path, render_status(state))
    print(f"已从 Schema {source_version} 迁移到 {SCHEMA_VERSION}")
    return 0


def command_doctor(args: argparse.Namespace) -> int:
    root = Path(args.package_root).expanduser().resolve()
    checks: list[tuple[str, bool, str]] = []
    checks.append(("Python 3.10+", sys.version_info >= (3, 10), sys.version.split()[0]))
    checks.append(("Git 命令", shutil.which("git") is not None, shutil.which("git") or "未发现"))

    level_docs = [
        root / "LEVEL1-小型项目开发流程.md",
        root / "LEVEL2-已有与开源项目改进流程.md",
        root / "LEVEL3-持续运营产品开发流程.md",
    ]
    checks.append(("三份 LEVEL SOP", all(path.is_file() for path in level_docs), "根目录"))
    for relative in [
        "SKILL.md",
        "VERSION",
        "schemas/workflow-state.schema.json",
        "references/level-selection.md",
        "references/risk-and-permissions.md",
        "references/state-protocol.md",
        "references/tool-routing.md",
        "references/platform-compatibility.md",
    ]:
        path = root / relative
        checks.append((relative, path.is_file(), str(path)))

    schema_path = root / "schemas" / "workflow-state.schema.json"
    schema_valid = False
    if schema_path.is_file():
        try:
            json.loads(schema_path.read_text(encoding="utf-8"))
            schema_valid = True
        except (OSError, json.JSONDecodeError):
            schema_valid = False
    checks.append(("状态 Schema JSON", schema_valid, str(schema_path)))

    if args.project:
        project = Path(args.project).expanduser().resolve()
        state_path = project / ".project-workflow" / "state.json"
        state_valid = False
        if state_path.is_file():
            try:
                state_valid = not validate_state(_load_json(state_path), project)
            except ValueError:
                state_valid = False
        checks.append(("项目状态", state_valid, str(state_path)))

    required_failures = 0
    for name, passed, detail in checks:
        if name == "Git 命令" and not passed:
            print(f"WARN {name}：{detail}")
            continue
        marker = "PASS" if passed else "FAIL"
        print(f"{marker} {name}：{detail}")
        if not passed:
            required_failures += 1
    return 1 if required_failures else 0


def _managed_block(content: str) -> str:
    start = content.find(MANAGED_START)
    end = content.find(MANAGED_END)
    if start < 0 or end < start:
        raise ValueError("适配器模板缺少托管区块标记")
    return content[start : end + len(MANAGED_END)]


def _merge_managed_content(existing: str, rendered: str) -> str:
    block = _managed_block(rendered)
    start = existing.find(MANAGED_START)
    end = existing.find(MANAGED_END)
    if start >= 0 and end >= start:
        suffix_start = end + len(MANAGED_END)
        merged = existing[:start].rstrip() + "\n\n" + block + existing[suffix_start:]
        return merged.strip() + "\n"
    if not existing.strip():
        return rendered.strip() + "\n"
    return existing.rstrip() + "\n\n" + block + "\n"


def _write_with_backup(path: Path, content: str) -> None:
    if path.exists():
        backup = path.with_name(f"{path.name}.project-level-workflow.bak")
        atomic_write_text(backup, path.read_text(encoding="utf-8"))
    atomic_write_text(path, content)


def command_render_adapter(args: argparse.Namespace) -> int:
    project = Path(args.project).expanduser().resolve()
    state_path, _, _ = _state_paths(project)
    try:
        state = _load_json(state_path)
    except ValueError as exc:
        print(f"状态无效：\n- {exc}", file=sys.stderr)
        return 1
    errors = validate_state(state, project)
    if errors:
        print("状态无效：\n- " + "\n- ".join(errors), file=sys.stderr)
        return 1

    definitions = {
        "codex": (
            PACKAGE_ROOT / "adapters" / "codex" / "AGENTS.fragment.md",
            project / "AGENTS.md",
        ),
        "claude-code": (
            PACKAGE_ROOT / "adapters" / "claude-code" / "CLAUDE.fragment.md",
            project / "CLAUDE.md",
        ),
        "cursor": (
            PACKAGE_ROOT / "adapters" / "cursor" / "project-level-workflow.mdc",
            project / ".cursor" / "rules" / "project-level-workflow.mdc",
        ),
    }
    template_path, target_path = definitions[args.platform]
    if not template_path.is_file():
        print(f"适配器模板不存在：{template_path}", file=sys.stderr)
        return 1
    rendered = template_path.read_text(encoding="utf-8")
    rendered = rendered.replace("{{LEVEL}}", str(state["level"]))
    rendered = rendered.replace("{{SOP}}", LEVEL_SOPS[state["level"]])

    if target_path.exists():
        existing = target_path.read_text(encoding="utf-8")
        content = _merge_managed_content(existing, rendered)
    else:
        content = rendered.strip() + "\n"
    _write_with_backup(target_path, content)
    print(f"已生成 {args.platform} 项目入口：{target_path}")
    return 0


def _git_output(project: Path, *arguments: str) -> tuple[int, str]:
    git = shutil.which("git")
    if not git:
        return 127, ""
    completed = subprocess.run(
        [git, *arguments],
        cwd=project,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    return completed.returncode, completed.stdout.rstrip()


def inspect_git(project: Path) -> dict[str, Any]:
    project = project.expanduser().resolve()
    result: dict[str, Any] = {
        "available": shutil.which("git") is not None,
        "repository": False,
        "branch": None,
        "default_branch": None,
        "changed_files": [],
        "changes_in_scope": None,
        "unrelated_changes": [],
        "remote_name": None,
        "remote_url": None,
        "authenticated": False,
        "ahead_commits": 0,
    }
    if not result["available"] or not project.is_dir():
        return result
    code, inside = _git_output(project, "rev-parse", "--is-inside-work-tree")
    if code != 0 or inside.lower() != "true":
        return result
    result["repository"] = True

    code, branch = _git_output(project, "branch", "--show-current")
    if code == 0 and branch:
        result["branch"] = branch

    code, status = _git_output(project, "status", "--porcelain=v1", "--untracked-files=all")
    if code == 0 and status:
        changed: list[str] = []
        for line in status.splitlines():
            path = line[3:] if len(line) > 3 else line
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            changed.append(path.strip('"').replace("\\", "/"))
        result["changed_files"] = changed

    code, remotes = _git_output(project, "remote")
    if code == 0 and remotes:
        names = [name for name in remotes.splitlines() if name]
        remote_name = "origin" if "origin" in names else names[0]
        result["remote_name"] = remote_name
        _, remote_url = _git_output(project, "remote", "get-url", remote_name)
        result["remote_url"] = remote_url or None
        _, remote_head = _git_output(
            project, "symbolic-ref", "--quiet", "--short", f"refs/remotes/{remote_name}/HEAD"
        )
        if remote_head.startswith(f"{remote_name}/"):
            result["default_branch"] = remote_head.split("/", 1)[1]
        if branch:
            ahead_code, ahead = _git_output(
                project, "rev-list", "--count", f"{remote_name}/{branch}..HEAD"
            )
            if ahead_code == 0 and ahead.isdigit():
                result["ahead_commits"] = int(ahead)
    return result


def _verifications_passed(state: dict[str, Any]) -> bool:
    verifications = state.get("verifications")
    if not isinstance(verifications, list) or not verifications:
        return False
    accepted = {"pass", "passed", "ok", "success", "成功", "通过"}
    for verification in verifications:
        if not isinstance(verification, dict):
            return False
        status = str(verification.get("status") or verification.get("result") or "").lower()
        if status not in accepted:
            return False
    return True


def _changes_are_in_scope(state: dict[str, Any], git_info: dict[str, Any]) -> bool:
    explicit = git_info.get("changes_in_scope")
    if isinstance(explicit, bool):
        return explicit
    changed = git_info.get("changed_files") or []
    task = state.get("current_task") or {}
    paths = task.get("paths") or []
    if not changed or not paths:
        return False
    normalized = [str(path).strip("/").replace("\\", "/") for path in paths]
    return all(
        any(file == allowed or file.startswith(f"{allowed}/") for allowed in normalized)
        for file in changed
    )


def evaluate_git_action(
    action: str, state: dict[str, Any], git_info: dict[str, Any]
) -> dict[str, Any]:
    supported = {
        "git_init",
        "create_branch",
        "local_commit",
        "push_own_branch",
        "create_draft_pr",
        "force_push",
        "rewrite_history",
        "delete_remote_branch",
        "ready_pr",
        "merge",
        "release",
    }
    if action not in supported:
        raise ValueError(f"未知 Git 动作：{action}")
    decision: dict[str, Any] = {
        "action": action,
        "allowed": False,
        "requires_gate": False,
        "reasons": [],
    }
    reasons: list[str] = decision["reasons"]

    if action in {
        "force_push",
        "rewrite_history",
        "delete_remote_branch",
        "ready_pr",
        "merge",
        "release",
    }:
        reasons.append("禁止自动执行高影响远端动作；人工 Gate 不能把它变成无人值守动作。")
        return decision
    if action == "git_init":
        decision["requires_gate"] = True
        reasons.append("Git 初始化会改变项目治理边界，必须先通过人工 Gate。")
        return decision

    if not git_info.get("available"):
        reasons.append("未发现 Git 命令。")
    if not git_info.get("repository"):
        reasons.append("当前目录不是 Git 仓库。")
    if state.get("risk") not in {"R1", "R2"}:
        reasons.append("只有 R1/R2 任务可自动执行本地 Git 动作。")
    if not isinstance(state.get("current_task"), dict) or not state.get("current_task"):
        reasons.append("缺少已确认的 current_task。")

    if action == "create_branch":
        decision["allowed"] = not reasons
        return decision

    if not (state.get("git") or {}).get("skill_created_branch"):
        reasons.append("当前分支不是本 Skill 创建或明确接管的分支。")
    if not git_info.get("branch"):
        reasons.append("无法识别当前分支。")
    if not git_info.get("changed_files"):
        reasons.append("没有可提交的文件修改。")
    if not _changes_are_in_scope(state, git_info):
        reasons.append("修改超出 current_task 声明范围。")
    if git_info.get("unrelated_changes"):
        reasons.append("检测到用户无关修改，禁止纳入自动提交。")
    if not _verifications_passed(state):
        reasons.append("尚无完整通过的验证证据。")

    if action == "local_commit":
        decision["allowed"] = not reasons
        return decision

    permissions = state.get("permissions") or {}
    branch = git_info.get("branch")
    default_branch = git_info.get("default_branch")
    if not permissions.get("allow_push_own_branch"):
        reasons.append("permissions.allow_push_own_branch=false。")
    if branch in {"main", "master", default_branch}:
        reasons.append("禁止自动写入默认分支。")
    if not git_info.get("remote_name") or not git_info.get("remote_url"):
        reasons.append("未配置可确认的 Git Remote。")
    if not git_info.get("authenticated"):
        reasons.append("尚未确认远端身份验证。")
    if int(git_info.get("ahead_commits") or 0) < 1:
        reasons.append("当前分支没有待推送提交。")

    if action == "create_draft_pr" and not permissions.get("allow_create_draft_pr"):
        reasons.append("permissions.allow_create_draft_pr=false。")

    decision["allowed"] = not reasons
    return decision


def command_git_policy(args: argparse.Namespace) -> int:
    project = Path(args.project).expanduser().resolve()
    state_path, _, _ = _state_paths(project)
    try:
        state = _load_json(state_path)
    except ValueError as exc:
        print(f"状态无效：\n- {exc}", file=sys.stderr)
        return 1
    errors = validate_state(state, project)
    if errors:
        print("状态无效：\n- " + "\n- ".join(errors), file=sys.stderr)
        return 1
    git_info = inspect_git(project)
    if args.authenticated:
        git_info["authenticated"] = True
    decision = evaluate_git_action(args.action, state, git_info)
    print(json.dumps({"decision": decision, "git": git_info}, ensure_ascii=False, indent=2))
    return 0 if decision["allowed"] else 2


def _public_markdown_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in root.rglob("*.md"):
        relative = path.relative_to(root).as_posix()
        if relative.startswith(("docs/superpowers/", "tests/", ".project-workflow/")):
            continue
        if "__pycache__" in path.parts:
            continue
        paths.append(path)
    return sorted(paths)


def _markdown_table_errors(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    groups: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines() + [""]:
        if line.strip().startswith("|") and line.strip().endswith("|"):
            current.append(line.strip())
        elif current:
            groups.append(current)
            current = []
    separator = re.compile(r"^\|(?:\s*:?-{3,}:?\s*\|)+$")
    for index, group in enumerate(groups, start=1):
        if len(group) < 2 or not any(separator.fullmatch(line) for line in group):
            errors.append(f"{path.name} 的第 {index} 个 Markdown 表格缺少有效分隔行")
    return errors


def _markdown_link_errors(root: Path, path: Path, text: str) -> list[str]:
    errors: list[str] = []
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        raw_target = match.group(1).strip().strip("<>")
        target = raw_target.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if " " in target:
            target = target.split(" ", 1)[0]
        candidate = (path.parent / unquote(target)).resolve()
        try:
            candidate.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{path.relative_to(root)} 的相对链接越出包目录：{raw_target}")
            continue
        if not candidate.exists():
            errors.append(f"{path.relative_to(root)} 的相对链接不存在：{raw_target}")
    return errors


def validate_package(root: Path) -> list[str]:
    root = root.expanduser().resolve()
    errors: list[str] = []
    required = [
        "SKILL.md",
        "README.md",
        "VERSION",
        "CHANGELOG.md",
        "LICENSE",
        "LEVEL1-小型项目开发流程.md",
        "LEVEL2-已有与开源项目改进流程.md",
        "LEVEL3-持续运营产品开发流程.md",
        "schemas/workflow-state.schema.json",
        "evals/evals.json",
        "references/level-selection.md",
        "references/risk-and-permissions.md",
        "references/state-protocol.md",
        "references/tool-routing.md",
        "references/platform-compatibility.md",
        "references/git-and-draft-pr.md",
        "adapters/codex/AGENTS.fragment.md",
        "adapters/claude-code/CLAUDE.fragment.md",
        "adapters/cursor/project-level-workflow.mdc",
        "scripts/install.ps1",
        "scripts/install.sh",
        "scripts/update.ps1",
        "scripts/update.sh",
        "scripts/uninstall.ps1",
        "scripts/uninstall.sh",
    ]
    for relative in required:
        if not (root / relative).is_file():
            errors.append(f"缺少公共包文件：{relative}")
    if errors:
        return errors

    try:
        version = (root / "VERSION").read_text(encoding="utf-8").strip()
        schema = json.loads(
            (root / "schemas" / "workflow-state.schema.json").read_text(encoding="utf-8")
        )
        evals = json.loads((root / "evals" / "evals.json").read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, OSError) as exc:
        return [f"公共合同无法读取：{exc}"]
    if not SEMVER.fullmatch(version):
        errors.append("VERSION 不是合法 SemVer")
    if schema.get("properties", {}).get("workflow_version", {}).get("const") != version:
        errors.append("Schema workflow_version 与 VERSION 不一致")
    if evals.get("version") != version:
        errors.append("evals 版本与 VERSION 不一致")
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## [{version}]" not in changelog:
        errors.append("CHANGELOG 未登记当前 VERSION")

    private_paths = ("C:\\Users\\", "D:\\VibeCodingFiles", "/Users/")
    secret_patterns = (
        re.compile(r"ghp_[A-Za-z0-9]{20,}"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    )
    unfinished = re.compile(r"\b(?:TODO|TBD|FIXME|CHANGEME)\b", re.IGNORECASE)
    markdown_files = _public_markdown_files(root)
    for path in markdown_files:
        relative = path.relative_to(root)
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"Markdown 不是有效 UTF-8：{relative}")
            continue
        if not any(line.startswith("#") for line in text.splitlines()):
            errors.append(f"Markdown 缺少标题：{relative}")
        for value in private_paths:
            if value in text:
                errors.append(f"公共文件包含个人绝对路径：{relative}")
        if unfinished.search(text):
            errors.append(f"公共 Markdown 包含未完成占位词：{relative}")
        for pattern in secret_patterns:
            if pattern.search(text):
                errors.append(f"公共 Markdown 疑似包含密钥：{relative}")
        errors.extend(_markdown_table_errors(path, text))
        errors.extend(_markdown_link_errors(root, path, text))

    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    if len(skill.splitlines()) >= 500:
        errors.append("SKILL.md 必须少于 500 行")
    if "Qima" not in skill or "不得直接调用" not in skill:
        errors.append("SKILL.md 缺少 Qima reminder-only 边界")
    if "allow_push_own_branch=false" not in skill or "allow_create_draft_pr=false" not in skill:
        errors.append("SKILL.md 缺少公开远程权限默认关闭声明")

    permission_properties = schema.get("properties", {}).get("permissions", {}).get("properties", {})
    for name in ("allow_push_own_branch", "allow_create_draft_pr"):
        if permission_properties.get(name, {}).get("default") is not False:
            errors.append(f"Schema 中 {name} 必须默认 false")

    for relative in (
        "adapters/codex/AGENTS.fragment.md",
        "adapters/claude-code/CLAUDE.fragment.md",
        "adapters/cursor/project-level-workflow.mdc",
    ):
        adapter = (root / relative).read_text(encoding="utf-8")
        if "{{LEVEL}}" not in adapter or "{{SOP}}" not in adapter:
            errors.append(f"适配器未使用统一 LEVEL/SOP 占位：{relative}")
    return errors


def command_validate_package(args: argparse.Namespace) -> int:
    root = Path(args.package_root).expanduser().resolve()
    errors = validate_package(root)
    if errors:
        print("包验证失败：\n- " + "\n- ".join(errors), file=sys.stderr)
        return 1
    print(f"包验证通过：project-level-workflow {(root / 'VERSION').read_text(encoding='utf-8').strip()}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project Level Workflow 状态工具")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="初始化项目流程状态")
    init_parser.add_argument("--project", required=True)
    init_parser.add_argument("--level", required=True, type=int, choices=(1, 2, 3))
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(handler=command_init)

    validate_parser = subparsers.add_parser("validate", help="校验项目流程状态")
    validate_parser.add_argument("--project", required=True)
    validate_parser.set_defaults(handler=command_validate)

    status_parser = subparsers.add_parser("status", help="刷新人类可读状态摘要")
    status_parser.add_argument("--project", required=True)
    status_parser.set_defaults(handler=command_status)

    transition_parser = subparsers.add_parser("transition", help="批准 Gate 并转换阶段")
    transition_parser.add_argument("--project", required=True)
    transition_parser.add_argument("--approve-gate", required=True)
    transition_parser.add_argument("--to-stage", required=True)
    transition_parser.add_argument("--approved-by", required=True)
    transition_parser.add_argument("--next-gate")
    transition_parser.set_defaults(handler=command_transition)

    migrate_parser = subparsers.add_parser("migrate", help="迁移项目状态 Schema")
    migrate_parser.add_argument("--project", required=True)
    migrate_parser.set_defaults(handler=command_migrate)

    doctor_parser = subparsers.add_parser("doctor", help="检查 Skill 包和项目环境")
    doctor_parser.add_argument("--package-root", default=str(PACKAGE_ROOT))
    doctor_parser.add_argument("--project")
    doctor_parser.set_defaults(handler=command_doctor)

    adapter_parser = subparsers.add_parser("render-adapter", help="生成平台项目入口")
    adapter_parser.add_argument("--platform", required=True, choices=("codex", "claude-code", "cursor"))
    adapter_parser.add_argument("--project", required=True)
    adapter_parser.set_defaults(handler=command_render_adapter)

    git_parser = subparsers.add_parser("git-policy", help="检查 Git 动作是否满足自动执行条件")
    git_parser.add_argument("--project", required=True)
    git_parser.add_argument(
        "--action",
        required=True,
        choices=(
            "git_init",
            "create_branch",
            "local_commit",
            "push_own_branch",
            "create_draft_pr",
            "force_push",
            "rewrite_history",
            "delete_remote_branch",
            "ready_pr",
            "merge",
            "release",
        ),
    )
    git_parser.add_argument(
        "--authenticated",
        action="store_true",
        help="调用方已通过独立工具确认远端身份有效",
    )
    git_parser.set_defaults(handler=command_git_policy)

    package_parser = subparsers.add_parser("validate-package", help="执行发布前全包静态校验")
    package_parser.add_argument("--package-root", default=str(PACKAGE_ROOT))
    package_parser.set_defaults(handler=command_validate_package)
    return parser


def main() -> int:
    configure_utf8_output()
    try:
        args = build_parser().parse_args()
        return int(args.handler(args))
    except (OSError, ValueError) as exc:
        print(f"执行失败：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
