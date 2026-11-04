### 1. Create a label
Issue: none
Label: release-3

### 2. Apply / remove labels
Issue: 26-config.md
Add: release-3
Remove: none

### 3. Create an issue
Issue: new (27-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** The greeter reads its output format and colour from a config file, the base the Milestone's colour and JSON output build on.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Cap:** 5 features. Used: 1. Maintenance fixes: 0, outside the cap.

## Scope

- **Config file loader**: third in the Milestone's order and the first planned feature that is unblocked; it gives scripts a stable `~/.greetrc` and clears the blocker of #24 and #25.
  - #26 Config file loader

## Maintenance fixes

None. The Triage batch and the Release-end Retro planning for Release 2 (#2) left no readable record (no `## Triage batch` comment on #2, no closed `retro-planning` issue created after #2), so maintenance fixes were left out of this plan.

## Left out

- #24 Colour output: first in the Milestone's order, blocked by #26 (open). Waits for the next Release.
- #25 JSON output for scripts: second in the Milestone's order, blocked by #26 (open). Waits for the next Release.

## Notes

Posted as a comment when the Release is cut. Until then, issues filed during this Release wait for the next Release planning, except Tickets split from a Spec in it.

Planned by the Release thread from the Milestone issue's order, without waiting for the user.
~~~
