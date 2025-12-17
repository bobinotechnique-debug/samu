$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Path (Split-Path -Path $PSScriptRoot -Parent) -Parent
$nonAscii = @()

Get-ChildItem -Path $repoRoot -Recurse -File | Where-Object {
    $_.FullName -notmatch '[\\/]\.git[\\/]'
} | ForEach-Object {
    $content = [System.IO.File]::ReadAllText($_.FullName)
    if ($content.ToCharArray() | Where-Object { [int][char]$_ -gt 127 }) {
        $nonAscii += $_.FullName
    }
}

if ($nonAscii.Count -gt 0) {
    Write-Error "Non-ASCII content detected."
    $nonAscii | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Output "ASCII guard passed."
