---
name: test-backfill
description: Find untested or newly added logic and backfill unit tests for its edge cases (null and empty inputs, boundary values, error paths, state transitions), replacing external dependencies and APIs with mocks or fakes, and prove each test can fail. Use when the user asks to add or improve tests for existing code, raise coverage, or cover a change that was written without tests. Not for test-first development (`tdd-loop`).
---

# Test Backfill

Owns choosing and writing tests for code that already exists: finding the gaps, picking the cases, isolating dependencies, and proving each test can fail. Its test-design rules also apply to tests written under `tdd-loop`. It does not own changing production code (bugs found go to `tdd-loop`), test-code formatting (`java-code-style`), Java 8 compatibility of test libraries (`java8-pro`), or commits (`atomic-ordered-git-commits`).

## Settings

Resolve each setting from, highest first: the current request; a `test-backfill` entry under `Skill settings` in the project's AGENTS.md or CLAUDE.md; the project's build and test configuration; the defaults below.

- `scope`: `changed` — code changed in the current task or the given diff; an explicitly named class, method, or path counts as in scope. Or `uncovered` (untested code in a named area, found with the coverage report).
- `coverage`: `if-available` — use an existing coverage report or task (JaCoCo) to find gaps; do not add the plugin unless asked. Or `off`.
- `mutation-check`: `boundaries` — prove the boundary and error-path tests can fail (see step 4). Or `all`, `off`.
- `on-bug`: `report` — when a correct test fails because the code is wrong, leave the test out and report the bug. Or `add-failing` (keep the failing test so the bug stays visible).

## 1. Find the gaps

- List the behaviors in scope: public methods, their branches, throw sites, and state changes. Read existing tests and the coverage report to see which are already covered.
- Start with logic where a mistake costs most: branching, validation, arithmetic and money, parsing, state transitions, and error handling. Skip trivial accessors, generated code, and plain delegation.
- The expected result comes from the contract: the Javadoc, spec, and type names, and callers when those are silent. If the contract is unclear, ask or list the question. Do not assume the current output is correct.

## 2. Choose the cases

For each behavior, go through this list and keep only the cases that apply:

- **Null:** each reference input that the contract allows to be null gets its documented handling. Where the code rejects null, test the exception it throws (`requireNonNull(x, "x")` throws `NullPointerException` with message `"x"`). If null is unchecked and undocumented, report it instead of inventing behavior.
- **Empty:** empty and blank strings, empty collections, arrays, and varargs, `Optional.empty()`.
- **Boundaries:** at, just below, and just above each limit (a `MAX` constant, a size check, `<` vs `<=`). Also 0, 1, and negative values, `Integer.MIN_VALUE`/`MAX_VALUE` where arithmetic can overflow, and decimal scale and rounding.
- **State:** every relevant enum or lifecycle value, including terminal ones; illegal transitions; repeated calls.
- **Errors:** every throw site, with the exception type and the message when callers rely on it. Failures from dependencies are propagated, translated, or logged exactly as the code says.
- **Returned data:** unmodifiable views, defensive copies, ordering guarantees, and duplicates.
- **Equality:** if `equals`/`hashCode` are overridden, test equal, unequal, `null`, other types, and new or unsaved instances.
- **Concurrency:** only when the code promises thread safety, and only with deterministic tests. Otherwise report the gap.

## 3. Test design

These rules also apply under `tdd-loop`.

- Match the existing tests: framework, assertion and mocking libraries, naming, location (`src/test/java`, mirroring the package), and fixture style. Adding a test dependency (Mockito, `junit-jupiter-params`, WireMock) needs approval, and it is added per `java-dependency-management`.
- Each test covers one behavior through the public API, laid out as arrange, act, and assert blocks. Keep loops and conditionals out of test bodies; put setup in helpers, and use parameterized tests for boundary tables when the project has them.
- Assert specific results: values, state, exception type and message. "No exception was thrown" is not enough.
- Keep tests deterministic: no sleeps, real clocks, randomness, network, or shared mutable state between tests.
- **External dependencies:** replace them at an existing seam, such as a constructor-injected interface. Use the project's mocking library; if it has none, write a small fake. Mock only boundaries: repositories, HTTP and messaging clients, the clock, the file system, other services. Never mock the class under test or value and domain objects.
- **External APIs:** stub at the client interface or at the HTTP level with the project's tool (WireMock, MockWebServer). Cover success, 4xx, 5xx, timeout, malformed and empty bodies, and missing optional fields.
- Stub only what the test path uses. Verify interactions only when the interaction is the behavior (for example, "saves once" or "never saves"); otherwise assert the result.
- If there is no seam (a static call, `new` inside the method, `Instant.now()`), do not change production code to add one without asking. Report it.

## 4. Run and prove

- Run the new tests with the project's runner (`mvn -q test -Dtest=…`, `./gradlew test --tests …`). They should pass against the current code.
- **A failing test:** first check the test itself. If the test is correct and the code is wrong, follow `on-bug`. Never change the expected value to match output you have not confirmed is correct.
- **Mutation check (per `mutation-check`):** break the line each test guards (flip `>=` to `>`, `<=` to `<`, drop a guard), run again, and confirm the test fails. Restore the line, then confirm the production code is back to its original state, for example with `git diff`. A test no mutation can fail is not doing its job; strengthen or drop it.
- Run the module's full suite before finishing.

## Never

- Leave production code changed. The only allowed edits are temporary mutations, and they are reverted.
- Disable, skip, or weaken tests, or claim results you did not see in the runner's output.
- Assert current behavior that contradicts the documented contract.

## Report

- Behaviors covered, each with its tests.
- Gaps left and why (no seam, unclear contract, needs a dependency).
- Bugs found, with the failing input and the expected and actual results. Offer to fix each one with `tdd-loop`, using the failing test as its first red. If the cause is not clear from the test, diagnose it with `systematic-debugging` first.
- Mutation results, and the commands run with their results.

See [references/example.md](references/example.md) for a worked backfill.
