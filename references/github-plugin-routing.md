# GitHub 插件交付路由

所有 LEVEL 的 push、Draft PR、Merge、Tag 和 Release 任务必须自动选择 Codex GitHub 插件。插件不可用或未连接时，说明安装/连接要求和降级限制；不得静默改用不受本工作流治理的远程写入方式。

## 固定流程

```text
本地验证 → GitHub 插件可用性/身份/仓库只读检查 → 远程动作计划
→ 一次执行前确认 → GitHub 插件执行远程变更 → Commit/PR/Tag/Release 远端验证
→ CHANGELOG、Release Record 与状态证据
```

## 只读检查

在请求确认前自动读取并展示：

- 目标仓库、默认分支、身份权限和当前 Remote 对应关系。
- 当前 main、目标分支、开放 PR、同名 Tag/Release 和分支保护相关事实。
- 本地提交、文件范围、验证证据、未验证项和与目标分支的差异。

只读检查不能替代本地测试，也不能把插件返回的动作成功提示当作远端验证。

## 合并后的远程动作计划

一次计划必须列出：

- 待 push 的分支和提交。
- Draft PR 的 base/head、标题、正文和 Review 重点。
- 建议 Merge 方式及其兼容、历史和回滚影响。
- `vX.X` Tag 的目标 Commit。
- Release 标题、正文、已知限制和回滚方式。
- 明确不会执行的生产、宣传或其他外部动作。

## 执行前确认

push、创建或更新 Draft PR、转 Ready、Merge、Tag、Release、删除远程分支和公开评论都属于远程写入。范围配置和历史授权不能替代本次动作确认；用户确认合并计划后，只执行计划中列出的动作。Force Push 和改写公共历史永久禁止。

## 插件执行与远端验证

批准后使用 GitHub 插件执行。完成每类动作后再次读取对应远端对象：

- push：验证远端分支 Commit SHA 与批准提交一致。
- Draft PR：验证 head/base、状态、标题、正文和关联 Commit。
- Merge：验证 PR 状态、合并方式、merge Commit 和 main 树。
- Tag：验证 Tag 名称、类型和目标 Commit。
- Release：验证 Tag、标题、正文、draft/prerelease 状态和公开 URL。

任何回读不一致都按未完成报告，不继续猜测或自动重试高影响动作。
