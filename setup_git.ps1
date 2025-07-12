# OLX Car Scraper - Git Setup Script
Write-Host "Setting up Git repository for OLX Car Scraper..." -ForegroundColor Green

# Check if Git is available
try {
    git --version
    Write-Host "Git is available" -ForegroundColor Green
} catch {
    Write-Host "Git is not available. Please restart PowerShell after installing Git." -ForegroundColor Red
    exit 1
}

# Initialize git repository
Write-Host "Initializing Git repository..." -ForegroundColor Yellow
git init

# Add all files
Write-Host "Adding files to Git..." -ForegroundColor Yellow
git add .

# Make initial commit
Write-Host "Making initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: OLX Car Scraper with Selenium and SQLAlchemy"

# Add remote repository
Write-Host "Adding remote repository..." -ForegroundColor Yellow
git remote add origin git@github.com:JGSalgueiro/olx-car-scrapper.git

# Set main branch and push
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

Write-Host "Setup complete! Your repository is now on GitHub." -ForegroundColor Green
Write-Host "Repository URL: https://github.com/JGSalgueiro/olx-car-scrapper" -ForegroundColor Cyan 