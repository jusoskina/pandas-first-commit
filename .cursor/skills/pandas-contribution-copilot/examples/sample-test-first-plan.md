# Sample test-first plan

**Example only.** Test file path is a placeholder until repo inspection. Aligns with [change-type-rules.md](../references/change-type-rules.md) (error message improvement).

---

## Test-first plan

### Likely test location

`<nearest pandas/tests/.../test_<module>.py after inspection>`

*Placeholder example:* `pandas/tests/frame/test_<something>.py` — replace after `git grep` / `rg` finds existing coverage for `some_method`.

### Why this location

Existing tests for `DataFrame.some_method` (or the relevant frame API) should live in the same directory as related frame tests. Adding the regression test next to related cases keeps pandas test organization consistent and makes review easier.

### Test to add or update

Add a new test, e.g. `test_some_method_invalid_args_raises_clear_error`, that:

1. Builds a minimal DataFrame fixture (same shape as the reproduction)
2. Calls `some_method` with the incompatible arguments from the issue
3. Asserts `ValueError` is raised
4. Asserts the message matches an expected pattern using `pytest.raises(..., match=...)`

Example sketch (illustrative — not verified against real pandas API):

```python
def test_some_method_invalid_args_raises_clear_error():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    with pytest.raises(ValueError, match=r"other.*invalid|expected"):
        df.some_method(axis="columns", other="invalid")
```

Include a comment with the GitHub issue number when available:

```python
# GH-XXXXX
```

### Targeted command

```bash
pytest <nearest pandas/tests/.../test_<module>.py> -k "test_some_method_invalid_args_raises_clear_error"
```

### Expected first result

**Before** the error-message fix: the test should **fail** — either the message does not match `match=`, or the current message is too vague to assert reliably (in that case, tighten `match=` after inspecting the current text).

**After** the fix: the test should **pass** with the improved message.

### Notes on exception testing

- Use the **most specific** exception type confirmed in source (`ValueError` assumed here — verify).
- Use `pytest.raises(ValueError, match=r"...")` to check both type and message.
- Prefer a regex that captures the essential clarity improvement, not the entire string verbatim, unless the message is stable and short.
- Do not use broad `Exception` or bare `pytest.raises(Exception)`.
