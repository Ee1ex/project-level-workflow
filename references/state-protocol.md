# 项目状态协议

## 何时读取

初始化、恢复、更新阶段、生成 Gate、迁移版本或发现聊天与项目状态冲突时读取。

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

`state.json` 是机器状态，`STATUS.md` 是人类摘要。需求、设计和任务细节仍以对应目录中的批准文档为准。

## 必填字段

- `schema_version`、`workflow_version`、`project_id`
- `level`、`stage`、`gate`、`status`、`risk`
- `permissions`、`current_task`、`artifacts`、`verifications`
- `git`、`remote`、`history`、`updated_at`

## 写入规则

- 使用 UTF-8、两空格缩进和末尾换行。
- 时间使用带时区的 ISO 8601。
- 项目文件保存相对路径，不保存个人绝对路径。
- 先写同目录临时文件，校验成功后原子替换。
- 更新前把有效旧状态复制为 `state.backup.json`。
- 不保存密钥、Token、个人信息、完整日志或大段命令输出。

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
7. 推荐选择及批准后的下一步。
