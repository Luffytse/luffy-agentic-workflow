# agentic-review eval

A small fixture pull request with planted problems of known Bug classes (one of them a break of the fixture's own `REVIEW.md` Always check line), plus two plausible false alarms, to check that `agentic-review` reports the right Findings with the right Severity and drops the false ones. Rerun it whenever `agentic-review` changes, at Standard and at Deep depth. A Verify-only check hands the Verifier the false alarms and two real controls as candidates, so Verify's drop call is tested even when no Finder raises them; run it whenever `VERIFY.md` changes, alongside the full runs.

## Files

- `base/`: the fixture repo before the change (a tiny Python cost splitter with its own `docs/index.md` and a `REVIEW.md` holding one Always check line, which the change breaks once).
- `after/`: the files the change adds or edits; `setup.sh` also deletes `docs/currency.md` (renamed to `docs/money.md`).
- `SPEC.md`: the ticket the change builds; `setup.sh` copies it, untracked, to `.scratch/SPEC.md` in the scratch repo.
- `EXPECTED.md`: the planted Findings (Bug class, Severity, every location), the false alarms, the known extras, how a run is scored, and the scoring of the Verify-only check.
- `VERIFY-ONLY.md`: the candidate Findings handed to the Verifier in the Verify-only check, in the fixed Finding format, each tagged with its Finder.
- `setup.sh`: builds the fixture as a scratch repo.
- `briefs.sh`: builds the Finder and Verifier briefs from the current `FINDERS.md` and `VERIFY.md`, whole, so nobody cuts them out by hand.
- `RESULTS.md`: one entry per run.

## How to run

A run is: build the fixture, build the briefs, start the agents, score.

1. Build the fixture as a scratch repo outside this one: `evals/agentic-review/setup.sh <new-empty-dir>`. Branch `main` holds `base/`; branch `planted` adds one commit with the change.
2. Build the briefs: `evals/agentic-review/briefs.sh <scratch-repo> standard` (or `deep`). It writes them to `<scratch-repo>.briefs/<depth>/`, outside the scratch repo, each file complete: one per Finder, the shared part, and the Verifier brief (at Deep one per stance), taken word for word from the current `FINDERS.md` and `VERIFY.md`. The adversarial angles are the ones every run so far used (Standard: bugs and edge cases plus security and privacy; Deep: bugs and edge cases plus money, numbers and time); name two others as the last two arguments.
3. Start every Finder as a brand-new subagent on its tier from [`FINDERS.md`](../../plugins/dev-skills/upstream-skills/agentic-review/FINDERS.md), each given one brief file and told to read only that and the scratch repo. Merge their candidates, tag each with its Finder, paste them into the `verifier*.md` placeholder, and start the Verifier(s). At Deep, `finder-gap-sweep.md` runs after Verify, with the kept Findings pasted in. Apply the Rank rules of `agentic-review`.
4. Repeat at the other depth.
5. Compare each report with `EXPECTED.md` and add an entry to `RESULTS.md`. Keep `EXPECTED.md` and `VERIFY-ONLY.md` away from the reviewing agents: they work in the scratch repo, not in this one. `VERIFY-ONLY.md` would prime the Finders.

If the Review runs as a fresh session that does its own Find and Verify, ask it for a Standard Review instead: "Run agentic-review at Standard depth on branch planted since main, spec at .scratch/SPEC.md". It is a single Review over a fixed point, so no pull request or Round comment is needed.

## Verify-only check

Run it whenever `VERIFY.md` changes, alongside the full runs. In the full runs no Finder has raised F1 or F2 so far, so their rows read "never raised" and a `VERIFY.md` change that stops dropping false alarms would still pass. This check is what makes such a change fail the eval. It catches a `VERIFY.md` change that makes the Verifier keep false alarms; a merely weaker drop rule can still pass, because the Verifier drops claims that plainly do not hold (see the 0.22.13 runs in `RESULTS.md`).

1. Build the fixture with `setup.sh` as above (a new scratch repo, or the full runs' one if it is still clean).
2. Build the briefs: `evals/agentic-review/briefs.sh --verify-only <scratch-repo> standard`. It writes `<scratch-repo>.briefs/standard-verify-only/verifier.md`: the Verifier brief from `VERIFY.md`, word for word, with the inputs `VERIFY.md` says every Verifier gets: all candidate Findings (the contents of `VERIFY-ONLY.md`, pasted with their Finder tags, never the file's path or name), no open Importants, the diff commands in the scratch repo on branch `planted` (`git diff --merge-base main`, `git log --oneline main..planted`, `main` as the base for `git show main:<file>`), the spec `.scratch/SPEC.md`, the fixture's `REVIEW.md` as the standards list and with its Always check line, and the default meaning of Important from `agentic-review`'s `SKILL.md`.
3. In a fresh session, start one brand-new Verifier subagent on the regular tier (Standard), given that file and nothing else.
4. Repeat with `briefs.sh --verify-only <scratch-repo> deep`: three brand-new Verifiers, one per file (`verifier-tracer.md`, `verifier-skeptic.md`, `verifier-spec-checker.md`), each the same brief with one Deep stance from `VERIFY.md`. Combine their votes by `VERIFY.md`'s rules.
5. Score each result with the Verify-only section of `EXPECTED.md` and record it in `RESULTS.md`. The Verifiers work in the scratch repo and read only their brief; none of them sees this README, `EXPECTED.md` or `RESULTS.md`.

The fixture's own tests pass (`python3 -m unittest` in the scratch repo): the planted bugs are the kind tests miss.
