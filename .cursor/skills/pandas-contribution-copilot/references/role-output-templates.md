# Role output templates

## When to use this reference

Copy and fill these templates at workflow stages 3, 7, 8, and 9. Replace `<placeholders>` with facts from the actual change — **do not invent details**. If unknown, write `Unknown` or ask the user.

---

## Risk classification

**When:** After inspecting context, before test-first planning (workflow stage 3).

```markdown
## Risk classification

Risk level: <Low | Medium | High>

Reason:
- <reason based on files, type, and scope>

Backwards compatibility:
- <No known compatibility risk | Possible compatibility risk | Compatibility risk requires maintainer input>

CI impact:
- <Targeted tests only | Broader pandas test impact | Unknown>

Recommendation:
- <Proceed | Narrow scope first | Ask maintainer or clarify issue first>
```

---

## Change clarification

**When:** Start of workflow (stage 1), before any code edits.

```markdown
## Change clarification

### User problem
<what problem this solves>

### Expected behavior
<what should happen>

### Current behavior
<what appears to happen now>

### Contribution type
<docs | test | bug fix | error message | behavior clarification | unclear>

### Scope
In scope:
- <item>

Out of scope:
- <item>

### Open questions
- <question, if any>
```

---

## Test-first plan

**When:** After context inspection (stage 4), before implementation.

```markdown
## Test-first plan

### Likely test location
<path>

### Why this location
<brief reason from nearby tests or pandas test layout>

### Test to add or update
<plain-English description>

### Targeted command
pytest <path> -k "<test_name_or_keyword>"

### Expected first result
<For behavior bugs: test should fail before the fix. For docs-only: describe doc check instead.>
```

---

## Checks run report

**When:** End of stage 6 and start of stage 7. **Always show this table explicitly** — do not summarize checks only in prose.

Copy this table and fill every row. Use `PASS`, `FAIL`, `WARN`, `NOT RUN`, or `RECOMMENDED` in the **Result** column.

```markdown
## Checks run report

| Check | Command | Result | Notes |
|-------|---------|--------|-------|
| Targeted pytest | `pytest <path> -k "<keyword>"` | PASS / FAIL / NOT RUN | <e.g. 1 passed in 0.05s> |
| pre-commit | `pre-commit run --files <files>` | PASS / FAIL / NOT RUN | <hooks passed or failing hook name> |
| PR readiness checker | `python3 ../scripts/check_pandas_contribution.py --base main` | PASS / FAIL / WARN / NOT RUN | <exit code; contribution type; risk level> |
| Doc checks (if applicable) | `./ci/code_checks.sh docstrings` etc. | PASS / FAIL / NOT RUN / N/A | |

### Checker summary (if checker ran)

| Item | Value |
|------|-------|
| Base branch | <e.g. main / upstream/main> |
| Changed files | <count> |
| Contribution type | <e.g. code + tests> |
| Risk level | <low / medium / high> |
| Checker failures | <count or 0> |
| Checker warnings | <count or 0> |
```

**Result rules:**

- `PASS` — command ran and succeeded (pytest green, pre-commit hooks passed, checker exit 0 with no FAIL rows)
- `FAIL` — command ran and failed
- `WARN` — checker or review flagged non-blocking issues (e.g. docs warning)
- `NOT RUN` — command not executed; explain why in Notes (e.g. no dev build yet)
- `RECOMMENDED` — command suggested for contributor to run locally; assistant did not run it

**Do not** truncate checker output with `head` or omit the checker row when it was run.

---

## PR readiness check

**When:** Before opening a PR (stage 7).

```markdown
## PR readiness check

### Scope
- [ ] Change is limited to one issue or one clear improvement
- [ ] No unrelated formatting or refactoring
- [ ] Risky internals avoided or explicitly justified

### Tests
- [ ] Test added or updated for code behavior change
- [ ] Test is located near related existing tests
- [ ] Targeted pytest command provided
- [ ] Warning/exception behavior tested with category/type and message where relevant
- [ ] No public network dependency in unit tests

### Docs
- [ ] Docs or docstring updated if user-facing behavior changed
- [ ] Docstring follows pandas / NumPy style where applicable
- [ ] Examples are minimal and accurate

### Compatibility
- [ ] No public API/signature change, or compatibility risk is explicitly called out
- [ ] Deprecation path included if required
- [ ] Optional dependency handling follows pandas conventions if relevant

### CI / guardrails
- [ ] Pre-commit command suggested or run
- [ ] **Checks run report** table shown with pytest, pre-commit, and checker rows
- [ ] PR readiness checker run from pandas repo after commit (or NOT RUN explained)
- [ ] Relevant pandas code/doc check suggested where applicable
- [ ] CI risk summarized

### PR communication
- [ ] PR title uses a pandas-style prefix (BUG, DOC, TST, ENH, PERF, TYP, CLN, BLD)
- [ ] PR references the issue if non-trivial
- [ ] PR description explains what changed, why, and how it was tested
```

---

## PR title and description

**When:** PR package generation (stage 8).

```markdown
## Suggested PR title
<PREFIX: concise title — e.g. DOC: fix read_csv quoting parameter description>

## PR description

### What changed
- <item>

### Why
- <item>

### Tests
- <commands run or recommended — do not claim pass unless verified>

### Risk
- <low/medium/high and why>

### Notes for reviewers
- <anything worth calling out>
```

---

## Engineering summary

**When:** Handoff after plan or readiness review (stage 9). Audience: engineers implementing or reviewing the change.

```markdown
## Engineering summary

- **Contribution type:** <type>
- **Files likely changed:** <paths>
- **Key implementation decision:** <decision or "TBD after inspection">
- **Tests added/updated:** <paths or "None for docs-only">
- **Commands run or recommended:** <commands>
- **Remaining technical risk:** <risk and mitigations>
```

---

## PM summary

**When:** Handoff after plan or readiness review (stage 9). Audience: product/project stakeholders who may not know pandas internals.

Use plain language. Focus on user impact, not implementation.

```markdown
## PM summary

- **User-facing problem:** <what pandas users experience today>
- **User-facing impact:** <what improves for users after merge — or "No user-visible change">
- **Scope:** <what this PR includes>
- **Non-scope:** <what is explicitly not included>
- **Release note needed?** <Yes | No | Unclear>
- **Business value:** <why this matters — reliability, clarity, correctness, etc.>
```

---

## QA notes

**When:** Handoff after plan or readiness review (stage 9). Audience: QA or reviewers validating behavior without deep codebase knowledge.

```markdown
## QA notes

- **Behavior to validate:** <observable behavior in plain terms>
- **Regression cases:** <cases that must still pass>
- **Edge cases:** <inputs, dtypes, NA, empty data, etc. if relevant>
- **Manual checks, if any:** <steps — or "Automated tests sufficient">
- **Automated test coverage:** <test file/command that covers this change>
```

---

## DevOps / CI notes

**When:** Handoff after plan or readiness review (stage 9). Audience: CI/maintainers assessing pipeline impact.

```markdown
## DevOps / CI notes

- **CI jobs likely affected:** <e.g. unit tests, doc build — or "Standard unit test job">
- **Dependencies touched:** <none | optional deps | build deps>
- **Network/file-system sensitivity:** <e.g. tests must not hit network>
- **Performance sensitivity:** <low | medium | high — or "Not performance-related">
- **Guardrails:** <pre-commit, check_pandas_contribution.py, etc.>
- **Merge readiness:** <ready after checks | blocked on X>
```
