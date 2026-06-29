# PR readiness checker

Deterministic checker for workflow stages 6–7. Full script docs: [scripts/README.md](../../../../scripts/README.md).

## When to run

From the **pandas git repo root**, on a branch with **commits ahead of base** — not from the copilot meta-repo alone.

## Commands

```bash
# From pandas repo (script in copilot meta-repo)
python3 ../scripts/check_pandas_contribution.py --base upstream/main

# If script is in the pandas repo
python scripts/check_pandas_contribution.py --base upstream/main
```

## What it does

- Compares `HEAD` to a base branch
- Groups changed files by category
- Infers contribution type and risk level
- Runs a PASS / WARN / FAIL checklist
- Suggests targeted pytest, pre-commit, and doc check commands

## What it does not do

- Prove correctness or that tests pass
- Replace maintainer review or test-first planning
- Run checks itself — only recommends commands

## Reporting

Always include checker results in the **Checks run report** table from [role-output-templates.md](../../pandas-contribution-core/references/role-output-templates.md). Use `PASS`, `FAIL`, `WARN`, or `NOT RUN` — never bury results in prose alone.
