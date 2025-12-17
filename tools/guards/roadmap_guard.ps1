$ErrorActionPreference = 'Stop'

param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..' '..')).Path,
    [switch]$Strict
)

$rootStepPath = Join-Path $RepoRoot 'roadmap/phase0/step-00-bootstrap.md'
$docsStepPath = Join-Path $RepoRoot 'docs/roadmap/phase0/step-01-harden-bootstrap.md'
$docsRoadmapIndex = Join-Path $RepoRoot 'docs/roadmap/INDEX.md'

if (-not (Test-Path -Path $rootStepPath)) {
    Write-Error 'Roadmap guard failed. Missing roadmap/phase0/step-00-bootstrap.md.'
    throw 'Required bootstrap step is missing.'
}

$rootStepContent = Get-Content -Path $rootStepPath -Raw
if ($rootStepContent -notmatch '## Status' -or $rootStepContent -notmatch 'Done') {
    Write-Error 'Roadmap guard failed. Phase 0 bootstrap status must be marked Done.'
    throw 'Bootstrap step is not sealed.'
}

if (-not (Test-Path -Path $docsStepPath)) {
    Write-Error 'Roadmap guard failed. Missing docs/roadmap/phase0/step-01-harden-bootstrap.md.'
    throw 'Phase 0 hardening step file is missing.'
}

if (-not (Test-Path -Path $docsRoadmapIndex)) {
    Write-Error 'Roadmap guard failed. Missing docs/roadmap/INDEX.md.'
    throw 'Roadmap index is missing.'
}

$indexContent = Get-Content -Path $docsRoadmapIndex -Raw
if ($indexContent -notmatch 'docs/roadmap/phase0/step-01-harden-bootstrap.md') {
    Write-Error 'Roadmap guard failed. docs/roadmap/INDEX.md must reference docs/roadmap/phase0/step-01-harden-bootstrap.md.'
    throw 'Roadmap index does not reference Phase 0 hardening step.'
}

$requiredSections = @('## Goal', '## Deliverables', '## Acceptance Criteria', '## Tests', '## Risks')
$stepContent = Get-Content -Path $docsStepPath -Raw
$missingSections = $requiredSections | Where-Object { $stepContent -notmatch [regex]::Escape($_) }

if ($missingSections.Count -gt 0) {
    Write-Error "Roadmap guard failed. docs/roadmap/phase0/step-01-harden-bootstrap.md missing sections: $($missingSections -join ', ')"
    throw 'Phase 0 hardening step is incomplete.'
}

Write-Output 'Roadmap guard passed.'
