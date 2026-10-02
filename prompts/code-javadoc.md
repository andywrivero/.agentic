# Javadoc Prompts

Use these prompts with the existing `javadoc` skill whenever creating or editing Java types or methods.

## 1. Add or Update Javadoc

Add or update Javadoc for **[identify the Java type or members]**.

- Apply the `javadoc` skill. Inspect the implementation, annotations, callers, and existing documentation before writing.
- Document useful contracts, including parameters, return values, checked exceptions, and major unchecked exceptions where applicable. Keep nullability annotations and documented contracts in sync.
- Use a concise summary fragment beginning with a third-person singular present-tense verb. Use `{@code ...}` for code terms and `{@link ...}` for relevant cross-references.
- Skip trivial getters, setters, and standard constructors; use inherited documentation for unchanged override contracts.
- Edit documentation only; preserve code logic and formatting. Keep the result compact and suitable for IDE hover.

## 2. Review Javadoc Accuracy and Completeness

Review Javadoc in **[identify the Java files, types, or diff]** for accuracy, completeness, and IDE readability.

- Apply the `javadoc` skill and compare each documented contract with the implementation, annotations, and relevant callers.
- Check summary fragments, tag ordering, generic type parameters, parameters, returns, checked and major unchecked exceptions, and nullability guarantees.
- Check for stale parameter names, claims that disagree with behavior, redundant documentation of trivial members, and duplicated override documentation that should inherit its contract.
- Make focused Javadoc-only corrections. Do not change implementation logic or expand scope to unrelated files.
- Summarize the documentation corrections; if none are needed, report that and note any remaining uncertainty.

## 3. Document a Java API Type

Document **[identify the class, interface, enum, or record]** for developers using and maintaining it.

- Apply the `javadoc` skill and describe the type's responsibility, relevant usage constraints, and threading or immutability guarantees when established by the code.
- Document useful public and protected contracts, plus package-private or private methods with non-obvious behavior, side effects, invariants, or control flow.
- Add applicable generic type parameter and member tags. Keep nullability contracts explicit and use `{@inheritDoc}` when an override preserves its inherited contract.
- Keep summaries concise and paragraphs compact for hover display. Avoid documenting obvious behavior or inventing guarantees not supported by the implementation.
- Preserve code behavior and make only documentation changes; summarize the coverage added.