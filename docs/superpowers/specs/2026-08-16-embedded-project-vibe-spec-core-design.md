# Project Vibe Spec 包内内核集成设计

## 1. 文档用途

本文定义 `project-level-workflow` 下一版的自包含集成方案：把 `project-vibe-spec` 作为包内治理内核随主 Skill 一起安装，只暴露一个可发现的 `project-level-workflow` Skill。用户不需要另行 Clone、下载或安装 `project-vibe-spec`。

本文是已确认设计，不授权部署、公开发布、远程推送、删除旧 Skill 或修改用户项目数据。源码实施目标仍是：

`D:\VibeCoding-Project\project-level-workflow`

当前 C 盘目录只保存交接材料；实施前必须确认真实源码 checkout 可写，并重新检查 Git 状态与分支基线。

## 2. 已确认目标

- 一份发布仓库。
- 一条安装命令。
- 安装后只显示一个可调用 Skill：`project-level-workflow`。
- PVS 规则、references 和治理模板全部包含在主包内。
- LEVEL 1–4 按各自边界自动读取包内 PVS 能力。
- 安装和运行不依赖网络，也不检查用户是否另装了 PVS。
- 新功能目标版本从 `0.3.0` 升到 `0.4.0`。

## 3. 授权与来源

用户已确认拥有 `project-vibe-spec` 源码，并授权完整复制、修改和随 `project-level-workflow` 公开分发。

内嵌 PVS 内核统一适用 `project-level-workflow` 根目录的 MIT License。新增来源记录，至少包含：

- 原仓库：`https://github.com/dnwwdwd/project-vibe-spec.git`
- 本次同步基线：`dae5315`（`Strengthen cross-module governance gates`）
- 纳入日期与主包版本。
- 原文件到内核文件的映射。
- 为单 Skill、分层加载和包校验做过的修改摘要。

## 4. 采用方案与取舍

采用“包内分层内核”，不采用全量融合或构建时生成。

选择原因：

- 比全量融合更容易追踪 PVS 来源、同步上游变化和审查差异。
- 比构建时生成更符合“从仓库直接安装也开包即用”的目标。
- 内核不作为第二个 Skill 暴露，避免触发冲突和双重事实源。
- 保持当前 `LEVEL.md` 的等级语义，不借集成之机重新设计四级模型。

## 5. 目标包结构

```text
project-level-workflow/
├─ SKILL.md
├─ LEVEL.md
├─ core/
│  └─ project-vibe-spec/
│     ├─ PVS.md
│     ├─ SOURCE.md
│     ├─ references/
│     │  ├─ decision-gates.md
│     │  └─ document-maintenance.md
│     └─ assets/
│        └─ governance-starter/
├─ references/
│  └─ project-vibe-spec-bridge.md
├─ templates/
├─ scripts/
│  └─ workflow.py
├─ schemas/
├─ adapters/
├─ evals/
└─ tests/
```

`core/project-vibe-spec/PVS.md` 由原 PVS `SKILL.md` 转为内部规则入口，不保留可被平台识别为第二个 Skill 的嵌套 `SKILL.md`。原相对引用同步改为内核目录内的有效路径。

## 6. 唯一入口与分层加载

### 6.1 唯一可发现入口

用户始终触发根目录 `SKILL.md`。根入口完成项目发现、LEVEL 推荐、状态恢复、风险判断和人工 Gate 路由；需要 PVS 能力时读取包内 `core/project-vibe-spec/PVS.md` 及其相关资源。

运行时不得：

- 要求用户另行安装 `$project-vibe-spec`。
- 从个人 Skills 目录查找独立 PVS。
- 在运行期间下载 PVS。
- 因用户环境存在独立 PVS 而改变包内规则优先级。

### 6.2 LEVEL 1

自动复用 PVS 的项目接管、文档地图、需求确认、范围护栏和验证原则，但只建立 PVS-Lite。继续使用现有 LEVEL 1 Project Brief、状态和待验证模板；不默认创建完整 Requirements、Decisions、Progress、PDD 或 PRD 文档包。

### 6.3 LEVEL 2

自动读取完整 PVS 内核，包括：

- 首次接管与文档职责映射。
- 需求分类和跨模块影响分析。
- 数据设计与数据库变更确认 Gate。
- 决策记录和需求台账。
- 大任务阶段计划与进度治理。
- 实现与文档同步。
- 行为验收、交付和安全 Git 范围。

当目标项目没有等价文档时，从包内 `assets/governance-starter/` 复制所需模板；存在等价目录时继续复用，不建立平行事实源。

PVS governance starter 是 LEVEL 2 新建治理文档的唯一默认模板源。主包现有 `templates/level2/` 中与 Requirements、Decisions、PDD、PRD、项目地图或技术规格重叠的文件，本轮不删除，只保留为兼容入口，并通过模板职责映射标记为“不再用于新项目的默认生成”。主包特有且不重叠的部署 readiness、运营 readiness、回滚、待验证和任务/Gate 类模板继续保留。

包内新增确定性的模板职责映射，至少记录：职责、默认模板、兼容模板和适用 LEVEL。初始化、文档说明和测试只能指向每项职责的一个默认模板；不能同时从两套模板生成同一职责文档。

### 6.4 LEVEL 3

只加载与已有仓库接管、需求可追溯、跨模块影响、回归、Review、PR 和交接相关的 PVS 原则。已有仓库规则优先，不强行创建完整 PVS 文档包。

### 6.5 LEVEL 4

只加载需求澄清、方案比较、数据/安全/运营风险和决策 Gate。保持“只分析、不实现”的现有边界，不创建代码任务、数据库迁移或部署步骤。

## 7. Bridge 的职责

保留 `references/project-vibe-spec-bridge.md` 的公开路径，避免破坏现有引用。它从“外部 Skill 分层说明”改为“包内 PVS 内核加载矩阵”，至少说明：

- 每个 LEVEL 应读取的 PVS 章节和资源。
- 每个 LEVEL 明确不加载或不创建的内容。
- 项目已有文档优先和单一事实源规则。
- 内核路径与缺失时的错误处理。

`LEVEL.md` 继续是等级语义唯一权威源；PVS 内核负责项目协作契约，不重新定义 LEVEL。

## 8. 安装、更新与卸载

### 8.1 安装

安装器只创建一个托管目录：`skills/project-level-workflow/`。`core/project-vibe-spec/` 随主包整体复制。

Dry Run 显示：

- 主包版本。
- PVS 来源提交。
- PVS 内核文件数量。
- 安装目标。
- 将被新建、覆盖或备份的托管路径。

正式安装前先执行包完整性校验；内核缺文件、链接失效、编码错误或版本契约不一致时，不开始替换。

### 8.2 更新

更新顺序固定为：

1. 校验新包及 PVS 内核。
2. 检查目标项目状态和需要的状态迁移。
3. 把旧主包整体移动到带时间戳的备份目录。
4. 安装新主包和同版本内核。
5. 运行安装后 Doctor。

校验失败发生在第 3 步之前，不能留下半安装状态。PVS 内核与主包使用同一版本生命周期，不允许分别更新。

### 8.3 已有独立 PVS

安装器和 Doctor 可以检测用户 Skills 根目录中是否存在独立 `project-vibe-spec`，但只能显示提示，不能覆盖、移动或删除。

提示需说明：

- 主包运行时只读取包内 PVS 内核。
- 独立副本仍可能被用户直接触发，并可能与主包版本不同。
- 如需移除，必须另行列出精确路径、文件数量和影响，取得用户确认后执行。

### 8.4 卸载

用户显式运行主包卸载器时，包内 PVS 内核随主包托管目录一起移除。卸载器继续保留目标项目中的 `.project-workflow/`、`docs/project-workflow/` 和用户治理文档。独立 `project-vibe-spec` 不属于主包托管范围，不处理。

## 9. 状态与兼容

- 现有旧 LEVEL 映射保持不变。
- 已有 `.project-workflow/state.json` 不因 PVS 内嵌而重置。
- 新初始化状态使用主包版本 `0.4.0`。
- 现有状态中的 LEVEL、stage、Gate、权限、任务、验证和历史继续保留。
- 只读 `validate` 不修改已有状态。已有状态第一次由 `0.4.0` 成功执行 transition、status 刷新或其他明确写状态的命令时，把 `workflow_version` 更新为 `0.4.0`，先写备份，并在 history 记录旧/新工作流版本；该更新不改变 LEVEL、Gate 或批准状态。
- 状态 Schema 只有在字段契约实际变化时才升级；不能为了版本号变化制造无必要迁移。
- 适配器仍引用根 `LEVEL.md`、状态和 Bridge，不复制 PVS 全文。

## 10. Doctor 与包校验

Doctor 新增：

- PVS 内核入口存在。
- 两份 PVS reference 存在并可读。
- governance starter 模板清单完整。
- 内核 Markdown 为 UTF-8，内部相对链接有效。
- `SOURCE.md` 的原仓库、同步提交和许可证声明存在。
- 发现独立 PVS 时输出非阻断提示。

`validate-package` 新增：

- 内核必需文件契约。
- 内核不得含可被识别为第二个 Skill 的 `SKILL.md`。
- 公开说明不得要求用户另行 Clone 或安装 PVS。
- 根入口、Bridge、LEVEL 文档和内核之间的引用一致。
- 模板职责映射中每项职责只有一个默认模板，重叠的旧 LEVEL 2 模板只能标为兼容入口。
- 安装器、更新器和卸载器的托管文件范围包含整个内核。

## 11. 错误处理

- 内核缺失或损坏：Doctor 和包校验失败，安装器在替换前退出。
- LEVEL 运行时找不到内核入口：停止当前流程并报告包损坏，不静默回退到外部 Skill。
- 内核模板缺失：不得创建残缺治理结构；报告精确缺失文件。
- 检测到外部独立 PVS：只提示版本分歧风险，不改变加载来源。
- 更新失败：保留当前有效安装和原项目状态；只有完成新包校验后才允许进入替换阶段。

## 12. 验证方案

### 12.1 包契约测试

- 当前完整包通过校验。
- 测试副本缺少任一内核必需文件时明确失败。
- 内核出现嵌套 `SKILL.md` 时失败。
- 公开文件出现外部 PVS 安装要求时失败。
- 内核链接、来源记录和 MIT 许可声明通过。
- 模板职责映射不存在两个默认来源。

### 12.2 安装与更新测试

- PowerShell 和 POSIX Shell Dry Run 均显示内核摘要。
- 临时全新安装后只有一个顶层可发现 Skill，内核文件齐全。
- 模拟 `0.3.0` 到 `0.4.0` 更新，确认先校验、再备份、后替换。
- 更新后项目状态不重置。
- 新包损坏时旧包不被替换。
- 存在独立 PVS 时只提示，不修改或删除它。

### 12.3 LEVEL 行为测试

- LEVEL 1 能读取内核原则，但只采用 PVS-Lite。
- LEVEL 2 离线定位完整 PVS 与 governance starter。
- LEVEL 3 不强制创建完整 PVS 文档包。
- LEVEL 4 保持只分析、不实现。
- 四级初始化、validate、Doctor、适配器渲染和包校验继续通过。

### 12.4 回归命令

```text
python -m unittest discover -s tests -v
python scripts/workflow.py doctor --package-root .
python scripts/workflow.py validate-package --package-root .
```

另外在临时目录执行四级初始化、平台适配器渲染以及安装/更新生命周期测试。未运行的真实平台触发或安装验证必须单独列为待验证，不能由静态测试代替。

## 13. 完成定义

同时满足以下条件才算完成：

1. 仓库和发布包包含完整 PVS 内核、来源记录和治理模板。
2. 安装后只暴露一个 `project-level-workflow` Skill。
3. LEVEL 1–4 都从包内加载对应 PVS 能力，不需要外部下载或查找。
4. 安装、更新、Doctor、包校验和卸载契约覆盖内核。
5. 现有项目状态、等级语义和安全 Gate 不被削弱。
6. 新增测试与现有回归全部实际通过。
7. 独立旧 PVS 不被自动删除、覆盖或作为运行时回退来源。

## 14. 明确不做

- 不重新设计四个 LEVEL 的语义。
- 不把完整 PVS 强制应用到 LEVEL 1、3 或 4。
- 不保留第二个可发现的 PVS Skill 入口。
- 不在运行时联网同步 PVS。
- 不使用 Git submodule 作为用户安装前提。
- 不自动删除用户已有独立 PVS。
- 不在本功能中部署、发布、推送或创建远程资源。

## 15. 实施前 Gate

开始实现前必须完成：

1. 将真实源码仓库加入可写工作区，或确认一个以真实 Git 历史为基线的可写 checkout。
2. 重新检查 D 盘仓库的分支、Remote、工作区和与远端 `main` 的关系。
3. 确认本轮只修改集成所需的文档、内核、安装器、运行时契约、测试、evals、版本和变更记录。
4. 不删除文件；若实施中发现确需删除或替换旧入口，先列出路径、数量和影响并等待确认。
5. 提交、推送、发布和安装到用户真实 Skills 目录仍需分别确认。
