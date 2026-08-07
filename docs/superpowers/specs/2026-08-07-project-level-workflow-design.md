# Project Level Workflow Skill 设计规格

> 状态：待用户书面审阅
>
> 日期：2026-08-07
>
> 首版语言：中文
>
> 暂定 Skill 名称：`project-level-workflow`

## 1. 目标

把现有 LEVEL 1、LEVEL 2、LEVEL 3 开发流程做成一套可公开分发、可跨 Agent 使用的项目推进系统。

系统接收项目目标和现有上下文，推荐合适 LEVEL，经用户确认后自动创建阶段文档、执行低风险工作、运行验证、维护本地 Git 与 Draft PR，并持续推进到下一个人工 Gate。系统必须能在 Codex、Claude Code 和 Cursor 之间通过项目文件恢复状态，不依赖某一段聊天历史。

## 2. 第一性原理与设计结论

### 2.1 真正目标

真正目标不是把三篇 Markdown 塞进一个超长 Prompt，而是让以下能力稳定发生：

1. 选对流程等级。
2. 每个阶段都有明确输入、产出和完成证据。
3. 低风险工作尽量自动推进。
4. 高风险和不可逆决策必须停下来交给人。
5. 更换 Agent 或中断会话后能够继续。
6. 人读的 SOP 和 Agent 执行的标准不分叉。

### 2.2 已确认事实

- 三份 LEVEL SOP 已存在，并已整合用户提供的本地文档、两篇开发流程文章和工具资料。
- 用户允许自动创建本地分支、worktree 和本地提交。
- 用户允许自动推送 Skill 自己创建的功能分支，并创建或更新 Draft PR。
- 转为 Ready、公开评论、合并、Release、删除远程分支和其他高影响远程写入必须经过人工 Gate。
- Qima 只在适用时提醒用户，不直接调用。
- 首版只提供中文，但需要兼容 Codex、Claude Code 和 Cursor。
- 需要上传 GitHub，支持他人安装和更新。

### 2.3 关键限制

- `SKILL.md` 和规则文件本质上是 Agent 指令，不是操作系统级安全边界。真正的工具权限仍由 Codex、Claude Code、Cursor、GitHub 和本机沙箱控制。
- 不假设所有用户都安装 Product Design、Supabase、GitHub、Vercel、Netlify 或其他 Plugin。
- 不把聊天记录当成权威状态。
- 不在状态文件中保存密钥、Token、用户数据或完整命令输出。

## 3. 范围

### 3.1 v1 包含

- LEVEL 推荐、确认和升级判断。
- 三套 SOP 的按需加载与阶段推进。
- 项目状态初始化、验证、迁移和恢复。
- 按 LEVEL 生成最小文档包。
- 风险分类、自动执行权限和人工 Gate。
- 本地分支、worktree、提交与 Diff 检查。
- 经配置授权后的自有功能分支 Push 和 Draft PR。
- Codex、Claude Code、Cursor 适配入口。
- Windows PowerShell 与 macOS/Linux Shell 安装入口。
- GitHub 分发、版本、升级、卸载、Doctor 和 Changelog。
- 静态验证、临时 Git 仓库测试和场景评测。

### 3.2 v1 不包含

- 自动调用 Qima。
- 自动安装或授权第三方 Plugin。
- 自动修改生产数据库、生产密钥或生产环境。
- 自动把 Draft PR 转为 Ready、合并或发布 Release。
- 自动公开宣传内容或上传自媒体平台。
- 多语言版本。
- 图形化管理界面。
- 用 Hooks 绕过或替代各平台权限系统。

## 4. 触发规则

### 4.1 应触发

- 用户提出开发小工具、插件、网页、Mod 等新项目。
- 用户提出改进已有仓库或参与开源项目。
- 用户提出开发 App、SaaS、小程序等持续运营产品。
- 用户要求判断项目属于哪个 LEVEL。
- 用户要求按标准流程推进，或继续到下一个人工 Gate。
- 用户明确指定 LEVEL 1、LEVEL 2 或 LEVEL 3。

### 4.2 不应触发

- 单纯知识问答。
- 只要求解释、审查或诊断，没有授权推进项目。
- 用户明确要求跳过本流程。
- “我想开发一个 Skill”等 Skill 创建或调试请求；这些请求优先交给 `skill-creator-cn`。

### 4.3 显式调用

当自动触发不稳定时，用户可以明确说：

- “先判断这个项目属于哪个 LEVEL，再开始开发。”
- “按 LEVEL 2 流程推进到下一个人工 Gate。”
- “继续当前项目流程。”

## 5. 总体架构

采用“共享核心 + 平台适配器”。三份 LEVEL SOP 是唯一权威流程源；主 Skill 只保存路由、状态机、权限和加载规则。

```text
project-level-workflow/
├─ SKILL.md
├─ LEVEL1-小型项目开发流程.md
├─ LEVEL2-已有与开源项目改进流程.md
├─ LEVEL3-持续运营产品开发流程.md
├─ references/
│  ├─ level-selection.md
│  ├─ risk-and-permissions.md
│  ├─ state-protocol.md
│  ├─ tool-routing.md
│  └─ platform-compatibility.md
├─ templates/
│  ├─ common/
│  │  ├─ status.md
│  │  ├─ gate-report.md
│  │  └─ acceptance-report.md
│  ├─ level1/
│  │  └─ project-brief.md
│  ├─ level2/
│  │  ├─ project-map.md
│  │  └─ change-proposal.md
│  └─ level3/
│     ├─ idea-review.md
│     ├─ prd.md
│     ├─ tech-spec.md
│     ├─ task.md
│     ├─ deploy-readiness.md
│     └─ rollback-plan.md
├─ schemas/
│  └─ workflow-state.schema.json
├─ scripts/
│  ├─ workflow.py
│  ├─ install.ps1
│  ├─ install.sh
│  ├─ update.ps1
│  ├─ update.sh
│  ├─ uninstall.ps1
│  └─ uninstall.sh
├─ adapters/
│  ├─ codex/
│  ├─ claude-code/
│  └─ cursor/
├─ evals/
│  └─ evals.json
├─ tests/
├─ README.md
├─ CHANGELOG.md
├─ VERSION
└─ LICENSE
```

## 6. 组件职责

### 6.1 `SKILL.md`

负责：

- 说明触发时机和排除场景。
- 发现项目上下文和已保存状态。
- 推荐 LEVEL 并停在首次确认 Gate。
- 读取对应 LEVEL SOP，而不是同时加载三份全文。
- 根据风险、权限和当前阶段选择下一动作。
- 维护“执行—验证—记录—推进—停在 Gate”的循环。
- 指向模板、状态协议和平台适配说明。

`SKILL.md` 控制在 500 行以内，不复制 LEVEL 正文和大段模板。

### 6.2 三份 LEVEL SOP

继续作为：

- 用户在语雀中阅读和维护的流程总览。
- Agent 执行时的权威阶段标准。
- GitHub 仓库中可直接审阅的公开文档。

对公共规则的修改必须先更新 SOP，再更新相关测试和适配器；不得在适配器中定义冲突规则。

### 6.3 `workflow.py`

使用 Python 标准库实现确定性操作：

- `init`：创建状态与目录。
- `validate`：校验状态、文件和版本。
- `status`：生成或刷新 `STATUS.md`。
- `transition`：在 Gate 批准后改变阶段。
- `doctor`：检查运行环境、Git、平台适配和文件完整性。
- `render-adapter`：生成 Codex、Claude Code 或 Cursor 入口。
- `migrate`：升级状态 Schema。

核心脚本不访问网络、不执行生产操作，也不替 Agent 决定 LEVEL 或批准 Gate。

### 6.4 平台适配器

- Codex：安装共享 Skill，并生成最小项目入口；核心仍使用标准 `SKILL.md`。
- Claude Code：安装到个人或项目 Skill 目录；只在适配层使用 Claude 专属字段和权限提示。
- Cursor：生成 `.cursor/rules/project-level-workflow.mdc`，让 Cursor 读取共享 SOP、状态和项目级 `AGENTS.md`。

适配器只处理发现、路径和格式差异，不复制业务流程。

### 6.5 项目级规则生成器

根据已确认 LEVEL 和项目环境生成精简 `AGENTS.md`，必要时补充 Claude/Cursor 入口。内容只包括：

- 当前 LEVEL 和权威文档位置。
- 项目启动、测试、构建命令。
- 允许与禁止修改范围。
- 风险和审批边界。
- 当前任务与验证要求。

不得把完整 SOP 重复写进项目规则。

## 7. 项目状态协议

### 7.1 文件布局

```text
.project-workflow/
├─ state.json
└─ state.backup.json

docs/project-workflow/
├─ STATUS.md
├─ decisions/
├─ requirements/
├─ tasks/
├─ evidence/
└─ gates/
```

### 7.2 `state.json` 核心字段

```text
schema_version
workflow_version
project_id
level
stage
gate
status
risk
permissions
current_task
artifacts
verifications
git
remote
history
updated_at
```

约束：

- 使用 UTF-8 JSON。
- 时间使用带时区的 ISO 8601。
- 路径优先保存项目根目录相对路径。
- 不保存密钥、Token、用户数据或长日志。
- 更新时先写临时文件、校验成功后原子替换，并保留上一份备份。

### 7.3 `STATUS.md`

固定展示：

1. 当前 LEVEL、阶段和状态。
2. 本轮目标与不做范围。
3. 已完成内容。
4. 验证命令与结果摘要。
5. 当前风险和未决事项。
6. 当前人工 Gate。
7. 推荐选择及批准后的下一步。

## 8. 执行状态机

```text
未初始化
  → 读取项目与规则
  → 推荐 LEVEL
  → LEVEL 确认 Gate
  → 初始化文档与状态
  → 选择当前最小任务
  → 风险分类
  → 低风险执行
  → 运行验证
  → 更新状态、文档与 Git
  → 当前阶段是否完成？
       ├─ 否：继续下一个最小任务
       └─ 是：生成 Gate 报告并停止
  → 用户批准
  → 进入下一阶段
```

每次恢复时先运行 `validate`，再核对 Git 和项目规则。聊天中的说法与状态文件冲突时，不自行选择；展示差异并询问用户。

## 9. 风险与权限

### 9.1 风险分级

| 风险 | 示例 | 默认行为 |
| --- | --- | --- |
| R1 | 文档、模板、独立样式、只读分析 | 自动执行并验证 |
| R2 | 边界清晰的业务逻辑、测试、内部 API | 已有批准任务内自动执行，测试后提交 |
| R3 | 数据库、认证授权、公共 API、核心依赖、部署配置 | 执行前停在人工 Gate |
| R4 | 生产数据、密钥、支付、不可逆迁移、生产发布 | 只分析和准备，不自主执行 |

### 9.2 Git 权限

自动允许：

- 创建 Skill 自己的功能分支或 worktree。
- 在验证通过后创建小而明确的本地提交。
- 经用户配置授权后，推送 Skill 自己创建的功能分支。
- 经用户配置授权后，创建或更新 Draft PR。

必须询问：

- 初始化一个尚未使用 Git 的目录。
- 处理与用户未提交修改重叠的文件。
- 修改他人分支、公开评论、转为 Ready、合并、Release 或删除远程分支。

禁止：

- Force Push。
- 改写公共历史。
- 自动提交用户已有的无关修改。
- 未经确认执行清理、重置或删除。

### 9.3 公开包的安全默认值

公开发布版本默认关闭自动 Push 和 Draft PR。安装或项目初始化时由用户显式开启：

```text
allow_push_own_branch
allow_create_draft_pr
```

用户当前个人配置可把两项设为 `true`，但不能把该偏好硬编码成所有安装者的默认值。

## 10. 工具路由与降级

- Product Design、Supabase、GitHub、Vercel、Netlify 等 Plugin 都是可选能力。
- 使用前检查是否安装、登录、授权以及是否适合当前技术栈。
- Plugin 缺失时使用通用文档、CLI 或人工流程，不中断核心 SOP。
- Qima 只输出“此阶段可考虑手动使用某 Skill”的提醒。
- 任何外部工具的建议都不能越过当前风险等级和人工 Gate。

## 11. 安装、升级与卸载

### 11.1 安装

- `install.ps1` 面向 Windows PowerShell。
- `install.sh` 面向 macOS、Linux、WSL 和 Git Bash。
- 安装器检查平台、目标路径、现有版本和冲突文件。
- 已存在同名 Skill 时先显示版本与差异，不静默覆盖用户修改。
- Cursor 适配器按项目生成规则；不依赖已经弃用的 `.cursorrules`。

### 11.2 升级

- 使用语义化版本。
- 升级前保存用户配置和状态备份。
- 先迁移 `state.json` Schema，再替换共享文件。
- 本地有未识别修改时停止并给出保留、对比或手工合并说明。

### 11.3 卸载

- 只删除安装器创建且能通过清单确认的文件。
- 默认保留项目内 `.project-workflow/` 和 `docs/project-workflow/`。
- 删除项目状态必须单独确认。

## 12. 错误处理

### 12.1 状态损坏

1. 停止阶段推进。
2. 校验 `state.backup.json`。
3. 可恢复时展示差异并恢复。
4. 两份都不可用时，从文档和 Git 生成恢复建议，不猜测 Gate 批准状态。

### 12.2 工作区不干净

- 保留用户已有修改。
- 改动不重叠时可在独立 worktree 继续。
- 改动重叠或基线不明确时停下来询问。
- 不自动 Stash、Reset 或把无关修改放进提交。

### 12.3 验证失败

- 先记录失败命令、退出码和最小错误摘要。
- 完成一次根因诊断和一次有证据的修正循环。
- 根因仍不明确、修正扩大范围或需要 R3/R4 操作时，生成 Gate 报告并停止。
- 不通过删除测试、降低断言或跳过检查伪造成功。

### 12.4 远程操作失败

- 保留本地提交和状态。
- 不改用 Force Push。
- 记录认证、权限、网络或分支保护错误，给出人工处理步骤。

### 12.5 工具不可用

- 标记“未执行”及原因。
- 使用已定义的降级流程。
- 如果缺失工具会使验收证据不足，则停在 Gate，不声称完成。

## 13. 测试与评测

### 13.1 静态检查

- `SKILL.md` frontmatter、名称和 description 合法。
- 所有被引用文件存在。
- Markdown 链接和表格结构完整。
- 公共文件不包含个人绝对路径、密钥或占位符。
- 三个平台适配器能定位同一套 SOP。
- Schema、模板和示例状态一致。

### 13.2 确定性测试

- 在临时目录运行初始化、状态校验、状态迁移和状态恢复。
- 在临时 Git 仓库验证分支、提交、脏工作区和用户修改保护。
- 使用本地模拟 Remote 验证 Push 与 Draft PR 前置条件；CI 不执行真实公开写入。
- 分别测试 Windows 路径、POSIX 路径、空格和中文文件名。

### 13.3 Skill 场景评测

至少包含：

1. 新建静态小工具，推荐 LEVEL 1 并推进到上线 Gate。
2. 修复已有开源仓库 Bug，推荐 LEVEL 2 并生成变更提案与 Draft PR 计划。
3. 新建长期运营 SaaS，推荐 LEVEL 3 并停在需求、技术和生产 Gate。
4. 从有效 `state.json` 恢复任务。
5. 状态与聊天冲突时停止询问。
6. 遇到数据库、认证或生产部署时不越权。
7. “我想开发一个 Skill”不抢占 `skill-creator-cn`。
8. 单纯代码解释或 Review 不触发项目推进。
9. Plugin 缺失时正确降级。
10. 自动 Push 和 Draft PR 只在用户已开启权限且分支由本 Skill 创建时发生。

### 13.4 用户验收

首版起草后，使用 2～3 个真实提示词运行轻量评测，把完整输出和生成文件交给用户审阅。用户确认行为符合预期后，再进行打包和发布准备。

## 14. 发布策略

- GitHub 仓库公开发布。
- 使用 `VERSION`、Git Tag、GitHub Release 和 `CHANGELOG.md`。
- README 提供快速安装、平台差异、权限说明、升级和卸载。
- Release 前运行全部静态检查、确定性测试和场景评测。
- Release 发布属于人工 Gate；Agent 只能准备 Release Notes 和候选命令。

## 15. 成功标准

v1 完成必须同时满足：

- 三份现有 SOP 保持可单独导入语雀。
- 一个共享 `SKILL.md` 能按需读取正确 LEVEL。
- Codex 和 Claude Code 能以 Skill 方式加载。
- Cursor 能通过项目 Rule 和 `AGENTS.md` 使用同一核心流程。
- 中断后能从项目状态恢复。
- R1/R2 能自动推进并留下验证证据。
- R3/R4 能稳定停在人工 Gate。
- Git 自动化符合已确认的本地、Push 和 Draft PR 边界。
- 公开包默认不自动进行远程写入。
- 安装、升级、卸载和状态迁移可测试、可恢复。

## 16. 参考

- `LEVEL1-小型项目开发流程.md`
- `LEVEL2-已有与开源项目改进流程.md`
- `LEVEL3-持续运营产品开发流程.md`
- [OpenAI Developers](https://developers.openai.com/)
- [Claude Code：Extend Claude with skills](https://code.claude.com/docs/en/slash-commands)
- [Cursor：Rules](https://docs.cursor.com/context/rules-for-ai)
