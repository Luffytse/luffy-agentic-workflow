Title: Release 3

**Goal:** The greeter gets its quiet flag and `bye` keeps the whole name.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 3.

## Order

1. #20 Quiet flag: the one planned feature still to build on main (#21 is already done on main and waits for the user's answer); it moves the Milestone's goal.
2. #31 Names with spaces are cut at the first space: `ready-for-agent` bug, oldest of the bugs (2026-09-05); `bye` still cuts the name.
3. #33 test.sh does not test bye: `ready-for-agent` bug (2026-09-15); a broken `bye` passes the check today.

## Left out

None.

## Checked against main

Main at `9c924f4`.

- #20 Quiet flag: still valid
- #21 Shout flag: already fixed: `-s` is in `src/greet.sh`, pull request #8 (dabd7f9). A planned feature, so not closed: asked the user in a comment; unranked until answered.
- #30 Typo in usage text: already fixed: usage line reads `hello` in `src/greet.sh` (pull request #7, bcde54a). Closed as not planned.
- #31 Names with spaces are cut at the first space: changed scope: `hello` fixed by pull request #9 (8cb86e9); `bye` still cuts the name. Issue body updated.
- #32 --version always prints 0.0.0: obsolete: `--version` removed by pull request #10 (9c924f4). Closed as not planned.
- #33 test.sh does not test bye: still valid
- #34 greet sometimes fails: cannot tell: no reproduction, command or locale given. Left as it is, unchecked and not ranked.
- #45 Colour output is left to the next Milestone by the Milestone issue and was not checked.

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
