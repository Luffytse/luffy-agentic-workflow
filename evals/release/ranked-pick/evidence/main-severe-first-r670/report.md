# Release thread report (2026-11-04)

**Where it started.** No open release issue, and no open issue carries a release label. The last release issue, #2 (Release 2), is closed with its notes and holds both end-of-Release records (triage and retro-planning), so this run skipped steps 1 to 4 and planned the next Release. Nothing was cut.

**Planned: Release 3** (label `release-3`, Milestone #1). The proposed release issue is `36-release-3.md` (dry run: see `.scratch/proposed-actions.md`).

Goal: the greeter stops leaking names, its test runs fast, and it gains the farewell command and the quiet flag.

Size: 5. Used: 5. No severe issue past the size.

## Order

1. #31 greet.sh writes every name to a world-readable log: severe, a security hole (names and email addresses in `/tmp/greet.log`, mode 0666).
2. #35 test.sh takes 10 s: marked `next-release` by Release 2's Retro planning.
3. #10 Farewell command (Spec, with Tickets #11 and #12): first planned feature; no dependency between the features, so the Milestone's order stands, and a new command moves the goal furthest.
4. #20 Quiet flag: second planned feature.
5. #30 Typo in usage text: the oldest `ready-for-agent` bug (2026-09-01).

## Left out

None: every candidate fit within the size.

## Proposed to you

None: no unplanned feature is open.

## Labels

`release-3` created and applied to #31, #35, #10, #11, #12, #20 and #30; `next-release` removed from #35. Nothing waits on a reply.
