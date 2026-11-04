# Proposed actions

### 1. Create an issue
Issue: new (51-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter gains its quiet flag, and unknown commands and the usage text behave as they should.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 3.

## Order

1. #20 Quiet flag: group 2, the Milestone's only planned feature; no open blockers; it is the Milestone's goal.
2. #33 Unknown command exits 0 from a pipe: group 3, carried over from Release 2 and still at `ready-for-agent`; the user kept it going, so it comes before the other bugs.
3. #30 Typo in usage text: group 3, a `ready-for-agent` bug, open since 2026-09-01.

## Left out

- #31 Empty name prints `Hello, !`: carried over, an agent cannot take it: no state label (`bug` only; the fix waits on a decision: greet `world`, or refuse an empty name).

## Checked against main

Main at `cdcf69855464659c0e3b50e4ae7bbf8a1fdf4d3d`.

- #20 Quiet flag: still valid
- #30 Typo in usage text: still valid
- #31 Empty name prints `Hello, !`: still valid
- #32 Trailing space after the greeting: still valid
- #33 Unknown command exits 0 from a pipe: still valid
- #50 Colour output: still valid

## Proposed to the user

- #50 Colour output: an unplanned feature; the Milestone issue does not list it; carried over from Release 2

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
Issue: 33-exit-code.md
Add: release-3
Remove: none

### 5. Apply / remove labels
Issue: 30-usage-typo.md
Add: release-3
Remove: none
