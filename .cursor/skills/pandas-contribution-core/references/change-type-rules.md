# Change type rules

## When to use this reference

Use after intake when classifying the contribution type, planning tests/docs, choosing PR title prefixes, and estimating first-contribution fit. Cross-check with `pandas-plan-contribution` (risk + test-first planning).

---

## Quick reference

| Type | First PR fit | PR prefix |
|------|--------------|-----------|
| Docs-only | Good | `DOC` |
| Docstring update | Good | `DOC` |
| Error message improvement | Good | `BUG` or `CLN` |
| Regression test | Good | `TST` |
| Small bug fix | Good | `BUG` |
| Behavior clarification | Okay | `TST` or `DOC` |
| Tests-only | Good | `TST` |
| CI/config change | Okay | `BLD` or `CI` |
| Risky internals | Risky | — (avoid for first PR) |

---

## Docs-only

| Field | Guidance |
|-------|----------|
| **First PR fit** | Good |
| **Typical files** | `doc/**/*.rst`, `web/pandas/**/*.md`, root `.md` docs |
| **Tests** | Not required unless clarifying ambiguous behavior |
| **Docs** | The change *is* the docs — verify accuracy and Sphinx refs |
| **Risk notes** | Low if scope is one page/section; watch for behavior claims that contradict code |
| **Suggested checks** | `./ci/code_checks.sh docstrings`, `doctests`, `code`; `pre-commit run --files <files>` |
| **PR prefix** | `DOC` |

---

## Docstring update

| Field | Guidance |
|-------|----------|
| **First PR fit** | Good |
| **Typical files** | `pandas/**/*.py` (docstring only or mostly docstring) |
| **Tests** | Optional; add doctest or unit test if examples are executable |
| **Docs** | Follow NumPy docstring style; match nearby cross-ref patterns |
| **Risk notes** | Low unless docstring change implies undocumented behavior change |
| **Suggested checks** | `./ci/code_checks.sh docstrings`; targeted pytest if examples added |
| **PR prefix** | `DOC` |

---

## Error message improvement

| Field | Guidance |
|-------|----------|
| **First PR fit** | Good |
| **Typical files** | `pandas/**/*.py` where `raise` occurs |
| **Tests** | **Required** — `pytest.raises(ExpectedError, match=r"...")` for type and message |
| **Docs** | Update only if user-facing docs reference the old message |
| **Risk notes** | Medium if message is part of stable public API; tests may need regex updates elsewhere |
| **Suggested checks** | `pytest <nearest-test-file> -k "<keyword>"`; `pre-commit run --files <files>` |
| **PR prefix** | `BUG` (incorrect/misleading message) or `CLN` (clarity only, behavior unchanged) |

**Rules:**

- Use the most specific exception type.
- Test both exception type and message with `match=...`.
- Avoid catching broad `Exception` in tests.

---

## Regression test

| Field | Guidance |
|-------|----------|
| **First PR fit** | Good |
| **Typical files** | `pandas/tests/**/*.py` |
| **Tests** | The contribution — one focused test reproducing reported behavior |
| **Docs** | Only if test documents previously unclear intended behavior |
| **Risk notes** | Low if test matches issue reproduction; avoid testing private internals |
| **Suggested checks** | `pytest <new-or-updated-test-file>`; `pre-commit run --files <files>` |
| **PR prefix** | `TST` |

---

## Small bug fix

| Field | Guidance |
|-------|----------|
| **First PR fit** | Good (with regression test) |
| **Typical files** | `pandas/**/*.py` + matching `pandas/tests/**/*.py` |
| **Tests** | **Required** — failing test first, then fix |
| **Docs** | Update docstrings/docs/release notes if user-facing behavior changes |
| **Risk notes** | Medium if fix touches compatibility, dtypes, indexing, or NA handling |
| **Suggested checks** | Targeted `pytest`; `pre-commit`; consider whatsnew entry if user-visible |
| **PR prefix** | `BUG` |

**Rules:**

- Test before fix.
- Preserve backwards compatibility unless issue/maintainer requires otherwise.
- Call out compatibility risk explicitly in PR description.

---

## Behavior clarification

| Field | Guidance |
|-------|----------|
| **First PR fit** | Okay |
| **Typical files** | Tests and/or docs; minimal code if behavior was always intended |
| **Tests** | Preferred — test encodes the clarified contract |
| **Docs** | Update when clarification is user-facing |
| **Risk notes** | Medium — "clarification" may reveal a bug or breaking change |
| **Suggested checks** | Targeted `pytest`; docs checks if docs updated |
| **PR prefix** | `TST` (test clarifies behavior) or `DOC` (docs only) |

If clarification would change long-standing behavior, ask maintainer in issue before implementing.

---

## Tests-only contribution

| Field | Guidance |
|-------|----------|
| **First PR fit** | Good |
| **Typical files** | `pandas/tests/**/*.py` |
| **Tests** | Add, strengthen, or parametrize existing coverage |
| **Docs** | Rarely needed |
| **Risk notes** | Low if narrow; medium if many files or flaky-test territory |
| **Suggested checks** | `pytest <changed-test-files>`; `pre-commit run --files <files>` |
| **PR prefix** | `TST` |

---

## CI/config change

| Field | Guidance |
|-------|----------|
| **First PR fit** | Okay (not ideal for very first PR) |
| **Typical files** | `.github/`, `ci/`, `pyproject.toml`, `setup.py`, `environment.yml` |
| **Tests** | Not always applicable; verify CI config validity |
| **Docs** | Update contributor docs if workflow changes for contributors |
| **Risk notes** | Medium–high — affects all CI; needs DevOps/maintainer awareness |
| **Suggested checks** | Validate config locally if possible; `pre-commit`; note which CI jobs change |
| **PR prefix** | `BLD` or `CI` |

Warn contributor that maintainer review may take longer.

---

## Risky internals

| Field | Guidance |
|-------|----------|
| **First PR fit** | **Risky** — avoid unless explicitly scoped and maintainer-involved |
| **Typical files** | `pandas/_libs/**`, `*.pyx`, `*.pxd`, `core/indexes`, `core/internals`, `core/groupby` |
| **Tests** | Required and often complex; may need build step |
| **Docs** | Unlikely for internal-only changes |
| **Risk notes** | High — Cython, memory layout, performance, subtle regressions |
| **Suggested checks** | Full targeted test module; local build; expect broad CI |
| **PR prefix** | Varies — prefer not starting here |

**Rules:**

- Recommend narrowing scope or asking maintainer for clarification first.
- Do not propose Cython/internals changes without reading the actual files.
- Flag high risk in PR description and DevOps notes.

---

## Cross-cutting rules

### Warnings

- Test warning **category** and **message** where relevant.
- Use pandas warning test helpers or patterns from nearby tests.

### User-facing behavior

- Consider docs, docstrings, and release notes (`doc/source/whatsnew/`).
- If behavior changes without docs update, flag in PR readiness check.

### Out of scope for first contribution (unless explicitly requested)

- [ ] Large refactors
- [ ] Public API redesign
- [ ] Deprecations
- [ ] Optional dependency changes
- [ ] Performance rewrites
- [ ] Release engineering
- [ ] Changes without issue, test, or user-facing reason
