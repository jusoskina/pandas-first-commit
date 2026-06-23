---
name: pandas-contribution-copilot
description: >-
  Use when helping a new or returning contributor make a small, safe pandas
  contribution from an issue or change they have already chosen. Guides through
  clarifying the change, inspecting approved repo context, planning test-first
  implementation, scaffolding code/docs/tests, checking PR readiness, and
  producing handoff notes for Engineering, PM, QA, and DevOps. Best suited to
  docs updates, error message improvements, regression tests, small bug fixes,
  and behavior clarifications. Use when the user mentions pandas contribution,
  first PR, good first issue, or pandas open source.
---

# pandas Contribution Copilot

## Purpose

Help a new or returning engineer make a small, safe pandas-style contribution without needing to understand the whole pandas codebase first.

This skill assumes the contributor already has an issue, bug, failing example, or intended change. It does not select issues automatically.

The skill turns pandas contribution conventions into a guided workflow for:

- clarifying the intended change
- understanding the relevant area of the repo
- planning the smallest safe contribution
- writing or updating tests first
- scaffolding code, docs, or test changes
- checking PR readiness before review
- producing summaries for Engineering, PM, QA, and DevOps

The goal is not to automate pandas development end to end. The goal is to reduce ramp time, prevent avoidable review churn, and help the contributor move a change safely toward review and CI.

## Suitable issue types

This skill works best when the chosen issue or change is small, clear, and testable.

**Good fit:**

- documentation improvements
- docstring improvements
- small error message improvements
- small bug fixes with regression tests
- adding or strengthening tests
- clarifying existing behavior with tests/docs
- small cleanup changes when clearly scoped

**Good first contribution signals:**

- labelled or described as docs, tests, or good first issue
- unassigned or clearly available
- has a clear reproduction example
- has a clear expected behavior
- touches a narrow part of the codebase
- likely has nearby existing tests
- does not require broad API design discussion

**Use caution with:**

- public API changes
- backwards compatibility changes
- deprecations
- optional dependency changes
- typing changes
- performance-sensitive changes

**Treat as out of scope for a first contribution** unless explicitly requested and justified:

- Cython or compiled extension work
- large refactors
- broad indexing internals
- major API design
- release engineering
- dependency upgrades
- performance rewrites
- changes without a clear issue, test, or user-facing reason

## Approved context boundaries

Use only approved context unless the user explicitly expands the boundary.

**Approved context:**

- the local pandas repository
- pandas development and contribution documentation
- pandas user/API documentation
- files in the relevant pandas module
- existing tests near the affected behavior
- issue or PR text supplied by the user
- GitHub issue metadata supplied by the user or available through an approved tool

**Do not rely on:**

- random blog posts
- Stack Overflow snippets
- code copied from unrelated repositories
- unverified memory of pandas internals
- external implementation examples unless the user explicitly approves them

When uncertain, say what context is missing and ask whether to inspect the relevant repo files or docs.

## Starting workflow

Start by clarifying what the contributor already has.

Ask:

1. Is this your first pandas contribution?
2. What issue, bug, failing example, or change are you working on?
3. What type of contribution do you think this is?
   - docs
   - test
   - bug fix
   - error message
   - behavior clarification
   - not sure
4. Are you working in a local pandas checkout?
5. Do you want help planning only, or planning plus code/test scaffolding?

Do not recommend or select a new issue unless the user explicitly asks for help finding one. If the user does ask for help finding one, provide only general guidance on suitable issue types and ask them to bring back a specific issue.

## Contribution workflow

Follow this sequence.

### 1. Clarify the change

Before editing code, restate the intended contribution.

Output:

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

If the current and expected behavior are unclear, ask for a minimal reproducible example before proposing code.

If the change is too broad, narrow it before proceeding.

### 2. Inspect relevant context

Inspect only approved context.

Prefer:

- existing implementation near the affected behavior
- nearby tests
- documentation for the affected API
- pandas contribution guidance
- issue text supplied by the user

Use search commands such as `git grep`, `rg`, or IDE search to find:

- the function, method, class, or error message being changed
- existing tests that cover related behavior
- related docstring or documentation pages
- release note or whatsnew patterns if user-facing behavior changes

Do not scan the whole repo unnecessarily.

Do not propose implementation details for pandas internals without inspecting the relevant files.

### 3. Classify risk

Before implementation, classify the change.

Output:

```markdown
## Risk classification

Risk level: Low / Medium / High

Reason:
- <reason>

Backwards compatibility:
- No known compatibility risk / Possible compatibility risk / Compatibility risk requires maintainer input

CI impact:
- Targeted tests only / Broader pandas test impact / Unknown

Recommendation:
- Proceed / Narrow scope first / Ask maintainer or clarify issue first
```

Default to narrowing scope when risk is unclear.

### 4. Plan test-first work

For code behavior changes, tests come before implementation.

Use this sequence:

1. Identify the most relevant existing test file.
2. Add or update the smallest failing regression test.
3. Include the GitHub issue number as a comment when available.
4. Use pandas testing helpers where appropriate, such as `pandas._testing` assertion helpers.
5. Use `pytest.raises(..., match=...)` for exception type and message checks.
6. Use warning assertion helpers where the contribution is specifically about warnings.
7. Avoid public network access in unit tests.
8. Prefer parametrized pytest tests for simple input combinations.
9. Use Hypothesis only when the input domain is complex enough to justify it.

If the change is docs-only, define the documentation check instead of forcing a code test.

Output:

```markdown
## Test-first plan

### Likely test location
<path>

### Why this location
<brief reason based on nearby tests or pandas test organization>

### Test to add or update
<plain-English test description>

### Targeted command
```bash
pytest <path> -k "<test_name_or_keyword>"
```

### Expected first result
The test should fail before the implementation change if this is a behavior bug.
```

### 5. Scaffold implementation

Only scaffold implementation after the test-first plan.

Keep changes small.

**Implementation rules:**

- preserve backwards compatibility unless the issue explicitly requires a breaking change
- do not change public signatures without calling out the compatibility risk
- avoid broad refactors
- follow nearby code style rather than inventing a new style
- keep branch scope specific to one bug, feature, or docs change
- use pandas optional dependency helpers for optional dependencies
- add or update docs/docstrings when user-facing behavior changes
- do not suppress warnings or tests just to make CI pass

**When changing exceptions:**

- use the most specific exception type
- test the message with `match=...`
- avoid broad `Exception`

**When changing warnings:**

- use pandas warning test helpers or established nearby patterns
- verify both warning category and message where relevant

**When changing docs/docstrings:**

- follow NumPy docstring convention
- use pandas/Sphinx cross-reference style where nearby docs do so
- include examples only when they clarify behavior
- keep examples executable where possible

### 6. Run or recommend local checks

Suggest checks based on changed files.

Always suggest a targeted test command for code/test changes.

Common checks:

```bash
pytest <relevant-test-path> -k "<keyword>"
pre-commit run --files <changed-files>
```

For broader readiness, suggest:

```bash
pre-commit run --from-ref=upstream/main --to-ref=HEAD --all-files
```

For docs/docstrings where relevant, suggest pandas code/doc checks such as:

```bash
./ci/code_checks.sh docstrings
./ci/code_checks.sh doctests
./ci/code_checks.sh code
```

Do not claim checks passed unless they were actually run and results are available.

If checks cannot be run, say so and provide the exact commands the contributor should run.

### 7. PR readiness review

Before the contributor opens a PR, review the contribution against this checklist.

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
- [ ] Relevant pandas code/doc check suggested where applicable
- [ ] CI risk summarized

### PR communication
- [ ] PR title uses a pandas-style prefix such as BUG, DOC, TST, ENH, PERF, TYP, CLN, or BLD
- [ ] PR references the issue if non-trivial
- [ ] PR description explains what changed, why, and how it was tested
```

### 8. Generate PR package

When ready, produce a concise PR package.

```markdown
## Suggested PR title
<BUG/DOC/TST/etc: concise title>

## PR description

### What changed
- <item>

### Why
- <item>

### Tests
- <commands run or recommended>

### Risk
- <low/medium/high and why>

### Notes for reviewers
- <anything worth calling out>
```

## Multi-role outputs

For every completed plan or PR readiness review, produce role-specific outputs.

**Engineering summary**

```markdown
## Engineering summary
- Contribution type:
- Files likely changed:
- Key implementation decision:
- Tests added/updated:
- Commands run or recommended:
- Remaining technical risk:
```

**PM summary**

```markdown
## PM summary
- User-facing problem:
- User-facing impact:
- Scope:
- Non-scope:
- Release note needed? Yes/No/Unclear
- Business value:
```

**QA notes**

```markdown
## QA notes
- Behavior to validate:
- Regression cases:
- Edge cases:
- Manual checks, if any:
- Automated test coverage:
```

**DevOps / CI notes**

```markdown
## DevOps / CI notes
- CI jobs likely affected:
- Dependencies touched:
- Network/file-system sensitivity:
- Performance sensitivity:
- Guardrails:
- Merge readiness:
```

## Maintainability rules

Keep this skill maintainable.

- Do not encode large copies of pandas documentation in this file.
- Prefer short rules and links/references to external docs or local reference files.
- When a rule is inferred from current pandas docs, state it as a checkable behavior, not a vague principle.
- If pandas contribution guidance changes, update the relevant rule or move detailed rules into a reference file.
- Keep supported contribution types explicit.
- Keep out-of-scope areas explicit.
- Prefer deterministic scripts for checks that should not depend on model judgment.
- Do not claim certainty about pandas internals without inspecting the relevant files.

## Failure modes and honest responses

If the assistant lacks enough context, say:

> I do not have enough repo context to safely suggest an implementation yet. I need to inspect:
> - <file or docs area>
> - <nearby tests>
> - <issue text or reproduction>

If the change is too broad, say:

> This is too broad for a safe first contribution. I recommend narrowing it to:
> - <smaller version>

If there is a compatibility concern, say:

> This may affect backwards compatibility. Before implementation, we should either:
> 1. confirm the expected behavior in the issue discussion, or
> 2. limit the change to tests/docs that clarify current behavior.

If the user asks to skip tests for a code behavior change, say:

> For pandas-style contributions, skipping tests is likely to create review churn. I can help narrow the test to the smallest regression case instead.

## Demo script for technical screen

Use this demo path if presenting the artifact live.

1. Start with: "I have chosen a pandas issue and want help making a safe first contribution."
2. Ask for the issue, failing example, or intended change.
3. Clarify expected behavior and contribution type.
4. Identify likely implementation and test locations.
5. Propose a test-first plan.
6. Scaffold a minimal test or test outline.
7. Scaffold the smallest implementation or docs change.
8. Run or recommend targeted checks.
9. Produce:
   - PR readiness check
   - suggested PR title and description
   - Engineering summary
   - PM summary
   - QA notes
   - DevOps / CI notes
10. End the demo by explaining what is intentionally not automated:
    - no automatic issue selection in this version
    - no broad autonomous coding
    - no unapproved external context
    - no deep internals without explicit inspection
    - no claim that CI passed unless checks were run
    - no replacement for maintainer review
