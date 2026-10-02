# Java Member-Ordering Prompts

Use these prompts with the existing `java-member-ordering` skill whenever creating or touching Java types.

## 1. Reorder an Existing Java Type

Reorder members in **[identify the Java file or type]** to comply with the `java-member-ordering` skill.

- First inspect the full type and relevant project conventions.
- Make a structural-only change: preserve each member's body, signature, modifiers, annotations, and behavior. Do not silently fix unrelated bugs.
- Apply the skill's order: constants, mutable static fields and static initializers, instance fields, constructors and static factories, public/protected methods, private helpers in call-flow order, then nested types.
- Keep overrides at the end of the public/protected section, overloads adjacent, and related members readable. Do not add section-marker comments.
- Account for interface and enum-specific ordering, and apply the same rules inside nested types.
- Run the narrowest relevant tests or compile check and report the structural changes and verification.

## 2. Add or Change a Java Member

Make this change to **[identify the Java type]**: **[describe the requested member change]**.

- Apply the `java-member-ordering` skill to the entire touched type, not only the new member.
- Place fields above constructors and methods; keep all public/protected members before private helpers. Keep overloads adjacent and put private helpers in logical call-flow order.
- Preserve existing behavior and public contracts except where the requested change requires otherwise. Avoid unrelated reordering or cleanup.
- If adding a nested type, place it after all methods and order its own members by the same convention. Handle interfaces and enums according to their language-specific ordering.
- Run focused tests or compilation checks and summarize what changed.

## 3. Create a Java Type with Ordered Members

Create **[class, interface, or enum name]** to **[describe its responsibility and expected API]**.

- Follow the existing project conventions and the `java-member-ordering` skill from the start.
- For a class, order constants, mutable static fields/initializers, instance fields, constructors/factories, public/protected methods, private helpers, then nested types.
- For an interface, order constants, abstract/default/static methods, then nested types. For an enum, put enum constants first, then follow the normal class ordering for its remaining members.
- Keep overloads adjacent, overrides at the end of the public/protected section, and private helpers in call-flow order. Do not add section-marker comments.
- Add only the necessary implementation and focused tests; run the project's relevant test or compile check and report the result.
