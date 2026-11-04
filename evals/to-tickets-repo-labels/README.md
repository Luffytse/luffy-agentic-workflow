# to-tickets repo labels check

Does `to-tickets` apply the repo labels the repo's triage-labels doc records (its Repo labels table) by `triage`'s rule, judging each Ticket on its own work, and put a label the user named for the Spec on every Ticket? Bounded publication check for Ticket #692 of Spec #690. Local files only; no real issue or network call. The fixture's table records `frontend` (work under `ui/`) and `backend` (work under `api/`).

## Files

- [`cases.py`](cases.py): the three cases and their expected labels (below), shared by the other scripts.
- [`make_fixture.py`](make_fixture.py): `python3 make_fixture.py <out-dir> <case>` builds a scratch repo (local-files tracker doc, triage-labels doc with or without the table rows, release and Boundary docs, `.scratch/orders/SPEC.md` with the approved breakdown, `PROMPT.md`).
- [`score.py`](score.py): `python3 score.py <out-dir> <case>` reads the labels back from `.scratch/orders/issues/*.md` and checks the Spec's labels did not change. It reads outcomes only, never what the run said.
- [`test_cases.py`](test_cases.py): the scorer's self-test (a reference run per case passes, planted wrong runs fail) and checks that the rendered files say what each case means (the Repo labels rows are present or absent, the Spec's label line and the prompt match the case, the Spec names the UI file and the API file its tickets work in, nothing in the breakdown names a label). It reads no skill or doc text. Run `python3 evals/to-tickets-repo-labels/test_cases.py`; it prints `ok`.

Gap: the `to-spec` whole-Spec rule has no eval case (a conversation-driven synthesis with no seam to score); it is reviewed as text, and the PR's `**Eval:**` line names it.

## Cases

The fixture Spec "order totals" is end to end. Its tickets: 01 an API change (`api/orders.py`), 02 a UI change (`ui/cart.html`), blocked by 01, 03 a changelog line, blocked by 01 and 02. Every ticket also carries `ready-for-agent`.

| Case | Repo labels table | Spec's labels | Expected readback |
| --- | --- | --- | --- |
| `split` | `frontend`, `backend` | none | 01 `backend`; 02 `frontend`; 03 neither |
| `named` | `frontend`, `backend` | `backend`, named by the user (the prompt says so) | 01 `backend`; 02 `backend` and `frontend`; 03 `backend`; the Spec keeps `backend` |
| `no-table` | no rows | none | 01, 02, 03 no repo label |

## Run level

Each case: full run in a top-level session or a fresh regular-tier subagent, working directory `<out-dir>`, given only the text of `PROMPT.md` with `<checkout>` replaced by the checkout under test (a copy of its `plugins/` parent without `evals/`); the prompt tells it to load `to-tickets` from `<checkout>/plugins/dev-skills/skills/to-tickets/SKILL.md` and the skills it names, `triage` among them, from `<checkout>/plugins/dev-skills/skills/<name>/SKILL.md`. Keep this README, `cases.py` and `score.py` away from it. Then `python3 evals/to-tickets-repo-labels/score.py <out-dir> <case>`. Run each case on the branch's skill and on main's (`git archive <main sha> plugins | tar -x -C <dir>`) and record both in [RESULTS.md](RESULTS.md). The scorer and fixture are deterministic and self-tested.

Which cases discriminate: `named` (main does not copy a Spec label the user named) is the one that moved between the branch and main; `split` and `no-table` are regression guards (main judged per-ticket labels from the table too).

## Run record

See [RESULTS.md](RESULTS.md).
