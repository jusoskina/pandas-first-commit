---
name: pandas-ship-contribution
description: >-
  Generate PR title and description plus Engineering, PM, QA, and DevOps handoff
  summaries for a pandas contribution. Use when running /pandas-ship or
  automatically after verify succeeds.
disable-model-invocation: true
---

# Ship pandas contribution

**Workflow stages:** Stage 8 (PR package) + Stage 9 (role handoffs)

Read [pandas-contribution-core](../pandas-contribution-core/SKILL.md) and [role-output-templates.md](../pandas-contribution-core/references/role-output-templates.md).

## Objective

Produce PR communication and role-specific handoff summaries using facts from prior stages only — do not invent details.

## Stage 8 — Generate PR package

Output the **PR title and description** template. Use the correct PR prefix from [change-type-rules.md](../pandas-contribution-core/references/change-type-rules.md).

## Stage 9 — Generate role-specific outputs

Output all four summaries in the same response:

1. Engineering summary
2. PM summary
3. QA notes
4. DevOps / CI notes

Use placeholders only where facts are unknown — write `Unknown` or ask the user.

## Rules

- Run automatically when stage 7 succeeds — immediately after verify in the same response.
- Do not open a PR or push unless the user explicitly asks.
- Do not stop after stage 8 alone — always output all four role summaries.

## What is not automated

- No automatic issue selection
- No broad autonomous coding
- No unapproved external context
- No claim that CI passed unless checks were run
- No replacement for maintainer review
