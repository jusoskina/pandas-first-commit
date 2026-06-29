---
name: pandas-clarify-change
description: >-
  Run intake and clarify a chosen pandas contribution before any code edits.
  Use when starting a contribution session, running /pandas-start, or when the
  user wants to lock scope on an issue or change they already chose.
disable-model-invocation: true
---

# Clarify pandas change

**Workflow stage:** Intake + Stage 1

Read [pandas-contribution-core](../pandas-contribution-core/SKILL.md) for global invariants before proceeding.

## Objective

Restate the contribution in plain language and lock scope before any inspection or implementation.

## Intake questions

Ask before producing the change clarification:

1. **Experience:** First pandas contribution or returning contributor?
2. **Change:** What issue, bug, failing example, or intended change are you working on?
3. **Type:** What contribution type do you think this is? (docs / test / bug fix / error message / behavior clarification / not sure)
4. **Environment:** Do you have a local pandas checkout open?
5. **Depth:** Planning only, or planning plus code/test scaffolding?

**Do not** recommend or select a new issue unless the user explicitly asks.

## Steps

1. Ask intake questions (skip any the user already answered).
2. Restate current vs expected behavior in plain language.
3. Lock in-scope and out-of-scope items.
4. Output the **Change clarification** template from [role-output-templates.md](../pandas-contribution-core/references/role-output-templates.md).

## Stop if

- Current vs expected behavior is unclear → ask for a minimal reproducible example.
- Change is too broad → narrow scope before continuing (see core failure modes).

## Next step

When clarification is complete, suggest `/pandas-inspect` or continue to context inspection if the user wants to proceed in the same session.
