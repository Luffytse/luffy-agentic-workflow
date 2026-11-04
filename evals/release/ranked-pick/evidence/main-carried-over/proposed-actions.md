# Proposed actions

Release thread, 2026-11-04T09:00:00Z. "Find where you are": no open release issue, no open issue carries an unnamed release label, and the last release issue (#2, Release 2) is closed with both end-of-Release records, so the run goes to step 5 and plans Release 3.

### 1. Create an issue
Issue: new (35-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter gains its quiet flag and stops greeting an empty name as `Hello, !`.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 2.

## Order

1. #20 Quiet flag: the Milestone's only planned feature, with no open blockers; it is the one thing left that moves the Milestone's goal.
2. #31 Empty name prints `Hello, !`: a bug carried over from Release 2 (its fix needed a decision on the empty name), oldest open bug (2026-09-15).

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
