Title: Release 3

**Goal:** The greeter gains its quiet flag, `bye` keeps the whole name, and `test.sh` checks `bye`.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 3.

## Order

1. #20 Quiet flag: the only planned feature that can be ranked (feature 2, #21, waits on the user, since main already does it); nothing depends on it and it has no blockers, so it leads by the Milestone's order.
2. #31 Names with spaces are cut at the first space: a `ready-for-agent` bug, the oldest left (2026-09-05); its scope narrowed to `bye`, since `hello` was fixed in #9.
3. #33 test.sh does not test bye: a `ready-for-agent` bug (2026-09-15); a broken `bye` passes `test.sh` today, which matters while #31 changes `bye`.

## Left out

None.

## Checked against main

Main at `9c924f4`.

- #20 Quiet flag: still valid
- #21 Shout flag: already fixed: `src/greet.sh` handles a leading `-s`, added by pull request #8 (dabd7f9); `greet.sh -s hello Ada` prints `HELLO, ADA!`. A planned feature, so not closed: asked the user on the issue; it waits, unranked.
- #30 Typo in usage text: already fixed: the usage line in `src/greet.sh` says `hello`, fixed by pull request #7 (bcde54a), which did not close the issue. Closed as not planned.
- #31 Names with spaces are cut at the first space: changed scope: `hello` keeps the whole name since pull request #9 (8cb86e9); `bye` still cuts it (`cut -d' ' -f1` in `src/greet.sh`). Body updated to `bye` only.
- #32 --version always prints 0.0.0: obsolete: pull request #10 (9c924f4) removed `--version` from `src/greet.sh`; the repo keeps no version (`docs/dev-skills/release.md`). Closed as not planned.
- #33 test.sh does not test bye: still valid
- #34 greet sometimes fails: cannot tell: the issue gives no failing command, no output or exit code, no locale or environment of the build box and no steps to reproduce; main's `test.sh` passes. Unchecked, not ranked.

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
