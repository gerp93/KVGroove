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

# Script is in releases/, so project root is one level up
$ScriptDir = $PSScriptRoot
$ProjectRoot = Split-Path $ScriptDir -Parent
$DistFolder = Join-Path $ProjectRoot "dist"
$ReleasesFolder = $ScriptDir  # Script is already in releases folder
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

# Step 2: Create zip file
Write-Host "[2/6] Creating zip archive..." -ForegroundColor Yellow
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

# Step 3: Stage changes
Write-Host "[3/6] Staging changes for git..." -ForegroundColor Yellow
git add releases/$ZipName
git add -A  # Stage any other pending changes
Write-Host "Staged all changes" -ForegroundColor Green

# Step 4: Commit with version message
Write-Host "[4/6] Committing release..." -ForegroundColor Yellow
$CommitMessage = "Release v$Version"
git commit -m $CommitMessage
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Nothing to commit or commit failed" -ForegroundColor Yellow
}

# Step 5: Push to remote
Write-Host "[5/6] Pushing to GitHub..." -ForegroundColor Yellow
git push origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Push failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Pushed to GitHub!" -ForegroundColor Green

# Step 6: Create and push git tag
Write-Host "[6/6] Creating release tag v$Version..." -ForegroundColor Yellow
git tag -a "v$Version" -m "Release v$Version"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Tag may already exist" -ForegroundColor Yellow
}
git push origin "v$Version"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Tag push failed (may already exist on remote)" -ForegroundColor Yellow
} else {
    Write-Host "Tag v$Version created and pushed!" -ForegroundColor Green
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Release v$Version Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nRelease file: $ZipPath" -ForegroundColor White
Write-Host "Zip size: $ZipSize MB" -ForegroundColor White

Write-Host "`n----------------------------------------" -ForegroundColor DarkGray
Write-Host "  HOW TO PUBLISH ON GITHUB RELEASES" -ForegroundColor Magenta
Write-Host "----------------------------------------" -ForegroundColor DarkGray

Write-Host "`n Step 1: Open the GitHub Releases page" -ForegroundColor Yellow
Write-Host "   https://github.com/gerp93/KVGroove/releases/new" -ForegroundColor Cyan

Write-Host "`n Step 2: The tag is already created!" -ForegroundColor Yellow
Write-Host "   - Tag v$Version was pushed automatically" -ForegroundColor Green
Write-Host "   - Select it from the 'Choose a tag' dropdown" -ForegroundColor White

Write-Host "`n Step 3: Fill in release details" -ForegroundColor Yellow
Write-Host "   - Release title: KVGroove v$Version" -ForegroundColor Green
Write-Host "   - Description: Add release notes (new features, bug fixes, etc.)" -ForegroundColor White

Write-Host "`n Step 4: Attach the release file" -ForegroundColor Yellow
Write-Host "   - Drag and drop or click 'Attach binaries'" -ForegroundColor White
Write-Host "   - Upload: $ZipPath" -ForegroundColor Green

Write-Host "`n Step 5: Publish" -ForegroundColor Yellow
Write-Host "   - Click the green 'Publish release' button" -ForegroundColor White

Write-Host "`n----------------------------------------" -ForegroundColor DarkGray
Write-Host "  SAMPLE RELEASE NOTES" -ForegroundColor Magenta
Write-Host "----------------------------------------" -ForegroundColor DarkGray
Write-Host @"

## What's New in v$Version

### Features
- Feature 1
- Feature 2

### Bug Fixes
- Fix 1
- Fix 2

### Download
- **Windows:** Download ``KVGroove-v$Version-win64.zip``, extract, and run ``kvgroove.exe``

"@ -ForegroundColor Gray

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Done! Your release is ready to publish." -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
