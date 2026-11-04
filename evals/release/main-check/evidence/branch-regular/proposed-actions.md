### 1. Close
Issue: 30-usage-typo.md
Outcome: not planned
Reason: Checked against main: already fixed. `src/greet.sh` usage line reads `usage: greet.sh [-s] hello|bye <name>` (fixed by pull request #7, commit bcde54a, which did not close the issue).

### 2. Close
Issue: 32-version-zero.md
Outcome: not planned
Reason: Checked against main: obsolete. `src/greet.sh` has no `--version` option any more; pull request #10 (commit 9c924f4) removed it because the repo keeps no version (release doc policy: none).

### 3. Edit an issue body
Issue: 31-name-spaces.md
Body:
~~~
Names with spaces are cut at the first space, now in `bye` only:

- `greet.sh bye "Ada Lovelace"` prints `Goodbye, Ada!`

It should print `Goodbye, Ada Lovelace!`.

(`greet.sh hello "Ada Lovelace"` already prints the whole name.)

Checked against main: `hello` was fixed by pull request #9 (commit 8cb86e9); `bye` in `src/greet.sh` still cuts the name with `cut -d' ' -f1`.
~~~

### 4. Comment on an issue
Issue: 21-shout.md
Body:
~~~
Checked against main: already done. `src/greet.sh` handles `-s` (`greet.sh -s hello Ada` prints `HELLO, ADA!`), merged in pull request #8 (commit dabd7f9), which did not close this issue. This is a feature the Milestone issue lists, so closing it would change the Milestone's agreement: question for the user: close #21 as completed (shipped by #8), or keep it open for something more? It is not ranked in the next Release until answered.
~~~

### 5. Create a label
Issue: new
Label: release-3

### 6. Create an issue
Issue: new (46-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
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
~~~

### 7. Apply / remove labels
Issue: 20-quiet.md
Add: release-3
Remove: none

### 8. Apply / remove labels
Issue: 31-name-spaces.md
Add: release-3
Remove: none

### 9. Apply / remove labels
Issue: 33-test-bye.md
Add: release-3
Remove: none
