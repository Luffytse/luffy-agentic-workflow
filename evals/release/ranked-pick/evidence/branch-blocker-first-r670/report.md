# Release thread report (2026-11-04 09:00 UTC)

**Where I started.** No release issue is open, and no open issue carries a release label. The last release issue, #2 (Release 2), is closed and has both end-of-Release records (triage and retro-planning). So this run went straight to step 5 and planned the next Release. Nothing was cut and no changelog pull request was opened.

**Planned: Release 3** (label `release-3`, Milestone #1). Release issue: proposed as new `50-release-3.md`.

Goal: The greeter says goodbye and takes a quiet flag, completing the Milestone's commands.

Size: 5. Used: 4.

## Order

1. #10 Farewell command (a Spec, with Tickets #11 and #12): planned feature. Neither feature depends on the other. This one moves the goal furthest because it adds a whole new command, and it is first in the Milestone's order.
2. #40 Flags after the name are dropped: a bug that blocks #20, so it goes just before #20 and not in the bugs group.
3. #20 Quiet flag: planned feature, second. Its blocker #40 is placed right above it.
4. #30 Typo in usage text: a `ready-for-agent` bug, the oldest open one (2026-09-01).

Labels to apply: `release-3` (a new label) on #10, #11, #12, #40, #20 and #30. No issue carried `next-release`.

## Left out

None. Every candidate fit within the size of 5.

## Check against main (main at `f1e677e`)

All six issues (#10, #11, #12, #20, #30, #40) are still valid:
- `src/greet.sh` has no `bye` command and no `-q` flag.
- Its usage line still says `helo`.
- `greet.sh hello Ada -x` prints `Hello, Ada!` and ignores `-x`. One wording note on #40: main has no flag parser at all. The script just ignores every argument after the name, so the fix is to add flag parsing, not to repair a parser.

No questions for you came out of the check.

## Proposed features

None. Every open enhancement is listed in the Milestone issue or is a Ticket of a listed Spec.

## Deviation

The skill says that with more than 5 issues to check, they go in batches to premium-tier subagents. There were 6. This thread has no way to start subagents, so I read and checked all six myself.

All writes are recorded as dry-run blocks in `.scratch/proposed-actions.md`. Nothing waits on a reply.
