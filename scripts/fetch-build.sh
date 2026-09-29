#!/usr/bin/env bash
# mobile-build-fetch: download the pinned My Demo App release and verify its package name.
# Usage: scripts/fetch-build.sh [version] [build]   (defaults: 2.3.0 27)
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
version="${1:-2.3.0}"
build="${2:-27}"
target="$root/builds/mydemoapp-$version-$build.apk"
mkdir -p "$root/builds"

if [[ ! -f "$target" ]]; then
  gh release download "$version" -R saucelabs/my-demo-app-android \
    -p "mda-$version-$build.apk" -O "$target"
fi

aapt="$(find "${ANDROID_HOME:-$HOME/Android/Sdk}/build-tools" -name aapt -type f 2>/dev/null | sort | tail -1 || true)"
if [[ -n "$aapt" ]]; then
  "$aapt" dump badging "$target" | grep -E "^package:|launchable-activity" | cut -c1-160
fi
echo "BUILD=$target"
