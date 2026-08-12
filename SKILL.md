---
name: project-level-workflow
description: 当用户要开发新项目、改进已有或开源项目、建设长期运营产品、分析复杂项目需求、判断项目 LEVEL，或按标准流程推进到人工 Gate 时使用。支持 LEVEL 1–4，并按 PVS-Lite、完整 PVS、已有项目回归和需求分析分层保存证据。
compatibility: Codex、Claude Code、Cursor；核心脚本需要 Python 3.10+，安装器支持 PowerShell 或 POSIX Shell。
---

# Project Level Workflow

把项目推进变成可恢复、可验证、按责任模式和风险授权的流程。LEVEL 表示项目责任模式，R1–R4 表示当前动作风险；低等级不代表可以跳过高风险操作前的检查。

## 触发检查

在执行前确认用户确实要求推进项目、初始化流程或判断等级。

应使用本 Skill：

- 开发小工具、插件、网页、游戏 Mod、App、SaaS、小程序或客户端。
- 修改已有项目、团队仓库或 GitHub 开源项目。
- 建设需要上线并持续运营的自有产品或在线服务。
- 分析大型产品、多系统自动化或复杂编排的需求。
- 判断项目应采用哪个 LEVEL，或继续到下一个人工 Gate。
- 用户明确指定 LEVEL 1、LEVEL 2、LEVEL 3 或 LEVEL 4。

不要使用本 Skill：

- 只问知识、解释代码、只读 Review 或纯诊断且没有修改授权。
- 明确要求创建、修改或调试 Agent Skill；此时优先使用专门的 Skill 创建流程。

如果请求同时包含诊断和修复，先完成诊断并确认根因，再进入本流程。

## 第一步：发现项目与状态

1. 确定项目根目录，不对不明确的路径执行写操作。
2. 从根目录向上读取适用的 `AGENTS.md`、`CLAUDE.md`、`.cursor/rules/`、`CONTRIBUTING.md`、README 和项目文档。
3. 检查 `.project-workflow/state.json`；存在时先运行 `python scripts/workflow.py validate --project <项目根目录>`。
4. 验证通过后读取 `docs/project-workflow/STATUS.md` 和当前任务；状态与聊天、代码或项目规则冲突时展示差异并询问。
5. 状态不存在时进入 LEVEL 推荐，不直接创建大量文档或修改实现。

状态协议见 `references/state-protocol.md`；PVS 分层见 `references/project-vibe-spec-bridge.md`；外部能力路由见 `references/tool-routing.md`。

## 第二步：推荐并确认 LEVEL

按 `references/level-selection.md` 判断责任模式，不以代码行数或“以后可能更新”为唯一依据。选择顺序：

1. 他人、团队、公司或开源仓库的参与/改进 → LEVEL 3。
2. 自有、线上、需要持续运营并承担用户/数据/服务责任 → LEVEL 2。
3. 离线、静态或可下载交付，重新打包即可更新 → LEVEL 1。
4. 大型、多系统、复杂自动化或完整运营自动化 → LEVEL 4，当前只做需求分析。

输出：

- 推荐 LEVEL。
- 已确认事实与仍属假设的内容。
- 推荐理由，尤其是持续更新与持续运营的区别。
- 改用其他 LEVEL 会省略或增加什么。
- 需要项目负责人确认的问题。

用户明确确认前，不初始化正式流程、不写代码、不创建数据库、不部署、不创建远程资源。确认后读取根目录唯一权威文档 `LEVEL.md` 中当前等级的章节，不加载或维护分散的 LEVEL SOP。

## 第三步：初始化最小项目文档

运行：

```text
python scripts/workflow.py init --project <项目根目录> --level <1|2|3|4>
```

`init` 只写入 `.project-workflow/state.json`、`state.backup.json` 和 `docs/project-workflow/STATUS.md`，不未经确认生成大量项目文档。

- LEVEL 1：PVS-Lite 的 Project Brief、规则、文档地图、状态和 `pending-verification.md`；跨模块或高风险时再增加 REQ/决策。
- LEVEL 2：完整 PVS 的项目地图、PDD/PRD、Requirements/REQ、决策、业务流、UI/技术/API/数据、部署/运营、进度、待验证和交付文档。
- LEVEL 3：已有仓库项目地图、贡献/权限记录、变更提案、基线、问题复现、影响分析、回归、Review、PR 和交接记录。
- LEVEL 4：需求分析、范围、不做清单、MVP、方案比较、风险、验收和待确认事项；不创建代码实现文档，不自动拆开发任务。

模板位于 `templates/`；已有项目目录和事实文档优先，不能创建平行事实源。

## 第四步：按风险选择任务

读取 `references/risk-and-permissions.md`，记录目标、范围、不做、允许/禁止修改、验收标准、验证命令、风险等级和人工 Gate。未运行的检查写入 `pending-verification.md` 或状态的未决事项，不得标记为通过。

- R1：文档、模板、只读分析、独立小测试；可执行并留证据。
- R2：边界清晰的逻辑和内部 API；批准范围内执行，必须测试与 Review。
- R3：数据库、认证、权限、公共 API、部署配置；修改前和合并前人工批准。
- R4：生产数据、密钥、支付、不可逆迁移、生产发布；只分析和准备，不自主执行。

## 各 LEVEL 的实现边界

### LEVEL 1：PVS-Lite

以“实现—运行—观察—调整”为主，不要求每个小步骤都写测试或跑重型检查。完成或打包前集中做核心路径冒烟、构建/打包和必要人工验收；未运行项记录为待验证。仍然必须在删除数据、访问密钥或外部写入前做针对性检查和 Gate。

### LEVEL 2：完整 PVS 与持续运营

完整遵循 `project-vibe-spec` 的接管、需求、设计、数据、决策、进度、验证和交付流程。同步维护 PDD/PRD、REQ、业务流、UI/技术/API/数据/部署/运营和回滚文档。实现阶段不采用每改一步就跑大量完整测试的固定节奏，测试按风险、功能集成、里程碑和版本完成阶段集中安排；认证、权限、支付、生产数据、迁移、密钥和发布仍必须事前验证并经人工 Gate。

### LEVEL 3：已有与开源项目改进

保留原有仓库的项目地图、权限与贡献规则、修改前基线、问题复现、失败测试/人工复现、影响分析、受影响回归、CI、Review、PR、发布和交接责任。改动小不等于可以跳过基线与回归。

### LEVEL 4：只做需求分析

只分析机会/问题、目标用户、场景、范围、不做、MVP、验收、技术/数据/安全/运营/成本风险、方案取舍和待确认事项。不写代码、不改数据库、不部署、不接入生产、不做自动化实现、不自动拆开发任务。

## 状态迁移

旧状态迁移固定为：旧 LEVEL 1→新 LEVEL 1，旧 LEVEL 2→新 LEVEL 3，旧 LEVEL 3→新 LEVEL 4。迁移前写 `state.backup.json`，在 `STATUS.md` 记录旧/新等级、Schema、原因，并把 Gate 置为 `level-migration-review` 等待人工确认。旧 LEVEL 3 改为新 LEVEL 2 时，必须使用 `migrate --target-level 2 --approved-by ... --reason ...` 显式重确认，不能自动映射。

## 低风险执行循环与人工 Gate

读取相关实现、测试、配置和文档，建立修改前基线；一次完成一个最小可验证切片；按等级和风险运行必要检查；检查 Diff；同步文档、状态和证据。出现范围、架构、数据库、认证、权限、安全、生产、公开发布、外部 Provider 或高影响 Git 变化时停止并报告事实、证据、风险、方案和等待批准的动作。

Git 默认不推送、不创建 Draft PR；`allow_push_own_branch=false`、`allow_create_draft_pr=false`；Force Push、改写公共历史、主分支直推、Merge、Release 和生产写入禁止自动执行。Qima 只在能力缺口明确时提醒用户手动考虑，不得直接调用或自动串联。

## 平台适配

读取 `references/platform-compatibility.md`。Codex、Claude Code 和 Cursor 只处理路径、发现和格式差异，均引用 `LEVEL.md` 的当前等级章节，不重写等级流程。

## 每轮输出

报告当前 LEVEL、阶段、状态、本轮改动和原因、实际运行的命令及结果、本地 Git 状态、未执行检查、风险、下一步和是否停在人工 Gate。没有新鲜验证证据时，不声称任务完成。
