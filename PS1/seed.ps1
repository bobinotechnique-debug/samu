param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'
Set-Location $RepoRoot

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is required to run seed scripts."
    exit 1
}

python -m pip install --upgrade pip
python -m pip install -e ./backend[dev]

if (-not $env:SAMU_DATABASE_URL) {
    $env:SAMU_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/samu"
}

Set-Location (Join-Path $RepoRoot 'backend')
python -m scripts.seed_data
