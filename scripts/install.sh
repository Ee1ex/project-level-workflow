#!/usr/bin/env bash
set -euo pipefail

platform=""
scope="user"
project_path="$PWD"
dry_run="false"
mode="install"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform) platform="${2:-}"; shift 2 ;;
    --scope) scope="${2:-}"; shift 2 ;;
    --project) project_path="${2:-}"; shift 2 ;;
    --dry-run) dry_run="true"; shift ;;
    --mode) mode="${2:-}"; shift 2 ;;
    *) echo "错误：未知参数：$1" >&2; exit 2 ;;
  esac
done

case "$platform" in codex|claude-code|cursor) ;; *) echo "错误：--platform 必须是 codex、claude-code 或 cursor。" >&2; exit 2 ;; esac
case "$scope" in user|project) ;; *) echo "错误：--scope 必须是 user 或 project。" >&2; exit 2 ;; esac
case "$mode" in install|update) ;; *) echo "错误：内部 mode 无效。" >&2; exit 2 ;; esac

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)"
package_root="$(CDPATH= cd -- "$script_dir/.." && pwd -P)"
version_file="$package_root/VERSION"
[[ -f "$version_file" ]] || { echo "错误：找不到 VERSION，当前目录不是完整的 project-level-workflow 包。" >&2; exit 1; }
version="$(tr -d '\r\n' < "$version_file")"

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
  *) echo "错误：拒绝操作非托管目标：$target" >&2; exit 1 ;;
esac

installed_version_file="$target/VERSION"
if [[ "$mode" == "update" && ! -f "$installed_version_file" ]]; then
  echo "错误：目标未安装，不能更新：$target" >&2
  exit 1
fi

backup=""
if [[ -e "$target" ]]; then
  installed_version="unknown"
  [[ -f "$installed_version_file" ]] && installed_version="$(tr -d '\r\n' < "$installed_version_file")"
  if [[ "$mode" == "install" && "$installed_version" == "$version" ]]; then
    echo "project-level-workflow $version 已安装：$target"
    exit 0
  fi
  backup="$target.backup-$(date +%Y%m%d-%H%M%S)"
  [[ ! -e "$backup" ]] || { echo "错误：conflict backup 已存在：$backup" >&2; exit 1; }
fi

echo "模式：$mode；平台：$platform；范围：$scope；版本：$version"
echo "目标：$target"
[[ -z "$backup" ]] || echo "检测到现有安装或修改，将先创建 conflict backup：$backup"
if [[ "$dry_run" == "true" ]]; then
  echo "DryRun：仅显示计划，不写入文件。"
  exit 0
fi

mkdir -p -- "$(dirname -- "$target")"
[[ -z "$backup" ]] || mv -- "$target" "$backup"
mkdir -p -- "$target"

items=(SKILL.md README.md VERSION CHANGELOG.md LICENSE \
  LEVEL1-快速验证与轻量交付流程.md LEVEL2-可持续运营项目开发流程.md \
  LEVEL3-已有与开源项目改进流程.md LEVEL4-复杂项目需求分析流程.md \
  LEVEL1-小型项目开发流程.md LEVEL2-已有与开源项目改进流程.md LEVEL3-持续运营产品开发流程.md \
  references templates schemas scripts adapters evals)
for item in "${items[@]}"; do
  [[ -e "$package_root/$item" ]] || continue
  cp -R -- "$package_root/$item" "$target/"
done

echo "完成：project-level-workflow $version 已安装到 $target"
[[ -z "$backup" ]] || echo "原版本已保留在：$backup"
