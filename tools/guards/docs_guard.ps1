param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..' '..')).Path,
    [switch]$Strict
)

$ErrorActionPreference = 'Stop'

$required = @(
    'docs/INDEX.md',
    'docs/roadmap/INDEX.md',
    'docs/roadmap/phase0/INDEX.md',
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
    $fullPath = Join-Path $RepoRoot $path
    if (-not (Test-Path -Path $fullPath)) {
        $missing += $path
    }
}

if ($missing.Count -gt 0) {
    Write-Error "Docs guard failed. Missing files: $($missing -join ', ')"
    throw 'Documentation index files are missing.'
}

$indexReferenceErrors = @()

function Test-IndexReferences {
    param(
        [string]$IndexPath
    )

    $content = Get-Content -Path $IndexPath -Raw
    $matches = [regex]::Matches($content, "^-\s+([^\s]+)", 'Multiline')

    foreach ($match in $matches) {
        $relativeRef = $match.Groups[1].Value
        if ($relativeRef -notmatch '\\.md$') {
            continue
        }
        $targetPath = Join-Path $RepoRoot $relativeRef
        if (-not (Test-Path -Path $targetPath)) {
            $indexReferenceErrors += "$relativeRef referenced in $IndexPath is missing"
        }
    }
}

foreach ($path in $required) {
    Test-IndexReferences -IndexPath (Join-Path $RepoRoot $path)
}

if ($indexReferenceErrors.Count -gt 0) {
    Write-Error 'Docs guard failed. Index files reference missing targets.'
    foreach ($entry in $indexReferenceErrors) {
        Write-Error $entry
    }
    throw 'Index reference validation failed.'
}

$orphanFolders = @()
$docRoots = @('docs')

foreach ($docRoot in $docRoots) {
    $rootPath = Join-Path $RepoRoot $docRoot
    if (-not (Test-Path -Path $rootPath)) {
        continue
    }

    Get-ChildItem -Path $rootPath -Directory -Recurse | ForEach-Object {
        $indexPath = Join-Path $_.FullName 'INDEX.md'
        $markdownFiles = Get-ChildItem -Path $_.FullName -Filter '*.md' -File
        if ($markdownFiles.Count -gt 0 -and -not (Test-Path -Path $indexPath)) {
            $relativeDir = Resolve-Path -Path $_.FullName | ForEach-Object { $_.Path.Replace($RepoRoot + [System.IO.Path]::DirectorySeparatorChar, '') }
            $orphanFolders += $relativeDir
        }
    }
}

if ($orphanFolders.Count -gt 0) {
    Write-Error 'Docs guard failed. Directories with markdown files are missing INDEX.md.'
    foreach ($folder in $orphanFolders) {
        Write-Error "Missing INDEX.md in $folder"
    }
    throw 'Orphan documentation directories detected.'
}

$agentErrorTemplatePath = Join-Path $RepoRoot 'docs/ops/agent_errors.md'
$agentErrorTemplate = Get-Content -Path $agentErrorTemplatePath -Raw
$requiredSections = @('## Summary', '## How to add an entry', '## Entry template', '## Known Failure Patterns')
$missingSections = $requiredSections | Where-Object { $agentErrorTemplate -notmatch [regex]::Escape($_) }

if ($missingSections.Count -gt 0) {
    Write-Error "Docs guard failed. docs/ops/agent_errors.md is missing sections: $($missingSections -join ', ')"
    throw 'Agent error log template is incomplete.'
}

$requiredFields = @('Date:', 'Context (step ref):', 'Symptom:', 'Root cause:', 'Fix:', 'Prevention:', 'Files touched:')
$missingFields = $requiredFields | Where-Object { $agentErrorTemplate -notmatch [regex]::Escape($_) }

if ($missingFields.Count -gt 0) {
    Write-Error "Docs guard failed. docs/ops/agent_errors.md entry template missing fields: $($missingFields -join ', ')"
    throw 'Agent error log fields are incomplete.'
}

Write-Output 'Docs guard passed.'
