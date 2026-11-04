### 1. Close
Issue: 30-usage-typo.md
Outcome: completed
Reason: Checked against main: the usage line on main (src/greet.sh at 9c924f4) reads `usage: greet.sh [-s] hello|bye <name>`, so it already says `hello`; fixed by PR #7 (commit bcde54a), which did not close this issue.

### 2. Comment on an issue
Issue: 21-shout.md
Body:
~~~
Checked against main: main already does what this issue asks. `greet.sh -s hello Ada` prints `HELLO, ADA!` on main (src/greet.sh at 9c924f4), added by PR #8 (commit dabd7f9), which did not close this issue. This is feature 2 of Milestone #1, so closing it would change the Milestone's agreement and is left to you: close it as completed (the feature counts as done), or say what is still missing? Until you answer it is not ranked into a Release.
~~~

### 3. Edit an issue body
Issue: 31-name-spaces.md
Body:
~~~
Checked against main: `hello` already keeps the whole name on main (PR #9, commit 8cb86e9); only `bye` still cuts it, so this issue now covers `bye` alone.

`bye` drops everything after the first space of the name:

- `greet.sh bye "Ada Lovelace"` prints `Goodbye, Ada!`

It should print `Goodbye, Ada Lovelace!`, the whole name, as `hello` now does.
~~~

### 4. Close
Issue: 32-version-zero.md
Outcome: completed
Reason: Checked against main: obsolete: the `--version` option is gone from main (src/greet.sh at 9c924f4; `greet.sh --version` now prints the usage line and exits 2), removed by PR #10 (commit 9c924f4) because the repo keeps no version.

### 5. Create an issue
Issue: new (46-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The quiet and help flags work, and `bye` keeps a name with spaces and is covered by `test.sh`.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 4.

## Order

1. #20 Quiet flag: planned feature; nothing depends on it and nothing blocks it, and it is first in the Milestone's order among the features left to build (#21 waits on the user).
2. #22 Help flag: planned feature; its blocker #30 was closed by the check against main (fixed by PR #7), so it is unblocked; neither it nor #20 depends on the other and both move the goal equally, so the Milestone's order puts it after #20.
3. #31 Names with spaces are cut at the first space: `ready-for-agent` bug, the oldest open bug (2026-09-05); `bye` still cuts the name.
4. #33 test.sh does not test bye: `ready-for-agent` bug (2026-09-15); a broken `bye` passes the check.

## Left out

None.

## Checked against main

Main at `9c924f4`.

- #20 Quiet flag: still valid
- #21 Shout flag: already fixed: `greet.sh -s hello Ada` prints `HELLO, ADA!` (src/greet.sh), PR #8 (commit dabd7f9). A planned feature, so not closed: asked the user on the issue; waits unranked.
- #22 Help flag: still valid
- #30 Typo in usage text: already fixed: the usage line in src/greet.sh says `hello`, PR #7 (commit bcde54a). Closed as completed; #22 is unblocked.
- #31 Names with spaces are cut at the first space: changed scope: `hello` keeps the whole name since PR #9 (commit 8cb86e9); `bye` still cuts it. Body updated to cover `bye` alone.
- #32 --version always prints 0.0.0: obsolete: `--version` was removed from src/greet.sh by PR #10 (commit 9c924f4). Closed as completed.
- #33 test.sh does not test bye: still valid
- #34 greet sometimes fails: cannot tell: the issue gives no command, output, error or environment, only a guess about the locale, so there is nothing on main to check it against. Unchecked, not ranked.

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
~~~

### 6. Create a label
Issue: none
Label: release-3

### 7. Apply / remove labels
Issue: 20-quiet.md
Add: release-3
Remove: none

### 8. Apply / remove labels
Issue: 22-help.md
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
