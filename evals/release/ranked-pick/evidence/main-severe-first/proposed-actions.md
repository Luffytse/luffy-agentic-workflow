# Proposed actions (dry run)

### 1. Create a label
Issue: none
Label: release-3

### 2. Apply / remove labels
Issue: 31-name-log.md
Add: release-3
Remove: none

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
Issue: 35-slow-test.md
Add: release-3
Remove: none

### 8. Create an issue
Issue: new (36-release-3.md)
Title: Release 3
Labels: none
Parent: none
Body:
~~~
**Goal:** Close the name-leaking log hole, then round out the greeter with the farewell command and the quiet flag.

**Label:** `release-3`. Every issue in this Release carries it.

**Milestone:** #1

**Cap:** 5 features. Used: 2. Maintenance fixes: 2, outside the cap.

## Scope

- **Farewell command**: first in the Milestone issue's order; adds the `bye` command, moving the Milestone toward rounded-out commands. Unblocked, not parked.
  - #10 Farewell command
  - #11 bye: the command
  - #12 bye: usage text
- **Quiet flag**: second in the Milestone issue's order; adds `-q`, the Milestone's last planned feature. Unblocked, not parked.
  - #20 Quiet flag

## Maintenance fixes

- #31 greet.sh writes every name to a world-readable log: a security hole (names, including email addresses, readable by every user). The release doc's Release size rule says a severe issue joins past the size; build it first, before the features. Filed 2026-10-20, after Release 2's triage pass, so no Triage batch has seen it.
- #35 test.sh takes 10 s: Retro planning for Release 2 marked it to join the next Release (its `next-release` label and its body).

## Left out

- #30 Typo in usage text: not a planned feature of Milestone #1 and not marked by a Triage batch or Retro planning; `src/greet.sh` already reads `greet.sh hello`, so it looks stale and goes back to `triage`.

## Notes

Posted as a comment when the Release is cut. Until then, issues filed during this Release wait for the next Release planning, except Tickets split from a Spec in it.

Planned by the Release thread from the Milestone issue's order, without waiting for the user.
~~~
