# Sample checker output

**Example only.** Illustrative terminal output for `scripts/check_pandas_contribution.py`. This diff was **not** run against a real pandas branch. Format matches [scripts/README.md](../../../../scripts/README.md).

---

## Command

```bash
python scripts/check_pandas_contribution.py --base upstream/main
```

Run from the root of a pandas checkout after committing the error-message fix and test.

---

## Illustrative output

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
  [WARN] Consider whether docs, docstrings, or release notes are needed.

Suggested commands (not run by this checker)
----------------------------------------
  pytest pandas/tests/frame/test_api.py
  ./ci/code_checks.sh docstrings
  ./ci/code_checks.sh doctests
  ./ci/code_checks.sh code
  pre-commit run --files pandas/core/frame.py pandas/tests/frame/test_api.py

Note: This checker does not prove correctness or CI success. Run the suggested commands locally before opening a PR.
```

---

## Notes for demo

| Item | Explanation |
|------|-------------|
| `pandas/core/frame.py` | **Placeholder** — real path depends on inspection; shown for realistic checker output |
| `[WARN] docs...` | Heuristic fired because source changed without docs files; docstring update may still be needed |
| Exit code | Would be `0` (warning only, not `--strict`) |
| With `--strict` | Would exit `1` only if code changed without tests — here tests are present, so still `0` |

To demo a **code-without-tests** failure:

```bash
python scripts/check_pandas_contribution.py --base upstream/main --strict
# Illustrative: [FAIL] Code changed but no pandas/tests file changed.
```

*(That failure output is hypothetical — run against an actual branch to show real results.)*
