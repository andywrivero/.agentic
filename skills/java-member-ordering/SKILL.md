---
name: java-member-ordering
description: Place new or changed members consistently in a Java type, or perform a structural reorder when explicitly requested. Preserve member behavior and avoid unrelated cleanup.
---

# Java Member Ordering

Owns the placement of members in Java classes, interfaces, and enums. It performs structural moves only when a reorder is requested; for a narrow code change, place changed members consistently without sweeping unrelated members.

## Class order

1. Constants (static final fields).
2. Mutable static fields and static initializer blocks.
3. Instance fields.
4. Constructors and static factories.
5. Public methods, then protected methods, then package-private methods. Within each visibility group, keep overloads adjacent, put ordinary methods first, and overrides last.
6. Private helpers, ordered by call flow.
7. Nested types, each using the same rules.

Keep fields before constructors and methods. Use one blank line between members unless related fields read better as a group. Do not add section-marker comments. If overloads have different visibility, visibility order takes precedence over adjacency.

## Interfaces and enums

- Interfaces: constants, abstract methods, default methods, static methods, then nested types. Keep overloads adjacent within each method group.
- Enums: enum constants first, then fields, constructors, methods in the class order above, and nested types.

## Reordering existing members

When a full reorder is requested, move members without changing bodies, signatures, modifiers, annotations, or behavior. Do not silently fix issues noticed during the move; report them separately. Keep the diff limited to the requested type and necessary structural moves.
