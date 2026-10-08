# Spec and Architecture Verification Prompts

Copy one template, fill in the brackets, and paste it. Each one names its skill so the skill loads.

## Design first, then implement

Implement [feature] in [module/package]. Use the spec-architecture-verification skill: map the boundaries the change touches, write the design note, and stop before coding if it trips a drift rule.

## Design only

Use the spec-architecture-verification skill to analyze [feature/request] against [spec/ADR/API file]. Write the architecture map and design note only. Do not edit code.

## Review a change

Use the spec-architecture-verification skill to review [diff/branch vs main] for architectural drift, coupling, and contract changes. Do not edit. Report findings as: file:line, rule, risk, suggested fix.
