# Release thread report (2026-11-04)

Where I started: no release issue is open and no open issue carries a release label. The last Release, Release 2 (#2), is closed with its notes and both end-of-Release records (triage, retro-planning), so this run went straight to planning the next Release. Nothing was cut.

## Release 3 planned (release issue #4, label `release-3`, Milestone #1)

Goal: the greeter says goodbye, takes a quiet flag, and its usage text reads right.

Size: 5. Used: 3.

Order:
1. #10 Farewell command (Spec, with Tickets #11 and #12): first in the Milestone's order; a whole new command moves the goal furthest; nothing blocks it.
2. #20 Quiet flag: second in the Milestone's order; nothing blocks it.
3. #30 Typo in usage text: `ready-for-agent` bug, the oldest waiting (2026-09-01).

Left out: none. No severe or `next-release` issues were waiting.

## Proposed to you (not ranked, not labelled)

These are features the Milestone issue (#1) does not list. Plan them with `milestone` if you want them; nothing waits on your reply.
- #50 Colour output (`ready-for-agent`, enhancement).
- #51 Run shellcheck in test.sh (`ready-for-human`, enhancement).

All tracker writes (new release issue, the `release-3` label, labelling #10, #11, #12, #20, #30) are in `.scratch/proposed-actions.md`.
