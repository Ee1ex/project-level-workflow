<!-- project-level-workflow:start -->
## Project Level Workflow 托管入口

- 当前流程：LEVEL {{LEVEL}}
- 权威等级流程：`{{LEVEL_DOC}}`
- 当前分层策略：{{LEVEL_MODE}}
- 机器状态：`.project-workflow/state.json`
- 人类摘要：`docs/project-workflow/STATUS.md`
- 状态校验：`python scripts/workflow.py validate --project .`

执行当前任务前读取状态、`LEVEL.md` 对应章节和任务文档。只在已批准范围内自动推进 R1/R2；R3/R4、生产、公开发布和高影响 Git 操作必须停在人工 Gate。LEVEL 4 只做需求分析，不写代码、不改数据库、不部署、不做自动化实现。不要在本文件复制完整等级流程。
<!-- project-level-workflow:end -->
