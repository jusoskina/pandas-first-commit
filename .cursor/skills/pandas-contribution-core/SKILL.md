---
name: pandas-contribution-core
description: >-
  Shared rules and references for pandas open-source contributions. Defines
  approved context, change-type guidance, output templates, and global
  invariants. Loaded by stage skills — not invoked directly by users.
---

# pandas Contribution Core

Shared foundation for all pandas contribution stage skills. Stage skills link here; do not duplicate this content.

## Global invariants

- **Issue selection:** Do not recommend or select a new issue unless the user explicitly asks.
- **Test-first:** Code behavior changes need a test plan before implementation.
- **Docs-only:** Do not force code tests; suggest docs checks instead.
- **Inspect first:** Do not propose pandas internals without reading relevant local files.
- **Honesty:** Do not claim CI or checks passed unless they were run.
- **Scope:** One issue or one clear improvement per branch.
- **Local docs first:** Search local repo docs before online docs. If they conflict, prefer the local checkout.

## Suitable issue types

**Good fit:** docs, docstrings, error messages, regression tests, small bug fixes, behavior clarification via tests/docs.

**Use caution:** public API changes, backwards compatibility, deprecations, optional deps, typing, performance.

**Out of scope for first contribution** unless explicitly requested: Cython/compiled extensions, large refactors, broad indexing internals, major API design, release engineering, dependency upgrades, performance rewrites.

## Shared references

| Reference | Use when |
|-----------|----------|
| [approved-context.md](references/approved-context.md) | Before proposing changes; defining allowed sources |
| [change-type-rules.md](references/change-type-rules.md) | Classifying type, tests, docs, risk, PR prefix |
| [role-output-templates.md](references/role-output-templates.md) | Filling structured outputs at each stage |

## Stage skills and commands

| Phase | Skill | Command |
|-------|-------|---------|
| Intake + clarify | `pandas-clarify-change` | `/pandas-start` |
| Inspect context | `pandas-inspect-context` | `/pandas-inspect` |
| Risk + test plan | `pandas-plan-contribution` | `/pandas-plan` |
| Implement | `pandas-scaffold-change` | `/pandas-implement` |
| Checks + readiness | `pandas-verify-contribution` | `/pandas-verify` |
| PR + handoffs | `pandas-ship-contribution` | `/pandas-ship` |
| Full flow (demo) | `pandas-contribution-copilot` | `/pandas-full` |

Run stages in order unless the user explicitly asks to jump ahead.

## Failure modes

If context is insufficient, use the template in [approved-context.md](references/approved-context.md).

If the change is too broad:

> This is too broad for a safe first contribution. I recommend narrowing it to:
> - <smaller version>

If there is a compatibility concern:

> This may affect backwards compatibility. Before implementation, we should either:
> 1. confirm the expected behavior in the issue discussion, or
> 2. limit the change to tests/docs that clarify current behavior.

If the user asks to skip tests for a code behavior change:

> For pandas-style contributions, skipping tests is likely to create review churn. I can help narrow the test to the smallest regression case instead.

## Maintainability

- Do not encode large copies of pandas documentation in skills.
- Prefer deterministic scripts (`check_pandas_contribution.py`) for mechanical checks.
- Do not claim certainty about pandas internals without inspecting files.
