---
name: mobile-test-design
description: Turns a feature's context document into a prioritised, automation-ready list of test cases (P0 / P1 / P2) across eight categories, each with observable expected results, then stops for human approval before any test is written. Use after get-mobile-context (and auth and data planning) for every feature.
---

# Mobile Test Design

Decides exactly which cases will be automated, and gets that decision approved.

## When to use

- After the context, sign-in and data plans exist for a feature.
- Again when the feature or its rules change.

## Readiness check (stop if any is missing)

The goal of the feature, its main journey, the starting state, the sign-in
strategy, and at least one visible result per journey. No case may need a
secret that isn't in `.env`.

## Rules

- **Observable results only.** "The cart badge shows 1" is testable; "it
  worked" is not.
- **No invented behaviour.** Every case traces to a rule or screen in the
  context document.
- **Blockers are named.** A case that can't be automated yet says why.
- **Stop for approval.** Nothing is automated until a person approves the list.

## Priorities

- **P0:** a failure blocks a release (sign-in, checkout, core journeys).
- **P1:** important but has a workaround.
- **P2:** minor or cosmetic.

## Categories to cover

Happy path · input validation · error handling · edge cases · recovery and
retry · sign-in and session · app state (background, resume, rotate, kill) ·
regression risk.

## Case template

| Field | Example |
| --- | --- |
| ID | `CART-P0-01` |
| Priority | P0 |
| Scenario | Adding a product puts it in the cart |
| Preconditions | Fresh install, catalogue visible |
| Steps | Open a product, tap "Add to cart" |
| Expected | Cart badge shows 1; the cart lists the product with its price |
| Automation notes | Needs a stable id on the cart badge |

## Output

`docs/context/<app>-<feature>-testcases.md`, ending with an approval line
(who approved, when). Hand off to `mobile-test-automation`.
