# Auto-Simplify Prompts

Use these prompts with the existing `auto-simplify` skill. For Java changes, also follow the applicable `java8-pro` and `java-member-ordering` skills.

## 1. Simplify the Current Changes

Run a strict non-behavioral simplification pass over the code changed in the current working diff.

- Apply the `auto-simplify` skill and keep the pass within the diff scope.
- Run the project's relevant tests before editing and confirm they pass. If they fail, stop and report the baseline failure without refactoring.
- Simplify only where it improves clarity or removes real complexity. Preserve behavior, public APIs, business logic, and project conventions.
- After the edits, immediately rerun the same tests and the relevant build check. If a regression appears, repair or revert only this simplification pass.
- Finish with the skill's concise, bulleted change summary and verification results.

## 2. Reduce Complexity and Clarify Responsibilities

Simplify **[identify the changed class, method, or file]**, focusing on control flow and responsibility boundaries.

- Apply the `auto-simplify` skill. Run relevant tests first; do not proceed if the baseline is failing.
- Look for deep nesting that can become guard clauses, tangled conditionals that need clear predicates, and methods combining distinct responsibilities.
- Extract helpers only when they create a meaningful single-purpose boundary; do not split flat, straightforward code just to meet a line-count target.
- Keep new behavior and public contracts unchanged. For Java, place extracted private helpers according to `java-member-ordering` and retain the project's Java language level.
- Rerun the baseline tests and relevant build check immediately after the refactor, then summarize the edits and results.

## 3. Remove Dead Code and Flatten Unneeded Abstractions

Clean up **[identify the changed files or code path]**, focusing only on redundant or unused code introduced or touched within this scope.

- Apply the `auto-simplify` skill and run relevant tests before editing. Stop if the baseline fails.
- Remove confirmed unused imports, locals, parameters, unreachable code, and commented-out code. Inline single-use intermediates only when that makes the expression easier to read.
- Remove wrappers or abstractions only when they add no validation, transformation, or domain meaning. Do not pursue unrelated optimizations or reformat untouched legacy code.
- Preserve behavior, signatures, and contracts; honor applicable language and member-ordering constraints.
- Rerun the same tests and relevant build check immediately after the cleanup. Report the concise changes and verification results.
