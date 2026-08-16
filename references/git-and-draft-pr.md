# Git 与 Draft PR 执行规范

## 何时读取

准备初始化 Git、创建分支、本地提交、push、Draft PR、Merge、Tag 或 Release 前读取，并同时读取 `references/github-plugin-routing.md`。

## 目标

允许 Agent 自动完成证据充分的低风险本地 Git 工作，同时避免把用户无关修改、默认分支和公共历史置于自动化风险中。

## 动作矩阵

| 动作 | 默认策略 | 自动执行前提 |
|---|---|---|
| 检查状态、分支与 Remote | 允许 | 只读 |
| `git init` | 人工 Gate | 用户确认初始化当前目录 |
| 创建本地功能分支 | 条件允许 | R1/R2、已有任务、仓库有效 |
| 本地提交 | 条件允许 | Skill 自有或已接管分支、修改全在任务范围、验证通过、无无关修改 |
| push 自有分支 | GitHub 插件确认路径 | 满足本地提交条件、范围配置开启、Remote 与身份已确认，再取得动作时确认 |
| 创建或更新 Draft PR | GitHub 插件确认路径 | push 条件成立、范围配置开启，再取得动作时确认 |
| 写入默认分支 | 禁止自动执行 | 改为功能分支与 PR 流程 |
| 删除远端分支、转 Ready、Merge、Tag、Release | GitHub 插件确认路径 | 纳入合并后的远程计划，用户明确确认后由插件执行并回读 |
| Force Push、改写公共历史 | 永久禁止 | Gate 不得覆盖 |

## 范围判定

`current_task.paths` 应列出本轮允许修改的文件或目录。提交前将 `git status --porcelain` 的全部修改与该清单比较；只要存在无关文件，就停止并报告，不能通过 `git add -A` 绕过范围检查。

## 验证证据

本地提交至少需要一条状态为 `passed`、`pass`、`ok`、`success`、`成功` 或 `通过` 的验证记录，且所有记录都必须通过。推送和 Draft PR 使用同一批验证证据，并再次展示：

- Remote 名称与 URL。
- 当前分支和默认分支。
- 待推送提交数与提交摘要。
- 修改文件范围。
- 验证命令与结果。

## 身份与远端确认

工作流 CLI 不猜测 GitHub 登录状态。Agent 应优先通过 Codex GitHub 插件确认身份、仓库和远端状态，再把事实传给策略检查。认证信息、Token 和密钥不得写入状态文件。`allow_push_own_branch` 与 `allow_create_draft_pr` 只表示范围配置，不是动作时批准。

## Qima

Qima 只作为可选提醒：在需求不清、任务范围存在争议或准备进入高影响 Gate 时，可以提醒用户手动使用。不得由本 Skill 自动调用。
