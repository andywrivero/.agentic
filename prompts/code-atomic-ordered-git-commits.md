# Atomic Ordered Git Commit Prompts

Use these prompts with the existing `atomic-ordered-git-commits` skill. Never stage everything with `git add .` or `git add -A`.

## 1. Plan Atomic, Dependency-Ordered Commits

Analyze the current working tree and propose a small, atomic commit sequence in dependency order. Do not stage or commit anything yet.

- Apply the `atomic-ordered-git-commits` skill. Inspect `git status` and the relevant staged, unstaged, and untracked changes.
- Build a dependency graph across changed files and hunks, placing foundations before consumers and keeping refactors separate from feature work.
- For each proposed commit, list its logical scope, exact files or hunks, dependency rationale, and the build/test checks required.
- Present the complete graph and plan, then wait for explicit user confirmation before staging or committing.
- Call out unrelated changes and keep them untouched.

## 2. Execute an Approved Commit Plan

Execute the previously approved atomic commit plan: **[refer to the approved sequence]**.

- Apply the `atomic-ordered-git-commits` skill. Recheck the working tree and confirm the approved plan still matches the changes; if it does not, stop and present a revised plan for confirmation.
- Stage only the approved files or hunks for the current commit. Never use `git add .` or `git add -A`; split mixed-purpose file changes into separate staging passes when needed.
- For each dependency-ordered commit, run the relevant compile/build and tests before committing. Do not commit a failing state; stop and report the failure if it cannot be resolved within the approved scope.
- Use the approved Conventional Commit format. Do not amend earlier commits unless explicitly directed, and do not disturb unrelated changes.
- After the sequence, verify the resulting history and working tree, then summarize commits and checks.

## 3. Review a Commit Sequence

Review **[identify the proposed commit plan or existing commit range]** for atomicity, dependency order, and verification coverage. Do not stage or commit changes.

- Apply the `atomic-ordered-git-commits` skill and inspect the relevant diffs and commit history.
- Identify commits that mix concerns, depend on later commits, combine foundations with consumers, or omit required build/test verification.
- Report actionable findings first with commit/file references, impact, and a suggested ordering or split.
- Preserve the working tree; do not stage, rewrite, amend, or create commits.
- If the sequence is sound, state that clearly and note any verification gaps or assumptions.