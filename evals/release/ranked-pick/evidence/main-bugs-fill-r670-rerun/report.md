# Release thread report (2026-11-04)

**Where the run started.** No open release issue and no orphan release label. The last release issue, #2 (Release 2), is closed and holds both end-of-Release records (triage, retro-planning), so steps 1 to 4 had nothing to do and the run planned the next Release (step 5). Milestone #1 is open.

**Release 3 planned** (release issue `35-release-3.md`, label `release-3`, created). Goal: the greeter gains its quiet and shout flags, and its three oldest command bugs are fixed.

Size: 5. Used: 5. No severe issues and no `next-release` marks were waiting.

Order:
1. #20 Quiet flag: planned feature; no dependencies between the two flags and equal weight toward the goal, so the Milestone's order keeps it first.
2. #21 Shout flag: planned feature, second in the Milestone's order.
3. #30 Typo in usage text: `ready-for-agent` bug, oldest (2026-09-01).
4. #31 Empty name prints `Hello, !`: `ready-for-agent` bug (2026-09-15).
5. #32 Unknown command exits 0 from a pipe: `ready-for-agent` bug (2026-10-01); not severe.

Left out:
- #33 Trailing space after the greeting: Release size reached.

Not a candidate: #34 Names with accents come out mangled is at `needs-triage`.

Proposed features: none (no unplanned feature found).

Nothing waits on a reply.
