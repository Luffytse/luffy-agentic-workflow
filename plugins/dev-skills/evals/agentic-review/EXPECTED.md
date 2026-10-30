# Expected results

What a Review of the fixture (branch `planted` against `main`, spec `SPEC.md`) should report. Line numbers are in the `planted` tree (`after/` plus the untouched `base/` files). `REVIEW.md` is in `base/`, so it is on `main` before the change, as in a real repo.

## Planted Findings

| id | Bug class | Severity | Locations | What is wrong |
|----|-----------|----------|-----------|---------------|
| P1 | spare cents to the wrong people (spec mismatch) | Important | `splitter/split.py:11` | `i >= len(people) - spare` gives the spare cents to the **last** people; the spec (and `docs/splitting.md`) say the first. `split_evenly(1000, ["Ana", "Ben", "Caro"])` gives Caro 334. The tests only check the sum, so they pass. |
| P2 | unescaped user input in HTML | Important | `splitter/report.py:11` (`expense.payer`), `splitter/report.py:16` (`creditor`) | Names typed by trip members go into the shared page unescaped, while their neighbours (`description`, `debtor`, `title`) are escaped. Both locations must be listed in one Finding. |
| P3 | off-by-one skips the last creditor | Important | `splitter/split.py:27` | `range(len(creditors) - 1)` never pays the last creditor. With one creditor, the common case, `settle` returns no transfers at all; the spec asks for any number of creditors. |
| P4 | float money parsing truncates cents | Pre-existing | `splitter/money.py:6` | `int(float(text) * 100)` turns `"0.29"` into 28 and `"19.99"` into 1998. It is in `main` and already used by `load_expenses` on every amount, so the pull request did not cause it, though `splitter/cli.py:9` now also calls it. The spec puts parsing out of scope. Expected to be reported as Pre-existing (and, after a pull request's last Round, filed as one `needs-triage` issue). |
| P5 | docs index drift | Nit (fix expected; skip acceptable) | `docs/index.md:6` (links `currency.md`, renamed to `money.md` by this change), `docs/splitting.md` (new doc, no index line) | Both instances in one Finding (citing `docs/money.md` for the rename instead of the index line is fine). Reported by the standards Finder's drift check. Important is also acceptable if the Verifier cites the spec line "Every doc gets a line in `docs/index.md`". |
| P6 | public function without a docstring (the fixture `REVIEW.md` Always check line) | Nit (fix) | `splitter/cli.py:7` (`main`) | `REVIEW.md` says every public function in `splitter/` has a docstring. `main` has a comment where its docstring should be, so it breaks the line once; every other public function has one. Reported by the standards Finder's Always check step (Bug class "public function without a docstring"). A docstring is not behaviour, data or the spec, so the default meaning of Important (which the fixture `REVIEW.md` keeps) makes it a Nit; "fix" because the line is a standing rule. |

## False alarms (should be dropped by Verify)

| id | Looks like | Why it is correct |
|----|-----------|-------------------|
| F1 | `format_cents(...)` interpolated unescaped into HTML (`splitter/report.py:12`, `:16`), an extra instance of P2 | `format_cents` builds its string from an `int` with digits, a `-` and a `.`; nothing a user typed reaches it. If a Finder adds these locations to P2, Verify should remove them. |
| F2 | removing from `pending` while iterating it (`splitter/split.py:29`, `:36`) | The loop iterates `list(pending)`, a copy, and removes from the original. The inner `[person, owed]` lists are shared, so `item[1] -= pay` updates the original too. |

## Scoring

A run passes when:

- P1, P2, P3 are reported as Important, P4 as Pre-existing, P5 as a Nit (or Important with the reason above), and P6 as a Nit;
- P6 is reported once, as a Nit, with Bug class "public function without a docstring" and `splitter/cli.py:7` as its location, and the Review's Always check list shows the line as broken by that Finding (not `clear`);
- P2 and P5 each list both of their locations in one Finding;
- F1 and F2 are not reported (dropped by Verify, or never raised).

Record other Findings in `RESULTS.md` as extras, with whether each is real. A real extra is fine; a false extra counts against the run.
