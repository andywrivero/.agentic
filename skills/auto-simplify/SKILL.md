---
name: auto-simplify
description: Review and simplify code already changed in the current task when a cleanup pass is requested or clearly useful. Keep behavior and public contracts unchanged; do not perform general refactoring.
---

# Auto Simplify

Owns behavior-preserving cleanup of code in the active change. It does not own language compatibility, member ordering, documentation, or unrelated code review; use the corresponding skill only when that work is requested or needed.

## Scope

- Inspect the diff and limit edits to changed code. Do not sweep legacy code merely because its file is open.
- Look for real clarity improvements: tangled control flow, redundant intermediates, confirmed dead code, or wrappers with no meaningful behavior.
- Extract helpers only when they create a useful responsibility boundary. Line count alone is not a reason to split a method.
- Preserve behavior, public and protected contracts, exception behavior, and project conventions. Keep straightforward loops and abstractions when they communicate intent better.
- For Java, respect the project's language level and place newly extracted helpers according to the member-ordering convention when it applies.

## Workflow

Inspect the changed code, identify worthwhile simplifications, make only those edits, and summarize what changed. Do not add or run tests unless the user asks for testing or verification. If verification is requested, use the narrowest relevant check and report what did and did not run.
