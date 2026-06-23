# Sample first contribution flow

**Example only.** Fictional scenario for demo purposes. No code was run; no CI passed.

## Scenario

A new contributor chose a small pandas issue: a confusing error message when calling a DataFrame operation with incompatible arguments. Goal: clarify the message and add a regression test.

---

## 1. User opens the session

**User:**

> I have chosen a pandas issue and want help making a safe first contribution. It's about a confusing DataFrame error message.

**Assistant:**

> I'll follow the pandas contribution copilot workflow. A few intake questions:
>
> 1. Is this your first pandas contribution?
> 2. Can you share the issue link or describe the failing example?
> 3. What type do you think this is — docs, test, bug fix, error message, or not sure?
> 4. Do you have a local pandas checkout open?
> 5. Do you want planning only, or planning plus scaffolding?

---

## 2. User answers

**User:**

> First contribution. No issue number yet — I reproduced it locally. Calling `df.some_method(wrong_arg)` raises a vague `ValueError`. I think it's an error-message fix. I have pandas cloned. Planning plus scaffolding please.

**User (failing example):**

```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
df.some_method(axis="columns", other="invalid")  # vague error today
```

---

## 3. Assistant clarifies the change

**Assistant output:** See [sample-change-clarification.md](sample-change-clarification.md).

**Assistant (spoken):**

> Before we edit code, I'll restate the change. If this matches your intent, we'll inspect the repo next.

---

## 4. Assistant proposes context to inspect

**Assistant:**

> I need approved local context before suggesting implementation. I'll search for:
>
> - The method raising the error (likely in `pandas/core/` — exact path TBD)
> - Existing tests for this method under `pandas/tests/`
> - Whether docs mention this error
>
> Suggested commands:
>
> ```bash
> git grep "some_method" -- pandas/
> rg "some_method" pandas/tests/
> ```
>
> Should I inspect these in your checkout?

**User:**

> Yes, go ahead.

**Assistant (after inspection — illustrative):**

> Found implementation near `<pandas/core/...>` and tests in `<pandas/tests/.../test_*.py>`. Ready to plan the test first.

---

## 5. Assistant plans test-first work

**Assistant output:** See [sample-test-first-plan.md](sample-test-first-plan.md).

**Assistant (spoken):**

> We'll add a failing test that asserts the exception type and message before changing the raise statement.

---

## 6. Assistant suggests implementation constraints

**Assistant:**

> **Scaffolding constraints for this change:**
>
> - Keep the same exception type (`ValueError`) unless the issue says otherwise
> - Improve message clarity only — no signature or behavior change
> - Match wording style of nearby errors in the same module
> - Do not refactor surrounding code
> - Include issue reference in test comment when you have a GitHub issue number

---

## 7. Assistant recommends local checks

**Assistant:**

> **Recommended commands** (not run in this example):
>
> ```bash
> pytest <nearest-test-file> -k "test_error_message"
> pre-commit run --files <changed-files>
> python scripts/check_pandas_contribution.py --base upstream/main
> ```
>
> I have not run these. Please run locally and share results if you want help interpreting failures.

---

## 8. Assistant produces PR package and role outputs

**Assistant:**

> **Suggested PR title:** `CLN: clarify error message for DataFrame.some_method with invalid arguments`
>
> **PR description:** See [sample-pr-readiness-report.md](sample-pr-readiness-report.md) and role outputs in [sample-role-outputs.md](sample-role-outputs.md).
>
> **Checker output (illustrative):** [sample-checker-output.md](sample-checker-output.md)

---

## 9. Demo closing (assistant)

**Assistant:**

> **Intentionally not automated in this copilot:**
>
> - No automatic issue selection
> - No unapproved external context
> - No claim that CI passed unless you ran checks
> - No replacement for maintainer review
>
> Next step: run the suggested pytest and checker commands locally, then open the PR.
