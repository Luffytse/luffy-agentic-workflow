Title: Release 3

**Goal:** The greeter stops leaking the names it is given and its test runs fast, and it gains the farewell command and the quiet flag.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 5.

## Order

1. #31 greet.sh writes every name to a world-readable log: severe (a security hole): every run appends the name, sometimes an email address, to `/tmp/greet.log` at mode 0666, readable by every user.
2. #35 test.sh takes 10 s: marked `next-release` by Retro planning for Release 2: `test.sh` sleeps 10 s for nothing.
3. #10 Farewell command: planned feature (Spec, with Tickets #11 and #12); a new command moves "Round out the greeter's commands" furthest, and it is first in the Milestone's order; no open blockers.
4. #20 Quiet flag: planned feature; no feature depends on it and it adds a flag rather than a command, so it follows #10, as in the Milestone's order; no open blockers.
5. #30 Typo in usage text: `ready-for-agent` bug, open since 2026-09-01, the oldest bug.

## Left out

None.

## Checked against main

Main at `41bd115`.

- #10 Farewell command: still valid
- #11 bye: the command: still valid
- #12 bye: usage text: still valid
- #20 Quiet flag: still valid
- #30 Typo in usage text: still valid
- #31 greet.sh writes every name to a world-readable log: still valid
- #35 test.sh takes 10 s: still valid

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
