---
name: java-code-style
description: Format new or changed Java code to the house style and enforce it with lint configuration (indentation, wrapping, braces, blank lines, whitespace, imports, naming). Use when writing or changing Java code, reviewing formatting or Checkstyle findings, or setting up Checkstyle or .editorconfig. Not for reformatting untouched code.
---

# Java Code Style

Owns formatting, whitespace, imports, naming, and lint configuration for Java source. It does not own member order or spacing between members (`java-member-ordering`), Javadoc content and tags (`javadoc`), Java 8 language and API choices (`java8-pro`), or behavior-preserving cleanup (`auto-simplify`).

## Settings

Resolve each setting from, highest first: the current request; a `java-code-style` entry under `Skill settings` in the project's AGENTS.md or CLAUDE.md; project tooling (Checkstyle, Spotless, google-java-format, `.editorconfig`, `.idea/codeStyles`); the defaults below.

- `line-length`: `100`.
- `scope`: `changed` — format new and changed lines only; leave the rest of the file alone even where it deviates. Or `file` (whole files touched by the change).
- `verify`: `on-request` — run lint only when asked. Or `after-edit` (run the project's lint task on the changed files).
- `static-imports`: `first` — a static group before all other imports. Or `last`.

## Layout

- 4-space indents, no tabs, LF line endings, a final newline. No trailing whitespace, including on blank lines.
- Lines up to `line-length`; `package` and `import` lines are exempt.
- One statement and one variable declaration per line.
- Imports: no wildcards. Groups in order: static (per `static-imports`), `java.*` and `javax.*`, then everything else (project and third-party). One blank line between groups, alphabetical within each. One blank line after `package` and after the imports.

## Braces and blank lines

- K&R braces: `{` ends the line; `}` starts its own line; `} else {`, `} catch (…) {`, `} finally {` stay on one line.
- Always use braces for `if`, `else`, `for`, `while`, and `do`, even around one statement.
- Empty bodies still put `}` on its own line (`private Strings() {` then `}`), never `{}`.
- Method, constructor, lambda, and anonymous-class bodies have no blank line after `{` or before `}`. Type bodies follow `java-member-ordering`.
- Put one blank line before every block statement (`if`, `for`, `while`, `do`, `try`, `switch`, `synchronized`) unless it is the first statement of its enclosing block, such as right after a method signature.
- Put one blank line after every closing `}` of a block statement, and after a statement that wraps, unless the enclosing block closes on the next line.
- Keep runs of simple statements together. Never use two blank lines in a row.

```java
Order order = repository.findById(orderId)
                        .orElseThrow(() -> new OrderException("Unknown order: " + orderId));

if (order.getStatus().isTerminal()) {
    throw new OrderException("Order already closed: " + orderId);
}

order.setStatus(newStatus);
```

## Wrapping and whitespace

- Keep a chain on one line when it fits. When it does not, break before every `.` and align each continuation `.` under the first `.` of the chain, as above.
- Other breaks go before binary operators and after commas, with continuation lines indented 8 spaces past the statement.
- Put a space after keywords (`if (`, `for (`, `catch (`, `switch (`), around binary and ternary operators, `->`, and the enhanced-`for` `:`, and after commas and casts (`(BaseEntity) o`). No space inside parentheses or angle brackets (`Map<K, V>`), and none before a method's `(`.
- `switch`: indent `case` one level inside the switch and its statements one more; put `default` last; no blank lines between cases.
- Enums with arguments or bodies: one constant per line, `},` after a constant body, `;` after the last constant, then one blank line before the members.

## Declarations and naming

- Annotations go one per line above the modifiers.
- Modifiers follow JLS order (`public static final`, `protected abstract`, `public synchronized`). Omit redundant modifiers, such as `public`/`static`/`final` on interface constants, `public abstract` on interface methods, and `private` on enum constructors.
- Long literals use `L` (`-1L`) and float literals use `f` (`0.75f`).
- Use `this.` for field assignments in constructors, setters, and builder methods, and read fields without it.
- Constants, including a logger named `LOGGER`, are in `UPPER_SNAKE_CASE`. Type parameters are single capitals (`T`, `K`, `V`).
- Property accessors are `getX`/`isX`/`setX`. Computed values and actions are named for what they do, without `get` (`total()`, `weight()`, `describe()`). Builder methods take the property name (`priority(…)`), and the builder finishes with `build()`. Static factories have short names (`builder(…)`, `of(…)`).
- Conventional short names: `e` for caught exceptions; `o` for the `equals` parameter, with `that` for the cast.

## Lint enforcement

1. Look for project lint and formatter config first: Checkstyle (`checkstyle.xml`, `maven-checkstyle-plugin`, Gradle `checkstyle`), Spotless, google-java-format, `.editorconfig`, `.idea/codeStyles`. If it exists, it wins over the rules above. Follow it, and never hand-format against a formatter the build runs.
2. Without project config, the rules above apply. [references/checkstyle.xml](references/checkstyle.xml) enforces the mechanical ones, and [references/editorconfig](references/editorconfig) sets up editors. Blank lines after wrapped statements and naming intent need review by eye.
3. Do not add lint config, plugins, or dependencies to a project unless asked. When asked, copy the bundled files and set `line-length` in them.
4. Never silence findings (`@SuppressWarnings("checkstyle:…")`, `CHECKSTYLE:OFF`, exclusions) to make lint pass. Fix the code, or report the finding.
5. When `verify` is active, run the project's task (`mvn checkstyle:check`, `gradle checkstyleMain`, `spotlessCheck`). If there is none and a Checkstyle jar is available, run `java -jar <checkstyle-all.jar> -c <this skill>/references/checkstyle.xml <paths>`. Report the command and its result, or say that lint was not run.

## Scope

Format only what `scope` covers. Report deviations found elsewhere instead of fixing them. Reformat existing code only when asked, and keep formatting-only edits apart from behavior changes so they can be committed separately (see `atomic-ordered-git-commits`). For reviews, report findings as: file:line, rule, fix.
