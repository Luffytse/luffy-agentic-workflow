# Release thread report (2026-11-04 09:00 UTC)

**Where it started:** no open release issue and no issue carrying an unnamed release label. The last Release, Release 2 (#2), is closed with its notes and both end-of-Release records (triage, retro-planning), so this run went straight to planning the next Release (step 5). Nothing was cut in this run.

**Planned: Release 3** (label `release-3`, release issue to be opened as #35), in Milestone #1 "Round out the greeter's commands".

Goal: The greeter gains its quiet and shout flags, and its three oldest ready bugs are fixed.

Size: 5. Used: 5. No severe issues and no `next-release` issues were waiting.

## Order

1. #20 Quiet flag: planned feature, first in the Milestone's order; no dependencies between the two flags, so the Milestone's order breaks the tie.
2. #21 Shout flag: planned feature, second in the Milestone's order; no blockers.
3. #30 Typo in usage text: `ready-for-agent` bug, oldest (2026-09-01).
4. #31 Empty name prints a double space: `ready-for-agent` bug (2026-09-15).
5. #32 Unknown command exits 0 from a pipe: `ready-for-agent` bug (2026-10-01).

## Left out

- #33 Trailing space after the greeting: Release size of 5 reached. It is the first candidate for the next planning.

## Not candidates

- #34 Names with accents come out mangled: at `needs-triage`, so not ranked; it needs triage first.

## Proposed to the user

None: no unplanned features are open.

Tracker writes are recorded in `.scratch/proposed-actions.md` (dry run): open the release issue, create the `release-3` label, and apply it to #20, #21, #30, #31 and #32. Nothing waits on a reply.
