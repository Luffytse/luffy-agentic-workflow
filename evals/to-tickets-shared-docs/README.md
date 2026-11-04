# to-tickets shared doc lines check

Does `to-tickets` keep Tickets that can build in parallel from editing the same doc lines that describe a rule: one Ticket carries both edits, or the later Ticket is blocked by the earlier one, and Tickets that edit different lines stay unblocked? Bounded publication check for issue #656. Local files only; no real issue or network call.

## Files

- [`cases.py`](cases.py): the four cases and their expected shape (below), shared by the other scripts.
- [`make_fixture.py`](make_fixture.py): `python3 make_fixture.py <out-dir> <case>` builds a scratch repo (local-files tracker doc, label, release and Boundary docs, a small glossary, `.scratch/greeter/SPEC.md` with two work items, `PROMPT.md`, and for `resume` the first Ticket filed earlier).
- [`score.py`](score.py): `python3 score.py <out-dir> <case>` reads `.scratch/greeter/issues/*.md` back: how many Tickets, and which `**Blocked by:**` line names which. It reads no report.
- [`test_cases.py`](test_cases.py): the scorer's self-test (reference runs pass, planted wrong runs fail) and the fixture self-test: each case's rendered `SPEC.md` names a glossary entry for each work item (the same one for `shared` and `resume`, two different ones for `separate`, and for `hidden` items 01 and 03 share one that 02 does not), names a different code file and function per item, states item 02's code dependency in `hidden` only and writes no blocking edge itself, and the filed-Ticket folder and prompt match the case. It reads no skill or doc text. Run `python3 -I evals/to-tickets-shared-docs/test_cases.py`; it prints `ok`.

## Cases

Work items of the fixture Spec (each names its own code file and function and the glossary entry its docs update rewrites): "Add a shout option" (`greet.py`, `format_greeting`, entry `Greeting`), "Record greetings in a history" (`history.py`, `record_greeting`, entry `Greeting`, or `History` in `separate`), and for `hidden` "Log shouted greetings" (`loudlog.py`, `record_shout`, entry `Loud log`, calls the shout option). The Spec states no blocking edge for the shared entry.

| Case | Items and glossary entries rewritten | Expected readback |
| --- | --- | --- |
| `shared` | 01 shout and 02 history, both `Greeting` | one Ticket carrying both, or two Tickets with exactly one blocked by the other |
| `separate` (control) | 01 shout `Greeting`, 02 history `History` | two Tickets, neither blocked |
| `hidden` | 01 shout `Greeting`; 02 log shouted greetings `Loud log`, needs 01 in code; 03 history `Greeting` | 02 in 01's Ticket or blocked by it; 01 and 03 in one Ticket or joined by a blocker path (direct or through 02); no cycle |
| `resume` | 01 shout filed and unblocked; 02 history, both `Greeting` | 01 and 02 only; 02 carries the history item and is blocked by 01; 01 gains no blocker |

## Run level

Each case: a fresh regular-tier session (the recorded runs were `claude -p` sessions with file tools only, run from `<out-dir>`; a fresh subagent does equally) that loads `to-tickets` from this checkout (`plugins/dev-skills/skills/to-tickets/`), working directory `<out-dir>`, given only the skill folder and `PROMPT.md`. Keep this README, `cases.py` and `score.py` away from it. Then `python3 score.py <out-dir> <case>`.

The scorer and fixture are deterministic and self-tested (`test_cases.py`).

## Run record

### Run for #656 (shared-doc-lines rule added to step 3 of `to-tickets`)

Eight fresh regular-tier runs, two per case (`shared`, `resume`) on the pull request's skill (the rule commit on base 3a0eef9, plugin 0.76.0) and two on main's (`git archive` of 3a0eef9, plugin 0.76.0), each given the skill folder and the fixture's `PROMPT.md`, scored with `score.py`. The runs were `claude -p` sessions on the regular tier with file tools only, not Agent-tool subagents; they are decision-level runs, not a top-level session. The fixture's two items touch different code (`greet.py` `format_greeting` and `history.py` `record_greeting`) and share only the glossary entry `Greeting`, so the doc lines are the only reason to order them.

- Pull request: `shared` PASS twice, `resume` PASS twice.
- Main: `shared` PASS twice, `resume` PASS twice.

Main's skill already passes both cases: its reports name the shared glossary entry as the reason for the blocking edge, so main's step 3 plus the model's own care about conflicts already produce the expected result here. The case does not show the rule changing the outcome. It stays as a regression guard for the rule, with the `separate` control guarding against over-blocking (`separate` was not rerun on the changed fixture; its scorer and fixture are self-tested). An earlier version of the fixture, whose items shared one function, also passed on main (3 cases, one run each).

### Run for #656, case-check follow-up (`hidden` added, `separate` run, scorer checks 02's content)

Five more fresh regular-tier `claude -p` runs (file tools only, same method and base as above), one parallel batch: `hidden` twice on the pull request's skill and twice on main's, and `separate` once on the pull request's skill.

- Pull request: `hidden` PASS twice (02 and 03 each blocked by 01); `separate` PASS (no edges).
- Main: `hidden` PASS twice, with the same edges.

`hidden` was written to make main find a pair it did not expect (01 and 03 share a glossary entry but no code, while 01 and 02 are tied in code), and main still got it right in both runs. So no case here separates the pull request's skill from main's: all four cases are a regression guard for the rule and a check against over-blocking, not a demonstrated gain. The rule is the only text that names doc lines, but a regular-tier model reading main's step 3 already orders items that rewrite one entry. `separate` was run on the branch only, and not on main.

### Run for #692 (repo-label rule added to `to-tickets` step 3)

Four fresh regular-tier subagents (Agent tool, file tools only), one per case (`shared`, `separate`, `hidden`, `resume`), each given the `to-tickets` and `triage` skills from the branch (head b2b7cbf, plugin 0.79.0) and the fixture's `PROMPT.md`, scored with `score.py`. Subagent runs, not a top-level session.

- `shared`: PASS (02 blocked by 01).
- `separate`: PASS (no edges).
- `resume`: PASS (02 filed blocked by 01, no other new ticket).
- `hidden`: the scorer reported "no Ticket carries work item 01/02/03", because the subagent wrote the acceptance criteria in its own words and no checkbox line carried the key names (`format_greeting`, `record_shout`, `record_greeting`). Read by hand, the set is correct: three tickets, 02 (log shouted greetings) blocked by 01 and 03 (record in history) blocked by 01. Recorded as a scorer key-wording miss, not a skill result; the scorer was left unchanged in this change.

The change does not touch the shared-doc-lines rule, so these are regression guards.
