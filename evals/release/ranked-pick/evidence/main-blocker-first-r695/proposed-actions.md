### 1. Create an issue
Issue: new (41-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter gains its farewell command and a working quiet flag, with flags after the name no longer dropped and the usage line's typo fixed.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 4.

## Order

1. #10 Farewell command: planned feature 1; no other feature depends on either planned feature, and a new command moves the Milestone's goal (round out the greeter's commands) furthest; the Milestone issue's order agrees. A Spec, standing for its Tickets #11 and #12.
2. #40 Flags after the name are dropped: open blocker of planned feature #20 (Quiet flag), so it lands just before it in group 2 rather than among the bugs.
3. #20 Quiet flag: planned feature 2, a flag rather than a command, so it moves the goal less than #10; placed right after its blocker #40.
4. #30 Typo in usage text: `ready-for-agent` bug, the oldest open bug (2026-09-01).

## Left out

None.

## Checked against main

Main at `af44282`.

- #10 Farewell command: still valid
- #11 bye: the command: still valid
- #12 bye: usage text: still valid
- #20 Quiet flag: still valid
- #30 Typo in usage text: still valid
- #40 Flags after the name are dropped: still valid

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
