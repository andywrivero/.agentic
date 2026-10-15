#!/usr/bin/env python3
"""PreToolUse guard for the read-only specialist agents.

Used by explore, tests, debug, review, and api-design. Those agents need Bash
for search, git inspection, diagnostics, and running builds/tests, but must not
modify files or repository state. This hook blocks Bash commands that would.

It is a guardrail against accidental or "helpful" edits, not a security
sandbox: a determined command (for example one hidden inside `sh -c '...'`)
can get past it.

Exit 0 lets the command continue to the normal permission flow.
Exit 2 blocks it and sends the reason on stderr back to the agent.
"""
import json
import re
import sys

# Where a new command can begin: start of input, after a separator or opening
# token, after `find -exec`, after shell keywords, and after prefixes such as
# sudo/xargs/env (with their flags) or leading VAR=value assignments.
CMD_START = (
    r"(?:^|[;&|(`{!\n]|\$\(|-exec(?:dir)?\s)\s*"
    r"(?:(?:sudo|xargs|env|time|nohup|command|exec|then|do|else)\s+"
    r"(?:-\S+\s+(?:[^\s;&|-]\S*\s+)?)*)*"
    r"(?:\w+=\S*\s+)*"
)
# Arguments before a flag, staying inside one command segment.
ARGS = r"(?:[^\s;&|]+\s+)*?"
GIT = CMD_START + r"git\s+(?:-[Cc]\s+\S+\s+)*"

RULES = [
    (CMD_START + r"(?:rm|rmdir|mv|cp|touch|mkdir|ln|chmod|chown|truncate|dd|tee|install|patch|unlink|shred)(?=\s|$|;|&|\|)",
     "file-modifying command"),
    (CMD_START + r"find\b[^;&|]*\s-delete\b", "find -delete"),
    (CMD_START + r"sed\s+" + ARGS + r"(?:-[a-zA-Z]*i[a-zA-Z]*(?:\.\S*)?(?=\s|$)|--in-place)",
     "in-place sed edit"),
    (CMD_START + r"perl\s+" + ARGS + r"-[a-zA-Z]*i[a-zA-Z]*(?:\.\S*)?(?=\s|$)",
     "in-place perl edit"),
    (GIT + r"(?:add|am|apply|checkout|cherry-pick|clean|commit|merge|mv|pull|push|rebase|reset|restore|revert|rm|switch|worktree|update-ref|gc|prune|init)\b",
     "git command that changes the repository or working tree"),
    (GIT + r"stash(?!\s+(?:list|show)\b)", "git stash"),
    (GIT + r"branch\s+" + ARGS + r"-(?:[dDmMcC]\b|-delete\b|-move\b|-copy\b)",
     "git branch change"),
    (r"\s--(?:fix|write)(?=\s|$|=)"
     r"|\bspotless(?:Apply|:apply)\b|\bformatter:format\b|\brewrite:run\b"
     r"|\bversions:(?:set|use-|update-)"
     r"|\b(?:gofmt|goimports)\s+" + ARGS + r"-w\b",
     "formatter or tool that rewrites source files"),
]
RULES = [(re.compile(pattern), reason) for pattern, reason in RULES]

QUOTED = re.compile(r"'[^']*'|\"(?:[^\"\\]|\\.)*\"")
# An output redirection and its target; `2>&1`-style fd duplication is skipped.
REDIRECT = re.compile(r"(?<![<>=-])(?:&|\d+)?>>?\|?(?!&)\s*([^\s;&|()<>]*)")
ALLOWED_REDIRECT_TARGETS = (
    "/dev/null", "/dev/stdout", "/dev/stderr",
    "/tmp/", "/private/tmp/", "/var/folders/", "$TMPDIR", "${TMPDIR}",
)


def find_violation(command):
    for pattern, reason in RULES:
        if pattern.search(command):
            return reason
    # Drop the quotes but keep the text, minus any < or > inside it, so
    # `grep "a > b"` is not a redirect while `> "/tmp/x.log"` keeps its target.
    unquoted = QUOTED.sub(
        lambda m: m.group(0)[1:-1].replace(">", " ").replace("<", " "), command)
    for match in REDIRECT.finditer(unquoted):
        target = match.group(1)
        if not target.startswith(ALLOWED_REDIRECT_TARGETS):
            return "output redirection into a file (" + (target or "no target") + ")"
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        print("Read-only guard could not parse the hook input; command blocked.",
              file=sys.stderr)
        return 2
    command = (payload.get("tool_input") or {}).get("command")
    if not isinstance(command, str):
        return 0
    reason = find_violation(command)
    if reason is None:
        return 0
    print(
        "Blocked by the read-only guard (" + reason + "). This specialist must not "
        "modify files or repository state. If a change or extra instrumentation is "
        "needed, describe it in your findings for the main orchestrator. To keep "
        "command output, pipe it (| tail, | grep) or redirect it under /tmp.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
