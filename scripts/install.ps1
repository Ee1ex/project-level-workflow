[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('codex', 'claude-code', 'cursor')]
    [string]$Platform,

    [ValidateSet('user', 'project')]
    [string]$Scope = 'user',

    [string]$ProjectPath = (Get-Location).Path,
    [switch]$DryRun,

    [Parameter(DontShow = $true)]
    [ValidateSet('install', 'update')]
    [string]$Mode = 'install'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Resolve-InstallTarget {
    param([string]$SelectedPlatform, [string]$SelectedScope, [string]$SelectedProject)

    if ($SelectedScope -eq 'project') {
        if (-not (Test-Path -LiteralPath $SelectedProject -PathType Container)) {
            throw "错误：项目目录不存在：$SelectedProject"
        }
        $base = [System.IO.Path]::GetFullPath((Resolve-Path -LiteralPath $SelectedProject).Path)
        $relative = switch ($SelectedPlatform) {
            'codex' { '.codex/skills/project-level-workflow' }
            'claude-code' { '.claude/skills/project-level-workflow' }
            'cursor' { '.cursor/skills/project-level-workflow' }
        }
        return [System.IO.Path]::GetFullPath((Join-Path $base $relative))
    }

    $userRoot = [System.IO.Path]::GetFullPath($env:USERPROFILE)
    $resolved = switch ($SelectedPlatform) {
        'codex' {
            $codexRoot = if ([string]::IsNullOrWhiteSpace($env:CODEX_HOME)) {
                Join-Path $userRoot '.codex'
            } else {
                [System.IO.Path]::GetFullPath($env:CODEX_HOME)
            }
            [System.IO.Path]::GetFullPath((Join-Path $codexRoot 'skills/project-level-workflow'))
        }
        'claude-code' { [System.IO.Path]::GetFullPath((Join-Path $userRoot '.claude/skills/project-level-workflow')) }
        'cursor' { [System.IO.Path]::GetFullPath((Join-Path $userRoot '.cursor/skills/project-level-workflow')) }
    }
    return $resolved
}

function Assert-SafeTarget {
    param([string]$TargetPath)

    $leaf = Split-Path -Leaf $TargetPath
    if ($leaf -ne 'project-level-workflow') {
        throw "错误：拒绝操作非托管目标：$TargetPath"
    }
    $root = [System.IO.Path]::GetPathRoot($TargetPath)
    if ($TargetPath -eq $root -or $TargetPath.Length -le $root.Length + 8) {
        throw "错误：目标路径过宽，已停止：$TargetPath"
    }
}

function Copy-Package {
    param([string]$SourceRoot, [string]$TargetPath)

    $items = @(
    'SKILL.md', 'README.md', 'LEVEL.md', 'VERSION', 'CHANGELOG.md', 'LICENSE',
        'references', 'templates', 'schemas', 'scripts', 'adapters', 'evals'
    )
    New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
    foreach ($item in $items) {
        $sourceItem = Join-Path $SourceRoot $item
        if (Test-Path -LiteralPath $sourceItem) {
            Copy-Item -LiteralPath $sourceItem -Destination $TargetPath -Recurse -Force
        }
    }
}

$packageRoot = [System.IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
$versionPath = Join-Path $packageRoot 'VERSION'
if (-not (Test-Path -LiteralPath $versionPath -PathType Leaf)) {
    throw "错误：找不到 VERSION，当前目录不是完整的 project-level-workflow 包。"
}
$version = (Get-Content -LiteralPath $versionPath -Raw -Encoding UTF8).Trim()
$target = Resolve-InstallTarget -SelectedPlatform $Platform -SelectedScope $Scope -SelectedProject $ProjectPath
Assert-SafeTarget -TargetPath $target

$installedVersionPath = Join-Path $target 'VERSION'
if ($Mode -eq 'update' -and -not (Test-Path -LiteralPath $installedVersionPath -PathType Leaf)) {
    throw "错误：目标未安装，不能更新：$target"
}

$backup = $null
if (Test-Path -LiteralPath $target) {
    $installedVersion = if (Test-Path -LiteralPath $installedVersionPath -PathType Leaf) {
        (Get-Content -LiteralPath $installedVersionPath -Raw -Encoding UTF8).Trim()
    } else {
        'unknown'
    }
    if ($Mode -eq 'install' -and $installedVersion -eq $version) {
        Write-Host "project-level-workflow $version 已安装：$target"
        exit 0
    }
    $timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $backup = "$target.backup-$timestamp"
    if (Test-Path -LiteralPath $backup) {
        throw "错误：冲突备份已存在，请稍后重试：$backup"
    }
}

Write-Host "模式：$Mode；平台：$Platform；范围：$Scope；版本：$version"
Write-Host "目标：$target"
if ($backup) {
    Write-Host "检测到现有安装或修改，将先创建 conflict backup：$backup"
}
if ($DryRun) {
    Write-Host 'DryRun：仅显示计划，不写入文件。'
    exit 0
}

$parent = Split-Path -Parent $target
New-Item -ItemType Directory -Path $parent -Force | Out-Null
if ($backup) {
    Move-Item -LiteralPath $target -Destination $backup
}

try {
    Copy-Package -SourceRoot $packageRoot -TargetPath $target
} catch {
    if ((-not (Test-Path -LiteralPath $target)) -and $backup -and (Test-Path -LiteralPath $backup)) {
        Move-Item -LiteralPath $backup -Destination $target
    }
    throw
}

Write-Host "完成：project-level-workflow $version 已安装到 $target"
if ($backup) {
    Write-Host "原版本已保留在：$backup"
}
