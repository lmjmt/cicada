#!/usr/bin/env bash
# One-click script to fetch latest upstream updates and merge into custom-main
set -euo pipefail

cd "$(dirname "$0")/.."

echo "📥 Fetching latest commits from upstream (wquguru/cicada)..."
git fetch upstream main

echo "🔄 Updating local main..."
git checkout main
git merge --ff-only upstream/main
git push origin main

echo "🔀 Merging upstream changes into custom-main..."
git checkout custom-main
git merge main -m "chore: merge upstream main into custom-main"
git push origin custom-main

echo "🎉 Upstream sync complete! To test and deploy locally, simply run: ./scripts/deploy.sh"
