# Expected results

What a Review of the fixture (branch `planted` against `main`, spec `SPEC.md`) should report. Line numbers are in the `planted` tree (`after/` plus the untouched `base/` files). `REVIEW.md` is in `base/`, so it is on `main` before the change, as in a real repo.

## Planted Findings

| id | Bug class | Severity | Locations | What is wrong |
|----|-----------|----------|-----------|---------------|
| P1 | spare cents to the wrong people (spec mismatch) | Important | `splitter/split.py:11` | `i >= len(people) - spare` gives the spare cents to the **last** people; the spec (and `docs/splitting.md`) say the first. `split_evenly(1000, ["Ana", "Ben", "Caro"])` gives Caro 334. The tests only check the sum, so they pass. |
| P2 | unescaped user input in HTML | Important | `splitter/report.py:11` (`expense.payer`), `splitter/report.py:16` (`creditor`) | Names typed by trip members go into the shared page unescaped, while their neighbours (`description`, `debtor`, `title`) are escaped. Both locations must be listed in one Finding. |
| P3 | off-by-one skips the last creditor | Important | `splitter/split.py:27` | `range(len(creditors) - 1)` never pays the last creditor. With one creditor, the common case, `settle` returns no transfers at all; the spec asks for any number of creditors. |
| P4 | float money parsing truncates cents | Pre-existing | `splitter/money.py:6` | `int(float(text) * 100)` turns `"0.29"` into 28 and `"19.99"` into 1998. It is in `main` and already used by `load_expenses` on every amount, so the pull request did not cause it, though `splitter/cli.py:9` now also calls it. The spec puts parsing out of scope. Expected to be reported as Pre-existing (and, after a pull request's last Round, filed as one `needs-triage` issue). |
| P5 | docs index drift | Nit (fix expected; skip acceptable) | `docs/dev-skills/index.md:6` (links `../currency.md`, that is `docs/currency.md`, renamed to `money.md` by this change), `docs/splitting.md` (new doc, no index line) | Both instances in one Finding (citing `docs/money.md` for the rename instead of the index line is fine). Reported by the standards Finder's drift check. Important is also acceptable if the Verifier cites the spec line "Every doc gets a line in `docs/dev-skills/index.md`". |
| P6 | public function without a docstring (the fixture `REVIEW.md` Always check line for `splitter/*.py`) | Nit (fix) | `splitter/cli.py:7` (`main`) | `REVIEW.md` says every public function in `splitter/` has a docstring. `main` has a comment where its docstring should be, so it breaks the line once; every other public function has one. Reported by the standards Finder's Always check step (Bug class "public function without a docstring"). A docstring is not behaviour, data or the spec, so the default meaning of Important (which the fixture `REVIEW.md` keeps) makes it a Nit; "fix" because the line is a standing rule. |

## False alarms (should be dropped by Verify)

| id | Looks like | Why it is correct |
|----|-----------|-------------------|
| F1 | `format_cents(...)` interpolated unescaped into HTML (`splitter/report.py:12`, `:16`), an extra instance of P2 | `format_cents` builds its string from an `int` with digits, a `-` and a `.`; nothing a user typed reaches it. If a Finder adds these locations to P2, Verify should remove them. |
| F2 | removing from `pending` while iterating it (`splitter/split.py:29`, `:36`) | The loop iterates `list(pending)`, a copy, and removes from the original. The inner `[person, owed]` lists are shared, so `item[1] -= pay` updates the original too. |

In a full run F1 counts as reported when a kept Finding lists `splitter/report.py:12`, or lists `:16` for `format_cents` and not for `creditor`; P2's own `:16` (for `creditor`) is not F1. F2 counts as reported when a kept Finding says `settle` skips a debtor, or loses a payment, because it removes from `pending` while iterating it.

## Known extras

Real bugs in the fixture that were not planted. Runs have reported them, at more than one Severity, so a run is scored on the Severity it gives, within the ones accepted here. Both are in `splitter/split.py`, which is new in this change, so neither is Pre-existing.

| id | Bug class | Locations | What is wrong | Severity a run should give |
|----|-----------|-----------|---------------|----------------------------|
| K1 | payer outside the people list | `splitter/split.py:17-19` | `total_paid` counts every payer, so a payer who is not in `people` adds their spend to the total that is split, but `balances` only gives a balance to `people`. The balances no longer sum to zero and that payer is never repaid. | Important: money is lost on a realistic path. Nit, fix or skip, is also accepted. |
| K2 | duplicate names collapse shares | `splitter/split.py:9-11` | With a name twice in `people`, both shares are written to one dict key, so the shares no longer add up to the total, against the spec's "The shares add up to exactly the total". | Important, when the Verifier's reason is that the shares no longer add up to the total, as the spec asks. Nit, fix or skip, is also accepted. |

## Scoring

A run passes when:

- P1, P2, P3 are reported as Important, P4 as Pre-existing, P5 as a Nit (or Important with the reason above), and P6 as a Nit;
- P6 is reported once, as a Nit, with Bug class "public function without a docstring" and a location that includes `splitter/cli.py:7`, and the Review's Always check list shows the line as broken by that Finding (not `clear`);
- P2 and P5 each list both of their locations in one Finding;
- F1 and F2 are not reported (dropped by Verify, or never raised), by the wording under False alarms.

Known extras: a run that reports K1 or K2 at an accepted Severity is not penalised, and neither is a run that does not report them. Record each in its own row. One reported as Pre-existing counts against the run, like a false extra.

Record other Findings in `RESULTS.md` as extras, with whether each is real. A real extra is fine; a false extra counts against the run.

## Verify-only check

The full runs rarely test Verify's drop call: no Finder has raised F1 or F2 yet, so their rows read "never raised". This check hands the Verifier the candidates in `VERIFY-ONLY.md` directly (see the eval README for how to run it). Two are the false alarms, written as persuasive Findings; two are real controls, so a Verifier that drops everything fails too. `VERIFY-ONLY.md` lists them in a shuffled order with no ids; this is the mapping:

| id | Title in `VERIFY-ONLY.md` | Is | Expected keep or drop | Severity | Caused by this change? | Final Locations |
|----|---------------------------|----|-----------------------|----------|------------------------|-----------------|
| V-a | Amounts go into the shared page without escaping | F1 | drop | n/a | n/a | n/a |
| V-b | settle skips the debtor after one who is paid off | F2 | drop | n/a | n/a | n/a |
| V-c | settle never pays the last creditor | P3 | keep | Important | yes | `splitter/split.py:27` |
| V-d | Names typed by trip members reach the summary page unescaped | P2, with F1's `:12` folded in | keep | Important | yes | `splitter/report.py:11`, `splitter/report.py:16` |

Why each is expected:

- **V-a** is dropped because the code does not do what the claim says: `format_cents` builds its string from an `int` with digits, a `-` and a `.`, and every amount reaches it through `parse_amount`, which returns an `int`. A value that is not a number makes `format_cents` raise (`cents < 0` on a string), so no markup reaches the page. Dropping it only as a repeat of V-d does not count: V-d's `:12` is wrong too.
- **V-b** is dropped because the loop iterates `list(pending)`, a copy, so removing from `pending` skips no one, and the shared `[person, owed]` lists keep `item[1] -= pay` in step. On the candidate's input, `settle` gives `[("Ben", "Ana", 1000), ("Caro", "Ana", 1000)]`: Caro is not skipped. Eve is never paid, but that is V-c's off-by-one at `:27`; keeping V-b with its scenario rewritten to that bug fails the row, because the Bug class at `:29` and `:36` is not real.
- **V-c** is kept as Important and caused by this change (`splitter/split.py` is not on `main`).
- **V-d** is kept as Important and caused by this change, with `splitter/report.py:12` removed from its Locations: the amount cell holds only `format_cents` output, as in V-a. `:16` stays, because `creditor` on that line is unescaped.

The check passes when:

- V-a is dropped because `format_cents` output cannot carry markup (it is built from an `int`, and a value that is not a number makes it raise); a drop only as a repeat of V-d does not count;
- V-b is dropped; keeping it with its scenario rewritten to V-c's off-by-one at `:27` does not count as a drop;
- V-c is kept as Important, caused by this change, with `splitter/split.py:27`;
- V-d is kept as Important, caused by this change, with exactly `splitter/report.py:11` and `splitter/report.py:16`;
- every Location the Verifier gives, in any answer, is `file:line` counted within that file (as `grep -n` on the `planted` tree gives it), never a line counted across the diff or a listing of several files (#98).

On Deep, the one Verifier runs on the premium tier; score it the same way.

## Script briefs

What a Round briefed from the script leaves. The run is a fresh regular-tier subagent given `script-briefs/PROMPT.md` (Round 1 at Standard, then the Verifier's brief from three canned Finder messages in `script-briefs/messages/`); it starts no agent. `script-briefs/score.py` builds the briefs the plugin script gives for the same inputs and compares byte for byte with what the run left in `<out-dir>/repo.briefs/round/`.

| id | Check | Pass when |
|----|-------|-----------|
| F1 | files | exactly `finder-standards.md`, `finder-spec.md`, `finder-adversarial.md` and `verifier.md` (the table of `review-rounds` at Standard names three Finders and one Verifier) |
| B1-B3 | Finder briefs | each is identical to the script's file of that name |
| B4 | Verifier brief | identical to the script's, so the three messages are carried over unchanged, each under its Finder, and only the Always check line the standards Finder's Bug class names is in it |
| L1 | work tree | the repository has no new or changed file (the briefs were written outside it) |
| H1 | by hand | the reply names the script command it ran for the Finders and for the Verifier |

B1-B3 compare against the script run with exactly `--base main --head planted`, so a run that passes `--base <sha>` instead of `main` fails them too.

Expected: on the branch's skill every check passes. On main's skill, which has no script, a hand-built set cannot be byte-identical, so B1-B4 fail while F1 and L1 may pass: that shows the change moved the briefs from hand-made to the script's. A run that passes B1-B4 on main's skill means the checks are too loose.
