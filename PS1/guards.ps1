param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path,
    [switch]$Strict
)

$ErrorActionPreference = 'Stop'

& (Join-Path $RepoRoot 'PS1' 'validate.ps1') -RepoRoot $RepoRoot -Strict:$Strict
