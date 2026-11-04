# Results

One entry per run of a `to-tickets` repo-labels case, newest first. Rerun when a pull request changes how `to-tickets` or the rule in `triage` applies repo labels, as the [evals guide](../../docs/dev-skills/evals.md) says, and record the commit and the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`.

## Runs

### 2026-11-04, branch `ticket-692` (Ticket #692, Spec #690), commit 8684ca5, dev-skills 0.78.1 (base, main 56def67): cases `split`, `named`, `no-table`

Setup: six runs by the Spec thread, regular tier, decision-level fresh subagents given only each case's `PROMPT.md` (`<checkout>` = a copy of the branch's `plugins/` at 8684ca5, or a `git archive` of main 56def67), scored with `score.py`. The cases had passed the premium case check (verdicts: fix, for the shared prompt line, now applied) before any run.

| Case | Branch's skill | Main's skill |
| --- | --- | --- |
| `split` | PASS | PASS (main judged each ticket's labels from the table too) |
| `named` | PASS | FAIL: 01, 02 and 03 carry only `ready-for-agent`; the Spec-named `backend` was not copied (01, 02, 03 lack `backend`, 02 also lacks `frontend`) |
| `no-table` | PASS | PASS |

`named` is the one case that moved with the change; `split` and `no-table` are regression guards (`no-table` also shows a repo with no Repo labels rows sees no change).

Gap: no case covers `to-spec` applying the repo labels rule to the whole Spec (text-only; named on the pull request's `**Eval:**` line).
