# Release thread report (2026-11-04 09:00 UTC)

## Where the run started

There is no open release issue and no open issue carries a release label. The last release issue, #2 Release 2, is closed and holds its notes and both end-of-Release records (triage, retro-planning), so the run went straight to step 5 and planned the next Release. Steps 1 to 4 had nothing to do. The four pull requests merged since Release 2 (#7, #8, #9, #10) are not released yet. Release 3's changelog entry will list them when Release 3 is cut.

## Release 3 planned (written to `.scratch/proposed-actions.md`)

Goal: the greeter's quiet and shout flags work as their issues say, and its three oldest open bugs are cleared.
Milestone: #1. Label: `release-3` (new label). Size: 5, used 5. No severe issues and no `next-release` issues.

Order:
1. #20 Quiet flag: planned feature. Neither flag depends on the other, so the Milestone issue's order decides.
2. #21 Shout flag: planned feature, second in the Milestone issue's order.
3. #30 Typo in usage text: oldest `ready-for-agent` bug.
4. #31 Names with spaces are cut at the first space: next oldest bug.
5. #32 --version always prints 0.0.0: next oldest bug.

Left out because the size was reached: #33 test.sh does not test bye, and #34 greet sometimes fails.

Proposed to you: #45 Colour output is an unplanned feature. The Milestone issue does not list it as a feature and names it under Excluded. Plan it with `milestone` if you want it. Note that its `--version` part no longer fits, because #10 removed `--version`.

Nothing here waits on your reply.

## Things to look at

Three issues in the Order look already done or obsolete on main. Pull requests merged after Release 2's triage pass without closing them:
- #21 Shout flag: #8 added `-s`, and `greet.sh -s hello Ada` prints `HELLO, ADA!` on main.
- #30 Typo in usage text: #7 fixed the usage line and said in its body that it does not close #30.
- #32 --version always prints 0.0.0: #10 removed `--version` entirely.

The rules count all three as candidates because they are open and at `ready-for-agent`, so they take three of the five slots. Their threads should only need to confirm the behaviour and close them. If you would rather spend those slots on #33 and #34, close #21, #30 and #32 first (or have a `triage` run do it) and reorder the Release. #31 is only half fixed: #9 fixed `hello`, but `bye "Ada Lovelace"` still prints `Goodbye, Ada!`.

#34 gives no reproduction ("not sure why ... might be the locale"). It reads as `needs-info` more than `ready-for-agent`.

## Subagents

This run started none, and the skill called for none at this step.
