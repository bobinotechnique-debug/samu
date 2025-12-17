param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..' '..')).Path,
    [switch]$Strict
)

$ErrorActionPreference = 'Stop'

$agents = @(
    'agents/backend.md',
    'agents/frontend.md',
    'agents/devops.md',
    'agents/docs.md'
)

$missing = @()
$precedenceViolations = @()
$headerViolations = @()

foreach ($agent in $agents) {
    $fullPath = Join-Path $RepoRoot $agent
    if (-not (Test-Path -Path $fullPath)) {
        $missing += $agent
        continue
    }

    $content = Get-Content -Path $fullPath -Raw

    if ($content -notmatch 'Root agent \(AGENT\.md\) overrides') {
        $precedenceViolations += $agent
    }

    $headerLine = ($content -split "`n")[0]
    if (-not $headerLine.Trim().StartsWith('#')) {
        $headerViolations += $agent
    }
}

if ($missing.Count -gt 0) {
    Write-Error "Agents guard failed. Missing agents: $($missing -join ', ')"
    throw 'Required agent files are missing.'
}

if ($precedenceViolations.Count -gt 0) {
    Write-Error "Agents guard failed. Precedence not declared in: $($precedenceViolations -join ', ')"
    throw 'Agent precedence violations detected.'
}

if ($headerViolations.Count -gt 0) {
    Write-Error "Agents guard failed. Missing agent header lines in: $($headerViolations -join ', ')"
    throw 'Agent headers are missing.'
}

Write-Output 'Agents guard passed.'
