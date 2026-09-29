---
name: write-pr-description
description: Drafts a pull request description from the branch's real commits and diff - a short summary, the grouped changes, a test table with one row per case and its real result, and follow-ups - shows it for approval, and only then creates or updates the pull request. Never invents a change or a result, never force-pushes. Use after review-automation-changes.
---

# Write PR Description

Makes the pull request say exactly what changed and what was tested.

## When to use

- After `review-automation-changes` has no open blockers.

## Rules

- **Only what's real.** Every change comes from the diff; every result from an
  actual run.
- **Ask before any push**, and never force-push.
- **Mention stray commits** that don't belong to the change.

## Steps

1. Find the base branch; read `git log` and `git diff` against it (and the
   existing pull request, if there is one).
2. Group the changes (screens, flows, tests, docs, CI).
3. Draft:
   - **Summary:** 2 to 4 bullets on what changed and why.
   - **Changes:** the groups.
   - **Tests:** a table, one row per case ID, with Passed / Partial / Not run
     and the evidence (report link or command).
   - **Follow-ups and blockers.**
4. Show the draft and wait for approval.
5. Ask before pushing; then `gh pr create` (or `gh pr edit`) and return the link.
