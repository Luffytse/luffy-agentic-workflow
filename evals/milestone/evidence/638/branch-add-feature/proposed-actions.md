### 1. Edit an issue body
Issue: .scratch/issues/30-colour.md
Body:
~~~
## What to build

`greet.sh hello <name>` colours the name green when standard output is a terminal, and prints it plain otherwise (a pipe, a file). A `--no-color` flag before the command turns the colour off. The usage line becomes exactly `usage: greet.sh [--no-color] hello|bye <name>`.

Planned with the user on 2026-11-02 as one lone Ticket, from the request "Someone asked for coloured greetings."

**Model tier:** regular

## Acceptance criteria

- [ ] `greet.sh hello Ada` with standard output on a terminal prints `Hello, Ada!` with `Ada` in green.
- [ ] `greet.sh hello Ada` with standard output not a terminal prints plain `Hello, Ada!`, with no colour codes.
- [ ] `greet.sh --no-color hello Ada` prints plain `Hello, Ada!` even on a terminal.
- [ ] `greet.sh` with no command prints exactly `usage: greet.sh [--no-color] hello|bye <name>` to standard error and exits 2.
- [ ] `bash test.sh` covers the terminal case and `--no-color`.
~~~

### 2. Apply / remove labels
Issue: .scratch/issues/30-colour.md
Add: enhancement
Remove: needs-triage

### 3. Edit an issue body
Issue: .scratch/issues/00-milestone.md
Body:
~~~
## Goal

By the end, the greeter can say goodbye and can run silently in scripts, so it can ship as 1.0.

## Features, in build order

In this order, up to 2 at once. Each feature is its own issue carrying `milestone-1`.

| # | Feature | Kind | Accepted when |
| --- | --- | --- | --- |
| 1 | `10-farewell.md` Add a farewell command | Spec | `greet.sh bye Ada` prints `Goodbye, Ada!`; no name greets the world; tests cover both |
| 2 | `20-quiet.md` Add a --quiet flag | lone Ticket | `--quiet` prints nothing and keeps the exit code |
| 3 | `30-colour.md` Colour output (added 2026-11-02 by the user) | lone Ticket | the name in `hello` is green only when standard output is a terminal; `--no-color` turns it off; usage line is exactly `usage: greet.sh [--no-color] hello\|bye <name>`; a test covers the terminal case and `--no-color` |


## Acceptance

- Every feature above is merged and its issue closed.
- The user runs `greet.sh --quiet bye Ada` at the Milestone review and sees nothing, exit 0.

## Excluded

- Translations.
~~~

### 4. Apply / remove labels
Issue: .scratch/issues/30-colour.md
Add: milestone-1
Remove: none

### 5. Make an issue a sub-issue of a parent
Issue: .scratch/issues/30-colour.md
Parent: .scratch/issues/00-milestone.md

### 6. Edit an issue body
Issue: .scratch/issues/12-bye-usage.md
Body:
~~~
The usage line names `bye`. Model tier: cheap.

## Acceptance criteria

- [ ] `greet.sh` with no command prints exactly `usage: greet.sh [--no-color] hello|bye <name>` to standard error and exits 2.
- [ ] `bash test.sh` checks that exact line.

_Updated for `30-colour.md` (added to the Milestone 2026-11-02): the exact usage line now names `[--no-color]`, the end state once both have landed._
~~~
