$mirrorRoot = "$env:USERPROFILE\Desktop\BlackVertex\mirrors"
$statusFile = "$env:USERPROFILE\Desktop\BlackVertex\index_status.json"

if (-Not (Test-Path $statusFile)) {
    Write-Host "❌ index_status.json not found. Run searchverify.py first." -ForegroundColor Red
    exit
}

$data = Get-Content $statusFile | ConvertFrom-Json

$deleted = 0
foreach ($url in $data.PSObject.Properties.Name) {
    if ($data[$url] -eq $true) {
        $slug = ($url -split "/")[-2]
        $folder = Join-Path $mirrorRoot $slug
        if (Test-Path $folder) {
            Remove-Item -Recurse -Force $folder
            Write-Host "🗑 Deleted: $slug"
            $deleted++
        }
    }
}

Write-Host "`n✅ Cleanup complete. Deleted $deleted verified mirror folders."
pause
