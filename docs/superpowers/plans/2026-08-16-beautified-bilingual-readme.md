# Beautified Bilingual README Implementation Plan

> **For Codex:** Execute this plan inline, task by task. Use test-driven development, inspect each diff, and make one local commit per task. Do not use sub-agents and do not perform remote GitHub writes.

**Goal:** Replace the Project Level Workflow repository homepage with a minimal, project-native bilingual README and two self-contained SVG diagrams while keeping the installed package complete.

**Architecture:** Markdown remains the searchable and copyable source of product truth. Two language-isomorphic README files share static local SVG assets. Repository and installer contract tests enforce language parity, safe asset constraints, and package-copy completeness without changing workflow runtime behavior.

**Tech Stack:** Markdown, SVG 1.1-compatible markup, Python `unittest`, PowerShell, POSIX shell, Git.

---

## Task 1: Lock the bilingual README and package contracts

**Files:**
- Modify: `tests/test_repository_contract.py`
- Modify: `tests/test_lifecycle_scripts.py`
- Modify: `tests/test_install_integration.py`
- Test: `tests/test_repository_contract.py`
- Test: `tests/test_lifecycle_scripts.py`
- Test: `tests/test_install_integration.py`

### Step 1: Add failing repository contract tests

Add tests that require:

- `README.en.md`, `assets/readme/hero.svg`, and `assets/readme/workflow.svg` to exist.
- `README.md` to link to `README.en.md`, and `README.en.md` to link back to `README.md`.
- Both README files to expose these seven H2 sections in the same order: Hero content has no H2; then Quick Start, How It Works, Choose a LEVEL, Two-Layer Project Memory, Compatibility/Safety/GitHub Delivery, and Platforms/Development Verification/License.
- Both SVGs to contain a `viewBox`, `<title>`, and `<desc>`.
- README and SVG sources to reject remote image URLs, remote fonts, scripts, `foreignObject`, animation, visitor counters, trophies, dynamic statistics, and badge walls.
- Required 1.0 terms to remain discoverable: `LEVEL 1 / LEVEL 2`, `AUTO`, `CONFIRM`, `MANUAL_ONLY`, `Phase 0`, `GitHub`, `X.X`, and `core/project-vibe-spec/PVS.md`; the Chinese README additionally retains `稳定认知层`, `演进记录层`, `负责人确认后可实施`, and `GitHub 插件`.

Keep assertions semantic: inspect headings, links, paths, and forbidden tokens rather than snapshots of prose.

### Step 2: Add failing installer contract tests

Extend lifecycle script checks so both `scripts/install.ps1` and `scripts/install.sh` name `README.en.md` and `assets` in their package item lists.

Extend the PowerShell integration installation test so its temporary installed Skill must contain:

```text
README.en.md
assets/readme/hero.svg
assets/readme/workflow.svg
```

Do not modify update tests because update scripts delegate package copying to the installers.

### Step 3: Run the focused tests and confirm the intended failure

Run:

```powershell
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_repository_contract tests.test_lifecycle_scripts tests.test_install_integration -v
```

Expected: FAIL because the English README and SVG assets do not exist and the installers do not list them. Confirm failures are contract failures, not syntax or environment errors.

### Step 4: Inspect the test-only diff

Run:

```powershell
git diff -- tests/test_repository_contract.py tests/test_lifecycle_scripts.py tests/test_install_integration.py
git diff --check
```

Expected: only the three intended test files change; no whitespace errors.

### Step 5: Commit the red tests

```powershell
git add tests/test_repository_contract.py tests/test_lifecycle_scripts.py tests/test_install_integration.py
git commit -m "test: define bilingual README contract"
```

Expected: one local commit containing only the failing contract tests.

## Task 2: Include bilingual documentation assets in installations

**Files:**
- Modify: `scripts/install.ps1`
- Modify: `scripts/install.sh`
- Test: `tests/test_lifecycle_scripts.py`
- Test: `tests/test_install_integration.py`

### Step 1: Make the smallest installer changes

Add `README.en.md` and `assets` to the existing package item arrays in both installers. Preserve their current copy, backup, dry-run, platform, and scope behavior.

### Step 2: Run installer tests

Run:

```powershell
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_lifecycle_scripts tests.test_install_integration -v
```

Expected: installer list assertions pass. The integration test may still fail only because the source assets and English README are introduced in later tasks; no other failure is acceptable.

### Step 3: Inspect the diff

Run:

```powershell
git diff -- scripts/install.ps1 scripts/install.sh
git diff --check
```

Expected: two item-list additions only.

### Step 4: Commit the installer change

```powershell
git add scripts/install.ps1 scripts/install.sh
git commit -m "fix: package bilingual README assets"
```

Expected: one local commit containing only installer list changes.

## Task 3: Build the self-contained SVG system

**Files:**
- Create: `assets/readme/hero.svg`
- Create: `assets/readme/workflow.svg`
- Test: `tests/test_repository_contract.py`

### Step 1: Create the Hero SVG

Create `assets/readme/hero.svg` with `viewBox="0 0 1200 520"`, accessible `<title>` and `<desc>`, and only inline SVG primitives. Use:

```text
background  #09111F
foreground  #F6F8FB
accent      #65E6D1
muted       #9EACBF
```

Show the project name, `Choose the right workflow depth. Keep the full project memory.`, a restrained LEVEL 1–4 path, and `AUTO / CONFIRM / MANUAL_ONLY`. Keep essential text at 20 SVG units or larger and auxiliary labels at 18 or larger.

### Step 2: Create the workflow SVG

Create `assets/readme/workflow.svg` with `viewBox="0 0 1200 420"`, accessible `<title>` and `<desc>`, and the left-to-right relationship:

```text
LEVEL 1–4 -> AUTO / CONFIRM / MANUAL_ONLY -> Evidence & Memory -> GitHub Delivery Gate
```

Use the same palette, spacing rhythm, thin strokes, and 8–10 unit corner radii. Do not include detailed risk rules in the diagram.

### Step 3: Run the SVG contract tests

Run:

```powershell
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_repository_contract -v
```

Expected: SVG existence, accessibility, and safety assertions pass; README assertions still fail until Tasks 4 and 5.

### Step 4: Inspect the SVG sources and diff

Run:

```powershell
rg -n "https?://|@import|foreignObject|<script|<animate|<image" assets/readme
git diff -- assets/readme/hero.svg assets/readme/workflow.svg
git diff --check
```

Expected: `rg` returns no matches; the diff contains only the two SVGs with no whitespace errors.

### Step 5: Commit the visual assets

```powershell
git add assets/readme/hero.svg assets/readme/workflow.svg
git commit -m "feat: add project-native README visuals"
```

Expected: one local commit containing only the two SVG files.

## Task 4: Rewrite the Chinese README homepage

**Files:**
- Modify: `README.md`
- Test: `tests/test_repository_contract.py`

### Step 1: Replace the homepage content

Rewrite `README.md` in this exact reading order:

1. Hero and English-language switch.
2. `## 3 分钟快速开始`.
3. `## 它如何工作`.
4. `## 选对 LEVEL`.
5. `## 双层项目记忆`.
6. `## 兼容、安全与 GitHub 交付`.
7. `## 平台、开发验证与许可证`.

Use `assets/readme/hero.svg` and `assets/readme/workflow.svg` at `width="100%"`. Put commands in Markdown code blocks, not SVG. Preserve the complete clone -> dry run -> install -> `init` -> `status` first-success path.

Keep the public 1.0 semantics concise and accurate:

- LEVEL 1/2 personal-first positioning and all four responsibility modes.
- `AUTO`, `CONFIRM`, and `MANUAL_ONLY` as user-facing execution states.
- `Phase 0 → Phase N`, scope freeze, and DoD for LEVEL 2 without routine phase gates.
- Existing-repository reuse for LEVEL 3.
- LEVEL 4 analysis first, then implementation after owner confirmation, with external Skill routing only.
- Stable cognition and evolution record layers, with embedded PVS at `core/project-vibe-spec/PVS.md`.
- `0.4.0` migration compatibility, backup state, old LEVEL 4 boundary, high-risk confirmations, GitHub plugin routing, no force push/public-history rewrite, and public `X.X` versions.
- Codex, Claude Code, Cursor, update/uninstall facts, validation commands, and MIT.

Avoid repeated explanations, badge walls, fabricated claims, and fixed test-count claims.

### Step 2: Run the Chinese README contract tests

Run:

```powershell
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_repository_contract -v
```

Expected: Chinese content and link assertions pass; English parity assertions still fail because `README.en.md` does not yet exist.

### Step 3: Run the README audit

Run:

```powershell
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\admin\.codex\skills\beautify-github-readme\scripts\audit_readme.py' README.md
```

Expected: audit completes without broken local-image, missing-alt, forbidden-dynamic-component, or heading-order findings. Treat advisory prose-density findings as review input, not automatic failure.

### Step 4: Inspect and commit

Run:

```powershell
git diff -- README.md
git diff --check
git add README.md
git commit -m "docs: redesign Chinese README homepage"
```

Expected: one local commit containing only `README.md`.

## Task 5: Add the isomorphic English README

**Files:**
- Create: `README.en.md`
- Test: `tests/test_repository_contract.py`
- Test: `tests/test_install_integration.py`

### Step 1: Write the full English version

Create `README.en.md` with the exact translated H2 order:

1. `## Quick Start in 3 Minutes`.
2. `## How It Works`.
3. `## Choose the Right LEVEL`.
4. `## Two-Layer Project Memory`.
5. `## Compatibility, Safety, and GitHub Delivery`.
6. `## Platforms, Development Verification, and License`.

Link back to `README.md`, reuse the same SVG assets, preserve identical commands and facts, and translate the Chinese content without adding or removing product promises.

### Step 2: Run README and installation tests

Run:

```powershell
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_repository_contract tests.test_lifecycle_scripts tests.test_install_integration -v
```

Expected: all bilingual repository and installed-package contracts pass.

### Step 3: Run the English README audit

Run:

```powershell
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\admin\.codex\skills\beautify-github-readme\scripts\audit_readme.py' README.en.md
```

Expected: audit completes without broken local-image, missing-alt, forbidden-dynamic-component, or heading-order findings.

### Step 4: Check language parity and commit

Run a short read-only PowerShell comparison that extracts H2 headings and fenced command blocks from both README files. Confirm there are six H2 sections in matching semantic order and command blocks are identical apart from prose-language comments.

Then run:

```powershell
git diff -- README.en.md
git diff --check
git add README.en.md
git commit -m "docs: add English README homepage"
```

Expected: one local commit containing only `README.en.md`.

## Task 6: Render, audit, and close the branch locally

**Files:**
- Verify: `README.md`
- Verify: `README.en.md`
- Verify: `assets/readme/hero.svg`
- Verify: `assets/readme/workflow.svg`
- Verify: all changed tests and installers

### Step 1: Render wide and narrow SVG previews

Use an available local SVG renderer or browser screenshot path to render each SVG at 900 px and 360 px widths. Save previews outside the repository or under ignored `.superpowers/`; do not add render artifacts to Git.

Inspect all four previews for clipped text, overlaps, minimum readable type, contrast, balanced whitespace, and visible container edges on both light and dark surrounding backgrounds. If a defect is found, patch the SVG, rerun Task 3 checks, and amend only by creating a new local fix commit (do not rewrite earlier history).

### Step 2: Run both README audits

```powershell
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\admin\.codex\skills\beautify-github-readme\scripts\audit_readme.py' README.md
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\admin\.codex\skills\beautify-github-readme\scripts\audit_readme.py' README.en.md
```

Expected: no blocking findings.

### Step 3: Run full project verification

```powershell
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests -v
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/workflow.py doctor --package-root .
& 'C:\Users\admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/workflow.py validate-package --package-root .
git diff origin/main...HEAD --check
```

Expected: complete test suite passes; Doctor reports PASS; package validation reports PASS; diff check emits no errors.

### Step 4: Inspect scope and working tree

```powershell
git status --short --branch
git diff --stat origin/main...HEAD
git diff --name-status origin/main...HEAD
git log --oneline origin/main..HEAD
```

Expected: committed branch scope is limited to the approved design, plan, tests, two installers, two README files, and two SVG assets. `.superpowers/` remains untracked and excluded. No version, runtime, schema, LEVEL, release, or installed user-Skill file changes exist.

### Step 5: Create a verification closeout commit only if needed

If verification required source corrections, commit each coherent correction with a specific message and rerun the affected checks. If no tracked file changed, do not create an empty commit.

### Step 6: Prepare the remote-operation handoff without executing it

Report:

- Branch and local commits.
- Changed-file scope.
- Exact verification evidence.
- Proposed PR title and body.
- Proposed merge method.
- Explicit statement that this README-only change does not create a new tag or Release.
- Rollback approach and any unverified visual or external-link items.

Stop before push, PR creation, merge, tag, or Release. Those actions require one fresh explicit confirmation and GitHub-plugin readback after execution.

## Plan self-check

- Spec coverage: all seven reading stages, bilingual parity, two SVGs, installer completeness, safety constraints, and verification are mapped to tasks.
- Placeholder check: no `TODO`, `TBD`, omitted implementation decision, or unspecified file remains.
- Interface consistency: repository tests, both installer item lists, integration installation output, README links, and SVG paths use the same exact filenames.
- Scope control: no LEVEL semantics, workflow runtime, state schema, public version, tag, Release, installed user Skill, or remote repository state is changed.
