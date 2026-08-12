<!-- project-level-workflow:start -->
## Project Level Workflow 托管入口

- 当前流程：LEVEL {{LEVEL}}
- 权威等级流程：`{{LEVEL_DOC}}`
- 当前分层策略：{{LEVEL_MODE}}
- 机器状态：`.project-workflow/state.json`
- 人类摘要：`docs/project-workflow/STATUS.md`
- 状态校验：`python scripts/workflow.py validate --project .`

恢复会话时先校验状态。按 `LEVEL.md` 对应章节推进当前最小任务，保留用户已有修改；到人工 Gate 后报告事实、证据、风险、方案和推荐决策，未经批准不继续。LEVEL 4 只做需求分析，不写代码、不改数据库、不部署、不做自动化实现。
<!-- project-level-workflow:end -->
