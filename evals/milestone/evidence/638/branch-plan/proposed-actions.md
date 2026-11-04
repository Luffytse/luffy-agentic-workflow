### 1. Create a label
Issue: none
Label: milestone-1

### 2. Create an issue
Issue: new (31-milestone-1.md)
Title: Milestone 1: Farewell and quiet
Labels: milestone-1
Parent: none
Body:
~~~
## Goal

By the end, the greeter can say goodbye and can run silently in scripts, so it can ship as 1.0.

## Features, in build order

In this order, up to 2 at once. Each feature is its own issue carrying `milestone-1`.

| # | Feature | Kind | Accepted when |
| --- | --- | --- | --- |
| 1 | `.scratch/issues/10-farewell.md` Farewell command (Tickets `.scratch/issues/11-bye-code.md`, `.scratch/issues/12-bye-usage.md`) | Spec | `greet.sh bye Ada` prints `Goodbye, Ada!` and exits 0; `greet.sh bye` prints `Goodbye, world!`; `bash test.sh` covers both. |
| 2 | `.scratch/issues/20-quiet.md` Quiet flag | lone Ticket | `greet.sh --quiet hello Ada` prints nothing and exits 0; `greet.sh --quiet nope` prints nothing and exits 2. |

## Acceptance

- Every feature above is merged and its issue closed.
- At the Milestone review the user runs `greet.sh --quiet bye Ada` and sees nothing.

## Excluded

- Colour output (`.scratch/issues/30-colour.md`).
- Translations.
~~~

### 3. Apply / remove labels
Issue: .scratch/issues/10-farewell.md
Add: milestone-1
Remove: none

### 4. Apply / remove labels
Issue: .scratch/issues/11-bye-code.md
Add: milestone-1
Remove: none

### 5. Apply / remove labels
Issue: .scratch/issues/12-bye-usage.md
Add: milestone-1
Remove: none

### 6. Make an issue a sub-issue of a parent
Issue: .scratch/issues/10-farewell.md
Parent: .scratch/issues/31-milestone-1.md

### 7. Apply / remove labels
Issue: .scratch/issues/20-quiet.md
Add: milestone-1
Remove: none

### 8. Make an issue a sub-issue of a parent
Issue: .scratch/issues/20-quiet.md
Parent: .scratch/issues/31-milestone-1.md
