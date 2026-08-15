# Embedded Project Vibe Spec Core Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` or `executing-plans` to implement this plan task-by-task. Do not dispatch subagents unless the user explicitly chooses that execution mode. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Release `project-level-workflow` 0.4.0 as one self-contained Skill that embeds the complete Project Vibe Spec governance core and never requires a second Skill download.

**Architecture:** Keep `SKILL.md` as the only discoverable entry and `LEVEL.md` as the only LEVEL authority. Vendor the authorized PVS source under `core/project-vibe-spec/` with a non-discoverable `PVS.md`, route each LEVEL through the existing Bridge, and make Doctor, package validation, installers, lifecycle tests, state version updates, adapters, and evals enforce the single-Skill contract.

**Tech Stack:** Markdown Agent Skills, Python 3.10+ standard library, JSON Schema 2020-12, PowerShell, POSIX Shell, `unittest`, Git.

## Global Constraints

- Source repository: `D:\VibeCoding-Project\project-level-workflow`.
- Current handoff workspace: `C:\Users\admin\Documents\project-level-workflow`; it is not the implementation checkout.
- Target release: `0.4.0`; current verified baseline: `0.3.0` at local commit `c17f449`.
- PVS source repository: `https://github.com/dnwwdwd/project-vibe-spec.git`; authorized source commit: `dae5315`.
- The root MIT License covers the embedded PVS core; preserve source and modification provenance in `core/project-vibe-spec/SOURCE.md`.
- Expose exactly one discoverable Skill: root `SKILL.md`. Never create `core/project-vibe-spec/SKILL.md`.
- Do not require network access, a second install, Git submodules, or runtime lookup in the user's personal Skills directory.
- Preserve the confirmed LEVEL meanings and legacy LEVEL migration mapping.
- PVS governance starter is the only default source for overlapping LEVEL 2 governance documents.
- Keep overlapping `templates/level2/` files as compatibility entries in 0.4.0; do not delete them.
- Never delete, overwrite, move, or uninstall an independently installed `project-vibe-spec`; only report its path and version-divergence risk.
- Preserve user changes. Do not reset, stash, clean, force-push, rewrite history, deploy, publish, push, create a PR, or install into the real user Skills directory without the corresponding user authorization.
- Use `apply_patch` for source edits. Formatting or test commands may run normally.
- Report only checks actually run. Static checks do not prove real platform trigger behavior.

---

## Planned File Map

**Create in the implementation repository:**

- `core/project-vibe-spec/PVS.md` — internal PVS workflow entry without Skill frontmatter.
- `core/project-vibe-spec/SOURCE.md` — source commit, authorization, MIT coverage, and modification map.
- `core/project-vibe-spec/references/decision-gates.md` — authorized PVS decision Gate rules.
- `core/project-vibe-spec/references/document-maintenance.md` — authorized PVS document responsibility rules.
- `core/project-vibe-spec/assets/governance-starter/**` — the 17 authorized governance templates from commit `dae5315`.
- `templates/template-map.json` — one default template per governance responsibility plus compatibility paths.
- `tests/test_embedded_pvs.py` — core structure, provenance, template authority, and single-Skill tests.
- `tests/test_install_integration.py` — temporary project-scope install/update behavior tests.
- `docs/superpowers/specs/2026-08-16-embedded-project-vibe-spec-core-design.md` — confirmed design copied from the handoff document.
- `docs/superpowers/plans/2026-08-16-embedded-project-vibe-spec-core.md` — this implementation plan copied into the source repository.
- `docs/release/0.4.0-readiness.md` — local release-readiness evidence; not a publication authorization.

**Modify:**

- `SKILL.md` — route PVS requirements to the embedded core.
- `LEVEL.md` — state the embedded loading boundary without redefining LEVELs.
- `README.md` — document one-command, one-Skill, offline use.
- `references/project-vibe-spec-bridge.md` — convert external dependency wording into an embedded loading matrix.
- `references/platform-compatibility.md` — declare the same internal core path for Codex, Claude Code, and Cursor.
- `scripts/workflow.py` — embedded-core contract, template-map validation, Doctor checks, package checks, and workflow-version refresh.
- `scripts/install.ps1`, `scripts/install.sh` — preflight validation, core copying, Dry Run summary, independent-copy warning, and rollback-safe staging.
- `scripts/update.ps1`, `scripts/update.sh` — retain Doctor/state preflight and rely on the staged installer.
- `scripts/uninstall.ps1`, `scripts/uninstall.sh` — explain that embedded core is removed with the managed package while independent PVS is untouched.
- `schemas/workflow-state.schema.json` — update current package version const to `0.4.0`; do not change Schema version unless fields change.
- `adapters/codex/AGENTS.fragment.md`, `adapters/claude-code/CLAUDE.fragment.md`, `adapters/cursor/project-level-workflow.mdc` — point to the embedded Bridge/core contract.
- `evals/evals.json` — version 0.4.0 and self-contained behavior cases.
- `tests/test_doctor.py`, `tests/test_package_validation.py`, `tests/test_repository_contract.py`, `tests/test_workflow_state.py`, `tests/test_lifecycle_scripts.py`, `tests/test_adapters.py`, `tests/test_evals.py` — focused regressions.
- `CHANGELOG.md`, `VERSION` — 0.4.0 release contract.

**Do not delete:** any existing source, template, release document, backup, project state, or independent installed Skill.

---

### Task 1: Establish the Writable Baseline and Copy Approved Design Artifacts

**Files:**

- Create: `docs/superpowers/specs/2026-08-16-embedded-project-vibe-spec-core-design.md`
- Create: `docs/superpowers/plans/2026-08-16-embedded-project-vibe-spec-core.md`
- Read: `SKILL.md`, `LEVEL.md`, `README.md`, `scripts/workflow.py`, `scripts/install.*`, `scripts/update.*`, `scripts/uninstall.*`, `tests/`, `evals/evals.json`

**Interfaces:**

- Consumes: confirmed handoff design and this plan.
- Produces: a verified clean implementation baseline and repository-local specifications for all later tasks.

- [ ] **Step 1: Make the real repository writable without changing its contents**

Add `D:\VibeCoding-Project\project-level-workflow` as a writable workspace root, or create a writable checkout from its verified Git history. Do not implement in the handoff-only C drive root.

Expected: `apply_patch` can target files under the implementation checkout.

- [ ] **Step 2: Re-run the Git baseline checks**

Run from the implementation repository:

```powershell
git -c safe.directory=D:/VibeCoding-Project/project-level-workflow status --short --branch
git -c safe.directory=D:/VibeCoding-Project/project-level-workflow log -8 --oneline --decorate
git -c safe.directory=D:/VibeCoding-Project/project-level-workflow remote -v
git -c safe.directory=D:/VibeCoding-Project/project-level-workflow diff --stat
```

Expected: no tracked or untracked source changes. Record the actual branch and commit; do not assume they remain `codex/level-model-v1` and `c17f449`.

If the repository is dirty, stop and report every modified path. Do not reset, stash, clean, or overwrite it.

- [ ] **Step 3: Choose an implementation branch only after checking the real baseline**

Recommended branch name:

```text
codex/embed-project-vibe-spec-core
```

Creating or switching branches is deferred until the user confirms which verified commit should be the base. A remote fetch is read-only but may require network approval; do not fetch merely to hide an unclear baseline.

- [ ] **Step 4: Copy the confirmed design and plan with `apply_patch`**

Copy the exact contents of:

```text
C:\Users\admin\Documents\project-level-workflow\docs\handoff\project-vibe-spec-embedded-core-design.md
C:\Users\admin\Documents\project-level-workflow\docs\handoff\project-vibe-spec-embedded-core-implementation-plan.md
```

to the two repository-local paths listed above. Preserve UTF-8 and final newlines.

- [ ] **Step 5: Verify the documentation copy**

Run:

```powershell
rg -n "只暴露一个可发现|0\.4\.0|dae5315|PVS governance starter" docs/superpowers
rg -n -i "\b(TODO|TBD|FIXME|CHANGEME)\b" docs/superpowers
```

Expected: the first command finds all four confirmed decisions; the second returns no matches.

- [ ] **Step 6: Local commit Gate**

Do not commit automatically. If the user authorizes a local documentation commit, use only:

```powershell
git add docs/superpowers/specs/2026-08-16-embedded-project-vibe-spec-core-design.md docs/superpowers/plans/2026-08-16-embedded-project-vibe-spec-core.md
git commit -m "docs: design embedded project vibe spec core"
```

Otherwise leave the files uncommitted and continue only if the user explicitly authorizes implementation in that worktree.

---

### Task 2: Add the Embedded PVS Core and Single Template Authority

**Files:**

- Create: `core/project-vibe-spec/PVS.md`
- Create: `core/project-vibe-spec/SOURCE.md`
- Create: `core/project-vibe-spec/references/decision-gates.md`
- Create: `core/project-vibe-spec/references/document-maintenance.md`
- Create: `core/project-vibe-spec/assets/governance-starter/**`
- Create: `templates/template-map.json`
- Create: `tests/test_embedded_pvs.py`

**Interfaces:**

- Consumes: authorized PVS commit `dae5315` from `C:\Users\admin\.codex\skills\project-vibe-spec`.
- Produces: `core/project-vibe-spec/PVS.md`; `templates/template-map.json` with `version: 1` and unique `roles[*].name`/`roles[*].default` values.

- [ ] **Step 1: Write the failing embedded-core contract tests**

Create `tests/test_embedded_pvs.py` with this complete test structure:

```python
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
        source = (CORE / "SOURCE.md").read_text(encoding="utf-8")
        self.assertIn("https://github.com/dnwwdwd/project-vibe-spec.git", source)
        self.assertIn("dae5315", source)
        self.assertIn("MIT", source)
        self.assertIn("PVS.md", source)

    def test_template_map_has_one_default_per_role(self) -> None:
        data = json.loads((ROOT / "templates" / "template-map.json").read_text(encoding="utf-8"))
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
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run:

```powershell
python -m unittest tests.test_embedded_pvs -v
```

Expected: FAIL because `core/project-vibe-spec/PVS.md` and `templates/template-map.json` do not exist.

- [ ] **Step 3: Add the internal PVS entry and provenance**

Create `core/project-vibe-spec/PVS.md` from source `project-vibe-spec/SKILL.md` with these exact transformations:

```markdown
# Project Vibe Spec 包内治理内核

> 本文件是 `project-level-workflow` 的内部治理资源，不是独立 Skill 入口。由根目录 `SKILL.md` 和 `references/project-vibe-spec-bridge.md` 按 LEVEL 加载。
```

Remove only the original YAML frontmatter and replace the original H1 with the block above. Preserve sections 1–7 and keep relative links as:

```markdown
[assets/governance-starter](assets/governance-starter)
[references/document-maintenance.md](references/document-maintenance.md)
[references/decision-gates.md](references/decision-gates.md)
```

Create `core/project-vibe-spec/SOURCE.md` with this exact contract:

```markdown
# Project Vibe Spec 来源与授权

- 原仓库：`https://github.com/dnwwdwd/project-vibe-spec.git`
- 同步提交：`dae5315`（Strengthen cross-module governance gates）
- 纳入版本：`project-level-workflow 0.4.0`
- 授权：源码所有者已确认允许复制、修改并随本包公开分发。
- 许可证：本目录内容统一适用包根目录的 MIT License。

## 文件映射与修改

- 原 `SKILL.md` → `PVS.md`：移除独立 Skill frontmatter，增加包内加载说明；治理规则保持原意。
- 原 `references/` → 本目录 `references/`：内容保持原意。
- 原 `assets/governance-starter/` → 本目录同名路径：模板内容保持原意。
- 原 `README.md` 与 `agents/openai.yaml` 不作为运行时资源复制，因为本包只暴露根 `project-level-workflow` Skill。
```

- [ ] **Step 4: Copy the authorized references and 17 templates**

Using `apply_patch`, add the exact UTF-8 contents from these source paths to the same relative paths under `core/project-vibe-spec/`:

```text
C:\Users\admin\.codex\skills\project-vibe-spec\references\decision-gates.md
C:\Users\admin\.codex\skills\project-vibe-spec\references\document-maintenance.md
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\AGENTS.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\DOCUMENT_MAP.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\Decisions\DEC-YYYYMMDD-NNN.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\Decisions\LEDGER.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\Decisions\README.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\Progress\LEDGER.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\Progress\PROG-REQ-YYYYMMDD-NNN-slug.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\Progress\README.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\Requirements\LEDGER.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\Requirements\README.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\Requirements\REQ-YYYYMMDD-NNN.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\docs\BUG_TRACKER.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\docs\BUSINESS_FLOW.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\docs\PDD.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\docs\PRD.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\docs\PROGRESS.md.template
C:\Users\admin\.codex\skills\project-vibe-spec\assets\governance-starter\docs\UI_GUIDE.md.template
```

Do not copy the source `.git/`, source `README.md`, or source `agents/openai.yaml`.

- [ ] **Step 5: Add the deterministic template map**

Create `templates/template-map.json`:

```json
{
  "version": 1,
  "roles": [
    {"name": "project_contract", "levels": [1, 2], "default": "core/project-vibe-spec/assets/governance-starter/AGENTS.md.template", "compatibility": []},
    {"name": "document_map", "levels": [1, 2], "default": "core/project-vibe-spec/assets/governance-starter/DOCUMENT_MAP.md.template", "compatibility": ["templates/level2/project-map.md"]},
    {"name": "requirements_ledger", "levels": [2], "default": "core/project-vibe-spec/assets/governance-starter/Requirements/LEDGER.md.template", "compatibility": []},
    {"name": "requirement_record", "levels": [2], "default": "core/project-vibe-spec/assets/governance-starter/Requirements/REQ-YYYYMMDD-NNN.md.template", "compatibility": ["templates/level2/requirements.md"]},
    {"name": "decision_ledger", "levels": [2], "default": "core/project-vibe-spec/assets/governance-starter/Decisions/LEDGER.md.template", "compatibility": []},
    {"name": "decision_record", "levels": [2], "default": "core/project-vibe-spec/assets/governance-starter/Decisions/DEC-YYYYMMDD-NNN.md.template", "compatibility": ["templates/level2/decision-record.md"]},
    {"name": "bug_tracker", "levels": [2], "default": "core/project-vibe-spec/assets/governance-starter/docs/BUG_TRACKER.md.template", "compatibility": []},
    {"name": "pdd", "levels": [2], "default": "core/project-vibe-spec/assets/governance-starter/docs/PDD.md.template", "compatibility": []},
    {"name": "prd", "levels": [2], "default": "core/project-vibe-spec/assets/governance-starter/docs/PRD.md.template", "compatibility": ["templates/level2/prd.md", "templates/level2/tech-spec.md"]},
    {"name": "ui_guide", "levels": [2], "default": "core/project-vibe-spec/assets/governance-starter/docs/UI_GUIDE.md.template", "compatibility": []},
    {"name": "business_flow", "levels": [2], "default": "core/project-vibe-spec/assets/governance-starter/docs/BUSINESS_FLOW.md.template", "compatibility": []},
    {"name": "project_progress", "levels": [2], "default": "core/project-vibe-spec/assets/governance-starter/docs/PROGRESS.md.template", "compatibility": []},
    {"name": "feature_progress_ledger", "levels": [2], "default": "core/project-vibe-spec/assets/governance-starter/Progress/LEDGER.md.template", "compatibility": []},
    {"name": "feature_progress_record", "levels": [2], "default": "core/project-vibe-spec/assets/governance-starter/Progress/PROG-REQ-YYYYMMDD-NNN-slug.md.template", "compatibility": ["templates/level2/task.md"]}
  ]
}
```

The three PVS directory README templates remain copyable support files but are not document responsibilities, so they do not need separate role entries.

- [ ] **Step 6: Run focused tests**

Run:

```powershell
python -m unittest tests.test_embedded_pvs -v
```

Expected: 3 tests PASS.

- [ ] **Step 7: Review and optional local commit Gate**

Run:

```powershell
git diff --check
git status --short
```

If a local commit is authorized:

```powershell
git add core/project-vibe-spec templates/template-map.json tests/test_embedded_pvs.py
git commit -m "feat: embed project vibe spec governance core"
```

---

### Task 3: Enforce the Embedded-Core Package Contract

**Files:**

- Modify: `scripts/workflow.py`
- Modify: `tests/test_doctor.py`
- Modify: `tests/test_package_validation.py`
- Modify: `tests/test_repository_contract.py`

**Interfaces:**

- Consumes: `core/project-vibe-spec/` and `templates/template-map.json` from Task 2.
- Produces: `PVS_CORE_FILES`, `_embedded_pvs_errors(root) -> list[str]`, and deterministic Doctor/package failures.

- [ ] **Step 1: Add failing package and Doctor tests**

Add to `tests/test_package_validation.py`:

```python
    def test_embedded_pvs_contract_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "package"
            shutil.copytree(ROOT, package)
            (package / "core" / "project-vibe-spec" / "PVS.md").unlink()
            errors = workflow.validate_package(package)
        self.assertIn("PVS 内核", " ".join(errors))

    def test_nested_pvs_skill_entry_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "package"
            shutil.copytree(ROOT, package)
            nested = package / "core" / "project-vibe-spec" / "SKILL.md"
            nested.write_text("---\nname: project-vibe-spec\n---\n", encoding="utf-8")
            errors = workflow.validate_package(package)
        self.assertIn("第二个 Skill", " ".join(errors))

    def test_external_pvs_install_instruction_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "package"
            shutil.copytree(ROOT, package)
            readme = package / "README.md"
            readme.write_text(readme.read_text(encoding="utf-8") + "\ngit clone https://example/project-vibe-spec.git\n", encoding="utf-8")
            errors = workflow.validate_package(package)
        self.assertIn("外部 PVS", " ".join(errors))
```

Also add `import shutil` to that test module.

Add to `tests/test_doctor.py`:

```python
    def test_doctor_warns_but_passes_for_independent_pvs(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            package = parent / "project-level-workflow"
            shutil.copytree(ROOT, package)
            (parent / "project-vibe-spec").mkdir()
            result = run_cli("doctor", "--package-root", str(package))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("WARN 独立 project-vibe-spec", result.stdout)

    def test_doctor_reports_embedded_pvs(self):
        result = run_cli("doctor", "--package-root", str(ROOT))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PVS 包内内核", result.stdout)
        self.assertIn("PVS 模板职责映射", result.stdout)
```

Also add `import shutil` to `tests/test_doctor.py`.

Add to `tests/test_repository_contract.py`:

```python
    def test_only_root_skill_is_discoverable(self):
        skill_files = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("SKILL.md"))
        self.assertEqual(skill_files, ["SKILL.md"])
```

- [ ] **Step 2: Run the focused tests and verify failure**

Run:

```powershell
python -m unittest tests.test_package_validation tests.test_doctor tests.test_repository_contract -v
```

Expected: FAIL because `workflow.py` does not yet enforce or report the embedded core.

- [ ] **Step 3: Add embedded-core constants and validator**

Near the existing package constants in `scripts/workflow.py`, add:

```python
PVS_CORE = Path("core/project-vibe-spec")
PVS_TEMPLATE_MAP = Path("templates/template-map.json")
PVS_CORE_FILES = (
    "PVS.md",
    "SOURCE.md",
    "references/decision-gates.md",
    "references/document-maintenance.md",
)
EXTERNAL_PVS_INSTALL = re.compile(
    r"(?:git\s+clone[^\n]*project-vibe-spec|skills[/\\]project-vibe-spec|\$project-vibe-spec)",
    re.IGNORECASE,
)
```

Add this complete helper before `validate_package`:

```python
def _embedded_pvs_errors(root: Path) -> list[str]:
    errors: list[str] = []
    core = root / PVS_CORE
    for relative in PVS_CORE_FILES:
        if not (core / relative).is_file():
            errors.append(f"PVS 内核缺少文件：{PVS_CORE / relative}")
    if (core / "SKILL.md").exists():
        errors.append("PVS 内核不得包含第二个 Skill 入口：core/project-vibe-spec/SKILL.md")
    source_path = core / "SOURCE.md"
    if source_path.is_file():
        source = source_path.read_text(encoding="utf-8")
        for marker in ("dnwwdwd/project-vibe-spec", "dae5315", "MIT"):
            if marker not in source:
                errors.append(f"PVS 来源记录缺少：{marker}")

    map_path = root / PVS_TEMPLATE_MAP
    if not map_path.is_file():
        errors.append(f"PVS 模板职责映射不存在：{PVS_TEMPLATE_MAP}")
        return errors
    try:
        data = json.loads(map_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"PVS 模板职责映射无法读取：{exc}")
        return errors
    roles = data.get("roles")
    if data.get("version") != 1 or not isinstance(roles, list) or not roles:
        errors.append("PVS 模板职责映射必须包含 version=1 和非空 roles")
        return errors
    names: set[str] = set()
    defaults: set[str] = set()
    for entry in roles:
        if not isinstance(entry, dict):
            errors.append("PVS 模板职责条目必须是对象")
            continue
        name = entry.get("name")
        default = entry.get("default")
        if not isinstance(name, str) or not name or name in names:
            errors.append(f"PVS 模板职责名称无效或重复：{name}")
        else:
            names.add(name)
        if not isinstance(default, str) or not default or default in defaults:
            errors.append(f"PVS 默认模板无效或重复：{default}")
        else:
            defaults.add(default)
            if not (root / default).is_file():
                errors.append(f"PVS 默认模板不存在：{default}")
        compatibility = entry.get("compatibility", [])
        if not isinstance(compatibility, list):
            errors.append(f"PVS compatibility 必须是数组：{name}")
            continue
        for relative in compatibility:
            if not isinstance(relative, str) or not (root / relative).is_file():
                errors.append(f"PVS 兼容模板不存在：{relative}")
    return errors
```

- [ ] **Step 4: Extend Doctor and package validation**

In `command_doctor`, append checks using the existing `(name, passed, detail)` shape:

```python
    pvs_errors = _embedded_pvs_errors(root)
    checks.append(("PVS 包内内核", not pvs_errors, "; ".join(pvs_errors) or str(root / PVS_CORE)))
    checks.append(("PVS 模板职责映射", (root / PVS_TEMPLATE_MAP).is_file(), str(root / PVS_TEMPLATE_MAP)))
```

Before returning from Doctor, detect only the exact sibling directory and print a non-blocking warning:

```python
    independent_pvs = root.parent / "project-vibe-spec"
    if independent_pvs.is_dir():
        print(
            f"WARN 独立 project-vibe-spec：{independent_pvs}；"
            "本包不会读取、覆盖或删除该目录。"
        )
```

Do not add this warning to `required_failures`.

In `validate_package`, add `core/project-vibe-spec/PVS.md`, `core/project-vibe-spec/SOURCE.md`, both PVS references, and `templates/template-map.json` to `required`, then append:

```python
    errors.extend(_embedded_pvs_errors(root))
    for path in _public_markdown_files(root):
        relative = path.relative_to(root)
        if relative == PVS_CORE / "SOURCE.md":
            continue
        text = path.read_text(encoding="utf-8")
        if EXTERNAL_PVS_INSTALL.search(text):
            errors.append(f"公共文件包含外部 PVS 安装或调用要求：{relative}")
```

Ensure `_public_markdown_files` includes Markdown under `core/` while still excluding test fixtures and backups.

- [ ] **Step 5: Run focused and existing package tests**

Run:

```powershell
python -m unittest tests.test_embedded_pvs tests.test_package_validation tests.test_doctor tests.test_repository_contract -v
python scripts/workflow.py doctor --package-root .
python scripts/workflow.py validate-package --package-root .
```

Expected: all focused tests PASS; Doctor reports `PASS PVS 包内内核`; package validation passes.

- [ ] **Step 6: Review and optional local commit Gate**

Run `git diff --check` and inspect only Task 3 paths. If authorized:

```powershell
git add scripts/workflow.py tests/test_doctor.py tests/test_package_validation.py tests/test_repository_contract.py
git commit -m "test: enforce embedded pvs package contract"
```

---

### Task 4: Route All LEVELs to the Embedded Core Without Redefining Them

**Files:**

- Modify: `SKILL.md`
- Modify: `LEVEL.md`
- Modify: `README.md`
- Modify: `references/project-vibe-spec-bridge.md`
- Modify: `references/platform-compatibility.md`
- Modify: `tests/test_repository_contract.py`

**Interfaces:**

- Consumes: `core/project-vibe-spec/PVS.md` and `templates/template-map.json`.
- Produces: exact embedded paths and a LEVEL loading matrix used by humans and adapters.

- [ ] **Step 1: Write failing routing assertions**

Add to `tests/test_repository_contract.py`:

```python
    def test_public_workflow_routes_to_embedded_pvs(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        bridge = (ROOT / "references" / "project-vibe-spec-bridge.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for text in (skill, bridge, readme):
            self.assertIn("core/project-vibe-spec/PVS.md", text)
            self.assertNotIn("另行安装 `project-vibe-spec`", text)
        self.assertIn("templates/template-map.json", bridge)
        self.assertIn("LEVEL.md", bridge)
```

- [ ] **Step 2: Run the test and verify failure**

Run `python -m unittest tests.test_repository_contract -v`.

Expected: FAIL because current public docs describe PVS as an external Skill.

- [ ] **Step 3: Update the root Skill routing**

In `SKILL.md`, replace external-PVS wording with this contract near project discovery and LEVEL initialization:

```markdown
包内 PVS 治理入口为 `core/project-vibe-spec/PVS.md`。按 `references/project-vibe-spec-bridge.md` 只加载当前 LEVEL 需要的章节和模板；不得要求用户另行安装、查找或下载 `project-vibe-spec`。包内入口缺失时按包损坏停止，不回退到个人 Skills 目录中的独立副本。
```

For LEVEL 2, replace “完整遵循外部 `project-vibe-spec`” with:

```markdown
读取 `core/project-vibe-spec/PVS.md` 全部流程及其两份 reference；治理文档以 `templates/template-map.json` 声明的 PVS starter 为唯一默认来源，项目已有等价事实源仍优先。
```

For LEVEL 1, 3, and 4, point to the Bridge matrix and preserve current scope limits verbatim.

- [ ] **Step 4: Rewrite the Bridge as an internal loading matrix**

Keep the current file path and create a table with these exact semantics:

```markdown
| LEVEL | 读取 PVS 内核 | 默认模板来源 | 禁止扩大 |
|---|---|---|---|
| 1 | 首次接管、事实与需求确认、实现边界、验证与交付 | PVS 的 AGENTS/DOCUMENT_MAP；其余使用 LEVEL 1 模板 | 不创建完整 Requirements/Decisions/Progress/PDD/PRD 包 |
| 2 | `PVS.md` 全文、两份 reference、governance starter | `templates/template-map.json` 中的 PVS 默认模板 | 不覆盖项目已有等价事实源 |
| 3 | 事实与需求、跨模块影响、实现边界、验证与 Git 交付 | 既有仓库文档；PVS 只补缺 | 不强制复制完整 PVS 文档包 |
| 4 | 需求确认、方案/数据 Gate、风险和验收 | 分析记录和现有 LEVEL 4 模板 | 不写代码、不改数据库、不部署、不拆实现任务 |
```

State explicitly that `LEVEL.md` remains the sole LEVEL authority and `core/project-vibe-spec/PVS.md` is only the collaboration-contract core.

- [ ] **Step 5: Update LEVEL, README, and platform compatibility**

Add the exact internal path and offline/single-Skill guarantee without duplicating the PVS body. README must say:

```markdown
0.4.0 起，完整 PVS 治理规则和 starter 模板已内嵌在 `core/project-vibe-spec/`。安装本包后只显示一个 `project-level-workflow` Skill；四个 LEVEL 均不需要第二次下载或联网补齐 PVS。
```

Do not include `$project-vibe-spec`, a personal Skills path, or an external clone command outside `SOURCE.md`.

- [ ] **Step 6: Run routing and package tests**

Run:

```powershell
python -m unittest tests.test_repository_contract tests.test_package_validation -v
python scripts/workflow.py validate-package --package-root .
```

Expected: PASS with no external-install contract errors.

- [ ] **Step 7: Review and optional local commit Gate**

If authorized:

```powershell
git add SKILL.md LEVEL.md README.md references/project-vibe-spec-bridge.md references/platform-compatibility.md tests/test_repository_contract.py
git commit -m "docs: route levels to embedded pvs core"
```

---

### Task 5: Refresh Workflow Version on Explicit State Writes Only

**Files:**

- Modify: `scripts/workflow.py`
- Modify: `tests/test_workflow_state.py`
- Modify: `schemas/workflow-state.schema.json`

**Interfaces:**

- Consumes: `load_version() -> str` and current state dictionaries.
- Produces: `_refresh_workflow_version(state: dict[str, Any]) -> bool`; history event `workflow_version_updated`.

- [ ] **Step 1: Write failing state-version tests**

Add to `tests/test_workflow_state.py`:

```python
    def test_validate_does_not_mutate_older_workflow_version(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(run_cli("init", "--project", temp, "--level", "1").returncode, 0)
            state_path = Path(temp) / ".project-workflow" / "state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["workflow_version"] = "0.3.0"
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            before = state_path.read_bytes()
            result = run_cli("validate", "--project", temp)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(state_path.read_bytes(), before)

    def test_status_refreshes_workflow_version_with_backup_and_history(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(run_cli("init", "--project", temp, "--level", "2").returncode, 0)
            project = Path(temp)
            state_path = project / ".project-workflow" / "state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["workflow_version"] = "0.3.0"
            state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
            result = run_cli("status", "--project", temp)
            self.assertEqual(result.returncode, 0, result.stderr)
            current = json.loads(state_path.read_text(encoding="utf-8"))
            backup = json.loads((project / ".project-workflow" / "state.backup.json").read_text(encoding="utf-8"))
            self.assertEqual(current["workflow_version"], "0.4.0")
            self.assertEqual(backup["workflow_version"], "0.3.0")
            event = next(item for item in current["history"] if item.get("event") == "workflow_version_updated")
            self.assertEqual(event["from_version"], "0.3.0")
            self.assertEqual(event["to_version"], "0.4.0")
```

- [ ] **Step 2: Temporarily set package version contracts to 0.4.0 and verify the focused failure**

Update `VERSION` to `0.4.0`, `schemas/workflow-state.schema.json` `workflow_version.const` to `0.4.0`, and `evals/evals.json` `version` to `0.4.0`. Add an empty 0.4.0 heading to `CHANGELOG.md` only if needed to keep existing package-contract tests runnable; Task 8 will replace it with complete release notes.

Run `python -m unittest tests.test_workflow_state -v`.

Expected: the validate non-mutation test passes; the status refresh test fails because `status` does not write state.

- [ ] **Step 3: Implement version refresh**

Add:

```python
def _refresh_workflow_version(state: dict[str, Any]) -> bool:
    current = load_version()
    previous = state.get("workflow_version")
    if previous == current:
        return False
    now = utc_now()
    state["workflow_version"] = current
    state["updated_at"] = now
    state["history"].append(
        {
            "event": "workflow_version_updated",
            "from_version": previous,
            "to_version": current,
            "at": now,
        }
    )
    return True
```

In `command_status`, retain `backup_path`, deep-copy the validated state, call the helper, validate again, then write backup and state only when it returns `True`; always render STATUS from the current in-memory state.

In `command_transition`, take `previous` before calling `_refresh_workflow_version`, call the helper before appending `gate_approved`, and keep the current backup/write sequence.

Keep `command_migrate` unchanged when `schema_version` is already current: it remains a no-op and must not advance `workflow_version` before the new package has been installed. Do not call the helper from `command_validate`, `command_migrate`, or Doctor.

- [ ] **Step 4: Run state and package tests**

Run:

```powershell
python -m unittest tests.test_workflow_state tests.test_package_validation -v
```

Expected: all tests PASS; validate remains byte-for-byte read-only; status creates a 0.3.0 backup and 0.4.0 state.

- [ ] **Step 5: Review and optional local commit Gate**

If authorized:

```powershell
git add scripts/workflow.py tests/test_workflow_state.py schemas/workflow-state.schema.json VERSION evals/evals.json CHANGELOG.md
git commit -m "feat: refresh workflow version on state writes"
```

---

### Task 6: Make Install and Update Atomic, Self-Contained, and Single-Skill

**Files:**

- Modify: `scripts/install.ps1`, `scripts/install.sh`
- Modify: `scripts/update.ps1`, `scripts/update.sh`
- Modify: `scripts/uninstall.ps1`, `scripts/uninstall.sh`
- Modify: `tests/test_lifecycle_scripts.py`
- Create: `tests/test_install_integration.py`

**Interfaces:**

- Consumes: CLI `validate-package`, package `core/`, target parent directory.
- Produces: staged installation with `core` copied, `PVS 内核` Dry Run summary, independent PVS warning, and restoration-safe update.

- [ ] **Step 1: Add failing lifecycle source assertions**

Add to `tests/test_lifecycle_scripts.py`:

```python
    def test_installers_validate_and_copy_embedded_core(self) -> None:
        for name in ("install.ps1", "install.sh"):
            with self.subTest(script=name):
                content = self._read(name)
                self.assertIn("validate-package", content)
                self.assertIn("core", content)
                self.assertIn("PVS 内核", content)
                self.assertIn("project-vibe-spec", content)

    def test_uninstallers_leave_independent_pvs_untouched(self) -> None:
        for name in ("uninstall.ps1", "uninstall.sh"):
            with self.subTest(script=name):
                content = self._read(name)
                self.assertIn("独立 project-vibe-spec", content)
                self.assertIn("不处理", content)
```

- [ ] **Step 2: Add temporary PowerShell integration test**

Create `tests/test_install_integration.py`:

```python
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallIntegrationTests(unittest.TestCase):
    @unittest.skipUnless(os.name == "nt" and shutil.which("powershell"), "PowerShell integration test")
    def test_project_install_is_single_skill_and_preserves_independent_pvs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            skills = project / ".codex" / "skills"
            independent = skills / "project-vibe-spec"
            independent.mkdir(parents=True)
            marker = independent / "keep.txt"
            marker.write_text("keep", encoding="utf-8")
            result = subprocess.run(
                [
                    "powershell", "-NoProfile", "-File", str(ROOT / "scripts" / "install.ps1"),
                    "-Platform", "codex", "-Scope", "project", "-ProjectPath", str(project),
                ],
                text=True, encoding="utf-8", errors="replace", capture_output=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            installed = skills / "project-level-workflow"
            skill_files = sorted(path.relative_to(installed).as_posix() for path in installed.rglob("SKILL.md"))
            self.assertEqual(skill_files, ["SKILL.md"])
            self.assertTrue((installed / "core" / "project-vibe-spec" / "PVS.md").is_file())
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")
            self.assertIn("独立 project-vibe-spec", result.stdout)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run lifecycle tests and verify failure**

Run:

```powershell
python -m unittest tests.test_lifecycle_scripts tests.test_install_integration -v
```

Expected: FAIL because installers do not validate/copy `core` or warn about an independent PVS.

- [ ] **Step 4: Implement PowerShell preflight and staging**

In `install.ps1`:

1. Add `'core'` to `Copy-Package` items.
2. Resolve Python using the same `python`/`python3` logic as `update.ps1`.
3. Run `workflow.py validate-package --package-root $packageRoot` before any move.
4. Compute `$pvsFiles = @(Get-ChildItem -LiteralPath (Join-Path $packageRoot 'core/project-vibe-spec') -Recurse -File)` and print `PVS 内核：$($pvsFiles.Count) 个文件`.
5. Compute `$independentPvs = Join-Path (Split-Path -Parent $target) 'project-vibe-spec'`; if it exists, print `提示：检测到独立 project-vibe-spec：$independentPvs；本安装不处理该目录。`.
6. Copy to `$staging = "$target.installing-$PID"`; only after a complete copy move the old target to backup and staging to target.
7. In `catch`, remove only the exact validated staging/partial managed target, then restore the backup. Never recurse outside a leaf ending in `project-level-workflow` or `.installing-$PID`.

Use this operation order:

```powershell
Copy-Package -SourceRoot $packageRoot -TargetPath $staging
if ($backup) { Move-Item -LiteralPath $target -Destination $backup }
Move-Item -LiteralPath $staging -Destination $target
```

- [ ] **Step 5: Implement the same POSIX contract**

In `install.sh`:

- Add `core` to `items=(...)`.
- Resolve Python and run `"$python_cmd" "$package_root/scripts/workflow.py" validate-package --package-root "$package_root"` before any `mv`.
- Count PVS files using `find "$package_root/core/project-vibe-spec" -type f | wc -l` and print the summary.
- Warn if `"$(dirname "$target")/project-vibe-spec"` exists.
- Copy into `staging="$target.installing-$$"`, add a trap that removes only that exact staging path, then move old target to backup and staging to target.

Required order:

```bash
mkdir -p -- "$staging"
for item in "${items[@]}"; do
  [[ -e "$package_root/$item" ]] || continue
  cp -R -- "$package_root/$item" "$staging/"
done
[[ -z "$backup" ]] || mv -- "$target" "$backup"
mv -- "$staging" "$target"
```

Do not construct or evaluate shell command strings.

- [ ] **Step 6: Update lifecycle messages**

Keep update scripts' Doctor and project-state migration before replacement. Update comments to state that the staged installer validates and copies the embedded core.

Update both uninstallers to print:

```text
托管目录中的 PVS 包内内核将随 project-level-workflow 一起移除。
独立 project-vibe-spec 不属于本包托管范围，本卸载器不处理。
```

Do not add code that finds or deletes the independent directory.

- [ ] **Step 7: Run lifecycle tests**

Run:

```powershell
python -m unittest tests.test_lifecycle_scripts tests.test_install_integration -v
```

Expected: static lifecycle tests PASS; PowerShell temporary install PASS on Windows; no real user Skill directory is touched.

If Bash is available, also run a project-scope temporary Dry Run and installation using a new temporary directory. Record Bash as untested if the runtime is unavailable.

- [ ] **Step 8: Review and optional local commit Gate**

If authorized:

```powershell
git add scripts/install.ps1 scripts/install.sh scripts/update.ps1 scripts/update.sh scripts/uninstall.ps1 scripts/uninstall.sh tests/test_lifecycle_scripts.py tests/test_install_integration.py
git commit -m "feat: install embedded pvs core atomically"
```

---

### Task 7: Update Adapters and Evals for the One-Skill Runtime

**Files:**

- Modify: `adapters/codex/AGENTS.fragment.md`
- Modify: `adapters/claude-code/CLAUDE.fragment.md`
- Modify: `adapters/cursor/project-level-workflow.mdc`
- Modify: `evals/evals.json`
- Modify: `tests/test_adapters.py`
- Modify: `tests/test_evals.py`

**Interfaces:**

- Consumes: root Bridge and embedded core path.
- Produces: rendered platform entry points and eval cases that never instruct a second install.

- [ ] **Step 1: Write failing adapter and eval assertions**

Add to `tests/test_adapters.py`:

```python
    def test_all_adapters_reference_embedded_pvs_bridge(self):
        for relative in (
            "adapters/codex/AGENTS.fragment.md",
            "adapters/claude-code/CLAUDE.fragment.md",
            "adapters/cursor/project-level-workflow.mdc",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("references/project-vibe-spec-bridge.md", text)
            self.assertIn("core/project-vibe-spec/PVS.md", text)
```

Add to `tests/test_evals.py`:

```python
    def test_self_contained_pvs_cases_exist(self) -> None:
        data = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
        by_id = {case["id"]: case for case in data["cases"]}
        for case_id in ("level2-bundled-pvs", "single-skill-offline", "independent-pvs-not-required"):
            self.assertIn(case_id, by_id)
        self.assertFalse(by_id["level2-bundled-pvs"]["expected_output"]["external_install"])
        self.assertEqual(by_id["level2-bundled-pvs"]["expected_output"]["pvs_source"], "bundled")
```

- [ ] **Step 2: Run focused tests and verify failure**

Run `python -m unittest tests.test_adapters tests.test_evals -v`.

Expected: FAIL because adapters and eval cases lack embedded-core references.

- [ ] **Step 3: Update all three adapters**

Add this compact block inside each managed entry without copying the PVS body:

```markdown
- PVS 分层路由：`references/project-vibe-spec-bridge.md`
- PVS 包内内核：`core/project-vibe-spec/PVS.md`
```

Keep `LEVEL.md`, state paths, LEVEL 4 boundary, and managed markers unchanged.

- [ ] **Step 4: Add exact self-contained eval cases**

Append to `evals/evals.json`:

```json
{
  "id": "level2-bundled-pvs",
  "prompt": "我要开发有登录、云端数据和持续运营责任的自有产品，请按 LEVEL 2 完整 PVS 推进；不要让我再安装其他 Skill。",
  "expected_output": {"trigger": true, "level": 2, "pvs_source": "bundled", "external_install": false},
  "files": ["SKILL.md", "references/project-vibe-spec-bridge.md", "core/project-vibe-spec/PVS.md"]
},
{
  "id": "single-skill-offline",
  "prompt": "断网环境只安装 project-level-workflow 后，帮我初始化一个 LEVEL 2 项目。",
  "expected_output": {"trigger": true, "level": 2, "single_skill": true, "network_required": false},
  "files": ["README.md", "core/project-vibe-spec/PVS.md", "templates/template-map.json"]
},
{
  "id": "independent-pvs-not-required",
  "prompt": "我没有单独安装 project-vibe-spec，是否还能按完整流程开发长期运营产品？",
  "expected_output": {"trigger": true, "level": 2, "pvs_source": "bundled", "external_install": false},
  "files": ["SKILL.md", "references/project-vibe-spec-bridge.md"]
}
```

Keep all previous LEVEL, migration, Git policy, and negative trigger cases.

- [ ] **Step 5: Run adapter/eval and package tests**

Run:

```powershell
python -m unittest tests.test_adapters tests.test_evals tests.test_package_validation -v
```

Expected: PASS.

- [ ] **Step 6: Review and optional local commit Gate**

If authorized:

```powershell
git add adapters evals/evals.json tests/test_adapters.py tests/test_evals.py
git commit -m "test: cover one-skill pvs routing"
```

---

### Task 8: Complete 0.4.0 Documentation, Release Contract, and Full Verification

**Files:**

- Modify: `VERSION`
- Modify: `CHANGELOG.md`
- Modify: `README.md`
- Modify: `schemas/workflow-state.schema.json`
- Modify: `evals/evals.json`
- Create: `docs/release/0.4.0-readiness.md`
- Modify as required by failures: only files already in this plan's scope

**Interfaces:**

- Consumes: all previous task outputs.
- Produces: internally consistent 0.4.0 package and evidence-backed readiness report.

- [ ] **Step 1: Finalize the version contract**

Set these exact values:

```text
VERSION                                      0.4.0
schemas/workflow-state.schema.json           properties.workflow_version.const = 0.4.0
evals/evals.json                             version = 0.4.0
CHANGELOG.md                                 heading ## [0.4.0]
```

The 0.4.0 changelog entry must cover: embedded PVS core, one visible Skill, PVS template authority, package/Doctor validation, staged installers, workflow-version refresh, adapter/eval coverage, and independent PVS non-deletion.

- [ ] **Step 2: Create the local readiness document**

Create `docs/release/0.4.0-readiness.md` with these sections:

```markdown
# Project Level Workflow 0.4.0 Release Readiness

## Scope and non-goals
## Embedded PVS source and MIT authorization
## One-Skill and template-authority contract
## State and compatibility behavior
## Commands actually run and results
## Platform installation matrix
## Unexecuted checks and reasons
## Risks, rollback, and independent PVS handling
## Publication Gate
```

Populate results only after running the following steps. Keep publication status `not authorized` unless the user separately authorizes Release.

- [ ] **Step 3: Run the complete unit suite**

Run from repository root:

```powershell
python -m unittest discover -s tests -v
```

Expected: all tests PASS. Record exact test count and elapsed time.

If the system Python launcher fails, use the bundled runtime explicitly:

```text
C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
```

- [ ] **Step 4: Run Doctor and package validation**

Run:

```powershell
python scripts/workflow.py doctor --package-root .
python scripts/workflow.py validate-package --package-root .
```

Expected: Doctor reports PASS for the PVS internal core and template map; package validation reports `project-level-workflow 0.4.0`.

- [ ] **Step 5: Run four-level initialization and adapter smoke tests in a temporary root**

Create one narrow temporary directory with `New-Item` or the platform temp API. For each LEVEL 1–4:

```powershell
python scripts/workflow.py init --project <temp-level-project> --level <1|2|3|4>
python scripts/workflow.py validate --project <temp-level-project>
python scripts/workflow.py render-adapter --project <temp-level-project> --platform codex
```

Also render `claude-code` and `cursor` for at least one LEVEL 2 project. Verify generated files contain `core/project-vibe-spec/PVS.md`, the Bridge path, the expected LEVEL number, and no external install instruction.

Expected: every command exits 0. Temporary directories may be removed only after resolving and verifying their exact paths remain under the intended temp root.

- [ ] **Step 6: Run installer lifecycle verification**

Run:

```powershell
python -m unittest tests.test_install_integration tests.test_lifecycle_scripts -v
```

Then run PowerShell project-scope Dry Run against a fresh temporary project and record the PVS file count, target path, and absence of writes. If Bash is available, repeat using `install.sh`; otherwise record POSIX runtime verification as not executed.

- [ ] **Step 7: Static safety and consistency scans**

Run:

```powershell
rg -n -i "git\s+clone.*project-vibe-spec|\$project-vibe-spec|skills[/\\]project-vibe-spec" -g "*.md" -g "*.py" -g "*.ps1" -g "*.sh" .
rg -n -i "\b(TODO|TBD|FIXME|CHANGEME)\b" -g "*.md" .
rg --files core/project-vibe-spec
git diff --check
git status --short --branch
git diff --stat
```

Expected: external-install scan matches only the validator pattern/tests and `SOURCE.md` provenance where explicitly allowed; placeholder scan has no public contract hits; exactly one `SKILL.md` exists; diff check passes.

- [ ] **Step 8: Review every changed path against scope**

Compare `git status --porcelain=v1 -uall` with the Planned File Map. Stop if any unrelated path appears. Do not use `git add -A`.

- [ ] **Step 9: Update readiness evidence**

Write exact commands, return codes, test counts, platform results, unexecuted checks, independent-PVS behavior, and remaining risks into `docs/release/0.4.0-readiness.md`.

- [ ] **Step 10: Final local commit Gate**

Do not commit unless the user authorizes it after seeing the final diff and verification summary. If authorized, stage only the paths listed by `git status` that belong to this plan and use a message such as:

```powershell
git commit -m "release: embed project vibe spec in 0.4.0"
```

Do not push, create a PR, publish a Release, install into the real user Skills directory, or remove an independent PVS without separate authorization and post-action verification.

---

## Final Review Checklist

- [ ] Root `SKILL.md` is the only `SKILL.md` in the package.
- [ ] `core/project-vibe-spec/PVS.md`, both references, all 17 templates, and `SOURCE.md` are present.
- [ ] Source commit `dae5315` and root MIT coverage are recorded.
- [ ] PVS starter is the only default source for overlapping LEVEL 2 governance responsibilities.
- [ ] Existing overlapping templates remain present as compatibility entries.
- [ ] LEVEL 1 uses only PVS-Lite; LEVEL 2 uses full PVS; LEVEL 3 does not force a full pack; LEVEL 4 remains analysis-only.
- [ ] Runtime never asks for or falls back to an external PVS Skill.
- [ ] Install/update preflight validates the package before replacement and copies `core/`.
- [ ] Independent `project-vibe-spec` is detected only for warning and is never changed.
- [ ] Read-only validate never mutates state; explicit writes update workflow version with backup/history.
- [ ] Version, Schema, evals, changelog, and readiness docs agree on 0.4.0.
- [ ] Unit tests, Doctor, package validation, four-level init, adapters, and temporary install checks are reported truthfully.
- [ ] No deletion, real installation, commit, push, PR, deployment, or Release occurred without the required user Gate.
