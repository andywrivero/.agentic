---
name: java-logging-exceptions
description: Write and review Java exception handling and logging. Covers checked vs. unchecked exceptions, wrapping with the cause, custom exception types, catch scope, interrupts, log levels, parameterized messages, stack traces, and keeping secrets out of logs. Use when adding or changing try/catch/throw code, custom exceptions, or log statements, or when reviewing them.
---

# Java Logging and Exceptions

Owns how code raises, wraps, catches, and logs failures, and how log statements are written. It does not own where exceptions are translated between layers (`spec-architecture-verification`), checked exceptions inside lambdas (`java8-pro`'s `exception-wrapper`), `@throws` documentation (`javadoc`), the logger field's name (`java-code-style`), or diagnosing a failure (`systematic-debugging`).

## Settings

Resolve each setting from, highest first: the current request; a `java-logging-exceptions` entry under `Skill settings` in the project's AGENTS.md or CLAUDE.md; the project's logging setup (SLF4J, Log4j 2, `java.util.logging`, Logback config); the defaults below.

- `framework`: `auto` — use the logging API the project already uses; never add a second one. Or name one.
- `message-style`: `follow-file` — match the exception message style of nearby code (in the samples, `"Unknown order: " + orderId`). Or `sentence` (a capitalized phrase with no trailing period).

## Exceptions

- **Checked vs. unchecked:** follow the project. A common split, and the one in the samples:
  - checked, domain-specific exceptions (`OrderException`) for failures callers are expected to handle
  - `IllegalArgumentException`, `IllegalStateException`, and `NullPointerException` (via `Objects.requireNonNull(x, "x")`) for caller mistakes and broken invariants
- **Custom types:** extend the project's base exception. Provide `(String message)` and `(String message, Throwable cause)` constructors, plus `serialVersionUID`. Add a new type only when callers would handle it differently.
- **Wrapping:** always pass the original as the cause. The new message adds context the cause lacks (operation, ids), not a copy of the cause's message.
- **Catching:**
  - Catch the narrowest type that you can handle.
  - Catch `Exception`, `RuntimeException`, or `Throwable` only at a top-level boundary (request handler, scheduled job, thread `run`, `main`), and log it there once.
  - Never catch `Error` subclasses to carry on.
- **Handle or propagate, not both:** either deal with the exception (recover, fall back, translate) or let it propagate. Logging and then rethrowing logs the same failure twice.
- **Never swallow:** an empty `catch` needs a comment saying why ignoring the exception is safe, for example `// close failure after successful write is harmless`.
- **`InterruptedException`:** restore the flag with `Thread.currentThread().interrupt()` before returning or wrapping it, unless you rethrow it.
- **Resources:** use try-with-resources. Never `return` or `throw` from `finally`; it hides the original exception.
- **Signalling:** do not use exceptions for normal control flow, and do not return `null` or error codes where the project uses exceptions or `Optional`.
- **Messages:** say what failed and include the identifying values. Never include passwords, tokens, keys, or personal data.

## Logging

- **Choosing a level:**
  - `ERROR`/`SEVERE`: someone must act.
  - `WARN`/`WARNING`: unexpected, but handled.
  - `INFO`: rare lifecycle or business events.
  - `DEBUG`/`FINE`: diagnostics.

  Do not log at `INFO` inside loops or on hot paths.
- **Parameterized messages:**
  - SLF4J and Log4j 2: `{}` placeholders, with the exception as the last argument, which keeps its stack trace: `log.warn("Save failed for order {}", id, e)`.
  - `java.util.logging`:
    - `{0}` placeholders are formatted by `MessageFormat`, which writes numbers with locale grouping (`1234567` becomes `1,234,567`). Pass ids as `String.valueOf(id)`.
    - A `Throwable` passed in the parameters array is dropped. To keep the stack trace, use `log(Level, String, Throwable)` with a pre-built message, or `log(Level, Throwable, Supplier<String>)`.
    - Use a `Supplier` for expensive messages.
- **Stack traces:** log a stack trace once, at the place that handles the failure. Never use `printStackTrace()` or `System.out`/`System.err`.
- **Context:** include identifiers (order id, request id), or put them in MDC (`MDC.put`, cleared in `finally`) if the project uses MDC.
- **Safety:** never log secrets or personal data. Strip CR and LF from user-supplied values unless the log format already escapes them.
- **Loggers:** one `private static final` logger per class, created from its own class and named per `java-code-style`.

## Workflow

Apply these rules to the code being written or changed. For existing code, report issues instead of fixing them. Changing which exception type a method throws, or whether a method logs, is a behavior change: check callers and tests, and ask first if either relies on the current behavior.

For reviews, report findings as: file:line, rule, fix.

See [references/example.md](references/example.md) for a worked review.
