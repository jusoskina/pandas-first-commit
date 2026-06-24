# Sample change clarification

**Example from [GH#62682](https://github.com/pandas-dev/pandas/issues/62682).** Aligns with [role-output-templates.md](../references/role-output-templates.md).

---

## Change clarification

### User problem

When a user adds a string Arrow array to a DataFrame containing values pyarrow cannot box (e.g. `Categorical`, `DateOffset`), pandas surfaces cryptic pyarrow errors instead of a clear pandas exception.

### Expected behavior

pandas raises a clear `TypeError` at the operation site explaining that the operation is not supported for the dtypes involved.

### Current behavior

```python
import pandas as pd
import numpy as np

arr = pd.array(["a", np.nan])
df1 = pd.DataFrame([[pd.Categorical(["test"]), pd.Categorical(["test"])]])
df2 = pd.DataFrame([[pd.offsets.Minute(3), pd.offsets.Minute(3)]])

arr + df1
# pyarrow.lib.ArrowInvalid: Could not convert ... Categorical ...

arr + df2
# pyarrow.lib.ArrowTypeError: No temporal attributes found on object.
```

### Contribution type

bug fix (error reporting) + regression test

### Scope

In scope:

- Catch `ArrowInvalid` / `ArrowTypeError` from `_box_pa` in `_evaluate_op_method`
- Raise `TypeError` using `_op_method_error_message`
- Add regression test in `pandas/tests/arithmetic/test_string.py`
- Reference GH#62682 in commit message

Out of scope:

- Rewriting all `_box_pa` call sites
- Fixing unrelated string operations
- Waiting for #61828 merge (noted in issue; standalone test is acceptable)
- Docs site changes (error message improvement only)

### Open questions

- Should other `_box_pa` callers get the same treatment? — **start with arithmetic path only**
- Does #61828 add overlapping tests? — **align with maintainer feedback if that PR lands first**
