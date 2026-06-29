---
name: pandas-contribution-copilot
description: >-
  Orchestrate the full pandas contribution workflow from intake through PR
  handoffs. Use for demos, technical screens, or when the user runs
  /pandas-full. For single steps, use stage commands (/pandas-start,
  /pandas-inspect, etc.) instead.
disable-model-invocation: true
---

# pandas Contribution Copilot (hub)

Thin orchestrator for the full contribution flow. Detailed instructions live in stage skills — this hub sequences them.

## When to use

- Demo or technical screen walkthrough
- User runs `/pandas-full` and wants the end-to-end flow
- User asks to "walk me through" a first contribution

For a single step, use the matching command instead (see table below).

## Shared foundation

All global rules and templates: [pandas-contribution-core](../pandas-contribution-core/SKILL.md)

## Stage commands

| Step | Command | Skill |
|------|---------|-------|
| 1. Intake + clarify | `/pandas-start` | `pandas-clarify-change` |
| 2. Inspect context | `/pandas-inspect` | `pandas-inspect-context` |
| 3. Risk + test plan | `/pandas-plan` | `pandas-plan-contribution` |
| 4. Implement | `/pandas-implement` | `pandas-scaffold-change` |
| 5. Verify | `/pandas-verify` | `pandas-verify-contribution` |
| 6. Ship | `/pandas-ship` | `pandas-ship-contribution` |

## Full flow

Run stages in order. Follow each stage skill completely before moving on.

1. `/pandas-start` — intake + change clarification
2. `/pandas-inspect` — find relevant files and tests
3. `/pandas-plan` — risk classification + test-first plan
4. `/pandas-implement` — scaffold minimal change (if user requested)
5. `/pandas-verify` — checks + PR readiness; on success, auto-continue to ship
6. Ship runs automatically after verify succeeds (stages 8–9 in same response)

Revisit a stage if scope, risk, or context changes.

## Demo script

Example walkthrough: [examples/sample-first-contribution-flow.md](examples/sample-first-contribution-flow.md). Supporting outputs in `examples/`.

**Demo opener:** "I have chosen a pandas issue and want help making a safe first contribution."

**Demo closer:** Explain what is intentionally not automated (see ship skill).

## Examples

| Example | File |
|---------|------|
| Full flow | [sample-first-contribution-flow.md](examples/sample-first-contribution-flow.md) |
| Change clarification | [sample-change-clarification.md](examples/sample-change-clarification.md) |
| Test-first plan | [sample-test-first-plan.md](examples/sample-test-first-plan.md) |
| Checker output | [sample-checker-output.md](examples/sample-checker-output.md) |
| PR readiness | [sample-pr-readiness-report.md](examples/sample-pr-readiness-report.md) |
| Role outputs | [sample-role-outputs.md](examples/sample-role-outputs.md) |
