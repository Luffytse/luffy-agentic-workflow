# Results

One entry per run of a `to-tickets` Milestone-signal case, newest first. Rerun when a pull request changes how `to-tickets` treats a Spec as in a Milestone or handles a ticket with an unfiled blocker, as the [evals guide](../../docs/dev-skills/evals.md) says, and record the commit and the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`.

## Runs

### 2026-11-09, branch `claude/to-tickets-fixes-56` (Ticket #56), commit 09cf7f5, dev-skills 1.3.0 (base, main 2229fd3): cases `planning`, `labelled-unfiled`, `plain`

Setup: regular tier, decision-level fresh subagents given only each case's `PROMPT.md` plus the skill (from the branch's `plugins/`, or a `git archive` of main 2229fd3), scored with `score.py`. The cases passed a case check by a fresh premium reviewer before these runs: `planning` fixed (applied: a body check for the named blocker, and the third case `labelled-unfiled`, added from that check), `plain` kept, and fixture fixes applied (the Boundary record sentence cut, approval wording instead of "?").

| Case | Branch's skill | Main's skill |
| --- | --- | --- |
| `planning` | PASS | FAIL: main published 01 only, with `ready-for-agent` and no `milestone-2`, and held 02 for its unfiled blocker; no 02 file |
| `labelled-unfiled` | PASS (02 published with `milestone-2` only) | FAIL: main published 01 with `ready-for-agent` and `milestone-2` but held 02 as a dependent with a dangling blocker, so ticket 02 is missing |
| `plain` | PASS | PASS (regression guard) |

### Existing to-tickets cases, branch only (regression check, baseline already passing)

Same setup and commit, branch's skill only.

| Eval | Case | Result |
| --- | --- | --- |
| agent-label | `unrestricted` | PASS |
| agent-label | `inherited` | PASS |
| agent-label | `milestone` | PASS |
| agent-label | `no-mapping` | PASS |
| agent-label | `resume` | PASS |
| agent-label | `conflict` | scorer FAIL: "report lacks 'conflict' for ticket 02". The behaviour was right (01 published with `ready-for-agent` and `alpha-only`; 02 and 03 held; one question about `beta-only` against `alpha-only`); the report said "different agent's label" instead of the word conflict. A wording miss in an unchanged path, recorded as is. |
| shared-docs | `shared`, `separate`, `hidden`, `resume` | PASS |
| repo-labels | `split`, `named`, `no-table` | PASS |
