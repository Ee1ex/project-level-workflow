---
name: project-level-workflow
description: 当用户要开发新项目、改进已有或开源项目、建设长期运营产品、判断项目 LEVEL、按标准流程推进，或继续到下一个人工 Gate 时使用。根据风险推荐 LEVEL 1/2/3，确认后自动推进低风险工作并保存证据；纯问答、只读审查、单纯诊断和 Skill 创建请求不触发。
compatibility: Codex、Claude Code、Cursor；核心脚本需要 Python 3.10+，安装器支持 PowerShell 或 POSIX Shell。
---

# Project Level Workflow

把项目推进变成可恢复、可验证、按风险授权的流程。自动完成已经获批的低风险工作，在方向、数据、安全、生产和公开发布等人工 Gate 前停止。

## 触发检查

在执行前确认用户是否真的要求推进项目。

应使用本 Skill：

- 开发小工具、插件、网页、游戏 Mod、App、SaaS、小程序或客户端。
- 修改已有项目、团队仓库或 GitHub 开源项目。
- 判断项目应采用哪个 LEVEL。
- 按标准流程开始、继续或推进到下一个人工 Gate。
- 用户明确指定 LEVEL 1、LEVEL 2 或 LEVEL 3。

不要使用本 Skill：

- 用户只问知识、要求解释代码或了解现状。
- 用户只要求 Review、诊断或报告，没有授权修改或推进。
- 用户明确要求跳过这套流程。
- 用户要创建、修改或调试 Agent Skill；这类请求优先使用专门的 Skill 创建流程。

如果意图同时包含“诊断”和“修复”，先完成诊断，确认根因后再进入本流程。

## 第一步：发现项目与状态

1. 确定项目根目录，不对不明确的路径执行写操作。
2. 读取根目录和父目录适用的 `AGENTS.md`、`CLAUDE.md`、`.cursor/rules/`、`CONTRIBUTING.md`、README 与项目文档。
3. 检查 `.project-workflow/state.json`。
4. 状态存在时，先运行 `python scripts/workflow.py validate --project <项目根目录>`；验证通过后读取 `docs/project-workflow/STATUS.md` 和当前任务。
5. 状态不存在时，进入 LEVEL 推荐；不要直接创建大量文档或修改代码。
6. 状态、聊天、代码或项目规则互相冲突时，列出差异并询问，不自行选择权威版本。

状态协议详见 [references/state-protocol.md](references/state-protocol.md)。

## 第二步：推荐并确认 LEVEL

按 [references/level-selection.md](references/level-selection.md) 判断，不以代码行数作为唯一标准。风险高于规模时按更高 LEVEL 执行。

给出：

- 推荐 LEVEL。
- 已确认事实与仍属假设的内容。
- 推荐理由。
- 如果改用其他 LEVEL 会省略或增加什么。
- 需要用户确认的问题。

用户未明确确认 LEVEL 前，不初始化正式流程、不写代码、不创建数据库、不创建远程资源。

确认后只读取一份权威 SOP：

| LEVEL | 权威 SOP |
| --- | --- |
| 1 | `LEVEL1-小型项目开发流程.md` |
| 2 | `LEVEL2-已有与开源项目改进流程.md` |
| 3 | `LEVEL3-持续运营产品开发流程.md` |

不要同时加载三份 SOP。只有出现升级或降级判断时才读取另一份的边界部分。

## 第三步：初始化最小项目文档

运行状态初始化命令，并按 LEVEL 只创建最小文档包：

```text
python scripts/workflow.py init --project <项目根目录> --level <1|2|3>
```

LEVEL 1：

- `project-brief.md`
- `acceptance-checklist.md`（需要最终验收时）
- `README.md`（对外发布时）

LEVEL 2：

- `project-map.md`
- `change-proposal.md` 或仓库 Issue
- 简短技术方案、测试与回归计划

LEVEL 3：

- `idea-review.md`
- PRD、体验设计、技术方案、任务卡
- 测试、发布、回滚和运营文档

模板位于 `templates/`。仓库已有模板时优先使用原模板，并把本流程要求映射进去，避免维护两套平行文档。

## 第四步：选择最小任务并分类风险

读取 [references/risk-and-permissions.md](references/risk-and-permissions.md)，为当前任务写清：

- 目标和关联需求。
- 范围与明确不做。
- 允许和禁止修改的文件或模块。
- 验收标准和验证命令。
- 风险等级 R1、R2、R3 或 R4。
- 当前自动权限和人工 Gate。

没有可观察验收标准时，不开始实现。

## 第五步：低风险自动执行循环

对已经批准范围内的 R1/R2 任务，持续执行以下循环，直到当前阶段完成或遇到 Gate：

1. 读取相关文件、调用链和现有测试，解释当前逻辑与最小改动点。
2. 记录修改前基线。Bug 修复先建立可重复失败证据。
3. 一次只实现一个最小纵向切片，不做无关重构。
4. 每完成一个小步就运行对应测试或检查。
5. 检查 Diff，排除用户原有修改、无关格式化、密钥、日志和构建产物。
6. 更新实现文档、验证证据、`state.json` 与 `STATUS.md`。
7. 验证通过后创建小而明确的本地提交。
8. 当前阶段未完成时选择下一个最小任务；阶段完成时生成 Gate 报告并停止。

验证失败时先做一次根因诊断和一次有证据的修正。根因仍不明确、范围扩大或需要 R3/R4 操作时停止，不删除测试、降低断言或跳过检查来伪造成功。

## Git 与 Draft PR

执行任何 Git 写入前，读取 [references/git-and-draft-pr.md](references/git-and-draft-pr.md)，先运行策略检查并保存证据。

自动本地 Git 仅适用于本 Skill 创建或明确接管的分支和任务范围。
公开配置始终从 `allow_push_own_branch=false`、`allow_create_draft_pr=false` 开始；只有用户在自己的项目状态中显式开启后，策略层才会放行相应远端动作。

- 可自动创建功能分支或 worktree。
- 可在验证通过后创建本地提交。
- 只有 `allow_push_own_branch=true` 时才可推送本 Skill 创建的功能分支。
- 只有 `allow_create_draft_pr=true` 时才可创建或更新 Draft PR。
- Push 或 Draft PR 前再次展示 Remote、分支、提交范围和验证结果。

修改他人分支、公开评论、转为 Ready、合并、Release、删除远程分支、Force Push、改写公共历史都必须停止；其中 Force Push 和改写公共历史禁止执行。

工作区存在用户未提交修改时保留原状。无法隔离或与任务文件重叠时询问，不自动 Stash、Reset 或提交无关修改。

## 人工 Gate

出现以下任一情况立即停止：

- LEVEL、目标、范围、验收或技术方向存在会显著改变结果的歧义。
- 数据库、认证、权限、支付、隐私、合规、安全或公共 API 变化。
- 生产权限、密钥、数据删除、不可逆迁移或生产部署。
- 需要安装或授权新的外部 Provider，或迁移现有 Provider。
- 测试失败原因不明、回滚不可用或证据不足。
- 需要 Git 高影响远程动作。
- 准备公开发布产品、Release 或宣传内容。

Gate 报告固定包含：

1. 当前 LEVEL、阶段和任务。
2. 已确认事实。
3. 已完成内容和验证证据。
4. 未知项、风险和失败影响。
5. 可选方案及取舍。
6. 推荐决策与理由。
7. 等待用户批准的具体动作。

用户没有明确批准前，不改变 Gate 状态。批准后使用 `transition` 更新状态，再继续执行。

## 工具路由

需要外部能力时读取 [references/tool-routing.md](references/tool-routing.md)。

- Product Design、Supabase、GitHub、Vercel、Netlify 等能力都必须先检查安装、登录、授权和技术栈匹配。
- 工具缺失时优先走通用流程并记录未执行项，不因安装工具阻塞核心路径。
- Qima 只能提醒用户在当前阶段手动考虑相应 Skill，不得直接调用、自动串联或套用不匹配的固定技术栈。
- 外部工具不能绕过风险等级、项目规则和人工 Gate。

## 平台适配

读取 [references/platform-compatibility.md](references/platform-compatibility.md)。

- Codex 使用共享 `SKILL.md` 和项目 `AGENTS.md`。
- Claude Code 使用共享 Skill 和精简 `CLAUDE.md` 入口。
- Cursor 使用 `.cursor/rules/project-level-workflow.mdc` 和项目 `AGENTS.md`。
- 平台适配层只处理路径、发现和格式差异，不得重写 LEVEL 流程。

## 每轮输出

完成一轮自动执行后，简洁报告：

- 当前 LEVEL、阶段和状态。
- 本轮改动与原因。
- 运行的验证和结果。
- 本地分支、提交和 Draft PR 状态。
- 未执行检查及原因。
- 当前风险、下一步和是否停在 Gate。

没有新鲜验证证据时，不声称任务完成。
