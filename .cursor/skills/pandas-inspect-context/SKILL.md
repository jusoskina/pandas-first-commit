---
name: pandas-inspect-context
description: >-
  Inspect local pandas repo context for a chosen contribution — find relevant
  source, tests, and docs near affected behavior. Use when running
  /pandas-inspect or after change clarification is complete.
disable-model-invocation: true
---

# Inspect pandas context

**Workflow stage:** Stage 2

Read [pandas-contribution-core](../pandas-contribution-core/SKILL.md) and [approved-context.md](../pandas-contribution-core/references/approved-context.md) before proposing anything.

## Objective

Find implementation, tests, and docs near the affected behavior using approved context only.

## Inputs needed

- Change clarification from stage 1 (or equivalent user description)
- Local pandas checkout

## Steps

1. Search narrowly for symbols, error strings, or API names related to the change.
2. Use inspection commands from [approved-context.md](../pandas-contribution-core/references/approved-context.md).
3. List relevant source files, existing test locations, and related docs.
4. Note open questions discovered during inspection.

## Expected output

```markdown
## Context inspection

### Relevant source files
- <path> — <why>

### Relevant test files
- <path> — <why>

### Relevant docs
- <path> — <why, or "none found">

### Open questions
- <question, if any>
```

## Stop if

- Required files are not accessible → use missing-context template from approved-context.
- Do not propose internals without inspection.

## Next step

When inspection is complete, suggest `/pandas-plan` for risk classification and test-first planning.
