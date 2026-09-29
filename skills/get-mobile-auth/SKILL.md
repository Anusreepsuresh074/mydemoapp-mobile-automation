---
name: get-mobile-auth
description: Chooses and documents how the tests sign in, one strategy per sign-in method the app offers (email and password, phone and one-time code, Google or other single sign-on), wires the settings as environment variables, and never commits a credential. Use after the app is set up and before the first test that needs a signed-in user.
---

# Get Mobile Auth

Most mobile flows start behind a sign-in screen. This skill decides, once and
on purpose, how the tests get past it.

## When to use

- After `create-mobile-framework-structure`, before automation.
- When the app adds a new sign-in method.

## Rules

- **Test accounts only.** Never a production or personal account.
- **No secrets in the repo.** Values live in `.env` (git-ignored) or the CI
  secret store; `.env.example` lists the names with empty values.
- **Don't automate someone else's sign-in page.** Third-party consent screens
  (Google, Apple) are fragile, trigger bot protection and may break the
  provider's terms. Prefer an account already signed in on the test device.
- **Fail fast.** A test that needs a variable that isn't set stops with a
  clear message, instead of failing halfway through a flow.

## Steps

1. **List every sign-in method** the app offers.
2. **Pick a strategy per method**:

| Method | Preferred strategy | Fallback |
| --- | --- | --- |
| Email + password | A dedicated test account | None needed |
| Phone + one-time code | A fixed code on a test environment | Reuse a signed-in session; manual (never in CI) |
| Single sign-on | Account pre-signed in on the device | Manual, skipped in CI |

3. **Wire it**: variable names in `.env.example`, a fixture that reads them.
4. **Document** each method's strategy, the reason, and CI limits in the
   flow document's "Sign-in and data" section.
5. **Note iOS differences**: keychain state survives some reinstalls; Face ID
   or Touch ID prompts need explicit handling on simulators.
6. **Hand off** to `mobile-test-data` or `mobile-test-design`.
