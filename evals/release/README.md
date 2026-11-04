# release eval

Checks of the `release` skill (`plugins/dev-skills/skills/release/`) on its one path: check the current Release shipped, write the changelog entry, run the cut steps and whole-Release check, close the Release, run the end-of-Release pass, then check every open issue against main and rank and pick the next Release. Each run gets an entry in [RESULTS.md](RESULTS.md). The parked-scope traces are in [`parked-scope/`](parked-scope/README.md); the check of every open issue against main before ranking is the [main-check case](#main-check-case).

## Run level

| Check | Run level |
| --- | --- |
| `ranked-pick/test_cases.py` | no model session: builds each case and scores a reference run and planted wrong runs |
| the twelve ranked-pick cases (runs kept in `ranked-pick/evidence/`) | decision-level in a subagent: every tracker, pull request and skill-run write is a block in `.scratch/proposed-actions.md`, so nothing real is labelled, opened, merged or closed |
| `main-check/test_cases.py` | no model session: builds the case, checks its rendered input says what each issue means, and scores a reference run and planted wrong runs |
| the main-check case (runs kept in `main-check/evidence/`) | decision-level in a subagent, as the ranked-pick cases |

## Ranked-pick cases

[`ranked-pick/make_fixture.py`](ranked-pick/make_fixture.py) builds one case outside this repo: `python3 evals/release/ranked-pick/make_fixture.py <out-dir> <case>`. It makes `<out-dir>/repo` and `<out-dir>/PROMPT.md`. The repo is a tiny shell greeter with a dry-run local tracker (`docs/dev-skills/issue-tracker.md`: issue and pull request files under `.scratch/`, every write a numbered block), a Boundary record that lets agents merge, a triage label doc with `next-release`, and main's `src/greet.sh` and `test.sh` carrying each defect an open issue of the case reports (so every open issue is true on main, as `release` checks it against main before ranking), a release doc with the versioning policy **none**, the name `Release <n>` (label `release-<n>`), the case's Release size, no cut steps and `bash test.sh` as the whole-Release check. Milestone 1 (#1) lists the case's features in order. Except in `no-version` and `old-shape-cut`, Release 2 (#2) is already cut and closed, with its notes and both end-of-Release records, so the run goes straight to planning Release 3. The case data and the expected picks are in [`ranked-pick/cases.py`](ranked-pick/cases.py).

| Case | Fixture | Expected pick for Release 3 |
| --- | --- | --- |
| `severe-first` | size 5; features #10 (Spec, Tickets #11, #12) and #20; bug #30 (oldest); #31 a security hole, unmarked, newest; #35 marked `next-release`, not severe | Order #31, #35, #10, #20, #30; labels on those and #11, #12; `next-release` removed from #35; Used 5 |
| `blocker-first` | size 5; #20 blocked by bug #40, outside the Milestone; bug #30 | Order #10, #40, #20, #30 (the blocker just before its feature, not in group 3); Used 4 |
| `bugs-fill` | size 5; features #20, #21; ready bugs #30 to #33, oldest first; #34 at `needs-triage` | Order #20, #21, #30, #31, #32; #33 left out (size); #34 never ranked |
| `unplanned-feature` | size 5; features #10, #20; bug #30; #50 a `ready-for-agent` enhancement the Milestone does not list; #51 an agent-found enhancement at `ready-for-human` | Order #10, #20, #30; #50 proposed to the user, never labelled or left out; #51 not ranked |
| `size-reached` | size 3; features #20 to #23; bug #30 | Order #20, #21, #22; #23 and #30 left out with the reason; Used 3 |
| `severe-past-size` | size 2; three severe bugs (#36 delivery stopped, #31 lost data, #37 a leaked token, oldest first in that order); #35 marked, not severe; features #10, #20 | Order #36, #31, #37 ("Used: 2, plus 1 severe past the size"); #35, #10, #20 left out; #35 keeps its mark |
| `reorder` | goal "usable from scripts"; features listed #24 colour, #25 JSON output, #26 config loader, with #24 and #25 blocked by #26 | Order #26 (others depend on it), #25 (moves the goal furthest), #24, each with a line of reason |
| `empty` | size 5; Milestone lists only #20 Quiet flag, blocked by #40, a bug at `ready-for-human` (no agent can take it); #50 a `ready-for-agent` enhancement the Milestone does not list; #34 a bug at `needs-triage`; no severe, marked or `ready-for-agent` bug | nothing qualifies, so nothing is taken: no `Release 3` issue opened, no label created or applied, no mark removed; `.scratch/report.md` says nothing qualified and why (#20 waits on #40, which is at `ready-for-human`), names #20 as left out, and proposes #50 to the user |
| `carried-over` | size 5; Release 2 (closed, cut earlier) has #31 and #34 in its Order (Used 3) and under `## Carried over` (#34 closed since); its Notes carry "- #32 ...: not finished, carried to the next Release.", outside the section; Milestone lists #20; #31 and #32 carry only `bug` (no state label) | Order exactly #20 and #31 (either order; the skill gives a carried-over issue no group); #31 labelled; #32 (a carried-over-shaped line in Notes only) and #34 (closed) never ranked |
| `carry-over-cut` | Release 2 (#2) open, cut in step 1: #10 and #20 shipped by merged pull requests, #31 open with `release-2` (it blocks the cut), #21 open; the prompt says the user chose to carry #31 over, every other issue shipped, and to do step 1 only | #2 edited (body, whole) to hold `## Carried over` with exactly one line `- #31 <title>: <why>`, the rest of the body kept; that edit comes before the block removing `release-2` from #31; no other issue loses the label |
| `no-version` | Release 2 (#2) open: #10 and #20 closed by merged pull requests #7 (`Closes #10`) and #8 (`Fixes #20`); #9 merged with no issue; feature #21 open | the cut: a changelog pull request changing only `CHANGELOG.md`, entry `## Release 2` with `Commits: <Release 1's end>..<main>`, #10 and #20 listed, #9 under "Also merged", no `Versions:` line; merged; notes on #2, #2 closed; `triage` then `retro-planning` run, each with its end-of-Release record; then Release 3 with Order #21 |
| `old-shape-cut` | as `no-version`, but #2 was written before the Order list: a `**Cap:**` line and a `## Scope` list, no `## Order` | as `no-version`: #2 is the current Release and is cut, not planned again |

### Running a case

1. Build it into a scratch directory outside this repo.
2. Start a **fresh** session at the **premium** tier (load `model-tiers` for the model), working directory `<out-dir>/repo`, and give it only the text between the `---` lines of `<out-dir>/PROMPT.md`, with `<checkout>` replaced by the checkout under test. Keep this README, `cases.py`, `score.py` and `test_cases.py` away from it: the Expected column is the answer.
3. Score it: `python3 evals/release/ranked-pick/score.py <out-dir> <case>`. It prints one line per check and exits 1 when any fails. It reads the `Release 3` issue the run opens (its Order, Left out, Proposed to the user and Size; in `empty`, that none is opened), the label writes and, in `no-version` and `old-shape-cut`, the cut's blocks and their order. Read `.scratch/report.md` too.
4. Run each case on the branch's skill and on main's, and record both in [RESULTS.md](RESULTS.md) with the commit, plugin version and run level.

### Self-test of the cases

`python3 evals/release/ranked-pick/test_cases.py` builds each case, checks every open issue's claim on the rendered main (a feature is not on main yet, a bug's command shows the bug; `test.sh` passes except in `severe-past-size`, whose #36 says it is red), and scores a reference run (also with `Issue:` lines given as paths) written from the case's expected pick; the reference must pass, and planted wrong runs (two Order entries swapped, a non-severe marked issue taken past the size, an unplanned feature ranked, a `Versions:` line in a repo with no version, the mark left on a taken issue, a severe issue left out, `old-shape-cut` planned again with no cut) must fail. For `empty` the reference run opens no release issue and writes no label, with a report that says nothing qualified, why and the proposed #50; planted wrong runs (an empty `Release 3` issue opened, a label applied, a report that does not say nothing qualified) must fail. It proves the builder and scorer agree; it is not a model run of the skill.

## Main-check case

The check against main of `release` step 5 ("Check against main"): before ranking, every open issue with no release label, not parked and not left to a later Milestone is read against main, given one verdict, and acted on; the release issue records the verdicts. [`main-check/make_fixture.py`](main-check/make_fixture.py) builds the case outside this repo: `python3 evals/release/main-check/make_fixture.py <out-dir>`. It makes `<out-dir>/repo` and `<out-dir>/PROMPT.md`: the ranked-pick greeter, tracker and docs (Release size 5), with Release 2 (#2) cut and closed with both end-of-Release records, so the run goes straight to planning Release 3. Main's `src/greet.sh` has `hello` and `bye`; after Release 2's end four pull requests merged that close no issue: #7 fixes the usage line's `helo`, #8 adds `-s` (shout), #9 makes `hello` keep a name with spaces (`bye` still cuts it), #10 drops `--version`. Milestone 1 (#1) lists #20 Quiet flag, #21 Shout flag and #22 Help flag (blocked by #30), and its Excluded list leaves #45 to the next Milestone. The case data and the expected outcome are in [`main-check/main_case.py`](main-check/main_case.py).

| Issue | Fixture | Expected |
| --- | --- | --- |
| #20 | planned feature `-q`, not on main | still valid; ranked |
| #21 | planned feature `-s`, which main already does (#8) | already fixed (or obsolete), with evidence; not closed: it goes to the user (named in `.scratch/report.md`) and is not ranked |
| #22 | planned feature `-h`, not on main, blocked by #30 | still valid; ranked (its blocker closes as completed, which clears it), not left out |
| #30 | bug: the usage line says `helo`; fixed on main by #7 | already fixed (or obsolete); closed as completed, the reason naming #7 or `src/greet.sh` |
| #31 | bug: `hello` and `bye` cut names at the first space; #9 fixed `hello` only | changed scope; its body edited whole to the `bye` half with a note naming main's change; ranked |
| #32 | bug: `--version` prints 0.0.0; #10 removed the option | obsolete (or already fixed); closed as completed with the reason |
| #33 | bug: `test.sh` does not test `bye`; still true | still valid; ranked |
| #34 | `ready-for-agent` bug with no command, output or steps | cannot tell, saying what is missing; not ranked |
| #45 | enhancement the Milestone leaves to the next Milestone; its body names `--version`, which a check would find changed | not checked: no row, no write |

The release issue for Release 3 has a `## Checked against main` section right after `## Left out` with a row for each of #20 to #34, Order #20, #22, #31, #33 (#20 and #22 either way round; Used 4), and the closes and the edit come before it is opened.

### Running the case

As the ranked-pick cases: build it, give a **fresh** session at the **premium** tier, working directory `<out-dir>/repo`, only the text between the `---` lines of `<out-dir>/PROMPT.md` with `<checkout>` replaced by the checkout under test, keep this README and the `main-check/` files away from it, and score it with `python3 evals/release/main-check/score.py <out-dir>` (one line per check, exit 1 when any fails). Read `.scratch/report.md` too. Run it on the branch's skill and on main's, and also at the **regular** tier, to learn whether regular suffices for the check; record each run in [RESULTS.md](RESULTS.md) and keep its `.scratch/proposed-actions.md`, `.scratch/report.md` and score in `main-check/evidence/<branch|main>-<tier>/` (the folders without a prefix hold the runs before Ticket #680; its runs are in `680-branch-premium/`, `680-main-premium/` and `680-branch-regular/`).

### Self-test of the case

`python3 evals/release/main-check/test_cases.py` builds the case and checks its rendered input: main's script and history make each verdict decidable (the usage line, `hello` and `bye` with a spaced name, `-s`, `--version` gone, `test.sh` without `bye`), the merged pull requests close no issue, the Milestone issue lists #20, #21 and #22, #22 is blocked by the open #30 and `-h` is not on main, the dry-run tracker reads a blocker closed as not planned as uncleared, and the Milestone issue leaves #45 to the next Milestone, and #34 names no command. It then scores a reference run written from the expected outcome, which must pass, and planted wrong runs (the planned feature closed, also through an `Issue:` path, not asked about in the report or with no `Checked against main:` comment on it, the later-Milestone issue edited or given a row, the section missing, a wrong verdict, the unreadable issue ranked, a close or row with no evidence, an already-fixed issue closed as not planned, the feature it blocks left out, the check's writes after the release issue), which must fail; a Left out line saying the planned feature waits or the unreadable issue is unchecked, `Issue:` lines given as paths, and #22 ranked before #20, still pass. Runs before Ticket #680 (the `main-check/evidence/` folders without the `680-` prefix) were made without #22 and scored #30 and #32 as closed not planned. It proves the builder and scorer agree; it is not a model run of the skill.
