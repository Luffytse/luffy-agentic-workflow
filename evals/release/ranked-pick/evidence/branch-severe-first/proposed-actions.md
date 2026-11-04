# Proposed actions

### 1. Create a label
Issue: none
Label: release-3

### 2. Create an issue
Issue: new (36-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter stops writing names to a world-readable log, its tests run fast again, and it gains the bye command and the quiet flag.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 5.

## Order

1. #31 greet.sh writes every name to a world-readable log: group 1, severe: a security hole that leaks names, including email addresses, to every user on the machine.
2. #35 test.sh takes 10 s: group 1, marked `next-release` by Release 2's retro planning: `test.sh` sleeps 10 s for nothing, slowing every check.
3. #10 Farewell command: group 2, planned feature (Spec, with Tickets #11 and #12); no feature depends on another, so the Milestone's order stands and it comes first, as the larger step toward rounding out the commands.
4. #20 Quiet flag: group 2, planned feature; second in the Milestone's order, with no open blockers.
5. #30 Typo in usage text: group 3, `ready-for-agent` bug, the oldest open (filed 2026-09-01).

## Left out

None.

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
~~~

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
