#!/usr/bin/env bash
set -euo pipefail

platform=""
scope="user"
project_path="$PWD"
dry_run="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform) platform="${2:-}"; shift 2 ;;
    --scope) scope="${2:-}"; shift 2 ;;
    --project) project_path="${2:-}"; shift 2 ;;
    --dry-run) dry_run="true"; shift ;;
    *) echo "错误：未知参数：$1" >&2; exit 2 ;;
  esac
done

case "$platform" in codex|claude-code|cursor) ;; *) echo "错误：--platform 无效。" >&2; exit 2 ;; esac
case "$scope" in user|project) ;; *) echo "错误：--scope 无效。" >&2; exit 2 ;; esac

if [[ "$scope" == "project" ]]; then
  [[ -d "$project_path" ]] || { echo "错误：项目目录不存在：$project_path" >&2; exit 1; }
  base="$(CDPATH= cd -- "$project_path" && pwd -P)"
  case "$platform" in
    codex) target="$base/.codex/skills/project-level-workflow" ;;
    claude-code) target="$base/.claude/skills/project-level-workflow" ;;
    cursor) target="$base/.cursor/skills/project-level-workflow" ;;
  esac
else
  case "$platform" in
    codex) target="${CODEX_HOME:-$HOME/.codex}/skills/project-level-workflow" ;;
    claude-code) target="$HOME/.claude/skills/project-level-workflow" ;;
    cursor) target="$HOME/.cursor/skills/project-level-workflow" ;;
  esac
fi

case "$target" in
  */project-level-workflow) ;;
  *) echo "错误：拒绝删除非托管路径：$target" >&2; exit 1 ;;
esac

echo "将卸载 project-level-workflow：$target"
echo "托管目录包含统一 LEVEL.md；只删除该托管目录。"
echo "托管目录中的 PVS 包内内核将随 project-level-workflow 一起移除。"
echo "独立 project-vibe-spec 不属于本包托管范围，本卸载器不处理。"
echo "项目状态 .project-workflow 与 docs/project-workflow 将保留。"
[[ -e "$target" ]] || { echo "未发现安装目录，无需处理。"; exit 0; }
if [[ "$dry_run" == "true" ]]; then
  echo "DryRun：仅显示计划，不删除文件。"
  exit 0
fi

rm -rf -- "$target"
echo "卸载完成；项目执行状态仍然保留。"
