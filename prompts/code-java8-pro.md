# Java 8 Pro Prompts

Use these prompts with the existing `java8-pro` skill.

## 1. Implement a Java 8 Feature

Implement the requested feature in the current project: **[describe the feature]**.

- First inspect the relevant implementation, nearby tests, and project conventions.
- Apply the `java8-pro` skill: keep the code compatible with JDK 8 and follow its language, API, exception, and architecture rules.
- Make the smallest complete change that fits the existing design. Preserve established public APIs unless the feature requires otherwise.
- Add or update focused tests for the behavior.
- Run the narrowest relevant tests, then the configured build or compile check when practical. Report what passed and anything not verified.

## 2. Refactor Java Code for Java 8

Refactor **[identify the class, method, or code path]** to improve clarity and maintainability without changing observable behavior.

- Inspect callers and existing tests before changing the code.
- Apply the `java8-pro` skill and keep all code strictly compatible with JDK 8.
- Prefer lambdas, method references, and streams where they make the intent clearer; retain ordinary loops when they are simpler or better suited to the work.
- Use `java.time` for date/time changes and use `Optional` only where appropriate for return values.
- Preserve public contracts, exception semantics, and project conventions. Avoid unrelated cleanup.
- Run focused tests or compilation checks and summarize the behavior-preservation evidence.

## 3. Review Java 8 Compatibility

Review **[identify the files, diff, or feature]** for correctness, maintainability, and strict Java 8 compatibility. Do not edit files.

- Apply the `java8-pro` skill as the review standard.
- Report actionable findings first, ordered by severity, with file and line references and a concise explanation of impact.
- Check for post-Java 8 syntax and APIs, including `var`, records, text blocks, pattern matching, `List.of`/`Set.of`/`Map.of`, and `Stream.toList()`.
- Also check relevant Java 8 idioms: legacy date/time APIs, unsafe `Optional` usage, raw types, swallowed checked exceptions in lambdas, and blocking where the existing async contract supports `CompletableFuture`.
- Distinguish confirmed issues from assumptions. If there are no findings, say so and note any meaningful verification gaps.
