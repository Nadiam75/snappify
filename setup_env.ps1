# PowerShell script to set up virtual environment and install requirements
Write-Host "Creating virtual environment..." -ForegroundColor Green
python -m venv venv

Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

Write-Host "Upgrading pip..." -ForegroundColor Green
python -m pip install --upgrade pip

Write-Host "Installing requirements..." -ForegroundColor Green
pip install numpy pillow opencv-python
pip install pycocotools
pip install -r requirements.txt --no-deps Polygon3 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Note: Polygon3 skipped (requires Visual C++ Build Tools)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Virtual environment setup complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the environment, run:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "Note: Polygon3 was skipped as it requires Microsoft Visual C++ Build Tools." -ForegroundColor Yellow
Write-Host "If you need it, install from: https://visualstudio.microsoft.com/visual-cpp-build-tools/" -ForegroundColor Yellow

