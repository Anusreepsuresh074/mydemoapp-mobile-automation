---
name: mobile-build-fetch
description: Gets the correct app build (Android APK/AAB or iOS app/IPA) from the place the team really publishes it, verifies it is the build it claims to be, and saves it with its version in the file name. Never hardcodes a distribution token. Use when there is no build yet, or a newer build is needed.
---

# Mobile Build Fetch

Tests are only meaningful against a known build. This skill makes sure the
build under test is the right one and that anyone can tell which one it was.

## When to use

- Before `create-mobile-framework-structure`, if there is no build on disk.
- Whenever a new build must be tested.

## Rules

- **Ask, don't guess, where builds come from.** The source must be the one the
  team treats as official.
- **Version in the name.** Save as `builds/<app>-<version>-<build>.<ext>`, so
  a newer build never silently replaces an older one.
- **No tokens in files.** Credentials for a build service come from
  environment variables or the CI secret store.
- **iOS is different.** Signing means iOS builds usually come from CI or a
  local Xcode build, not a simple download; say so rather than pretend.

## Steps

1. **Confirm the source.** In order of preference: a CI build artifact
   (reproducible), a store testing track, a beta distribution service, or a
   build from source.
2. **Download or build** with that source's own tool.
3. **Verify.** Android: read the package name and version with
   `aapt dump badging`. iOS: read the bundle id and version from `Info.plist`.
4. **Record it.** Add the source, version, build number and date to the app's
   flow document (`docs/<app>-flow.md`).
5. **Hand off** to `create-mobile-framework-structure` (first time) or to the
   test run.

## Output

The build file in `builds/` (git-ignored) and a one-line note in the flow
document.
