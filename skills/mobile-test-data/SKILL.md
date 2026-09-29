---
name: mobile-test-data
description: Decides how each piece of data a feature's tests depend on (an account with an order, a cart with items, a saved address) is created and cleaned up, records the choice in the flow document, and never relies on data another test left behind. Use when a feature needs backend state before the UI can be tested.
---

# Mobile Test Data

A UI test is only repeatable if its starting data is. This skill plans that
data before tests are written.

## When to use

- When `get-mobile-context` lists data the tests need.
- When a test is flaky because "it depends what's already there".

## Rules

- **Own your data.** A test never depends on records another test created.
- **Bounded growth.** If data accumulates, either clean it up or write down an
  accepted limit and who resets it.
- **Real shapes only.** Before seeding through an API, compare with a real
  record; never invent a schema.
- **Automated cleanup or it isn't a plan.**

## Strategies

| Strategy | Use when | Cleanup |
| --- | --- | --- |
| Isolated data per test (default) | Data is cheap to create | Deleted by the test's fixture |
| Shared parent, unique child per test | The parent is expensive (an account) but children are cheap (orders) | Children deleted per test |
| Shared read-only data | Tests only read it (a product catalogue) | None; never modified |
| Seeded through an API | The UI path to create it is slow | Deleted through the same API |
| Built into the app | Demo or offline apps ship their own data | Reset by clearing app data |

## Steps

1. **List** each precondition from the context document.
2. **Reuse** an existing documented fixture if one fits.
3. **Choose** a strategy per precondition (table above).
4. **Document** it in the flow document: precondition, strategy, owner of cleanup.
5. **Hand off** to `mobile-test-design`.
