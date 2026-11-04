# Proposed actions

### 1. Create an issue
Issue: new (31-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter gains its quiet, shout and read-names-from-a-file options.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 3. Used: 3.

## Order

1. #20 Quiet flag: planned feature; no feature depends on another, all move the goal equally, so the Milestone issue's order (1st) breaks the tie.
2. #21 Shout flag: planned feature; no dependencies, equal weight toward the goal, Milestone issue's order (2nd) breaks the tie.
3. #22 Read names from a file: planned feature; no dependencies, equal weight toward the goal, Milestone issue's order (3rd) breaks the tie.

## Left out

- #23 Repeat flag: the size was reached (planned feature, ranked 4th by the Milestone issue's order).
- #30 Typo in usage text: the size was reached (group 3, `ready-for-agent` bug, open since 2026-09-01).

## Proposed to the user

None.

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
~~~

### 2. Create a label
Issue: none
Label: release-3

### 3. Apply / remove labels
Issue: 20-quiet.md
Add: release-3
Remove: none

### 4. Apply / remove labels
Issue: 21-shout.md
Add: release-3
Remove: none

### 5. Apply / remove labels
Issue: 22-name-file.md
Add: release-3
Remove: none
