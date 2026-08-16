# Project Level Workflow 1.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 v0.4.0 改造成以 LEVEL 1/2 为核心、文档记忆完整、前三个等级低审批、LEVEL 4 外部路由、GitHub 插件自动交付和两段版本号的 1.0。

**Architecture:** 保留根 `SKILL.md`、唯一 `LEVEL.md`、包内 PVS 和现有状态 CLI。通过新的文档契约、个人执行策略、GitHub 路由和 LEVEL 4 能力矩阵分离核心治理与外部能力；用 Schema 2.0 和兼容迁移承载行为变化，不删除旧模板。

**Tech Stack:** Markdown Skill contract、Python 3.10+ 标准库 CLI、JSON Schema、PowerShell/POSIX 生命周期脚本、`unittest`、Codex GitHub 插件。

## Global Constraints

- 实施基线必须是 GitHub `v0.4.0` 或与其树一致的 `main`，不得在本机旧 `0.3.0` 分支直接修改。
- 公共版本固定为 `1.0`，后续只使用 `X.X`；Tag 为 `v1.0`；Schema 为 `2.0`。
- LEVEL 1–4 都需要负责人显式确认；LEVEL 1 未确认前不得写入项目。
- LEVEL 1/2 必须保留稳定认知层和演进记录层；小改动也必须留下结构化记录。
- LEVEL 2 全量采用包内 PVS 和 Phase 0 → Phase N，但普通 Phase 完成不是 Gate。
- LEVEL 4 的专业 Skill 仅路由、提醒和经确认安装，不内嵌第二个 Skill。
- GitHub 交付自动选择 Codex GitHub 插件；远程写入、Merge、Tag、Release 前仍需一次明确确认。
- 不批量删除旧模板、用户文档或兼容入口；不覆盖用户已有等价事实源。
- Force Push 和改写公共历史继续禁止。

---

### Task 1: 建立干净的 v0.4.0 实施基线

**Files:**
- Read: all files at repository root
- Verify: `docs/release/0.4.0-readiness.md`
- Create during execution: isolated worktree branch `codex/personal-first-workflow-1-0`

**Interfaces:**
- Consumes: GitHub tag `v0.4.0`, remote `main`, clean local Git repository.
- Produces: a clean worktree whose `HEAD` tree equals the approved 0.4.0 baseline.

- [ ] **Step 1: Fetch and compare the authoritative refs**

```powershell
git fetch origin main --tags
git rev-parse v0.4.0^{commit}
git rev-parse origin/main^{commit}
git diff --stat v0.4.0..origin/main
```

Expected: refs resolve. If the diff is non-empty, stop and review post-release changes before choosing the base.

- [ ] **Step 2: Create the isolated implementation worktree**

```powershell
git worktree add -b codex/personal-first-workflow-1-0 D:\VibeCoding-Project\project-level-workflow-1.0-worktree v0.4.0
git -C D:\VibeCoding-Project\project-level-workflow-1.0-worktree status --short
```

Expected: empty status on `codex/personal-first-workflow-1-0`.

- [ ] **Step 3: Copy the approved spec and plan into the worktree**

Copy exactly:

```text
docs/superpowers/specs/2026-08-16-personal-first-workflow-1-0-design.md
docs/superpowers/plans/2026-08-16-personal-first-workflow-1-0.md
```

- [ ] **Step 4: Run the untouched baseline**

```powershell
python -m unittest discover -s tests -v
python scripts/workflow.py doctor --package-root .
python scripts/workflow.py validate-package --package-root .
```

Expected: existing 0.4.0 tests and both validators pass. Record any environment-only skips separately.

- [ ] **Step 5: Commit the approved design artifacts**

```powershell
git add docs/superpowers/specs/2026-08-16-personal-first-workflow-1-0-design.md docs/superpowers/plans/2026-08-16-personal-first-workflow-1-0.md
git commit -m "docs: approve personal-first workflow 1.0 design"
```

### Task 2: 实现两段版本和 Schema 2.0 迁移

**Files:**
- Modify: `VERSION`
- Modify: `scripts/workflow.py`
- Modify: `schemas/workflow-state.schema.json`
- Modify: `tests/test_repository_contract.py`
- Modify: `tests/test_package_validation.py`
- Modify: `tests/test_workflow_state.py`
- Modify: `tests/test_lifecycle_scripts.py`

**Interfaces:**
- Produces: `PUBLIC_VERSION = ^\d+\.\d+$`, schema `2.0`, migration from `0.9.0`, `1.0.0`, `1.1.0`, and workflow refresh from historical `0.4.0` to `1.0` without making the old state unreadable.

- [ ] **Step 1: Make the public-version contract fail first**

Replace the SemVer test with:

```python
def test_version_uses_two_numeric_segments(self):
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    self.assertRegex(version, re.compile(r"^\d+\.\d+$"))
    self.assertEqual(version, "1.0")
```

Add a package validation test that writes `1.0.0` into a copied package and expects the error text `两段版本`.

- [ ] **Step 2: Run the targeted tests and observe failure**

```powershell
python -m unittest tests.test_repository_contract tests.test_package_validation -v
```

Expected: FAIL because `VERSION` is `0.4.0` and the validator accepts three segments.

- [ ] **Step 3: Implement the two-part parser and constants**

Use these exact public constants in `workflow.py`:

```python
SCHEMA_VERSION = "2.0"
LEGACY_SCHEMA_VERSIONS = {"0.9.0", "1.0.0", "1.1.0"}
TWO_PART_VERSION = re.compile(r"^\d+\.\d+$")
LEGACY_THREE_PART_VERSION = re.compile(r"^\d+\.\d+\.\d+$")
```

`load_version()` and `validate_package()` must accept only `TWO_PART_VERSION` and report `两段版本（X.X）`. State reading/migration must temporarily accept either two-part values or `LEGACY_THREE_PART_VERSION`, so an installed 0.4.0 state can reach `status`/`migrate` and be refreshed safely. Set `VERSION` to `1.0`; set Schema `schema_version.const` to `2.0` and `workflow_version.const` to `1.0`.

- [ ] **Step 4: Add migration assertions**

Add a state test that starts from schema `1.1.0`, workflow `0.4.0`, LEVEL 4, stage `requirements-analysis`; after `migrate`, assert:

```python
self.assertEqual(current["schema_version"], "2.0")
self.assertEqual(current["workflow_version"], "1.0")
self.assertEqual(current["level"], 4)
self.assertEqual(current["stage"], "requirements-analysis")
self.assertEqual(current["gate"], "level4-execution-review")
self.assertEqual(current["status"], "waiting_approval")
```

For LEVEL 1–3 migration, assert the level stays unchanged and no additional semantic-review Gate is introduced.

- [ ] **Step 5: Run migration and lifecycle tests**

```powershell
python -m unittest tests.test_workflow_state tests.test_lifecycle_scripts tests.test_repository_contract tests.test_package_validation -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```powershell
git add VERSION scripts/workflow.py schemas/workflow-state.schema.json tests/test_repository_contract.py tests/test_package_validation.py tests/test_workflow_state.py tests/test_lifecycle_scripts.py
git commit -m "feat: adopt two-part workflow version 1.0"
```

### Task 3: 建立大文档与小记录模板契约

**Files:**
- Create: `references/documentation-contract.md`
- Create: `templates/common/change-record.md`
- Create: `templates/common/release-record.md`
- Create: `templates/level1/architecture.md`
- Create: `templates/level1/progress-record.md`
- Modify: `templates/level1/project-brief.md`
- Modify: `templates/template-map.json`
- Modify: `tests/test_templates.py`
- Modify: `tests/test_embedded_pvs.py`

**Interfaces:**
- Produces: stable-knowledge roles and append-only evolution roles that map to existing PVS starter paths without creating a second truth source.

- [ ] **Step 1: Add failing template-contract tests**

Extend `TEMPLATES` with the five new template paths. Add:

```python
def test_personal_project_memory_templates_cover_handoff_and_history(self):
    required = {
        "templates/level1/architecture.md": ["模块", "调用关系", "数据", "构建与交付"],
        "templates/level1/progress-record.md": ["目标", "涉及文件", "行为变化", "验证", "兼容影响"],
        "templates/common/change-record.md": ["范围", "不做", "旧行为", "新行为", "验证"],
        "templates/common/release-record.md": ["版本", "提交", "变更", "验证", "已知限制"],
    }
    for relative, sections in required.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for section in sections:
            self.assertIn(section, text, f"{relative}: {section}")
```

- [ ] **Step 2: Run the template test and observe missing files**

```powershell
python -m unittest tests.test_templates -v
```

Expected: FAIL for missing templates.

- [ ] **Step 3: Create the exact template responsibilities**

Write templates that implement the approved design contract:

```text
architecture.md      = current modules, calls, data, dependencies, build/delivery, compatibility boundaries
progress-record.md   = one small feature/fix with files, behavior, verification, compatibility
change-record.md     = reusable scoped before/after record
release-record.md    = immutable version/commit/remote evidence record
```

Update `project-brief.md` with scope freeze and document-entry fields. Add template-map roles `project_architecture`, `change_record`, `release_record`, and `level1_progress_record`; reuse PVS Requirements/Decisions/Progress ledgers as defaults where applicable.

- [ ] **Step 4: Verify templates and PVS mapping**

```powershell
python -m unittest tests.test_templates tests.test_embedded_pvs -v
```

Expected: PASS and no nested `SKILL.md`.

- [ ] **Step 5: Commit**

```powershell
git add references/documentation-contract.md templates tests/test_templates.py tests/test_embedded_pvs.py
git commit -m "feat: add durable project memory contract"
```

### Task 4: 重写四级权威流程和 PVS Bridge

**Files:**
- Modify: `SKILL.md`
- Modify: `LEVEL.md`
- Modify: `references/level-selection.md`
- Modify: `references/project-vibe-spec-bridge.md`
- Create: `references/personal-execution-loop.md`
- Modify: `references/risk-and-permissions.md`
- Modify: `tests/test_repository_contract.py`

**Interfaces:**
- Produces: explicit LEVEL confirmation for all levels; L1 memory-first loop; L2 full PVS/Phase; L3 reuse-first change flow; L4 analysis-then-execution routing.

- [ ] **Step 1: Change the expected headings and contracts first**

In `test_repository_contract.py`, assert these headings:

```python
headings = (
    "## LEVEL 1：快速开发与完整项目记忆",
    "## LEVEL 2：完整 PVS 持续运营",
    "## LEVEL 3：已有、团队与开源项目改进",
    "## LEVEL 4：复杂自动化参考与路由",
)
```

Also assert `SKILL.md` contains `用户明确确认前` for LEVEL 1, `AUTO`/`CONFIRM`/`MANUAL_ONLY`, and references the new documentation contract and personal execution loop.

- [ ] **Step 2: Run the repository contract test and observe failure**

```powershell
python -m unittest tests.test_repository_contract -v
```

Expected: FAIL on old headings and missing references.

- [ ] **Step 3: Rewrite LEVEL.md as the single authority**

Implement the exact flows, default documents, record granularity and Gate boundaries from the approved design. Preserve the old numeric migration history in a compatibility section; do not retain “LEVEL 4 永久只分析”.

- [ ] **Step 4: Rewrite the Bridge and execution policy**

Define:

```text
L1 = PVS traceability core + durable memory, light execution
L2 = full PVS + Phase 0 → N, no automatic phase-approval gate
L3 = repository facts first + change/regression/handoff records
L4 = reference pipeline + external capability routing
```

Keep R1–R4 in state for compatibility, but expose `AUTO`, `CONFIRM`, `MANUAL_ONLY` to L1–L3 users.

- [ ] **Step 5: Run contract tests**

```powershell
python -m unittest tests.test_repository_contract tests.test_templates -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```powershell
git add SKILL.md LEVEL.md references tests/test_repository_contract.py
git commit -m "feat: make levels one through three personal-first"
```

### Task 5: 让 init 和 STATUS 支持分层文档与静默风险

**Files:**
- Modify: `scripts/workflow.py`
- Modify: `references/state-protocol.md`
- Modify: `schemas/workflow-state.schema.json`
- Modify: `tests/test_workflow_state.py`
- Modify: `tests/test_adapters.py`

**Interfaces:**
- Produces: level-aware initial stage, status renderer, LEVEL 4 semantic review, preserved backups and idempotent adapters.

- [ ] **Step 1: Add failing state behavior tests**

Add assertions:

```python
expected_stage = {1: "project-memory", 2: "phase-0", 3: "repository-intake", 4: "requirements-analysis"}
```

For LEVEL 1–3 `STATUS.md`, assert it contains `执行策略` and does not contain an empty `当前人工 Gate` section. For LEVEL 4, assert explicit risk and Gate sections remain.

- [ ] **Step 2: Run tests and observe old fixed rendering**

```powershell
python -m unittest tests.test_workflow_state tests.test_adapters -v
```

Expected: FAIL because all levels currently start at `initialization` and share fixed status sections.

- [ ] **Step 3: Implement level-aware state helpers**

Add exact mappings:

```python
INITIAL_STAGE = {1: "project-memory", 2: "phase-0", 3: "repository-intake", 4: "requirements-analysis"}
DEFAULT_EXECUTION_POLICY = {1: "AUTO", 2: "AUTO", 3: "AUTO", 4: "CONFIRM"}
```

Add `execution_policy` to Schema with enum `AUTO`, `CONFIRM`, `MANUAL_ONLY`. Preserve `risk` for compatibility. Render risk/Gate details always for L4 and only when non-empty/high-impact for L1–3.

- [ ] **Step 4: Update adapters**

Remove LEVEL 4 `只做需求分析` wording. Render the current level heading, bundled PVS boundary, state path and external-routing boundary without copying the workflow.

- [ ] **Step 5: Run state and adapter tests**

```powershell
python -m unittest tests.test_workflow_state tests.test_adapters -v
```

Expected: PASS with backups preserved and adapters idempotent.

- [ ] **Step 6: Commit**

```powershell
git add scripts/workflow.py references/state-protocol.md schemas/workflow-state.schema.json adapters tests/test_workflow_state.py tests/test_adapters.py
git commit -m "feat: add level-aware state and status rendering"
```

### Task 6: 增加 LEVEL 4 外部能力和 GitHub 插件路由

**Files:**
- Create: `references/level4-capability-routing.md`
- Create: `references/github-plugin-routing.md`
- Modify: `references/tool-routing.md`
- Modify: `references/git-and-draft-pr.md`
- Modify: `SKILL.md`
- Modify: `tests/test_repository_contract.py`
- Modify: `tests/test_git_policy.py`
- Modify: `evals/evals.json`

**Interfaces:**
- Produces: installed-first LEVEL 4 routing and mandatory GitHub-plugin delivery routing; remote mutations still require action-time approval.

- [ ] **Step 1: Add routing contract tests**

Assert the two references exist. Assert GitHub routing contains all actions:

```python
for action in ("push", "Draft PR", "Merge", "Tag", "Release"):
    self.assertIn(action, github_routing)
self.assertIn("GitHub 插件", github_routing)
self.assertIn("执行前确认", github_routing)
self.assertIn("远端验证", github_routing)
```

Assert LEVEL 4 routing lists ten nodes and includes `已安装则路由`, `缺失时提醒安装`, `拒绝安装时降级` and `不得内嵌`.

- [ ] **Step 2: Run contract and eval tests and observe failure**

```powershell
python -m unittest tests.test_repository_contract tests.test_evals tests.test_git_policy -v
```

Expected: FAIL for missing references/cases.

- [ ] **Step 3: Write the routing references**

GitHub flow must be exactly:

```text
local verification → plugin availability/auth/repository read → remote action plan
→ one approval → plugin mutation → remote commit/PR/tag/release read-back
→ release record
```

Do not change Force Push/history rewrite from forbidden. Merge and Release remain not auto-allowed by `git-policy`; the policy result must direct the agent to the explicit GitHub approval path instead of suggesting direct local execution.

- [ ] **Step 4: Add eval cases**

Add unique cases for all-level GitHub routing, unavailable plugin, LEVEL 4 installed capability, LEVEL 4 missing capability, install declined, and no nested skill installation.

- [ ] **Step 5: Run routing tests**

```powershell
python -m unittest tests.test_repository_contract tests.test_evals tests.test_git_policy -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```powershell
git add SKILL.md references tests evals/evals.json
git commit -m "feat: route external capabilities and GitHub delivery"
```

### Task 7: 同步公开文档、安装器和发布契约

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `evals/evals.json`
- Modify: `scripts/install.ps1`
- Modify: `scripts/install.sh`
- Modify: `scripts/update.ps1`
- Modify: `scripts/update.sh`
- Modify: `tests/test_install_integration.py`
- Modify: `tests/test_lifecycle_scripts.py`
- Modify: `tests/test_package_validation.py`
- Create: `docs/release/1.0-readiness.md`

**Interfaces:**
- Produces: public 1.0 contract, two-part updater comparisons, install/update preservation, release-readiness evidence template.

- [ ] **Step 1: Add failing lifecycle assertions**

Assert install/update copies the four new references and five new templates, accepts `1.0`, rejects `1.0.0`, preserves an independent PVS installation, and rolls back a failed staged replacement.

- [ ] **Step 2: Run lifecycle tests and observe failure**

```powershell
python -m unittest tests.test_install_integration tests.test_lifecycle_scripts tests.test_package_validation -v
```

Expected: FAIL on new files/version contract.

- [ ] **Step 3: Update public and lifecycle contracts**

README must lead with L1/L2 personal priority, explain big docs + small records, full L2 PVS, lightweight L4 routing, automatic GitHub plugin selection, and `X.X`. CHANGELOG must add `## [1.0] - 2026-08-16`. Readiness must separate executed tests from unexecuted platform checks.

- [ ] **Step 4: Run lifecycle tests**

```powershell
python -m unittest tests.test_install_integration tests.test_lifecycle_scripts tests.test_package_validation -v
```

Expected: PASS; Bash-only runtime checks may remain explicitly unexecuted when Bash is unavailable.

- [ ] **Step 5: Commit**

```powershell
git add README.md CHANGELOG.md evals scripts tests docs/release/1.0-readiness.md
git commit -m "docs: prepare project level workflow 1.0"
```

### Task 8: 全量验证、安装冒烟和交付准备

**Files:**
- Update evidence only: `docs/release/1.0-readiness.md`
- No functional files unless a verified failure requires a scoped fix.

**Interfaces:**
- Produces: reproducible local evidence and a GitHub-plugin release plan; no remote mutation before approval.

- [ ] **Step 1: Run the full suite**

```powershell
python -m unittest discover -s tests -v
python scripts/workflow.py doctor --package-root .
python scripts/workflow.py validate-package --package-root .
```

Expected: all applicable tests pass; skipped checks are named with reasons.

- [ ] **Step 2: Run LEVEL 1–4 smoke projects**

For four temporary projects, run `init`, `validate`, `status`, and all three `render-adapter` platforms. Assert L1 starts `project-memory`, L2 starts `phase-0`, L3 starts `repository-intake`, and L4 starts `requirements-analysis`.

- [ ] **Step 3: Run version and migration smoke tests**

Verify `VERSION=1.0`, Schema `2.0`, evals `1.0`, Changelog `[1.0]`, rejection of `1.0.0`, migration backup, old L4 review Gate, and byte-stable read-only validation.

- [ ] **Step 4: Inspect the final diff and package inventory**

```powershell
git status --short
git diff v0.4.0...HEAD --stat
git diff v0.4.0...HEAD --check
git log --oneline v0.4.0..HEAD
```

Expected: only approved 1.0 files, no whitespace errors, no generated artifacts, secrets, unrelated changes or nested `SKILL.md`.

- [ ] **Step 5: Commit readiness evidence**

```powershell
git add docs/release/1.0-readiness.md
git commit -m "test: record workflow 1.0 release readiness"
```

- [ ] **Step 6: Prepare the GitHub plugin plan and stop for approval**

Using the GitHub plugin, read the target repository, current `main`, open PRs, existing `v1.0` tag and releases. Present branch, commits, files, tests, proposed PR, merge method, tag and release body. Do not push, create/merge PR, tag or publish until the user confirms this exact remote plan.
