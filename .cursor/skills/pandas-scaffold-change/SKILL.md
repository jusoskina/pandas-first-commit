---
name: pandas-scaffold-change
description: >-
  Scaffold the minimal pandas code, test, or docs change from an approved
  test-first plan. Use when running /pandas-implement or after planning is
  complete.
disable-model-invocation: true
---

# Scaffold pandas change

**Workflow stage:** Stage 5

Read [pandas-contribution-core](../pandas-contribution-core/SKILL.md) and [change-type-rules.md](../pandas-contribution-core/references/change-type-rules.md).

## Objective

Produce the smallest change that satisfies the approved test-first plan.

## Inputs needed

- Approved test-first plan from stage 4
- Context inspection results from stage 2

## Gate

**Stop if** test-first plan is missing for a behavior change → return to `/pandas-plan`.

## Implementation checklist

- [ ] Preserve backwards compatibility unless issue requires otherwise
- [ ] Do not change public signatures without calling out risk
- [ ] No broad refactors
- [ ] Match nearby code style
- [ ] One bug/feature/docs change per branch
- [ ] Use pandas optional-dependency helpers when relevant
- [ ] Update docs/docstrings for user-facing behavior
- [ ] Do not suppress warnings or tests to pass CI

## Expected output

Provide code, test, or docs edits (or a diff outline if the user asked for planning only). Match patterns from inspected nearby files.

## Next step

After scaffolding, suggest `/pandas-verify` to run checks and review PR readiness.
