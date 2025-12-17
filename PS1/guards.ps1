$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Path $PSScriptRoot -Parent

& "$repoRoot/tools/guards/ascii_guard.ps1"
& "$repoRoot/tools/guards/docs_guard.ps1"
& "$repoRoot/tools/guards/roadmap_guard.ps1"
& "$repoRoot/tools/guards/agents_guard.ps1"

Write-Output 'All guards passed.'
