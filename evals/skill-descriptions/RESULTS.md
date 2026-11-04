# Results

One entry per run of the skill-descriptions cases, newest first. Record the commit, the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`, the model tier, the run level ([README](README.md#run-level-and-tier)), whether the descriptions came from the branch or from main, and the description word counts (`build_listing.py --counts`). An entry written inside an open pull request names the commit it ran on as its base.

## Template

```
### <date>, commit <sha>, dev-skills <version>, <branch's | main's> descriptions

Run level: decision-level, fresh subagent per batch, listing only
Tier: regular
Setup: <batch size and count, where the skills came from (checkout or git archive of main), words total and longest>
Score: <score.py's overall line and its misses>
Compare (new runs only): <compare.py's output against the entry named as baseline>
Pass: yes | no. Lessons: <descriptions to change, cases that were noise>
```

## Runs

Superseded: an earlier baseline (b7f9873, 143/143) and new run (86a3ab9, 143/143) are invalid. The batch files headed each situation with its case id, which names the expected skill, so the model was told the answer. The runs below use opaque labels (`S1`, `S2`, ...) from `make_batches.py` at 377bf79 and replace them.

### 2026-11-04, commit 377bf79 (branch claude/project-thread-pp8ua5), dev-skills 0.67.0 (no bump yet), branch's descriptions: new run

Run level: decision-level, fresh subagent per batch, listing only.
Tier: regular.
Setup: the same 143 cases and the same 21 batches (seed 621, opaque labels) as the baseline below, built from the branch's skills at 377bf79 (descriptions total 1198 words, longest 60); 21 fresh subagents, each reading its own batch file instead of being pasted its text (limitation: the subagent held a read tool and the run folder's `batches.json` maps labels to case ids, which name the expected skill; the instruction named a single file).
Score: 143/143 = 100.0%; every skill full; no misses.
Confusion pairs: none.
Compare against the baseline below (`compare.py base new`), output verbatim:

```
baseline: 142/143   new: 143/143
PASS
```

Pass: yes. Lessons: the 34% cut in description words (1810 -> 1198) lost no pick on these cases. The baseline is still nearly saturated (142/143), so the guard is no regression, not an improvement.

### 2026-11-04, commit b7f9873 (main), dev-skills 0.67.0, main's descriptions: baseline

Run level: decision-level, fresh subagent per batch, listing only.
Tier: regular.
Setup: 143 cases in 21 batches of 7 (`make_batches.py` at 377bf79 on a `git archive` of main, seed 621, opaque labels), 21 fresh subagents started in one parallel batch, each reading its own batch file instead of being pasted its text (same limitation as the new run: a read tool and `batches.json` in the folder; the instruction named a single file). Descriptions total 1810 words, longest 163 (milestone). The cases passed the Case check before the run.
Score: 142/143 = 99.3%; one miss.
Confusion pairs: agentic-review -> review-rounds (case agentic-review-t3, "run a ticket check"), likely because both descriptions mention a Ticket check; the model's reasoning was not captured, and a single flip may be noise.
Pass: baseline.
