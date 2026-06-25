---
name: pandas-contribution-copilot
description: >-
  Use when helping a new or returning contributor make a small, safe pandas
  contribution from an issue or change they have already chosen. Guides through
  clarifying the change, inspecting approved repo context, planning test-first
  implementation, scaffolding code/docs/tests, checking PR readiness, and
  producing handoff notes for Engineering, PM, QA, and DevOps. Best suited to
  docs updates, error message improvements, regression tests, small bug fixes,
  and behavior clarifications. Use when the user mentions pandas contribution,
  first PR, good first issue, or pandas open source.
---

# pandas Contribution Copilot

## Purpose

Help a new or returning engineer make a small, safe pandas-style contribution without needing to understand the whole pandas codebase first.

This skill assumes the contributor already has an issue, bug, failing example, or intended change. It does not select issues automatically.

The goal is not to automate pandas development end to end. The goal is to reduce ramp time, prevent avoidable review churn, and help the contributor move a change safely toward review and CI.

## References

Read these files for detailed rules and templates. Do not duplicate their content in chat — link or apply them directly.

| Reference | Use when |
|-----------|----------|
| [approved-context.md](references/approved-context.md) | Before proposing changes; defining what sources are allowed |
| [contribution-workflow.md](references/contribution-workflow.md) | Running the end-to-end workflow (stages 1–9) |
| [change-type-rules.md](references/change-type-rules.md) | Classifying contribution type, tests, docs, risk, PR prefix |
| [role-output-templates.md](references/role-output-templates.md) | Filling structured outputs (risk, PR package, role summaries) |

**Deterministic checker:** Run at stage 6–7 from the **pandas repo** after commit. Always show the **Checks run report** table from [role-output-templates.md](references/role-output-templates.md) — never bury checker/pytest/pre-commit results in prose alone.

## Suitable issue types

This skill works best when the chosen issue or change is small, clear, and testable. See [change-type-rules.md](references/change-type-rules.md) for per-type guidance and first-PR fit.

**Good fit:** docs, docstrings, error messages, regression tests, small bug fixes, behavior clarification via tests/docs.

**Use caution:** public API changes, backwards compatibility, deprecations, optional deps, typing, performance.

**Out of scope for first contribution** unless explicitly requested: Cython/compiled extensions, large refactors, broad indexing internals, major API design, release engineering, dependency upgrades, performance rewrites.

## Quick start

1. Ask intake questions from [contribution-workflow.md](references/contribution-workflow.md).
2. Follow workflow stages 1–9 in order.
3. Use only [approved context](references/approved-context.md).
4. Apply [change-type rules](references/change-type-rules.md) for the contribution type.
5. Output templates from [role-output-templates.md](references/role-output-templates.md).

Do not recommend or select a new issue unless the user explicitly asks.

## Core rules

- **Test-first:** Code behavior changes need a test plan before implementation.
- **Docs-only:** Do not force code tests; suggest docs checks instead.
- **Inspect first:** Do not propose pandas internals without reading relevant local files.
- **Honesty:** Do not claim CI or checks passed unless they were run.
- **Explicit checks table:** At stages 6–7, always output the **Checks run report** table (pytest, pre-commit, checker) with PASS/FAIL/NOT RUN per row.
- **Post-readiness handoff:** When stage 7 succeeds (no required check `FAIL`, no blocking readiness items), immediately run stages 8 and 9 in the same response — PR package plus Engineering, PM, QA, and DevOps summaries. Do not stop after the readiness check alone.
- **Scope:** One issue or one clear improvement per branch.

## Maintainability rules

- Do not encode large copies of pandas documentation in this skill.
- Prefer short rules here; put detailed rules in `references/`.
- Prefer deterministic scripts (`check_pandas_contribution.py`) for mechanical checks.
- Do not claim certainty about pandas internals without inspecting files.

## Failure modes and honest responses

If the assistant lacks enough context, use the template in [approved-context.md](references/approved-context.md).

If the change is too broad, say:

> This is too broad for a safe first contribution. I recommend narrowing it to:
> - <smaller version>

If there is a compatibility concern, say:

> This may affect backwards compatibility. Before implementation, we should either:
> 1. confirm the expected behavior in the issue discussion, or
> 2. limit the change to tests/docs that clarify current behavior.

If the user asks to skip tests for a code behavior change, say:

> For pandas-style contributions, skipping tests is likely to create review churn. I can help narrow the test to the smallest regression case instead.

## Demo script for technical screen

Example walkthrough: [examples/sample-first-contribution-flow.md](examples/sample-first-contribution-flow.md). Supporting outputs in `examples/`.

1. Start with: "I have chosen a pandas issue and want help making a safe first contribution."
2. Run intake and workflow from [contribution-workflow.md](references/contribution-workflow.md).
3. Produce outputs from [role-output-templates.md](references/role-output-templates.md).
4. After commit and a successful stage 7, stages 8–9 run automatically (PR package + role handoffs) — no extra prompt needed.
5. End by explaining what is intentionally not automated:
   - no automatic issue selection
   - no broad autonomous coding
   - no unapproved external context
   - no deep internals without explicit inspection
   - no claim that CI passed unless checks were run
   - no replacement for maintainer review
