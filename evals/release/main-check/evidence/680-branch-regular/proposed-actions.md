### 1. Close
Issue: 30-usage-typo.md
Outcome: completed
Reason: Checked against main: already fixed. `src/greet.sh` usage line now reads `usage: greet.sh [-s] hello|bye <name>`; fixed by pull request #7 (bcde54a, "fix: usage line says hello"). This unblocks #22.

### 2. Comment on an issue
Issue: 21-shout.md
Body:
~~~
Checked against main: `src/greet.sh` already does what this issue asks. `-s` before the command prints the greeting in capitals (pull request #8, dabd7f9, "feat: -s shouts the greeting"); `greet.sh -s hello Ada` prints `HELLO, ADA!`. This is a planned feature of Milestone #1, so closing it would change the Milestone's agreement and it is not closed here. Question for the user: close #21 as completed (work already on main), or keep it open for something more? It is left out of Release 3 until you answer; nothing waits on the reply.
~~~

### 3. Edit an issue body
Issue: 31-name-spaces.md
Body:
~~~
Checked against main: `hello` was fixed by pull request #9 (8cb86e9, "fix: hello keeps the whole name"); only `bye` still drops everything after the first space (`src/greet.sh`, the `bye` case still pipes the name through `cut -d' ' -f1`). Scope narrowed to `bye`.

`bye` drops everything after the first space of the name:

- `greet.sh bye "Ada Lovelace"` prints `Goodbye, Ada!`

It should print the whole name, `Goodbye, Ada Lovelace!`.
~~~

### 4. Close
Issue: 32-version-zero.md
Outcome: completed
Reason: Checked against main: obsolete. The `--version` option is gone from `src/greet.sh` (pull request #10, 9c924f4, "chore: drop --version"), and `docs/dev-skills/release.md` says this repo keeps no version (policy: none), so there is nothing left to print.

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
**Goal:** The greeter gets its quiet and help flags, and `bye` and the tests stop being broken for full names and for `bye`.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 4.

## Order

1. #20 Quiet flag: planned feature, first in the Milestone's order; nothing depends on it, so the Milestone's order stands.
2. #22 Help flag: planned feature; its blocker #30 was closed as completed by the check against main (usage line already fixed), so it is startable.
3. #31 Names with spaces are cut at the first space: `ready-for-agent` bug, oldest (2026-09-05); scope narrowed to `bye` by the check against main.
4. #33 test.sh does not test bye: `ready-for-agent` bug, next oldest (2026-09-15).

## Left out

- #21 Shout flag: planned feature, but main already has it; closing it would change the Milestone's agreement, so it waits on the user's answer and is not ranked.
- #34 greet sometimes fails: unchecked (cannot tell), not ranked.

## Checked against main

Main at `9c924f4`.

- #20 Quiet flag: still valid
- #21 Shout flag: already fixed: `src/greet.sh` handles `-s` (pull request #8, dabd7f9); a planned feature, so not closed, a question went to the user on the issue
- #22 Help flag: still valid: `src/greet.sh` has no `-h`
- #30 Typo in usage text: already fixed: usage line reads `hello|bye` on main (pull request #7, bcde54a); closed as completed
- #31 Names with spaces are cut at the first space: changed scope: `hello` fixed by pull request #9 (8cb86e9), `bye` still cuts the name; body updated
- #32 --version always prints 0.0.0: obsolete: `--version` removed by pull request #10 (9c924f4) and the repo keeps no version; closed as completed
- #33 test.sh does not test bye: still valid: `test.sh` checks `hello` only
- #34 greet sometimes fails: cannot tell: no steps, error or locale named, so it cannot be reproduced from main; says what is missing: a command line, the output and the locale

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
