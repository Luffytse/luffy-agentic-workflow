# triage eval

Checks of the `triage` skill (`plugins/dev-skills/skills/triage/`). Each run gets an entry in [RESULTS.md](RESULTS.md).

## Run level

| Check | Run level |
| --- | --- |
| `backlog-sweep/test_cases.py` | no model session: builds the case and scores a reference run and planted wrong runs |
| the backlog-sweep case | decision-level in a fresh session: every tracker write is a block in `.scratch/proposed-actions.md`, so nothing real is labelled, commented on or closed |

## Backlog-sweep case

[`backlog-sweep/make_fixture.py`](backlog-sweep/make_fixture.py) builds the case outside this repo: `python3 evals/triage/backlog-sweep/make_fixture.py <out-dir>`. It makes `<out-dir>/repo` and `<out-dir>/PROMPT.md`. The repo is the release eval's tiny shell greeter and dry-run local tracker (`evals/release/ranked-pick/make_fixture.py`), with an `Author:` header on each issue and a `duplicate` close outcome. Milestone 1 (#1) lists #10 Farewell (shipped in Release 3) and #20 Quiet flag. Releases 1, 2 and 3 (#2, #3, #4) are closed, each with an Order, a Left out list and its notes; Release 3 was cut just now and has no end-of-Release record yet. The run is its Triage batch, as `release` step 4 runs it. The case data and the expected outcome are in [`backlog-sweep/sweep_case.py`](backlog-sweep/sweep_case.py).

| Issue | Fixture | Expected |
| --- | --- | --- |
| #30, #31 | two `ready-for-agent` bugs reporting the same `helo` typo in the usage line, still on main; #31 is newer | #31 closed as a duplicate (or not planned), linking #30; #30 stays open |
| #32 | `ready-for-agent` bug: `hello` with no name prints `Hello, !`; main defaults the name to `world` since pull request #8, which did not close it | closed as completed (main already does it), with the reason |
| #33 | `ready-for-agent` bug, still true on main, in the Left out lists of Releases 1, 2 and 3 | closed as not planned, saying "reopen to bring it back" |
| #34 | the same, left out of Releases 2 and 3 only | stays open |
| #36 | the same, left out of Releases 1 and 3, not 2 | stays open |
| #20 | the Milestone's planned feature, left out of all three Releases | stays open (never expired) |
| #40 | `ready-for-agent` bug that blocks #20 | gains `next-release` |
| #41 | new at `needs-triage`: every name is written to a world-readable log (true on main) | `bug`, `ready-for-agent` and `next-release` |
| #50 | new at `needs-triage`: an enhancement an agent found in an audit | `ready-for-human`, not closed, unmarked |
| #51 | an agent-found enhancement left at `ready-for-agent`, in all three Left out lists | `ready-for-human`, `ready-for-agent` removed, not closed |

No other issue gains `next-release`, no release label is applied, every comment starts with the triage disclaimer, and one `## Triage batch` summary on #4 names #31, #32, #33, #40, #41, #50 and #51.

### Running the case

1. Build it into a scratch directory outside this repo.
2. Start a **fresh** session at the **premium** tier (load `model-tiers` for the model), working directory `<out-dir>/repo`, and give it only the text between the `---` lines of `<out-dir>/PROMPT.md`, with `<checkout>` replaced by the checkout under test. Keep this README, `sweep_case.py`, `score.py` and `test_cases.py` away from it: the Expected column is the answer.
3. Score it: `python3 evals/triage/backlog-sweep/score.py <out-dir>`. It prints one line per check and exits 1 when any fails. Read `.scratch/report.md` too.
4. Run it on the branch's skill and on main's, and record both in [RESULTS.md](RESULTS.md) with the commit, plugin version and run level; keep each run's `.scratch/proposed-actions.md`, `.scratch/report.md` and score in `backlog-sweep/evidence/<branch|main>/` (`branch/` and `main/` hold the runs of #636; the runs of Ticket #680 are in `680-branch/` and `680-main/`).

### Self-test of the case

`python3 evals/triage/backlog-sweep/test_cases.py` builds the case and scores a reference run written from the expected outcome; the reference must pass, and planted wrong runs (a duplicate closed with no link, an obsolete issue closed with no reason or as not planned, the issue left out twice expired, an expiry without "reopen to bring it back", an agent-found enhancement expired, put at or left at `ready-for-agent`, the planned feature expired, the severe issue or the feature-blocker unmarked, an extra mark, a release label applied, no summary, a comment without the disclaimer) must fail. It proves the builder and scorer agree; it is not a model run of the skill.
