# Changelog

本项目的所有重要变化都会记录在此文件中。

## [1.0] - 2026-08-16

- 公共版本改为两段式 `1.0`，状态 Schema 升级为 `2.0`，并兼容迁移 `0.4.0` 三段版本状态。
- LEVEL 1 改为快速开发与完整项目记忆，使用稳定认知层、演进记录层和轻量 Change/Progress Record。
- LEVEL 2 全量采用包内 PVS、Phase 0 → Phase N、范围冻结和 DoD；普通 Phase 完成不再形成审批 Gate。
- LEVEL 3 优先复用 Issue、PR、CHANGELOG、ADR 和仓库文档，不为小改动创建平行完整 PVS 文档树。
- LEVEL 4 改为先分析、负责人确认后可实施，保留十节点参考并只路由外部专业能力。
- LEVEL 1–3 对用户使用 `AUTO`、`CONFIRM`、`MANUAL_ONLY`；状态继续兼容内部 R1–R4。
- 所有 LEVEL 的 GitHub 远程交付自动路由 Codex GitHub 插件，执行前统一确认并在完成后回读验证。
- 新增双层文档、项目架构、Change Record、Release Record、个人执行循环和路由契约；旧模板继续作为兼容入口。

## [0.4.0] - 2026-08-16

- 将 Project Vibe Spec 治理内核、两份参考规则和完整 governance starter 嵌入 `core/project-vibe-spec/`，包内只保留根 `SKILL.md` 一个可发现入口。
- 以 `templates/template-map.json` 确立 PVS starter 为 LEVEL 2 重叠治理职责的唯一默认模板，同时保留原 `templates/level2/` 路径作为兼容入口。
- Doctor 与 `validate-package` 新增 PVS 内核完整性、模板映射、单 Skill 和无外部安装指令校验。
- PowerShell 与 POSIX 安装器增加包预检、PVS 文件统计、staging 替换、冲突备份和失败回滚；独立安装的 `project-vibe-spec` 只告警，绝不修改或删除。
- `status` 与 `transition` 在显式状态写入时安全刷新 `workflow_version`，保留旧状态备份和 `workflow_version_updated` 历史；只读 `validate` 保持字节级不变。
- Codex、Claude Code、Cursor 适配器统一引用包内 Bridge 与 PVS 内核，并新增单 Skill、离线和无需独立 PVS 的 eval 覆盖。

## [0.3.0] - 2026-08-13

- 将四级模型合并到根目录唯一权威文档 `LEVEL.md`，删除四份分散 SOP 和旧三级兼容入口。
- CLI、Doctor、包校验、状态摘要和三平台适配器统一引用 `LEVEL.md` 的当前等级章节。
- 安装、更新和卸载契约只管理统一 `LEVEL.md`，不再复制旧版 LEVEL 文件。
- 将持续运营所需的立项、PRD、技术、任务、发布和回滚模板从旧 LEVEL 3 归位到 LEVEL 2；LEVEL 3 只保留已有、团队与开源项目改进模板。
- 保留旧状态 `1→1、2→3、3→4` 的安全迁移能力，但不再保留冗余旧文档入口。

## [0.2.0] - 2026-08-12

- 将项目模型从三级调整为四级：快速验证、可持续运营、已有/开源改进和复杂项目需求分析。
- 明确“持续更新”与“持续运营”的区别，静态、离线和可下载更新物默认保留 LEVEL 1。
- 为 LEVEL 1/2 增加 PVS-Lite、完整 PVS 和待验证事项桥接说明。
- 将旧 LEVEL 2/3 的责任模式迁移到新 LEVEL 3/4，并保留旧文件名兼容入口。
- 增加旧状态 `1→1、2→3、3→4` 迁移、备份、STATUS 记录和迁移后人工 Gate；支持显式重确认旧 LEVEL 3 为新 LEVEL 2。
- 更新四级状态校验、Doctor、包校验、适配器、模板、安装器、更新器、评测和测试。

## [0.1.0] - 2026-08-07

- 建立三级项目开发流程 Skill 首版。
- 规划 Codex、Claude Code 和 Cursor 共享核心与平台适配器。
- 定义低风险自动推进、人工 Gate、状态恢复和 Git/Draft PR 权限边界。
- 提供 Codex、Claude Code、Cursor 三平台适配器和跨平台生命周期脚本。
- 增加状态 CLI、Git 动作策略、中文场景 Evals 与发布前全包校验。
