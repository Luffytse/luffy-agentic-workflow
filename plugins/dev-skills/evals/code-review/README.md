# code-review eval

A small fixture pull request with planted problems of known Bug classes, plus two plausible false alarms, to check that `code-review` reports the right Findings with the right Severity and drops the false ones. Rerun it whenever `code-review` changes, at Standard and at Deep depth.

## Files

- `base/`: the fixture repo before the change (a tiny Python cost splitter with its own `docs/index.md`).
- `after/`: the files the change adds or edits; `setup.sh` also deletes `docs/currency.md` (renamed to `docs/money.md`).
- `SPEC.md`: the ticket the change builds; `setup.sh` copies it, untracked, to `.scratch/SPEC.md` in the scratch repo.
- `EXPECTED.md`: the planted Findings (Bug class, Severity, every location), the false alarms, and how a run is scored.
- `RESULTS.md`: one entry per run.

## How to run

1. Build the fixture as a scratch repo outside this one: `plugins/dev-skills/evals/code-review/setup.sh <new-empty-dir>`. Branch `main` holds `base/`; branch `planted` adds one commit with the change.
2. In a fresh session in that directory, ask for a Standard Review: "Run code-review at Standard depth on branch planted since main, spec at .scratch/SPEC.md". It is a single Review over a fixed point, so no pull request or Round comment is needed.
3. Repeat in another fresh session at Deep depth.
4. Compare each report with `EXPECTED.md` and add an entry to `RESULTS.md`. Keep `EXPECTED.md` away from the reviewing session: run it in the scratch repo, not in this one.

The fixture's own tests pass (`python3 -m unittest` in the scratch repo): the planted bugs are the kind tests miss.
