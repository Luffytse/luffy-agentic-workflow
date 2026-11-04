### 1. Edit an issue body
Issue: .scratch/issues/30-colour.md
Body:
~~~
## What to build

`greet.sh hello <name>` prints the name in green when standard output is a terminal, and plain when it is not (a pipe or a file). `--no-color` turns the colour off. The usage line names the new flag.

**Model tier:** regular.

**Blocked by:** `.scratch/issues/12-bye-usage.md` (it sets the usage line that names `bye`, which this Ticket changes again).

## Acceptance criteria

- [ ] `greet.sh hello Ada` with standard output on a terminal prints `Ada` in green.
- [ ] `greet.sh hello Ada` with standard output not a terminal prints `Hello, Ada!` with no colour codes.
- [ ] `greet.sh --no-color hello Ada` prints `Hello, Ada!` with no colour codes, on a terminal too.
- [ ] `greet.sh` with no command prints exactly `usage: greet.sh [--no-color] hello|bye <name>` to standard error and exits 2.
- [ ] `bash test.sh` covers the terminal case and `--no-color` (and checks the new usage line in place of the old one).

## Notes

Planned with the user on 2026-11-02 as one lone Ticket, the third feature of Milestone 1 (`.scratch/issues/00-milestone.md`). Before that it read: "Someone asked for coloured greetings. Not looked at yet."
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
| 3 | `30-colour.md` Colour output (added 2026-11-02 by the user) | lone Ticket | the name in `hello` is green only when standard output is a terminal; `--no-color` turns it off; the usage line is exactly `usage: greet.sh [--no-color] hello\|bye <name>`; a test covers the terminal case and `--no-color` |


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
