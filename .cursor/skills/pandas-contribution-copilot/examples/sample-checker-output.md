# Sample checker output

**Example from [GH#62682](https://github.com/pandas-dev/pandas/issues/62682).** Actual output from:

```bash
cd pandas
python3 ../scripts/check_pandas_contribution.py --base main
```

Run after commit `53aa953` on branch `bug-box_pa-clear-errors-62682`. Format matches [scripts/README.md](../../../../scripts/README.md).

---

## Terminal output

```text
============================================================
PANDAS PR READINESS CHECK
============================================================
Base branch: main
Changed files: 2

Changed files by category
----------------------------------------
  Source (2):
    - pandas/core/arrays/arrow/array.py
    - pandas/tests/arithmetic/test_string.py
  Tests (1):
    - pandas/tests/arithmetic/test_string.py
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
  [WARN] Consider whether docs, docstrings, or release notes are needed.

Suggested commands (not run by this checker)
----------------------------------------
  pytest pandas/tests/arithmetic/test_string.py
  ./ci/code_checks.sh docstrings
  ./ci/code_checks.sh doctests
  ./ci/code_checks.sh code
  pre-commit run --files pandas/core/arrays/arrow/array.py pandas/tests/arithmetic/test_string.py

Note: This checker does not prove correctness or CI success. Run the suggested commands locally before opening a PR.
```

---

## How this maps to the Checks run report table

| Checker item | Value |
|--------------|-------|
| Exit code | `0` |
| Contribution type | code + tests |
| Risk level | low |
| FAIL rows | 0 |
| WARN rows | 1 (docs optional for error-path fix) |

---

## Demo notes

| Item | Explanation |
|------|-------------|
| Run location | Must be inside the **pandas** git repo, not `pandas-first-commit` alone |
| Requires commit | `git diff main...HEAD` — uncommitted edits are invisible to the checker |
| `[WARN] docs...` | Heuristic: source changed without docs files; OK for this fix |
| Pair with table | Always show this output **and** the Checks run report table at stages 6–7 |
