param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')),
    [switch]$Strict
)

$ErrorActionPreference = 'Stop'

$resolvedRepoRoot = (Resolve-Path -Path $RepoRoot).Path

$guards = @(
    @{ Name = 'ASCII'; Path = Join-Path $resolvedRepoRoot 'tools/guards/ascii_guard.ps1' },
    @{ Name = 'Agents'; Path = Join-Path $resolvedRepoRoot 'tools/guards/agents_guard.ps1' },
    @{ Name = 'Docs'; Path = Join-Path $resolvedRepoRoot 'tools/guards/docs_guard.ps1' },
    @{ Name = 'Roadmap'; Path = Join-Path $resolvedRepoRoot 'tools/guards/roadmap_guard.ps1' }
)

foreach ($guard in $guards) {
    if (-not (Test-Path -Path $guard.Path)) {
        Write-Error "${($guard.Name)} guard script not found at $($guard.Path)."
        exit 1
    }

    try {
        & $guard.Path -RepoRoot $resolvedRepoRoot -Strict:$Strict
        Write-Output "${($guard.Name)} guard: PASS"
    } catch {
        Write-Output "${($guard.Name)} guard: FAIL"
        if ($_.Exception.Message) {
            Write-Output $_.Exception.Message
        }
        exit 1
    }
}

Write-Output 'All guards passed.'
