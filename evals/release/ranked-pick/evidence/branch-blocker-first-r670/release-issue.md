Title: Release 3

**Goal:** The greeter says goodbye and takes a quiet flag, completing the Milestone's commands.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 4.

## Order

1. #10 Farewell command: planned feature; no other feature depends on it or on #20, it moves the Milestone's goal (round out the commands) furthest by adding a whole new command, and it is first in the Milestone's order. A Spec, standing for its Tickets #11 and #12.
2. #40 Flags after the name are dropped: a bug that blocks planned feature #20 (Quiet flag), so it lands just before it in group 2, not in group 3.
3. #20 Quiet flag: planned feature; it adds a flag rather than a command, so it moves the goal less than #10, and it is second in the Milestone's order; its open blocker #40 is placed just above it.
4. #30 Typo in usage text: a `ready-for-agent` bug, the oldest open one (2026-09-01); the usage line on main still says `helo`.

## Left out

None.

## Checked against main

Main at `f1e677e`.

- #10 Farewell command: still valid
- #11 bye: the command: still valid
- #12 bye: usage text: still valid
- #20 Quiet flag: still valid
- #30 Typo in usage text: still valid
- #40 Flags after the name are dropped: still valid

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
