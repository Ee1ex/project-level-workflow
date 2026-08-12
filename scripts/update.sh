#!/usr/bin/env bash
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)"
installer="$script_dir/install.sh"
target="project-level-workflow"
[[ -f "$installer" ]] || { printf '错误：找不到 %s 安装器。\n' "$target" >&2; exit 1; }
package_root="$(CDPATH= cd -- "$script_dir/.." && pwd -P)"
workflow="$script_dir/workflow.py"
[[ -f "$workflow" ]] || { echo "错误：找不到 workflow.py，不能运行 Doctor。" >&2; exit 1; }

if command -v python3 >/dev/null 2>&1; then
  python_cmd="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  python_cmd="$(command -v python)"
else
  echo "错误：更新前 Doctor 需要 Python 3.10+。" >&2
  exit 1
fi

forward_args=("$@")
scope="user"
project_path="$PWD"
dry_run="false"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --scope) scope="${2:-}"; shift 2 ;;
    --project) project_path="${2:-}"; shift 2 ;;
    --dry-run) dry_run="true"; shift ;;
    --platform) shift 2 ;;
    *) echo "错误：未知参数：$1" >&2; exit 2 ;;
  esac
done

"$python_cmd" "$workflow" doctor --package-root "$package_root"
if [[ "$scope" == "project" && -f "$project_path/.project-workflow/state.json" ]]; then
  if [[ "$dry_run" == "true" ]]; then
    echo "DryRun：将对项目状态执行 migrate：$project_path"
  else
    "$python_cmd" "$workflow" migrate --project "$project_path"
  fi
fi

# 统一 LEVEL.md、VERSION、conflict 与 backup 策略由同目录安装器统一执行，不再安装分散或旧版 LEVEL 文档。
# 包括 --dry-run 在内的全部公开参数都会保持原始参数边界转发。
# shellcheck disable=SC2086 -- 参数通过 "$@" 保持原始边界。
exec "$installer" "${forward_args[@]}" --mode update
