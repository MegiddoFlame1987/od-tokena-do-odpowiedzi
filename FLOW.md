# Flow in this repository

This repository follows Mazor Studio Flow v1. The rules live in one file in the hub
repository: `flow/FLOW.md` in `MegiddoFlame1987/mozar-studio`. The short version:

- Tasks arrive by email through the orchestrator and must carry `REPO`, `ZADANIE`,
  `PRIORYTET` and `KRYTERIUM` (what "done" means). No criterion, no task.
- An agent writes, never merges. Every change is a pull request.
- `.github/workflows/flow-checks.yml` runs the checks in GitHub Actions: the level,
  the suppression-comment block, the tests and the linter this repository has.
- `flow/classify.py` sets the level from the changed paths: `standard` for code,
  content, docs and new tests; `elevated` for `.github/`, CI, secrets, auth,
  dependencies, data schema, changed or deleted tests. The agent cannot lower it.
- A separate read-only QC session verifies the exact commit and posts `verdict: PASS`
  or `verdict: FAIL`.
- Norbert accepts with a comment line `ACCEPT <TASK-ID>` (plus ` GOVERNANCE` when the
  level is elevated) and merges by hand. Auto-merge is off.

These files are installed and updated by `python flow/init.py <repo>` in the hub
repository, always through a pull request. Edit them there, not here.
