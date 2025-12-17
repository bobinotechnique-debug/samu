$ErrorActionPreference = 'Stop'

param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..' '..')).Path,
    [switch]$Strict
)

$binaryExtensions = @(
    '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.ico', '.pdf', '.zip', '.gz', '.tgz',
    '.xz', '.7z', '.tar', '.jar', '.exe', '.dll', '.pdb', '.so', '.dylib', '.mp3', '.mp4'
)

try {
    $trackedFiles = git -C $RepoRoot ls-files
} catch {
    Write-Error 'ASCII guard failed. Unable to list tracked files via git.'
    throw
}

$nonAscii = @()

foreach ($relativePath in $trackedFiles) {
    $extension = [System.IO.Path]::GetExtension($relativePath).ToLowerInvariant()
    if ($binaryExtensions -contains $extension) {
        continue
    }

    $fullPath = Join-Path $RepoRoot $relativePath
    if (-not (Test-Path -Path $fullPath)) {
        continue
    }

    $bytes = [System.IO.File]::ReadAllBytes($fullPath)
    $lineNumber = 1

    for ($i = 0; $i -lt $bytes.Length; $i++) {
        $current = $bytes[$i]

        if ($current -eq 10) {
            $lineNumber++
            continue
        }

        if ($current -gt 127) {
            $nonAscii += [pscustomobject]@{
                Path = $relativePath
                Line = $lineNumber
                ByteValue = $current
            }
            break
        }
    }
}

if ($nonAscii.Count -gt 0) {
    Write-Error 'ASCII guard failed. Non-ASCII content detected.'
    foreach ($item in $nonAscii) {
        Write-Error "Non-ASCII byte $($item.ByteValue) detected in $($item.Path) at line $($item.Line)."
    }
    throw 'ASCII guard blocked due to non-ASCII content.'
}

Write-Output 'ASCII guard passed.'
