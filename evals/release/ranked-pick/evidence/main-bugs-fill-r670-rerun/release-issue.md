Title: Release 3

**Goal:** The greeter gains its quiet and shout flags, and its three oldest command bugs are fixed.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 5.

## Order

1. #20 Quiet flag: planned feature; nothing depends on either flag and both move the Milestone's goal equally, so the Milestone issue's order (first) keeps it first.
2. #21 Shout flag: planned feature; second in the Milestone issue's order, with no dependency or goal difference to change it.
3. #30 Typo in usage text: `ready-for-agent` bug, the oldest (2026-09-01).
4. #31 Empty name prints `Hello, !`: `ready-for-agent` bug, second oldest (2026-09-15).
5. #32 Unknown command exits 0 from a pipe: `ready-for-agent` bug, third oldest (2026-10-01); a wrong exit code, not severe.

## Left out

- #33 Trailing space after the greeting: `ready-for-agent` bug (2026-10-10); the Release size of 5 was reached.

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
