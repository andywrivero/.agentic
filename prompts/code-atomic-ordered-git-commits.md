# Atomic Ordered Git Commit Prompts

Use the atomic-ordered-git-commits skill for commit planning or execution. Never stage everything at once.

## Plan only

Plan dependency-ordered commits for the current changes. List the scope and exact files or hunks per commit; do not stage or commit.

## Execute

Execute the approved plan [reference plan], or commit the current requested scope in dependency order. Stage only the relevant files or hunks and report the commits and remaining changes.

## Review only

Review [plan/commit range] for atomicity and dependency order. Do not stage, rewrite, amend, or create commits; report actionable findings.
