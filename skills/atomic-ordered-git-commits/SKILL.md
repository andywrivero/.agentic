---
name: atomic-ordered-git-commits
description: Splits working-tree changes into small, atomic, dependency-ordered commits (foundations before consumers, e.g. a new exception/interface before the code that throws/implements it) instead of one large commit, verifying the build and tests pass at every individual commit step. Use whenever the user asks to commit changes that mix multiple concerns (new types plus their callers, a fix plus a refactor, several unrelated files), not only when they explicitly ask for "atomic commits" - also use when reviewing whether a proposed commit plan is properly ordered and sliced before executing it.
---

# Skill: Atomic & Dependency-Ordered Git Commits

## Description
Analyzes unstaged/staged working tree changes, constructs a dependency graph (AST/type hierarchy), breaks changes into granular atomic units, and executes commits in strict bottom-up dependency order.

## Objectives
1. Order commits so that dependencies (e.g., interfaces, base classes, custom exceptions) are committed BEFORE dependent consumers (e.g., caller methods, routes, UI).
2. Ensure every commit represents a single logical unit of work (Atomic).
3. Ensure the project builds and unit tests pass at EVERY individual commit step.
4. Facilitate non-destructive git rollbacks (`git revert`) without breaking unrelated code.

---

## Workflow Protocol

### Step 1: Diff & Dependency Analysis
1. Execute `git status` and `git diff` to view the full scope of modified/untracked files.
2. Build a topological dependency graph across changed files:
   - **Order 1 (Foundations):** Custom Exception definitions, Domain Entities, Types/Interfaces, Database Migrations.
   - **Order 2 (Core Logic):** Utility functions, DAO methods, core business services implementing Order 1.
   - **Order 3 (Integration):** REST controllers, API routes, event handlers consuming Order 2 logic.
   - **Order 4 (Tests & Documentation):** Unit/integration tests, documentation updates referencing Order 1–3.

### Step 2: Atomic Grouping & Slicing
- Group modified lines into discrete atomic clusters.
- **Rule:** If a single file contains both a new base class/exception AND a caller method, use `git add -p` (patch mode) or split the file edits into separate staging passes.
- **Rule:** Never combine refactoring changes with new feature additions in the same commit.

### Step 3: Verification & Interactive Staging
For each atomic group $G_n$ in dependency order ($n = 1 \dots N$):
1. **Stage:** Stage only the specific files or hunks for group $G_n$ using `git add <file>`. Do NOT use `git add .`.
2. **Compile Check:** Run the compiler/linter on the staged workspace (`npm run build`, `mvn compile`, `go build`, etc.).
3. **Test Check:** Run relevant unit tests to guarantee $G_n$ does not break existing functionality.
4. **Commit Execution:** Execute commit using Conventional Commit standards:
   - Format: `<type>(<scope>): <short summary in imperative mood>`
   - Example 1: `feat(auth): introduce InvalidTokenException class`
   - Example 2: `feat(auth): throw InvalidTokenException in TokenValidator`
   - Example 3: `fix(api): catch InvalidTokenException in AuthController`

### Step 4: Final Validation
1. Verify the linear history: `git log --oneline -n <N>`
2. Confirm working tree cleanliness: `git status`

---

## Safety Rules & Constraints
- **NEVER** use `git add .` or `git add -A`.
- **NEVER** commit broken builds or failing unit test states.
- If a hook fails, resolve the issue and commit again—do NOT amend prior commits unless explicitly directed.
- Always present the proposed commit execution graph to the user for confirmation prior to executing the `git commit` loop.
