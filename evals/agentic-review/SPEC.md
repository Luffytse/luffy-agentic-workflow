# Ticket #1: Even splitting, settle-up and the summary page

Stands in for the ticket the fixture's pull request builds. Pass this file to `agentic-review` as the spec.

Trip members type in who paid what. We want to split the total evenly and tell everyone who pays whom.

## What to build

- `split.split_evenly(total_cents, people)` returns each person's share in cents. The shares add up to exactly the total. When the total does not divide evenly, the spare cents go one each to the **first** people in the list. No people raises `ValueError`.
- `split.balances(expenses, people)` returns what each person is owed (positive) or owes (negative).
- `split.settle(balances)` returns transfers `(debtor, creditor, cents)` that bring every balance to zero, for any number of debtors and creditors.
- `report.render_summary_html(title, expenses, transfers)` renders the summary page. The page is shared with the whole group as a link, and every name and description in it was typed by a trip member.
- A command, `python3 -m splitter.cli TOTAL NAME...`, that prints each person's share.
- A short doc, `docs/splitting.md`, explaining the split rule. Every doc gets a line in `docs/index.md`.

## Out of scope

- Changing how amounts are parsed or stored.
- Uneven splits and currencies.
