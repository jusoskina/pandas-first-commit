# Pandas first commit

Welcome to the pandas first contribution copilot repository.

## Slash commands

Run these from the Cursor command palette (`/`):

| Command | What it does |
|---------|--------------|
| `/pandas-start` | Intake + clarify the change |
| `/pandas-inspect` | Inspect local repo context |
| `/pandas-plan` | Risk classification + test-first plan |
| `/pandas-implement` | Scaffold minimal change |
| `/pandas-verify` | Run checks + PR readiness (auto-continues to ship on success) |
| `/pandas-ship` | PR package + role handoffs |
| `/pandas-full` | Full end-to-end flow (demos) |

## Skills layout

- **Core:** `.cursor/skills/pandas-contribution-core/` — shared rules and templates
- **Stages:** `pandas-clarify-change`, `pandas-inspect-context`, `pandas-plan-contribution`, `pandas-scaffold-change`, `pandas-verify-contribution`, `pandas-ship-contribution`
- **Hub:** `.cursor/skills/pandas-contribution-copilot/` — orchestrator + examples

## Checker script

See [scripts/README.md](scripts/README.md) for `check_pandas_contribution.py`.
