# Sample first contribution flow

**Example based on a real contribution walkthrough** ([GH#62682](https://github.com/pandas-dev/pandas/issues/62682)). Pytest and pre-commit were run locally; checker was run after commit.

## Scenario

A first-time contributor chose [GH#62682](https://github.com/pandas-dev/pandas/issues/62682): pyarrow boxing errors when adding a string array to a DataFrame with Categorical or DateOffset values. Goal: raise a clear pandas `TypeError` and add a regression test.

---

## 1. User opens the session

**User:**

> I'm a first-time pandas contributor. Please walk me through [GH#62682](https://github.com/pandas-dev/pandas/issues/62682). I have a local checkout and want planning plus scaffolding.

**Assistant:**

> I'll follow the pandas contribution copilot workflow. A few intake questions:
>
> 1. Is this your first pandas contribution?
> 2. Can you share the issue link or failing example?
> 3. What type do you think this is?
> 4. Do you have a local pandas checkout open?
> 5. Planning only, or planning plus scaffolding?

---

## 2. User answers

**User:**

> First contribution. Issue link above. Bug fix / error reporting. Pandas cloned in Cursor. Planning plus scaffolding please.

**Reproduction from the issue:**

```python
import pandas as pd
import numpy as np

invalid1 = pd.Categorical(["test"])
invalid2 = pd.offsets.Minute(3)
arr = pd.array(["a", np.nan])
df1 = pd.DataFrame([[invalid1, invalid1]])
df2 = pd.DataFrame([[invalid2, invalid2]])

arr + df1  # ArrowInvalid: ... Categorical ...
arr + df2  # ArrowTypeError: No temporal attributes found on object.
```

---

## 3. Assistant clarifies the change

**Assistant output:** See [sample-change-clarification.md](sample-change-clarification.md).

---

## 4. Assistant inspects local context

**Assistant:**

> I'll inspect approved local context:
>
> - `git grep "_box_pa" -- pandas/`
> - `rg "_evaluate_op_method" pandas/core/arrays/arrow/`
> - `pandas/tests/arithmetic/test_string.py` for string `+` tests
>
> **Found:** `_evaluate_op_method` in `pandas/core/arrays/arrow/array.py` calls `self._box_pa(other)` without catching pyarrow boxing failures. String arithmetic tests live in `pandas/tests/arithmetic/test_string.py`.

---

## 5. Assistant plans test-first work

**Assistant output:** See [sample-test-first-plan.md](sample-test-first-plan.md).

---

## 6. Assistant scaffolds the fix

**Branch:** `bug-box_pa-clear-errors-62682`

**Change:** Wrap `_box_pa` in `_evaluate_op_method` and raise `TypeError` via `_op_method_error_message` when pyarrow raises `ArrowInvalid` or `ArrowTypeError`.

**New error (both repro cases):**

```
TypeError: operation 'add' not supported for dtype 'string' with dtype 'object'
```

---

## 7. Assistant runs checks (stages 6–7)

**Assistant output:**

> ## Checks run report
>
> | Check | Command | Result | Notes |
> |-------|---------|--------|-------|
> | Targeted pytest | `pytest pandas/tests/arithmetic/test_string.py::test_add_dataframe_with_unboxable_values -xvs` | PASS | 1 passed in 0.05s |
> | pre-commit | `pre-commit run --files pandas/core/arrays/arrow/array.py pandas/tests/arithmetic/test_string.py` | PASS | All hooks passed |
> | PR readiness checker | `python3 ../scripts/check_pandas_contribution.py --base main` | PASS | exit 0; 1 checker warning (docs optional) |
> | Doc checks | `./ci/code_checks.sh docstrings` | N/A | Error-path fix only |
>
> ### Checker summary
>
> | Item | Value |
> |------|-------|
> | Base branch | main |
> | Changed files | 2 |
> | Contribution type | code + tests |
> | Risk level | low |
> | Checker failures | 0 |
> | Checker warnings | 1 |
>
> Full checker terminal output: [sample-checker-output.md](sample-checker-output.md)

---

## 8. Assistant produces PR package and role outputs

**Suggested PR title:** `BUG: raise clear TypeError when _box_pa fails in arithmetic ops`

**Outputs:** [sample-pr-readiness-report.md](sample-pr-readiness-report.md), [sample-role-outputs.md](sample-role-outputs.md)

---

## 9. Demo closing (assistant)

> **Intentionally not automated:**
>
> - No automatic issue selection
> - No claim that upstream CI passed (only local checks shown)
> - No replacement for maintainer review
>
> **Checker reminder:** run from the pandas repo after commit, not from the copilot meta-repo alone.
