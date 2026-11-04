### 1. Create a label
Issue: none
Label: milestone-1

### 2. Create an issue
Issue: new (31-milestone-1-quiet-flag.md)
Title: Milestone 1: Quiet flag
Labels: milestone-1
Parent: none
Body:
~~~
## Goal

Scripts can run the greeter silently.

## Features, in build order

One at a time, in this order. Each feature is its own issue carrying `milestone-1`.

| # | Feature | Kind | Accepted when |
| --- | --- | --- | --- |
| 1 | `.scratch/issues/20-quiet.md` Add a --quiet flag | lone Ticket | `greet.sh --quiet hello Ada` prints nothing and exits 0; `greet.sh --quiet nope` prints nothing and exits 2 |

## Acceptance

- Every feature above is merged and its issue closed.

## Excluded

- None.
~~~

### 3. Apply / remove labels
Issue: .scratch/issues/20-quiet.md
Add: milestone-1
Remove: none

### 4. Make an issue a sub-issue of a parent
Issue: .scratch/issues/20-quiet.md
Parent: .scratch/issues/31-milestone-1-quiet-flag.md
