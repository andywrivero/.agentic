#!/usr/bin/env bash
# Links this repo's skills, agents, Claude hooks, and Claude rules into each
# tool's home directory, creating folders as needed. Each file gets its own
# symlink; anything already at a destination is replaced. Safe to rerun after
# adding, renaming, or removing files. Copilot reads skills from ~/.agents/skills.
#
# Claude loads every ~/.claude/rules/*.md without a paths: field in every project,
# so global Claude instructions go in claude/rules/ rather than a CLAUDE.md.
#
# Merge these into the global files by hand: codex/AGENTS.md and
# codex/config.toml. prompts/ is reference only and is not installed.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Replaces DEST with a symlink to SRC, unless it already is one.
link() {
    local src="$1" dest="$2"
    if [ "$(readlink "$dest" 2>/dev/null)" = "$src" ]; then
        return
    fi
    rm -rf "$dest"
    ln -s "$src" "$dest"
    echo "linked $dest"
}

# Removes links in DIR that point into this repo but no longer resolve.
prune() {
    local dir="$1" entry
    for entry in "$dir"/*; do
        if [ -L "$entry" ] && [ ! -e "$entry" ]; then
            case "$(readlink "$entry")" in
                "$REPO"/*) rm "$entry" && echo "removed dead link $entry" ;;
            esac
        fi
    done
}

# Links each SRC into DIR under its own name, after pruning DIR.
link_into() {
    local dir="$1" src
    shift
    mkdir -p "$dir"
    prune "$dir"
    for src in "$@"; do
        if [ -e "$src" ]; then
            link "$src" "$dir/$(basename "$src")"
        fi
    done
}

# Skills are shared by every tool.
for dir in "$HOME/.claude/skills" "$HOME/.codex/skills" "$HOME/.agents/skills"; do
    link_into "$dir" "$REPO"/skills/*
done

link_into "$HOME/.claude/agents" "$REPO"/claude/agents/*.md
link_into "$HOME/.claude/hooks" "$REPO"/claude/hooks/*
link_into "$HOME/.claude/rules" "$REPO"/claude/rules/*.md

link_into "$HOME/.codex/agents" "$REPO"/codex/agents/*.toml

link_into "$HOME/.copilot/agents" "$REPO"/copilot/agents/*.agent.md
