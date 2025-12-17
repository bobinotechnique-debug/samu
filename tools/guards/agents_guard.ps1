$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Path (Split-Path -Path $PSScriptRoot -Parent) -Parent
$agents = @(
    'agents/backend.md',
    'agents/frontend.md',
    'agents/devops.md',
    'agents/docs.md'
)

$missing = @()
$violations = @()

foreach ($agent in $agents) {
    $fullPath = Join-Path $repoRoot $agent
    if (-not (Test-Path -Path $fullPath)) {
        $missing += $agent
        continue
    }

    $content = Get-Content -Path $fullPath -Raw
    if ($content -notmatch 'Root agent \(AGENT\.md\) overrides') {
        $violations += $agent
    }
}

if ($missing.Count -gt 0) {
    Write-Error "Agents guard failed. Missing agents: $($missing -join ', ')"
    exit 1
}

if ($violations.Count -gt 0) {
    Write-Error "Agents guard failed. Precedence not declared in: $($violations -join ', ')"
    exit 1
}

Write-Output 'Agents guard passed.'
