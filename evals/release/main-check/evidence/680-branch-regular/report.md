# Release report, 2026-11-04

Found: Release 2 is closed with its notes, triage record and retro-planning record, no open release issue, no stray release label. Went to step 5 (plan the next Release). Milestone #1 is open.

## Release 3 planned (release issue 46-release-3.md, label release-3, size used 4 of 5)

Order: 1. #20 Quiet flag; 2. #22 Help flag (blocker #30 cleared); 3. #31 names with spaces (bye only); 4. #33 test.sh does not test bye.

## Check against main
- #30 closed as completed (usage line already says hello, PR #7). #22 is unblocked.
- #32 closed as completed, obsolete (--version removed by PR #10; repo keeps no version).
- #31 body updated: hello fixed by PR #9, only bye still cuts the name.
- #20, #22, #33 still valid.
- #34 cannot tell (no steps, output or locale given): unchecked, not ranked.
- #45 belongs to a later Milestone (Milestone #1 excludes it): not checked, not ranked. Note for the next planning: its text mentions `--version` listing features, and `--version` is gone from main.

## Questions for the user (nothing waits on a reply)
- #21 Shout flag: main already has `-s` (PR #8). It is a planned feature of Milestone #1, so I did not close it. Close it as completed, or keep it open for more work? It is left out of Release 3 until you answer; a Milestone table row exists for it.

## Notes
- No unplanned features to propose. No severe issues, no `next-release` marks, no parked issues.
- No subagents were started: I read all 8 checked issues myself, since main is one short script. Verdicts and evidence were opened by me.
- Steps 1 to 4 did not run (nothing to cut or close). All writes are in .scratch/proposed-actions.md (10 blocks).
