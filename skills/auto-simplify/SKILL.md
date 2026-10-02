---
name: auto-simplify
description: "Executes a strict, non-behavioral second-pass review over newly written or modified code. Reduces cognitive complexity, enforces single-responsibility, and removes dead code without altering public API contracts, functional logic, or breaking existing tests. Use after writing or editing code to clean it up before submission."
---

# Skill: Auto-Simplify & Auto-Refactor Engine

## Description
Executes a strict, non-behavioral second-pass review over newly written or modified code. Focuses on code hygiene, cognitive complexity reduction, single-responsibility enforcement, and dead code removal without altering public API contracts, functional logic, or breaking existing tests.

## Objectives
1. Eliminate cognitive clutter by reducing deep nesting, early returns, and applying guard clauses.
2. Enforce Single Responsibility Principle (SRP) by extracting bloated methods/functions into focused helper routines.
3. Remove dead/unreachable code, unused imports, commented-out code blocks, and redundant intermediate variables.
4. Clean up over-engineered abstractions, wrapper methods, and verbose language constructs.
5. Remove performance regressions introduced by this pass itself (e.g., a redundant stream traversal or unnecessary collection copy created while refactoring). Do not go looking for unrelated pre-existing performance optimizations outside the diff scope — that is not this skill's job.

---

## Refactoring Protocol & Checklist

### Step 1: Target Scope Analysis
1. Inspect `git diff` or target working tree files to identify newly written or modified methods.
2. Run the project's actual test command (e.g., `mvn test` or `./gradlew test`) and confirm it passes BEFORE applying any simplifications — do not proceed on the assumption that tests pass without running them.

### Step 2: Refactoring Execution Checklist

#### 1. Cognitive Complexity & Control Flow
- Convert deeply nested `if/else` structures into **early exit guard clauses**.
- Replace complex, multi-line conditional chains or nested ternaries with clear boolean variables or isolated predicate methods.

#### 2. Method Granularity & SRP (Single Responsibility)
- Extract methods exceeding ~20–25 lines or those performing multiple distinct operations (e.g., validation + transformation + execution) into private, single-purpose helper functions. Do not extract purely to hit a line-count target when the length comes from flat, low-complexity constructs (e.g., a straight field-by-field DTO mapper) with no real branching or mixed responsibilities to separate.
- Ensure function names state exact intent without using ambiguous conjunctives (e.g., split `validateAndSave` logic into clear discrete steps).
- When extracting new private helper methods in Java, place them per the project's `java-member-ordering` convention (public/protected methods before private helpers, helpers grouped together) rather than inserting them immediately after the call site.

#### 3. Dead Code & Variable Pruning
- Remove unused imports, dead parameters, unused local variables, and commented-out code blocks.
- Inline single-use variable assignments if inlining improves code readability without hiding complex calculations.

#### 4. Abstraction Flattening
- Eliminate unnecessary wrapper methods that merely delegate to underlying methods without adding validation, transformation, or domain logic.
- Replace verbose anonymous types or boilerplate constructs with concise modern language idioms (e.g., lambdas or method references). Do not introduce pattern matching (`instanceof`/`switch`) or other JDK 9+ syntax on a Java 8 target — defer to `java8-pro` for the project's language-level constraints.

---

## Safety Constraints
- **Zero Behavioral Regressions:** Do NOT alter public method signatures, API contracts, or core business logic.
- **Verification Rule:** Re-run project build commands and unit test suites immediately after refactoring. If any test fails, revert the refactoring pass.
- Do NOT rewrite or reformat unmodified legacy code outside the diff scope.

---

## Output Summary
Provide a concise, bulleted change summary explaining what was simplified (e.g., *"Extracted validation helper in UserService"*, *"Converted nested IFs to guard clauses in TokenValidator"*).
