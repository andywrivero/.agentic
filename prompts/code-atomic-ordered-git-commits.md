# Atomic Ordered Git Commit Prompts

Copy one template, fill in the brackets, and paste it. Each one names its skill so the skill loads.

## Plan only

Use the atomic-ordered-git-commits skill to plan commits for [all current changes / these paths]. For each commit, list the message, files or hunks, and dependencies. Do not stage or commit.

## Commit current changes

Use the atomic-ordered-git-commits skill to commit [all current changes / these paths] as dependency-ordered commits. Report the commits and anything left uncommitted.

## Execute an approved plan

Use the atomic-ordered-git-commits skill to execute the plan above exactly as approved. Stop and ask if the working tree no longer matches it.

## Review only

Use the atomic-ordered-git-commits skill to review [plan / commit range, e.g. main..HEAD] for atomicity, dependency order, and message quality. Do not modify history. Report findings as: commit, problem, suggested fix.
