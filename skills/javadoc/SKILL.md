---
name: javadoc
description: Write, update, or review Javadoc for Java types and members. Use when documentation is requested or when a change alters a documented or public API contract. Do not trigger for unrelated Java edits.
---

# Javadoc

Owns Javadoc comments only. Do not change code, signatures, or annotations, and do not sweep files for undocumented members beyond the requested scope.

## Settings

Resolve each setting from, highest first: the current request; a `javadoc` entry under `Skill settings` in the project's AGENTS.md or CLAUDE.md; project tooling (Checkstyle Javadoc checks, `javadoc` plugin custom tags, formatter line length); the defaults below.

- `visibility`: `api-plus-complex` — public and protected members, plus package-private or private members with non-obvious contracts, side effects, or invariants. Or `api` (public and protected only), `all-nontrivial`.
- `unchecked-marker`: `off`. Set `on` to end every `@throws` description for an unchecked exception with `(unchecked)`.
- `line-length`: the project formatter's limit; otherwise 100.

## Content

- First sentence: a standalone summary in third person ("Returns the active session…", not "Return…" or "This method is used to…"). Javadoc and IDE tooltips show it on its own.
- Describe the contract, not the implementation: what it does, preconditions, postconditions, side effects, and edge cases (empty, null, negative, concurrent use). Do not restate the name ("Gets the name").
- Types: state the responsibility, and thread-safety or immutability when callers need to know. Add a short `<pre>{@code …}</pre>` example only for non-obvious usage.
- Nullability: state null handling in `@param`/`@return` wording that matches actual behavior. An annotation alone does not prove null is checked or which exception is thrown.
- Skip trivial getters, setters, and field-assigning constructors unless they validate or have side effects. For overrides that keep the inherited contract, omit the comment or use `{@inheritDoc}` plus only what is added.
- Deprecation: pair `@deprecated` with `@Deprecated`, and say what to use instead with `{@link}`.

## Tags and formatting

- Order: `@param <T>` type parameters, `@param` in declaration order, `@return` (omit for `void` and constructors), `@throws`, `@see`, `@since`, `@deprecated`.
- `@throws`: document checked exceptions and the unchecked exceptions callers can reasonably expect (invalid arguments, illegal state). Do not list every possible runtime exception. Use `@throws`, not `@exception`.
- `@param`/`@return` text is a lowercase phrase with no trailing period unless it spans sentences.
- Use `{@code}` for identifiers, literals, and code; `{@link}` for useful cross-references, linking each target only once per comment. Never use `<tt>` or `<code>`.
- Write HTML that doclint accepts (it fails JDK 8+ builds by default): `<p>` before each new paragraph and never `<p/>`; escape `<`, `>`, `&` outside `{@code}`; close lists and tables.
- Use `@apiNote`, `@implSpec`, and `@implNote` only if the project's javadoc build defines them.
- Wrap at `line-length` and match the file's existing comment style.

## Workflow

Read the declaration, its implementation, annotations, callers when relevant, and any inherited contract. Fix stale parameter names, outdated behavior, and wrong exceptions you find in scope. Report contract questions instead of guessing at guarantees. Do not add or run tests or the javadoc tool unless asked.
