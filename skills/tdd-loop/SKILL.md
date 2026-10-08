---
name: tdd-loop
description: Drive a code change through strict red-green-refactor cycles. Write one failing test, run it with the project's command-line test runner and confirm it fails for the expected reason, write the minimum code to pass, then refactor with the tests green. Use when the user asks for TDD or test-first work, when the project's AGENTS.md or CLAUDE.md requires it, or to fix a bug whose cause is known (from `systematic-debugging`) by first reproducing it in a test. Not for diagnosing failures or adding tests to existing code after the fact.
---

# TDD Loop

Owns the test-first cycle: the test list, the order of steps, running the tests, and what counts as red and green. It does not own finding a bug's cause (`systematic-debugging`), spec and design analysis (`spec-architecture-verification`), test design and edge-case selection (`test-backfill`), what a refactor may change (`auto-simplify`), formatting of test or production code (`java-code-style`), Java 8 compatibility of test dependencies (`java8-pro`), or commits (`atomic-ordered-git-commits`).

The test runs in this loop are required while it is active, even when another skill's `verify` setting is `on-request`.

## Settings

Resolve each setting from, highest first: the current request; a `tdd-loop` entry under `Skill settings` in the project's AGENTS.md or CLAUDE.md; the project's build and test configuration; the defaults below.

- `run-scope`: `widening` — run only the new test for red, the test class for green and after each refactor, and the module's full suite before finishing. Or `full` (the full suite at every step).
- `commit`: `none` — leave committing to the user. Or `per-cycle` (commit each finished cycle, test and code together, with `atomic-ordered-git-commits`).
- `confirm-list`: `when-ambiguous` — start cycling unless the test list depends on open questions. Or `always` (wait for approval of the test list).

## 0. Prepare

1. Find the test command. Use the wrapper if there is one (`./mvnw`, `./gradlew`).
   - Maven: `mvn -q test -Dtest='OrderTest#removesItem'`. In multi-module builds, add `-pl <module> -am -Dsurefire.failIfNoSpecifiedTests=false`.
   - Gradle: `./gradlew test --tests 'com.example.OrderTest.removesItem'`.
2. Run the existing suite once, so failures that existed before the change are known and not blamed on it.
3. If nothing can run tests (no build file, no test framework, no runner), stop. Propose the smallest setup and wait for approval.
4. Write the test list: one line per behavior, simplest first, taken from the acceptance criteria (from the `spec-architecture-verification` design note when there is one). Follow those with the edge cases from `test-backfill`'s case list. For a bug fix, the first item reproduces the bug.

## 1. Red

- Write one test for the next item on the list, following `test-backfill`'s test-design rules: match the existing tests, one behavior per test, deterministic, and mocks only at boundaries.
- Make it compile with the smallest stub, such as an empty method or a default return value. A compile error does not count as red.
- Run it. It must fail on its assertion, and the failure message must show the reason you expect. If it fails for another reason, fix the test and run it again.
- If it passes at once, stop and find out why. Either the behavior already exists, and the item comes off the list, or the test does not test what you think, and you fix it. Never write production code for a test that has not failed.

## 2. Green

- Write the minimum production code that makes this test pass. Add nothing for later items, even when you can see what is coming.
- Run the test, then the test class. All must pass, and earlier tests must still pass.
- Do not change the test to make it pass. If the test was wrong, say so, fix it, and go back to red.

## 3. Refactor

- Refactor only when everything is green. Clean up production and test code from this cycle (duplication, names, structure) under `auto-simplify`'s rules, without adding behavior.
- Make one change at a time and run the tests after each. If they go red, undo that change.
- Behavior found while refactoring goes on the test list. It does not go into the code.

Then take the next item. Finish when the list is empty and the full suite passes.

## Never

- Claim a result you did not see in the runner's output, or skip a run because the outcome seems obvious.
- Disable, skip, or delete tests (`@Disabled`, `@Ignore`, `-DskipTests`, `-x test`), weaken assertions, or catch exceptions in a test so it passes.
- Change an expected value to match output you have not confirmed is correct.

## Report

For each cycle: the test, the red command and failure message, the green change, the refactor, and the results. Finish with the full-suite command and result, and any failures that existed before the change.

See [references/example.md](references/example.md) for two worked cycles.
