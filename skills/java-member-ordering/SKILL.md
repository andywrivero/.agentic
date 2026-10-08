---
name: java-member-ordering
description: Place new or changed members in Java classes, interfaces, enums, and records in a consistent order, or reorder a type when explicitly asked. Use when writing a new Java type, adding members to one, or reviewing member order.
---

# Java Member Ordering

Owns where members sit inside a Java type. It moves existing members only when a reorder is requested; for ordinary edits, place new or changed members correctly and leave the rest alone.

## Settings

Resolve each setting from, highest first: the current request; a `java-member-ordering` entry under `Skill settings` in the project's AGENTS.md or CLAUDE.md; project tooling (Checkstyle `DeclarationOrder`, IDE arrangement rules in `.idea/codeStyles` or `.editorconfig`); the defaults below.

- `method-grouping`: `visibility` — public, then protected, then package-private, then private. Or `functional` (group related methods together regardless of visibility, as in the Oracle conventions).
- `overrides`: `last` — `@Override` methods close their visibility group. Or `inline` (treat them as ordinary methods).
- `local-consistency`: `follow-file` — when a narrow edit lands in a file that consistently uses another order, match the file. Or `follow-skill`.

## Class order

1. Constants (`static final`).
2. Other static fields and static initializer blocks.
3. Instance fields and instance initializer blocks.
4. Constructors, then static factory methods.
5. Non-private methods, grouped per `method-grouping`.
6. Private methods, in call order: a helper follows the first method that calls it; shared low-level utilities go last.
7. Nested types (static nested classes, inner classes, interfaces, enums), each ordered by the same rules.

Within each field group, order by visibility (public → private) unless the file groups related fields together. Keep overloads adjacent, ordered by parameter count; with `method-grouping: visibility`, a visibility difference outranks adjacency. With `overrides: last`, put `Object` overrides (`equals`, `hashCode`, `toString`) at the very end of the group. Static methods follow the same visibility groups as instance methods.

Start the first member on the line right after the type's opening brace, with no blank line between them; this applies to every type kind, including nested types. Use one blank line between members; related fields may sit together. Do not add section-marker comments.

## Other type kinds

- Interfaces: constants, abstract methods, default methods, static methods, private methods (Java 9+), nested types. Keep overloads adjacent.
- Enums: constants first (required by the language), then the class order from step 1.
- Records (Java 16+): static fields, compact or canonical constructor, other constructors, static factories, methods, nested types.
- Lombok: annotation-generated members have no position; treat explicit `@Builder` constructors as constructors.

## Reordering

When a full reorder is requested, move members without changing bodies, signatures, modifiers, annotations, Javadoc, or comments attached to them. Keep each member's leading comment with it. Do not fix issues noticed during the move; report them separately. Keep the diff to the requested type.

See [references/example.md](references/example.md) for a worked example of the default order.
