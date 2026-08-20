# ELX Level

<p align="right"><a href="README.md">简体中文</a></p>

<img src="assets/readme/hero.svg" alt="ELX Level: choose the right workflow depth and keep the full project memory" width="100%">

A four-level project workflow built for individual developers. It puts LEVEL 1 / LEVEL 2 first, keeps routine progress in `AUTO`, and pauses only important decisions in `CONFIRM` or `MANUAL_ONLY`.

## Quick Start in 3 Minutes

This example uses Windows, Codex, a project-scoped installation, and LEVEL 1. Review the Dry Run first; confirm the LEVEL before initializing the project.

```powershell
git clone https://github.com/Ee1ex/elx-level.git
Set-Location elx-level

$ProjectPath = 'D:\path\to\your-project'
./scripts/install.ps1 -Platform codex -Scope project -ProjectPath $ProjectPath -DryRun
./scripts/install.ps1 -Platform codex -Scope project -ProjectPath $ProjectPath

python "$ProjectPath\.codex\skills\elx-level\scripts\workflow.py" init --project $ProjectPath --level 1
python "$ProjectPath\.codex\skills\elx-level\scripts\workflow.py" status --project $ProjectPath
```

Initialization creates `.elx-level/state.json` and `docs/elx-level/STATUS.md`. Other platforms and installation scopes are covered below. [`LEVEL.md`](LEVEL.md) is the single authoritative source for all four LEVEL definitions.

## How It Works

<img src="assets/readme/workflow.svg" alt="How LEVEL, execution mode, project memory, and the GitHub delivery gate connect" width="100%">

1. **Responsibility sets the depth.** First decide whether you are building quickly, operating continuously, improving an existing repository, or orchestrating complex automation.
2. **Risk sets the pause point.** LEVEL 1–3 expose only `AUTO`, `CONFIRM`, and `MANUAL_ONLY`; routine implementation, tests, and local commits are not gates.
3. **Evidence becomes memory.** Goals, architecture, and current facts stay stable while decisions, changes, and verification accumulate for the next handoff.
4. **Public delivery is confirmed separately.** Push, PR, Merge, Tag, and Release route automatically to the Codex GitHub plugin, receive one consolidated confirmation, and are verified by reading GitHub back afterward.

## Choose the Right LEVEL

| LEVEL | Responsibility mode | Best suited to | Default approach |
| --- | --- | --- | --- |
| **1** | Fast development with complete project memory | Offline tools, scripts, Skills, plugins, mods, prototypes, static pages, and versioned downloads | Implement → run → observe → adjust; keep small changes in lightweight records |
| **2** | Complete PVS for continuous operations | Products for which you own accounts, permissions, cloud data, services, deployment, backup, rollback, monitoring, or support | Full embedded PVS; `Phase 0 → Phase N`, scope freeze, and DoD, with routine phases continuing automatically |
| **3** | Existing, team, and open-source project improvement | Other people's, team, company, or open-source repositories | Reuse Issues, PRs, CHANGELOG, and ADRs; add only a project map, Change Record, baseline, regression evidence, and handoff |
| **4** | Complex automation reference and routing | Large products, multi-system orchestration, complex automation, and multi-person collaboration | Analyze first, then implement after owner confirmation; use the ten nodes as a reference and route external professional Skills without embedding them |

The decision order is simple: prefer LEVEL 3 for existing or collaborative repositories; choose LEVEL 2 for online operation and ongoing responsibility; default offline, static, or downloadable deliverables to LEVEL 1; consider LEVEL 4 for large multi-system orchestration.

“May be updated later” does not mean “continuously operated.” Repackaging a download or updating a static page usually remains LEVEL 1. Long-term responsibility for availability, users, permissions, data, releases, and support usually moves the project to LEVEL 2.

## Two-Layer Project Memory

Project memory is not a document count. It means two kinds of information remain ready for handoff:

- The **stable cognition layer** answers “What is the project now?”: goals, scope, critical paths, architecture, modules, calls, data, dependencies, build, tests, and delivery.
- The **evolution record layer** answers “Why did it become this?”: Requirements, Decisions, Progress, Bugs, CHANGELOG, Release Records, and verification evidence.

LEVEL 1 establishes both layers, but a small feature or edit needs only Progress/Changelog or a lightweight Change Record. LEVEL 2 uses the full embedded PVS across product, requirements, decisions, business flow, UI, architecture, API, data, permissions, deployment, monitoring, backup, rollback, operations, Bugs, pending verification, and version history. LEVEL 3 reuses existing repository facts instead of creating a parallel documentation tree.

The complete governance rules and starter templates are embedded in [`core/project-vibe-spec/PVS.md`](core/project-vibe-spec/PVS.md), with responsibilities mapped in [`templates/template-map.json`](templates/template-map.json). Installing this package does not require a second PVS Skill download.

## Compatibility, Safety, and GitHub Delivery

Version `2.0` uses workflow `2.0` and schema `2.0`. Reading and migration remain compatible with historical three-part `0.4.0` state; after a safe refresh, new public versions use only two-part `X.X`. `migrate` copies the complete legacy `.project-workflow` directory to `.elx-level` while leaving the source unchanged; if both directories exist, it stops without overwriting either. LEVEL 1–4 from `0.4.0` keep their numeric meaning, while the old LEVEL 4 remains at its analysis boundary until execution is confirmed. Older states migrate by protocol: old LEVEL 1 → new LEVEL 1, old LEVEL 2 → new LEVEL 3, and old LEVEL 3 → new LEVEL 4.

These actions always require confirmation: bulk deletion, production data, secrets, payments, account permissions, irreversible migration, security reduction, production deployment, public publishing, outbound messages, Merge, and Release. Force Push and rewriting public history are prohibited.

Every LEVEL uses the same GitHub delivery contract. The plugin first reads the remote state, presents the branch and commits, file scope, test evidence, PR, Merge, Tag/Release, rollback, and unverified items, then requests one remote-operation confirmation. A success response is not completion; the Codex GitHub plugin must read the result back from GitHub.

## Platforms, Development Verification, and License

Codex, Claude Code, and Cursor are supported:

```powershell
./scripts/install.ps1 -Platform codex -Scope user -DryRun
./scripts/install.ps1 -Platform cursor -Scope project -ProjectPath 'D:\path\to\project' -DryRun
```

```sh
./scripts/install.sh --platform claude-code --scope user --dry-run
./scripts/install.sh --platform claude-code --scope user
```

Adapters reference only the current LEVEL, state, and layering strategy instead of copying the complete workflow. The updater runs Doctor first, explicitly migrates project state, and creates a timestamped backup before replacing the new installation. The uninstaller removes only `elx-level` and preserves `.elx-level/`, `docs/elx-level/`, the legacy `.project-workflow/`, and the legacy Skill installation by default.

Development verification uses only the Python 3.10+ standard library:

```sh
python -m unittest discover -s tests -v
python scripts/workflow.py doctor --package-root .
python scripts/workflow.py validate-package --package-root .
```

The current public version is `2.0`, with Git Tag target `v2.0`. The project is available under the [MIT License](LICENSE).
