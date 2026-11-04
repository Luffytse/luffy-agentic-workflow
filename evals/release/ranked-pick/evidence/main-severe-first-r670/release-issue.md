Title: Release 3

**Goal:** The greeter stops leaking names, its test runs fast, and it gains the farewell command and the quiet flag.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 5.

## Order

1. #31 greet.sh writes every name to a world-readable log: severe, a security hole: every name given, email addresses included, lands in `/tmp/greet.log` at mode 0666 for any user to read.
2. #35 test.sh takes 10 s: marked `next-release` by Release 2's Retro planning, because `test.sh` sleeps 10 s for nothing on every check.
3. #10 Farewell command: first planned feature; nothing depends on either feature and neither blocks the other, so the Milestone's order stands, and a whole new command (with its Tickets #11 and #12) moves "round out the greeter's commands" furthest.
4. #20 Quiet flag: second planned feature; a flag on the existing commands, after the new command in the Milestone's order.
5. #30 Typo in usage text: `ready-for-agent` bug, open since 2026-09-01, the oldest bug.

## Left out

None.

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
