# Rebuttals

One rebuttal per candidate in `VERIFY-ONLY.md`, each as a fixer would send it after a Round kept that candidate as Important. `briefs.sh --rebuttal` pairs each with its Finding by title and numbers them in this file's order. Each cited `file:line` `text` pair holds at the `planted` head (`test-rebuttal.sh` checks it); whether the argument holds is for the rebuttal Verifier.

### Rebuttal of: settle never pays the last creditor

The loop bound is deliberate. `splitter/split.py:24` `sorted(((owed, person)` puts the creditors largest first, and the balances always sum to zero, because `splitter/split.py:19` `paid.get(person, 0) - shares[person]` subtracts shares that add up to exactly the total. So once every creditor but the last has been paid, what is left in `pending` is exactly what the last creditor is owed, and nothing is lost: the last creditor needs no loop pass of its own. The tests agree: `python3 -m unittest` in the repo prints `Ran 6 tests` and `OK`.

### Rebuttal of: Amounts go into the shared page without escaping

The amount cells cannot carry markup. Every amount enters through `splitter/expenses.py:15` `Expense(payer, parse_amount(amount), description)`, and `splitter/money.py:6` `return int(float(text) * 100)` returns an `int`. `splitter/money.py:13` `return f"{sign}{cents // 100}.{cents % 100:02d}"` builds the string from integer arithmetic, so it holds only digits, a `-` and a `.`. A value that is not a number never gets that far: `python3 -c 'from splitter.money import format_cents; format_cents("<b>")'` fails with `TypeError: '<' not supported between instances of 'str' and 'int'` at `splitter/money.py:11` `sign = "-" if cents < 0 else ""`.

### Rebuttal of: Names typed by trip members reach the summary page unescaped

The payer and creditor are not free text. The people on a trip are set up by the organiser, who passes them on the command line (`splitter/cli.py:10` `split_evenly(total, argv[2:])`), and `splitter/split.py:19` `paid.get(person, 0) - shares[person]` only works for people in that list, so a name that is not a trip member's never makes it into `balances` or `settle`. The fields that members type freely, the description and the title, are already escaped (`splitter/report.py:11` `escape(expense.description)`), and so is the debtor. There is nothing left to escape.

### Rebuttal of: settle skips the debtor after one who is paid off

The loop does not walk the list it removes from. `splitter/split.py:29` `for item in list(pending):` iterates a copy, so `splitter/split.py:36` `pending.remove(item)` cannot shift the walk, and the copy shares the same `[person, owed]` lists, so `splitter/split.py:34` `item[1] -= pay` stays in step. On the Finding's own input, `python3 -c 'from splitter.split import settle; print(settle({"Ana": 2000, "Eve": 500, "Ben": -1000, "Caro": -1000, "Dan": -500}))'` prints `[('Ben', 'Ana', 1000), ('Caro', 'Ana', 1000)]`: Caro pays Ana, so no debtor is skipped. Eve is never paid, but that is the separate loop bound at `splitter/split.py:27`, not this Finding.
