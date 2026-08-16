# Project Level Workflow 双语 README 美化设计

日期：2026-08-16
状态：规格已批准
目标分支：`codex/beautify-readme-1-0`
基线：远端 `main`，Commit `0917103008c770785b3479468168cd0cb52aa952`

## 1. 目标

把 Project Level Workflow 1.0 的仓库首页重构为一份简约、项目原生、首次使用者优先的双语 README。新版首页必须让第一次访问的个人开发者快速理解项目价值、完成一次成功安装与初始化、看懂四个 LEVEL 和三种执行策略，同时保留 1.0 的项目记忆、兼容迁移、安全与 GitHub 交付契约。

本次只改进仓库首页信息架构、双语文案和 README 视觉资产，不重新设计 LEVEL 1–4 模型，不修改运行时语义、版本、Schema、安装器行为或发布状态。

## 2. 设计来源与使用边界

### 2.1 `beautify-github-readme`

作为实施流程和质量规范，采用其以下原则：

- README mode：允许重构整份 README 的信息顺序、文案层级和视觉系统。
- 项目原生 Hero：视觉材料必须来自 LEVEL、执行策略、项目记忆和交付 Gate，不使用通用装饰。
- `Value → First success → Mechanism → Detail` 的阅读路径。
- 纯 SVG 负责身份、结构和流程，Markdown 负责可复制、可搜索、可翻译和经常变化的文字。
- 在 GitHub 宽屏与窄屏下验证 SVG、链接、对比度和内容可读性。

### 2.2 `beautify-github-profile`

该仓库不是 Agent Skill，没有 `SKILL.md`，不伪装安装。它只作为 README 组件资料库，用于评估 Header、Badge、Stats、图标和动态组件。根据本项目的简约方向，主动舍弃：

- 访客计数、Trophy、贡献蛇和个人活跃度组件。
- 依赖第三方运行服务的动态 Stats 卡片。
- 大量技术 Logo、徽章墙、装饰 GIF 和与流程机制无关的 Profile 组件。

保留的启发只有“用明确的 Header 建立入口”和“每个视觉组件必须有信息职责”。

## 3. 目标读者与项目故事

### 3.1 首要读者

第一次接触 Project Level Workflow、希望让个人项目更可恢复、更可验证，但不想承受重复审批和过重文档负担的个人开发者。

### 3.2 次要读者

- 从 `0.4.0` 升级到 `1.0` 的既有用户。
- 需要改进已有、团队或开源仓库的维护者。
- 需要了解复杂自动化分析与外部能力路由边界的负责人。

### 3.3 项目故事

```text
Audience: 首次使用工作流的个人开发者
One-sentence value: 选择刚好的流程强度，保留完整项目记忆，只在真正重要时确认。
Primary proof: LEVEL 1–4 责任模式、AUTO / CONFIRM / MANUAL_ONLY、可执行的快速开始与状态验证。
First successful action: Clone → Dry Run → 安装 → init → status。
Visual theme: 深海蓝、薄线流程、大留白、单一青绿色强调色的简约技术地图。
```

## 4. 执行模式与设计深度

采用 README mode 的完整重构，但限制在“有意义的最小重构”：

- 重排内容，使首次成功路径和工作机制早于详细 LEVEL 解释。
- 删除重复承诺、过长内部说明和不帮助首次使用的前置信息。
- 保留全部 1.0 公共契约、迁移、安全、平台和验证事实。
- 不把 README 变成营销落地页，不添加无证据的用户量、性能、采用率、评价或兼容声明。

## 5. 双语文档结构

### 5.1 文件

- `README.md`：中文主入口，首行区域提供 `English` 链接。
- `README.en.md`：完整英文同构版本，首行区域提供 `简体中文` 链接。

### 5.2 同构规则

- 两份 README 使用相同章节顺序、相同视觉资产和相同命令。
- LEVEL、`AUTO`、`CONFIRM`、`MANUAL_ONLY`、PVS、Schema、GitHub 等公共术语保持一致。
- 英文版完整表达中文事实，不缩减为摘要，不增加中文版没有的产品承诺。
- 修改公共行为描述时必须同步两份文档。

## 6. 固定阅读顺序

1. Hero：项目名、核心价值、LEVEL 1–4 路径、三种执行状态。
2. 3 分钟快速开始：Clone、Dry Run、安装、`init`、`status` 的一条完整成功路径。
3. 它如何工作：LEVEL → 执行策略 → 验证记录 → GitHub 交付 Gate。
4. 选对 LEVEL：四行责任模式表、选择顺序和“持续更新不等于持续运营”。
5. 双层项目记忆：稳定认知层与演进记录层，以及各 LEVEL 的文档深度。
6. 兼容、安全与 GitHub 交付：`0.4.0` 迁移、备份、旧 L4 Gate、高风险边界与插件路由。
7. 平台、开发验证与许可证：Codex、Claude Code、Cursor，测试命令、更新、卸载、版本与 MIT。

不得把目录、架构细节、迁移说明或长表格放在快速开始之前。

## 7. 视觉系统

### 7.1 视觉令牌

```text
Palette:
  background: #09111F
  foreground: #F6F8FB
  primary:    #65E6D1
  muted-dark: #9EACBF
  muted-light:#667085

Typography:
  sans: Inter, Segoe UI, system-ui, sans-serif
  mono: ui-monospace, SFMono-Regular, Consolas, monospace

Shape:
  radius: 8–10 SVG units
  stroke: 1–2 SVG units
  spacing unit: 8 SVG units

Motif:
  一条连接 LEVEL 1–4 的责任路径，以及由路径进入执行策略和交付 Gate 的细线。

Composition:
  大留白、稀疏技术地图、一个青绿色强调色，不使用厚重阴影和装饰网格。
```

### 7.2 Hero

文件：`assets/readme/hero.svg`

- 纯 SVG，`viewBox="0 0 1200 520"`，README 使用 `width="100%"`。
- 保留项目名、中文或语言中立的核心价值表达、LEVEL 1–4、`AUTO / CONFIRM / MANUAL_ONLY`。
- 不放版本角标、平台 Logo、测试数字、维护者信息、安装命令或第三方徽章。
- 项目名和核心价值是主层级；四级路径是次层级；三种状态是最低但仍可读的核心信息。
- essential text 在 900 CSS px 预览时不小于 20 SVG units，辅助标签不小于 18。

两份 README 共用同一 Hero。为避免中英文本冲突，Hero 的长价值句使用语言中立的简短英文：`Choose the right workflow depth. Keep the full project memory.`；中文和英文的完整价值说明留在紧随其后的 Markdown alt text 与段落中。

### 7.3 工作机制图

文件：`assets/readme/workflow.svg`

- 纯 SVG，`viewBox="0 0 1200 420"`。
- 从左到右表达：`LEVEL 1–4 → AUTO / CONFIRM / MANUAL_ONLY → Evidence & Memory → GitHub Delivery Gate`。
- 只展示机制节点和关系，不把详细安全规则塞入图内。
- 中文和英文 README 共用英文短标签；两份文档在图下分别用本语言解释。

### 7.4 明确不使用

- 生成式 raster、照片、人物、Mascot 或混合 SVG 合成。
- GIF、SVG animation、JavaScript、`foreignObject`、远程字体和远程 raster 引用。
- Shields badge 墙、动态统计服务、访客计数和社交证明组件。
- 每个章节重复使用装饰 Banner 或卡片。

## 8. 文案原则

- 先写用户结果，再写内部机制。
- 每个概念只解释一次；重复内容改为链接到 `LEVEL.md`、`SKILL.md` 或 reference。
- 保持 `LEVEL.md` 是四级流程的唯一权威源，README 只做入口和摘要。
- 命令必须可复制，不放进 SVG。
- 迁移限制、高风险动作和未自动执行边界必须可见，不因美化而隐藏。
- 不把 80 项测试写成长期承诺；README 只保留验证命令。具体历史测试证据继续留在 Release 与 readiness 文档。

## 9. 文件范围

计划修改或新增：

- `README.md`
- `README.en.md`
- `assets/readme/hero.svg`
- `assets/readme/workflow.svg`
- `tests/test_repository_contract.py`：增加双语入口、资产存在、关键结构和禁止动态组件的契约测试。
- 本设计文档。

除非实现验证发现明确必要，不修改 `VERSION`、`LEVEL.md`、`SKILL.md`、Schema、运行时脚本、安装器、模板、适配器或 Release 文档。

## 10. 实施与错误边界

- 从远端 `main` 基线在 `codex/beautify-readme-1-0` 分支实施。
- 视觉伴侣生成的 `.superpowers/` 目录不进入项目提交。
- 先写失败的 README 契约测试，再生成 SVG 和双语文档。
- 英文翻译不得改变产品语义；发现术语歧义时以 `LEVEL.md` 和 `SKILL.md` 为准。
- 外部链接失败、图片未渲染或窄屏不可读时，修复后再交付；不以 alt text 代替视觉检查。
- 不自动 Push、创建 PR、Merge、Tag 或 Release。

## 11. 验证与验收

### 11.1 自动检查

```powershell
python -m unittest discover -s tests -v
python scripts/workflow.py doctor --package-root .
python scripts/workflow.py validate-package --package-root .
python C:\Users\admin\.codex\skills\beautify-github-readme\scripts\audit_readme.py README.md
python C:\Users\admin\.codex\skills\beautify-github-readme\scripts\audit_readme.py README.en.md
git diff --check
```

补充结构检查：

- 两份 README 的一级和二级章节顺序同构。
- 中英文互链、内部相对链接、SVG 引用和命令路径存在。
- 不包含访客数、Trophy、动态 Stats、外部字体、脚本或远程图片依赖。

### 11.2 视觉检查

- Hero 与工作机制图分别渲染为 900 px GitHub 宽度和 360 px 窄屏预览。
- 检查文字裁切、路径重叠、留白、对比度和最小字号。
- 在浅色与深色外围背景上确认 SVG 边缘和容器边界。
- 检查 README 第一屏能回答“是什么、对我有什么用、下一步看什么”。

### 11.3 验收标准

- 第一次访问者能在 Hero 后立即找到一条完整安装与初始化路径。
- 工作机制先于 LEVEL 细节出现。
- LEVEL 1–4、三种执行策略、双层项目记忆、迁移和安全边界均准确。
- 中文和英文版本章节同构、链接互通、命令一致。
- 两张 SVG 在宽屏与窄屏下清晰，不依赖 GitHub 会剥离的能力。
- README 比现状更容易扫描，不因美化增加无关组件。
- 项目运行时、版本和已发布 `v1.0` 语义不发生变化。

## 12. 非目标

- 不修改 GitHub 仓库描述、Topics、Social Preview 或账号 Profile README。
- 不建立文档站、GitHub Pages 或额外网站。
- 不更新已安装的 `project-level-workflow` 用户级 Skill。
- 不创建新的项目版本、Tag 或 Release。
- 不向两个参考仓库添加署名、Showcase 或 PR；如最终满意，是否添加可选署名必须另行确认。
