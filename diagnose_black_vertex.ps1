Write-Host "=== BLACK VERTEX DIAGNOSTIC START ===" -ForegroundColor Cyan

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Python is not installed or not in PATH." -ForegroundColor Red
    exit
} else {
    $pyVer = python --version
    Write-Host "[OK] Python found: $pyVer" -ForegroundColor Green
}

# Check script presence
$scriptPath = "black_vertex.py"
if (-not (Test-Path $scriptPath)) {
    Write-Host "[ERROR] black_vertex.py not found." -ForegroundColor Red
    exit
} else {
    Write-Host "[OK] Script exists: $scriptPath" -ForegroundColor Green
}

# Check input URLs file
if (-not (Test-Path "urls.txt")) {
    Write-Host "[ERROR] urls.txt not found." -ForegroundColor Red
} else {
    $urlCount = (Get-Content "urls.txt" | Where-Object { $_ -ne "" }).Count
    Write-Host "[OK] urls.txt found with $urlCount URLs." -ForegroundColor Green
}

# Check dependencies
$deps = @("requests", "beautifulsoup4")
foreach ($pkg in $deps) {
    $installed = python -m pip show $pkg 2>$null
    if ($installed) {
        Write-Host "[OK] $pkg is installed." -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Missing Python package: $pkg" -ForegroundColor Red
    }
}

# Check output folder
if (-not (Test-Path "mirrors")) {
    Write-Host "[WARN] Output folder 'mirrors' does not exist yet." -ForegroundColor Yellow
} else {
    $htmlFiles = Get-ChildItem -Recurse -Filter "index.html" -Path "mirrors"
    Write-Host "[OK] Found $($htmlFiles.Count) mirrored pages in mirrors/." -ForegroundColor Green
}

# Check environment variables
$indexNow = $env:INDEXNOW_KEY
$googleToken = $env:GOOGLE_INDEX_TOKEN
if ($indexNow) {
    Write-Host "[OK] INDEXNOW_KEY is set." -ForegroundColor Green
} else {
    Write-Host "[WARN] INDEXNOW_KEY not set." -ForegroundColor Yellow
}
if ($googleToken) {
    Write-Host "[OK] GOOGLE_INDEX_TOKEN is set." -ForegroundColor Green
} else {
    Write-Host "[WARN] GOOGLE_INDEX_TOKEN not set." -ForegroundColor Yellow
}

Write-Host "=== DIAGNOSTIC COMPLETE ===" -ForegroundColor Cyan
