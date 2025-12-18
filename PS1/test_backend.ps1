param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'
Set-Location $RepoRoot

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is required to run backend tests."
    exit 1
}

python -m pip install --upgrade pip
python -m pip install -e ./backend[dev]

$env:SAMU_DATABASE_URL = "sqlite+pysqlite:///:memory:"
$env:SAMU_REDIS_URL = "redis://localhost:6379/0"
$env:SAMU_TESTING = "true"
$env:SAMU_ENVIRONMENT = "ci"

python -m pytest backend/tests
