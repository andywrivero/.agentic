# Systematic Debugging Prompts

Copy one template, fill in the brackets, and paste it. Each one names its skill so the skill loads.

## Diagnose only

Use the systematic-debugging skill to find the root cause of [symptom / failing test / error]. Do not fix it. Report the reproduction, each hypothesis with its result, and the cause.

## Diagnose and fix

Use the systematic-debugging skill to find the root cause of [symptom], then fix it with the tdd-loop skill, using the reproduction as the first failing test.

## From a stack trace or log

Use the systematic-debugging skill on this [stack trace / build output / log]: [paste]. Find the first relevant failure and trace it to its cause before suggesting any change.
