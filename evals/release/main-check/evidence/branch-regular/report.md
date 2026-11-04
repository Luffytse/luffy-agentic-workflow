# Release report

Find where you are: the last release issue (#2, Release 2) is closed and holds both end-of-Release records, so this run went to step 5 (plan the next Release). No open release issue, nothing to cut.

Planned Release 3 (label `release-3`, release issue proposed as #46), size 5, used 3: Order #20 Quiet flag, #31 Names with spaces (bye), #33 test.sh bye check. Nothing left out.

Check against main (main at 9c924f4):
- #20 still valid; #33 still valid.
- #21 Shout flag: already done on main (PR #8), but it is a planned feature, so not closed. QUESTION for the user: close #21 as completed (shipped by PR #8, which did not carry a closing keyword)? Commented on #21; it is unranked until answered.
- #30 usage typo: already fixed (PR #7); closed as not planned.
- #32 --version: obsolete (removed by PR #10); closed as not planned.
- #31: changed scope (hello fixed by PR #9; bye still cuts); body updated, ranked.
- #34 greet sometimes fails: cannot tell; left as is, unchecked, not ranked.
- #45 Colour output: left to the next Milestone; not checked.

No unplanned features to propose. Subagents not needed (8 issues, read myself). All writes are in .scratch/proposed-actions.md.
