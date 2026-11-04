# Release thread report (2026-11-04)

**Where I started.** No open release issue; the last one, #2 Release 2, is closed with its notes and both end-of-Release records (triage, retro-planning). So this run went straight to step 5 and planned the next Release. Nothing was cut.

**Planned: Release 3** (label `release-3`, release issue proposed as new #35), Milestone #1. Size 5, used 5.

Order:
1. #20 Quiet flag: planned feature; no dependency between the two features, Milestone order breaks the tie.
2. #21 Shout flag: planned feature, second in the Milestone order.
3. #30 Typo in usage text: oldest `ready-for-agent` bug (2026-09-01).
4. #31 Empty name prints `Hello, !`: next oldest bug (2026-09-15).
5. #32 Unknown command exits 0 from a pipe: next oldest bug (2026-10-01).

Left out: #33 Trailing space after the greeting: the size was reached.

No severe or `next-release` issues; none to remove `next-release` from.

**Check against main** (main at `cdcf698`): #20, #21, #30, #31, #32, #33 still valid (reproduced on main). #34 Names with accents come out mangled: cannot tell; the issue gives no example name, locale or terminal, and `greet.sh hello José` prints correctly on main. It is left unchecked and is at `needs-triage`, so it is not a candidate anyway; it needs the reporter's case. No questions were raised to you.

**Proposed features:** none (no unplanned features open).

**Note on method:** 7 issues were in the check's scope; the skill hands more than 5 to premium-tier read-only subagents, but this thread has no way to start subagents, so I checked all 7 myself.

All tracker writes are recorded in `.scratch/proposed-actions.md` (dry run). Nothing waits on a reply.
