---
name: java-dependency-management
description: Add, upgrade, remove, and diagnose Maven or Gradle dependencies: version management (BOMs, dependencyManagement, version catalogs), scopes, version conflicts, unused or undeclared dependencies, and known vulnerabilities. Use when a change touches pom.xml, build.gradle(.kts), libs.versions.toml, or dependency versions, or when a classpath error (NoSuchMethodError, ClassNotFoundException) points to a version conflict.
---

# Java Dependency Management

Owns how dependencies are declared, versioned, scoped, and verified in Maven and Gradle builds. It does not own whether a new library or framework belongs in the design (`spec-architecture-verification`), Java 8 compatibility of a library (`java8-pro`), or diagnosing a failure before it is known to be a dependency problem (`systematic-debugging`).

## Settings

Resolve each setting from, highest first: the current request; a `java-dependency-management` entry under `Skill settings` in the project's AGENTS.md or CLAUDE.md; the build's own conventions; the defaults below.

- `new-dependency`: `ask` — propose a new dependency (coordinates, version, scope, why) and wait for approval. Or `allow` (add it, and report it).
- `vuln-check`: `if-configured` — run a vulnerability scan only when the build already has one (OWASP dependency-check, a Gradle plugin, Snyk). Or `always` (suggest how to run one if none exists), `off`.
- `verify`: `after-edit` — after changing the build, run the build and tests and compare the dependency tree. Or `on-request`.

## Read the build first

- Use the wrapper (`./mvnw`, `./gradlew`) if there is one, so the build tool version matches the project.
- Find where versions live: Maven `<properties>`, `<dependencyManagement>`, the parent POM, and imported BOMs (`<scope>import</scope>`); Gradle version catalogs (`gradle/libs.versions.toml`), `platform(...)`, and convention plugins in `buildSrc` or `build-logic`. In multi-module builds, find the module that owns the shared versions.
- Note the Java target, then defer library compatibility to `java8-pro` when it is 8.

## Add or upgrade

- **Before adding:** check whether the JDK, an existing dependency, or a project utility already covers the need. Check whether the library is already on the classpath transitively; if code uses it directly, declare it explicitly instead of relying on the transitive copy.
- **Coordinates:** copy exact `groupId:artifactId` from the project's official docs or Maven Central. Watch for look-alike names, relocated artifacts (`javax` → `jakarta`), and classifiers.
- **Versions:**
  - Pin an exact, released version. No `SNAPSHOT` outside your own modules, no ranges (`[1.0,)`), no `+` or `latest.release`.
  - Declare the version once, where the project keeps versions: a property, `dependencyManagement`, or the version catalog.
  - If a BOM manages a family (Spring, Jackson, JUnit, Netty), upgrade the BOM and leave the individual artifacts unversioned.
- **Scopes:**
  - Maven: `compile`, `provided` (supplied by the container), `runtime` (needed only to run), `test`.
  - Gradle: `implementation`, `api` (only when the type appears in the module's public API), `compileOnly`, `runtimeOnly`, `testImplementation`.
- **Upgrades:** read the release notes for breaking changes, especially on major versions. Compare the tree before and after, because an upgrade can change transitive versions.

## Resolve conflicts

- Maven picks the version *nearest* the root, even when it is older; Gradle picks the *highest*. Both can produce `NoSuchMethodError` at runtime.
- Diagnose with:
  - Maven: `mvn dependency:tree -Dverbose -Dincludes=<group>:<artifact>`. The output shows `omitted for conflict with …`.
  - Gradle: `./gradlew dependencyInsight --dependency <name> --configuration runtimeClasspath`.
  - If the build has Maven Enforcer, run `mvn enforcer:enforce -Denforcer.rules=requireUpperBoundDeps` or `dependencyConvergence`.
- **Fixes, in order of preference:**
  1. Align the version through a BOM or `dependencyManagement`, or a Gradle `platform` or constraint.
  2. Upgrade the direct dependency that drags in the old version.
  3. Use an `<exclusion>`, last, with a comment explaining why.
- Never fix a conflict by copying classes, shading by hand, or reordering dependencies until it happens to work.

## Clean up

- `mvn dependency:analyze` lists *used undeclared* dependencies (declare them) and *unused declared* ones (candidates for removal).
- Before removing anything it calls unused, confirm nothing loads it at runtime: reflection, `ServiceLoader`, JDBC drivers, logging bindings, annotation processors.

## Vulnerabilities

- Per `vuln-check`, run the project's scanner, for example `mvn org.owasp:dependency-check-maven:check` or `./gradlew dependencyCheckAnalyze`. Note that the OWASP scanner needs an NVD download, which is slow without an API key.
- Fix a finding by upgrading to a patched version through the managed location. If no patched version exists, report the finding and whether the vulnerable code path is reachable. Never suppress a finding without approval.

## Never

- Add a repository, disable checksum or TLS verification, or edit `~/.m2/settings.xml` or `~/.gradle/gradle.properties` without asking.
- Put credentials or tokens in build files.
- Leave the build unverified: when `verify` is active, run `./mvnw -q verify` or `./gradlew build` and report the command, its result, and any tree changes.

See [references/example.md](references/example.md) for a worked conflict.
