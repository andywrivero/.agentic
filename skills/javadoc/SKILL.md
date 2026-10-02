---
name: javadoc
description: Analyzes Java source files and generates or updates clean, professional Javadoc optimized for IDE hover tooltips and developer productivity. Enforces Oracle JavaDoc specifications, modern tag conventions (Java 8-21+), nullability-annotation sync, correct exception mapping (including unchecked exceptions), generics type parameters, and clean summary fragments. Use whenever writing a new Java class, interface, enum, or record, or editing an existing one, and Javadoc comments are missing, outdated, or need review - even if the user's request doesn't explicitly mention documentation.
---

# Skill: Javadoc Documentation Engine

## Description
Analyzes Java source files and generates or updates clean, professional Javadoc optimized specifically for IDE hover tooltips and developer productivity. Enforces Oracle JavaDoc specifications, modern tag conventions (Java 8–21+), nullability-annotation sync, correct exception mapping, generics type parameters, and clean summary fragments.

## Objectives
1. Add or update missing/outdated Javadoc tags (`@param`, `@return`, `@throws`, `@param <T>`).
2. Maintain clean, non-obvious documentation—explain *why* and contract behavior, not just restating field or method names.
3. Ensure HTML5 compatibility and proper inline tag usage (`{@code}`, `{@link}`).
4. Optimize every block for IDE hover popups: punchy lead sentence, compact `<p>`-separated paragraphs, no walls of text.
5. Keep nullability annotations (`@NonNull`, `@Nullable`, `@NotNull`, etc.) and Javadoc contracts in sync.
6. Skip redundant Javadocs on trivial getters, setters, standard constructors, or standard overridden interface methods (`@Override`) — use `{@inheritDoc}` instead where appropriate.

---

## Workflow Protocol

### Step 1: Target Scope & Diff Inspection
1. Inspect the target `.java` file, class, interface, enum, or record.
2. Scan existing Javadoc blocks to check for outdated parameter names, stale nullability contracts, or missing checked/runtime exceptions.

### Step 2: Scope & Visibility (Internal Focus)
- **Document everything useful, not just public APIs.** Generate Javadoc for `public`, `protected`, package-private, and complex `private` methods — developers rely on hover tooltips while reading internal code too.
- **Skip trivial code.** Do not document obvious getters, setters, or standard constructors that just assign fields. If the code is self-documenting, skip it.
- A "complex" private method (worth documenting) is one with non-obvious control flow, side effects, tricky invariants, or a non-trivial contract — not a one-line delegation.

### Step 3: Documentation Standards & Rules

#### 1. Summary Fragment (First Sentence)
- Must be a concise **summary fragment**, not a complete sentence. Start with a third-person singular present-tense verb (e.g., "Executes...", "Calculates...", "Validates...").
- Do NOT use passive voice like "This method is used to...".
- Make it crisp and punchy — IDE hover popups bold/preview this sentence in isolation, so it must stand alone and convey the method's purpose at a glance.

#### 2. Class, Interface & Record Level
- Document overall responsibility, threading/concurrency guarantees (e.g., "Instances of this class are immutable" or "This class is thread-safe."), and usage examples if complex.
- **Records (Java 14+):** Use `@param <componentName>` for record components in the header Javadoc.
- **Generics:** Document type parameters using `@param <T>` explaining the bounds and purpose.

#### 3. Method Level & Tag Ordering
Always include `@param`, `@return`, and `@throws` where applicable — IDE tooltips pull these into organized, highly readable metadata blocks. Follow strict standard tag ordering:
1. `@param <T>` (Type parameters)
2. `@param name` (Method parameters)
3. `@return` (Return value description; omit for `void` methods)
4. `@throws ExceptionClass` or `@exception` (Document all checked exceptions and major unchecked exceptions like `IllegalArgumentException` or `NullPointerException` if part of the method contract)
5. `@see` / `@since` / `@deprecated`

**Unchecked exception marker:** For any `@throws` whose exception extends `RuntimeException` (or `Error`) — whether or not it is declared in the `throws` clause — append `(unchecked)` to the end of the description so the caller knows it isn't a checked exception, e.g.:
```
@throws IllegalArgumentException (unchecked) if {@code id} is negative
```

#### 4. Nullability Annotation Sync
When a parameter or return type carries a nullability annotation (`@NonNull`, `@Nullable`, `@NotNull`, etc.), the Javadoc must state the contract explicitly:
- **`@param` constraints:** Open the `@param` text with the rule itself, e.g. `@param userId the unique identifier; must not be null` or `@param options configuration options; can be null for defaults`.
- **`@return` constraints:** Clarify nullable returns in the `@return` tag, e.g. `@return the active session user, or {@code null} if no session exists`.
- **Validation rule:** If a parameter is marked `@NonNull` (or equivalent), the Javadoc must also include a corresponding `@throws NullPointerException` entry specifying when/why it is thrown (e.g., `@throws NullPointerException (unchecked) if {@code userId} is null`).

#### 5. Formatting & Inline Tags
- Wrap all variable names, class names, method names, and constant literals in `{@code term}` — IDEs render this as monospace font in the hover popup.
- Use `{@link FullyQualifiedClass#method}` for internal cross-references.
- Keep descriptions compact: use short paragraphs separated by `<p>` tags rather than one dense block, so the hover box doesn't require excessive scrolling.
- Do NOT use raw HTML tags like `<tt>` or `<code>` (deprecated).

#### 6. Leverage Inheritance
For overridden methods that don't alter the inherited contract, use `{@inheritDoc}` so the IDE dynamically pulls the parent/interface documentation into the hover window instead of duplicating it.

---

## Filter & Exclusion Rules (Noise Reduction)
- **Do NOT document:** Standard trivial getters/setters (`getFoo()`, `setFoo()`) or standard constructors that just assign fields, unless they perform custom validation, transformations, or side effects.
- **Do NOT duplicate `@Override` docs:** If a method implements an interface method without altering its contract, omit the method Javadoc so it inherits naturally (`{@inheritDoc}` if custom behavior is added).
- These exclusions apply regardless of visibility — a trivial private getter is still trivial.

---

## Output Execution Pattern
1. Generate or update the Javadoc comments directly inline above the respective class, record, interface, or method.
2. Keep line length within 100–120 characters where possible.
3. Preserve existing code formatting and code logic untouched.
