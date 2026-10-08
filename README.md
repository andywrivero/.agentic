# Agentic skills and prompts

- `skills/` — agent skills, symlinked into `~/.claude/skills/`. Each `SKILL.md` stays short; bulky reference material lives in its `references/` folder and loads only when needed.
- `prompts/` — copy-paste templates for chat sessions. Each template names its skill so the skill loads.

## Customizing skill settings

Each skill has a **Settings** section with defaults. Override them per project by adding a block to the project's `AGENTS.md` or `CLAUDE.md`:

```markdown
## Skill settings

- atomic-ordered-git-commits: message-format=conventional, verify=each-commit
- auto-simplify: verify=after-edit
- java-code-style: line-length=120, verify=after-edit
- java-member-ordering: method-grouping=functional
- java8-pro: exception-wrapper=com.example.error.ServiceException
- javadoc: visibility=api, unchecked-marker=on
- spec-architecture-verification: checkpoint=always, verify=after-edit
- tdd-loop: run-scope=full, commit=per-cycle
```

Precedence, highest first: the current chat request → this block → project tooling config (commitlint, Checkstyle, formatter, build files) → skill defaults. To override one setting for a single request, say so in the prompt, e.g. "…and run the tests after each commit."
