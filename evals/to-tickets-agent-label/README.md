# to-tickets runtime-derived agent label check

Does `to-tickets` give a Ticket whose acceptance criteria demonstrably require one agent's native runtime that agent's configured agent-only label, even when the source Spec has none, and leave every other label rule alone? Bounded publication check for issue #512 (absorbs #468). Local files only; no real issue or network call. The fixture names two imaginary agents, `alpha` and `beta`, with labels `alpha-only` and `beta-only`.

## Files

- [`cases.py`](cases.py): the six cases and their expected labels (below), shared by the other scripts.
- [`make_fixture.py`](make_fixture.py): `python3 make_fixture.py <out-dir> <case>` builds a scratch repo (local-files tracker doc, triage-labels doc with or without the agent-only mapping, release and Boundary docs, `.scratch/greeter/SPEC.md` with the approved breakdown, `PROMPT.md`, and for `resume` the two tickets filed earlier).
- [`score.py`](score.py): `python3 score.py <out-dir> <case>` reads the labels back from `.scratch/greeter/issues/*.md` and checks `REPORT.txt`, the run's final reply saved by hand.
- [`test_cases.py`](test_cases.py): the scorer's self-test (a reference run per case passes, twelve planted wrong runs fail) and a check that the inherited case's rendered Spec names only the source's runtime. It reads no skill or doc text. Run `python3 evals/to-tickets-agent-label/test_cases.py`; it prints `ok`.

## Cases

Children of the fixture Spec: 01 ordinary (formatter output), 02 requires beta's native runtime (tests pass inside beta's own runtime, output recorded), 03 ordinary, blocked by 02. Every ticket also carries `ready-for-agent`.

| Case | Source labels | Mapping | Expected readback | Report must |
| --- | --- | --- | --- | --- |
| `unrestricted` | none | alpha, beta | 01 no agent label; 02 `beta-only` | name 02 and `beta-only` with the criterion |
| `inherited` | `alpha-only` | alpha, beta | 01 and 02 both `alpha-only` (02 needs alpha here) | nothing extra |
| `conflict` | `alpha-only` | alpha, beta | 01 `alpha-only`; 02 (needs beta) and 03 (blocked by 02) not published; source label unchanged | name 02, the conflict and `alpha-only`; name 03 as waiting on 02 |
| `no-mapping` | none | none | 01 and 02 no agent label | name 02 as needing beta's runtime and the missing mapping |
| `milestone` | `milestone-1`, `release-m1-r1` | alpha, beta | 01 both membership labels; 02 `beta-only` plus both | name 02 and `beta-only` |
| `resume` | none | alpha, beta | 01 and 02 already filed, 02 unlabelled: 02 gains `beta-only`; no new ticket | name 02 and `beta-only` |

## Run level

Each case: full run in a top-level session or a fresh subagent that loads `to-tickets` from this checkout (`plugins/dev-skills/skills/to-tickets/`), working directory `<out-dir>`, given only `PROMPT.md`. Keep this README, `cases.py` and `score.py` away from it. Save its final reply to `<out-dir>/REPORT.txt`, then `python3 score.py <out-dir> <case>`. The `conflict` run stops at the question; the scorer reads that question from `REPORT.txt`.

The scorer and fixture are deterministic and self-tested (`test_cases.py`).

## Run record

Runner: six fresh regular-tier subagents, each given only the `to-tickets` SKILL.md (checkout at commit 48d4ca6 for the skill text, unchanged in 684e147) and the fixture's `PROMPT.md`, scored with `score.py`. All six PASS. Subagent runs, not a top-level session.

- `unrestricted`: PASS. 01 `ready-for-agent`; 02 `ready-for-agent, beta-only`; the report named 02, `beta-only` and the criterion.
- `inherited`: the first run, on fixture 48d4ca6, found a fixture bug: `SPEC.md` still named beta for 02, so the model correctly held 02 as a conflict and the scorer said "ticket 02 missing". The self-test alone had missed it. Fixed in 684e147; rerun PASS: 01 and 02 both `ready-for-agent, alpha-only`, no conflict.
- `conflict`: PASS. 01 `alpha-only` published; 02 and 03 held, one question asked, source label unchanged.
- `no-mapping`: PASS. Neither labelled; the report named 02 as needing beta's runtime and the missing mapping.
- `milestone`: PASS. 02 `ready-for-agent, beta-only, milestone-1, release-m1-r1`; 01 both membership labels.
- `resume`: PASS. 02 gained `beta-only`, no new ticket.

### Run for #623 (local-files recipe removed from `to-tickets`)

Twelve fresh regular-tier subagents, one per case on the pull request's skill and on main's (`git archive` of cc54278, plugin 0.64.0), each given the skill folder and the fixture's `PROMPT.md`, scored with `score.py`. Subagent runs, not a top-level session. Pull request: all six PASS. Main: five PASS; `conflict` failed on the report wording (it lacked "conflict" for ticket 02), a wording miss, not a label error. The change moved no label result: the fixture's own tracker doc supplies the file shape.
