### 1. Create a label
Issue: none
Label: release-3

### 2. Apply / remove labels
Issue: 10-farewell.md
Add: release-3
Remove: none

### 3. Apply / remove labels
Issue: 11-bye-code.md
Add: release-3
Remove: none

### 4. Apply / remove labels
Issue: 12-bye-usage.md
Add: release-3
Remove: none

### 5. Apply / remove labels
Issue: 20-quiet.md
Add: release-3
Remove: none

### 6. Create an issue
Issue: new (52-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter can say goodbye and greet quietly, finishing the commands Milestone 1 plans.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1 Milestone 1: Round out the greeter's commands

**Cap:** 5 features. Used: 2. Maintenance fixes: 0, outside the cap.

## Scope

- **Farewell command**: first in the Milestone's order; adds the `bye` command the Milestone's goal calls for.
  - #10 Farewell command
  - #11 bye: the command
  - #12 bye: usage text
- **Quiet flag**: second in the Milestone's order; adds the `-q` flag, the Milestone's last planned feature.
  - #20 Quiet flag

## Maintenance fixes

None. The Triage batch rows (`## Triage batch` comments on the Release 2 issue, #2) and a closed Retro planning record created after #2 were not found, so maintenance fixes were not read for this planning and may be missing.

## Left out

- #30 Typo in usage text: not a planned feature of the Milestone and not chosen as a maintenance fix; put to the user as a question.
- #50 Colour output: not listed by the Milestone issue, and colour is not a command, so it does not serve the Milestone's goal.
- #51 Run shellcheck in test.sh: `ready-for-human`, not a candidate here.

## Notes

Posted as a comment when the Release is cut. Until then, issues filed during this Release wait for the next Release planning, except Tickets split from a Spec in it.

Planned by the Release thread from the Milestone issue's order, without waiting for the user.
~~~
