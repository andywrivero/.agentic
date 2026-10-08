---
name: spec-architecture-verification
description: Analyze the spec and the system's design (component boundaries, dependency direction, domain model, API contracts) before writing code, then verify the change against them, to prevent architectural drift and unintended coupling. Use before implementing a feature or change that adds types, packages, modules, or dependencies, changes a public API or schema, or touches more than one component; also when reviewing a change for design fit. Not for edits confined to one method body.
---

# Spec and Architecture Verification

Owns the design check around a change: what the spec requires, where the change belongs, which boundaries and contracts it touches, and whether the result still fits. It does not own code-level formatting and naming (`java-code-style`), member order (`java-member-ordering`), Javadoc wording (`javadoc`), Java 8 compatibility of APIs and dependencies (`java8-pro`), or behavior-preserving cleanup (`auto-simplify`).

## Settings

Resolve each setting from, highest first: the current request; a `spec-architecture-verification` entry under `Skill settings` in the project's AGENTS.md or CLAUDE.md; project architecture docs and tooling (ADRs, ArchUnit tests, Maven enforcer, `module-info.java`, Checkstyle `ImportControl`); the defaults below.

- `depth`: `proportional` — no note for edits confined to one method or private member that change no contract; a few lines for changes inside one component; the full analysis for new types, packages, modules, dependencies, public API, or anything crossing components. Or `full` (always the full analysis).
- `checkpoint`: `on-drift` — continue after the analysis unless the plan trips a drift rule below; then stop and ask. Or `always` (present the design note and wait for approval before writing code), `never` (proceed and report drift at the end).
- `verify`: `on-request` — run architecture checks only when asked. Or `after-edit` (run the project's ArchUnit tests, `jdeps`, or enforcer rules after editing).

## 1. Pin down the spec

- Read, in order of authority: the request; specs and decisions in the repo (`docs/`, ADRs, architecture notes, AGENTS.md or CLAUDE.md); contracts (OpenAPI or AsyncAPI files, protobuf or GraphQL schemas, public interfaces, published DTOs, events, DB migrations); tests that pin current behavior.
- Restate the request as acceptance criteria. List what is ambiguous as questions instead of guessing.
- If the request contradicts a spec, contract, or ADR, stop and ask which one wins.

## 2. Map the architecture the change touches

Base each point on files, not assumptions, and name the file that shows it. Map only what the change touches.

- **Components:** build modules (Maven modules, Gradle subprojects, JPMS modules), top-level packages, and what each one owns.
- **Dependency direction:** which components import which (`grep '^import'`, `jdeps -verbose:package`). Note cycles and violations that already exist.
- **Patterns in use:** layering (web → service → persistence), ports and adapters, and DDD building blocks (aggregates, entities, value objects, repositories, domain services, events). Also note where validation and invariants live, how errors cross layers, how objects are created (builders, factories), and where the transaction and DI boundaries are.
- **Enforced rules:** ArchUnit tests, enforcer or import-control rules, and `module-info` exports. These are hard constraints.

Where the code is inconsistent, follow the dominant pattern nearest the change and report the inconsistency.

## 3. Write the design note before coding

Keep it in the reply, not in a file, sized per `depth`:

- **Placement:** where each new or changed type goes, and why that component owns it.
- **Dependencies:** new edges between components or on libraries, and their direction.
- **Contracts:** each public API, schema, serialized form, or event that changes, and whether the change is backward compatible.
- **Patterns:** the existing example each new piece follows, and any new pattern with the reason the existing one does not fit.
- **Criteria:** each acceptance criterion, and the code and test that will satisfy it.

## Drift rules

Each of these triggers a stop under `checkpoint: on-drift`:

- **Direction:** an inner layer or the domain model starts depending on an outer one (service, web, persistence, framework, logging), or a new cycle appears between packages or modules.
- **Boundaries:** code reaches into another component's internals instead of its public API (exported packages, interfaces, facades). Visibility is widened (package-private to public, unexported to exported) just to make a cross-component call compile.
- **Domain:** an invariant the model enforces is duplicated in or moved to a service or controller, or an aggregate is changed other than through its root. Mutable internal collections are exposed, or an aggregate holds another aggregate by object where the project uses ids.
- **Contracts:** a published API, schema, serialized form, or event changes incompatibly (removed or renamed members, new required inputs, narrowed outputs, changed error types) without versioning or explicit approval. Prefer additive changes.
- **Leakage:** persistence entities, framework types, or another layer's exceptions cross a boundary the project maps or translates at.
- **New machinery:** a new framework, layer, abstraction, or pattern is added where an existing one would serve, or "for later".
- **Shared code:** a shared utility package starts depending on domain or service code.

## 4. Verify after writing

- Check every import the change added against the dependency map. Run the checks in `verify` and report the command and its result, or say none were run.
- Walk each acceptance criterion and point to the code and test that meet it. Report gaps.
- Report deviations from the design note, and drift you found but left alone because it was out of scope.

For reviews, do not edit. Report findings as: file:line, rule, risk, suggested fix.

See [references/example.md](references/example.md) for a worked design note.
