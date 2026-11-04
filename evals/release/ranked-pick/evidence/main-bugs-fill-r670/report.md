# Release thread report (2026-11-04 09:00 UTC)

## Where it started

No open release issue and no open issue carries a release label. The last release issue, #2 (Release 2), is closed and already holds both end-of-Release records (triage and retro-planning), so this run went straight to step 5: plan the next Release. Nothing was cut and no changelog pull request was opened.

## Release 3 planned (dry run: proposed in `.scratch/proposed-actions.md`)

- Release issue: new #35, "Release 3", label `release-3` (label created), Milestone #1.
- Goal: the greeter gains its quiet and shout flags, rounding out Milestone 1's commands, and its three oldest bugs are fixed.
- Size: 5. Used: 5. No severe issue, so none past the size.

Order:

1. #20 Quiet flag: planned feature, first in the Milestone's order (no dependency between the two flags, they move the goal equally, so the Milestone order breaks the tie).
2. #21 Shout flag: planned feature, second in the Milestone's order.
3. #30 Typo in usage text: oldest ready-for-agent bug (2026-09-01).
4. #31 Empty name prints `Hello, !`: ready-for-agent bug (2026-09-15).
5. #32 Unknown command exits 0 from a pipe: ready-for-agent bug (2026-10-01).

Left out:

- #33 Trailing space after the greeting: size reached. It is the next bug in line.

Proposed to you: none (no unplanned feature is open).

Not a candidate: #34 "Names with accents come out mangled" is still at `needs-triage` (filed 2026-08-01, the oldest open bug). It needs triage before it can be planned.

No taken issue carried `next-release`, so no mark was removed. Nothing waits on your reply.
