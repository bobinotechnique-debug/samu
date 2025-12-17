$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Path (Split-Path -Path $PSScriptRoot -Parent) -Parent
$required = @(
    'docs/INDEX.md',
    'docs/roadmap/INDEX.md',
    'docs/specs/INDEX.md',
    'docs/api/INDEX.md',
    'docs/ux/INDEX.md',
    'docs/ops/INDEX.md',
    'specs/INDEX.md',
    'api/INDEX.md',
    'ux/INDEX.md',
    'ops/INDEX.md'
)

$missing = @()
foreach ($path in $required) {
    $fullPath = Join-Path $repoRoot $path
    if (-not (Test-Path -Path $fullPath)) {
        $missing += $path
    }
}

if ($missing.Count -gt 0) {
    Write-Error "Docs guard failed. Missing files: $($missing -join ', ')"
    exit 1
}

Write-Output "Docs guard passed."
