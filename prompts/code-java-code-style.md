# Java Code-Style Prompts

Copy one template, fill in the brackets, and paste it. Each one names its skill so the skill loads.

## Write or change code

[Describe the change] in [class/package]. Use the java-code-style skill so the new and changed lines match the house style. Do not reformat other code.

## Reformat a file

Use the java-code-style skill to reformat [file/path]. Change formatting only, without touching behavior, names, or member order.

## Set up lint

Use the java-code-style skill to add its Checkstyle config and .editorconfig to this project and wire Checkstyle into the [Maven/Gradle] build. Run it and report the findings without fixing them.

## Review only

Use the java-code-style skill to review [files/diff] for formatting, import, and naming issues. Do not edit. Report findings as: file:line, rule, fix.
