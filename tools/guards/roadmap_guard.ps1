$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Path (Split-Path -Path $PSScriptRoot -Parent) -Parent
$stepPath = Join-Path $repoRoot 'roadmap/phase0/step-00-bootstrap.md'

if (-not (Test-Path -Path $stepPath)) {
    Write-Error 'Roadmap guard failed. Missing roadmap/phase0/step-00-bootstrap.md.'
    exit 1
}

$content = Get-Content -Path $stepPath -Raw
if ($content -notmatch '## Status\s*\nDone') {
    Write-Error 'Roadmap guard failed. Phase 0 status is not marked Done.'
    exit 1
}

Write-Output 'Roadmap guard passed.'
