<#
.SYNOPSIS
    Download (or safely re-download) the UnlockAI workshop workspace on Windows.

.DESCRIPTION
    The no-git path from BOOTSTRAP.md Step 2 method C, as a script you can just run.
    Safe to run again after a failed attempt: an existing workspace is renamed to
    <name>-backup-<timestamp> rather than deleted, so a student's brand file,
    output/ work and .env are never lost.

    Needs no admin rights, no git, and no Python. Windows PowerShell 5.1 or 7.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File windows\get-workspace.ps1
#>
[CmdletBinding()]
param(
    # Where the workspace should end up.
    [string] $TargetFolder = (Join-Path $HOME "Downloads\unlockai-social-media"),

    [string] $ArchiveUrl = "https://codeload.github.com/Kusalin-T/unlockai-social-media/zip/refs/heads/master",

    # Folder name inside the GitHub zip (repo name + branch).
    [string] $ArchiveRootName = "unlockai-social-media-master"
)

$ErrorActionPreference = 'Stop'
# Invoke-WebRequest in PowerShell 5.1 is dramatically slower with the progress bar on.
$ProgressPreference = 'SilentlyContinue'

$bootstrapTemp = Join-Path $env:TEMP ("unlockai-bootstrap-" + [guid]::NewGuid().ToString("N"))
$archivePath = Join-Path $bootstrapTemp "unlockai.zip"
$extractPath = Join-Path $bootstrapTemp "extract"

try {
    # Back up BEFORE the move. Move-Item onto an existing folder either fails or,
    # with -Force, moves the source *inside* it and still reports success.
    if (Test-Path -LiteralPath $TargetFolder) {
        $backup = "$TargetFolder-backup-" + (Get-Date -Format 'yyyyMMdd-HHmmss')
        Move-Item -LiteralPath $TargetFolder -Destination $backup
        Write-Host "Kept your previous workspace as:" -ForegroundColor Yellow
        Write-Host "  $backup"
    }

    New-Item -ItemType Directory -Force -Path $extractPath | Out-Null

    Write-Host "Downloading the toolkit..."
    Invoke-WebRequest -Uri $ArchiveUrl -Headers @{ "Cache-Control" = "no-cache" } -OutFile $archivePath

    Expand-Archive -Path $archivePath -DestinationPath $extractPath

    $extracted = Join-Path $extractPath $ArchiveRootName
    if (-not (Test-Path -LiteralPath $extracted)) {
        # Branch renamed, or GitHub changed the folder name — take whatever single
        # folder the archive actually contained rather than failing outright.
        $extracted = (Get-ChildItem -LiteralPath $extractPath -Directory | Select-Object -First 1).FullName
    }

    Move-Item -LiteralPath $extracted -Destination $TargetFolder

    Write-Host ""
    Write-Host "Workspace ready:" -ForegroundColor Green
    Write-Host "  $TargetFolder"
    Write-Host ""
    Write-Host "Next, run these two lines:"
    Write-Host "  cd `"$TargetFolder`""
    Write-Host "  claude"
    Write-Host "Then type / and check the five skills appear."
}
finally {
    # Never leave a copy of the repo behind in TEMP.
    Remove-Item -LiteralPath $bootstrapTemp -Recurse -Force -ErrorAction SilentlyContinue
}
