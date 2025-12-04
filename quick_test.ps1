# Quick test script for OCR API (Windows PowerShell)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "OCR API Quick Test" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if server is running
Write-Host "1. Checking server health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    Write-Host "✓ Server is running" -ForegroundColor Green
    $health | ConvertTo-Json -Depth 5
} catch {
    Write-Host "✗ Server is not running!" -ForegroundColor Red
    Write-Host "Please start the server first: python run_server.py --reload" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "2. Checking models status..." -ForegroundColor Yellow
$models = Invoke-RestMethod -Uri "http://localhost:8000/models" -Method Get
$models | ConvertTo-Json -Depth 5

Write-Host ""
Write-Host "3. Testing OCR on first available image..." -ForegroundColor Yellow

# Find first image
$image = Get-ChildItem -Filter "*.jpg" | Select-Object -First 1
if (-not $image) {
    $image = Get-ChildItem -Filter "*.png" | Select-Object -First 1
}

if (-not $image) {
    Write-Host "✗ No images found in current directory" -ForegroundColor Red
    exit 1
}

Write-Host "Using image: $($image.Name)" -ForegroundColor Cyan
Write-Host ""

# Test OCR
try {
    $form = @{
        file = Get-Item $image.FullName
    }
    $result = Invoke-RestMethod -Uri "http://localhost:8000/ocr" -Method Post -Form $form
    
    # Save result
    $result | ConvertTo-Json -Depth 10 | Out-File -FilePath "test_result.json" -Encoding UTF8
    Write-Host "Result saved to: test_result.json" -ForegroundColor Green
    Write-Host ""
    
    # Show summary
    Write-Host "Summary:" -ForegroundColor Cyan
    if ($result.success) {
        Write-Host "✓ Success! Processing time: $($result.processing_time_ms) ms" -ForegroundColor Green
        foreach ($modelName in $result.models.PSObject.Properties.Name) {
            $modelResult = $result.models.$modelName
            if ($modelResult.success) {
                $num = $modelResult.num_detections
                $text = $modelResult.full_text
                if ($text.Length -gt 80) { $text = $text.Substring(0, 80) + "..." }
                Write-Host "  $modelName : $num detections - $text" -ForegroundColor White
            } else {
                Write-Host "  $modelName : Failed" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "✗ Failed: $($result.error)" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "Full result available in: test_result.json" -ForegroundColor Cyan
    Write-Host "View with: Get-Content test_result.json | ConvertFrom-Json | ConvertTo-Json -Depth 10" -ForegroundColor Gray
    
} catch {
    Write-Host "✗ Error: $_" -ForegroundColor Red
}

