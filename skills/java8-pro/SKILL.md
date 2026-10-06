---
name: java8-pro
description: Keep Java code compatible with a Java 8 target (source, target, or release 8 / 1.8) and idiomatic for it. Use when adding or changing Java code in a Java 8 project, or when reviewing Java 8 compatibility. Not for modernizing untouched code.
---

# Java 8 Compatibility and Idioms

Owns Java 8 language, API, and dependency compatibility, plus Java 8 idioms in code being written or changed. It does not own general refactoring (`auto-simplify`), member placement (`java-member-ordering`), or Javadoc (`javadoc`).

## Settings

Resolve each setting from, highest first: the current request; a `java8-pro` entry under `Skill settings` in the project's AGENTS.md or CLAUDE.md; the build configuration; the defaults below.

- `idioms`: `new-code` — apply the idioms below to new or changed code only. Or `compat-only` (enforce compatibility, leave style alone).
- `verify`: `on-request` — compile or test only when asked. Or `after-edit` (run the project's compile task).
- `exception-wrapper`: `auto` — reuse the project's own unchecked exception type for checked exceptions in lambdas; fall back to `UncheckedIOException` for `IOException`. Or name a specific class.

## Confirm the target

Read the level from build configuration (`maven.compiler.release`/`source`/`target`, `maven-compiler-plugin`, Gradle `sourceCompatibility`/`options.release`, toolchains). Do not infer it from the installed JDK. If the build uses `source`/`target` 8 without `release` 8 while compiling on JDK 9+, warn that post-8 APIs can still compile and then fail at runtime (for example `ByteBuffer.flip()` returning `ByteBuffer`). Do not change build config unless asked.

## Compatibility rules

- No post-8 language features: `var`, private interface methods, diamond with anonymous classes, effectively-final resources in try-with-resources, switch expressions, text blocks, records, sealed types, pattern matching, modules.
- No post-8 APIs. Common traps: `List/Set/Map.of`, `copyOf`, `Stream.toList`, `Optional.isEmpty`/`or`/`ifPresentOrElse`/`stream`/no-arg `orElseThrow`, `String.isBlank`/`strip`/`lines`/`repeat`, `Files.readString`, `Path.of`, `InputStream.transferTo`/`readAllBytes`, `Predicate.not`, `java.net.http`. Full list: [references/post-java8-apis.md](references/post-java8-apis.md).
- New or upgraded dependencies must support a Java 8 runtime. Spring Framework 6 / Boot 3, Hibernate 6, Mockito 5, and many Jakarta EE 9+ libraries do not.

## Idioms for new or changed code

- Lambdas and method references instead of anonymous classes for functional interfaces. Mark custom single-method interfaces `@FunctionalInterface`.
- Streams for clear filter/map/collect pipelines; keep loops when they are clearer, need early exit, or mutate state. No side effects inside stream operations. Avoid `parallel()` unless measured. Give `Collectors.toMap` a merge function when keys can collide.
- `Map.computeIfAbsent`, `merge`, `getOrDefault`, and `removeIf` instead of manual check-then-act code.
- `Optional` only as a return type for a possibly absent result; not for fields, parameters, or collections. Prefer `map`/`orElse`/`orElseGet`/`orElseThrow(supplier)` to `isPresent` + `get`.
- `java.time` for new date and time code. Convert at the boundary when a legacy API requires `Date` or `Calendar`.
- Checked exceptions in lambdas: wrap per `exception-wrapper` with the original as the cause. Never swallow them or throw a bare `RuntimeException`.
- `CompletableFuture`: follow the project's existing async API. Pass an explicit executor for blocking work instead of the common pool. Handle failures with `exceptionally`/`handle`/`whenComplete`.

## Workflow

Confirm the target, then check only the code in scope. Fix compatibility issues in code you are changing; report ones found elsewhere. If `verify` is active, run the project's compile task and report the exact command and result. Otherwise say that compatibility was not compiler-verified.
