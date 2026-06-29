---
name: pandas-plan-contribution
description: >-
  Classify risk and create a test-first plan for a pandas contribution. Use when
  running /pandas-plan or after context inspection is complete.
disable-model-invocation: true
---

# Plan pandas contribution

**Workflow stages:** Stage 3 (risk) + Stage 4 (test-first plan)

Read [pandas-contribution-core](../pandas-contribution-core/SKILL.md), [change-type-rules.md](../pandas-contribution-core/references/change-type-rules.md), and [role-output-templates.md](../pandas-contribution-core/references/role-output-templates.md).

## Objective

Set risk level and compatibility expectations, then define the smallest test or docs check that validates the change.

## Inputs needed

- Change clarification (stage 1)
- Context inspection results (stage 2)

## Stage 3 — Classify risk

1. Apply [change-type-rules.md](../pandas-contribution-core/references/change-type-rules.md) for the contribution type.
2. Output the **Risk classification** template.

**Stop if** risk is high or unclear → narrow scope or ask maintainer first. Default to narrowing when uncertain.

## Stage 4 — Plan test-first work

**For code/test contributions:**

1. Identify the most relevant existing test file.
2. Define the smallest failing regression test to add or update.
3. Include GitHub issue number in a comment when available.
4. Use `pandas._testing` helpers where appropriate.
5. Use `pytest.raises(..., match=...)` for exceptions.
6. Use warning assertion helpers for warning changes.
7. No public network in unit tests.
8. Prefer parametrized pytest for simple input combos.
9. Use Hypothesis only when input domain complexity justifies it.

**For docs-only contributions:**

- Define which docs pages or docstrings change
- Plan `./ci/code_checks.sh docstrings`, `doctests`, and `code` as applicable
- Do not invent a code test unless behavior is ambiguous

Output the **Test-first plan** template.

**Stop if** no test location found → search more or ask user before implementing.

## Next step

When planning is complete, suggest `/pandas-implement` if the user requested scaffolding.
