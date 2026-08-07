# 平台兼容协议

## 何时读取

安装 Skill、生成项目规则、切换 Agent 或诊断触发问题时读取。

## 共享核心

三个平台共同读取根目录 `SKILL.md`、三份 LEVEL SOP、`references/`、`templates/` 和项目状态。平台适配器不得复制或改写业务流程。

## Codex

- 个人 Skill 安装到 Codex Skills 目录，项目也可保留仓库内共享副本。
- 项目规则使用根目录 `AGENTS.md`。
- 外部 Plugin 与工具以当前会话实际可用能力为准。

## Claude Code

- 使用个人或项目 `.claude/skills/<skill-name>/SKILL.md`。
- 项目持久规则使用 `CLAUDE.md`，只放项目事实、命令和边界。
- Claude 专属 frontmatter、权限和 Hooks 只写在适配层，不能成为共享核心依赖。

## Cursor

- 使用 `.cursor/rules/project-level-workflow.mdc` 项目规则。
- 可同时使用简洁 `AGENTS.md` 作为通用项目入口。
- 不生成旧式 `.cursorrules`。
- 规则引用共享 SOP、状态和当前任务，不复制完整流程。

## 降级

平台不支持自动 Skill 发现时，用户显式引用项目规则或 `SKILL.md`。平台没有某个 Plugin 时走通用流程。任何平台都不能把指令文件视为操作系统级权限边界。
