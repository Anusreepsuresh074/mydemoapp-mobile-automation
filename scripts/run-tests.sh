#!/usr/bin/env bash
# Starts a local Appium server, checks the environment, runs pytest, then stops Appium.
# Usage: scripts/run-tests.sh [pytest args]   e.g. scripts/run-tests.sh -m smoke
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"
export APPIUM_HOME="$root/.appium"
export ANDROID_HOME="${ANDROID_HOME:-$HOME/Android/Sdk}"
export PATH="$ANDROID_HOME/platform-tools:$PATH"
# Load .env, but values already in the environment win: in CI the secrets arrive as environment
# variables, and the empty placeholders copied from .env.example must not overwrite them.
if [[ -f .env ]]; then
  while IFS='=' read -r key value; do
    [[ $key =~ ^[A-Z_][A-Z0-9_]*$ ]] || continue
    [[ -n "${!key:-}" ]] && continue
    value="${value%\"}"
    value="${value#\"}"
    export "$key=$value"
  done < .env
fi
python="${PYTHON:-$root/.venv/bin/python}"
[[ -x "$python" ]] || python=python3

mkdir -p reports
# Run Appium's own binary, not through npx: then $! is the server itself and the trap stops it.
node_modules/.bin/appium --address "${APPIUM_HOST:-127.0.0.1}" --port "${APPIUM_PORT:-4723}" \
  --log reports/appium.log --log-level warn &
appium_pid=$!
trap 'kill "$appium_pid" 2>/dev/null || true; wait "$appium_pid" 2>/dev/null || true' EXIT

for _ in $(seq 1 60); do
  curl -sf "http://${APPIUM_HOST:-127.0.0.1}:${APPIUM_PORT:-4723}/status" >/dev/null && break
  sleep 1
done

scripts/env-check.sh
# Same as CI (disable-animations): no system animations, so screens settle at once.
for setting in window_animation_scale transition_animation_scale animator_duration_scale; do
  adb -s "${DEVICE_NAME:-emulator-5554}" shell settings put global "$setting" 0
done
# The CI emulator action leaves stdout non-blocking, so a long failure message ended pytest with a
# BlockingIOError and lost the summary. Make the output blocking again first.
"$python" -c 'import os; os.set_blocking(1, True); os.set_blocking(2, True)'
"$python" -m pytest "$@"
