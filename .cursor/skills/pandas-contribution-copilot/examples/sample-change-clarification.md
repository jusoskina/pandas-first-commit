# Sample change clarification

**Example only.** Fictional DataFrame error-message contribution. Aligns with [role-output-templates.md](../references/role-output-templates.md).

---

## Change clarification

### User problem

When a user calls `DataFrame.some_method()` with incompatible arguments (e.g. an invalid combination of `axis` and another parameter), pandas raises a `ValueError` with a message that does not explain which argument is wrong or what values are expected. New users struggle to fix their code.

### Expected behavior

pandas raises the same exception type (`ValueError`) but with a clear message that:

- Names the problematic argument or combination
- States what went wrong in plain language
- Does not change successful-path behavior

### Current behavior

Calling the method with incompatible arguments raises `ValueError` with a generic or misleading message (exact text to be confirmed after inspecting the implementation).

```python
# Illustrative reproduction — example only
df.some_method(axis="columns", other="invalid")  # raises vague ValueError
```

### Contribution type

error message improvement (+ regression test)

### Scope

In scope:

- Clarify the error message at the raise site (exact file TBD after repo inspection)
- Add one regression test asserting exception type and message
- Keep change limited to this one error path

Out of scope:

- Changing method signature or public API
- Refactoring the method or related helpers
- Fixing other error messages in the same module
- Documentation site overhaul (docstring tweak only if the public doc references the old message)

### Open questions

- Exact file and line of the `raise` statement — **resolve by inspecting local checkout**
- Is the current exception type definitely `ValueError`, or should it be more specific? — **confirm from source**
- Is there an existing GitHub issue number to reference in the test comment? — **ask contributor**
