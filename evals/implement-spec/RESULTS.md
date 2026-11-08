# Results

One entry per build-flow check of `implement-spec`, newest first. Rerun when a pull request changes how `implement-spec` behaves, as the [evals guide](../../docs/dev-skills/evals.md) says, and record the commit and the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`. An entry written inside an open pull request names the commit and plugin version it ran on as its base; anything that happens after the entry's last commit (later Rounds, merges, the merge itself) is recorded on the pull request, not in the file.

## Template

Every new entry records its run level, decision-level in a subagent or full build-flow in a top-level session (see [`implement`'s Run level](../implement/README.md#run-level)); earlier entries have no such line and are not rewritten.

```
### <date>, commit <sha>, dev-skills <version>

Run level: decision-level in a subagent | full build-flow in a top-level session
Setup: <repo, origin, tracker, spec and tickets>
Steps: <what each step of SKILL.md did, step by step>
Not exercised: <paths of the skill this run did not reach>
Pass: yes | no. Lessons: <what to change in implement-spec, if anything>
```

## Runs

### 2026-11-08, branch `claude/project-thread-l4rfwp`, base main `293bf5e`, dev-skills 1.0.1 (no bump): #14 squash-check case

Setup: the [squash-check case](README.md#squash-check-check) (`squash-check/make_fixture.py <out-dir> unlanded|landed`), one fresh subagent per scenario per skill version (the branch's `implement-spec` folder, and a `git archive` of `origin/main` at `293bf5e`), each given the folder and `PROMPT.md` only, scored with `score.py`.
Steps: step 6.4 after a chained step 6.3.
Self-test: `python3 evals/implement-spec/squash-check/test_cases.py` passes (reference answers pass, planted wrong ones fail). Not a model run.
Run level: decision-level in a subagent. Tier: regular, one fresh subagent per run, single run each, made by the coordinator and scored with `score.py`.

| Prompt | Scenario | Branch skill | Main skill (`293bf5e`) |
| --- | --- | --- | --- |
| original | `unlanded` | 5/5 PASS (branch text at `37fb7bb`) | 5/5 PASS |
| original | `landed` | 5/5 PASS (`37fb7bb`) | 5/5 PASS |
| redesigned (`7d75a47`: notes say step 6.3 exited 0 with no output, no cue to inspect) | `unlanded` | 5/5 PASS (`37fb7bb`) | 5/5 PASS: main's model inspected the repo, found no squash commit, kept both and redid 6.3 |
| redesigned | `unlanded` | 5/5 PASS (final text, `f81dd4b`) | not rerun |
| redesigned | `landed` | 5/5 PASS (`f81dd4b`) | not rerun |
| redesigned (notes say the chain landed and Ticket 32 has since changed `bye.sh`) | `later` | 5/5 PASS (`f81dd4b`) | 5/5 PASS: main's model also deletes |

Case check: a fresh premium-tier subagent returned keep for both scenarios, with three fixes, applied: the README no longer says `unlanded` separates the branch from main, this entry records the runs, and the scorer accepts a `Next` that begins "Step 6.4 check failed; redo 6.3" (a passing variant is in the self-test).
Not exercised: a squash that landed with a differing file right after step 6.3 (the diff half of the check), main on the redesigned `landed`, a full build-flow run.
Pass: yes, as a regression guard: the case fails no skill version, so it does not separate the branch from main. Lessons: the redesign (one, per the evals guide) did not make main fail, because main's step 1 "landed" definition and step 9 keep rule lead a careful model to the same answer (Retro #702). The real failure was an unchecked `&&` chain in a long thread, which a short fixture cannot reproduce; the rule still adds the explicit check.

### 2026-11-04, main `9d1de32`, dev-skills 0.80.0 (no bump): #695 merge-authority and corrective-check cases, spec flow, through the `merging` load; closing case on main and its case check

Run level: decision-level in a subagent (merge-authority); decision-level in a session (closing)
Setup: (1) the merge-authority builder, `spec` flow, the nine cases, one fresh regular-tier subagent per case in one parallel batch, given the skills from a `git archive` of `origin/main` at `9d1de32` and the prompt text only (the first entry of [`../implement/RESULTS.md`](../implement/RESULTS.md) holds the same nine for the ticket flow). Evidence: [`evidence/695/`](evidence/695/). (2) The closing case, one fresh premium-tier subagent on main's skills, scored with the final `closing/score.py`. Evidence: [`evidence/695-closing/`](evidence/695-closing/); the subagent's write of `report.md` was refused (#694), so the thread wrote its final message there first.
Case check (Spec #626): a fresh premium-tier subagent that did not write the closing case returned **fix**: valid and needed, a regression guard on main's text (the reconcile rule is explicit there, as it was before `merging`), and fixes: the scorer rejected a correct body that notes Ticket #23 stays open (now it tests for a closing keyword followed by `#23` on one line, a bullet or a shared line included), the method and pull-request checks accept their usual variants, and the self-test lacked the rendered-input check (added: prompt, open pull request with four `Closes` lines, four open issues, two landed commits, no Boundary record or release doc). The self-test passes with a planted passing variant. The case is kept as a **regression guard**.
Steps: merge-authority scored by hand as in the `0027423` entry; closing scored by `score.py`.

| Case | Outcome | Matches |
| --- | --- | --- |
| `no-milestone`, `no-record-twoway` | agent merge (a merge commit); the rules line; no bump | yes |
| `inside-deep-adr` | agent merge; asks for `0.4.0`; `chore(release): 0.4.0` changing only `VERSION` as the last commit; the rules line | yes |
| `inside-boundary`, `outside-boundary`, `no-record-oneway` | handed to the user, naming the production-data deletion and the one-way Door | yes |
| `retro-inside`, `retro-outside`, `unrelated-no-issue` | design answer on pull request 1; the Boundary record only; the thread merges with `Agent-merged rules: REVIEW.md` | yes |
| closing, main's skills | 11/11 PASS: body edited before the merge dropping `Closes #23`, merge commit with the typed title, #20, #21 and #22 closed as completed after it, #23 never closed | yes |

Not exercised: steps 1 to 7 and the real merge; the closing case on a branch's skill (no skill change here). Single run per case.
Pass: yes. Lessons: none.

### 2026-11-04, branch `claude/project-thread-bryult` at `dde4766`, base main `91a35d3`, dev-skills 0.78.0 (no bump): #671 main-check case

Run level: decision-level in a subagent. Tier: regular. Fresh subagents, one per scenario per skill version, all in one parallel batch, each given the `implement-spec` folder (the branch's at `dde4766`, or a `git archive` of `origin/main` at `91a35d3`) and `PROMPT.md` only, scored with `score.py`. Driven by the Ticket thread.
Setup: the [main-check case](README.md#main-check-check) (`main-check/make_fixture.py <out-dir> fixed|valid|worker`). Evidence: [`evidence/671/`](evidence/671/), one folder per run with `answer.md` and `score.txt`.
Case check: two fresh premium-tier checks. The first returned keep for `valid` and fix for `fixed` and `worker`: tickets 51 and 52 ask for each script "with a test" and pull request 9 added only the scripts; pull request 9 now adds the matching tests (both in `fixed`, bye only in `worker`), the self-test checks them, and the `valid` scorer no longer fails an incidental "already". The second returned keep, with one fix: the owner record no longer says the owner is reached through the coordinator, which could have led a run to tell the owner only through `Message`.
Steps: step 1 to the first Implementer's start (a Worker: its ticket's), one run per scenario per version.

| Run | Scorer |
| --- | --- |
| branch, `fixed` | 8/8: no Spec branch, worktree or Implementer; "Spec 50 is already fixed on main", naming commit `134bd3a`, pull request 9 and both scripts and tests; stopped |
| branch, `valid` | 7/7: Spec branch made and pushed, worktrees and Implementers for 51 and 52; building |
| branch, `worker` | 10/10: nothing made; the coordinator told Ticket 51 is already fixed (commit `4aaa3f6`, pull request 9, `src/bye.sh`), the owner `spec-thread-50` told the same; stopped |
| main, `fixed` | 7/8, FAIL thread (`waiting`): it found pull request 9 and made nothing, but asked whether pull request 9 counts (by the landed rule neither ticket had landed) and waited |
| main, `valid` | 7/7: the same build as the branch |
| main, `worker` | 9/10, FAIL thread (`waiting`): nothing made, the coordinator and owner told about pull request 9, but it asked the coordinator to confirm and waited |

Not exercised: the changed-scope and cannot-tell verdicts, a Spec only part of whose tickets main has, a re-entry after the coordinator's answer, and a full build-flow run. One run per scenario and version, no variance estimate.
Pass: yes for the branch. Main's `fixed` and `worker` runs fail only on the end state: main's model already noticed the work on main and built nothing, so the change moves the outcome (main asks and waits with no rule for it; the branch reports with evidence and stops), not the noticing. Lessons: none for #671.

### 2026-11-04, commit 01d5c54 (claude/project-thread-nrdyzw) vs main 617d884, dev-skills 0.72.0 (no bump): ticket-branch case, scenario `waiting` (step 9)

Run level: decision-level in a subagent. Tier: regular. Fresh subagents, one per skill version, each given the `implement-spec` folder (the branch's checkout at 01d5c54, or a `git archive` of main 617d884) and the `waiting` prompt only: no scorer or `fixture.json`.
Setup: the [ticket-branch case](README.md#ticket-branch-check), scenario `waiting` (`make_fixture.py <out-dir> waiting`, scored with `score.py`): Ticket 32 landed on `spec-30` with its local `ticket-32` and worktree `wt-32`; Ticket 31 has not landed, waits on the user, and keeps an unpushed commit on `ticket-31` in worktree `wt-31`.
Case check: two fresh premium-tier checks. The first returned fix (no real worktrees in the fixture, scorer forms for deleting `ticket-31`, the Keep check); the second returned fix (backticks, a `Thread:` value in backticks, a trailing aside, prompt wording that tipped the run). Both were fixed, and the final verdict was keep: valid, needed.
Steps: step 9 cleanup, one run per skill version.
- Branch, `waiting`: 9/9.
- Main, `waiting`: 9/9. Its Cleanup was `git worktree remove .../wt-32 && git branch -D ticket-32 && git worktree prune`: it kept `ticket-31`, kept the thread open and named Ticket 31 in the report, because it read step 9 together with steps 6.4 and 3.1 and reasoned that unlanded work stays.
Not exercised: a model that follows main's step 9 ("remove any worktrees left ... and their local Ticket branches") literally; a full build-flow run. Single run per version, no variance estimate.
Pass: yes for the branch. Lessons: the contradiction in main's text is real, but a careful model resolves it from steps 3.1 and 6.4, so `waiting` is a guard scenario, not a discriminating one; the skill fix pins the behaviour in the text.

### 2026-11-04, commit 0d969c8 (claude/project-thread-szfunq) vs main f8760e5, dev-skills 0.68.0 (no bump): ticket-branch case

Run level: decision-level in a subagent. Tier: regular. Fresh subagents, each given the `implement-spec` folder (the branch's checkout, or a `git archive` of main) and the prompt only: no scorer, `fixture.json` or `EXPECTED`. `SKILL.md` has not changed since a9a01db; only `evals/` changed after it.
Setup: the [ticket-branch case](README.md#ticket-branch-check), scenarios `reuse` (a local, never-pushed `ticket-31` holds a wip commit; Ticket 31 has not landed) and `landed` (the pushed `spec-30` also holds Ticket 31's squash commit), each built with `make_fixture.py` and scored with `score.py`.
Case check: a first premium reviewer returned fix (the scorer's evidence and rebase checks); fixed in e50c4bf, and the `landed` scenario was added after. A second fresh premium pass read the cases before the scorer and prompt fixes below and returned fix for `reuse` (the scorer ignored `Cleanup:`) and fix for `landed` (the prompt said "next frontier ticket" and the scorer did not check the Brief); both were fixed in 28a8627 and 0d969c8. The fixed cases were checked by the self-test and by the model reruns on the final prompt and scorer, not by a third premium pass. `landed` is kept as a stated guard scenario that passes on main by design (`reuse` is the discriminating one).
Steps: step 3.1 on re-entry, one run per scenario per skill version. The `reuse` answers were made on a9a01db (branch) and main f8760e5 and re-scored with the final scorer; `landed` was rerun with fresh subagents on 0d969c8 and on main f8760e5, on the final prompt.
- Branch, `reuse`: 10/10.
- Main, `reuse`: 5/10. It ran `git branch -D ticket-31` and then `git worktree add /tmp/wt-31 -b ticket-31 spec-30`, discarding the surviving wip commit and telling the Implementer not to rely on it; main's text says nothing about a leftover branch, and the run said so itself. The scorer reports five failures: the cleanup check (a delete in `Cleanup:`), the reuse decision, no-new-branch, the handoff and the evidence-check.
- Branch, `landed`: 7/7.
- Main, `landed`: 7/7. Main passes because its step 1 already treats a squash commit on the Spec branch as landed, so `landed` does not separate main from the branch (it guards the new text's landed sentence only); `reuse` is the discriminating scenario.
Not exercised: a full build-flow run; a real Implementer; a conflict while merging the Spec tip in. Single run per version, no variance estimate.
Pass: yes for the branch. Lessons: none for the skill.

### 2026-11-04, commits b5b7c0a and ab4c7a4 (claude/project-thread-ypj9u9), dev-skills 0.66.0 (no bump): owner-claim case, branch's and main's skills

Run level: decision-level in a subagent. Tier: regular (fresh subagents).
Setup: `owner-claim/`, one run per skill version, six scenarios plus 4b each. Each subagent got the skill folder, `SPEC.md` and `PROMPT.md` only; `EXPECTED.md` was kept away. The branch's skill was the checkout at `b5b7c0a`; the baseline was a `git archive` of main at `9233e77` (dev-skills 0.66.0 on main; the branch leaves the version as it is).
Case check: a premium-tier reviewer returned fix for scenarios 1 to 4, keep for 5 and drop for 6. All fixes were applied: neutral prompt wording, the second read's result stated, "before step 2", scenario 4b added, the old own-record scenario 6 replaced by a Worker scenario, and the skill gained the "record in force" wording to close a third-thread gap. The post-fix cases were not re-checked by a second premium pass.
Branch run: scenarios 1 to 6 and 4b all pass `EXPECTED.md`. 1 asks the coordinator, stops and posts nothing. 2 posts a record naming T1's before the Spec branch, re-reads and builds. 3 posts before step 2. 4 stops and posts only its own earlier record. 4b asks about T2, not the stopped thread. 5 asks the user, waits and posts no record. 6 (Worker) posts no record.
Main run: 2 fails (builds, posts no record, names none replaced). 3 fails (no record posted). 4b fails (asks which of T2 or the earlier thread is running, and "does not choose by comment order"). 1, 4, 5 and 6 pass by the run's own reasoning ("beyond the skill": it says main has no rule and acts on common sense); it reported that the cases measure nothing about main until the rule exists.
Not exercised: a full build-flow (steps 3 to 9); a real tracker or coordinator.
Rerun after Round 1: the Worker clause in `SKILL.md` step 1 and scenario 6 (T1's comment on the Spec, T1 running) were changed in `ab4c7a4`; the skill text between `b5b7c0a` and `ab4c7a4` differs only by the Worker clause. Scenario 6 got no run on main with the new prompt. The branch was rerun once at `ab4c7a4` (all six scenarios plus 4b, same method, regular tier, fresh subagent, dev-skills 0.66.0): all pass `EXPECTED.md`; scenario 6's Worker skipped the owner-record bullet, posted no record, did not ask whether T1 runs, and built 51 only.
Pass: yes for the branch. Lessons: scenarios 1, 4, 5 and 6 do not separate main from the branch (a careful model stops by common sense); the discriminating scenarios are 2, 3 and 4b. A single run per version, no variance estimate.

### 2026-11-04, commit ad8ab26 (the Spec branch, claude/project-thread-vk76z1), dev-skills 0.62.0 (no bump yet): #643 closing case, branch's and main's skills

**Superseded 2026-11-04 (Ticket #695):** both owed items (the merge-authority cases through step 8's `merging` load, and the premium case check) are done in the first entry of this file.

Run level: decision-level in a session.
Setup: the closing case ran twice, on fresh dry-run fixtures built by `closing/make_fixture.py` into a scratch runs directory (`c-branch`, `c-main`), each a fresh premium-tier subagent given only the prompt text. The branch's skills were a `git archive` of the `plugins/` folder at `ad8ab26`; main's were a `git archive` of `origin/main` at `9367726`.
Score: `closing/score.py` on each run: 11 PASS, 0 FAIL, for both the branch's and main's.
Not exercised: a full build-flow in a top-level session with real tracker writes; steps 1 to 7. Still owed: the merge-authority cases through step 8's new `merging` load, and the premium case check of Spec #626, once it lands.
Pass: yes, decision-level. Lessons: none.

### 2026-11-04, branch `ticket-643` off `fff4fb0` (the Spec branch, claude/project-thread-vk76z1), dev-skills 0.62.0 (no bump): #643 closing case, self-test, model runs recorded above

**Superseded 2026-11-04 (Ticket #695):** the closing case's model runs are the entry above; the merge-authority cases through step 8's `merging` load ran on main 9d1de32 (0.80.0) in the first entry of this file; the premium case check of Spec #626 is in that entry too.

Run level: no model session.
Setup: `python3 evals/implement-spec/closing/test_cases.py`, which builds the fixture with `closing/make_fixture.py` and scores a reference run, ten planted wrong runs and a real-write run.
Score: `OK: 1 case, 12 scored runs`: the reference run passes; every planted wrong run fails on the check it plants (`-v` lists them).
Not exercised: everything a model run covers; the closing case's model runs are recorded in the entry above. Still owed: the premium case check of Spec #626, once it lands, and the merge-authority cases through step 8's new `merging` load.
Pass: n/a (self-test only). Lessons: none yet.

### 2026-11-04, commit `0027423` (`ticket-638`), dev-skills 0.61.0 (no bump): #638 merge-authority and corrective-check decisions, spec flow

Run level: decision-level in a subagent
Setup: the merge-authority builder, `spec` flow, one case per fresh regular-tier subagent, with the skills from a `git archive` copy of `0027423` with `evals/` removed. The subagents could not start subagents. For the six merge-authority cases each was told that every step before the merge step was done and the review was ready to merge. The three corrective-check cases got `DECISION.md`. Evidence: [`evidence/638/`](evidence/638/), one folder per case with the prompt it was given and its `decision.md`. In the copied evidence, the run directory's path reads `<runs>`, so that the `vendor-model` check in `scripts/check-plugin.sh` passes.
Steps: each answer was scored by hand against its case's Expected line (the six) or the README's corrective-check table (the three).

| Case | Outcome | Matches |
| --- | --- | --- |
| `no-milestone` | agent merge; no bump (no release doc), no number asked; `Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md` in the body and the report | yes |
| `inside-deep-adr` | agent merge; asks the coordinator for `0.4.0`; `chore(release): 0.4.0` changing only `VERSION` as the last commit, kept by the merge commit; the same `Agent-merged rules:` line | yes |
| `inside-boundary` | handed to the user, not merged, naming "delete production or customer data" from the Boundary record and the one-way Door; no bump | yes |
| `outside-boundary` | the same, with the Boundary record applied as written; Deep and the ADR not named as the reason | yes |
| `no-record-twoway` | agent merge on the empty record; two-way Door; the same `Agent-merged rules:` line | yes |
| `no-record-oneway` | handed to the user: the empty record allows no irreversible action, so the one-way production deletion stops it | yes |
| `retro-inside`, `retro-outside`, `unrelated-no-issue` | a design answer would be recorded as a comment on pull request 1 (it builds no issue); the boundaries are the Boundary record's only; the thread squash-merges, with `Agent-merged rules: REVIEW.md` | yes, all three |

No run named a Milestone issue as a source of boundaries. Where one mentioned the Milestone, it said the Milestone issue holds none. `unrelated-no-issue` also noted that its pull request lacks a `Retro origin` line; the fixture leaves it out on purpose, and the run did not treat it as a reason to stop.
Not exercised: steps 1 to 6 (Implementer, reviewers), the real bump commit and the real merge. The bump and merge are stated, not made.
Pass: yes, decision-level. Lessons: none for #638.

### 2026-11-03, base 15d9dc740e4a887b858d6c0749be9b4647c4f2bb (the Spec branch, claude/project-thread-0vecgo, after #573), dev-skills 0.52.0 (no bump): #574 one merge rule, model runs owed

**Superseded 2026-11-04 (Ticket #695):** the `spec` flow ran at dev-skills 0.61.0 in the `0027423` entry above (a newer version than this entry's 0.52.0), and again on main 9d1de32 (0.80.0) in the first entry of this file.

Changed cases (shared fixture `make-fixture.sh`, `spec` flow, already built for the new rule by #573): `no-milestone` (now an agent merge with the `Agent-merged rules:` line), `inside-deep-adr` (new line name), `outside-boundary`, `no-record-twoway` and `no-record-oneway` (new), and the corrective-check cases `retro-inside`, `retro-outside` and `unrelated-no-issue` (all three merge by the one rule, membership from the originating Spec deciding only whether a Milestone issue applies). `inside-boundary` is unchanged.

Checked: `bash evals/implement/merge-authority/test-fixture.sh` gained two assertions on the skills under test (both name `Agent-merged rules:`; neither keeps `Milestone review:` or an inside/outside merge list). It failed before the `implement-spec` edit (step 8 to 10 still held the old lists and line name) and passes after, for both flows. Desk check, by the #574 Implementer, who wrote the step 8 text: each case read against the new step 8 gives its Expected line (empty record when `boundaries.md` is absent; Milestone issue read only when the Spec carries `milestone-1`; Deep and the ADR change never stop a merge; any ticket's one-way call makes the Spec pull request one-way, and a deletion the record, or an empty one, does not allow goes to the user).

Owed: one fresh regular-tier model run of each changed case with the `spec` flow. It could not happen here: the session has no subagent tool, and a separate `claude -p` session acting as the thread was refused by the environment's permission classifier in #573's attempt, so it was not retried. Run each case per the README (decision-level is enough) and record it above this entry. The Spec pull request merges with these runs still owed, so they are a follow-up after the merge.

Not exercised: everything a model run covers; steps 1 to 7 and the real bump commit and merge in any case.

Pass: n/a (a desk check; model runs owed). Lessons: none yet.

### 2026-11-02, base 1756497f83c5c897abef05db6e192d2cb51d8382, dev-skills 0.43.0: #476 corrective-check membership, red/green decisions

Setup: extended shared merge-authority fixture, `spec` flow, no forge or CI. The coordinator ran one fresh regular-tier decision subagent against unchanged main skills for the inside case, then a different fresh regular-tier decision subagent against the candidate skills committed with this entry for all three green cases. Thus green has two fresh agents across both build flows, each seeing its own three cases; cases within a flow are not isolated from each other. Prompts came from DECISION.md; agents read the real skills and tracker fixtures, without this README's scoring table. No full Review was delegated.

Red observed: Review outside because the check builds no issue; design Findings go to the user and rebuttals are unavailable. The build retro merge rule instead selects inside from originating Spec 10's `milestone-1` label, allows the thread to squash-merge the two-way REVIEW.md change and lists it for Milestone review. The first convergence failure still parks attempt 1 on the check PR, with no restart. This reproduces the membership disagreement through actual agent decisions. The red fixture lacked comment/Park tracker operations; these were added before green, so red is decision evidence only.

Green observed (fresh agent's actual decisions, scored against the fixed acceptance expectations):

| Case | Review / merge membership and source | Design / rebuttals | Clean check / first failed attempt |
| --- | --- | --- | --- |
| retro-inside | both `milestone-1`; `.scratch/issues/10-work.md` (Spec) | premium-tier agent answers within agreement, recorded on origin; eligible rebuttals | thread squash-merges REVIEW.md; lists file and agent answers for Milestone review; failure parks attempt 1 on PR, no restart |
| retro-outside | both outside; same origin Spec | user answers; no rebuttals | REVIEW.md goes to user; failure parks attempt 1 on PR, no restart |
| unrelated-no-issue | both outside; source none despite incidental reference to labelled work issue | user answers; no rebuttals | REVIEW.md goes to user; failure parks attempt 1 on PR, no restart |

The green agent also selected the `Milestone:` membership/source record and the current-origin/label reread before merge, comparing with the last Round; a change returns to Review without extra budget. Origin attempt history was not imported.

Checks: expanded merge-authority fixture integrity passes all six cases in both flows; `claude plugin validate .`, `bash scripts/check-plugin.sh`, and all 15 disposable packaging tests (`python3 scripts/test-check-plugin.py`) pass. Existing restart and Spec park fixture checks were attempted but their builders stop on macOS BSD `sed -i` (`undefined label`); those separate lifecycle checks are not reported as passed.

Not exercised: actual Finders, Verifiers, design-answer agents or rebuttal decisions; actual Round/answer/attempt comments and park writes; the changed-membership branch as a separate fixture; CI, bump, integration, merge, coordinator callbacks and full build/retro lifecycle. These are bounded decision-level red/green runs, not full execution proof. No new skill dependency was introduced. Not visual; Door: two-way (reverting this text/fixture change undoes it).

Pass: yes for all three membership/merge/first-failure decisions in this flow. Version is the base version, unchanged during review.

### 2026-11-02, commit 2423b9d (the ticket-442 branch), dev-skills 0.29.0: park check `inside`, decision-level run of step 5

Setup: the park fixture ([README](park/README.md)), `park/make-fixture.sh <dir> inside`, built in a scratch directory outside this repo (bare origin, local Markdown tracker with the Park operation, no forge, no CI): a Spec labelled `milestone-1` and three Tickets, 11 planted with two contradicting acceptance criteria, 12 blocked by 11, 13 free. Driven by a headless `claude -p` session at the premium tier (the Implementer had no Agent tool, so the run is a headless session, not a subagent), given `implement-spec` from the checkout and told that steps 1 to 4 were done and that Ticket checks 1 to 3 each kept an Important open on Ticket 11. A decision-level run of step 5: it could not start Implementers or reviewers.
Steps: membership decided as step 8 does (Spec carries `milestone-1`, Milestone issue the same): inside. Parked Ticket 11, did not bring it to the user as a decision. Wrote an attempt record comment on `11-code.md` in the `review-record` shape (`kind=attempt attempt=1`, `Outcome: park`, `Ended by: third Ticket check not clean`, the three checks as Rounds, R3-1 as the open row, Tried with both fix commits, Lesson, Untouched), added `parked` to the `Labels:` line with the tracker doc's Park operation and a second comment linking the history. Told the user once, one message word for word, counting "messages about Ticket 11: 1". Ticket 12 not started (its blocker is open); Ticket 13 goes on through steps 3 to 6; the Spec pull request opens as a draft only when 13 lands and stays a draft with no Rounds; step 9 lists Ticket 11 as waiting without telling it again; no retro.
Not exercised: steps 1 to 4 and 6 to 10 (real Implementers, the real Ticket checks, the draft, the Spec pull request's Rounds, the merge).
Pass: yes (matched the case's Expected line). Lessons (unclear points the session reported): `review-record` said an attempt record goes on the issue the pull request builds, so the Ticket case needed the added line there (since added); the marker's `pr=` and `head=` have no value before the draft opens (it wrote `pr=none` and the short fix commit); Ticket-check ids in `review-record` are `T<ticket>.<check>-<n>`, not the `R<round>-<n>` the scripted prompt used.

### 2026-11-02, commit 2423b9d (the ticket-442 branch), dev-skills 0.29.0: park check `outside`, decision-level run of step 5

Setup: as above, `park/make-fixture.sh <dir> outside`: the Spec labelled `enhancement` only (the Milestone issue holds `milestone-1`, the Spec does not). Driven the same way (headless `claude -p`, premium tier, a fresh session).
Steps: membership: the Spec lacks the label, so outside. Did not park: no `parked` label, no attempt record, no issue file changed. Brought Ticket 11 to the user, one message word for word naming the contradicting criteria, the three failed attempts and the open question (stdout, log file or drop the ticket). Ticket 12 not started; Ticket 13 goes on; the Spec pull request stays a draft with no Rounds, and step 9's report covers the whole Spec; no retro.
Not exercised: as above.
Pass: yes (matched the case's Expected line). Lessons: none new; on this path the skill puts no "once" rule on the message, and the session sent one anyway.

### 2026-11-01, commit e0b1ecf (base) plus the ticket-423 working tree, dev-skills 0.26.0: merge-authority `inside-boundary`, decision-level run of step 8

Setup: the merge-authority fixture, `make-fixture.sh <dir> inside-boundary spec`, built in a temporary directory outside this repo (bare origin, local Markdown tracker, no forge, no CI). Driven by the Spec thread of #398: one fresh regular-tier subagent, given `implement-spec` from the ticket-423 working tree and told that every step before step 8 was done (Review clean). This is a decision-level run of the merge step (membership, list, decision, words to the user, bump), not a full build-flow run: a subagent cannot start the Implementer and reviewer subagents the earlier steps need.
Steps: membership: Spec labelled `milestone-1`, so inside. Brought to the user: the merge deploys `migrations/002_purge_inactive_customers.sql` against `$PROD_DB_URL`, deleting customer rows, which is "delete production or customer data", listed in `docs/agents/boundaries.md` as needing approval and not allowed by the Milestone issue; Door one-way. Deep and the ADR change not counted as reasons. No version asked (no release doc); no `Milestone review:` line (not merging).
Not exercised: steps 1 to 7 (Tickets, ticket checks, the Spec pull request and its Review), and the real bump commit and merge; the subagent said what it would do and changed no branch.
Pass: yes (matched the case's Expected line). Lessons (unclear points the subagent reported, notes for later; the skill is unchanged for them): the `Milestone review:` line and step 9's list are tied to "a merge of yours", so it is not said whether to add them when the user merges; who decides the one-way call when an Implementer reports a data-deleting migration as reversible (it treated it as one-way on the facts); a `VERSION` file with no release doc could mislead.

### 2026-11-01, commit e0b1ecf (base) plus the ticket-423 working tree, dev-skills 0.26.0: merge-authority `inside-deep-adr`, decision-level run of step 8

Setup: the merge-authority fixture, `make-fixture.sh <dir> inside-deep-adr spec`, built in a temporary directory outside this repo (bare origin, local Markdown tracker, no forge, no CI). Driven by the Spec thread of #398: one fresh regular-tier subagent, given `implement-spec` from the ticket-423 working tree and told that every step before step 8 was done (Review clean). This is a decision-level run of the merge step (membership, list, decision, words to the user, bump), not a full build-flow run: a subagent cannot start the Implementer and reviewer subagents the earlier steps need.
Steps: membership: Spec labelled `milestone-1`, so inside; the Milestone issue adds only "sending any message to customers", not taken. No boundary crossed, Door two-way, no repo rule naming a person merger, clean Review, no late design answer; Deep and the ADR change do not stop it: agent merge, with a merge commit titled with the Spec pull request's typed title. Bump: release doc says pull requests bump and the pull request changes `src/`, so it asks the coordinator (`0.4.0`) and an Implementer on the Spec branch adds `chore(release): 0.4.0`, changing only `VERSION` (0.3.0 to 0.4.0), `CHANGELOG.md` untouched; a repeat keeps 0.4.0 while main's `VERSION` is unchanged. `Milestone review: docs/adr/0001-greetings-go-to-stdout.md` added to the body before the merge and named in the step 9 report.
Not exercised: steps 1 to 7 (Tickets, ticket checks, the Spec pull request and its Review), and the real bump commit and merge; the subagent said what it would do and changed no branch.
Pass: yes (matched the case's Expected line). Lessons (unclear points the subagent reported, notes for later; the skill is unchanged for them): step 8 does not say whether the `Milestone review:` line or step 8.1's body edit comes first; whether to name an ADR file whose amendment is trivial (read as yes).

### 2026-11-01, commit e0b1ecf (base) plus the ticket-423 working tree, dev-skills 0.26.0: merge-authority `no-milestone`, decision-level run of step 8

Setup: the merge-authority fixture, `make-fixture.sh <dir> no-milestone spec`, built in a temporary directory outside this repo (bare origin, local Markdown tracker, no forge, no CI). Driven by the Spec thread of #398: one fresh regular-tier subagent, given `implement-spec` from the ticket-423 working tree and told that every step before step 8 was done (Review clean). This is a decision-level run of the merge step (membership, list, decision, words to the user, bump), not a full build-flow run: a subagent cannot start the Implementer and reviewer subagents the earlier steps need.
Steps: membership: Spec labelled `enhancement` only (the Milestone issue has `milestone-1`, the Spec does not), so outside. Outside list: Deep (the Spec asks for it) and the ADR 0001 change hold; Door two-way. Brought to the user, naming both. No release doc, so no version asked and the bump skipped.
Not exercised: steps 1 to 7 (Tickets, ticket checks, the Spec pull request and its Review), and the real bump commit and merge; the subagent said what it would do and changed no branch.
Pass: yes (matched the case's Expected line). Lessons (unclear points the subagent reported, notes for later; the skill is unchanged for them): step 8.1 does not say what to do with a `VERSION` file when there is no release doc (read as skip); on the bring-to-user path, asking the user to say before merging is awkward when step 8.1 has nothing to do; the Milestone check is by label only, with no `Parent:` link considered.

### 2026-11-01, commit e0b1ecf (base) plus the ticket-423 working tree, dev-skills 0.26.0: merge-authority desk check, not a build-flow run

Driven by hand by the #423 Implementer, who wrote the step 8 text under test; no fresh session or subagent ran, and no thread, Review or merge happened. For each case of the merge-authority check ([README](README.md#merge-authority-check)) the fixture was built with `make-fixture.sh <dir> <case> spec` and the edited step 8 was read against its files, writing down the decision the text gives.

- **`no-milestone`:** the Boundary record names the form `milestone-<n>`; the work issue's labels (`enhancement`) hold none, so outside a Milestone. The outside list, unchanged word for word from main (checked with a diff of the bullets), holds on Deep and on the ADR 0001 change: brought to the user, naming both. No release doc, so no bump.
- **`inside-deep-adr`:** the work issue carries `milestone-1`; the Milestone issue `00-milestone.md` carries it too and adds one approval action (messages to customers), which the change does not take. No action needing approval, Door two-way, no repo rule naming a person merger: agent merge. Step 1 then reads the release doc ("pull requests bump", `src/` changed), asks for a number and adds the bump commit; the body gets `Milestone review: docs/adr/0001-greetings-go-to-stdout.md` before the merge, and the step 9 report names it. Only the Spec pull request bumps, and membership comes from the Spec's label alone (its tickets carry none).
- **`inside-boundary`:** inside a Milestone; the fixture's `CLAUDE.md` says a merge runs new migrations against production, so the merge would delete customer rows, the record's "delete production or customer data": brought to the user, naming that boundary and the Boundary record. The ADR change and Deep are not reasons inside a Milestone.

Not exercised: everything a real run does (steps 1 to 7, the ticket checks, the Review, the coordinator's answer, the bump commit itself, the merge). The three cases were then run as decision-level runs of the merge step by fresh regular-tier subagents: see the three entries above. Full build-flow runs of the three cases are still to come.

Pass: n/a (a desk check). Lessons: the planted crossing needs the fixture to say the merge itself takes the action (here, deploy on merge); a pull request that only adds a script someone runs later is a weaker plant, since "takes, or its merge would take" may not fire.

### 2026-10-30, commit 3ba7a42, dev-skills 0.8.0

Setup: a sandbox git repo with a bare local origin. The tracker is local Markdown, with a spec and two independent tickets (01 slugify, 02 initials, both regular tier) in `text.sh`/`test.sh`. The "pull request" was a Markdown file.

- **Step 2:** the Spec branch `spec/text-utils` was pushed.
- **Step 3:** two worktrees were made with `git worktree add <path> -b ticket/NN <spec>`, and two Implementers ran in parallel in the background. Both built test-first (red, then green) and merged the Spec tip before reporting. Ticket branches were never pushed (`git ls-remote` showed only main and the Spec branch throughout).
- Main moved mid-build, with an unrelated README commit.
- **Step 5, ticket checks** (Quick: standards and spec Finders, plus a Verifier when there were candidates). Ticket 01 check 1 was clean. Ticket 02 check 1 kept one Important (`for w in $1` globbed against the cwd) and skipped one Nit. The same Implementer fixed it test-first, and check 2 (fresh reviewers) confirmed it fixed and dismissed two new Nits as skip. Check comments were kept and posted once the draft opened.
- **Step 6:** main was merged into the Spec branch before landing 01. Because the Spec branch had moved, Implementer 01 re-merged the tip (clean). 01 was squash-merged and pushed, its worktree removed, and the draft opened with its evidence. Implementer 02 re-merged the tip and hit add/add conflicts in `text.sh` and `test.sh`, which it resolved after its ticket check. 02 was squash-merged and pushed, the body was updated and the pull request marked ready.
- **Step 7:** Round 1 (Quick) was clean. It had one drift Nit, which the Verifier dropped because it came from main: a Finder had diffed against the thread's stale local `main`. Main moved again before Round 2 and was merged into the Spec branch with no conflict. Round 2 (fresh reviewers) was clean.
- **Step 8:** a merge commit into main (`git merge --no-ff`); main keeps the ticket commits. The tickets were marked done in their files, and the worktrees were pruned.

Not exercised: a third ticket check or bringing a ticket to the user, a blocked ticket waiting on the frontier, the 3-Implementer cap (only 2 tickets), a main-merge conflict on the Spec branch, a Spec pull request Finding fixed by a new Implementer, Deep depth, a real GitHub pull request, and filing Pre-existing Findings.

Pass: yes. Lessons, both now in `SKILL.md`: (1) "fetch main" means `git fetch origin main`, and merges, diffs and comparisons use `origin/main`, never a possibly stale local `main`; (2) conflict resolutions from a ticket's re-merge of the Spec tip (step 6.2) are not seen by its ticket check, and are reviewed by the Spec pull request's Rounds 1 and 2 instead.
