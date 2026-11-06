#!/usr/bin/env bash
# One-click script to build release Cicada.app and deploy to /Applications/Cicada.app
set -euo pipefail

cd "$(dirname "$0")/.."

echo "🚀 Building Cicada (Release mode)..."
RELEASE=1 ./scripts/build.sh

echo "🔄 Quitting running Cicada instance..."
osascript -e 'tell application "Cicada" to quit' 2>/dev/null || true
for i in {1..10}; do
    if ! pgrep -x "Cicada" >/dev/null; then
        break
    fi
    sleep 0.3
done
if pgrep -x "Cicada" >/dev/null; then
    pkill -9 -x "Cicada" 2>/dev/null || true
fi

echo "📦 Installing to /Applications/Cicada.app..."
rm -rf /Applications/Cicada.app
cp -R build/Cicada.app /Applications/Cicada.app

echo "✨ Launching updated Cicada.app..."
open /Applications/Cicada.app

echo "🎉 Deployment complete! Cicada is now running with the latest custom changes."
