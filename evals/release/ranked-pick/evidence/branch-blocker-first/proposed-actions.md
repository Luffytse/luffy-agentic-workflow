### 1. Create an issue
Issue: new (41-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter says goodbye and takes a quiet flag, finishing Milestone 1's commands.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 4.

## Order

1. #10 Farewell command: planned feature; no other feature depends on it or on the quiet flag, and adding a whole new command moves the Milestone's goal (round out the greeter's commands) furthest, which also matches the Milestone's order. Its Tickets #11 and #12 come with it.
2. #40 Flags after the name are dropped: bug that blocks the planned feature #20 Quiet flag, so it goes in group 2 just before it.
3. #20 Quiet flag: planned feature; second in the Milestone's order and a smaller step toward its goal than a new command; startable once its blocker #40 lands.
4. #30 Typo in usage text: `ready-for-agent` bug, open since 2026-09-01.

## Left out

None.

## Proposed to the user

None.

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
Issue: 40-flag-parse.md
Add: release-3
Remove: none

### 7. Apply / remove labels
Issue: 20-quiet.md
Add: release-3
Remove: none

### 8. Apply / remove labels
Issue: 30-usage-typo.md
Add: release-3
Remove: none
