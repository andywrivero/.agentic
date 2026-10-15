## Engineering Delegation

The main agent is the engineering orchestrator and retains ownership
of the overall task, implementation decisions, and final result.

Use specialized agents when they improve accuracy, reduce context
noise, or provide independent verification:

- explore: repository discovery and dependency mapping
- tests: execute approved tests/builds and report failures
- docs: retrieve authoritative external documentation
- debug: investigate failures and return ranked root-cause hypotheses
- review: independently review proposed or completed changes
- api-design: evaluate public API and compatibility tradeoffs

All specialized agents return their findings to the main orchestrator.
They do not assume ownership of the overall task or proceed into
unrelated implementation unless explicitly delegated to do so.

Use deep planning before new features, architectural changes,
meaningful design tradeoffs, public API changes, cross-module changes,
security/concurrency-sensitive changes, or after the first reasonable
bug fix fails.

Do not delegate trivial work merely to satisfy this workflow.

Investigative and review agents are read-only unless explicitly
authorized otherwise.

Keep source-code editing centralized in the main implementation agent.

If the first reasonable fix fails, stop editing and use debug before
trying another fix.

Validate review findings before acting on them; do not accept them
automatically.

For foundational or compatibility-sensitive API design, or debugging
that stays unresolved, invoke api-design or debug with model opus.

Use the project's lowercase `explore` agent, not the built-in `Explore`.
