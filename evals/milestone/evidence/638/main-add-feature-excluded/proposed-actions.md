### 1. Edit an issue body
Issue: 30-colour.md
Body:
~~~
Someone asked for coloured greetings. Planned with the user on 2026-11-02 as one lone Ticket of Milestone 1 (`00-milestone.md`).

## What to build

`greet.sh hello <name>` prints the name in green only when standard output is a terminal; when it is not a terminal, the output has no colour codes. `--no-color` turns the colour off. The usage line becomes exactly `usage: greet.sh [--no-color] hello|bye <name>`.

Scope edges: the usage line names `bye`, which the farewell Ticket `12-bye-usage.md` adds, and it replaces the exact usage line that Ticket's check in `test.sh` expects; this Ticket updates that check to the new line and changes nothing else of the farewell command.

## Acceptance criteria

- [ ] A test in `bash test.sh` covers the terminal case: with standard output a terminal, `greet.sh hello Ada` prints the name in green.
- [ ] A test in `bash test.sh` covers `--no-color`: the name is printed with no colour.
- [ ] `greet.sh` with no command prints exactly `usage: greet.sh [--no-color] hello|bye <name>`.
~~~

### 2. Edit an issue body
Issue: 00-milestone.md
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


## Acceptance

- Every feature above is merged and its issue closed.
- The user runs `greet.sh --quiet bye Ada` at the Milestone review and sees nothing, exit 0.

## Excluded

- Translations.
~~~
Note: the only change is that "Colour output (`30-colour.md`)" leaves Excluded, as the user agreed on 2026-11-02 ("Yes, take it out of Excluded."). Read back after writing.

### 3. Edit an issue body
Issue: 00-milestone.md
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
| 3 | `30-colour.md` Colour output (added 2026-11-02 by the user) | lone Ticket | the name in `hello` is green only when standard output is a terminal; `--no-color` turns it off; usage line exactly `usage: greet.sh [--no-color] hello\|bye <name>`; a test covers the terminal case and `--no-color` |


## Acceptance

- Every feature above is merged and its issue closed.
- The user runs `greet.sh --quiet bye Ada` at the Milestone review and sees nothing, exit 0.

## Excluded

- Translations.
~~~
Note: the only change from block 2 is row 3, placed third (after the quiet flag) as the user said. Read back after writing.

### 4. Apply / remove labels
Issue: 30-colour.md
Add: milestone-1
Remove: none

### 5. Make an issue a sub-issue of a parent
Issue: 30-colour.md
Parent: .scratch/issues/00-milestone.md
