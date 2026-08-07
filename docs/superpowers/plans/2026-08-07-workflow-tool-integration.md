# 三层开发流程工具集成实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在三份 LEVEL 流程文档中加入按需工具路由、使用边界和人工确认 Gate，并把 Qima 明确为仅提醒、不默认调用的可选流程。

**Architecture:** 保留三份文档现有阶段结构，在各文档前部加入工具使用总则，在对应阶段加入最小化的工具触发提示，末尾补充统一来源。LEVEL 3 使用“Qima 前半段可参考、技术栈匹配后才继续”的混合路由；任何外部发布、生产部署和数据变更仍由人工批准。

**Tech Stack:** 标准 Markdown、语雀 Markdown 导入、Codex Skills/Plugins/MCP/CLI/Web 服务说明。

## Global Constraints

- 只修改 `LEVEL1-小型项目开发流程.md`、`LEVEL2-已有与开源项目改进流程.md`、`LEVEL3-持续运营产品开发流程.md`。
- Qima 只作为条件提醒，不写成 Agent 默认调用或自动执行步骤。
- 不把尚未读取成功的网页内容写成已验证事实；保留原链接并标注“使用前验证”。
- Supabase、Vercel 等未安装能力写成可选项，不触发安装或授权。
- 公开发布、生产部署、数据库破坏性变更和外部账号写入必须经过人工 Gate。
- 保持中文说明和语雀可导入的标准 Markdown，不引入专有渲染语法。

---

### Task 1: 更新 LEVEL 1 工具路由

**Files:**
- Modify: `LEVEL1-小型项目开发流程.md`

**Interfaces:**
- Consumes: 现有“需求分析 → 轻量设计 → 边做边改 → 最终验收 → 上线发布 → 宣传与反馈”流程。
- Produces: LEVEL 1 的轻量工具选择表、阶段触发提示、部署与宣传人工 Gate。

- [ ] **Step 1: 增加轻量工具原则和选择表**

写明工具是可选加速器；需求清楚时不强制提问，Qima 仅在需求或交互复杂度上升时提醒。

- [ ] **Step 2: 将工具放入对应阶段**

需求阶段加入 `grill-me`/`vibe-idea` 提醒，设计阶段加入 Product Design，开发测试加入安全 PowerShell 与浏览器验收，上线加入 GitHub、Vercel/Netlify、Supabase 条件选项。

- [ ] **Step 3: 完善宣传工具链与公开发布 Gate**

加入生图、视频总结、视频制作和自媒体上传的触发条件，明确自动上传只能生成草稿或在人工确认后发布。

- [ ] **Step 4: 检查 LEVEL 1 轻量性**

确认没有增加每轮 Review、固定 Phase 或不必要文档；工具提示不得改变 LEVEL 1 的快速迭代定位。

### Task 2: 更新 LEVEL 2 工具路由

**Files:**
- Modify: `LEVEL2-已有与开源项目改进流程.md`

**Interfaces:**
- Consumes: 现有“接管边界 → 快速理解 → 问题确认 → 方案与影响分析 → 小步开发 → 回归验收 → PR/交接 → 发布与成果沉淀”流程。
- Produces: 以 GitHub 和仓库既有规范为主的工具路由，以及不擅自迁移技术栈的约束。

- [ ] **Step 1: 增加仓库优先的工具原则和选择表**

说明仓库规则、维护者决策和现有 CI/CD 高于任何 Skill/Plugin 建议。

- [ ] **Step 2: 将工具放入项目理解、设计、开发和 PR 阶段**

使用 GitHub 能力做 Issue/PR/CI 定向协作，Product Design 仅用于体验审计，安全 PowerShell 用于 Windows 调用，代码审查与浏览器工具按变更类型启用。

- [ ] **Step 3: 限制 Qima 和基础设施插件**

Qima 只在新增独立页面或交互且维护者认可时提醒；Supabase、Vercel、Netlify 只在仓库原本采用或变更任务明确要求时使用。

- [ ] **Step 4: 检查贡献边界**

确认文档不授权 Agent 自动创建公开 Issue、提交 PR、合并或发布；这些操作保留人工确认。

### Task 3: 更新 LEVEL 3 混合路由

**Files:**
- Modify: `LEVEL3-持续运营产品开发流程.md`

**Interfaces:**
- Consumes: 现有 G0-G7 Gate、纵向切片、文档治理、测试上线与宣传增长流程。
- Produces: 明确的产品澄清、体验设计、技术平台选择、开发部署和宣传工具路由。

- [ ] **Step 1: 增加工具治理原则和分阶段选择表**

区分 Skill、Plugin、MCP/App、CLI/Web 服务，记录使用前提、输入、输出、替代方案和人工 Gate。

- [ ] **Step 2: 把 Qima 放入 G0-G3 的提醒路径**

`vibe-idea`、`vibe-interaction`、`vibe-design`、`vibe-prototype` 仅在产物需要时提醒；进入技术设计前设置平台选择 Gate。

- [ ] **Step 3: 增加技术平台选择 Gate**

CloudBase 且符合 Qima 固定栈时可提醒继续 `vibe-architecture`/`vibe-implement`；选择 Supabase、Vercel 或 Netlify 时保留文档契约，改走通用架构与实现流程。

- [ ] **Step 4: 集成 GitHub、部署、安全调用和宣传工具**

GitHub 支撑 Issue/PR/CI，Vercel/Netlify 先预览后生产，Supabase 作为数据库/认证/存储候选，Windows 命令遵守安全 PowerShell；宣传自动化在 G7 后执行。

- [ ] **Step 5: 检查持续运营约束**

确认日志、指标、隐私、密钥、回滚和生产批准不被工具自动化绕过。

### Task 4: 三文档一致性与语雀兼容验证

**Files:**
- Test: `LEVEL1-小型项目开发流程.md`
- Test: `LEVEL2-已有与开源项目改进流程.md`
- Test: `LEVEL3-持续运营产品开发流程.md`

**Interfaces:**
- Consumes: Task 1-3 的文档更新。
- Produces: 可导入语雀、层级清晰、工具边界一致的最终三文件。

- [ ] **Step 1: 搜索关键工具覆盖**

运行：`rg -n "Qima|grill-me|Product Design|Supabase|GitHub|Vercel|Netlify|PowerShell|自媒体|人工" LEVEL*.md`

预期：三个 LEVEL 均出现与其复杂度匹配的工具提示，Qima 均为“可提醒/可选”，无默认自动调用表述。

- [ ] **Step 2: 检查 Markdown 结构**

运行：`rg -n "^(#|##|###) " LEVEL*.md`

预期：标题层级连续，表格有表头和分隔行，链接采用标准 Markdown。

- [ ] **Step 3: 检查不确定来源标注**

运行：`rg -n "使用前验证|实际验证|自动发布|生产" LEVEL*.md`

预期：无法完整读取的外部流程不被包装成已验证能力；外部发布和生产操作均有人工确认。

- [ ] **Step 4: 最终人工通读**

逐份确认流程仍然分别适合小项目、已有项目改进和长期运营产品，没有把工具目录变成强制清单。
