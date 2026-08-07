# Project Level Workflow Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一套中文、可公开分发、兼容 Codex、Claude Code 与 Cursor 的三级项目开发流程 Skill，使 Agent 能自动推进低风险工作并在人工 Gate 停止。

**Architecture:** 以根目录 `SKILL.md` 作为路由和执行状态机，复用三份现有 LEVEL Markdown 作为唯一权威 SOP。Python 标准库脚本负责确定性的状态、校验、迁移、Doctor 和适配器渲染；PowerShell/Bash 脚本负责安装、升级和卸载；所有 Agent 通过项目内 `.project-workflow/state.json` 和 `docs/project-workflow/STATUS.md` 恢复流程。

**Tech Stack:** Markdown、Agent Skills `SKILL.md`、Python 3.10+ 标准库、JSON Schema、PowerShell、POSIX Shell、Git/GitHub Draft PR。

## Global Constraints

- 首版所有用户可见说明、模板和错误消息使用中文；命令、字段和专有名词保留原文。
- `LEVEL1-小型项目开发流程.md`、`LEVEL2-已有与开源项目改进流程.md`、`LEVEL3-持续运营产品开发流程.md` 是唯一权威 SOP，不复制三份正文。
- Qima 只能作为条件提醒，不得由本 Skill 自动调用。
- R1/R2 可在已批准范围内自动执行；R3/R4 必须停在人工 Gate。
- 公开包默认设置 `allow_push_own_branch=false`、`allow_create_draft_pr=false`；用户个人配置可以显式开启。
- 禁止 Force Push、改写公共历史、提交用户无关修改、自动生产发布和自动公开宣传。
- 当前工作区不是 Git 仓库。执行计划期间不得自动运行 `git init`；文件和测试完成后，在 Task 10 单独请求用户批准。
- 不引入第三方 Python 依赖；核心命令必须可离线运行。
- 不在公共文件、状态、测试夹具或日志中写入真实密钥、Token、个人绝对路径和用户数据。
- 每个任务先写失败测试，再实现最小内容，最后运行当前任务测试和完整回归。

---

## File Map

### Existing canonical files

- `LEVEL1-小型项目开发流程.md`：LEVEL 1 SOP。
- `LEVEL2-已有与开源项目改进流程.md`：LEVEL 2 SOP。
- `LEVEL3-持续运营产品开发流程.md`：LEVEL 3 SOP。
- `docs/superpowers/specs/2026-08-07-project-level-workflow-design.md`：已批准设计规格。

### New public package files

- `SKILL.md`：触发、LEVEL 路由、状态恢复、自动循环和 Gate。
- `README.md`：安装、使用、权限、兼容和故障排查。
- `VERSION`、`CHANGELOG.md`、`LICENSE`、`.gitignore`：公开发布元数据。
- `references/*.md`：LEVEL 选择、风险权限、状态协议、工具路由和平台差异。
- `templates/**`：按 LEVEL 创建项目文档。
- `schemas/workflow-state.schema.json`：状态格式合同。
- `scripts/workflow.py`：确定性 CLI。
- `scripts/install.*`、`scripts/update.*`、`scripts/uninstall.*`：跨平台生命周期脚本。
- `adapters/**`：Codex、Claude Code 和 Cursor 的项目入口模板。
- `evals/evals.json`：真实触发与行为用例。
- `tests/**`：静态、状态、适配器、安装和 Git 策略测试。

---

### Task 1: 建立公开仓库骨架与静态合同

**Files:**
- Create: `tests/test_repository_contract.py`
- Create: `README.md`
- Create: `VERSION`
- Create: `CHANGELOG.md`
- Create: `LICENSE`
- Create: `.gitignore`

**Interfaces:**
- Consumes: 三份根目录 LEVEL SOP 和已批准设计规格。
- Produces: 后续任务共用的仓库文件合同与版本 `0.1.0`。

- [ ] **Step 1: 写仓库合同失败测试**

创建 `tests/test_repository_contract.py`：

```python
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_canonical_level_docs_exist(self):
        expected = [
            "LEVEL1-小型项目开发流程.md",
            "LEVEL2-已有与开源项目改进流程.md",
            "LEVEL3-持续运营产品开发流程.md",
        ]
        for relative in expected:
            self.assertTrue((ROOT / relative).is_file(), relative)

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


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m unittest tests.test_repository_contract -v`

Expected: `test_public_metadata_exists` 和 `test_version_is_semver` 因文件不存在而失败。

- [ ] **Step 3: 创建最小公开元数据**

写入：

- `VERSION`：单行 `0.1.0`。
- `CHANGELOG.md`：包含 `# Changelog`、`## [0.1.0] - 2026-08-07` 和“建立三级开发流程 Skill 首版”。
- `LICENSE`：MIT License，版权主体写 `project-level-workflow contributors`。
- `.gitignore`：忽略 `__pycache__/`、`*.pyc`、`.venv/`、`.pytest_cache/`、测试临时目录和本地私有配置；不得忽略三份 SOP、模板、Schema、Adapter 或 Eval。
- `README.md`：包含定位、三级流程、兼容平台、快速开始、权限默认值、安装入口、升级卸载、状态目录、Qima 边界和许可证。

- [ ] **Step 4: 运行仓库合同测试**

Run: `python -m unittest tests.test_repository_contract -v`

Expected: 全部通过。

- [ ] **Step 5: 保存非 Git 检查点**

Run: `Get-FileHash -Algorithm SHA256 README.md VERSION CHANGELOG.md LICENSE`

Expected: 四个文件均输出 SHA256；当前不创建 Git 提交。

### Task 2: 创建核心 `SKILL.md` 与按需参考文档

**Files:**
- Create: `SKILL.md`
- Create: `references/level-selection.md`
- Create: `references/risk-and-permissions.md`
- Create: `references/state-protocol.md`
- Create: `references/tool-routing.md`
- Create: `references/platform-compatibility.md`
- Modify: `tests/test_repository_contract.py`

**Interfaces:**
- Consumes: 根目录三份 SOP、设计规格、版本 `0.1.0`。
- Produces: `project-level-workflow` 触发器、LEVEL 选择协议和跨平台公共规则。

- [ ] **Step 1: 扩展失败测试**

在 `RepositoryContractTests` 中增加：

```python
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
        ]:
            self.assertTrue((ROOT / relative).is_file(), relative)
            self.assertIn(relative, skill)

    def test_qima_is_reminder_only(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Qima", skill)
        self.assertIn("不得直接调用", skill)
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m unittest tests.test_repository_contract -v`

Expected: 因 `SKILL.md` 和 `references/` 不存在而失败。

- [ ] **Step 3: 创建 `SKILL.md`**

Frontmatter 必须为：

```yaml
---
name: project-level-workflow
description: 当用户要开发新项目、改进已有或开源项目、建设长期运营产品、判断项目 LEVEL、按标准流程推进，或继续到下一个人工 Gate 时使用。根据风险推荐 LEVEL 1/2/3，确认后自动推进低风险工作并保存证据；纯问答、只读审查、单纯诊断和 Skill 创建请求不触发。
compatibility: Codex、Claude Code、Cursor；核心脚本需要 Python 3.10+，安装器支持 PowerShell 或 POSIX Shell。
---
```

正文按以下固定顺序编写：触发检查、恢复现有状态、推荐并确认 LEVEL、读取单一 LEVEL SOP、初始化项目文档、风险分类、低风险自动循环、验证与 Git、人工 Gate 报告、平台降级、禁止事项。明确引用五份 `references/`，并保证不会同时加载三份 LEVEL SOP。

- [ ] **Step 4: 创建五份参考文档**

- `level-selection.md`：LEVEL 1/2/3 判定表、升级条件、冲突时优先按风险升级、首次选择必须人工确认。
- `risk-and-permissions.md`：R1～R4、Git 权限、远程配置、外部写入和人工 Gate。
- `state-protocol.md`：状态字段、原子写入、恢复、冲突和 `STATUS.md` 格式。
- `tool-routing.md`：Product Design、Supabase、GitHub、Vercel/Netlify、Qima 与降级策略。
- `platform-compatibility.md`：Codex、Claude Code、Cursor 的入口、差异和共同限制。

每份文档开头写明“何时读取”，并只引用根目录 SOP，不复制 SOP 全文。

- [ ] **Step 5: 运行测试与行数检查**

Run: `python -m unittest tests.test_repository_contract -v`

Run: `(Get-Content -Encoding utf8 SKILL.md).Count`

Expected: 测试通过；`SKILL.md` 少于 500 行。

### Task 3: 创建 LEVEL 文档模板包

**Files:**
- Create: `templates/common/status.md`
- Create: `templates/common/gate-report.md`
- Create: `templates/common/acceptance-report.md`
- Create: `templates/level1/project-brief.md`
- Create: `templates/level2/project-map.md`
- Create: `templates/level2/change-proposal.md`
- Create: `templates/level3/idea-review.md`
- Create: `templates/level3/prd.md`
- Create: `templates/level3/tech-spec.md`
- Create: `templates/level3/task.md`
- Create: `templates/level3/deploy-readiness.md`
- Create: `templates/level3/rollback-plan.md`
- Create: `tests/test_templates.py`

**Interfaces:**
- Consumes: 三份 LEVEL SOP 的最小文档包和 Gate 要求。
- Produces: Agent 可复制并填写的中文模板，不包含作者内部制作说明。

- [ ] **Step 1: 写模板失败测试**

创建 `tests/test_templates.py`，逐一断言上述十二个模板存在、UTF-8 可读、不包含未完成占位标记，并断言：

```python
required_sections = {
    "templates/level1/project-brief.md": ["目标用户", "核心路径", "本次不做", "验收标准"],
    "templates/level2/change-proposal.md": ["当前行为", "期望行为", "影响范围", "回归范围"],
    "templates/level3/prd.md": ["目标用户", "MVP", "不做清单", "验收标准", "成功指标"],
    "templates/common/gate-report.md": ["已确认事实", "验证证据", "风险", "推荐决策", "等待批准"],
}
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m unittest tests.test_templates -v`

Expected: 模板缺失失败。

- [ ] **Step 3: 创建模板**

每个模板使用固定 Markdown 标题和可删除的填写提示。提示写成 HTML 注释，避免进入最终公开正文。所有模板包含“状态、负责人、关联 Gate、最后更新时间”；LEVEL 3 技术模板明确前后端共享 API Contract、迁移、备份、监控和回滚。

- [ ] **Step 4: 运行模板和完整回归**

Run: `python -m unittest tests.test_templates tests.test_repository_contract -v`

Expected: 全部通过。

### Task 4: 实现状态 Schema、初始化与校验

**Files:**
- Create: `schemas/workflow-state.schema.json`
- Create: `scripts/workflow.py`
- Create: `tests/test_workflow_state.py`

**Interfaces:**
- Consumes: `references/state-protocol.md`、`VERSION`。
- Produces: `python scripts/workflow.py init|validate --project <path>`。

- [ ] **Step 1: 写 CLI 失败测试**

创建 `tests/test_workflow_state.py`，使用 `tempfile.TemporaryDirectory` 和 `subprocess.run` 验证：

```python
def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts/workflow.py"), *args],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
```

测试以下行为：

- `init --project <tmp> --level 1` 创建 `.project-workflow/state.json`、备份和 `docs/project-workflow/STATUS.md`。
- 初始远程权限均为 `false`。
- `validate` 对有效状态返回 0。
- 缺少必填字段、非法 LEVEL、状态中包含绝对路径时返回非 0 和中文错误。
- 第二次 `init` 不覆盖现有状态，除非显式 `--force`；`--force` 仍先生成备份。

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m unittest tests.test_workflow_state -v`

Expected: `scripts/workflow.py` 不存在导致失败。

- [ ] **Step 3: 创建 JSON Schema**

Schema 必须要求：`schema_version`、`workflow_version`、`project_id`、`level`、`stage`、`gate`、`status`、`risk`、`permissions`、`current_task`、`artifacts`、`verifications`、`git`、`remote`、`history`、`updated_at`。`level` 只允许 `1|2|3`，`risk` 只允许 `R1|R2|R3|R4`，远程权限默认 `false`。

- [ ] **Step 4: 实现最小 CLI**

`scripts/workflow.py` 使用 `argparse`，实现以下公开合同：

- `utc_now() -> str`：返回 UTC、带 `Z` 后缀的 ISO 8601 时间。
- `load_version() -> str`：读取根目录 `VERSION`，缺失或非 SemVer 时抛出可读错误。
- `atomic_write_json(path: Path, data: dict) -> None`：写入同目录临时文件，UTF-8、缩进 2、末尾换行，成功校验后用 `Path.replace` 原子替换。
- `build_initial_state(project: Path, level: int) -> dict`：生成 Schema 所需全部字段，远程权限固定初始化为 `false`。
- `validate_state(data: dict, project: Path) -> list[str]`：返回全部中文校验错误；无错误时返回空列表。
- `command_init(args: argparse.Namespace) -> int`：创建状态、备份和摘要；成功返回 0，冲突返回 2，输入错误返回 1。
- `command_validate(args: argparse.Namespace) -> int`：输出逐项结果；有效返回 0，无效返回 1。
- `build_parser() -> argparse.ArgumentParser`：注册 `init` 与 `validate` 以及本计划后续命令。
- `main() -> int`：分发命令并把预期错误转换成中文消息和稳定退出码。

不依赖第三方 JSON Schema 库；运行时校验由 Python 明确检查必填字段、枚举、类型、相对路径和敏感字段，Schema 文件作为公共合同。

- [ ] **Step 5: 运行状态测试与完整回归**

Run: `python -m unittest tests.test_workflow_state -v`

Run: `python -m unittest discover -s tests -v`

Expected: 全部通过。

### Task 5: 实现状态摘要、转换、迁移和 Doctor

**Files:**
- Modify: `scripts/workflow.py`
- Modify: `tests/test_workflow_state.py`
- Create: `tests/test_doctor.py`

**Interfaces:**
- Consumes: Task 4 的有效状态。
- Produces: `status`、`transition`、`migrate`、`doctor` 命令。

- [ ] **Step 1: 写失败测试**

覆盖：

- `status` 根据状态生成固定七段 `STATUS.md`。
- `transition --approve-gate G1 --to-stage design` 只在 Gate 名称匹配时执行，并追加历史记录。
- 未提供批准信息时不得跨 Gate。
- `migrate` 从受支持旧 Schema 备份后升级；未知新版本拒绝降级。
- `doctor` 检查 Python、Git、三份 SOP、Skill、Schema、状态和平台入口，输出逐项中文 PASS/FAIL，任一必需项失败时退出非 0。

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m unittest tests.test_workflow_state tests.test_doctor -v`

Expected: 新命令未实现失败。

- [ ] **Step 3: 实现命令**

增加以下公开合同：

- `render_status(data: dict) -> str`：按固定七段结构返回 Markdown，所有列表顺序稳定。
- `command_status(args: argparse.Namespace) -> int`：验证状态后原子刷新 `STATUS.md`。
- `command_transition(args: argparse.Namespace) -> int`：验证当前 Gate、批准信息和目标阶段后更新状态与历史。
- `command_migrate(args: argparse.Namespace) -> int`：只执行已登记的向前迁移，写入前备份。
- `command_doctor(args: argparse.Namespace) -> int`：检查运行时、Git、公共文件、状态和适配器并返回统一退出码。

`transition` 每次先验证当前状态、Gate、目标阶段和批准人字段，再备份并原子写入；不得通过自由文本目标跳过 Gate。

- [ ] **Step 4: 运行回归**

Run: `python -m unittest discover -s tests -v`

Expected: 全部通过。

### Task 6: 实现三平台适配器与项目规则渲染

**Files:**
- Create: `adapters/codex/AGENTS.fragment.md`
- Create: `adapters/claude-code/CLAUDE.fragment.md`
- Create: `adapters/cursor/project-level-workflow.mdc`
- Modify: `scripts/workflow.py`
- Create: `tests/test_adapters.py`

**Interfaces:**
- Consumes: 当前 LEVEL、状态目录、根目录 SOP。
- Produces: `render-adapter --platform codex|claude-code|cursor --project <path>`。

- [ ] **Step 1: 写适配器失败测试**

验证：

- Codex 输出项目 `AGENTS.md` 片段，引用当前 LEVEL SOP 和状态。
- Claude Code 输出 `CLAUDE.md` 片段，不复制 SOP。
- Cursor 输出 `.cursor/rules/project-level-workflow.mdc`，包含合法 frontmatter、`alwaysApply: false` 和中文 description。
- 重复运行幂等，不重复插入托管区块。
- 已存在用户文件时只替换带 `project-level-workflow:start/end` 标记的托管区块。
- 未识别平台返回非 0。

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m unittest tests.test_adapters -v`

Expected: 适配器和命令缺失失败。

- [ ] **Step 3: 创建适配器模板并实现渲染**

三个模板只包含项目入口、当前 LEVEL、权威文档、状态路径、验证命令、风险与 Gate；不得复制完整流程。`workflow.py` 增加 `render_adapter` 和托管区块替换函数，写入前备份用户文件。

- [ ] **Step 4: 运行回归**

Run: `python -m unittest discover -s tests -v`

Expected: 全部通过。

### Task 7: 实现安装、升级与卸载

**Files:**
- Create: `scripts/install.ps1`
- Create: `scripts/install.sh`
- Create: `scripts/update.ps1`
- Create: `scripts/update.sh`
- Create: `scripts/uninstall.ps1`
- Create: `scripts/uninstall.sh`
- Create: `tests/test_lifecycle_scripts.py`
- Modify: `README.md`

**Interfaces:**
- Consumes: 完整 Skill 包和平台目标。
- Produces: Codex、Claude Code、Cursor 的可预览安装生命周期。

- [ ] **Step 1: 写生命周期脚本静态失败测试**

检查六个脚本存在，并包含：

- `--dry-run` 或等价参数。
- 目标路径解析和“目标必须位于用户明确选择的 Skill/项目目录”检查。
- 版本比较、冲突文件停止、备份和中文错误。
- 卸载默认保留 `.project-workflow/` 与 `docs/project-workflow/`。
- PowerShell 不使用跨 Shell 的递归删除或字符串拼接命令。
- Shell 脚本启用严格模式并为路径加引号。

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m unittest tests.test_lifecycle_scripts -v`

Expected: 脚本缺失失败。

- [ ] **Step 3: 实现 PowerShell 和 Shell 脚本**

安装器参数统一表达：平台、作用域、目标项目、Dry Run。Codex/Claude 可安装个人或项目 Skill；Cursor 只渲染项目 Rule。更新器先运行 Doctor 和状态迁移；卸载器只依据安装清单删除托管文件。

- [ ] **Step 4: 更新 README**

添加 Windows、macOS/Linux/WSL 的安装、Dry Run、升级、卸载和回滚示例。明确公网一键命令需要用户自行审查下载内容，README 优先推荐 Clone/Release 后本地执行。

- [ ] **Step 5: 运行回归**

Run: `python -m unittest discover -s tests -v`

Expected: 全部通过；若当前环境有 `bash`，额外运行 `bash -n scripts/install.sh scripts/update.sh scripts/uninstall.sh` 并要求退出 0。

### Task 8: 固化 Git 与 Draft PR 安全策略

**Files:**
- Create: `references/git-and-draft-pr.md`
- Modify: `SKILL.md`
- Modify: `scripts/workflow.py`
- Create: `tests/test_git_policy.py`

**Interfaces:**
- Consumes: 用户权限配置、当前 Git 状态和当前任务范围。
- Produces: 只读 Git 检查、是否允许自动本地提交/Push/Draft PR 的确定性判断。

- [ ] **Step 1: 写 Git 策略失败测试**

在临时 Git 仓库覆盖：

- 非 Git 目录返回 `needs_git_init_approval`。
- 脏工作区包含非任务文件时返回 `blocked_by_user_changes`。
- 仅 Skill 创建分支、验证通过且权限开启时允许 Push。
- Draft PR 还要求配置 GitHub Remote 和可用认证；测试使用模拟结果，不写真实 GitHub。
- Force Push、主分支直推、删除远程分支、Ready、Merge、Release 永远不返回自动允许。

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m unittest tests.test_git_policy -v`

Expected: 策略函数不存在失败。

- [ ] **Step 3: 实现只读检查与策略函数**

`workflow.py` 增加两个公开合同：

- `inspect_git(project: Path) -> dict`：只运行只读 Git 命令，返回是否为仓库、当前分支、默认分支、脏文件、Remote 和认证可用性摘要；不修改 Git 状态。
- `evaluate_git_action(state: dict, git_info: dict, action: str) -> tuple[bool, str]`：对 `local_commit`、`push_own_branch`、`create_draft_pr`、`ready_pr`、`merge`、`release` 等动作返回布尔值和中文原因；后三项及其他高影响动作始终返回 false。

函数只判断，不执行 Push、PR、Merge 或 Release。Agent 根据返回结果行动，所有真实远程写入仍由平台权限系统控制。

- [ ] **Step 4: 创建 Git 参考并连接 `SKILL.md`**

文档写明分支命名、验证后提交、提交范围、Push/Draft PR 前置条件、失败回退和绝对禁止项。

- [ ] **Step 5: 运行回归**

Run: `python -m unittest discover -s tests -v`

Expected: 全部通过。

### Task 9: 创建场景评测与全包验证

**Files:**
- Create: `evals/evals.json`
- Create: `tests/test_evals.py`
- Create: `tests/test_package_validation.py`
- Modify: `scripts/workflow.py`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: 完整 Skill、SOP、模板、状态引擎和适配器。
- Produces: 可重复的 v1 验收证据。

- [ ] **Step 1: 写 Eval 合同失败测试**

要求 `evals/evals.json` 至少包含十个设计规格中的场景，每项包含 `id`、`prompt`、`expected_output`、`files`。额外断言正向触发覆盖三个 LEVEL，负向触发包含 Skill 创建、纯解释和只读 Review。

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m unittest tests.test_evals tests.test_package_validation -v`

Expected: Eval 和全包验证文件缺失失败。

- [ ] **Step 3: 创建 Evals 与全包检查**

`test_package_validation.py` 必须检查：

- 所有公共 Markdown 为 UTF-8，标题和表格闭合。
- 所有相对引用存在。
- 没有个人绝对路径、密钥模式和占位符。
- `SKILL.md` 少于 500 行。
- Qima 只有提醒边界。
- 公开远程权限默认为 false。
- 三平台适配器使用同一三份 SOP。
- `VERSION`、Schema、状态与 Changelog 版本一致。

同时在 `workflow.py` 注册 `validate-package --package-root <path>`，复用上述确定性检查并输出逐项中文结果；全部通过返回 0，任一失败返回 1。

- [ ] **Step 4: 更新 Changelog 并运行完整测试**

Run: `python -m unittest discover -s tests -v`

Expected: 0 failure、0 error。

- [ ] **Step 5: 运行三个轻量手工评测**

依次用以下提示词运行 Skill，并保存输出供用户审阅：

1. “帮我做一个不需要数据库的静态网页小工具，先判断 LEVEL 并推进到下一个人工 Gate。”
2. “帮我修复这个已有 GitHub 项目的一个 Bug，先理解仓库再推进。”
3. “我要开发一个长期运营的 SaaS，请按严格流程从调研开始。”

Expected: 分别推荐 LEVEL 1、2、3；未获确认时不越过首次 LEVEL Gate。

### Task 10: 最终验证、Git 初始化 Gate 与发布准备

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Create: `docs/release/0.1.0-readiness.md`

**Interfaces:**
- Consumes: Task 1～9 的全部产物和测试证据。
- Produces: 可供用户批准 Git 初始化和首次 GitHub 发布的 Release Readiness。

- [ ] **Step 1: 运行最终验证**

Run: `python scripts/workflow.py doctor --package-root .`

Run: `python -m unittest discover -s tests -v`

Run: `python scripts/workflow.py validate-package --package-root .`

Expected: 三个命令退出 0；测试输出 0 failure、0 error。

- [ ] **Step 2: 生成 Release Readiness**

记录版本、文件清单、测试命令和结果、三平台安装检查、已知限制、远程权限默认值、回滚方式和未执行检查。不得把未执行的 macOS/Linux 实机测试写成通过。

- [ ] **Step 3: 请求 Git 初始化批准**

向用户展示当前目录、计划创建的 `.git`、默认分支名、首个提交文件范围和建议仓库名称 `project-level-workflow`。只有用户批准后才运行 `git init`。

- [ ] **Step 4: 经批准后创建本地 Git 历史**

Run: `git init -b main`

Run: `git add -- SKILL.md LEVEL1-小型项目开发流程.md LEVEL2-已有与开源项目改进流程.md LEVEL3-持续运营产品开发流程.md README.md VERSION CHANGELOG.md LICENSE .gitignore references templates schemas scripts adapters evals tests docs`

Run: `git commit -m "feat: add project level workflow skill"`

Expected: 创建一个聚焦的首个提交，不包含工作区外文件、密钥或临时产物。

- [ ] **Step 5: 停在 GitHub 发布 Gate**

展示建议 Remote、仓库可见性、Draft Release Notes 和将要 Push 的分支。未经用户确认，不创建 GitHub 仓库、不添加 Remote、不 Push、不发布 Release。

---

## Plan Self-Review Checklist

- [ ] 设计规格中的 v1 范围均有对应 Task。
- [ ] 没有未完成占位词、空函数体或未定义步骤。
- [ ] `state.json` 字段、命令名、版本和路径在各 Task 中一致。
- [ ] 三份 LEVEL SOP 始终是唯一权威流程源。
- [ ] 公开包默认远程权限关闭，个人启用不改变公共默认。
- [ ] 当前非 Git 工作区不会被计划执行器擅自初始化。
- [ ] 所有完成声明都由新鲜测试、Doctor 和包验证支持。
