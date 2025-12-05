# KVGroove Release Script
# Creates a release build, zips it, commits, and pushes to GitHub

param(
    [string]$Version
)

# Get version from user if not provided
if (-not $Version) {
    $Version = Read-Host "Enter version number (e.g., 0.0.1)"
}

# Validate version format
if ($Version -notmatch '^\d+\.\d+\.\d+$') {
    Write-Host "Error: Invalid version format. Use format like 0.0.1" -ForegroundColor Red
    exit 1
}

$ProjectRoot = $PSScriptRoot
$DistFolder = Join-Path $ProjectRoot "dist"
$ReleasesFolder = Join-Path $ProjectRoot "releases"
$ReleaseName = "KVGroove-v$Version-win64"
$ZipName = "$ReleaseName.zip"
$ZipPath = Join-Path $ReleasesFolder $ZipName

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  KVGroove Release Builder v$Version" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Activate venv and build with PyInstaller
Write-Host "[1/6] Building executable with PyInstaller..." -ForegroundColor Yellow
& "$ProjectRoot\venv\Scripts\python.exe" -m PyInstaller --onefile --windowed "$ProjectRoot\kvgroove.py" --distpath "$DistFolder" --workpath "$ProjectRoot\build" --specpath "$ProjectRoot" -y
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: PyInstaller build failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Build complete!" -ForegroundColor Green

# Step 2: Create releases folder if it doesn't exist
Write-Host "[2/6] Preparing releases folder..." -ForegroundColor Yellow
if (-not (Test-Path $ReleasesFolder)) {
    New-Item -ItemType Directory -Path $ReleasesFolder | Out-Null
    Write-Host "Created releases folder" -ForegroundColor Green
}

# Step 3: Create zip file
Write-Host "[3/6] Creating zip archive..." -ForegroundColor Yellow
if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}
Compress-Archive -Path "$DistFolder\kvgroove.exe" -DestinationPath $ZipPath -CompressionLevel Optimal
Write-Host "Created: $ZipName" -ForegroundColor Green

# Get file size
$ExeSize = [math]::Round((Get-Item "$DistFolder\kvgroove.exe").Length / 1MB, 2)
$ZipSize = [math]::Round((Get-Item $ZipPath).Length / 1MB, 2)
Write-Host "  Executable: $ExeSize MB" -ForegroundColor Gray
Write-Host "  Zip archive: $ZipSize MB" -ForegroundColor Gray

# Step 4: Stage changes
Write-Host "[4/6] Staging changes for git..." -ForegroundColor Yellow
git add releases/$ZipName
git add -A  # Stage any other pending changes
Write-Host "Staged all changes" -ForegroundColor Green

# Step 5: Commit with version message
Write-Host "[5/6] Committing release..." -ForegroundColor Yellow
$CommitMessage = "Release v$Version"
git commit -m $CommitMessage
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Nothing to commit or commit failed" -ForegroundColor Yellow
}

# Step 6: Push to remote
Write-Host "[6/6] Pushing to GitHub..." -ForegroundColor Yellow
git push origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Push failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Pushed to GitHub!" -ForegroundColor Green

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Release v$Version Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nRelease file: $ZipPath" -ForegroundColor White
Write-Host "Zip size: $ZipSize MB" -ForegroundColor White
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "  1. Go to: https://github.com/gerp93/KVGroove/releases/new" -ForegroundColor White
Write-Host "  2. Tag version: v$Version" -ForegroundColor White
Write-Host "  3. Title: KVGroove v$Version" -ForegroundColor White
Write-Host "  4. Upload: $ZipName" -ForegroundColor White
Write-Host "  5. Publish release!" -ForegroundColor White
Write-Host ""
