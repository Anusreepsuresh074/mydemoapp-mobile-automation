---
name: mobile-coverage-audit
description: A read-only report of gaps between an app's flow document, its feature context documents and its approved test cases - flows marked Done with no test file, categories with no case, screens and rules that no case mentions. Reports gaps; never fills them. Use before a release or whenever coverage is in doubt.
---

# Mobile Coverage Audit

Answers "of everything we know about this app, what isn't tested?"

## When to use

- Before a release, or after several features were added.
- When a flow document and the tests may have drifted apart.

## Rules

- **Stop if an input is missing** (flow document, context documents, test cases).
- **Report, never fix.** Adding cases is `mobile-test-design`'s job.
- **Same vocabulary** as `mobile-test-design`: the eight categories, P0 / P1 / P2.
- **Honest matching.** Matching rules and screens to cases is text-based, so
  results say "likely covered" or "not found", never a bare "covered".
- **Only flag what applies.** A read-only screen doesn't need input-validation cases.

## Checks

1. **Status drift:** every flow marked Done has a test file on disk.
2. **Categories:** for each feature, which of the eight categories have cases.
3. **Screens:** each screen in the context documents appears in at least one case.
4. **Rules:** each business rule is referenced by at least one case.
5. **Priorities:** every P0 journey has an automated test.

## Output

`docs/context/<app>-coverage-audit.md`: a summary with percentages, then one
table per check, then open questions.
