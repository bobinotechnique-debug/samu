param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'
Set-Location $RepoRoot

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Error "npm is required to run frontend tests."
    exit 1
}

Set-Location (Join-Path $RepoRoot 'frontend')
npm install --silent --no-progress
npm run test
