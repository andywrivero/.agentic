---
name: java8-pro
description: "Enforces Java 8 (JDK 1.8) idioms, Stream API pipelines, java.time, Lambdas, and clean architecture while avoiding JDK 9+ features."
---

# Skill: Java 8 Pro & Clean Architecture

## Description
Enforces idiomatic Java 8 (JDK 1.8) code style, functional paradigms, and clean design principles. Guarantees strict compatibility with the Java 8 specification while eliminating legacy pre-Java 8 code smells (like `java.util.Date` or verbose anonymous inner classes).

## Strictly Forbidden Features (Requires JDK 9+)
Do NOT output code using features introduced after Java 8:
- ❌ No `var` local variable type inference (Java 10+)
- ❌ No `record` data carriers (Java 14+)
- ❌ No Text Blocks `"""` (Java 15+)
- ❌ No Pattern Matching for `instanceof` or `switch` (Java 16+)
- ❌ No `List.of()`, `Set.of()`, or `Map.of()` collection factory methods (Java 9+)
- ❌ No `.toList()` directly on `Stream` (use `.collect(Collectors.toList())`)

---

## Language Rules & Idioms

### 1. Functional Constructs & Streams
- **Lambdas & Method References:** Replace anonymous inner classes with lambda expressions or method references (`Class::method`) where applicable.
- **Stream API Pipelines:** Use `java.util.stream.Stream` for collection processing.
  - Correct Collector: `.collect(Collectors.toList())` or `.collect(Collectors.toSet())`.
- **Custom Functional Interfaces:** Annotate single-abstract-method interfaces with `@FunctionalInterface`.

### 2. Modern Date & Time API (`java.time`)
- **Forbidden:** Never use `java.util.Date`, `java.util.Calendar`, or `java.text.SimpleDateFormat`.
- **Required:** Use `java.time` classes (`LocalDate`, `LocalTime`, `LocalDateTime`, `ZonedDateTime`, `Instant`, `Duration`).
- **Formatting:** Use `java.time.format.DateTimeFormatter` for parsing and formatting.

### 3. Null Handling & Optional
- **`Optional<T>`:** Use `Optional` strictly as a return type for methods that may reasonably yield no result.
- Avoid calling `.get()` directly without checking; prefer `.map()`, `.flatMap()`, `.orElse()`, `.orElseGet()`, or `.orElseThrow()`.
- Do NOT use `Optional` for method parameters, class fields, or constructor arguments.

### 4. Interface Enhancements
- Utilize `default` methods on interfaces for optional operations or extension points.
- Use `static` helper methods inside interfaces to encapsulate factory or utility logic related to the interface contract.

### 5. Checked Exceptions in Lambdas & Streams
- Lambdas passed to `Stream`/`Function`/`Consumer` cannot throw checked exceptions directly.
- Never swallow the checked exception silently or wrap it in a bare `RuntimeException`.
- Catch the checked exception inside the lambda and rethrow it wrapped in the project's own unchecked exception type (e.g., a type from the `error` hierarchy such as `TransportException` or `SerializationException`) so callers outside the stream still get a meaningful, typed failure.

### 6. Asynchronous Composition
- Where the underlying `HttpClient` exposes an async/non-blocking contract, use `java.util.concurrent.CompletableFuture` (`thenApply`, `thenCompose`, `exceptionally`) rather than blocking calls or raw `Thread`/`ExecutorService` plumbing.

---

## Workflow Protocol

### Step 1: Pre-Check & Anti-Pattern Audit
Scan code for target cleanups:
- Verbose `for` loop filtering that can be converted into a clean `stream().filter().map()` pipeline.
- Raw types (e.g., using `List` instead of `List<String>`).
- Generic `catch (Exception e)` or empty catch blocks.

### Step 2: Code Execution & Refactoring
1. Keep classes explicit and typed (using standard Java 8 type parameters).
2. Use standard JavaBeans encapsulation (private `final` fields, constructors, explicit getters/setters).
3. Ensure custom exceptions extend `RuntimeException` (unchecked).

### Step 3: Verification Check
1. Verify that all imports come from JDK 8 packages.
2. Actually run the project's configured build command (e.g., `mvn compile` or `./gradlew compileJava`) and confirm it exits successfully — do not treat compilation as verified without executing it. If no build tool is configured yet, fall back to `javac -target 1.8 -source 1.8` against the changed files.

### Note on Target Version
This skill hardcodes the JDK 8 forbidden-features list above. If the project's target JDK ever changes, update that list rather than treating it as permanent — it encodes the current target, not a fixed language philosophy.
