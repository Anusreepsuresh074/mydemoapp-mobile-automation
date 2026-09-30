#!/usr/bin/env bash
# mobile-env-check: is the machine, the device and the Appium server healthy enough to trust a run?
# Prints one line per check: HEALTHY / DEGRADED / BROKEN. Exit 1 if anything is BROKEN.
set -uo pipefail

host="${APPIUM_HOST:-127.0.0.1}"
port="${APPIUM_PORT:-4723}"
min_mb="${MIN_AVAILABLE_MEMORY_MB:-2048}"
broken=0

say() { printf '%-9s %-22s %s\n' "$1" "$2" "$3"; [[ "$1" == BROKEN ]] && broken=1; }

available=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
if (( available >= min_mb )); then say HEALTHY memory "${available} MB available"; else say BROKEN memory "${available} MB available, need ${min_mb} MB"; fi

load=$(cut -d' ' -f1 /proc/loadavg); cores=$(nproc)
if awk -v l="$load" -v c="$cores" 'BEGIN{exit !(l < c)}'; then say HEALTHY cpu "load $load on $cores cores"; else say DEGRADED cpu "load $load on $cores cores"; fi

if curl -sf "http://$host:$port/status" >/dev/null; then say HEALTHY appium "server ready on $host:$port"; else say BROKEN appium "no answer on http://$host:$port/status"; fi

if ! command -v adb >/dev/null; then
  say BROKEN adb "adb not on PATH (install Android platform-tools)"
else
  device="${DEVICE_NAME:-}"
  if [[ -z "$device" ]]; then
    device=$(adb devices | awk 'NR>1 && $2=="device" {print $1; exit}')
  elif ! adb devices | awk -v d="$device" 'NR>1 && $1==d && $2=="device" {found=1} END {exit !found}'; then
    device=""
  fi
  if [[ -z "$device" ]]; then
    say BROKEN device "${DEVICE_NAME:-no device} is not online"
  else
    booted=$(adb -s "$device" shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')
    adb -s "$device" shell input keyevent KEYCODE_HOME >/dev/null 2>&1
    focus=$(adb -s "$device" shell dumpsys window 2>/dev/null | grep -m1 -E "mCurrentFocus" | tr -d '\r')
    # A fresh CI emulator often shows a system "not responding" dialog while it settles after boot.
    # Close system dialogs and look again for up to a minute; only a dialog that stays is BROKEN.
    dismissed=0
    for _ in 1 2 3 4 5 6; do
      grep -qi "not responding" <<<"$focus" || break
      dismissed=1
      adb -s "$device" shell am broadcast -a android.intent.action.CLOSE_SYSTEM_DIALOGS >/dev/null 2>&1
      sleep 10
      focus=$(adb -s "$device" shell dumpsys window 2>/dev/null | grep -m1 -E "mCurrentFocus" | tr -d '\r')
    done
    if [[ "$booted" == 1 && -n "$focus" ]]; then
      if grep -qi "not responding" <<<"$focus"; then
        say BROKEN device "$device shows a 'not responding' dialog that does not go away"
      elif (( dismissed )); then
        say DEGRADED device "$device booted; a 'not responding' dialog was closed while it settled"
      else
        say HEALTHY device "$device booted and responsive"
      fi
    else
      say BROKEN device "$device online but not responsive (boot_completed=$booted)"
    fi
  fi
fi

exit "$broken"
