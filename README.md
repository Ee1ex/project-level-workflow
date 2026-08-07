# Project Level Workflow

一套面向 AI Agent 的三级项目开发流程。它会根据项目规模、风险和生命周期推荐 LEVEL 1、LEVEL 2 或 LEVEL 3，在用户确认后自动推进低风险工作，并在人工 Gate 停止。

## 三个 LEVEL

- LEVEL 1：小工具、静态网页、插件、Skill、游戏 Mod 等轻量项目。
- LEVEL 2：已有项目改进、团队项目局部变更和 GitHub 开源贡献。
- LEVEL 3：App、SaaS、小程序、客户端等需要持续运营维护的产品。

三份根目录 LEVEL Markdown 是唯一权威 SOP，也可以分别导入语雀。

## 支持平台

- Codex：以 Agent Skill 方式安装。
- Claude Code：以项目或个人 Skill 方式安装。
- Cursor：生成项目级 `.cursor/rules/*.mdc` 与精简 `AGENTS.md` 入口。

## 工作方式

1. 读取项目目标、现有规则和历史状态。
2. 推荐 LEVEL，并等待用户确认。
3. 创建当前 LEVEL 所需的最小文档。
4. 自动执行已批准范围内的 R1/R2 工作。
5. 运行测试、Lint、类型检查或构建并记录证据。
6. 更新状态、本地提交，以及经授权的自有分支和 Draft PR。
7. 到达 R3/R4 或阶段 Gate 时停止，提交事实、证据、风险与推荐决策。

## 安全默认值

公开安装默认关闭自动远程写入：

```text
allow_push_own_branch=false
allow_create_draft_pr=false
```

Skill 禁止 Force Push、改写公共历史、提交用户无关修改、自动生产发布和自动公开宣传。Qima 仅在适用阶段提醒用户手动考虑，不由本 Skill 直接调用。

## 状态恢复

项目执行状态保存在：

```text
.project-workflow/state.json
docs/project-workflow/STATUS.md
```

前者供 Agent 恢复状态，后者供人直接查看。状态文件不得包含密钥、Token、用户数据或长日志。

## 安装

先 Clone 仓库，在包根目录审查并运行对应平台安装器。建议先使用 `DryRun` 查看目标路径：

```sh
git clone https://github.com/Ee1ex/project-level-workflow.git
cd project-level-workflow
```

```powershell
./scripts/install.ps1 -Platform codex -Scope user -DryRun
./scripts/install.ps1 -Platform codex -Scope user
```

如果 Windows 的本地执行策略阻止 `.ps1`，可在审查脚本后仅为本次进程显式运行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Platform codex -Scope user -DryRun
```

```sh
./scripts/install.sh --platform claude-code --scope user --dry-run
./scripts/install.sh --platform claude-code --scope user
```

项目级安装必须显式指定项目目录：

```powershell
./scripts/install.ps1 -Platform cursor -Scope project -ProjectPath 'D:\path\to\project' -DryRun
./scripts/install.ps1 -Platform cursor -Scope project -ProjectPath 'D:\path\to\project'
```

Cursor 项目级安装后，在目标项目根目录从已安装 Skill 路径初始化状态并生成项目 Rule：

```sh
python .cursor/skills/project-level-workflow/scripts/workflow.py init --project . --level 1
python .cursor/skills/project-level-workflow/scripts/workflow.py render-adapter --project . --platform cursor
```

LEVEL 参数应来自首次人工确认，不应由安装器猜测。Codex 或 Claude Code 也可以从各自安装目录调用同一 `workflow.py`。

## 更新与卸载

在最初 Clone 的源码目录执行 `git pull --ff-only`，审查新版本后再运行更新器；也可以从新下载并已审查的 Release 目录运行。更新器会先执行 Doctor；项目级更新在发现状态文件时先迁移状态，再把旧安装移动到带时间戳的 `backup` 目录并写入新版本，不会静默丢弃本地修改：

```sh
git pull --ff-only
```

```powershell
./scripts/update.ps1 -Platform codex -Scope user -DryRun
./scripts/update.ps1 -Platform codex -Scope user
./scripts/uninstall.ps1 -Platform codex -Scope user -DryRun
./scripts/uninstall.ps1 -Platform codex -Scope user
```

```sh
./scripts/update.sh --platform claude-code --scope user --dry-run
./scripts/update.sh --platform claude-code --scope user
./scripts/uninstall.sh --platform claude-code --scope user --dry-run
./scripts/uninstall.sh --platform claude-code --scope user
```

卸载只删除 Skill 安装目录，默认保留项目中的 `.project-workflow/` 与 `docs/project-workflow/`。

## 开发验证

核心实现只使用 Python 3.10+ 标准库：

```sh
python -m unittest discover -s tests -v
python scripts/workflow.py doctor --package-root .
```

## 版本与更新

项目使用语义化版本、Git Tag、GitHub Release 和 `CHANGELOG.md`。升级前会备份本地配置与状态；发现用户修改时停止，不静默覆盖。

## 卸载原则

卸载器只删除安装清单中由本项目创建的托管文件，默认保留项目内 `.project-workflow/` 和 `docs/project-workflow/`。删除项目状态需要单独确认。

## 许可证

[MIT License](LICENSE)
