Title: Release 3

**Goal:** The greeter gains its quiet and shout flags, and its known usage and output bugs are fixed.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 5.

## Order

1. #20 Quiet flag: planned feature; neither flag depends on the other and both move the goal equally, so the Milestone issue's order (first) breaks the tie.
2. #21 Shout flag: planned feature; second in the Milestone issue's order, no blockers.
3. #30 Typo in usage text: `ready-for-agent` bug, the oldest (2026-09-01); the usage line still says `greet.sh helo`.
4. #31 Empty name prints `Hello, !`: `ready-for-agent` bug, next oldest (2026-09-15); `${2-world}` keeps an empty name.
5. #33 Trailing space after the greeting: `ready-for-agent` bug, newest (2026-10-10); every greeting still ends `! `.

## Left out

None.

## Checked against main

Main at `9ea7fb1`.

- #20 Quiet flag: still valid
- #21 Shout flag: still valid
- #30 Typo in usage text: still valid
- #31 Empty name prints `Hello, !`: still valid
- #32 Unknown command exits 0 from a pipe: obsolete: `src/greet.sh` line 6 exits 2 on an unknown command, as it has since 3bb4614; `bash src/greet.sh nope | cat; echo "${PIPESTATUS[0]}"` prints 2. The pipeline's 0 is `cat`'s status. Closed as not planned.
- #33 Trailing space after the greeting: still valid
- #34 Names with accents come out mangled: cannot tell: the issue gives no name, command or environment that reproduces it, and on main `bash src/greet.sh hello José` prints the name's UTF-8 bytes unchanged. Unchecked; it is at `needs-triage` and not ranked.

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
