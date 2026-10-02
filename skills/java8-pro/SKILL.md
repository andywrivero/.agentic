---
name: java8-pro
description: Check or implement Java code for Java 8 source and API compatibility when the project targets JDK 8. Do not use for general Java cleanup or modernization.
---

# Java 8 Compatibility

Owns Java 8 source and standard-library compatibility. It does not own general refactoring, member placement, or Javadoc quality; address those separately only when requested.

## When it applies

Use when the project targets Java 8 and the task adds or changes Java code, or when Java 8 compatibility is explicitly under review. Confirm the configured source, target, or release level from project configuration where possible. Do not infer compatibility from the installed JDK or package names.

## Compatibility rules

- Do not use language features introduced after Java 8, including local variable type inference, records, text blocks, or pattern matching.
- Do not use post-Java-8 library APIs such as List.of, Set.of, Map.of, or Stream.toList.
- Prefer Java 8 APIs only when they suit the requested change and established project style. Preserve existing API and exception contracts.
- Keep loops when they are clearer than streams. Use java.time or Optional only when suitable to the requested change; do not modernize unrelated code.
- In lambdas and streams, preserve useful checked-exception context. Do not silently swallow failures.
- Compose asynchronous work with the project's existing asynchronous API when applicable; do not introduce asynchronous architecture as cleanup.

## Workflow

Check the target level and only the relevant changed code. Fix or report compatibility issues within the requested scope. Do not add or run tests unless the user asks for testing or verification; when requested, report the exact check and result.
