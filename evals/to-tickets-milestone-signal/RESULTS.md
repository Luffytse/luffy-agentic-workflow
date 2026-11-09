# Results

One entry per run of a `to-tickets` Milestone-signal case, newest first. Rerun when a pull request changes how `to-tickets` treats a Spec as in a Milestone or handles a ticket with an unfiled blocker, as the [evals guide](../../docs/dev-skills/evals.md) says, and record the commit and the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`.

## Runs

### 2026-11-09, branch `claude/to-tickets-fixes-56` (Ticket #56), commit d2d248f, dev-skills 1.3.0 (base, main 2229fd3): cases `planning`, `labelled-unfiled`, `plain`

Setup: regular tier, decision-level fresh subagents given only each case's `PROMPT.md` plus the skill (from the branch's `plugins/`, or a `git archive` of main 2229fd3), scored with `score.py`. The cases passed a case check by a fresh premium reviewer before the first runs: `planning` fixed (applied: a body check for the named blocker, and the third case `labelled-unfiled`, added from that check), `plain` kept, and fixture fixes applied (the Boundary record sentence cut, approval wording instead of "?"). Round 1 review of the pull request then removed the early Milestone label creation from `to-tickets` and changed `planning` to expect 01 `ready-for-agent` and 02 with no label; the runs below are the reruns at d2d248f. The earlier runs at 09cf7f5 are superseded for `planning` and kept here as history only.

| Case | Branch's skill | Main's skill |
| --- | --- | --- |
| `planning` | PASS (01 `ready-for-agent`, 02 no label, report names 02 and Hub login) | FAIL: 02 labelled `ready-for-agent` although its blocker is unfiled |
| `labelled-unfiled` | PASS (rerun at d2d248f) | FAIL, from the first runs: main published 01 with `ready-for-agent` and `milestone-2` but held 02 as a dependent with a dangling blocker, so ticket 02 is missing (main's skill is unchanged since) |
| `plain` | PASS | PASS (regression guard; from the first runs at 09cf7f5, the plain-path text was not touched by the Round 1 fix) |

### Existing to-tickets cases (regression check, baseline already passing)

Branch's skill at d2d248f unless noted.

| Eval | Case | Result |
| --- | --- | --- |
| agent-label | `unrestricted`, `inherited`, `milestone`, `no-mapping`, `resume` | PASS (rerun at d2d248f) |
| agent-label | `conflict` | scorer FAIL on the branch and on main: both reports said "different agent's label" / "alpha-only vs beta-only" and asked the right question, and the scorer wants the word "conflict". The wording miss is pre-existing and unchanged by this change. |
| shared-docs | `shared`, `separate`, `hidden`, `resume` | PASS at the first branch commit 09cf7f5; not rerun, because the Round 1 fix only removed the caller-named Milestone label clause |
| repo-labels | `split`, `named`, `no-table` | PASS at 09cf7f5; not rerun, for the same reason |
