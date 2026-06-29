# Sample PR readiness report

**Example from [GH#62682](https://github.com/pandas-dev/pandas/issues/62682).** Template from [role-output-templates.md](../../pandas-contribution-core/references/role-output-templates.md).

---

## Checks run report

| Check | Command | Result | Notes |
|-------|---------|--------|-------|
| Targeted pytest | `pytest pandas/tests/arithmetic/test_string.py::test_add_dataframe_with_unboxable_values -xvs` | PASS | 1 passed in 0.05s |
| pre-commit | `pre-commit run --files pandas/core/arrays/arrow/array.py pandas/tests/arithmetic/test_string.py` | PASS | All hooks passed |
| PR readiness checker | `python3 ../scripts/check_pandas_contribution.py --base main` | PASS | exit 0; 1 warning |
| Doc checks | `./ci/code_checks.sh docstrings` | N/A | Error-path fix |

### Checker summary

| Item | Value |
|------|-------|
| Base branch | main |
| Changed files | 2 |
| Contribution type | code + tests |
| Risk level | low |
| Checker failures | 0 |
| Checker warnings | 1 (docs optional) |

---

## PR readiness check

### Scope

- [x] Change is limited to one issue or one clear improvement
- [x] No unrelated formatting or refactoring
- [x] Risky internals avoided or explicitly justified

### Tests

- [x] Test added or updated for code behavior change
- [x] Test is located near related existing tests
- [x] Targeted pytest command provided
- [x] Exception type and message tested with `pytest.raises(..., match=...)`
- [x] No public network dependency in unit tests

### Docs

- [x] Docs or docstring update not required for internal error-path change
- [x] N/A — docstring style
- [x] Examples are minimal and accurate

### Compatibility

- [x] No public API/signature change
- [x] Deprecation path N/A
- [x] Optional dependency handling N/A

### CI / guardrails

- [x] Pre-commit run and passed
- [x] Checks run report table shown (pytest, pre-commit, checker)
- [x] Checker run from pandas repo after commit
- [x] CI risk summarized (targeted unit tests; low blast radius)

### PR communication

- [x] PR title uses `BUG` prefix
- [x] PR references GH#62682
- [x] PR description explains what, why, and how tested

---

## Suggested PR title

`BUG: raise clear TypeError when _box_pa fails in arithmetic ops`

## PR description (abbreviated)

### What changed

- Catch pyarrow boxing errors in `_evaluate_op_method` when `_box_pa` fails
- Add `test_add_dataframe_with_unboxable_values` for Categorical and DateOffset cases

### Why

- Fixes GH#62682 — users saw cryptic pyarrow errors instead of pandas `TypeError`

### Tests

- `pytest pandas/tests/arithmetic/test_string.py::test_add_dataframe_with_unboxable_values -xvs` — **passed locally**

### Risk

- Low — error-path only; no API change

### Notes for reviewers

- Related to #61828; issue author noted possible test overlap after that PR merges
