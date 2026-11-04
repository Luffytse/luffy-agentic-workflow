# Release run report: 2026-11-04

Release 2 is cut and closed, and both of its end-of-Release passes are recorded. This run planned **Release 3** (label `release-3`) for Milestone #1, with main at `9c924f4`. The tracker is in dry-run mode, so every write is in `.scratch/proposed-actions.md`.

**Goal:** The greeter gains its quiet flag, and `bye` keeps the whole name and is covered by `test.sh`.

**Size:** 5. Used: 3.

## Order

1. #20 Quiet flag: the only planned feature that can start now. Milestone order breaks the tie.
2. #31 Names with spaces are cut at the first space: the oldest `ready-for-agent` bug left. Its scope is now `bye` only, because #9 fixed `hello`.
3. #33 test.sh does not test bye: a `ready-for-agent` bug. Without it, a broken `bye` would still pass the check.

## Left out

- #22 Help flag: its blocker #30 is not cleared yet (see question 2).

## Questions for you (each is also a comment on its issue; nothing waits on them)

1. **#21 Shout flag**: main already does what it asks. #8 (`dabd7f9`) added `-s`, and `greet.sh -s hello Ada` prints `HELLO, ADA!`. It is a planned feature, so I did not close it. Close it as completed by #8?
2. **#30 Typo in usage text**: already fixed on main by #7 (`bcde54a`). The skill would close it as not planned. But #30 is #22's only blocker, and under the tracker doc a blocker closed as not planned never clears, so #22 could never start. I did not close it. Close it as completed by #7? That clears #22, and the next planning can take it.

## Other results of the check against main

- #32 --version always prints 0.0.0: obsolete. #10 (`9c924f4`) removed `--version`. Closed as not planned.
- #31: changed scope. The body is rewritten to cover `bye` only, with a note naming #9.
- #34 greet sometimes fails: cannot tell. The issue gives no command, no error output and no locale for the build box. It stays unchecked and unranked. It needs a reproduction.
- #20, #22, #33: still valid.
- #45 Colour output was not checked. Milestone #1 leaves it to the next Milestone. Note for that planning: its body says `--version` lists features, but #10 removed `--version`.

## Proposed features

None. No unplanned feature was found among the candidates.

## Notes on this run

- The check had 8 issues in scope, which is more than 5, so the skill hands them to premium-tier subagents. This thread cannot start subagents, so I read all 8 myself and confirmed each verdict by running `src/greet.sh` on main and reading the commits.
- No issue carried `next-release`, no issue was severe, and Release 2 carried nothing over.
- #7 through #10 merged since Release 2 without closing an issue. Release 3's changelog entry will list them under "Also merged".
