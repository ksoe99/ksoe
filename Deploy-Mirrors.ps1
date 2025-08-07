# Ensure we're in the right directory
Set-Location -Path "$PSScriptRoot"

# Step 1: Ensure .nojekyll exists
$nojekyllPath = ".\mirrors\.nojekyll"
if (-Not (Test-Path $nojekyllPath)) {
    New-Item -Path $nojekyllPath -ItemType File -Force | Out-Null
    Write-Host "✅ Created .nojekyll file"
}

# Step 2: Commit mirrors folder
git add mirrors
git commit -m "Deploy mirrors with .nojekyll" -m "Fixes GitHub Pages 404 issues" 2>$null

# Step 3: Split subtree and push
$hash = git subtree split --prefix=mirrors main
git push origin "$hash`:refs/heads/gh-pages" --force

Write-Host "`n🚀 Deployment complete. Wait 1 minute, then check your site!"
