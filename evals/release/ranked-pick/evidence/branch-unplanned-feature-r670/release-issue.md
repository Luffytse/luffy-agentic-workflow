Title: Release 3

**Goal:** The greeter says goodbye and can run quietly, and its usage text names its commands correctly.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 3.

## Order

1. #10 Farewell command: planned feature (Spec, with Tickets #11 and #12); neither planned feature depends on the other, and a whole new command moves the Milestone's goal ("round out the greeter's commands") further than a flag, which also matches the Milestone issue's order.
2. #20 Quiet flag: planned feature; second because it adds an option to an existing command rather than a new command, and the Milestone issue's order puts it second.
3. #30 Typo in usage text: group 3, `ready-for-agent` bug, open since 2026-09-01 (the oldest open bug); the usage line on main still says `greet.sh helo <name>`.

## Left out

None.

## Checked against main

Main at `f1e677e`.

- #10 Farewell command: still valid
- #11 bye: the command: still valid
- #12 bye: usage text: still valid
- #20 Quiet flag: still valid
- #30 Typo in usage text: still valid
- #50 Colour output: still valid
- #51 Run shellcheck in test.sh: still valid

## Proposed to the user

- #50 Colour output: an unplanned feature; the Milestone issue does not list it.
- #51 Run shellcheck in test.sh: an unplanned feature (at `ready-for-human`); the Milestone issue does not list it.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
