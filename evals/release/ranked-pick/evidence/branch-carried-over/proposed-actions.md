### 1. Create an issue
Issue: new (35-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter gains its quiet flag and no longer greets an empty name as `Hello, !`.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 2.

## Order

1. #20 Quiet flag: the Milestone's only planned feature, first in its order; no feature depends on another, and it has no open blockers.
2. #31 Empty name prints `Hello, !`: carried over from Release 2 (its `## Carried over` section: the fix needed a decision on the empty name); a bug, so placed in group 3, and the oldest open bug (2026-09-15).

## Left out

None.

## Checked against main

Main at `463ac14`.

- #20 Quiet flag: still valid
- #31 Empty name prints `Hello, !`: still valid
- #32 Trailing space after the greeting: still valid

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
Issue: 31-empty-name.md
Add: release-3
Remove: none
