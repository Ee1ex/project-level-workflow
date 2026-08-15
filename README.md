# Project Level Workflow

一套面向 AI Agent 的四级项目开发流程。LEVEL 表示项目责任模式，R1–R4 表示当前动作风险；两者分开判断，在人工 Gate 前保留事实、证据和用户决定。

## 四个 LEVEL

| LEVEL | 责任模式 | 适用项目 | 核心流程 |
| --- | --- | --- | --- |
| 1 | 快速验证与轻量交付 | 离线工具、脚本、Skill、插件、游戏 Mod、原型、静态页面、无用户系统的 Web 工具、版本化下载物 | PVS-Lite；快速实现，完成或打包前集中冒烟、构建/打包和人工验收 |
| 2 | 自有项目的可持续运营 | 自己负责、要上线并持续运营的 Web/App/小程序/在线服务；有账户、权限、云端数据、服务端逻辑、公开 API、定时任务或长期支持责任 | 完整 `project-vibe-spec`；维护需求、设计、数据、决策、进度、验证、发布、回滚和运营文档 |
| 3 | 已有与开源项目改进 | 参与他人、团队、公司或开源仓库，提交 Bug 修复、体验优化或功能 PR | 保留项目地图、权限与贡献规则、修改前基线、复现、受影响回归、CI、Review、PR 和交接 |
| 4 | 复杂项目需求分析 | 大型产品、多系统编排、复杂自动化、多人协作或完整运营自动化 | 当前只做机会/需求分析、范围、MVP、方案、风险、验收和待确认事项，不开发 |

“持续更新”和“持续运营”不是同一个判断。重新打包、上传新版本供用户下载，或更新一份静态页面，只要没有线上用户状态、云端业务数据、持续在线服务和运行责任，仍然默认 LEVEL 1。持续运营指需要长期承担服务可用性、用户/权限、数据、发布、备份、回滚、监控、反馈或支持责任，通常进入 LEVEL 2。

[`LEVEL.md`](LEVEL.md) 是四个等级的唯一权威流程源。0.3.0 起不再保留分散的四份活动 SOP 或旧三级兼容入口，避免同一规则在多个文件间重复；历史数字语义只在状态迁移协议中保留。

## 选择顺序

1. 参与他人、团队、公司或开源仓库？推荐 LEVEL 3。
2. 自己负责且需要线上运行和持续运营？推荐 LEVEL 2。
3. 只是离线、静态或可下载交付物，更新时重新打包/上传即可？推荐 LEVEL 1。
4. 大型、多系统或复杂自动化项目？推荐 LEVEL 4；第一版只做需求分析。
5. 再单独叠加当前动作的 R1–R4 风险和人工 Gate。

“以后可能更新”不能单独触发升级。无法区分时，列出事实、假设和替代 LEVEL，等待项目负责人确认。

## `project-vibe-spec` 分层

0.4.0 起，完整 PVS 治理规则和 starter 模板已内嵌在 `core/project-vibe-spec/PVS.md` 及其资源目录。安装本包后只显示一个 `project-level-workflow` Skill；四个 LEVEL 均不需要第二次下载或联网补齐 PVS。模板职责以 `templates/template-map.json` 为准。

LEVEL 1 使用 PVS-Lite：至少保留项目规则、`AGENTS.md`、`DOCUMENT_MAP.md`、Project Brief、`STATUS.md`、`state.json`/备份和必要的待验证事项；需求跨模块、持久化或高风险时再增加 REQ、决策或技术文档。

LEVEL 2 使用完整 PVS：复用已有文档目录，维护 PDD/PRD、Requirements/REQ、决策、业务流、UI/技术/API/数据/部署/运营文档及进度和验证证据。完整 PVS 不要求每次小改动都跑重型测试，测试按风险、功能集成、里程碑和版本完成阶段集中安排。

LEVEL 4 只建立分析材料和待确认记录；不写代码、不改数据库、不部署、不接入生产、不自动拆开发任务。

## 状态与兼容迁移

状态保存在 `.project-workflow/state.json` 和 `docs/project-workflow/STATUS.md`，更新前写入 `state.backup.json`。旧状态数字语义迁移为：

```text
旧 LEVEL 1 → 新 LEVEL 1
旧 LEVEL 2 → 新 LEVEL 3
旧 LEVEL 3 → 新 LEVEL 4
```

迁移会在状态和 `STATUS.md` 记录旧/新等级、Schema 版本和原因，并将迁移后的 Gate 置为待人工确认，不会静默批准。旧 LEVEL 3 若要改成新 LEVEL 2，必须使用显式重确认并留下批准人、原因和历史记录。

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
3. 只创建当前等级需要的最小文档。
4. 在批准范围内推进 R1/R2；R3/R4、生产、数据、密钥和公开发布停在人工 Gate。
5. 记录实际验证；未运行的检查只能写成待验证。

公开远程写入默认关闭：

```text
allow_push_own_branch=false
allow_create_draft_pr=false
```

禁止 Force Push、改写公共历史、提交用户无关修改、自动生产发布和自动公开宣传。外部 Plugin/服务不随本包安装，使用前仍需检查登录、授权、数据范围和费用。

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
