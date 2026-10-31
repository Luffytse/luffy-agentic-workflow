# agentic-review eval

A small fixture pull request with planted problems of known Bug classes (one of them a break of the fixture's own `REVIEW.md` Always check line), plus two plausible false alarms, to check that `agentic-review` reports the right Findings with the right Severity and drops the false ones. Rerun it whenever `agentic-review` changes, at Standard and at Deep depth. A Verify-only check hands the Verifier the false alarms and two real controls as candidates, so Verify's drop call is tested even when no Finder raises them; run it whenever `VERIFY.md` changes, alongside the full runs.

## Files

- `base/`: the fixture repo before the change (a tiny Python cost splitter with its own `docs/index.md` and a `REVIEW.md` holding one Always check line, which the change breaks once).
- `after/`: the files the change adds or edits; `setup.sh` also deletes `docs/currency.md` (renamed to `docs/money.md`).
- `SPEC.md`: the ticket the change builds; `setup.sh` copies it, untracked, to `.scratch/SPEC.md` in the scratch repo.
- `EXPECTED.md`: the planted Findings (Bug class, Severity, every location), the false alarms, the known extras, how a run is scored, and the scoring of the Verify-only check.
- `VERIFY-ONLY.md`: the candidate Findings handed to the Verifier in the Verify-only check, in the fixed Finding format, each tagged with its Finder.
- `RESULTS.md`: one entry per run.

## How to run

1. Build the fixture as a scratch repo outside this one: `evals/agentic-review/setup.sh <new-empty-dir>`. Branch `main` holds `base/`; branch `planted` adds one commit with the change.
2. In a fresh session in that directory, ask for a Standard Review: "Run agentic-review at Standard depth on branch planted since main, spec at .scratch/SPEC.md". It is a single Review over a fixed point, so no pull request or Round comment is needed.
3. Repeat in another fresh session at Deep depth.
4. Compare each report with `EXPECTED.md` and add an entry to `RESULTS.md`. Keep `EXPECTED.md` and `VERIFY-ONLY.md` away from the reviewing session: run it in the scratch repo, not in this one. `VERIFY-ONLY.md` would prime the Finders.

## Verify-only check

Run it whenever `VERIFY.md` changes, alongside the full runs. In the full runs no Finder has raised F1 or F2 so far, so their rows read "never raised" and a `VERIFY.md` change that stops dropping false alarms would still pass. This check is what makes such a change fail the eval. It catches a `VERIFY.md` change that makes the Verifier keep false alarms; a merely weaker drop rule can still pass, because the Verifier drops claims that plainly do not hold (see the 0.22.13 runs in `RESULTS.md`).

1. Build the fixture with `setup.sh` as above (a new scratch repo, or the full runs' one if it is still clean).
2. In a fresh session, start one brand-new Verifier subagent on the regular tier (Standard). Its brief is the Verifier brief from `VERIFY.md`, word for word, and it gets what `VERIFY.md` says every Verifier gets:
   - all candidate Findings: the contents of `VERIFY-ONLY.md`, pasted as the candidates with their Finder tags; never the file's path or name;
   - open Importants: none;
   - the diff commands, run in the scratch repo on branch `planted`: `git diff --merge-base main` and `git log --oneline main..planted`, with `main` as the base for `git show main:<file>`;
   - the spec, `.scratch/SPEC.md`;
   - the standards list (the fixture's `REVIEW.md`; it has no `CLAUDE.md`, `AGENTS.md` or `CODING_STANDARDS.md`) and the fixture's `REVIEW.md` with its Always check line;
   - the meaning of Important: the fixture's `REVIEW.md` keeps the default one in `agentic-review`'s `SKILL.md`, so pass that text.
3. Repeat in another fresh session with three brand-new Verifiers, one per Deep stance from `VERIFY.md` added to the same brief, and combine their votes by `VERIFY.md`'s rules.
4. Score each result with the Verify-only section of `EXPECTED.md` and record it in `RESULTS.md`. The Verifiers work in the scratch repo and read only their brief; none of them sees this README, `EXPECTED.md` or `RESULTS.md`.

The fixture's own tests pass (`python3 -m unittest` in the scratch repo): the planted bugs are the kind tests miss.
