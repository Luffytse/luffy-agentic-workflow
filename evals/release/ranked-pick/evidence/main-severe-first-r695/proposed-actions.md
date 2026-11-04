# Proposed actions

### 1. Create an issue
Issue: new (36-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter stops leaking the names it is given, and gains its farewell command and quiet flag.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 5.

## Order

1. #31 greet.sh writes every name to a world-readable log: severe (a security hole): every run appends the name, sometimes an email address, to `/tmp/greet.log` at mode 0666, readable by every user on the machine.
2. #35 test.sh takes 10 s: marked `next-release` by Release 2's Retro planning; `test.sh` sleeps 10 s for nothing, slowing every pre-push check.
3. #10 Farewell command: first planned feature; no feature depends on another, and it adds a whole new command, moving the Milestone's goal (round out the greeter's commands) furthest; it is also first in the Milestone's order. Stands for its Tickets #11 and #12.
4. #20 Quiet flag: second planned feature; a flag on existing commands, a smaller step toward the goal, and second in the Milestone's order.
5. #30 Typo in usage text: `ready-for-agent` bug, open since 2026-09-01, the oldest bug; the usage line still says `greet.sh helo`.

## Left out

None.

## Checked against main

Main at `49b4077`.

- #10 Farewell command: still valid
- #11 bye: the command: still valid
- #12 bye: usage text: still valid
- #20 Quiet flag: still valid
- #30 Typo in usage text: still valid
- #31 greet.sh writes every name to a world-readable log: still valid
- #35 test.sh takes 10 s: still valid

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
~~~

### 2. Create a label
Issue: none
Label: release-3

### 3. Apply / remove labels
Issue: 31-name-log.md
Add: release-3
Remove: none

### 4. Apply / remove labels
Issue: 35-slow-test.md
Add: release-3
Remove: none

### 5. Apply / remove labels
Issue: 10-farewell.md
Add: release-3
Remove: none

### 6. Apply / remove labels
Issue: 11-bye-code.md
Add: release-3
Remove: none

### 7. Apply / remove labels
Issue: 12-bye-usage.md
Add: release-3
Remove: none

### 8. Apply / remove labels
Issue: 20-quiet.md
Add: release-3
Remove: none

### 9. Apply / remove labels
Issue: 30-usage-typo.md
Add: release-3
Remove: none

### 10. Apply / remove labels
Issue: 35-slow-test.md
Add: none
Remove: next-release
