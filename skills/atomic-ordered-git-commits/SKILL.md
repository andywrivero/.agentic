---
name: atomic-ordered-git-commits
description: Plan or create small, dependency-ordered Git commits when the user requests commit work, especially when changes contain multiple concerns.
---

# Atomic Ordered Git Commits

Owns commit planning and Git staging/commit operations. It does not own implementation changes. Use only when the user asks to plan, review, or create commits.

## Plan

- Inspect status and relevant staged, unstaged, and untracked changes. Do not disturb unrelated work.
- Group changes into coherent commits, order dependencies before consumers, and keep unrelated refactors separate. Keep tests and documentation with the change when that makes a coherent commit.
- For each commit, state its scope, exact files or hunks, dependencies, and practical verification.
- A plan-only request authorizes no staging or commits. A direct request to commit authorizes the requested commit work; ask only if scope materially differs or an unresolved concrete issue prevents safe execution.

## Execute

- Recheck that the working tree still matches the authorized scope.
- Stage only approved files or hunks. Never use git add . or git add -A.
- Use the agreed commit order and message format. Do not amend prior commits unless explicitly requested.
- Run checks only when the user asks for testing or verification. Report failures and unrun checks accurately.
- After committing, report the commits and resulting working-tree status. Do not promise a clean tree if unrelated changes remain.
