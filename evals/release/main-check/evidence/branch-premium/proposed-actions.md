### 1. Close
Issue: 30-usage-typo.md
Outcome: not planned
Reason: Checked against main: already fixed: the usage line on main (`src/greet.sh`, the `*)` branch) prints `usage: greet.sh [-s] hello|bye <name>`, fixed by pull request #7 (bcde54a), which did not close this issue; running `greet.sh` with no command confirms it.

### 2. Comment on an issue
Issue: 21-shout.md
Body:
~~~
Checked against main: main already does what this issue asks. Pull request #8 (dabd7f9) added `-s`: `src/greet.sh` shifts a leading `-s` and upper-cases the output, and `bash src/greet.sh -s hello Ada` prints `HELLO, ADA!` on main at 9c924f4. That pull request did not close this issue. This is feature 2 of Milestone #1, so I have not closed it: closing it would change the Milestone's agreement. Should it be closed as done (its acceptance, "it works as its issue says", reads as met), or does it still lack something? Until you answer it waits, unranked, outside Release 3.
~~~

### 3. Edit an issue body
Issue: 31-name-spaces.md
Body:
~~~
`bye` drops everything after the first space of the name:

- `greet.sh bye "Ada Lovelace"` prints `Goodbye, Ada!`

It should print the whole name.

Checked against main: `hello` already keeps the whole name since pull request #9 (8cb86e9); only `bye` still cuts it, at the `cut -d' ' -f1` on its line in `src/greet.sh`.
~~~

### 4. Read an issue
Issue: 31-name-spaces.md
(Read back after the edit: the body must be exactly the body in block 3.)

### 5. Close
Issue: 32-version-zero.md
Outcome: not planned
Reason: Checked against main: obsolete: pull request #10 (9c924f4) removed the `--version` option from `src/greet.sh` because the repo keeps no version (`docs/dev-skills/release.md`, policy none); `greet.sh --version` now prints the usage line and exits 2, so there is no version output left to fix.

### 6. Create an issue
Issue: new (46-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
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
~~~

### 7. Create a label
Issue: none
Label: release-3

### 8. Apply / remove labels
Issue: 20-quiet.md
Add: release-3
Remove: none

### 9. Apply / remove labels
Issue: 31-name-spaces.md
Add: release-3
Remove: none

### 10. Apply / remove labels
Issue: 33-test-bye.md
Add: release-3
Remove: none
