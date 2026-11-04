# Release thread report (2026-11-04)

**Where I started.** Release 2 (#2) is closed, holds its notes and both end-of-Release records (triage, retro-planning), and no open release issue or unnamed release label exists, so this run went straight to step 5: plan the next Release. Milestone 1 (#1) is open.

**Planned: Release 3** (label `release-3`, release issue proposed as #31; dry run, see `.scratch/proposed-actions.md`).

Goal: The greeter gains its quiet, shout and read-names-from-a-file flags.

Size: 3. Used: 3.

## Order

1. #20 Quiet flag: planned feature; no feature depends on another and each moves the goal equally, so the Milestone issue's order (1st) breaks the tie.
2. #21 Shout flag: planned feature; Milestone order 2nd breaks the tie.
3. #22 Read names from a file: planned feature; Milestone order 3rd breaks the tie.

## Left out

- #23 Repeat flag: planned feature, 4th; the size was reached.
- #30 Typo in usage text: `ready-for-agent` bug (oldest open issue, filed 2026-09-01), group 3; the size was reached.

## Checked against main (`1901725`)

All five open candidates (#20, #21, #22, #23, #30) are still valid: `src/greet.sh` has only the `hello` command, with no `-q`, `-s`, `-f` or `-n` flag, and its usage line still prints `greet.sh helo <name>`. No closes, edits or questions.

## Proposed to the user

None: no unplanned features are open.

No severe or `next-release` issues are waiting. Nothing waits on a reply.
