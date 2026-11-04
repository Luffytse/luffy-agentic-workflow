# Proposed actions

### 1. Create an issue
Issue: new (35-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter gains its quiet and shout flags, rounding out Milestone 1's commands, and its three oldest bugs are fixed.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 5.

## Order

1. #20 Quiet flag: planned feature; no other feature depends on either flag and both move the goal equally, so the Milestone issue's order (first) breaks the tie.
2. #21 Shout flag: planned feature; second in the Milestone issue's order, with no blocker and nothing depending on it.
3. #30 Typo in usage text: ready-for-agent bug, the oldest open (2026-09-01); the usage line names a command, `helo`, that does not exist.
4. #31 Empty name prints `Hello, !`: ready-for-agent bug, filed 2026-09-15; an empty name gives a malformed greeting.
5. #32 Unknown command exits 0 from a pipe: ready-for-agent bug, filed 2026-10-01; scripts cannot tell an unknown command failed.

## Left out

- #33 Trailing space after the greeting: ready-for-agent bug (2026-10-10); the size of 5 was reached.

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
