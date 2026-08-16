# Project Level Workflow

一套 LEVEL 1 / LEVEL 2 优先、面向个人开发与长期接管的四级项目工作流。LEVEL 表示项目责任模式；LEVEL 1–3 对用户只展示 `AUTO`、`CONFIRM`、`MANUAL_ONLY`，在必要确认前保留事实、证据和用户决定。

## 四个 LEVEL

| LEVEL | 责任模式 | 适用项目 | 核心流程 |
| --- | --- | --- | --- |
| 1 | 快速开发与完整项目记忆 | 离线工具、脚本、Skill、插件、游戏 Mod、原型、静态页面和版本化下载物 | 实现—运行—观察—调整；稳定认知 + Ledger/小记录；集中验收 |
| 2 | 完整 PVS 持续运营 | 自己负责且承担账户、权限、云端数据、服务、部署、备份、回滚、监控或支持责任 | 全量包内 PVS；Phase 0 → Phase N、范围冻结、DoD 和持续运营 |
| 3 | 已有、团队与开源项目改进 | 参与他人、团队、公司或开源仓库 | 复用 Issue、PR、CHANGELOG、ADR；轻量 Change Record、基线、回归和交接 |
| 4 | 复杂自动化参考与路由 | 大型产品、多系统编排、复杂自动化和多人协作 | 先分析，负责人确认后可实施；十节点参考，外部专业能力只路由 |

“持续更新”和“持续运营”不是同一个判断。重新打包、上传新版本供用户下载，或更新一份静态页面，只要没有线上用户状态、云端业务数据、持续在线服务和运行责任，仍然默认 LEVEL 1。持续运营指需要长期承担服务可用性、用户/权限、数据、发布、备份、回滚、监控、反馈或支持责任，通常进入 LEVEL 2。

[`LEVEL.md`](LEVEL.md) 是四个等级的唯一权威流程源。0.3.0 起不再保留分散的四份活动 SOP 或旧三级兼容入口，避免同一规则在多个文件间重复；历史数字语义只在状态迁移协议中保留。

## 选择顺序

1. 参与他人、团队、公司或开源仓库？推荐 LEVEL 3。
2. 自己负责且需要线上运行和持续运营？推荐 LEVEL 2。
3. 只是离线、静态或可下载交付物，更新时重新打包/上传即可？推荐 LEVEL 1。
4. 大型、多系统或复杂自动化项目？推荐 LEVEL 4；先分析并确认实现边界。
5. 再选择 `AUTO`、`CONFIRM` 或 `MANUAL_ONLY`；内部 R1–R4 仅用于兼容和判断。

“以后可能更新”不能单独触发升级。无法区分时，列出事实、假设和替代 LEVEL，等待项目负责人确认。

## 双层文档与包内 PVS

完整 PVS 治理规则和 starter 模板内嵌在 `core/project-vibe-spec/PVS.md` 及其资源目录。安装本包后只显示一个 `project-level-workflow` Skill，不需要第二次下载 PVS。模板职责以 `templates/template-map.json` 为准。

稳定认知层回答“项目现在是什么”：`AGENTS.md`、`DOCUMENT_MAP.md`、目标、范围、核心路径、架构、模块、调用、数据、依赖、构建、测试和交付。演进记录层回答“为什么变成这样”：Requirements、Decisions、Progress、Bug、CHANGELOG、Release Record 和验证证据。

LEVEL 1 建立完整项目记忆，但小变化只需 Progress/Changelog，小功能和 Bug 使用轻量 Change Record；跨模块变化才增加详细 REQ/DEC/PROG 并同步架构事实。

LEVEL 2 全量使用包内 PVS，默认覆盖 AGENTS、DOCUMENT_MAP、PDD/PRD、Requirements、Decisions、Progress、业务流、UI、架构、API、数据、权限、部署、监控、备份、回滚、运营、Bug、待验证和版本记录。普通 Phase 达成 DoD 后自动继续，不形成重复审批。

LEVEL 3 优先复用已有仓库事实，不创建平行完整 PVS 文档树。LEVEL 4 先分析，负责人确认后可实施；专业 Skill 缺失时说明来源、用途、权限与降级方案，安装仍需确认。

## 状态与兼容迁移

状态保存在 `.project-workflow/state.json` 和 `docs/project-workflow/STATUS.md`，更新前写入 `state.backup.json`。Schema `1.1.0` / workflow `0.4.0` 升级到 `2.0` / `1.0` 时保持 LEVEL 1–4 不变；LEVEL 4 保持分析阶段并进入执行确认。更老状态数字语义继续兼容：

```text
旧 LEVEL 1 → 新 LEVEL 1
旧 LEVEL 2 → 新 LEVEL 3
旧 LEVEL 3 → 新 LEVEL 4
```

迁移会在状态和 `STATUS.md` 记录旧/新等级、版本和原因。`0.4.0` 的 LEVEL 1–3 不新增语义 Gate；更老数字重映射仍等待确认。

## 支持平台

- Codex：以 Agent Skill 方式安装。
- Claude Code：以项目或个人 Skill 方式安装。
- Cursor：生成项目级 `.cursor/rules/*.mdc` 与精简入口。

适配器只引用 `LEVEL.md` 的当前等级章节、状态和分层策略，不复制完整流程。

## 安装、更新与卸载

先 Clone 仓库，在包根目录审查并运行对应安装器。建议先使用 Dry Run：

```powershell
./scripts/install.ps1 -Platform codex -Scope user -DryRun
./scripts/install.ps1 -Platform codex -Scope user
./scripts/install.ps1 -Platform cursor -Scope project -ProjectPath 'D:\path\to\project' -DryRun
```

```sh
./scripts/install.sh --platform claude-code --scope user --dry-run
./scripts/install.sh --platform claude-code --scope user
```

项目级安装后，在目标项目根目录初始化已确认的等级：

```sh
python .cursor/skills/project-level-workflow/scripts/workflow.py init --project . --level 1
python .cursor/skills/project-level-workflow/scripts/workflow.py render-adapter --project . --platform cursor
```

更新器会先运行 Doctor；项目级状态存在时先执行迁移，再把旧安装移动到带时间戳的 `backup` 目录。卸载只删除托管 Skill 目录，默认保留项目中的 `.project-workflow/` 与 `docs/project-workflow/`。

## 工作方式与安全默认值

1. 读取项目规则、文档地图和相关状态。
2. 按选择协议推荐并等待 LEVEL 确认。
3. 建立或复用稳定认知层与演进记录层。
4. 在批准范围内按 `AUTO` 连续推进；需要决策时改为 `CONFIRM`，只允许人工执行时标记 `MANUAL_ONLY`。
5. 记录实际验证；未运行的检查只能写成待验证。

公开远程写入默认关闭：

```text
allow_push_own_branch=false
allow_create_draft_pr=false
```

所有 LEVEL 的 push、Draft PR、Merge、Tag 和 Release 自动选择 Codex GitHub 插件：先只读核对并合并远程动作计划，执行前一次确认，完成后远端回读验证。禁止 Force Push、改写公共历史、提交用户无关修改、自动生产发布和自动公开宣传。

## 版本

公共版本只使用 `X.X`，本版为 `1.0`；Git Tag 为 `v1.0`，状态 Schema 为独立的 `2.0`。读取和迁移兼容历史 `0.4.0` 三段状态，但新包和新状态不再写三段版本。

## 开发验证

核心实现只使用 Python 3.10+ 标准库：

```sh
python -m unittest discover -s tests -v
python scripts/workflow.py doctor --package-root .
python scripts/workflow.py validate-package --package-root .
```

四个等级都支持：

```sh
python scripts/workflow.py init --project <temporary-project> --level 1
python scripts/workflow.py init --project <temporary-project> --level 2
python scripts/workflow.py init --project <temporary-project> --level 3
python scripts/workflow.py init --project <temporary-project> --level 4
```

## 许可证

[MIT License](LICENSE)
