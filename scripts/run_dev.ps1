# VidMind Unified Development Runner for Windows
param (
    [switch]$BackendOnly,
    [switch]$FrontendOnly
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "         Starting VidMind Dev Stack        " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$root = Split-Path -Parent $PSScriptRoot

# Locate Python environment
$pythonExe = "python"
if (Test-Path "$env:USERPROFILE\anaconda3\envs\vidmind\python.exe") {
    $pythonExe = "$env:USERPROFILE\anaconda3\envs\vidmind\python.exe"
} elseif (Test-Path "$root\.venv\Scripts\python.exe") {
    $pythonExe = "$root\.venv\Scripts\python.exe"
}

Write-Host "[*] Using Python: $pythonExe" -ForegroundColor Green

# Initialize DB if needed
Write-Host "[*] Initializing Database..." -ForegroundColor White
& $pythonExe "$root\scripts\init_database.py"

if (-not $FrontendOnly) {
    Write-Host "[*] Launching Backend on http://localhost:8000 ..." -ForegroundColor Cyan
    $backendJob = Start-Process -FilePath $pythonExe -ArgumentList "-m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload" -WorkingDirectory $root -PassThru
    Write-Host "[+] Backend started with PID: $($backendJob.Id)" -ForegroundColor Green
}

if (-not $BackendOnly) {
    Write-Host "[*] Launching Frontend on http://localhost:5173 ..." -ForegroundColor Cyan
    Push-Location "$root\frontend"
    $frontendJob = Start-Process -FilePath "npm.cmd" -ArgumentList "run dev" -PassThru
    Pop-Location
    Write-Host "[+] Frontend started with PID: $($frontendJob.Id)" -ForegroundColor Green
}

Write-Host "`n[+] Dev stack running. Press Ctrl+C in terminals to stop." -ForegroundColor Cyan
