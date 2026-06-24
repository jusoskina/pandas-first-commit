# Pandas contribution scripts

## `check_pandas_contribution.py`

A lightweight, deterministic PR readiness checker for pandas contributions. It inspects the git diff against a base branch and flags obvious readiness issues before code review.

This script **supports** the [pandas Contribution Copilot](../.cursor/skills/pandas-contribution-copilot/SKILL.md) skill. The skill guides judgment-heavy workflow steps (clarifying the change, test-first planning, scaffolding, multi-role summaries). The checker catches mechanical guardrails the skill recommends but should not rely on model memory for.

### What it does

- Compares `HEAD` to a configurable base branch (default: `upstream/main`)
- Groups changed files into source, test, docs, CI/config, risky internals, and other
- Infers contribution type and a rough risk level
- Runs a checklist with `PASS` / `WARN` / `FAIL` statuses
- Suggests targeted `pytest`, `pre-commit`, and pandas `ci/code_checks.sh` commands
- Supports `--json` for machine-readable output and `--strict` for stricter exits

### What it does not do

- Prove that a change is correct or that tests pass
- Replace maintainer review or the copilot skill's planning workflow
- Automatically find the right test file (it only suggests search commands)
- Detect every user-facing behavior change with certainty (it uses simple diff heuristics)
- Run any checks itself — it only recommends commands

### Example usage

Run from the root of a pandas checkout, on a branch with commits ahead of the base:

```bash
python scripts/check_pandas_contribution.py
```

Common variants:

```bash
# Different base branch
python scripts/check_pandas_contribution.py --base origin/main

# Stricter: code changes without tests exit with failure
python scripts/check_pandas_contribution.py --strict

# JSON report for tooling
python scripts/check_pandas_contribution.py --json

# Widen the first-PR file-count threshold
python scripts/check_pandas_contribution.py --max-files 12
```

Exit codes:

- `0` — no failures (warnings alone still exit `0` unless `--strict` promotes them)
- `1` — git/checker error, or one or more `FAIL` results

### How it supports the copilot Skill

The skill's workflow stages 6–7 require an explicit **Checks run report** table (see `role-output-templates.md`). The assistant must show a row for pytest, pre-commit, and this checker with PASS/FAIL/NOT RUN — not bury results in prose.

1. **After scaffolding** — run the checker to see missing tests, docs warnings, or risky paths
2. **Before opening a PR** — confirm scope, risk, and suggested commands match the skill's checklist
3. **In demos** — show that guardrails are automated while planning stays assistant-guided

The skill should still produce human-readable summaries for Engineering, PM, QA, and DevOps. This script fills in the mechanical checklist portion.

### Sample output

```text
============================================================
PANDAS PR READINESS CHECK
============================================================
Base branch: upstream/main
Changed files: 2

Changed files by category
----------------------------------------
  Source (1):
    - pandas/core/frame.py
  Tests (1):
    - pandas/tests/frame/test_api.py
  Docs (0):
    (none)
  CI/Config (0):
    (none)
  Risky internals (0):
    (none)
  Other (0):
    (none)

Inferred contribution type: code + tests
Risk level: low
Risk reasons:
  - Code and tests changed together.

Checklist
----------------------------------------
  [PASS] Source and test files both changed.
  [PASS] File count (2) is within the threshold (8).

Suggested commands (not run by this checker)
----------------------------------------
  pytest pandas/tests/frame/test_api.py
  ./ci/code_checks.sh docstrings
  ./ci/code_checks.sh doctests
  ./ci/code_checks.sh code
  pre-commit run --files pandas/core/frame.py pandas/tests/frame/test_api.py

Note: This checker does not prove correctness or CI success. Run the suggested commands locally before opening a PR.
```
