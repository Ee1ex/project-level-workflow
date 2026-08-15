[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('codex', 'claude-code', 'cursor')]
    [string]$Platform,
    [ValidateSet('user', 'project')]
    [string]$Scope = 'user',
    [string]$ProjectPath = (Get-Location).Path,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$installer = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'install.ps1'))
if (-not (Test-Path -LiteralPath $installer -PathType Leaf)) {
    throw "错误：找不到 project-level-workflow 安装器。"
}
$packageRoot = [System.IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
$workflow = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'workflow.py'))
$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCommand) {
    $pythonCommand = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $pythonCommand -or -not (Test-Path -LiteralPath $workflow -PathType Leaf)) {
    throw "错误：更新前 Doctor 需要 Python 3.10+ 和 scripts/workflow.py。"
}

& $pythonCommand.Source $workflow doctor --package-root $packageRoot
if ($LASTEXITCODE -ne 0) {
    throw "错误：新版本 Doctor 未通过，已停止更新。"
}

if ($Scope -eq 'project') {
    $resolvedProject = [System.IO.Path]::GetFullPath($ProjectPath)
    $statePath = Join-Path $resolvedProject '.project-workflow/state.json'
    if (Test-Path -LiteralPath $statePath -PathType Leaf) {
        if ($DryRun) {
            Write-Host "DryRun：将对项目状态执行 migrate：$resolvedProject"
        } else {
            & $pythonCommand.Source $workflow migrate --project $resolvedProject
            if ($LASTEXITCODE -ne 0) {
                throw "错误：项目状态 migrate 失败，已停止更新。"
            }
        }
    }
}

# 更新复用安装器的原生 PowerShell 路径逻辑；staging 安装器会先校验包，
# 再同步统一 LEVEL.md、PVS 包内内核、VERSION、conflict 与 backup 策略。
$target = [System.IO.Path]::GetFullPath($ProjectPath)
Write-Verbose "更新基准路径：$target"
& $installer -Platform $Platform -Scope $Scope -ProjectPath $ProjectPath -DryRun:$DryRun -Mode update
