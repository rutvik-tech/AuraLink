# Creates a desktop shortcut that points to scripts\start_dev.bat
# Usage: PowerShell -ExecutionPolicy Bypass -File scripts\create_shortcut.ps1
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent
$targetBat = Join-Path $projectRoot "scripts\start_dev.bat"
$desktop = [Environment]::GetFolderPath('Desktop')
$shortcutName = 'AuraLink - Start.lnk'
$shortcutPath = Join-Path $desktop $shortcutName

if (-not (Test-Path $targetBat)) {
    Write-Host "Target batch file not found: $targetBat" -ForegroundColor Red
    exit 1
}

$wsh = New-Object -ComObject WScript.Shell
$sc = $wsh.CreateShortcut($shortcutPath)
$sc.TargetPath = $targetBat
$sc.WorkingDirectory = $projectRoot
# Try to use venv python as icon if available, otherwise default to shell icon
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"
if (Test-Path $venvPython) { $sc.IconLocation = "$venvPython,0" } else { $sc.IconLocation = "$env:WINDIR\system32\shell32.dll,0" }
$sc.Save()
Write-Host "Shortcut created: $shortcutPath" -ForegroundColor Green
