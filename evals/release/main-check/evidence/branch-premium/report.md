# Release thread report, 2026-11-04 09:00 UTC

## Where the run started

There was no open release issue, and no open issue carried a release label. Release 2 (#2) is closed and already has both end-of-Release records (triage and retro-planning), so the run went straight to step 5 and planned the next Release. Nothing was cut in this run. Main is at `9c924f4`.

## Release 3 planned (release issue #46, label `release-3`, Milestone #1)

**Goal:** The greeter gains its quiet flag, `bye` keeps the whole name, and `test.sh` checks `bye`.

**Size:** 5. Used: 3. No severe issues and no `next-release` issues.

Order:
1. #20 Quiet flag: the only planned feature that can be ranked. It has no blockers and nothing depends on it.
2. #31 Names with spaces are cut at the first space: the oldest `ready-for-agent` bug left. Its scope is now `bye` only.
3. #33 test.sh does not test bye: a `ready-for-agent` bug. Today a broken `bye` still passes `test.sh`.

Left out: none.

Proposed unplanned features: none. #45 Colour output was not checked or ranked, because Milestone #1 leaves it to the next Milestone. Heads-up: its body says `greet.sh --version` lists features, but main removed `--version` in #10, so it will need rescoping when the next Milestone plans it.

## Check against main (verdicts)

- #20: still valid.
- #21 Shout flag: already fixed by #8 (dabd7f9). **Question for you** (also posted on #21): it is feature 2 of Milestone #1, so I did not close it. Should it be closed as done, or does it still lack something? Until you answer it waits, unranked.
- #30 Typo in usage text: already fixed by #7 (bcde54a). Closed as not planned.
- #31: scope changed. `hello` was fixed in #9 (8cb86e9) and `bye` still cuts the name. I updated the body.
- #32 --version always prints 0.0.0: obsolete, because #10 (9c924f4) removed `--version`. Closed as not planned.
- #33: still valid.
- #34 greet sometimes fails: cannot tell. The issue gives no failing command, no output, no locale or environment and no repro steps. It is left unchecked and unranked; it needs details from its reporter.

## Notes on the run

- With 7 issues in scope, the skill says to hand the check to premium-tier subagents. This thread cannot start subagents, so I did every check myself, at the premium tier.
- The tracker is in dry run. Every write is in `.scratch/proposed-actions.md` (blocks 1 to 10). Nothing waits on a reply.
