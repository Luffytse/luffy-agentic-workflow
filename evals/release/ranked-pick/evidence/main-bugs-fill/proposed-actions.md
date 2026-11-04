# Proposed actions

### 1. Create a label
Issue: none
Label: release-3

### 2. Apply / remove labels
Issue: 20-quiet.md
Add: release-3
Remove: none

### 3. Apply / remove labels
Issue: 21-shout.md
Add: release-3
Remove: none

### 4. Create an issue
Issue: new (35-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter gains its quiet and shout flags, the two commands left in Milestone 1.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Cap:** 5 features. Used: 2. Maintenance fixes: 0, outside the cap.

## Scope

- **Quiet flag**: first in the Milestone's order; adds `-q`, one of the two commands that round out the greeter.
  - #20 Quiet flag
- **Shout flag**: second in the Milestone's order; adds `-s`, the last command the Milestone lists.
  - #21 Shout flag

## Maintenance fixes

None. Release 2's release issue (#2) has no `## Triage batch` comment and no closed `retro-planning` record was created after it, so neither source of maintenance fixes could be read; Release 2's maintenance fixes may be missing.

## Left out

- #30 Typo in usage text, #31 Empty name prints a double space, #32 Unknown command exits 0 from a pipe, #33 Trailing space after the greeting: `ready-for-agent` bugs that the Milestone issue does not list and that no Triage batch or Retro planning chose as maintenance fixes; each is put to the user to plan or not.
- #34 Names with accents come out mangled: `needs-triage`, so it belongs to `triage`, not Release planning.

## Notes

Posted as a comment when the Release is cut. Until then, issues filed during this Release wait for the next Release planning, except Tickets split from a Spec in it.

Planned by the Release thread from the Milestone issue's order, without waiting for the user.
~~~
