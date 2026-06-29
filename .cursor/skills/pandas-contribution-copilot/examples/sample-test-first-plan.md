# Sample test-first plan

**Example from [GH#62682](https://github.com/pandas-dev/pandas/issues/62682).** Aligns with [change-type-rules.md](../../pandas-contribution-core/references/change-type-rules.md) (bug fix + error reporting).

---

## Test-first plan

### Likely test location

`pandas/tests/arithmetic/test_string.py`

### Why this location

Existing string addition tests (`test_add`, `test_add_2d`) already cover string dtype arithmetic. The GH#62682 reproduction uses `pd.array(...) + DataFrame(...)`, which fits this module.

### Test to add or update

Add `test_add_dataframe_with_unboxable_values`:

1. Build `arr = pd.array(["a", np.nan])`
2. Build DataFrames containing `Categorical` and `Minute` offset (from issue repro)
3. Assert `TypeError` with pandas-style message (not pyarrow error types)

```python
def test_add_dataframe_with_unboxable_values():
    # GH#62682
    pytest.importorskip("pyarrow")

    invalid1 = pd.Categorical(["test"])
    invalid2 = pd.offsets.Minute(3)
    arr = pd.array(["a", np.nan])
    df1 = pd.DataFrame([[invalid1, invalid1]])
    df2 = pd.DataFrame([[invalid2, invalid2]])

    msg = "operation 'add' not supported for dtype 'string' with dtype 'object'"
    with pytest.raises(TypeError, match=msg):
        arr + df1
    with pytest.raises(TypeError, match=msg):
        arr + df2
```

### Targeted command

```bash
pytest pandas/tests/arithmetic/test_string.py::test_add_dataframe_with_unboxable_values -xvs
```

### Expected first result

**Before** the fix: test fails — pyarrow `ArrowInvalid` / `ArrowTypeError` escapes instead of pandas `TypeError`.

**After** the fix: test **passes** (verified locally: 1 passed in 0.05s).

### Notes on exception testing

- Assert pandas `TypeError`, not `pa.ArrowInvalid` or `pa.ArrowTypeError`
- Use `pytest.raises(TypeError, match=...)` for the message
- `pytest.importorskip("pyarrow")` because string array uses pyarrow backend
