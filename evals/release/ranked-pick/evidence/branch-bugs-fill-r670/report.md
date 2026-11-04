# Release thread report (2026-11-04)

**Where I started:** no open release issue, and no open issue carries a release label. The last release issue, #2 (Release 2), is closed and holds its notes and both end-of-Release records (triage, retro-planning). So nothing needed cutting, and I went straight to planning the next Release for Milestone #1. Main is at `9ea7fb1`.

## Release 3 (planned; release issue to be #35, label `release-3`)

Goal: the greeter gains its quiet and shout flags, and its known usage and output bugs are fixed.

Size: 5. Used: 5. No severe or `next-release` issues are waiting.

Order:
1. #20 Quiet flag: planned feature. Neither flag depends on the other, so the Milestone's order decides (first).
2. #21 Shout flag: planned feature, second in the Milestone's order.
3. #30 Typo in usage text: bug, oldest (2026-09-01).
4. #31 Empty name prints `Hello, !`: bug (2026-09-15).
5. #33 Trailing space after the greeting: bug (2026-10-10).

Left out: none.

## Check against main
- #20, #21, #30, #31, #33: still valid.
- #32 Unknown command exits 0 from a pipe: obsolete, closed as not planned. `src/greet.sh` exits 2 on an unknown command, and has since the first commit (3bb4614). The 0 comes from the pipeline: without `pipefail`, a pipeline returns `cat`'s status. Reopen it if the reporter wanted something else.
- #34 Names with accents come out mangled: cannot tell. The issue gives no way to reproduce it, and on main `hello José` prints the name unchanged. It is at `needs-triage`, so it is not a candidate either way. It needs a reproduction from the reporter.

## Questions and proposals
No questions for you, and no unplanned features to propose.

## Notes
- This was a dry run: every tracker write is in `.scratch/proposed-actions.md` (8 actions), and no issue file, label file, commit or branch was changed.
- There were 7 issues to check. The skill hands more than 5 to premium-tier subagents, but this thread had no way to start subagents, so I checked all 7 myself.
