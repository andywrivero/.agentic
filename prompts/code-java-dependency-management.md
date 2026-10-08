# Java Dependency Management Prompts

Copy one template, fill in the brackets, and paste it. Each one names its skill so the skill loads.

## Add a dependency

Use the java-dependency-management skill to add [library] for [purpose] to [module]. Propose the coordinates, version, and scope first, and check whether something already on the classpath covers the need.

## Upgrade

Use the java-dependency-management skill to upgrade [library/BOM] to [version or "the latest compatible"]. Summarize breaking changes from the release notes, compare the dependency tree before and after, and run the build.

## Resolve a conflict

Use the java-dependency-management skill to resolve [NoSuchMethodError / enforcer failure / conflicting versions of X]. Show the dependency tree evidence, then fix it in the preferred order: align, upgrade, and exclude only as a last resort.

## Audit only

Use the java-dependency-management skill to audit [module/project] for conflicts, unused or undeclared dependencies, unpinned versions, and known vulnerabilities. Do not edit. Report findings as: dependency, issue, fix.
