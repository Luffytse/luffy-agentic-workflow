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
- `brief-lib.sh`: the helpers `briefs.sh` and `milestone/briefs.sh` share to cut the briefs out of the skill files.
- `milestone/`: the Milestone-agreement check below (`make-fixture.sh`, `test-fixture.sh`, `briefs.sh`, `DESIGN-FINDINGS.md`, `EXPECTED.md`).

## How to run

A run is: build the fixture, build the briefs, start the agents, score.

1. Build the fixture as a scratch repo outside this one: `evals/agentic-review/setup.sh <new-empty-dir>`. Branch `main` holds `base/`; branch `planted` adds one commit with the change.
2. Build the briefs: `evals/agentic-review/briefs.sh <scratch-repo> standard` (or `deep`). It writes them to `<scratch-repo>.briefs/<depth>/`, outside the scratch repo, each file complete: one per Finder, the shared part, and the Verifier brief (at Deep one per stance), taken word for word from the current `FINDERS.md` and `VERIFY.md`. The adversarial angles are the ones every run so far used (Standard: bugs and edge cases plus security and privacy; Deep: bugs and edge cases plus money, numbers and time); name two others as the last two arguments.
3. Start every Finder as a brand-new subagent on its tier from [`FINDERS.md`](../../plugins/dev-skills/skills/agentic-review/FINDERS.md), each given one brief file and told to read only that and the scratch repo. Merge their candidates, tag each with its Finder, paste them into the `verifier*.md` placeholder, and start the Verifier(s). At Deep, `finder-gap-sweep.md` runs after Verify, with the kept Findings pasted in. Apply the Rank rules of `agentic-review`.
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

## Milestone-agreement check

Does a design Finding on a pull request inside a Milestone go to a premium-tier agent when its answer keeps what the user agreed, and to the user when it would change the Milestone's goal, an acceptance criterion or an exclusion; is the answer recorded and the row marked with who answered; and do later Finders leave settled designs alone? Rerun it whenever `agentic-review`'s design-Finding rules (`ROUNDS.md`, "Design Findings"), its settled designs or the `review-record` design-row Notes change. Scoring: [`milestone/EXPECTED.md`](milestone/EXPECTED.md).

The fixture, built by [`milestone/make-fixture.sh`](milestone/make-fixture.sh), is a scratch repo with a Boundary record (label form `milestone-<n>`), a local Markdown tracker with a "Comment on an issue" operation, a Milestone issue and a spec as files under `.scratch/issues/`, and a design-changing pull request (`.scratch/pulls/1.md`, branch `design`: `src/export.sh` and a new ADR) with its Round 1 comment holding two kept-design rows. Case `inside` labels the spec `milestone-1` and has the Round 1 designs kept by an agent, its answers recorded on the spec issue; case `outside` has no label and the user kept them. The two planted design Findings and one text Finding, as Round 2's Verify kept them, are in [`milestone/DESIGN-FINDINGS.md`](milestone/DESIGN-FINDINGS.md). [`milestone/test-fixture.sh`](milestone/test-fixture.sh) builds both cases and their briefs and checks each holds what the check needs; run it after changing the builder.

1. Build each case outside this repo: `bash evals/agentic-review/milestone/make-fixture.sh <out-dir> inside` (and `outside` into another directory). Each makes `<out-dir>/repo` and `<out-dir>/PROMPT.md`.
2. Build the briefs: `bash evals/agentic-review/milestone/briefs.sh <out-dir>` writes `<out-dir>/briefs/`, outside the repo: the Round 2 Finder and Verifier briefs at Standard depth, with the settled designs, and in case `inside` `design-answer-D1.md` and `design-answer-D2.md`, the design-answer brief from `ROUNDS.md` with one planted design Finding each. `--control` writes `<out-dir>/briefs-control/`, the Finder briefs with no settled designs, run against `<out-dir>/repo-control/`, a blind copy of the repo whose spec has no Decisions, comments or sorting exclusion and which has no Round 1 comment (rebuilt on each run).
3. **Design-answer agents** (case `inside`): start one brand-new premium-tier subagent per `design-answer-D*.md`, each given that file and told to read only it and the repo.
4. **Re-raise**: start the four Finders from `<out-dir>/briefs/` (`inside`, and `outside` if you want both), each a brand-new subagent on its tier from `FINDERS.md`, given one file; paste their candidates, tagged with their Finders, into `verifier.md`'s placeholder and start the Verifier. Optionally run the control Finders from `briefs-control/` the same way, each told to read only its file and `<out-dir>/repo-control`.
5. **Decision-level runs** (optional, both cases): give a fresh top-level session that can start subagents the text between the lines of `<out-dir>/PROMPT.md`, with its working directory at `<out-dir>/repo` and `<checkout>` replaced by this checkout's path. Keep `PROMPT.md`'s Expected line away from it.
6. Score with `milestone/EXPECTED.md` and add an entry to `RESULTS.md` with the Milestone-agreement template there, saying which parts ran and how they were driven.

