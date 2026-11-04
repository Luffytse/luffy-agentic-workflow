# Proposed actions: release run, 2026-11-04T09:00Z

Find where you are: no open release issue; no open issue carries a release label; the last release issue, #2 Release 2 (closed), holds both end-of-Release records. Case 4 goes to step 5: plan the next Release. Main at `9c924f4`.

### 1. Comment on an issue
Issue: 21-shout.md
Body:
~~~
Checked against main: main at `9c924f4` already does what this issue asks. `-s` was added by #8 (`dabd7f9`, "feat: -s shouts the greeting"), and `bash src/greet.sh -s hello Ada` prints `HELLO, ADA!`. #8's body has no closing keyword, so this issue stayed open. It is a planned feature of Milestone #1, so it is not closed without you: should it be closed as completed by #8? It waits for your answer, unranked, and is not in Release 3.
~~~

### 2. Comment on an issue
Issue: 30-usage-typo.md
Body:
~~~
Checked against main: main at `9c924f4` is already fixed. #7 (`bcde54a`, "fix: usage line says hello") changed the usage line, and `bash src/greet.sh` with no command now prints `usage: greet.sh [-s] hello|bye <name>`. #7's body says it does not close this issue. This issue is the only blocker of the planned feature #22 Help flag. Closing it as not planned would mean that blocker never clears (the tracker doc's Count open blockers rule), and #22 could never start. That would change Milestone #1's agreement, so it is not closed without you: should it be closed as completed by #7, which clears #22? Until you answer, #22 is left out of Release 3.
~~~

### 3. Edit an issue body
Issue: 31-name-spaces.md
Body:
~~~
`bye` drops everything after the first space of the name:

- `greet.sh bye "Ada Lovelace"` prints `Goodbye, Ada!`

It should print the whole name.

Checked against main: `hello` keeps the whole name since #9 (`8cb86e9`, "fix: hello keeps the whole name"); only `bye` still cuts it (`src/greet.sh`, the `bye)` line's `cut -d' ' -f1`), as of main at `9c924f4`.
~~~

### 4. Close
Issue: 32-version-zero.md
Outcome: not planned
Reason: Checked against main: obsolete. #10 (`9c924f4`, "chore: drop --version") removed `--version` from `src/greet.sh` because the repo keeps no version, and `greet.sh --version` now prints the usage line and exits 2.

### 5. Create an issue
Issue: new (46-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter gains its quiet flag, and `bye` keeps the whole name and is covered by `test.sh`.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 3.

## Order

1. #20 Quiet flag: the only planned feature that can start. No planned feature depends on another, and Milestone #1's order breaks the tie (#21 waits on the user and #22 is left out).
2. #31 Names with spaces are cut at the first space: a `ready-for-agent` bug, the oldest one left (2026-09-05). Its scope is now `bye` only.
3. #33 test.sh does not test bye: a `ready-for-agent` bug (2026-09-15). A broken `bye`, the command #31 changes, would still pass the check.

## Left out

- #22 Help flag: its blocker #30 is not cleared. #30's fix is on main, and the question on #30 asks whether to close it as completed. #22 waits for that answer.

## Checked against main

Main at `9c924f4`.

- #20 Quiet flag: still valid
- #21 Shout flag: already fixed: #8 (`dabd7f9`) added `-s`, and `greet.sh -s hello Ada` prints `HELLO, ADA!`. It is a planned feature, so it is not closed: it goes to the user as a question and waits, unranked.
- #22 Help flag: still valid
- #30 Typo in usage text: already fixed: #7 (`bcde54a`) changed the usage line in `src/greet.sh` to `hello`. Not closed: closing it as not planned would leave #22's blocker uncleared forever, so it goes to the user as a question.
- #31 Names with spaces are cut at the first space: changed scope: #9 (`8cb86e9`) fixed `hello`, and `bye` still cuts the name at the first space (`src/greet.sh`, the `bye)` line). The body now covers `bye` only.
- #32 --version always prints 0.0.0: obsolete: #10 (`9c924f4`) removed `--version` from `src/greet.sh`. Closed as not planned.
- #33 test.sh does not test bye: still valid
- #34 greet sometimes fails: cannot tell: the issue does not give the command that was run, the error output or the build box's locale, and nothing on main can be tied to the failure. Unchecked, and not ranked.

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
Issue: 31-name-spaces.md
Add: release-3
Remove: none

### 9. Apply / remove labels
Issue: 33-test-bye.md
Add: release-3
Remove: none
