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

function Resolve-UninstallTarget {
    if ($Scope -eq 'project') {
        if (-not (Test-Path -LiteralPath $ProjectPath -PathType Container)) {
            throw "错误：项目目录不存在：$ProjectPath"
        }
        $base = [System.IO.Path]::GetFullPath((Resolve-Path -LiteralPath $ProjectPath).Path)
        $relative = switch ($Platform) {
            'codex' { '.codex/skills/elx-level' }
            'claude-code' { '.claude/skills/elx-level' }
            'cursor' { '.cursor/skills/elx-level' }
        }
        return [System.IO.Path]::GetFullPath((Join-Path $base $relative))
    }

    $userRoot = [System.IO.Path]::GetFullPath($env:USERPROFILE)
    $resolved = switch ($Platform) {
        'codex' {
            $codexRoot = if ([string]::IsNullOrWhiteSpace($env:CODEX_HOME)) { Join-Path $userRoot '.codex' } else { [System.IO.Path]::GetFullPath($env:CODEX_HOME) }
            [System.IO.Path]::GetFullPath((Join-Path $codexRoot 'skills/elx-level'))
        }
        'claude-code' { [System.IO.Path]::GetFullPath((Join-Path $userRoot '.claude/skills/elx-level')) }
        'cursor' { [System.IO.Path]::GetFullPath((Join-Path $userRoot '.cursor/skills/elx-level')) }
    }
    return $resolved
}

$target = Resolve-UninstallTarget
if ((Split-Path -Leaf $target) -ne 'elx-level') {
    throw "错误：拒绝删除非托管路径：$target"
}

Write-Host "将卸载 elx-level：$target"
Write-Host '托管目录包含统一 LEVEL.md；只删除该托管目录。'
Write-Host '托管目录中的 PVS 包内内核将随 elx-level 一起移除。'
Write-Host '独立 project-vibe-spec 不属于本包托管范围，本卸载器不处理。'
Write-Host '新状态 .elx-level 与 docs/elx-level 将保留；旧状态 .project-workflow 也将保留。'
Write-Host '旧 Skill project-level-workflow 不在本次卸载范围。'
if (-not (Test-Path -LiteralPath $target)) {
    Write-Host '未发现安装目录，无需处理。'
    exit 0
}
if ($DryRun) {
    Write-Host 'DryRun：仅显示计划，不删除文件。'
    exit 0
}

Remove-Item -LiteralPath $target -Recurse -Force
Write-Host '卸载完成；项目执行状态仍然保留。'
