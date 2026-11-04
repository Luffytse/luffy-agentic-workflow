# Proposed actions

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
Issue: new (38-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter can say goodbye and greet quietly, finishing Milestone 1's planned commands.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Cap:** 5 features. Used: 2. Maintenance fixes: 0, outside the cap.

## Scope

- **Farewell command**: first in the Milestone's order; adds the `bye` command, the first of the Milestone's two remaining commands.
  - #10 Farewell command
  - #11 bye: the command
  - #12 bye: usage text
- **Quiet flag**: second in the Milestone's order; adds `-q`, the last planned feature, so this Release completes the Milestone's feature list.
  - #20 Quiet flag

## Maintenance fixes

None listed: the Triage batch and Release-end Retro planning records for Release 2 were not found in the form this planning reads (see the Release thread's report), so maintenance fixes were left out of this plan.

## Left out

- #31 `--save` overwrites ~/.profile: not a planned feature of Milestone 1 and not a maintenance fix; proposed to the user.
- #35 test.sh takes 10 s: not a planned feature; its `next-release` label and body note are not a Triage batch row or Retro planning verdict this planning reads; proposed to the user.
- #36 test.sh fails on main, so no pull request can pass: not a planned feature and not a maintenance fix; proposed to the user.
- #37 test.sh prints the registry token in CI logs: not a planned feature and not a maintenance fix; proposed to the user.

## Notes

Posted as a comment when the Release is cut. Until then, issues filed during this Release wait for the next Release planning, except Tickets split from a Spec in it.

Planned by the Release thread from the Milestone issue's order, without waiting for the user.
~~~
