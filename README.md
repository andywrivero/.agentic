# Agentic skills, prompts, and agents

Shared skills and prompts, plus per-tool agent setups for Claude Code, Codex, and GitHub Copilot.

- `skills/` — agent skills shared by every tool. Each `SKILL.md` stays short; bulky reference material lives in its `references/` folder and loads only when needed.
- `prompts/` — copy-paste templates for chat sessions. Each template names its skill so the skill loads. Reference only; not installed.
- `claude/` — `agents/` (subagent definitions), `hooks/` (the read-only Bash guard those agents use), and `rules/` (global instructions; every rule without a `paths:` field loads in every project).
- `codex/` — `agents/` (subagent profiles), `AGENTS.md` (the shared subagent workflow), and `config.toml` (the `[agents]` settings to merge).
- `copilot/` — `agents/`: `main` plus six specialists. Each agent file is self-contained.

The six specialist roles mean the same thing in every tool: `explore`, `review`, `docs`, `tests`, and `debug` never edit files; `api-design` writes only a design document at a path the main agent delegates. The main agent makes every other change.

## Install

Run `./install.sh`. It symlinks each file into place, creating folders as needed and replacing anything already at a destination. Rerun it after adding, renaming, or removing files; it also removes links to files that no longer exist.

| Source | Linked into |
| --- | --- |
| `skills/*` | `~/.claude/skills/`, `~/.codex/skills/`, `~/.agents/skills/` (Copilot reads skills from here) |
| `claude/agents/*.md` | `~/.claude/agents/` |
| `claude/hooks/*` | `~/.claude/hooks/` |
| `claude/rules/*.md` | `~/.claude/rules/` |
| `codex/agents/*.toml` | `~/.codex/agents/` |
| `copilot/agents/*.agent.md` | `~/.copilot/agents/` |

Merge these by hand, because the global files also hold machine-specific settings:

- `codex/AGENTS.md` → `~/.codex/AGENTS.md`: replace any older subagent section with this one and keep the file's other instructions.
- `codex/config.toml` → `~/.codex/config.toml`: update the keys in the existing `[agents]` table; don't add a second `[agents]` header. Keep the machine's `model` and `model_reasoning_effort`; the commented lines only record the recommended baseline.

## Customizing skill settings

Each skill has a **Settings** section with defaults. Override them per project by adding a block to the project's `AGENTS.md` or `CLAUDE.md`:

```markdown
## Skill settings

- atomic-ordered-git-commits: message-format=conventional, verify=each-commit
- auto-simplify: verify=after-edit
- java-code-style: line-length=120, verify=after-edit
- java-dependency-management: new-dependency=allow, vuln-check=always
- java-logging-exceptions: framework=slf4j, message-style=sentence
- java-member-ordering: method-grouping=functional
- java8-pro: exception-wrapper=com.example.error.ServiceException
- javadoc: visibility=api, unchecked-marker=on
- spec-architecture-verification: checkpoint=always, verify=after-edit
- systematic-debugging: fix=never, max-hypotheses=5
- tdd-loop: run-scope=full, commit=per-cycle
- test-backfill: mutation-check=all, on-bug=add-failing
```

Precedence, highest first: the current chat request → this block → project tooling config (commitlint, Checkstyle, formatter, build files) → skill defaults. To override one setting for a single request, say so in the prompt, e.g. "…and run the tests after each commit."
