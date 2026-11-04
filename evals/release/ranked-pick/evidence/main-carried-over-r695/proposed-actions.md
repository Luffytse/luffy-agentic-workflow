### 1. Create an issue
Issue: new (51-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter gains its quiet flag, and its usage text and unknown-command exit code behave as they should.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 3.

## Order

1. #20 Quiet flag: the Milestone's only planned feature, and what moves its goal (rounding out the commands) furthest; no open blockers.
2. #33 Unknown command exits 0 from a pipe: carried over from Release 2 at `ready-for-agent`; the user chose to keep it going, so it leads group 3.
3. #30 Typo in usage text: the oldest other `ready-for-agent` bug (filed 2026-09-01); the usage line still says `helo`.

## Left out

- #31 Empty name prints `Hello, !`: carried over, an agent cannot take it: no state label (only `bug`; the fix still waits on a decision: greet `world`, or refuse an empty name).

## Checked against main

Main at `37e0025`.

- #20 Quiet flag: still valid
- #30 Typo in usage text: still valid
- #31 Empty name prints `Hello, !`: still valid
- #32 Trailing space after the greeting: still valid
- #33 Unknown command exits 0 from a pipe: still valid
- #50 Colour output: still valid

## Proposed to the user

- #50 Colour output: an unplanned feature; the Milestone issue does not list it (the user removed it from Milestone 1's features on 2026-10-18); carried over from Release 2.

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
