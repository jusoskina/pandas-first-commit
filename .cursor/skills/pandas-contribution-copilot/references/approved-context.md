# Approved context

## When to use this reference

Use at the start of any contribution session and before proposing implementation details. Read again when the assistant is about to suggest code changes, cite pandas behavior, or expand beyond files the user has shared.

---

## Purpose

Approved context boundaries keep suggestions grounded in inspectable, trustworthy sources. They reduce hallucinated pandas internals and prevent copy-paste from unrelated codebases.

**Rule:** Do not propose pandas-internal implementation details before inspecting relevant local files or approved docs.

---

## Approved context

| Source | Use for |
|--------|---------|
| Local pandas repository | Implementation, tests, style, nearby patterns |
| Pandas development/contribution docs | PR norms, setup, testing conventions |
| Pandas API/user docs | Expected public behavior, doc cross-refs |
| Files near the affected implementation | The actual change surface |
| Nearby tests | Test location, assertion patterns, fixtures |
| Issue/PR text from the user | Scope, expected behavior, maintainer guidance |
| GitHub metadata | Only if supplied by the user or fetched via approved tooling |

---

## Approved pandas documentation context

Prefer local documentation from the checked-out pandas repository before using external web docs.

Approved local docs:
- `doc/source/`
- `doc/source/development/`
- `doc/source/reference/`
- `doc/source/user_guide/`
- `doc/source/getting_started/`
- `doc/source/whatsnew/`
- top-level repo files such as:
  - `CONTRIBUTING.md`
  - `README.md`
  - `pyproject.toml`
  - `environment.yml`

Approved online docs, only if local docs are missing or unavailable:
- pandas official documentation: `https://pandas.pydata.org/docs/`
- pandas GitHub repository: `https://github.com/pandas-dev/pandas`

Do not use random blogs, Stack Overflow, unrelated repos, or copied code examples unless the user explicitly approves them.

## Disallowed context

Do **not** rely on:

- [ ] Random blogs or tutorials
- [ ] Stack Overflow snippets
- [ ] Code from unrelated repositories
- [ ] Unverified model memory of pandas internals
- [ ] External implementation examples unless the user explicitly approves them

If tempted to use disallowed context, stop and inspect the local repo or ask the user.

---

## Recommended repo inspection commands

Run these in the local pandas checkout before suggesting changes:

```bash
# Find symbols, error strings, or API names
git grep "search_term" -- pandas/

# Faster ripgrep search (if available)
rg "search_term" pandas/

# See what you have changed so far
git status
git diff
git diff upstream/main...HEAD --name-only
```

**Search targets:**

- Function, method, class, or error message being changed
- Existing tests covering related behavior
- Related docstrings or `doc/` pages
- Release-note / whatsnew patterns for user-facing changes

**Scope rule:** Search narrowly. Do not scan the whole repo without reason.

---

## Missing context response template

When context is insufficient, use this template instead of guessing:

```markdown
I do not have enough repo context to safely suggest an implementation yet. I need to inspect:

- <file or module area, e.g. pandas/io/parsers/readers.py>
- <nearby test file, e.g. pandas/tests/io/parser/test_*.py>
- <issue text or minimal reproducible example from the user>

Should I inspect these files in your local checkout?
```

If the user has no local checkout, ask them to paste the relevant file snippets or open the pandas repo as the workspace.
