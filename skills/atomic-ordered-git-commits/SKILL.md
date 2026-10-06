---
name: atomic-ordered-git-commits
description: Plan, review, or create small, dependency-ordered Git commits with clear messages. Use when the user asks to commit, split changes into commits, or review a commit plan or range, especially when the working tree mixes several concerns.
---

# Atomic Ordered Git Commits

Owns commit planning, staging, commit messages, and commit-plan review. It does not own implementation changes; do not edit source files to make a commit work without asking.

## Settings

Resolve each setting from, highest first: the current request; an `atomic-ordered-git-commits` entry under `Skill settings` in the project's AGENTS.md or CLAUDE.md; project tooling (commitlint, commit templates, hooks); the defaults below.

- `message-format`: `auto` — match the convention in recent `git log`; fall back to Conventional Commits. Or `conventional`, `plain`.
- `verify`: `on-request` — run checks only when asked. Or `each-commit` (build/test with only that commit's changes applied), `final` (once after the last commit).
- `confirm-plan`: `when-ambiguous` — a direct commit request authorizes execution; stop for confirmation only if the scope is unclear. Or `always`.

## Plan

1. Inspect `git status`, staged, unstaged, and untracked changes. Leave unrelated or pre-existing work untouched and say so.
2. Group changes into commits that each do one logical thing and can be reverted on their own.
3. Order foundations before consumers: types, interfaces, exceptions, schema/migrations → core logic → integration points (controllers, wiring, config) → follow-ups. Keep tests and docs with the change they cover.
4. Keep separate: refactors vs. behavior changes, formatting-only changes, and file renames/moves (commit a move before editing the moved file so history follows it).
5. Keep together: generated files and lockfiles with the change that produced them.
6. Flag anything that should not be committed: secrets, credentials, local config, build output, large binaries.

For each commit, report: message, exact files or hunks, what it depends on, and how to verify it. Aim for every commit to compile; call out any commit that cannot.

## Messages

- Subject: imperative mood, ≤ 72 characters (aim for 50), no trailing period. Conventional form: `type(scope): summary`, with `type` from `feat`, `fix`, `refactor`, `test`, `docs`, `build`, `ci`, `chore`, `perf`, `style`.
- Body (when the why is not obvious): blank line after the subject, wrapped at 72, explains why and any side effects rather than restating the diff.
- Footer: `BREAKING CHANGE:` notes or `!` after the type for incompatible changes; issue references and required trailers per project or agent configuration.

## Execute

- A plan-only or review request authorizes no staging or commits.
- Recheck that the working tree still matches the plan before staging.
- Stage explicit paths only; never `git add .`, `git add -A`, or `git commit -a`. To stage part of a file non-interactively, write the wanted hunks to a patch and run `git apply --cached <patch>`; check the result with `git diff --cached`.
- Commit in the planned order. Never skip hooks (`--no-verify`). If a hook fails, fix the cause or report it, then create a new commit; re-stage files a formatter hook rewrote. Do not amend, rebase, or rewrite existing commits unless asked.
- Do not push unless asked.
- Finish with `git log --oneline -n <count>` and `git status`. Report each commit, any checks run and their results, and any changes left uncommitted.

## Review

When reviewing a plan or commit range, report commits that mix concerns, depend on later commits, would not build alone, or have unclear messages. Do not modify history.
