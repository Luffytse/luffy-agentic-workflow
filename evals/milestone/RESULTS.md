# Results

One entry per run of the `milestone` skill's dry run (the planning cases and the report cases; the delivery entries below are history, see the first entry), newest first ([README](README.md) says how to build, run and score it). Record the commit and the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`; an entry written inside an open pull request names the commit and version it ran on as its base. Each planning run also applies the shape to one real Milestone issue (`score.py --shape`) and names the migration it needs, if any; each `deliver` run also applies the loop, read-only, to one real Milestone and names the thread it would start next and the next Release it would plan.

## 2026-11-09 — Ticket #78: closing the accepted Milestone issue, `accepted` report case

Runner: the Ticket thread. Case check by a fresh premium-tier subagent: verdict fix (a release-cut confound, a stub prior report, a clock behind the message, a scorer too narrow on where and too loose on other actions, and a missing README entry and self-test); all fixed. One redesign of the fixture removed the prompt's `close` operation hint. Runs: one fresh premium-tier subagent each, `<checkout>` a `git archive` of the branch or of main (`065d1d7`, plugin 1.9.0, unbumped). Run level: decision-level in a subagent. Evidence: [`evidence/78/`](evidence/78/).

| Case | Branch | Main |
| --- | --- | --- |
| `accepted` (final fixture) | 3/3 (`branch`: comment and close, wording "close the Milestone issue yourself") | 3/3 (`main`: comment and close) |

Earlier branch run, same fixture, first wording ("close the Milestone issue only once the user accepts it"): did not close (`branch-earlier-wording`); the sentence was reworded to an instruction. On the first fixture main also closed in one run and, with a stub prior report and an uncut Release, did not close in another (the Release-cut confound the case check named).

Result: **regression guard**, not a failing-on-main case. A capable model closes the issue on acceptance from its own reading even though main's `reporting.md` says to stop rather than close, and each branch run said the skill gave no step, so the text change is a clarity fix rather than a measured behaviour change. The runs are single samples; they show the case scores a correct close and a missing one, not a rate. Not exercised: a real tracker or a `team-lead` session.

## 2026-11-09 — Ticket #55: milestone planning offers set-aside work first, `plan-setaside` case

Runner: the Ticket thread. Case check by a fresh premium-tier subagent: first verdict fix (the user's script named issue 31 and gave away the rule; the scorer counted the draft question), both fixed, then the self-test passes. Runs: one fresh premium-tier subagent each, `<checkout>` the branch's working tree or a `git archive` of main (`28f99ba`, plugin 1.2.0, unbumped), scored with the branch's `score.py`. Run level: decision-level in a subagent.

| Case | Branch | Main | Main's failures |
| --- | --- | --- | --- |
| `plan-setaside` | 7/7 | 5/7 | never asked whether the set-aside issue 31 joins; Excluded reads `- None.` |

Not exercised: the Retro, Spec-split, decision-ticket and relay sentences (wording-only rules, no case); a real tracker.

## 2026-11-04 — Ticket #638: model runs at `aeb9b39`, branch and main

Runner: the coordinator. Each case got a fresh premium-tier subagent with only the text of its `PROMPT.md`, and `<checkout>` was set to a `git archive` copy (with `evals/` removed) of the branch (`aeb9b39`, plugin 0.61.0, unbumped) or of main (`c29d3b1`, 0.61.0). The add cases were rebuilt with `aeb9b39`'s `make-fixture.sh`. The plan cases are the runs from the entry below; their fixtures did not change in `aeb9b39`. All were scored with `aeb9b39`'s `score.py`. Run level: decision-level in a subagent. Evidence: [`evidence/638/`](evidence/638/), one folder per `<branch|main>-<case>` holding the prompt, `proposed-actions.md`, `questions.md`, `report.md` and `score.txt`. `main-plan-small` wrote no actions file.

| Case | Branch | Main | Main's failures |
| --- | --- | --- | --- |
| `plan` | 22/22 | 0/2 | wrote no actions |
| `plan-small` | 17/17 | 0/3 | wrote no actions: it asked for the acceptance, the exclusions, a budget and boundaries beyond the Boundary record, then stopped with them unanswered |
| `add-feature` | 24/24 | 19/20 | touched Ticket 12 (usage line) updated once: 0 edits |
| `add-feature-excluded` | 25/25 | 20/21 | the same |

Pass: yes on the branch, for all four cases. Main fails the new behaviour: it has no Ticket-update step, and on the plan cases it wrote no Milestone issue. Not exercised: a real tracker; the read-back of each write (reads are not recorded); planning a feature with `grill-with-docs` or `to-spec` inside the run, because the plan was scripted.

## 2026-11-04 — Ticket #638: first model runs judged, scorer and fixture fixed (not yet passes)

The coordinator ran the four planning cases with fresh premium-tier subagents on `git archive` copies of `c3edc53` (branch) and `c29d3b1` (main), with `evals/` removed. Run dirs: the coordinator's scratchpad `evals638/run-<branch|main>-<case>/`. Scores: `plan` branch 22/22, main 0/2 (no actions); `plan-small` branch 16/17, main 0/3; `add-feature` branch 19/20, main 19/20; `add-feature-excluded` branch 19/21, main 19/21. The three branch failures, judged:

- `plan-small`, "no question on what a one-Release Milestone defaults": **scorer bug**. The one flagged question was the step 6 draft approval, which lists the defaults. The check now skips a question that names the draft. The branch run then scores 17/17.
- Both add cases, "touched Ticket 12 updated once" (main fails it too): **the fixture was wrong, and the skill was vague**. The plan only added `--no-color` to the usage line. Ticket 12 ("names `bye`") stays true once colour lands, so the agent was right to leave it as it was. The fixture's Ticket 12 now has acceptance criteria naming the exact usage line, and the plan changes that line, so 12's own test would check the old line. The skill's touch rule now says a Ticket is touched when its text would be wrong once both land, that it is updated to the end state, and that a Ticket the feature only builds on is not touched.
- `add-feature-excluded`, "Excluded drops colour and keeps translations": **scorer bug**. The section included the agent's note under the list ("colour output … taken out of Excluded"). The check now reads only the list items. The branch run passes it.

`test_score.py` passes 12/12, with new reference runs for the draft approval and the Excluded note, and a planted run that keeps colour in Excluded. These were not passes: the reruns are in the entry above.

## 2026-11-04 — Ticket #638: every plan is a Milestone; features added mid-Milestone join it

Base: Spec branch `claude/project-thread-28offd` at `006570d`, plugin **0.61.0** in both manifests. `milestone` now plans a one-Release Milestone with defaults (one at a time, Acceptance's first line, Excluded `None`), writes no Boundaries section or Budget line (the Boundary record holds them), and, when the user plans a feature while a Milestone is open, joins it to that Milestone without asking which, lists it, labels it and updates each open Ticket it touches; a change to the goal, acceptance or exclusions is one question.

Cases changed: `plan` no longer scripts a budget or a boundary, and its shape check now requires no Boundaries section; `add-feature` no longer pre-answers an agreement question and its plan touches Ticket 12 (the usage line lists `--no-color`); new `plan-small` and `add-feature-excluded`. The prompt now has the runner list every question in `questions.md`, so the question checks are scored.

Offline, run here: `test_score.py` passes 11/11 (a hand-written reference run of `plan-small`, `add-feature` and `add-feature-excluded` passes; a Boundaries section, a budget question, Ticket 12 left as it was, labelling before listing, an agreement question in `add-feature`, and none in `add-feature-excluded` each fail the check they plant). By reading main's text (`c29d3b1`) against the cases: its step 5 asks for the budget and boundaries and its shape holds `## Boundaries`, so `plan-small` fails the question and shape checks; its "Adding a feature" has no Ticket update, so both add cases fail "touched Ticket 12 updated once". That is a reading, not a run.

Real Milestone issue: Milestone 1 (#396, body as of 2026-11-04), `score.py --shape`: 4 of 6 pass. Migration: its `## Boundaries` section (no approvals, budget none, a note that is history) is now history and may be dropped, since it matches the Boundary record; its table still needs the `Feature` and `Accepted when` columns the 2026-11-02 entry names. The issue was not edited.

Model runs (owed when this entry was written): made by the coordinator on the branch and on main. They are recorded in the entry "Ticket #638: model runs at `aeb9b39`, branch and main" above, after the fixture and scorer fixes in the entry "first model runs judged".

## 2026-11-03 — Ticket #530: `milestone` slimmed to planning, add a feature, Startup verification and the report

`milestone` lost its remaining delivery text: Startup verification's four tracker-marker probes became a pointer to `worker-control`'s check plus the one loaded-skill-version probe, and the Delivery and Milestone review sections point at `team-lead`. The report is unchanged but for its thread inventory (no "check-in and stop threads"). Fixtures changed: the `add-feature` case's Startup verification result and the report fixture's probe names now use the check's rows; the cases' expectations and both scorers are unchanged.

Run offline only: both fixtures build, `score.py --shape` passes 8/8 on the `add-feature` Milestone issue, `report/test-score-durations.py` passes, `report/make-fixture.py` builds `ready`, `incomplete` and `final-cut`, and `scripts/check-plugin.sh` (with its new `milestone-no-delivery-detail` check), `scripts/test-check-plugin.py` and `claude plugin validate .` pass. **Owed, not run:** the model runs of `plan`, `add-feature`, and the report cases (`ready`, `incomplete`, `final-cut`, `reentry`) against the new text, by fresh premium-tier sessions as the README says.

## 2026-11-03 — Ticket #529: delivery moves to the team-lead skill

The delivery loop left `milestone` for the `team-lead` skill (ADR 0010). The cases `deliver`, `deliver-stall`, `deliver-pause` and `deliver-lift` were rebuilt on harness events in [`../team-lead/`](../team-lead/README.md), whose [RESULTS.md](../team-lead/RESULTS.md) records their runs from now on; `deliver-checkin-failed` and `deliver-thread-end` were cut with the records they tested, and their fixture code left `make-fixture.sh` and `score.py`. The delivery entries below, and their `evidence/`, stay as history of the earlier loop. The planning and report cases were not rerun: their fixtures and scorers are unchanged apart from dropping the delivery-only parts of the shared fixture.

## 2026-11-03 — Ticket #526: version hand-out and Ticket re-read leave the skill

The `deliver` fixtures now carry both rules in the fixture repo's `CLAUDE.md`; the skill says only to follow the repo's merge-time steps. No case was rerun in this entry: the scorer's hand-out and re-read checks are unchanged, and the entries below were recorded on the earlier skill text.

## 2026-11-02 — Ticket #408: report and stop for review

Base: main `d0c387e`, plugin **0.41.0** in both manifests throughout these runs.
The candidate is the source skill in this entry's commit, not an installed-plugin
load. Six coordinator-dispatched fresh premium-tier Codex subagents (`fork_turns:
none`) received only their fixture prompt/read surface and the source-skill path;
they did not see the scorer or expected results. The Implementer wrote the fixture
and scored their unchanged actions afterward. Runner identities: `/root/eval_red`,
`/root/eval_green`, `/root/eval_incomplete`, `/root/eval_final_ready`,
`/root/eval_reentry`, `/root/eval_final_cut`.

| Case | Score | Observed |
| --- | --- | --- |
| Baseline ready, before skill edit | 2/23, expected red | Empty action list; baseline defers reporting and treats parked F20 as incomplete. |
| Initial candidate ready | 23/23 | One report with both feature outcomes, criterion evidence, parked writer risk, B30 reason, all three visible user messages and the unplanned correction, per-thread and known partial usage, settings, versions, decisions and proposals; check-ins end before the report; no acceptance/close. |
| Incomplete feature | 2/2 | No final report or schedule ending with F20 open and unparked. |
| Final candidate ready | 23/23 | Same report behavior on the final skill; evidence gaps remain explicit. |
| Final candidate re-entry | 1/1 | Existing four actions, including report and schedule ending, unchanged; no duplicate writes or notification. |
| Final candidate final-cut | 2/2 | All features merged but R1's cut still due: Release thread/start record proposed, no report or schedule ending until it finishes. |

[Evidence](report/evidence/) retains inputs, prompts, actual proposed actions and
scorer output. Only the vendor model identifier emitted in final-cut actions is
replaced with `[premium-tier model]` to satisfy the repository's text rule;
[checksums](report/evidence/checksums.json) record original and committed hashes.
No score-relevant content was repaired. Re-entry includes the existing actions in
both the read surface and actions file, plus the before-actions comparison.

Initial green/incomplete ran before the final sequencing and evidence-capture
clarifications; they are supplementary evidence. Final ready, re-entry and
final-cut read the frozen final skill: SHA-256
`64242dd001852a1a4fcfad9b7ecd01380c1bf849e706278929b3d1ac819d10ad`;
reporting reference SHA-256
`11369839b1a25bef130a5c1bd9476d6946a9010b73fa30b46f7621173db5e138`.
Final-ready initially scored 22/23 because the scorer omitted the runtime alias
`cached_input`; accepting that alias gives 23/23 on the identical output. Guard
mutations swapping input/output totals or marking the progress correction planned
each fail their own check. Report contents were also read manually.

Round 1 Nit R1-2 added a scorer-only attribution guard: the original duration
checks accepted coordinator/build-10 durations swapped between their rows.
`python3 evals/milestone/report/test-score-durations.py` failed red on that
mutation, then passed for both initial and final reports after binding coordinator
120 minutes and build-10 50 minutes to their rows and wall time to its statement.
The unchanged ready reports now score 24/24 (one additional wall-time check);
the historical score files above retain their original 23-check outputs. Source
skill/reporting hashes and runtime behavior are unchanged.

Round 2 final Nit R2-1 added known start/end checks bound to the same thread
rows. Before the fix, coordinator `10:00–11:00 | 120 min` still passed; the new
regression failed red on that contradiction. Both recorded ready reports now
pass 26/26, while separately changing coordinator's end to 11:00 or build-10's
end to 12:00 (keeping their duration figures intact) fails the corresponding
session-evidence check. Duration-swap guards continue to pass. These are scorer
fixes only; historical artifacts and source-skill/reporting hashes remain unchanged.

Limits: these test decisions over supplied tracker/session records, not collection
from live runtime usage files, real recurring schedules, thread starts or stops,
tracker comments, installed dependency discovery, user acceptance or a proof run.
The initial Claude Code CLI attempt returned `Not logged in` before a model/tool
turn (zero usage), retained in [runtime result](report/evidence/claude-unavailable.json);
it is no behavior evidence. No real external operation was taken. The report names
unreadable history before 11:00Z, missing build-20 usage/version and unknown
parent/subagent overlap rather than inventing totals. Actual Milestone #396 still
has #409 to deliver, so this Ticket posts no real final report or acceptance.

## 2026-11-02 — Ticket #499: fresh Codex delivery evaluations

Source: main at `0c0cd6494bc37f484a6e5a0472872395cfe3da60`, dev-skills **0.41.0**, both treated as the base throughout this entry. No skill, metadata, fixture, scorer or version changed for these runs. Six fresh premium-tier Codex subagents (main’s `model-tiers` premium mapping, `fork_turns: none`) each received only their fixture's exact prompt body with the checkout substituted and their scratch working directory. They read the checkout skill and fixture tracker, not the eval README or scorer. The Implementer built fixtures outside the repository and scored them only after each evaluator finished. These are source-skill decision/action runs in the desktop environment, not six independently installed-plugin chats and not by-hand author simulations.

Evidence under [499-codex](evidence/499-codex/) preserves each submitted prompt, proposed-action trace with only model identifiers substituted, report where the prompt requests one, and scorer output including exit status, with the same model-only substitution. The thread-end prompt requests no report. No evaluator was shown its score or asked to patch actions after scoring. The repository checker rejects vendor model identifiers in every text file, including evidence: committed copies substitute only the three model identifiers from main’s tier map with bracketed tier-model descriptions. External originals remain untouched; [checksums](evidence/499-codex/checksums.json) record original and committed SHA-256 values. Rescoring those committed action copies preserves every score reported here. No action, marker, time, issue identifier, missing word or other score-relevant content was repaired. The scripted world supplies worker and tracker events; a proposed start never launches a real worker. The existing scorer is lexical: a failed check remains failed here even where the trace expresses similar meaning in other words.

| Case | Raw score | Outcome | Evidence |
| --- | --- | --- | --- |
| `deliver` | 101/107 | **fail** | [actions](evidence/499-codex/deliver/proposed-actions.md), [score](evidence/499-codex/deliver/score.txt), [report](evidence/499-codex/deliver/report.md) |
| `deliver-stall` | 53/54 | **fail** | [actions](evidence/499-codex/deliver-stall/proposed-actions.md), [score](evidence/499-codex/deliver-stall/score.txt), [report](evidence/499-codex/deliver-stall/report.md) |
| `deliver-pause` | 42/43 | **fail** | [actions](evidence/499-codex/deliver-pause/proposed-actions.md), [score](evidence/499-codex/deliver-pause/score.txt), [report](evidence/499-codex/deliver-pause/report.md) |
| `deliver-lift` | 92/95 | **fail** | [actions](evidence/499-codex/deliver-lift/proposed-actions.md), [score](evidence/499-codex/deliver-lift/score.txt), [report](evidence/499-codex/deliver-lift/report.md) |
| `deliver-checkin-failed` | 7/7 | **pass** | [actions](evidence/499-codex/deliver-checkin-failed/proposed-actions.md), [score](evidence/499-codex/deliver-checkin-failed/score.txt), [report](evidence/499-codex/deliver-checkin-failed/report.md) |
| `deliver-thread-end` | 7/7 | **pass** | [actions](evidence/499-codex/thread-end/proposed-actions.md), [score](evidence/499-codex/thread-end/score.txt) |

### Every scripted event: outcomes and limits

A pass below means that event's scored checks passed; it does not establish execution of the proposed side effects. Every event is covered, including the events added by #495–#498. Ranges identify each event in the stated range, not a sampled subset. The score files retain individual check lines, including cross-event checks.

| Case / event | Outcome and observed behavior | Named limit |
| --- | --- | --- |
| deliver 1 | **fail**: check-in helper precedes Release planner, recurring hourly target is correct; two checks fail. | Brief says `post the check-in record` without `<!-- milestone check-in -->`; Release name is delegated via release doc rather than explicitly naming `Milestone 1 · Release 1` or `release-m1-r1`. |
| deliver 2–9 | **pass**: one-slot Spec start, version wait/void/FIFO hand-out, reread after both skill merges, quiet start, no-bump merge and Release start. | Scripted merges and version file, not live GitHub builds. |
| deliver 10–17 | **pass**: Stand-ups, active Release left alone, completed Release end, blocked feature replanning, empty Release reused, fill helper ended, README started and active. | Scripted activity and fixed event clock. |
| deliver 18 | **fail**: one nudge, correct record and no takeover. | Message asks `Answer in a comment on 25-hello-doc.md`; scorer requires literal singular `issue`. Filename is present, but the check still fails. |
| deliver 19 | **pass**: first stall, proven archive helper, no second nudge or premature replacement. | Helper is only a proposed start. |
| deliver 20 | **fail**: archived reading precedes replacement start; two briefing checks fail. | Brief lists branch, issue/comments/attempt records/PR but not literal `tracker`; identifies `ticket-1410` without the literal start time `14:10`. No action was rewritten after scoring. |
| deliver 21–22 | **pass**: lost ready-PR callback recovered from tracker without bump, active worker not nudged, closed Ticket leads to Release. | Fixture PR state supplies the lost callback. |
| deliver 23 | **fail**: Release end and schedule-end helper recorded, no new build or Release. | Brief requires no future firing and `post milestone check-in ended`, but omits exact marker delimiters. Report correctly waits for scheduler shutdown confirmation; this fixture ends before that confirmation arrives. |
| deliver-stall 1–3, 5–7, 9–11, 13–14 | **pass**: arrange once; active starts; first stalls; unconfirmed farewell stop parks it and continues quiet; confirmed quiet stop permits replacement; second stall parks quiet; parked work skipped without repeat notifications. | Scripted session states and proposed archive/replacement only. |
| deliver-stall 4, 8, 12 | **fail**: one nudge at each due wake, recorded and sent. | Combined nudge check fails because messages name issue filenames without literal singular `issue`. |
| deliver-pause 1–8 | **pass**: two-slot limit, pause request, safe-point confirmation, no starts during pause despite free slot, state-only paused check-ins, resume from tracker and next Ticket start. | User messages and safe-point records are scripted, not live suspended builds. |
| deliver-pause 9 | **fail**: only farewell nudged, active README left alone. | Nudge asks for a comment on `10-farewell.md`, omitting literal singular `issue`; same lexical limit as deliver 18. |
| deliver-lift 1–3 | **pass**: arrange once, first Spec, initial active Stand-up. | Scripted scheduler and workers. |
| deliver-lift 4, 8, 12 | **fail**: one nudge at each due wake, sent and recorded. | The combined nudge check fails: messages name `.scratch/issues/<file>` but omit literal singular `issue`. |
| deliver-lift 5–7, 9–11, 13–15 | **pass**: failed stop parks farewell once; next feature continues, confirmed stop permits takeover; second stall parks quiet; parked work skipped; lifted park starts stop first. | Session reads are fixture records; no live stop or replacement. |
| deliver-lift 16 | **fail**: stop confirmed before fresh thread, PR #12 and attempt history included. | Brief lists branch, issue, comments, PR and attempt paths but not literal `tracker`. |
| deliver-lift 17–20 | **pass**: farewell lift reparked when stop still idle; review park adopted without duplicate notification; later user lift starts stop first. | User removals and review history are scripted. |
| deliver-lift 21 | **fail**: latest worker archived before fresh resume; PR #12 and review attempt history included. | Same missing literal `tracker` as event 16. |
| deliver-checkin-failed 1–4 | **pass**: helper proposed, refused target recorded with limit, delivery continues and never rearranges. | The schedule refusal is an event input, not a real scheduler call. |
| deliver-thread-end 1–3 | **pass**: helper ends only its own start, next wake preserves planner, matching planner end precedes new planning. | Fixed tracker overlay and proposed actions, not a live overlapping thread lifecycle. |

No fixture needed an unscripted user answer. No score was converted to a pass by manual interpretation. The failed checks expose explicitness/wording limits in generated briefs; the model-sanitized traces are retained for future evaluation work. They did not demonstrate a Codex-only mechanism defect that warrants a skill change, and this Ticket does not change shared instructions or weaken pass rules to achieve a green result.

### Live runtime evidence and read-only application

The coordinator separately reran the changed check-in probe and archive corroboration; see [Startup verification #499 entry](../startup-verification/RESULTS.md). Its initial heartbeat failed one-shot expiry; the retry proved target arrival and no future firing. At 19:58:25.292704 UTC, after the full negative bound, the coordinator found zero actual planted-token heartbeat deliveries in the intended target and one in the separate runner. The planted Scheduled check-in row fails with `token arrived in the runner, not the target`, and its planted-only verdict is `not ready: Scheduled check-in`. The eval remains partial because the separate-runner analogue differs from the scripted same-runner topology. Those live probes do not turn the fixture starts into actual takeover execution. Installed skill freshness and real worker-state marker were not rerun in this Ticket.

Read-only live application at base `0c0cd64`: [Milestone #396](https://github.com/Luffytse/luffy-dev-skills/issues/396) orders one build at a time. [Release #459](https://github.com/Luffytse/luffy-dev-skills/issues/459) remains open; a `release-m1-r3` open-issue search returns only #499 and #408. The coordinator's [completion record](https://github.com/Luffytse/luffy-dev-skills/issues/396#issuecomment-6586642922) independently confirms #407 and #495–#498 closed after PR #500 merged at this base, with affected #499/#408/#409 reread. Its [check-in record](https://github.com/Luffytse/luffy-dev-skills/issues/396#issuecomment-6585893315) names the sequence #499 then #408, then cut #459 and plan #409. Latest full [Startup verification result](https://github.com/Luffytse/luffy-dev-skills/issues/396#issuecomment-6582222297) is ready for its tested runtime at 0.39.0; this historical result is not a fresh 0.41.0 installed-cache proof.

Thus no next build starts while #499 occupies the slot. Once it closes, #408 gets a regular-tier Ticket thread with `implement`; its issue names no Review depth, so the brief leaves depth out. This eval-only Ticket receives no version number. A later #408 skill change receives a number only when requested just before merge, from main's version then. After all Release 3 issues close, its Release thread cuts #459 and plans the next Release around #409, plus any qualifying maintenance fixes found by Release-end planning. None of these threads, version hand-outs, tracker edits or Releases was actually started by this read-only application.

Validation: `bash scripts/check-plugin.sh`, `python3 scripts/test-check-plugin.py` (15 tests), and `claude plugin validate .` passed. No visual change; no visual QA applies. Door: two-way, eval evidence only. Main's skill and metadata remain unchanged, so no plugin bump or conditional Claude Code rerun is required.

## 2026-11-02 — PR #500 R2-1: thread end identity

Base: `4d8447a`, plugin 0.40.0. Fix: the R2-1 commit containing this entry;
version remains 0.40.0 pending the coordinator's final bump. Seam: the existing
dry-run tracker and proposed actions, with `make-thread-end-fixture.sh`'s focused
overlay and `score.py <out-dir> deliver-thread-end` (see README).

Driven by hand by the Implementer, reading the pre-fix and fixed lifecycle text;
no fresh agent session or real scheduler ran. Before: helper failure writes the
generic ended marker after the planner's start, so the Release running definition
allows a duplicate planner at event 1. Both end markers lack identity: **4/7**.
After: event 1 records check-helper's failure and `Ended check-helper; start
start-helper.`, tells the user the scheduling limit, and starts nothing. Event 2
starts nothing. Event 3 records `Ended release-planner; start start-planner.` and
starts and records the next Release planner for the still-eligible features:
**7/7**. The empty-issue fill report still writes its end; its behavior from R1-1
is preserved, not replaced with a tracker-derived completion rule.

Scorer guards on copies of the passing actions: replacing the helper identity
with the planner identity fails the helper-record check; inserting a Release
start at event 2 fails the next-wake check; removing the event 3 start fails both
the next-planning and ordering checks. Limit: these traces exercise the written
rule by hand, not a fresh Claude Code or Codex coordinator's adherence to it.

## Template

Every new entry records its run level (see [Run level](README.md#run-level)); earlier entries have no such line and are not rewritten.

```
### <date>, commit <sha>, dev-skills <version>: <case>

Run level: decision-level in a subagent | full build-flow in a top-level session
Driven by: <a fresh session at the premium tier | by hand, reading the skill's text>; skill text from <path, branch>
Proposed actions: <the numbered blocks, in short; the Milestone issue body when one was written>
Score: <n>/<m> (`score.py <out-dir> <case>`); questions not covered by the script: <none | list>
Report: <what it said comes next and what delivery waits for>
Before: <the same case run on the skill text before the change, and its score>
Real Milestone issue: <issue>, `score.py --shape`: <result; the migration it needs, or "matches"> (deliver: the loop applied to it, read-only)
Not exercised: <what this run did not reach>
Pass: yes | no. Lessons: <what to change in the skill, if anything>
```

## Runs

### 2026-11-02, commit 802f5a1 (branch `claude/project-thread-k0kn5z`; base d974834), dev-skills 0.40.0 (base, unchanged): `deliver`, one check added after Review Round 1

Review Round 1 found that a Release thread briefed to fill an empty release issue was never recorded as ended, so it counted as running and blocked the next build and Release threads. The skill now records its end when it reports, and `score.py` gained one `deliver` check for event 16 (the ended record before the Ticket thread of 25 starts). `deliver` is now 107 checks; the 106/106 in the entries below was scored before the check existed and is not re-scored here. Run: `score.py` on a freshly built fixture with empty `proposed-actions.md` files scores 35/107, which shows only that the scorer runs. No hand-driven `deliver` run was repeated for this check.

### 2026-11-02, commit 10deafa (branch `ticket-498`; base 6e4996c), dev-skills 0.40.0 (base, unchanged): `deliver-pause` (nine events) and `deliver-lift` (twenty-one events), pause, resume and lifted parks (#498; revised after Ticket checks 1 and 2)

Driven by: by hand, by me as the Implementer subagent of #498 (not a fresh Claude Code or Codex session), reading this branch's "Pause and resume", "Stand-up", "Takeover" and "Parked work" against fresh fixtures built with `make-fixture.sh <out-dir> deliver-pause`, `deliver-lift`, `deliver-stall`, `deliver` and `deliver-checkin-failed`, running `.scratch/world.sh <k>` for events 2 onward. The run is commit 10deafa's tree (the last commit that changes the skill, the evals or the docs, after Ticket check 2's fixes (a lifted Ticket's take-up message is held during a pause and sent with the resume's carry-on, a park by the user's own hand on a feature no thread worked on is neither adopted nor stop-guarded, the resume skips a thread whose issue was review-parked meanwhile, a lifted Ticket of a still-parked Spec waits for the Spec's lift) and Ticket check 1's fixes: a build thread's review park is adopted into a coordinator park record, the resume lists every asked thread, a lifted Ticket is handed to its running Spec thread; this entry's commit adds only this file's text). I decided each block by reading the text and wrote them down with a small scratch script that only numbers and formats the blocks I chose; no session of either agent ran any of it. The person driving it also wrote the skill text, the fixture and the scorer: that is this entry's main limit, and Ticket #498's criterion "one recorded Claude Code run" is met only as a hand-driven run, not by a session of either agent. The ticket names the `deliver` case; the pause and the lift are two further cases of the same fixture (as `deliver-stall` is), since `deliver`'s world has one running thread at a time and no park.

Proposed actions, `deliver-pause` ("up to 2 at once", 25 has no blocker, so Release 1 holds 10, 20 and 25): event 1 and 2 as in `deliver-stall`, except that the Release thread's brief groups 25 and both the Spec thread of 10 and the Ticket thread of 20 start (25 waits for a slot). Event 3 (10:20Z, the user pauses): a `<!-- milestone pause -->` comment on the Milestone issue quoting the user and listing the two threads asked (`Asked to reach a safe point:`), and one message to each running thread asking it to push, post a `<!-- milestone safe point -->` comment on its issue and wait; nothing started. Event 4 (10:30Z): 10's thread has recorded its safe point (head commit `farewell: usage text`, read on its branch) and 20 finished (#8 merged, no version change, closed), so a `<!-- milestone paused -->` comment lists both and the user is told in one line; no thread starts though a slot is free and 25 is startable. Events 5 and 6 (11:00Z, 12:00Z): a Stand-up record each ending `Paused since 10:20Z: this check-in records state only.`, nothing else; at 12:00Z 10's thread has done nothing since 10:28Z and is not nudged. Event 7 (12:30Z, the user resumes): a `<!-- milestone resume -->` comment with a `Told to carry on:` line for 10 (not the finished 20), a message telling 10's thread to carry on from its safe point, and the Ticket thread of 25 (`implement`, cheap, the Milestone issue linked) with its delivery-thread record; no Stand-up. Event 8 (13:00Z): a Stand-up, previous check-in the resume, 10 (pushed 12:45Z) and 25 (started 12:30Z) active. Event 9 (14:00Z): 10 silent since 12:45Z, one nudge asking for a comment on its issue, 25 (pushed 13:40Z) active.

Proposed actions, `deliver-lift`: events 1 to 14 as in `deliver-stall` (10 parked at event 6 with its stop unconfirmed, 20 parked at event 13 after a second stall). Event 15 (21:00Z check-in, the user removed `parked` from 20 at 20:40Z, its fresh thread's draft pull request #12 is on the tracker and its session still reads idle since 16:12Z): a `<!-- milestone park lifted -->` comment on 20, a stop thread briefed to archive that fresh thread's session, its delivery-thread record and the Stand-up record (10 parked and skipped); no fresh thread, since a writer may remain. Event 16 (21:10Z): the record reads archived since 21:06Z, so a stop record, then a fresh Ticket thread on 20 whose brief names the pushed branch (`quiet: the --quiet flag`), pull request #12 and the attempt history, and the thread it takes over from (16:10Z), and its delivery-thread record; no Stand-up. Event 17 (22:00Z, the user removed `parked` from 10 at 21:50Z): a park-lifted record on 10 and a stop thread for the Spec thread's session (started 10:05Z); no fresh thread. Event 18 (22:10Z): the record still reads idle on both reads, so no stop record and no fresh thread, 10 is parked again (the `parked` label and a park record naming the idle reading) and the user is told once. Event 19 (23:00Z check-in): 20's fresh thread (started 21:10Z) has parked 20 itself in review at 22:50Z (the label and an attempt record, no coordinator record), so the coordinator writes its own `<!-- milestone parked -->` record (review park, a writer may remain, linking the attempt record), no label, no message to the user, and a Stand-up listing 10 and 20 as parked and skipped. Event 20 (the user removed `parked` at 23:20Z): a park-lifted record and a stop thread for the thread started 21:10Z, no fresh thread. Event 21: the record reads archived since 23:36Z, a stop record, then a fresh Ticket thread naming pull request #12 and the attempt history.

Score: `deliver-pause` 43/43, `deliver-lift` 95/95 (its first 54 are `deliver-stall`'s checks on events 1 to 14), and, unchanged by this ticket, `deliver` 106/106, `deliver-stall` 54/54, `deliver-checkin-failed` 7/7 on hand-written runs (`score.py <out-dir> <case>`; empty `proposed-actions.md` files score 11/43 and 29/95).

Before: the same events run by hand on 6e4996c's skill text (the base: it skips parked work and says resuming is not part of the skill, and has no pause), scored by this branch's scorer: `deliver-pause` 19/43 and `deliver-lift` 69/95. On the old text the pause word starts nothing and records nothing at event 3 (no rule names it); at event 4 the freed slot starts 25's thread; the two check-ins nudge as usual (25 and 10 are both silent at 12:00Z) and the resume at event 7 is a no-op: 24 checks fail (the two lists, every pause, safe point, paused and resume record, the held start, the state-only check-ins and the start at the resume). In `deliver-lift` events 1 to 14 pass and the old text records only a Stand-up at events 15 and 19 and nothing at the others (the park stays, "starts nothing"; a review park is never recorded): 26 checks fail (the lift records, both stop threads, 20's fresh thread with its branch, pull request #12 and attempt history, and 10's second park and the user's message). Scorer guards, on copies of the passing runs: a thread for 25 at event 4 fails "nothing starts though a slot is free", "only the paused record and the message are written" and "no thread starts while paused"; a nudge to 10 at event 6 fails "records state only", "not nudged or stalled" and "one nudge in the whole run"; no thread for 25 at the resume fails 7 event-7 checks; a fresh thread on 20 at event 15, before the stop, fails "no fresh thread on 20 yet", "events 15 to 15: no fresh thread before its stop is confirmed" and the stop-thread count; a fresh thread on 10 at event 18 in place of the second park fails 5 checks; dropping the adopting park record at event 19 fails 2 checks (the record and the Stand-up's parked line stays but the adoption is missing).

Real Milestone issue: not reapplied (Milestone 1 #396's loop state is as in the entries below).
Not exercised: a fresh session of either agent; real threads receiving the pause message (the safe point records, the finished pull request and the sessions are played by `world.sh`); a pause that stays pending because a thread never reaches a safe point; a pause arriving while a takeover is in progress or after a nudge (the rule that a nudge older than the resume is void); a version number requested during a pause (recorded `Waiting`) or out across one; a skill merge's re-read during a pause; a pause of a Release thread; a resume or a pause word when none or one is in effect; a lifted park whose latest build thread already has a stop record newer than its start (the fresh thread at the same wake); a lifted Ticket during a pause (its held message), a feature the user parked by hand before any thread worked on it and its lifting (started with no stop), a thread whose issue was review-parked during a pause (skipped at the resume); a pause still pending at the resume (a safe point posted after it; the text now tells every listed thread to carry on, but no event plants it); a Ticket of a Spec lifted under a running Spec thread (handed to the Spec thread by message, and the Spec-not-running path through the Spec's own stop); a lifted park on a pull request that builds no issue; a lift read while paused or while no slot is free; a fresh thread whose start errors (parked again by "Takeover" step 4); a lift with no proven stop; Codex desktop; a late check-in after delivery is done (as in the #496 entry).
Pass: yes, as a by-hand run.

### 2026-11-02, commit 83dd6b7 (branch `ticket-497`), dev-skills 0.40.0: `deliver` (twenty-three events) and `deliver-stall` (fourteen events), takeover and park (#497)

Driven by: by hand, by me as the Implementer subagent of #497 (not a fresh Claude Code or Codex session), reading this branch's "Stand-up", "Takeover" and "Parked work" against fresh fixtures built with `make-fixture.sh <out-dir> deliver`, `deliver-stall` and `deliver-checkin-failed`, running `.scratch/world.sh <k>` for events 2 onward. The run is commit 83dd6b7's tree (the last commit that changes the skill, the evals or the docs, after Ticket check 1's fix that a nudge asks for its answer as a comment on the issue and Ticket check 2's fix that a takeover whose issue closed meanwhile ends with a takeover-ended record (also where the stop is not confirmed, from Ticket check 3); this entry's commit changes none of them). I decided each block by reading the text and wrote them down with a small scratch script that only numbers and formats the blocks I chose; no session of either agent ran it. So Ticket #497's criterion "one recorded Claude Code run" is met only as this hand-driven run, by the person who also wrote the skill text: that is this entry's main limit. "Before" and "after" are hand-written `proposed-actions.md` files for the same fixtures, differing only where the text differs.

Proposed actions, `deliver`: events 1 to 18 as in the #496 entry below, except that every nudge message (event 18 here, events 4, 8 and 12 in `deliver-stall`) asks for the answer as a comment on the thread's issue, since a message-only answer is not activity. Event 19 (17:00Z): the Ticket thread of 25 (started 14:10Z) has nothing after its 16:00Z nudge, so it has stalled: a `<!-- milestone stall -->` comment on `25-hello-doc.md` (stall 1 of this feature), the Stand-up record naming it still silent, then, the fixture's Confirmed stop row reading "archived by a thread", a stop thread with `milestone` at the cheap tier, briefed to archive that thread's session, write nothing on the tracker and report what the call returned, and its delivery-thread record on 25. The session record reads idle, so no stop record and no fresh thread. Event 20 (17:10Z): the stop thread reports; the session record reads archived since 17:06Z, so a `<!-- milestone stop confirmed -->` comment on 25 with that reading, then a Ticket thread with `implement`, tier cheap, briefed with the thread it takes over from, that its stop was confirmed, and to resume from the pushed branch (the 14:40Z commit) and the tracker, and its delivery-thread record with `Takes over from ...; stop confirmed at 17:10Z.` No Stand-up (a thread's wake). Event 21 (18:00Z): the fresh thread pushed at 17:35Z and turned #11 ready at 17:50Z with no report: told to merge with no bump, one Stand-up record. Events 22 and 23 as the old 20 and 21.

Proposed actions, `deliver-stall`: events 1 and 2 as in `deliver`. Event 3: the Spec thread of 10 active (its start at 10:05Z). Event 4: nudged. Event 5: still silent: the stall record on 10, the Stand-up record, a stop thread for 10's session and its record. Event 6 (13:10Z): the stop thread reports the archive call returned success, but the session record still reads idle since 10:30Z on both reads, so the stop is not confirmed: `parked` added to 10 and a `<!-- milestone parked -->` comment naming the idle reading and that a writer may remain, one message to the user, then step 2 starts the Ticket thread of 20 (10 parked holds no slot under one at a time) and its record. Event 7: 20 active; the Stand-up record lists `Parked, skipped: 10-farewell.md`. Event 8: 20 nudged. Event 9: stalled: stall record, Stand-up record, stop thread. Event 10 (16:10Z): the record reads archived since 16:06Z: stop record, then a fresh Ticket thread on 20 briefed to resume from the pushed branch (13:30Z) and the tracker, and its record. Event 11: the fresh thread active. Event 12: nudged. Event 13 (19:00Z): still silent, the feature's second stall: stall record (stall 2), the Stand-up record, `parked` on 20 and its park record naming the second stall, the user told at once; no stop thread, no fresh thread. Event 14: only the Stand-up record, both parked issues listed as skipped.

Score: `deliver` 106/106, `deliver-stall` 54/54, `deliver-checkin-failed` 7/7 on a hand-written run of its four events (`score.py <out-dir> <case>`; empty `proposed-actions.md` files score 35/106 and 17/54).

Before: the same events run by hand on d4b6c4b's skill text (the Stand-up only records a thread still silent after its nudge), scored by this branch's scorer at b5f0c82 (deb4ef6's checks plus the nudge checks e2c7f83 added): `deliver` 96/106, failing the nudge's ask for a comment on the issue at event 18 and the nine takeover checks at events 19 and 20 (the stall record, the stop thread, its brief, its record, the stop record, the fresh thread after it, its brief's branch and tracker, the thread it takes over from, its record); `deliver-stall` 33/54, failing the nudges' ask for a comment on the issue, the stall, stop thread, park, user message and next-feature checks at events 5 and 6, the parked line at event 7, all of 20's checks from event 8 on (on the old text 10 keeps the one slot for good, so 20 never starts) and the run's nudge and stall totals. Scorer guards, on copies of the passing runs: a fresh thread on 25 at event 19, before the stop record, fails three checks; a fresh Spec thread for 10 at event 6 in place of the park fails five; telling the user about 10 again at event 7 fails "not told about 10 again"; a nudge on parked 10 at event 8 fails three (the skip check, event 8's one nudge and the nudge total); a stop thread at event 13 in place of the second-stall park fails four.

Real Milestone issue: not reapplied (Milestone 1 #396's loop state is as in the entries below).
Not exercised: a fresh session of either agent; a real stop, a real session-details read and a real fresh thread (the stop thread's report and the session record are played by `world.sh` and `.scratch/sessions/`; the probes of the real stops are in `evals/startup-verification/RESULTS.md`, and neither probe ran a takeover); the coordinator taking the stop itself (Codex desktop's archive); no proven stop (a failed Confirmed stop row, or a worker of another kind); a stop thread that never reports by the next check-in; a takeover thread's start that errors; a stalled Release thread; a takeover in progress across a Stand-up; a takeover whose issue closed meanwhile, its stop confirmed or not (the takeover-ended record) or whose pull request turned ready or merged meanwhile (the fresh thread still starts); and what follows once the user lifts a park (resuming it was not part of the skill at this commit; the #498 entry above covers it).
Pass: yes, as a by-hand run.

### 2026-11-02, commit b74409f (branch `ticket-496`; base dced8d5), dev-skills 0.40.0 (base): `deliver`, twenty-one events, Stand-ups (#496)

Driven by: by hand, by me as the Implementer subagent of #496 (not a fresh Claude Code or Codex session), reading this branch's "Stand-up" and "Check-ins" against fresh fixtures built with `make-fixture.sh <out-dir> deliver` and `deliver-checkin-failed`, running `.scratch/world.sh <k>` for events 2 onward. The run is commit b74409f's tree (the last commit that changes the skill, the evals or the docs; this entry is the next commit and changes none of them). No fresh session ran it and no Claude Code or Codex session was started, so Ticket #496's criterion "one recorded Claude Code run" is met only as a hand-driven run, not by a session of either agent; and the person driving it also wrote the skill text: that is this entry's main limit. "Before" and "after" are two hand-written `proposed-actions.md` files for the same fixture, differing only where the text differs.

Proposed actions: events 1 to 9 and 11, 13, 16, 20, 21 as in the 2026-11-02 `deliver`, eighteen events entry (commit 4d0a751, #495) below (its events 17 and 18 are now 20 and 21). Event 10 (11:00Z, the first check-in): one `<!-- milestone stand-up -->` on the Milestone issue, `Check-in 11:00Z; previous delivery start 10:00Z.`, the Release thread started 10:50Z active, no decision; no nudge, no message. Events 12, 14, 15: a Stand-up record saying no delivery thread is running (12 and 15 then start their Release thread as before). Event 17 (15:00Z): the Ticket thread of 25 (started 14:10Z, pushed 14:40Z) active, no nudge. Event 18 (16:00Z): nothing pushed, commented or changed since 15:00Z, so one message to the thread and one `<!-- milestone nudge -->` comment on `25-hello-doc.md`, then the Stand-up record naming it silent and nudged; nothing started. Event 19 (17:00Z): #11 turned ready at 16:40Z with no report, so the coordinator acts as on a report: README only, no number, the thread is told to merge with no bump; one Stand-up record; no second nudge.

Score: 88/88 (`score.py <out-dir> deliver`); `deliver-checkin-failed` 7/7 on a hand-written run of its four events.

Before: the same twenty-one events run by hand on dced8d5's text (check-ins arranged, no Stand-up): 66/88, failing exactly the 22 Stand-up checks (a Stand-up record with the check-in's time at each of events 10, 12, 14, 15, 17, 18 and 19, the one nudge and its message at event 18 and the Stand-up record naming it, the act on the lost callback at event 19, its record, and the one-nudge total). Scorer guards, on copies of the passing run: a nudge also at event 17 fails "active thread gets no nudge", "writes nothing but its Stand-up record" and "exactly one nudge"; no Stand-up record at event 19 fails its four event-19 checks; an extra write (a close) at event 10 fails "writes nothing but its Stand-up record".

Real Milestone issue: not reapplied (Milestone 1 #396's loop state is as in the entries below).
Not exercised: a fresh session; a late check-in after delivery is done (the text says it holds no Stand-up; no event plants it, and the scorer's "recorded only at scheduled check-ins" would catch a record at event 21 but not a late check-in); real pull request, branch and comment timestamps (the fixture's tracker doc states them, in `.scratch/branches/` and `.scratch/pulls/`); a thread still silent at the next check-in after its nudge (the text says to record it and take no step; no event plants it); a finished Release or merged skill change found by a Stand-up (only a ready pull request is planted); Codex; the next Ticket's takeover.
Pass: yes, as a by-hand run.

### 2026-11-02, commit 21b0a52 (branch `ticket-495`; base 4d0a751), dev-skills 0.40.0 (base): `deliver-checkin-failed` (#495, Ticket check 1)

Driven by: by hand, by the Implementer of #495, reading this branch's "Check-ins" against a fresh fixture built with `make-fixture.sh <out-dir> deliver-checkin-failed`, running `.scratch/world.sh <k>` for events 2 to 4. No fresh session ran it, and the person driving it also wrote the skill text.

Proposed actions: event 1 as in `deliver` (the check-in thread and its record, then the Release thread and its record). Event 2: (5) `<!-- milestone check-in failed -->` on the Milestone issue, "the scheduler refused the coordinator's session as a target"; (6) the check-in thread's ended record; (7, 8) the Spec thread of 10 and its record; the user hears the limit in one line. Events 3 and 4: the hand-outs as in `deliver`, and no check-in thread, since the failed record marks check-ins off.

Score: 7/7 (`score.py <out-dir> deliver-checkin-failed`; an empty `proposed-actions.md` scores 1/7). `deliver` reruns at 54/54 on the same text.

Before: the same four events on 4f066d9's text, where a failure was only an event (the thread's report) and left nothing but the generic ended record: event 2 wrote the ended record and started the Spec thread; at event 3 the tracker showed no check-in record, no running check-in thread and nothing marking a failure, so the arrange rule fired again (a second check-in thread). 4/7: fails the failed record, its limit, and "not arranged again after the failure".

Not exercised: a fresh session; a coordinator scheduling its own check-ins and failing; the user's go-on naming Scheduled check-in (read as off by the same rule).
Pass: yes, as a by-hand run.

### 2026-11-02, commit 4d0a751 (base), dev-skills 0.40.0 (base): `deliver`, eighteen events, check-ins (#495)

Driven by: by hand, by the Implementer of #495, reading this branch's `plugins/dev-skills/skills/milestone/SKILL.md` ("Delivery", "Check-ins") against a fresh fixture built with `make-fixture.sh <out-dir> deliver`, running `.scratch/world.sh <k>` before each event from event 2 on. No fresh session ran it, and the person driving it also wrote the skill text: that is this entry's main limit.

Proposed actions: events 2 to 14 as the entry below. Event 1 now opens with (1) a check-in thread with `milestone`, tier cheap, briefed to read the coordinator's session as its parent session and create one recurring scheduled task bound to it, every 1 hour (the fixture's Boundary record), each firing carrying `Milestone check-in: <Milestone issue>`, read it back and post the `<!-- milestone check-in -->` record, and (2) its delivery-thread record on the Milestone issue, both before the Release thread (the Startup verification row names a thread scheduling into the coordinator's session, so a thread arranges them). Event 2's world adds the check-in record (schedule `sched-01`), so from then on check-ins are running and no wake arranges them again. Event 15: 36 has closed, so step 1 starts a Release thread to fill the empty 41 with 25, opening no second release issue. Event 16: 41 now carries 25, so the Ticket thread of 25 with `implement` (tier cheap). Event 17: every `release-m1-r2` issue is closed, so the Release thread for 41. Event 18: its ended record on 41; no feature is left open, so delivery is done: a check-in thread with `milestone` briefed with `sched-01` to delete it, read back that no future firing remains and post `<!-- milestone check-in ended -->`, and its record, before the one line to the user.

Score: 54/54 (`score.py <out-dir> deliver`; an empty `proposed-actions.md` scores 18/54).

Before: the same eighteen events run by hand on the base's text (no check-ins in Delivery): the same actions without the two check-in starts and their records: 48/54, failing exactly the six check-in checks (a check-in thread at event 1, its brief's interval, target and recurrence, its check-in record line, arranged before the Release thread, the end at event 18, and the end's read-back and ended record). Scorer guards, on copies of the passing run: a second check-in thread at event 10 fails "events 2 to 17: the check-ins are neither arranged again nor ended" (and event 10's "no thread started"); an end brief without the read-back fails event 18's read-back check; a check-in thread numbered after the Release thread fails "arranged before the Release thread starts".

Real Milestone issue: not reapplied (Milestone 1 #396's loop state is as the entry below, plus #407 now in build).
Not exercised: a fresh session; a real scheduler (the check-in record is played by `world.sh`; the Claude Code cloud-project probe of the targeting is in `evals/startup-verification/RESULTS.md`); the coordinator scheduling its own check-ins (Codex desktop's heartbeat); a check-in thread that fails to arrange them (the `deliver-checkin-failed` entry above); a scheduler whose shortest interval is longer than the record's; a go-on without check-ins.
Pass: yes, as a by-hand run.

### 2026-11-02, commit d85f265 (base), dev-skills 0.37.0 (base): `deliver`, with Milestone 1 as the second case

Driven by: by hand, by the Implementer of the delivery-loop Ticket, reading this branch's `plugins/dev-skills/skills/milestone/SKILL.md` ("Delivery") step by step against a fresh fixture built with `make-fixture.sh <out-dir> deliver`, running `.scratch/world.sh <k>` before each event from event 2 on (the fixture is built in event 1's state) and reading the state from the fixture's tracker each time. No fresh session ran it (the Implementer was not allowed to start further agents), and the person driving the run also wrote the skill text: that is this entry's main limit.

Proposed actions, by event (re-run after Ticket checks 1 and 2, on the twelve-event fixture, and after Round 2 of the pull request review, on the fourteen-event fixture):

1. Read: no release issue names the Milestone and no Release thread record, so step 1. Grouping: 10 (with 11 and 12), then 20, both open, unlabelled for a Release, with no open blocker; 25 is left out, blocked by the open `35-readme-tool.md`; 2 of the cap of 5. (1) Start a thread, `release`, briefed with the Milestone issue, the release doc, Milestone 1 · Release 1 (`release-m1-r1`), the grouping in order, and "no Release of this Milestone has been cut yet, so the plan is the feature scope only"; (2) its delivery-thread record on the Milestone issue. No build thread.
2. Read: `40-release-m1-r1.md` names the Milestone and its label is on 10, 11, 12 and 20, as grouped. Slots: the smaller of the project's 3 and the Milestone's "One at a time", so 1, none taken. Next in build order: 10, a Spec with its Tickets filed. (3) Start a thread, `implement-spec`, for 10, with the Milestone issue, model tier regular and Review depth Deep (10's own lines), and the repo; (4) its record on 10. 20 waits for 10 to close.
3. Read: #7 changes `skills/greeting/SKILL.md`, which the release doc says bumps (a changed skill rule: minor); main's `VERSION` reads 0.3.0 and no hand-out record is out. (5) Comment on 10: `<!-- milestone version hand-out -->`, `Version 0.4.0 for #7: merge it next, ...`; (6) message the Spec thread its number. No start: 10 still holds the one slot.
4. Read: #10 builds no issue and changes `skills/greeting/SKILL.md`, so it bumps; 0.4.0 is out for #7 (main has not reached it, #7 is open, 10's thread runs). (7) Comment on #10 itself: `Waiting: #10 asked while 0.4.0 was out.`; (8) tell the thread to hold #10.
5. Read: #7 closed unmerged, so its record is void and nothing is out; main still reads 0.3.0. #10's waiting request has no number after it and asked first. (9) Comment on #10: `Version 0.4.0 for #10 ...`, saying #7's record is void; (10) comment on 10: `Waiting: #9 asked while 0.4.0 was out.`; (11) message the thread both.
6. Read: main's `VERSION` reads 0.4.0, the number #10 got, so nothing is out; #10 changed the `greeting` skill (a wording rule), so a re-read is due. (12) Comment on 20: re-read after #10, still fits. #9's waiting request has no number after it: (13) comment on 10, `Version 0.5.0 for #9 ...`; (14) message the thread its number. No start: 10 holds the slot.
7. Read: main's `VERSION` reads 0.5.0, the number handed out; #9 changed the `greeting` skill, so a re-read is due before any start. 20 is the one open Milestone issue no running thread builds whose body names the skill; against main's new skill text (every message goes through one `say` function, farewells included) its criteria miss the farewell. (15) Edit 20's body, whole, adding `greet.sh --quiet bye Ada` prints nothing and exits 0 and a re-read note (inside the agreement: the Milestone's own acceptance already runs `greet.sh --quiet bye Ada`). 20 has no open blocker; 10 is closed, so the slot is free. (16) Start a thread, `implement`, for 20, tier regular, with no Review depth (20 names none, so `agentic-review` chooses); (17) its record on 20.
8. Read: #8 changes only `src/greet.sh` and `test.sh`, nothing the release doc says bumps. (18) Message the Ticket thread: no number, merge with no bump.
9. Read: #8 changed no skill, so no re-read; every issue labelled `release-m1-r1` is closed, and no Release thread is running. (19) Start a thread, `release`, for `40-release-m1-r1.md` and the Milestone issue (Triage batch, Release-end Retro planning, the cut, the next planning); (20) its record on the release issue. 25 is in no Release, so no build thread.
10. Read: the Release thread's record on 40 has no ended record after it and no newer release issue exists, so it is running: step 5 starts none, step 1 does not apply (40 is still open). No action.
11. Read: 40 is closed with its notes; the thread reports it planned nothing. (21) The ended record on 40. Step 1: no open release issue, no Release thread running, but the grouping is empty (25 still blocked), so nothing starts; the user would hear that 25 waits on 35.
12. Read: 35 is closed, so 25 is unblocked and the grouping holds it. (22) Start a thread, `release`, to plan Milestone 1 · Release 2 with 25, briefed with the last release issue cut (40) for its Triage batch and Release-end Retro planning, and, like the briefs of events 1 and 9, with "if no planned feature qualifies and no maintenance fix joins, open no release issue, label nothing, and report that it planned no Release"; (23) its record on the Milestone issue.
13. Read: `41-release-m1-r2.md` names the Milestone but no issue carries `release-m1-r2`, so it is empty: no current Release, and never done or cut; 25 is blocked again by the open `36-readme-style.md`, so the grouping is empty. (24) The ended record on the Milestone issue. Step 5 starts no Release thread for 41; step 1 has nothing to plan; the user would hear in one line that 41 holds no issue and that 25 waits on 36.
14. Read: the same state. No action: 41 is still empty, so no second Release thread starts.

Score: 42/42 (`score.py <out-dir> deliver`; an empty `proposed-actions.md` scores 16/42). Questions: none. Report: none written (the case has no user turn); the user hears only the Release planning differing from the grouping, a re-read that would change the agreement, a feature left blocked or parked, or delivery ending.

Before: the same case run by hand on the base's skill text, whose Delivery section said its steps were "not part of this skill yet" and to deliver "as the project's own instructions say". The fixture's project instructions hold only a thread limit (3), the tier map and "no `triage`", so the run started 10's and 20's build threads at event 1 (within the limit of 3, with no Review depth in their briefs; 25 is blocked) and, for events 2 to 14, wrote no action (no rule names the Release thread, the hand-out, the re-read or the Release boundary): 16/42. The 16 are the checks a run that does nothing passes (no extra thread, no number, no label). Scorer guards, on copies of the passing run: starting 20 in event 2 as well fails 2 checks; handing #8 the number 0.6.0 fails "no version handed out for a pull request that changes no skill"; starting 20's thread before its re-read fails "20-quiet re-read against the changed skill before its thread starts", and so does a copy whose only comment on 20 before its start is the delivery-thread record; a brief for 20 carrying `Review depth: Standard` fails "its brief carries no Review depth"; leaving #10 waiting at event 5 because main never read the void 0.4.0 fails "#7's number is void, so the waiting #10 gets 0.4.0", and so does keeping #7's number out; a second Release thread at event 10 fails "no thread started while the Release thread is running"; no Release thread at event 12 fails "a Release thread started to plan the next Release with 25-hello-doc"; a Release thread started at event 13 or at event 14 to cut the empty `41-release-m1-r2.md` fails that event's "no thread started" check; Release thread briefs without the open-no-release-issue line fail "each Release thread's brief says to open no release issue when nothing qualifies".

Real Milestone issue: Milestone 1 (#396), its open Release 3 (#459, `release-m1-r3`) and the release doc `docs/agents/release.md` (pull requests bump; a pull request changing `plugins/dev-skills/skills/` bumps), read on 2026-11-02 with main at 0.37.0; the loop applied read-only, nothing written:

- **Delivery gate.** The latest Startup verification result on #396 (2026-11-02T06:39:07Z) reads `not ready` (Scheduled check-in, Confirmed stop, and in its planted run Real worker state), and no go-on from the user is recorded on #396. Under the skill, delivery for Milestone 1 waits on the user's rerun or go-on, so everything below is what the loop would do once one is recorded, not what it would do now.

- **State.** Order rule "one at a time, in this order". Release 3's maintenance fixes #458, #448 and #447 are closed, and so is #405. Open: #406 (this Spec; its thread is running), then #473, #407 and #408, each blocked by the one before it (#473 by #406, #407 by #406 and #473, #408 by #407). Release 3's real build order matches the loop's: its release issue puts #458 first, then #405, #406, #473, #407, #408, so #473 and #407 come after #406, as the row 10a note on #396 says.
- **Next thread.** None now: #406 holds the one slot. Once #406 closes, #473 (a Spec with its Tickets #474 and #475 filed) gets a Spec thread with `implement-spec`, with no Review depth in its brief unless #473 or the user names one; after it, #407 first gets a `to-tickets` planning thread (its Tickets are not filed), then its Spec thread; then #408, a lone Ticket, with `implement`.
- **Version hand-out.** When #406's Spec pull request asks just before its merge, it changes the `milestone` skill, a changed skill: minor, so 0.38.0 if main still reads 0.37.0 and no other number is out, recorded on #406.
- **Re-read after that merge.** The open Milestone 1 issues no running thread builds that name the `milestone` skill or its files: #473, #474, #475, #407, #408 and #409. This repo runs `triage`, so a `triage` thread does the re-read, before #473's thread starts.
- **Release boundary and the next Release.** When every `release-m1-r3` issue is closed (#406, #483, #484, #473, #474, #475, #407, #408), a Release thread with `release` cuts Milestone 1 · Release 3. Its planning, by the rule step 1 groups with, takes **Milestone 1 · Release 4** (`release-m1-r4`): #409 (piece C5, the one planned feature left; its blocker #408 is closed by then), 1 of the cap of 5, plus the maintenance fixes the Release 3 Triage batch and Release-end Retro planning mark `joins the next Release` (not known yet). Once Release 4 is cut, no planned feature is left open, so delivery is done and the Milestone review follows.
- **Migration it needs.** Delivery-thread and version hand-out records start with this skill: the running #406 thread, and the threads before it, have none, so the first wake under the new text adds a delivery-thread record to #406, as the skill says for a feature already being built, before counting slots; without it the slot would read as free and #473 would start early. The feature table's columns still need the planning entry's migration (`Piece` to `Feature`, an `Accepted when` column); the loop reads only the order and the issues from it, so it runs either way.

Not exercised: a fresh session following the skill (the run was by hand, by its author); a real tracker and real threads (events were scripted and the threads' work was played by `world.sh`); the delivery gate (a `not ready` verdict, the user's rerun, and a go-on recorded on the Milestone issue): the fixture starts at `Verdict: ready`, and live #396 reads `not ready` now with no go-on recorded; a Spec with no Tickets yet (the `to-tickets` thread), maintenance fixes in a Release, a parked feature, the `triage` path of the re-read, and Releases bump; and these delivery branches: a repeat request after main's version moved (step 3.4), the post-merge version check finding main wrong (step 3.5), the patch bump branch (every hand-out here is minor), the step 4 question to the user over a change to the agreement and its close-as-obsolete outcome, related issues treated as one feature, the cap of 5 (no grouping here reaches it), step 1 filling an existing empty release issue once a blocker frees (and that Release thread's end recorded when it reports), and the Milestone done ending (no features left open).
Pass: yes, as a by-hand run. Lessons: Ticket check 1 found that a default Review depth of Standard kept Deep from ever reaching `agentic-review`, that a closed or parked pull request kept its number out for good, that step 5 lacked step 1's guard against a second Release thread, and that nothing re-planned features left blocked after the last Release; the skill now carries a depth only when one is named, voids such numbers, guards step 5 and runs step 1 again once a left-out feature is free, and the fixture's events 4, 5 and 10 to 12 check each. Ticket check 2 found that a waiting request was served only once main read the number ahead of it, which never happens when that number goes void; the skill now serves waiters at any wake with no number out, and events 4 to 6 check it. The first draft also started threads in "the Milestone issue's order", which leaves a Release's maintenance fixes unplaced; the skill now builds them first, in the release issue's order, as Release 3 did with #458. The missing records for threads started before this skill are the migration above. Round 2 of the pull request review found that a Release planning with nothing to plan still opened a release issue, which step 5 then read as a done Release, cutting empty Releases again and again; every Release thread's brief now says to open no release issue when nothing qualifies, an empty release issue is never done or cut, and events 12 to 14 check both. A rerun by a fresh premium-tier session is the next evidence to get.

### 2026-11-02, commit b14efe5 (base), dev-skills 0.37.0 (base): `plan` and `add-feature`, with Milestone 1 as the second case

Driven by: by hand, by the Implementer of the planning-phase Ticket, reading this branch's `plugins/dev-skills/skills/milestone/SKILL.md` step by step against fresh fixtures built with `make-fixture.sh`, taking each answer from the fixture's scripted user. The Implementer was not allowed to start further agents, so no fresh session ran it; the person driving the run also wrote the skill text, which is the main limit of this entry.

**`plan`.** Step 1 read the Boundary record (label form `milestone-<n>`), the tracker doc and `.scratch/labels.md`: no label in the form and no Milestone issue, so planning starts from the goal. Steps 2 to 6 took the scripted goal, features (10 and 20, both already planned), order ("two at once"), acceptance, exclusions, budget and extra boundary; `30-colour.md` was not proposed, as it does not serve the goal, and the user's answer to any proposal was "no" anyway. Step 7 took Milestone number 1 (no label in the form yet). Proposed actions, in order:

1. Create a label `milestone-1`.
2. Create an issue `Milestone 1: goodbye and quiet`, labelled `milestone-1`, with this body:

   ```
   ## Goal

   By the end, the greeter can say goodbye and can run silently in scripts, so it can ship as 1.0.

   ## Features, in build order

   In this order, up to 2 at once. Each feature is its own issue carrying `milestone-1`.

   | # | Feature | Kind | Accepted when |
   | --- | --- | --- | --- |
   | 1 | `10-farewell.md` Add a farewell command | Spec | `greet.sh bye Ada` prints `Goodbye, Ada!` and exits 0; no name greets the world; `bash test.sh` covers both |
   | 2 | `20-quiet.md` Add a --quiet flag | lone Ticket | `--quiet` prints nothing and keeps the exit code (0 for `hello`, 2 for an unknown command) |

   ## Acceptance

   - Every feature above is merged and its issue closed.
   - At the Milestone review the user runs `greet.sh --quiet bye Ada` and sees nothing.

   ## Excluded

   - Colour output (`30-colour.md`).
   - Translations.

   ## Boundaries

   - **Budget:** none.
   - Also needs the user's approval: publishing a release to the package registry.
   ```

3. to 8. Label `10-farewell.md`, then link it as a sub-issue of the Milestone issue; label `11-bye-code.md` and `12-bye-usage.md` (they keep their Spec parent); label `20-quiet.md`, then link it as a sub-issue.

Score: 24/24. Questions not covered by the script: none. Report: "Next is Startup verification, which has not run here yet; delivery starts only once its result on the Milestone issue reads Verdict: ready." No Release label and no thread were proposed.

**`add-feature`.** Step 1 found Milestone 1 open, so the run went to "Adding a feature mid-Milestone". Proposed actions, in order: (1) create the Ticket `50-colour-terminal.md` from the user's scripted plan (green only on a terminal, `--no-color`, a test for both), absorbing `30-colour.md`, labelled `enhancement` only; (2) a comment on `30-colour.md` pointing to it; (3) rewrite the Milestone issue body with a third row, `` `50-colour-terminal.md` Colour the name on a terminal (added 2026-11-02 by the user) | lone Ticket | the name is green only when standard output is a terminal; `--no-color` turns it off; a test covers both ``, every other line unchanged; (4, 5) label `50-colour-terminal.md` and `30-colour.md` with `milestone-1`; (6) link the Ticket as a sub-issue. No `release-0.4.0` label. Score: 17/17. Report: Release 0.4.0 keeps its scope; colour waits for the next Release planning.

Before: the same two cases run on the base's skill text (it said it held only Startup verification and to "go no further"), which writes no Milestone issue and edits none: an empty `proposed-actions.md`, scoring 0/2 on `plan` and 0/2 on `add-feature`. Scorer guards: a copy of the `add-feature` run with `30-colour.md` labelled before the row was in fails 2 checks ("labelled after the Milestone issue lists it", "nothing carries the Milestone label before it is listed"); a copy of the `plan` run that labels `30-colour.md` fails "30-colour never labelled"; a copy of the `add-feature` run whose rewritten body drops the second line of Acceptance fails only "goal, acceptance, exclusions and boundaries unchanged" (the scorer compares each of those sections whole).

Real Milestone issue: Milestone 1 (#396, body as of 2026-11-02T07:46:11Z, label `milestone-1`), `score.py --shape`: 6 of 7 checks pass. Its headings (Goal; Features, in build order; Acceptance; Excluded; Boundaries) are the shape's, in order; the order rule ("one at a time, in this order") comes before the table; Boundaries holds the Budget line and lines beyond it; its mid-Milestone row 10a is marked with its date and who added it, as the shape's added rows are. Migration it needs: its feature table's columns are `# | Piece | Kind | What it changes | Who merges`. Rename `Piece` to `Feature` and add an `Accepted when` column after `Kind`, holding each piece's acceptance criteria in short, from its own issue. `What it changes` and `Who merges` can stay as extra columns. The issue was not edited: this run only names the migration.

Not exercised: a fresh session following the skill (the run was by hand, by the skill's author); the user planning a feature inside the run with `grill-with-docs`, `to-spec` or `to-tickets` (the `plan` features were planned beforehand, and the `add-feature` plan was scripted in one answer); a real tracker; Startup verification and delivery, which follow planning, including the delivery gate (a `not ready` verdict, a rerun, a go-on recorded on the Milestone issue: live #396 reads `not ready` now with no go-on recorded) and the delivery branches the `deliver` entry above lists as not exercised.
Pass: yes for both cases, as a by-hand run. Lessons: labelling the issues a feature absorbs was unclear in the first draft ("its Tickets or related issues"); the skill now says every open issue the feature holds, its own, its Tickets, the issues it absorbs or its related issues. A rerun by a fresh premium-tier session is the next evidence to get.
