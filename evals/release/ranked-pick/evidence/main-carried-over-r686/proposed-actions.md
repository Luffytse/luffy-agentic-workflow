# Proposed actions

### 1. Create an issue
Issue: new (51-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter gains its quiet flag, and its usage text, empty-name greeting and unknown-command exit code are fixed.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 4.

## Order

1. #20 Quiet flag: the Milestone's only planned feature, with no blockers; it is the work that moves "Round out the greeter's commands" furthest.
2. #30 Typo in usage text: `ready-for-agent` bug, the oldest (2026-09-01); the usage line still sends users to a command that does not exist.
3. #31 Empty name prints `Hello, !`: carried over from Release 2 (the fix needed a decision on the empty name); a bug from 2026-09-15, placed with the bugs by age. The decision (greet `world`, or refuse an empty name) is still open in its body.
4. #33 Unknown command exits 0 from a pipe: `ready-for-agent` bug from 2026-10-01, carried over from Release 2 (not finished in time); scripts cannot tell a bad command from a good one.

## Left out

None.

## Checked against main

Main at `cdcf698`.

- #20 Quiet flag: still valid
- #30 Typo in usage text: still valid
- #31 Empty name prints `Hello, !`: still valid
- #32 Trailing space after the greeting: still valid
- #33 Unknown command exits 0 from a pipe: still valid
- #50 Colour output: still valid

## Proposed to the user

- #50 Colour output: an unplanned feature; the Milestone issue does not list it (the user removed it from Milestone 1's features on 2026-10-18), though Release 2 carried it over.

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
Issue: 30-usage-typo.md
Add: release-3
Remove: none

### 5. Apply / remove labels
Issue: 31-empty-name.md
Add: release-3
Remove: none

### 6. Apply / remove labels
Issue: 33-exit-code.md
Add: release-3
Remove: none
