# 项目状态协议

## 何时读取

初始化、恢复、更新阶段、生成 Gate、迁移版本、切换 LEVEL 或发现聊天与项目状态冲突时读取。

## 权威文件

```text
.elx-level/
├─ state.json
└─ state.backup.json

docs/elx-level/
├─ STATUS.md
├─ decisions/
├─ requirements/
├─ tasks/
├─ evidence/
└─ gates/
```

`state.json` 是机器状态，`STATUS.md` 是人类摘要。需求、设计和任务细节仍以对应目录中的批准文档为准。LEVEL 1 使用双层项目记忆；LEVEL 2 按完整 PVS 维护实际项目目录；LEVEL 3 沿用已有仓库目录；LEVEL 4 先写分析材料，负责人确认后可进入实现参考节点。

## 必填字段

- `schema_version`、`workflow_version`、`project_id`
- `level`、`stage`、`gate`、`status`、`risk`、`execution_policy`
- `permissions`、`current_task`、`artifacts`、`verifications`
- `git`、`remote`、`history`、`updated_at`

`level` 只能是 1、2、3 或 4。`execution_policy` 只能是 `AUTO`、`CONFIRM` 或 `MANUAL_ONLY`。`risk` 为兼容字段；LEVEL 1–3 的普通摘要不重复展示空风险和空 Gate。

## 写入规则

- 使用 UTF-8、两空格缩进和末尾换行。
- 时间使用带时区的 ISO 8601。
- 项目文件保存相对路径，不保存个人绝对路径。
- 先写同目录临时文件，校验成功后原子替换。
- 更新前把有效旧状态复制为 `state.backup.json`。
- 不保存密钥、Token、个人信息、完整日志或大段命令输出。
- 未运行的检查必须写成待验证，不得写成通过。

## 状态迁移

ELX Level 2.0 只允许 `migrate` 从旧 `.project-workflow` 一次性复制到 `.elx-level`；旧目录保持不变。其他命令发现只有旧目录时必须停止并提示运行 `migrate`，不得隐式复制。新旧状态目录并存时必须停止并要求人工核对，不覆盖任何一方。迁移后的状态摘要写入 `docs/elx-level/STATUS.md`。

Schema `1.1.0` / workflow `0.4.0` 迁移到 `2.0` / `2.0` 时保持 LEVEL 1–4 不变；LEVEL 1–3 不新增语义 Gate，LEVEL 4 保持分析阶段并进入 `level4-execution-review`。

更老状态的数字语义固定为：

旧状态数字语义固定为：

```text
旧 LEVEL 1 → 新 LEVEL 1
旧 LEVEL 2 → 新 LEVEL 3
旧 LEVEL 3 → 新 LEVEL 4
```

更老状态的迁移顺序是：读取并校验可迁移状态 → 写 `state.backup.json` → 写新 Schema 和新 LEVEL → 写 `STATUS.md`。迁移事件必须包含旧/新 LEVEL、来源/目标 Schema、迁移原因和时间；数字重映射后 Gate 设为 `level-migration-review`、状态设为等待人工确认，不能把旧 Gate 静默当作已批准。旧 LEVEL 3 改为新 LEVEL 2 时必须记录 `approved_by` 和 `reason`。

## 恢复规则

1. 先校验 `state.json`。
2. 无效时校验备份。
3. 可恢复时展示差异并恢复。
4. 两份都无效时，从文档和 Git 生成恢复建议，但不猜测用户是否批准过 Gate。
5. 聊天与状态冲突时展示双方证据并询问。

## `STATUS.md` 分层结构

1. 当前 LEVEL、阶段和状态。
2. 本轮目标与不做范围。
3. 已完成内容。
4. 验证命令与结果摘要。
5. 执行策略；LEVEL 4 始终显示风险和 Gate，LEVEL 1–3 只在非空或高影响时显示。
6. 当前人工 Gate（存在时）。
7. 最近等级迁移记录。
8. 推荐选择及批准后的下一步。
