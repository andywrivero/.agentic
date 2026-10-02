---
name: javadoc
description: Write, update, or review Javadoc when documentation is requested or a changed API contract needs documentation. Do not trigger for unrelated Java edits.
---

# Javadoc

Owns Javadoc comments only. Do not change implementation logic or perform a documentation sweep beyond the requested scope.

## Workflow

- Inspect the documented declaration, annotations, implementation, and relevant inherited contract. Update stale comments when they conflict with behavior.
- Document useful contracts and non-obvious behavior. Skip trivial accessors and constructors; use inherited documentation when an override preserves its contract.
- Keep nullability statements aligned with actual behavior. An annotation alone does not prove that null is checked or that a particular exception is thrown.
- Include parameters, returns, type parameters, and meaningful checked or unchecked exceptions where applicable. Do not list every possible runtime exception.
- Write a concise, complete first sentence that accurately summarizes the element. Prefer direct active wording; use code and link tags where they clarify identifiers or references.
- Keep comments compact and preserve surrounding code formatting.

## Scope

Add or update comments only for the requested declarations or meaningful contract changes. Do not document methods merely because a Java file was touched. Do not add or run tests unless the user asks for testing or verification.
