---
name: pandas-verify-contribution
description: >-
  Run local checks and review PR readiness for a pandas contribution. Use when
  running /pandas-verify or after implementation is complete. On success,
  automatically continues to ship (PR package + role handoffs).
disable-model-invocation: true
---

# Verify pandas contribution

**Workflow stages:** Stage 6 (checks) + Stage 7 (PR readiness)

Read [pandas-contribution-core](../pandas-contribution-core/SKILL.md), [role-output-templates.md](../pandas-contribution-core/references/role-output-templates.md), and [checker-usage.md](references/checker-usage.md).

## Objective

Run or recommend targeted local checks, then verify the contribution meets pandas PR expectations.

## Stage 6 — Run or recommend checks

**Rule:** Always output the **Checks run report** table. Do not bury checker/pytest/pre-commit results in prose. Do not claim `PASS` unless the command actually ran and succeeded.

**For code/test changes, run or recommend:**

```bash
pytest <relevant-test-path> -k "<keyword>"
pre-commit run --files <changed-files>
```

**Deterministic checker** (see [checker-usage.md](references/checker-usage.md)):

```bash
python3 ../scripts/check_pandas_contribution.py --base upstream/main
```

**Docs/docstrings:**

```bash
./ci/code_checks.sh docstrings
./ci/code_checks.sh doctests
./ci/code_checks.sh code
```

**Stop if** a required check fails → fix before PR readiness review.

## Stage 7 — Review PR readiness

Stage 7 must include both:

1. **Checks run report** table (do not omit)
2. **PR readiness check** checklist from [role-output-templates.md](../pandas-contribution-core/references/role-output-templates.md)

If the checker was not run, say so explicitly (`NOT RUN` + reason).

**Stage 7 success:** No required check has `FAIL`, and no critical PR readiness item is blocking. `WARN` and explained `NOT RUN` rows do not block success unless the user asks to stop.

## On stage 7 success — continue immediately

Do not stop after the PR readiness check. In the **same response**, follow [pandas-ship-contribution](../pandas-ship-contribution/SKILL.md) (stages 8 and 9) without waiting for another user prompt.

Do not open a PR or push unless the user explicitly asks.
