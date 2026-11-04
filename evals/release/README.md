# release eval

Checks of the `release` skill (`plugins/dev-skills/skills/release/`) on its one path: check the current Release shipped, write the changelog entry, run the cut steps and whole-Release check, close the Release, run the end-of-Release pass, then rank and pick the next Release. Each run gets an entry in [RESULTS.md](RESULTS.md). The parked-scope traces are in [`parked-scope/`](parked-scope/README.md).

## Run level

| Check | Run level |
| --- | --- |
| `ranked-pick/test_cases.py` | no model session: builds each case and scores a reference run and planted wrong runs |
| the nine ranked-pick cases (runs kept in `ranked-pick/evidence/`) | decision-level in a subagent: every tracker, pull request and skill-run write is a block in `.scratch/proposed-actions.md`, so nothing real is labelled, opened, merged or closed |

## Ranked-pick cases

[`ranked-pick/make_fixture.py`](ranked-pick/make_fixture.py) builds one case outside this repo: `python3 evals/release/ranked-pick/make_fixture.py <out-dir> <case>`. It makes `<out-dir>/repo` and `<out-dir>/PROMPT.md`. The repo is a tiny shell greeter with a dry-run local tracker (`docs/dev-skills/issue-tracker.md`: issue and pull request files under `.scratch/`, every write a numbered block), a Boundary record that lets agents merge, a triage label doc with `next-release`, and a release doc with the versioning policy **none**, the name `Release <n>` (label `release-<n>`), the case's Release size, no cut steps and `bash test.sh` as the whole-Release check. Milestone 1 (#1) lists the case's features in order. Except in `no-version` and `old-shape-cut`, Release 2 (#2) is already cut and closed, with its notes and both end-of-Release records, so the run goes straight to planning Release 3. The case data and the expected picks are in [`ranked-pick/cases.py`](ranked-pick/cases.py).

| Case | Fixture | Expected pick for Release 3 |
| --- | --- | --- |
| `severe-first` | size 5; features #10 (Spec, Tickets #11, #12) and #20; bug #30 (oldest); #31 a security hole, unmarked, newest; #35 marked `next-release`, not severe | Order #31, #35, #10, #20, #30; labels on those and #11, #12; `next-release` removed from #35; Used 5 |
| `blocker-first` | size 5; #20 blocked by bug #40, outside the Milestone; bug #30 | Order #10, #40, #20, #30 (the blocker just before its feature, not in group 3); Used 4 |
| `bugs-fill` | size 5; features #20, #21; ready bugs #30 to #33, oldest first; #34 at `needs-triage` | Order #20, #21, #30, #31, #32; #33 left out (size); #34 never ranked |
| `unplanned-feature` | size 5; features #10, #20; bug #30; #50 a `ready-for-agent` enhancement the Milestone does not list; #51 an agent-found enhancement at `ready-for-human` | Order #10, #20, #30; #50 proposed to the user, never labelled or left out; #51 not ranked |
| `size-reached` | size 3; features #20 to #23; bug #30 | Order #20, #21, #22; #23 and #30 left out with the reason; Used 3 |
| `severe-past-size` | size 2; three severe bugs (#36 delivery stopped, #31 lost data, #37 a leaked token, oldest first in that order); #35 marked, not severe; features #10, #20 | Order #36, #31, #37 ("Used: 2, plus 1 severe past the size"); #35, #10, #20 left out; #35 keeps its mark |
| `reorder` | goal "usable from scripts"; features listed #24 colour, #25 JSON output, #26 config loader, with #24 and #25 blocked by #26 | Order #26 (others depend on it), #25 (moves the goal furthest), #24, each with a line of reason |
| `no-version` | Release 2 (#2) open: #10 and #20 closed by merged pull requests #7 (`Closes #10`) and #8 (`Fixes #20`); #9 merged with no issue; feature #21 open | the cut: a changelog pull request changing only `CHANGELOG.md`, entry `## Release 2` with `Commits: <Release 1's end>..<main>`, #10 and #20 listed, #9 under "Also merged", no `Versions:` line; merged; notes on #2, #2 closed; `triage` then `retro-planning` run, each with its end-of-Release record; then Release 3 with Order #21 |
| `old-shape-cut` | as `no-version`, but #2 was written before the Order list: a `**Cap:**` line and a `## Scope` list, no `## Order` | as `no-version`: #2 is the current Release and is cut, not planned again |

### Running a case

1. Build it into a scratch directory outside this repo.
2. Start a **fresh** session at the **premium** tier (load `model-tiers` for the model), working directory `<out-dir>/repo`, and give it only the text between the `---` lines of `<out-dir>/PROMPT.md`, with `<checkout>` replaced by the checkout under test. Keep this README, `cases.py`, `score.py` and `test_cases.py` away from it: the Expected column is the answer.
3. Score it: `python3 evals/release/ranked-pick/score.py <out-dir> <case>`. It prints one line per check and exits 1 when any fails. It reads the `Release 3` issue the run opens (its Order, Left out, Proposed to the user and Size), the label writes and, in `no-version` and `old-shape-cut`, the cut's blocks and their order. Read `.scratch/report.md` too.
4. Run each case on the branch's skill and on main's, and record both in [RESULTS.md](RESULTS.md) with the commit, plugin version and run level.

### Self-test of the cases

`python3 evals/release/ranked-pick/test_cases.py` builds each case and scores a reference run written from the case's expected pick; the reference must pass, and planted wrong runs (two Order entries swapped, a non-severe marked issue taken past the size, an unplanned feature ranked, a `Versions:` line in a repo with no version, the mark left on a taken issue, a severe issue left out, `old-shape-cut` planned again with no cut) must fail. It proves the builder and scorer agree; it is not a model run of the skill.
