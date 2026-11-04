Title: Release 3

**Goal:** The greeter gains its quiet and shout flags, and stops misprinting its usage line, empty names and the exit code of an unknown command.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 5.

## Order

1. #20 Quiet flag: planned feature; neither feature depends on the other and both move the Milestone's goal equally, so the Milestone issue's order puts it first.
2. #21 Shout flag: planned feature; second in the Milestone issue's order, with no dependency to reorder it.
3. #30 Typo in usage text: `ready-for-agent` bug, the oldest (2026-09-01); the usage line names a command that does not exist.
4. #31 Empty name prints `Hello, !`: `ready-for-agent` bug, second oldest (2026-09-15).
5. #32 Unknown command exits 0 from a pipe: `ready-for-agent` bug, third oldest (2026-10-01); scripts cannot detect a bad command.

## Left out

- #33 Trailing space after the greeting: the size was reached (youngest `ready-for-agent` bug, 2026-10-10).

## Checked against main

Main at `cdcf698`.

- #20 Quiet flag: still valid
- #21 Shout flag: still valid
- #30 Typo in usage text: still valid
- #31 Empty name prints `Hello, !`: still valid
- #32 Unknown command exits 0 from a pipe: still valid
- #33 Trailing space after the greeting: still valid
- #34 Names with accents come out mangled: cannot tell: the issue gives no example name, locale or terminal; on main `greet.sh hello José` passes the UTF-8 bytes through unchanged, so the report's case is needed to tell whether it still happens. Unchecked, not ranked (it is also at `needs-triage`, so not a candidate).

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
