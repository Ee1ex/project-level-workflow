# ELX / Eelex 品牌与仓库迁移设计

状态：用户已于 2026-08-20 批准命名方向；等待书面规格复核。

## 目标

建立两条清晰且可长期扩展的项目命名线：

- `ELX` 用于正式公开的工具、方法、Skill、CLI 和框架。
- `Eelex` 用于作者身份、博客和个人内容。

本次迁移包含两个独立项目：

1. 把 `Project Level Workflow 1.0` 完整改名并升级为 `ELX Level 2.0`。
2. 把个人博客 `Eelex Journal` 改名为 `Eelex Blog`。

测试仓库、临时实验和内部项目不强制使用品牌前缀。

## 已确认事实

### Project Level Workflow

- GitHub 仓库：`Ee1ex/project-level-workflow`。
- 当前远端默认分支：`main`。
- 当前远端 `main`：`b5eefb0ee9c74cc9bc13335db6e8e582993810d9`。
- 当前公共版本：`1.0`，Tag/Release：`v1.0`。
- `D:\VibeCoding-Project\project-level-workflow` 是旧本地仓库，仍停留在 `codex/level-model-v1`，不得直接覆盖或继续开发。
- `C:\Users\admin\Documents\project-level-workflow` 是交接与规格目录，不是功能实施仓库。

### Eelex Journal

- GitHub 仓库：`Ee1ex/Eelex-Journal`。
- 当前远端默认分支：`main`。
- 当前远端 `main` 与本地 `HEAD`：`ce22d7d77435e803063f415651da8ceb9ef0c620`。
- 本地仓库：`D:\VibeCoding-Project\Eelex-Journal`。
- 当前本地分支：`codex/home-editorial-demo`。
- 当前未跟踪用户改动：`.codex/`、`public/eelex-avatar.png`。迁移不得覆盖、提交或删除这些改动，除非用户另行授权。

## 品牌架构

### ELX 产品线

命名规则：

```text
展示名：ELX <Product>
仓库名：elx-<product>
```

`ELX` 是 `Eelex` 去除重复元音后保留的技术型签名。它用于产品归属，不取代 GitHub 账号 `Ee1ex`。

GitHub 只读检索显示，已有若干第三方仓库使用或包含 `elx`。因此 `ELX` 被定义为 `Ee1ex` 账号下的产品前缀，不宣称为全网独占名称；正式商标或商业化前需另做商标、域名和包注册表检查。

### Eelex 内容线

命名规则：

```text
展示名：Eelex <Project>
仓库名：eelex-<project>
```

该命名线保留完整作者身份，适用于博客、文章、作品集和个人内容项目。

## ELX Level 2.0 命名契约

| 对象 | 旧值 | 新值 |
| --- | --- | --- |
| 产品展示名 | Project Level Workflow | ELX Level |
| GitHub 仓库 | `Ee1ex/project-level-workflow` | `Ee1ex/elx-level` |
| Skill 标识 | `project-level-workflow` | `elx-level` |
| 用户级安装目录 | `.codex/skills/project-level-workflow` | `.codex/skills/elx-level` |
| 项目级安装目录 | 对应平台下的 `project-level-workflow` | 对应平台下的 `elx-level` |
| 状态目录 | `.project-workflow` | `.elx-level` |
| 项目文档目录 | `docs/project-workflow` | `docs/elx-level` |
| 公共版本 | `1.0` | `2.0` |
| Git Tag | `v1.0` | `v2.0` |

以下名称描述功能概念而非品牌，不强制替换：

- `workflow.py`
- `workflow_version`
- `schema_version`
- 文档中表示一般流程含义的“工作流”与 `workflow`

## ELX Level 迁移语义

### 立即切换

- `2.0` 的新安装、新状态和新文档只写 `elx-level` 与 `.elx-level`。
- 不提供长期可发现的 `project-level-workflow` Skill 别名。
- 不承诺旧安装目录继续接收后续更新。
- `v1.0` 保留为旧品牌最终稳定发布，不移动、不覆盖。

### 一次性状态复制

当 `2.0` 在项目中发现 `.project-workflow` 且尚无 `.elx-level` 时：

1. 完整读取并验证旧状态。
2. 将旧状态复制到 `.elx-level`。
3. 刷新包名、公共版本和必要路径引用。
4. 保留 `.project-workflow` 原目录作为回滚备份。
5. 迁移成功后只读写 `.elx-level`。

若新旧目录同时存在，不自动覆盖任何一方；命令必须停止并报告冲突。若复制或验证失败，不改变旧状态，并返回可执行的恢复说明。

### 安装迁移

更新器可以从旧安装发现 `1.0`，但新版本安装目标只能是 `elx-level`。替换旧用户级安装涉及目录移除时，必须先列出目标、数量和影响并获得用户确认；默认安全路径是先安装并验证新目录，再保留旧目录等待单独清理确认。

### 外部交付

GitHub 仓库改名、Push、PR、Merge、Tag 和 Release 都是独立远程动作。实施完成后必须先提供分支、提交、文件范围、测试证据、PR 与 Merge 方案、`v2.0` Tag/Release 文案、回滚和未验证项，再集中请求一次明确确认。

仓库改名后必须回读验证：

- 新仓库路径可访问。
- 默认分支和 Commit SHA 未意外变化。
- Tag、Release、开放 PR、仓库 About 和 README 链接指向新品牌。
- 旧 GitHub URL 的重定向仅作为平台行为记录，不作为 Skill 兼容机制。

## Eelex Blog 命名契约

| 对象 | 旧值 | 新值 |
| --- | --- | --- |
| 展示名 | Eelex Journal / Eelex Code Hub 等现有标题 | Eelex Blog |
| GitHub 仓库 | `Ee1ex/Eelex-Journal` | `Ee1ex/eelex-blog` |
| 本地实施工作树 | 不直接修改现有脏工作树 | 新建隔离工作树 |

博客改名只覆盖品牌和仓库身份，不自动重做视觉设计、内容架构、路由、域名或部署平台。实施前需要检索标题、README、站点元数据、包名、内部链接、部署配置和仓库链接，形成精确受影响清单。

现有 `.codex/` 与 `public/eelex-avatar.png` 属于用户改动，必须保持未跟踪状态并排除在改名提交之外。

## 实施分解

### 子项目 A：ELX Level 2.0

1. 从 GitHub `main@b5eefb0` 建立隔离工作树和 `codex/elx-level-2-0` 分支。
2. 先写失败测试，覆盖新名称、安装目录、状态复制、冲突停止、版本与包完整性。
3. 最小修改运行时、安装器、模板、适配器、文档和 Release 记录。
4. 完成全量回归、LEVEL 1–4、三平台适配器和 `1.0 → 2.0` 状态迁移冒烟。
5. 创建本地提交，不执行远程动作。

### 子项目 B：Eelex Blog

1. 以 `main@ce22d7d` 建立隔离工作树和 `codex/eelex-blog-rename` 分支。
2. 只读建立名称、元数据、链接和部署影响清单。
3. 先写或补充失败检查，再最小修改公开品牌文本和仓库引用。
4. 运行仓库既有测试、构建、路由和静态检查。
5. 创建本地提交，不执行远程仓库改名或 Push。

两个子项目分别提交、分别验证，不共享工作树，不把博客用户改动带入改名分支。

## 不做项

- 不重新设计四级 LEVEL 模型。
- 不修改 `ELX Level` 的风险 Gate 和 GitHub 交付边界，除非改名迁移需要修正文案或路径。
- 不立即删除旧 Skill 安装、旧状态目录、Tag 或 Release。
- 不在本次范围内为所有历史实验仓库统一改名。
- 不把 `ELX` 描述为已注册或全网独占商标。
- 不在未确认前执行 GitHub 仓库改名、Push、PR、Merge、Tag 或 Release。

## 验收标准

### ELX Level

- 所有公开产品标识、Skill 标识、安装目标和新状态路径使用 `elx-level`。
- 旧 `.project-workflow` 可一次性复制迁移，旧目录字节保持不变。
- 新旧状态目录冲突时停止，不覆盖数据。
- `VERSION = 2.0`、`workflow_version = 2.0`、`schema_version = 2.0`。本次迁移改变品牌、安装位置和状态目录，不改变状态 JSON 的结构契约。
- 包校验、Doctor、全量 unittest、LEVEL 1–4 和三平台适配器冒烟通过。
- 安装、更新、卸载、README、About、Changelog 和 Release 文案一致。

### Eelex Blog

- 页面和元数据的正式名称为 `Eelex Blog`。
- 仓库内不再把产品正式名称显示为 `Eelex Journal`，历史记录和文章语境除外。
- 构建、测试、关键路由和静态资源检查通过。
- 用户现有未跟踪文件未被修改、移动、删除或提交。

## 回滚

- ELX Level：保留 `v1.0`、旧状态目录和旧安装备份；本地变更通过 Revert 提交回滚，不改写历史。
- Eelex Blog：仓库改名前可直接放弃隔离分支；改名后使用 GitHub 仓库设置改回旧名并回读验证。
- 两个项目都禁止 Force Push 和改写公共历史。
