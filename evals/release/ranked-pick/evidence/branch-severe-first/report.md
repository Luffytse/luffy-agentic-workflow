# Release thread report (2026-11-04)

**Where it started:** no open release issue and no issue carries an unnamed release label; the last Release, Release 2 (#2), is closed with its notes and both end-of-Release records (triage, retro-planning). So this run went straight to planning the next Release.

**Planned: Release 3** (release issue to be opened as #36, label `release-3`, Milestone #1). Size 5, used 5; no severe issue past the size.

Goal: the greeter stops writing names to a world-readable log, its tests run fast again, and it gains the bye command and the quiet flag.

## Order

1. #31 greet.sh writes every name to a world-readable log: severe (security hole leaking names and email addresses), ranked first.
2. #35 test.sh takes 10 s: marked `next-release` by Release 2's retro planning.
3. #10 Farewell command (Spec, Tickets #11, #12): planned feature, first in the Milestone's order; nothing depends on another feature, so that order stands.
4. #20 Quiet flag: planned feature, second in the Milestone's order.
5. #30 Typo in usage text: `ready-for-agent` bug, the oldest open (2026-09-01).

## Left out

None.

## Proposed to you

None: no unplanned features are open.

## Tracker writes (dry run, see `.scratch/proposed-actions.md`)

Create label `release-3`; open the release issue; apply `release-3` to #31, #35, #10, #11, #12, #20, #30; remove `next-release` from #35. Nothing waits on a reply.
