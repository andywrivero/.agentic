---
name: auto-simplify
description: Simplify recently changed code, or a named area, without changing behavior. Use when the user asks for a cleanup or simplification pass, or after writing code when a pass is clearly worthwhile. Not for general refactoring, bug hunting, or modernizing untouched code.
---

# Auto Simplify

Owns behavior-preserving cleanup. It does not own bug fixes, language-level compatibility (`java8-pro`), member placement (`java-member-ordering`), or documentation (`javadoc`); apply those only when requested or required by the edit.

## Settings

Resolve each setting from, highest first: the current request; an `auto-simplify` entry under `Skill settings` in the project's AGENTS.md or CLAUDE.md; project lint and formatter config; the defaults below.

- `scope`: `changed` — code changed in the current task or the given diff; an explicitly named class, method, or path counts as in scope. Or `file` (whole files touched by the change).
- `verify`: `on-request` — run checks only when asked. Or `after-edit` (run the narrowest relevant tests or compile after editing).

## What to improve

Apply a change only when the result is clearly easier to read or maintain:

- Control flow: replace deep nesting with guard clauses or early returns; untangle nested ternaries and long boolean chains with well-named variables or predicate methods.
- Structure: extract a helper when a method mixes distinct steps (for example validate, transform, persist). Line count alone is not a reason; flat code such as a field-by-field mapper can stay long.
- Duplication: merge logic repeated within the change. Do not invent abstractions for two similar lines.
- Dead weight: unused imports, locals, and private members; commented-out code; redundant intermediates; wrappers that only delegate.
- Naming: rename local or private identifiers that hide intent. Leave public names alone.
- Library use: replace hand-written logic with an existing project utility or standard-library call when it is equivalent.

## Guardrails

- Preserve observable behavior: return values, exceptions and their types and messages, side-effect order, logging, thread safety, and null handling.
- Preserve public and protected signatures, serialized forms, and anything reached by reflection, DI, annotations, or configuration. Treat code as dead only after confirming nothing references it that way.
- Do not introduce extra passes over data, extra copies, or eager evaluation where the original was lazy.
- Keep straightforward loops when a stream or abstraction would be less clear. Follow the project's style and language level.
- Do not touch code outside `scope`. Report worthwhile issues found there instead of fixing them.

## Workflow

Inspect the target code and its callers, make only the worthwhile edits, and summarize each one in a line (what and why). If `verify` is active, use the narrowest relevant check and report what ran and what did not. If nothing is worth changing, say so.
