# VidMind Environment Setup Script for Windows PowerShell
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "       VidMind Environment Setup          " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Check Conda
$condaCmd = Get-Command "conda" -ErrorAction SilentlyContinue
if (-not $condaCmd) {
    $condaPath = "C:\Users\User\anaconda3\Scripts\conda.exe"
    if (Test-Path $condaPath) {
        $condaCmd = $condaPath
    } else {
        Write-Host "[!] Conda not found in PATH or standard location." -ForegroundColor Yellow
        Write-Host "    Falling back to standard Python virtual environment..." -ForegroundColor Yellow
    }
}

if ($condaCmd) {
    Write-Host "[+] Found Conda: $condaCmd" -ForegroundColor Green
    Write-Host "[*] Creating/updating 'vidmind' conda environment..." -ForegroundColor White
    & $condaCmd env create -f "environment.yml" --force
    Write-Host "[+] Conda environment 'vidmind' created. Activate with: conda activate vidmind" -ForegroundColor Green
} else {
    Write-Host "[*] Creating Python venv in .venv..." -ForegroundColor White
    python -m venv .venv
    .\.venv\Scripts\python.exe -m pip install --upgrade pip
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    Write-Host "[+] Virtual environment created. Activate with: .\.venv\Scripts\Activate.ps1" -ForegroundColor Green
}

# 2. Frontend Dependencies
Write-Host "`n[*] Installing Frontend Dependencies..." -ForegroundColor White
if (Test-Path "frontend/package.json") {
    Push-Location frontend
    npm install
    Pop-Location
    Write-Host "[+] Frontend dependencies installed." -ForegroundColor Green
} else {
    Write-Host "[*] Frontend directory not yet initialized." -ForegroundColor Yellow
}

Write-Host "`n[+] Setup complete!" -ForegroundColor Cyan
