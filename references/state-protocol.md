# 项目状态协议

## 何时读取

初始化、恢复、更新阶段、生成 Gate、迁移版本、切换 LEVEL 或发现聊天与项目状态冲突时读取。

## 权威文件

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

`state.json` 是机器状态，`STATUS.md` 是人类摘要。需求、设计和任务细节仍以对应目录中的批准文档为准。LEVEL 1 可以使用精简目录；LEVEL 2 按完整 PVS 维护实际项目目录；LEVEL 3 沿用已有仓库目录；LEVEL 4 只写分析材料和待确认记录。

## 必填字段

- `schema_version`、`workflow_version`、`project_id`
- `level`、`stage`、`gate`、`status`、`risk`
- `permissions`、`current_task`、`artifacts`、`verifications`
- `git`、`remote`、`history`、`updated_at`

`level` 只能是 1、2、3 或 4。LEVEL 是责任模式，不替代 `risk`。

## 写入规则

- 使用 UTF-8、两空格缩进和末尾换行。
- 时间使用带时区的 ISO 8601。
- 项目文件保存相对路径，不保存个人绝对路径。
- 先写同目录临时文件，校验成功后原子替换。
- 更新前把有效旧状态复制为 `state.backup.json`。
- 不保存密钥、Token、个人信息、完整日志或大段命令输出。
- 未运行的检查必须写成待验证，不得写成通过。

## 旧等级迁移

旧状态数字语义固定为：

```text
旧 LEVEL 1 → 新 LEVEL 1
旧 LEVEL 2 → 新 LEVEL 3
旧 LEVEL 3 → 新 LEVEL 4
```

迁移顺序是：读取并校验可迁移状态 → 写 `state.backup.json` → 写新 Schema 和新 LEVEL → 写 `STATUS.md`。迁移事件必须包含旧/新 LEVEL、来源/目标 Schema、迁移原因和时间。迁移后 Gate 设为 `level-migration-review`、状态设为等待人工确认，不能把旧 Gate 静默当作已批准。新 LEVEL 2 没有自动来源；旧 LEVEL 3 改为新 LEVEL 2 时必须记录 `approved_by` 和 `reason`。

## 恢复规则

1. 先校验 `state.json`。
2. 无效时校验备份。
3. 可恢复时展示差异并恢复。
4. 两份都无效时，从文档和 Git 生成恢复建议，但不猜测用户是否批准过 Gate。
5. 聊天与状态冲突时展示双方证据并询问。

## `STATUS.md` 固定结构

1. 当前 LEVEL、阶段和状态。
2. 本轮目标与不做范围。
3. 已完成内容。
4. 验证命令与结果摘要。
5. 当前风险和未决事项。
6. 当前人工 Gate。
7. 最近等级迁移记录。
8. 推荐选择及批准后的下一步。
