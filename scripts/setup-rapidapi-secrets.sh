#!/bin/bash
# Setup script for GitHub secrets required by CI/CD workflow
# Run this after creating your RapidAPI account

echo "🔐 Setting up GitHub Secrets for RapidAPI CI/CD"
echo "================================================"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed"
    echo "Please install it first: https://cli.github.com/"
    exit 1
fi

# Check if user is logged in
if ! gh auth status &> /dev/null; then
    echo "❌ You are not logged into GitHub CLI"
    echo "Please run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is ready"
echo ""

# Get repository name
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "")
if [ -z "$REPO" ]; then
    echo "⚠️ Could not detect repository"
    read -p "Enter your repository (format: owner/repo): " REPO
fi

echo "📝 Repository: $REPO"
echo ""

# Get RapidAPI Key
echo "🔑 Step 1: RapidAPI Key"
echo "   Get this from: https://rapidapi.com/developer/dashboard"
echo "   Click on 'Authorization' or 'Apps' to find your key"
read -s -p "   Enter RapidAPI Key: " RAPIDAPI_KEY
echo ""

# Get API ID (user provided)
echo ""
echo "🔑 Step 2: RapidAPI API ID"
echo "   Your API ID: api_7bd483b9-3862-4fab-97b7-7c1e0f58e408"
read -p "   Press Enter to use the provided ID, or type a different one: " API_ID
API_ID=${API_ID:-api_7bd483b9-3862-4fab-97b7-7c1e0f58e408}

# Get Version ID (user provided)
echo ""
echo "🔑 Step 3: RapidAPI Version ID"
echo "   Your Version ID: apiversion_2ba128c1-0903-43a6-84d4-f81d1477164c"
read -p "   Press Enter to use the provided ID, or type a different one: " VERSION_ID
VERSION_ID=${VERSION_ID:-apiversion_2ba128c1-0903-43a6-84d4-f81d1477164c}

echo ""
echo "🚀 Setting up secrets..."
echo ""

# Set secrets
echo "Setting RAPIDAPI_KEY..."
echo "$RAPIDAPI_KEY" | gh secret set RAPIDAPI_KEY -R "$REPO"

echo "Setting RAPIDAPI_API_ID..."
echo "$API_ID" | gh secret set RAPIDAPI_API_ID -R "$REPO"

echo "Setting RAPIDAPI_VERSION_ID..."
echo "$VERSION_ID" | gh secret set RAPIDAPI_VERSION_ID -R "$REPO"

echo ""
echo "✅ All secrets set successfully!"
echo ""
echo "🔍 Verifying secrets..."
echo ""

# List secrets
echo "Secrets configured for $REPO:"
gh secret list -R "$REPO" | grep -E "RAPIDAPI"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Push changes to main.py to trigger the workflow"
echo "2. Or manually trigger from GitHub Actions tab"
echo "3. Check the Actions tab to see workflow runs"
echo ""
