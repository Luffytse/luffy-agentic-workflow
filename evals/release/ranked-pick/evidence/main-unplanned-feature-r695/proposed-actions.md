### 1. Create an issue
Issue: new (52-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter says goodbye with a `bye` command, takes a `-q` quiet flag, and its usage line names `hello` correctly.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Size:** 5. Used: 3.

## Order

1. #10 Farewell command: Milestone feature 1; nothing depends on either feature, and a whole new command moves "Round out the greeter's commands" furthest; the Milestone's order agrees. Spec, standing for its Tickets #11 and #12.
2. #20 Quiet flag: Milestone feature 2; independent of #10, a flag rather than a new command, so it moves the goal less; the Milestone's order agrees.
3. #30 Typo in usage text: a `ready-for-agent` bug, the oldest open one (2026-09-01); users are shown a command, `helo`, that does not exist.

## Left out

None.

## Checked against main

Main at `af44282`.

- #10 Farewell command: still valid
- #11 bye: the command: still valid
- #12 bye: usage text: still valid
- #20 Quiet flag: still valid
- #30 Typo in usage text: still valid
- #50 Colour output: still valid
- #51 Run shellcheck in test.sh: still valid

## Proposed to the user

- #50 Colour output: an unplanned feature; the Milestone issue does not list it.
- #51 Run shellcheck in test.sh: an unplanned feature; the Milestone issue does not list it. It is at `ready-for-human`, so it waits on the user either way.

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
