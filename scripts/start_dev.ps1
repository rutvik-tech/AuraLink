# Script to start development server and open browser
# Usage: powershell -ExecutionPolicy Bypass -File scripts\start_dev.ps1
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root\..  # go to project root (auralink)

# Ensure venv exists (check project and workspace root)
$localVenv = Join-Path $PWD ".venv\Scripts\python.exe"
$parentVenv = Join-Path (Join-Path $PWD "..") ".venv\Scripts\python.exe"
if (Test-Path $localVenv) {
  $venv = $localVenv
} elseif (Test-Path $parentVenv) {
  $venv = $parentVenv
} else {
  Write-Host "Virtualenv python not found (checked ./ .venv and ../ .venv). Please create a virtualenv and install requirements." -ForegroundColor Yellow
  exit 1
}

Write-Host "Running migrations, collecting static files, and seeding database..."
& $venv manage.py migrate --noinput
& $venv manage.py collectstatic --noinput
try {
  & $venv manage.py seed
} catch {
  Write-Host "Seed may have partially failed or already run: $_" -ForegroundColor Yellow
}

# Check if port 8000 is in use and warn
$portInUse = (Get-NetTCPConnection -State Listen -LocalPort 8000 -ErrorAction SilentlyContinue)
if ($portInUse) {
  Write-Host "Port 8000 is already in use. The server cannot be started." -ForegroundColor Red
  exit 1
}

Write-Host "Starting development server in a new window..."
# Start server in a new PowerShell window so logs are visible
$psCommand = "& '$venv' manage.py runserver 127.0.0.1:8000"
Start-Process -FilePath powershell -ArgumentList ('-NoExit','-Command', $psCommand) -WorkingDirectory $PWD

# Wait a moment then open browser
Start-Sleep -Seconds 2
try {
  Start-Process "http://127.0.0.1:8000"
  Write-Host "Opened http://127.0.0.1:8000 in default browser"
} catch {
  Write-Host "Could not open browser automatically. Please open http://127.0.0.1:8000 manually." -ForegroundColor Yellow
}

Write-Host "Done. Close the server window to stop the dev server." -ForegroundColor Green