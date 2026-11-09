# to-tickets Milestone-signal and unfiled-blocker check

Does `to-tickets` treat a Spec as in a Milestone when its caller says it is planning a feature of a named Milestone whose issue is not written yet (publish the split without asking, Tickets labelled with that Milestone's label), and does it leave `ready-for-agent` off a Ticket whose blocker is planned but not filed, naming that blocker in its report? Bounded publication check for Ticket #56 (absorbs #20 and #28). Local files only; no real issue or network call. The Boundary record's label form is `milestone-<n>`.

## Files

- [`cases.py`](cases.py): the two cases and their expected labels (below), shared by the other scripts.
- [`make_fixture.py`](make_fixture.py): `python3 make_fixture.py <out-dir> <case>` builds a scratch repo (local-files tracker doc, triage-labels, release and Boundary docs, `.scratch/greeter/SPEC.md` with an unapproved breakdown, `PROMPT.md`).
- [`score.py`](score.py): `python3 score.py <out-dir> <case>` reads the labels back from `.scratch/greeter/issues/*.md` and checks `REPORT.txt`, the run's final reply saved by hand.
- [`test_cases.py`](test_cases.py): the scorer's self-test (a reference run per case passes, planted wrong runs fail) and checks that the rendered Spec, prompt and Boundary record say what each case means. It reads no skill or doc text. Run `python3 evals/to-tickets-milestone-signal/test_cases.py`; it prints `ok`.

## Cases

Fixture Spec "greeter" has a proposed breakdown nobody has approved and no label: 01 format a greeting, 02 greet a logged-in user.

| Case | Caller says | 02 blocked by | Expected |
| --- | --- | --- | --- |
| `planning` | it is planning a feature of Milestone 2, issue not written yet | the Hub login feature, planned and not filed | published with no question; 01 `ready-for-agent`, `milestone-2`; 02 `milestone-2` only; report names 02 and Hub login |
| `plain` (control) | nothing | 01 | nothing published; one question asking for approval |

## Run level

Each case: full run in a top-level session or a fresh regular-tier subagent, working directory `<out-dir>`, given only the text of `PROMPT.md`, loading `to-tickets` from the checkout under test (`plugins/dev-skills/skills/to-tickets/SKILL.md`) and the skills it names from the same checkout. Keep this README, `cases.py` and `score.py` away from it. Save its final reply to `<out-dir>/REPORT.txt`, then `python3 score.py <out-dir> <case>`. Run each case on the branch's skill and on main's (`git archive <main sha> plugins | tar -x -C <dir>`). `planning` discriminates (main asks for approval and labels 02 ready); `plain` is a regression guard.

## Run record

None yet: the runs are owed to the Ticket #56 thread.
