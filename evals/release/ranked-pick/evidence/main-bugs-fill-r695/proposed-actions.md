### 1. Create a label
Issue: none
Label: release-3

### 2. Create an issue
Issue: new (35-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter gains its quiet and shout flags, completing Milestone 1's commands, and its oldest bugs in usage text, empty names and exit codes are fixed.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 5.

## Order

1. #20 Quiet flag: planned feature, first in the Milestone's order; no feature depends on another, so the Milestone's order stands, and it moves the goal as far as #21.
2. #21 Shout flag: planned feature, second in the Milestone's order; with #20 it completes the Milestone's features.
3. #30 Typo in usage text: `ready-for-agent` bug, oldest open bug (2026-09-01); the usage line names a command that does not exist.
4. #31 Empty name prints `Hello, !`: `ready-for-agent` bug, second oldest (2026-09-15).
5. #32 Unknown command exits 0 from a pipe: `ready-for-agent` bug, third oldest (2026-10-01); a script piping the greeter cannot see the failure, but nothing is lost and delivery is not stopped, so it is not severe.

## Left out

- #33 Trailing space after the greeting: the size was reached (`ready-for-agent` bug, newest, 2026-10-10).

## Checked against main

Main at `37e0025`.

- #20 Quiet flag: still valid
- #21 Shout flag: still valid
- #30 Typo in usage text: still valid
- #31 Empty name prints `Hello, !`: still valid
- #32 Unknown command exits 0 from a pipe: still valid
- #33 Trailing space after the greeting: still valid
- #34 Names with accents come out mangled: cannot tell: the issue gives no example name, no output and no locale; on main `src/greet.sh` echoes the name unchanged and `greet.sh hello José` prints `Hello, José! ` in a UTF-8 locale. Unchecked, not ranked (it is also at `needs-triage`, so not a candidate).

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
~~~

### 3. Apply / remove labels
Issue: 20-quiet.md
Add: release-3
Remove: none

### 4. Apply / remove labels
Issue: 21-shout.md
Add: release-3
Remove: none

### 5. Apply / remove labels
Issue: 30-usage-typo.md
Add: release-3
Remove: none

### 6. Apply / remove labels
Issue: 31-empty-name.md
Add: release-3
Remove: none

### 7. Apply / remove labels
Issue: 32-exit-code.md
Add: release-3
Remove: none
