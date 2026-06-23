# Contribution workflow

## When to use this reference

Use as the step-by-step playbook after intake. Follow stages in order unless the user explicitly asks to jump ahead. Revisit a stage if scope, risk, or context changes.

---

## Intake questions

Ask before starting workflow stages:

1. **Experience:** First pandas contribution or returning contributor?
2. **Change:** What issue, bug, failing example, or intended change are you working on?
3. **Type:** What contribution type do you think this is? (docs / test / bug fix / error message / behavior clarification / not sure)
4. **Environment:** Do you have a local pandas checkout open?
5. **Depth:** Planning only, or planning plus code/test scaffolding?

**Do not** recommend or select a new issue unless the user explicitly asks. If they ask for issue-finding help, give general suitability guidance only and ask them to return with a specific issue.

---

## Global rules

- **Code behavior changes:** Plan tests before implementation. A failing regression test should exist (or be outlined) before scaffolding the fix.
- **Docs-only changes:** Do not force code tests. Define docs checks instead (see stage 4 and 6).
- **Scope:** One issue or one clear improvement per branch.
- **Honesty:** Do not claim checks passed unless they were run and results are visible.

---

## Stage 1 — Clarify the change

| | |
|---|---|
| **Objective** | Restate the contribution in plain language and lock scope. |
| **Inputs needed** | Issue link/text, failing example, or user description of intended change. |
| **Expected output** | Change clarification block (template in [role-output-templates.md](role-output-templates.md)). |
| **Stop if** | Current vs expected behavior is unclear → ask for a minimal reproducible example. Change is too broad → narrow scope before continuing. |

---

## Stage 2 — Inspect local context

| | |
|---|---|
| **Objective** | Find implementation, tests, and docs near the affected behavior. |
| **Inputs needed** | Local pandas checkout; approved context only ([approved-context.md](approved-context.md)). |
| **Expected output** | List of relevant files, existing test locations, and any open questions from inspection. |
| **Stop if** | Required files are not accessible → use missing-context template. Do not propose internals without inspection. |

---

## Stage 3 — Classify risk

| | |
|---|---|
| **Objective** | Set risk level and compatibility/CI expectations before editing. |
| **Inputs needed** | Change type, files touched (or likely), contribution type rules ([change-type-rules.md](change-type-rules.md)). |
| **Expected output** | Risk classification block (template in [role-output-templates.md](role-output-templates.md)). |
| **Stop if** | Risk is high or unclear → narrow scope or ask maintainer/issue author first. Default to narrowing when uncertain. |

---

## Stage 4 — Plan test-first work

| | |
|---|---|
| **Objective** | Define the smallest test or docs check that validates the change. |
| **Inputs needed** | Inspected test files; contribution type. |
| **Expected output** | Test-first plan with targeted `pytest` command and expected first result. |

**For code/test contributions:**

1. Identify the most relevant existing test file.
2. Add or update the smallest failing regression test.
3. Include GitHub issue number in a comment when available.
4. Use `pandas._testing` helpers where appropriate.
5. Use `pytest.raises(..., match=...)` for exceptions.
6. Use warning assertion helpers for warning changes.
7. No public network in unit tests.
8. Prefer parametrized pytest for simple input combos.
9. Use Hypothesis only when input domain complexity justifies it.

**For docs-only contributions:**

- [ ] Define which docs pages or docstrings change
- [ ] Plan `./ci/code_checks.sh docstrings`, `doctests`, and `code` as applicable
- [ ] Do not invent a code test unless behavior is ambiguous and a test would clarify it

**Stop if** | No test location found → search more or ask user before implementing.

---

## Stage 5 — Scaffold minimal implementation

| | |
|---|---|
| **Objective** | Produce the smallest change that satisfies the plan. |
| **Inputs needed** | Approved test-first plan from stage 4. |
| **Expected output** | Code, test, or docs diff outline (or actual edits if user requested scaffolding). |

**Implementation checklist:**

- [ ] Preserve backwards compatibility unless issue requires otherwise
- [ ] Do not change public signatures without calling out risk
- [ ] No broad refactors
- [ ] Match nearby code style
- [ ] One bug/feature/docs change per branch
- [ ] Use pandas optional-dependency helpers when relevant
- [ ] Update docs/docstrings for user-facing behavior
- [ ] Do not suppress warnings or tests to pass CI

Type-specific rules: [change-type-rules.md](change-type-rules.md).

**Stop if** | Test-first plan is missing for a behavior change → return to stage 4.

---

## Stage 6 — Run or recommend checks

| | |
|---|---|
| **Objective** | Suggest targeted local checks; run them only if environment allows. |
| **Inputs needed** | List of changed files; contribution type. |
| **Expected output** | Exact commands with no claim of success unless run. |

**Always suggest for code/test changes:**

```bash
pytest <relevant-test-path> -k "<keyword>"
pre-commit run --files <changed-files>
```

**Broader readiness (optional):**

```bash
pre-commit run --from-ref=upstream/main --to-ref=HEAD --all-files
```

**Docs/docstrings:**

```bash
./ci/code_checks.sh docstrings
./ci/code_checks.sh doctests
./ci/code_checks.sh code
```

**Deterministic guardrail (if available in repo):**

```bash
python scripts/check_pandas_contribution.py --base upstream/main
```

---

## Stage 7 — Review PR readiness

| | |
|---|---|
| **Objective** | Verify the contribution meets pandas PR expectations before opening. |
| **Inputs needed** | Final diff scope; check results (if any). |
| **Expected output** | PR readiness check (template in [role-output-templates.md](role-output-templates.md)). |
| **Stop if** | Critical checklist items fail → address before PR. |

---

## Stage 8 — Generate PR package

| | |
|---|---|
| **Objective** | Produce title, description, and reviewer notes. |
| **Inputs needed** | Completed readiness review. |
| **Expected output** | Suggested PR title and description (template in [role-output-templates.md](role-output-templates.md)). |

---

## Stage 9 — Generate role-specific outputs

| | |
|---|---|
| **Objective** | Hand off summaries for Engineering, PM, QA, and DevOps. |
| **Inputs needed** | All prior stage outputs. |
| **Expected output** | Four role summaries using placeholders only — no invented facts. |

Templates: [role-output-templates.md](role-output-templates.md).

Produce role outputs after a completed plan or PR readiness review.
