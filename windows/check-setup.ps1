<#
.SYNOPSIS
    Check that a Windows machine is ready for the UnlockAI workshop.

.DESCRIPTION
    Prints one line per check so a helper walking past can see what is wrong in
    a couple of seconds. Read-only: changes nothing, installs nothing, and never
    prints environment variables, tokens or the contents of .env.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File windows\check-setup.ps1
#>
[CmdletBinding()]
param(
    [string] $TargetFolder = (Join-Path $HOME "Downloads\unlockai-social-media")
)

$problems = @()

function Test-Item {
    param(
        [string] $Label,
        [scriptblock] $Check,
        [switch] $Optional
    )
    try { $result = & $Check } catch { $result = $null }
    if ($result) {
        Write-Host ("  [ok]   {0,-26} {1}" -f $Label, $result) -ForegroundColor Green
    } elseif ($Optional) {
        Write-Host ("  [info] {0,-26} not installed (not required)" -f $Label) -ForegroundColor DarkGray
    } else {
        Write-Host ("  [--]   {0,-26} not found" -f $Label) -ForegroundColor Yellow
        $script:problems += $Label
    }
}

Write-Host ""
Write-Host "Machine" -ForegroundColor Cyan
Write-Host ("  Windows           {0}" -f (Get-CimInstance Win32_OperatingSystem).Version)
Write-Host ("  PowerShell        {0} ({1})" -f $PSVersionTable.PSVersion, $PSVersionTable.PSEdition)
Write-Host ("  ExecutionPolicy   {0}" -f (Get-ExecutionPolicy))

Write-Host ""
Write-Host "Tools" -ForegroundColor Cyan
Test-Item "claude"  { (claude --version) 2>$null }
Test-Item "py"      { (py --version) 2>$null }
Test-Item "git" { (git --version) 2>$null } -Optional

# The Microsoft Store stub answers `python` but isn't a real interpreter.
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python -and $python.Source -like "*WindowsApps*") {
    Write-Host "  [!!]   python is the Microsoft Store stub - use 'py' instead" -ForegroundColor Red
    $problems += "python-store-stub"
}

Write-Host ""
Write-Host "Workspace" -ForegroundColor Cyan
if (-not (Test-Path -LiteralPath $TargetFolder)) {
    Write-Host ("  [--]   not downloaded yet: {0}" -f $TargetFolder) -ForegroundColor Yellow
    Write-Host "         run: powershell -ExecutionPolicy Bypass -File windows\get-workspace.ps1"
    $problems += "workspace"
} else {
    Write-Host ("  [ok]   {0}" -f $TargetFolder) -ForegroundColor Green

    foreach ($skill in @("brand", "caption", "ideas", "calendar", "autoreply")) {
        $path = Join-Path $TargetFolder ".claude\skills\$skill\SKILL.md"
        if (Test-Path -LiteralPath $path) {
            Write-Host ("  [ok]   /{0}" -f $skill) -ForegroundColor Green
        } else {
            Write-Host ("  [!!]   /{0} MISSING" -f $skill) -ForegroundColor Red
            $problems += "skill:$skill"
        }
    }

    # Symptom of the old Move-Item -Force bug.
    $nested = Join-Path $TargetFolder "unlockai-social-media-master"
    if (Test-Path -LiteralPath $nested) {
        Write-Host "  [!!]   nested 'unlockai-social-media-master' folder found" -ForegroundColor Red
        Write-Host "         re-run windows\get-workspace.ps1 (it backs up first)"
        $problems += "nested-folder"
    }
}

Write-Host ""
if ($problems.Count -eq 0) {
    Write-Host "All good. cd into the folder and run: claude" -ForegroundColor Green
    exit 0
}
Write-Host ("Needs attention: {0}" -f ($problems -join ", ")) -ForegroundColor Yellow
Write-Host "See windows\README.md or DEBUG.md. Still stuck? Raise your hand."
exit 1
