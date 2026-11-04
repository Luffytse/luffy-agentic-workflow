# Proposed actions

### 1. Create an issue
Issue: new (04-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter says goodbye, takes a quiet flag, and its usage text reads right.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 3.

## Order

1. #10 Farewell command: planned feature, first in the Milestone's order; no feature depends on another, and it adds a whole new command, moving the goal of rounding out the commands furthest. A Spec, standing for its Tickets #11 and #12.
2. #20 Quiet flag: planned feature, second in the Milestone's order; no blockers.
3. #30 Typo in usage text: a `ready-for-agent` bug, open since 2026-09-01, the oldest bug waiting.

## Left out

None.

## Proposed to the user

- #50 Colour output: an unplanned feature; the Milestone issue does not list it.
- #51 Run shellcheck in test.sh: an unplanned feature; the Milestone issue does not list it (it is also at `ready-for-human`).

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
~~~

### 2. Create a label
Issue: none
Label: release-3

### 3. Apply / remove labels
Issue: 10-farewell.md
Add: release-3
Remove: none

### 4. Apply / remove labels
Issue: 11-bye-code.md
Add: release-3
Remove: none

### 5. Apply / remove labels
Issue: 12-bye-usage.md
Add: release-3
Remove: none

### 6. Apply / remove labels
Issue: 20-quiet.md
Add: release-3
Remove: none

### 7. Apply / remove labels
Issue: 30-usage-typo.md
Add: release-3
Remove: none
