# Results

One entry per build-flow check of `implement`, newest first. Rerun when a pull request changes how `implement` behaves, as the [evals guide](../../docs/dev-skills/evals.md) says, and record the commit and the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`. An entry written inside an open pull request names the commit and plugin version it ran on as its base; anything that happens after the entry's last commit (later Rounds, merges, the merge itself) is recorded on the pull request, not in the file.

## Template

Every new entry records its run level (see [Run level](README.md#run-level)); earlier entries have no such line and are not rewritten.

```
### <date>, commit <sha>, dev-skills <version>

Run level: decision-level in a subagent | full build-flow in a top-level session
Setup: <repo, origin, tracker, ticket>
Steps: <what each step of SKILL.md did, step by step>
Not exercised: <paths of the skill this run did not reach>
Pass: yes | no. Lessons: <what to change in implement, if anything>
```

## Runs

### 2026-11-04, branch `claude/project-thread-bryult` at `dde4766`, base main `91a35d3`, dev-skills 0.78.0 (no bump): #671 main-check case

Run level: decision-level in a subagent
Setup: the [main-check case](README.md#main-check-check) (`main-check/make_fixture.py <out-dir> fixed|valid`), one fresh regular-tier subagent per scenario per skill version, all in one parallel batch, each given the `implement` folder (the branch's at `dde4766`, or a `git archive` of `origin/main` at `91a35d3`) and `PROMPT.md` only, scored with `score.py`. Driven by the Ticket thread. Evidence: [`evidence/671/`](evidence/671/), one folder per run with `answer.md` and `score.txt`; run directory paths read `<runs>`.
Case check: two fresh premium-tier checks. The first returned keep for `valid` and fix for `fixed`: the Ticket asks for the fix "with a test" and pull request 7 fixed only `src/greet.sh`, so under the skill it read as changed scope; pull request 7 now also adds the usage-line test, and the self-test checks it. The second returned keep.
Steps: step 1 to the Implementer's start, one run per scenario per version.

| Run | Scorer |
| --- | --- |
| branch, `fixed` | 7/7: no branch, no brief; "Ticket 40 is already fixed on main", naming `src/greet.sh`, `test.sh`, commit `30b2f0b` and pull request 7, asking the coordinator to close it as completed; stopped |
| branch, `valid` | 7/7: worktree with `-b ticket-40-usage-typo origin/main`, pushed; Implementer briefed; building |
| main, `fixed` | 6/7, FAIL thread (`waiting`, not `stopped`): it also fetched, found pull request 7 and made no branch or brief, but asked the coordinator to confirm whether to close the ticket and waited for the answer |
| main, `valid` | 7/7: the same build as the branch |

Not exercised: the changed-scope and cannot-tell verdicts, a re-entry after the coordinator's answer, the coordinator's close, and a full build-flow run. One run per scenario and version, no variance estimate.
Pass: yes for the branch. Main's `fixed` run fails only on the end state: on this small fixture main's model already noticed the fix and built nothing, so what the change moves is the outcome, not the noticing. With no rule for this case, main asks and waits; the branch reports the evidence the close needs and stops. Lessons: a fixture where the fix is harder to see (a different file, or no merged pull request record) would test whether main notices at all; not needed for this change.

### 2026-11-04, base main `5edb3e2`, candidate `ticket-631` at `dcb0492`, dev-skills 0.63.0 (no bump): #631 eval-test case, tests for instructions to an agent

Run level: decision-level in a subagent
Setup: the eval-test builder (`make_fixture.py`), one fresh regular-tier subagent per skill version and flow (`ticket`, `spec`), each given `PROMPT.md` and its fixture only and scored with `score.py`. Candidate skills as archived from `ticket-631` at `dcb0492`; the candidate runs were repeated there, with rebuilt fixtures and fresh subagents, after the case-check and ticket-check edits to the briefs and the `tdd` line, and the first candidate runs (at `2c55b43`) also passed; base skills from a `git archive` of `origin/main` at `5edb3e2`.
Steps: scored by the scorer's seven lines per run.

| Run | Plan | Scorer |
| --- | --- | --- |
| candidate, ticket | TEST eval; BASELINE main's version; SEAM-CONFIRMED-BY me; EVIDENCE the eval run on both versions and their scores | all 7 PASS |
| candidate, spec | the same | all 7 PASS |
| main, ticket | TEST eval; BASELINE main's skill; SEAM-CONFIRMED-BY user ("proposed to the Ticket thread for the user to confirm before my first test"); EVIDENCE "the eval failing on main's skill and passing on the changed skill" | FAIL on seam (the Implementer chose the seam, not the user) and on evidence (names the eval run or a stated gap); the other lines PASS |
| main, spec | the same two lines | the same two lines FAIL (seam: user; evidence without run or gap wording); the others PASS |

Case check: two premium-tier case checks. The first returned fix (the seam line of the prompt leaked the rule and could not tell the versions apart; the scorer's word lists were too narrow; the README's expected result for main was loose); all three were applied in the commit before this entry. The second returned keep, noting that EVIDENCE alone is weak on main, that BASELINE accepts a leading "none", and that TEST may not fail on main because a main agent may pick an eval anyway.
Not exercised: the choice between an eval and a sentence grep. TEST passed on main's runs (an agent given criteria about agent behaviour chose an eval anyway), so this case does not show that choice changing between versions. Also not exercised: building a skill-text Ticket for real (the plan is the only output) and the Ticket thread writing the brief from the skill.
Pass: partial. Green on the candidate in both flows; red on main on SEAM and EVIDENCE only. Criterion 3's TEST change (grep to eval) is a stated gap: main's Implementer chose an eval anyway, so the case does not show that choice changing. Lessons: add a Ticket whose acceptance criteria make a sentence grep tempting if the eval-versus-grep choice itself is to be tested; tighten BASELINE so a leading "none" fails.

### 2026-11-04, commit `0027423` (`ticket-638`), dev-skills 0.61.0 (no bump): #638 merge-authority and corrective-check decisions, ticket flow

Run level: decision-level in a subagent
Setup: the merge-authority builder, `ticket` flow, one case per fresh regular-tier subagent, with the skills from a `git archive` copy of `0027423` with `evals/` removed. The subagents could not start subagents. For the six merge-authority cases each was told that every step before the merge step was done and the review was ready to merge. The three corrective-check cases got `DECISION.md`. Evidence: [`evidence/638/`](evidence/638/), one folder per case with the prompt it was given and its `decision.md`. In the copied evidence, the run directory's path reads `<runs>`, so that the `vendor-model` check in `scripts/check-plugin.sh` passes.
Steps: each answer was scored by hand against its case's Expected line (the six) or the README's corrective-check table (the three).

| Case | Outcome | Matches |
| --- | --- | --- |
| `no-milestone` | agent merge; no bump (no release doc), no number asked; `Agent-merged rules: docs/dev-skills/adr/0001-greetings-go-to-stdout.md` in the body and the report | yes |
| `inside-deep-adr` | agent merge; asks the coordinator for `0.4.0`; `chore(release): 0.4.0` changing only `VERSION` as the last commit before the squash; the same `Agent-merged rules:` line | yes |
| `inside-boundary` | handed to the user, not merged, naming "delete production or customer data" from the Boundary record and the one-way Door; no bump | yes |
| `outside-boundary` | the same, with the Boundary record applied as written; Deep and the ADR not named as the reason | yes |
| `no-record-twoway` | agent merge on the empty record; two-way Door; the same `Agent-merged rules:` line | yes |
| `no-record-oneway` | handed to the user: the empty record allows no irreversible action, so the one-way production deletion stops it | yes |
| `retro-inside`, `retro-outside`, `unrelated-no-issue` | a design answer would be recorded as a comment on pull request 1 (it builds no issue); the boundaries are the Boundary record's only; the thread squash-merges, with `Agent-merged rules: REVIEW.md` | yes, all three |

No run named a Milestone issue as a source of boundaries. Where one mentioned the Milestone, it said the Milestone issue holds none.
Not exercised: steps 1 to 6 (Implementer, reviewers), the real bump commit and the real merge. The bump and merge are stated, not made.
Pass: yes, decision-level. Lessons: none for #638.

### 2026-11-04, branch `ticket-638` off `006570d` (the Spec branch, claude/project-thread-28offd), dev-skills 0.61.0 (no bump): #638 no Milestone-issue boundaries, model runs owed

Changed: step 7 (and `implement-spec` step 8) reads only the Boundary record; a Milestone issue holds no boundaries of its own, and the retro check's merge no longer reads its `Retro origin` issue's labels. The fixture's Boundary record lost its "Milestone issues" section and its Milestone issue its `## Boundaries` section; the Expected lines for `no-milestone` and `outside-boundary` and the corrective-check table now say the record applies as written.

Checked: `bash evals/implement/merge-authority/test-fixture.sh` gains two fixture checks and one skill check (neither build skill names a Milestone issue's own boundaries or a Milestone-issue test); the skill check fails on the base's `implement` text (2 hits) and the whole script passes after, for both flows.

Not exercised here: everything a model run covers. The model runs, owed when this entry was written, are in the entry above (`0027423`).

Pass: n/a (a fixture check; model runs owed). Lessons: none yet.

### 2026-11-03, base d4e71bb (the Spec branch, claude/project-thread-0vecgo), dev-skills 0.52.0 (no bump): #573 one merge rule, model runs owed

Changed cases (fixture builder `make-fixture.sh`, `ticket` flow): `no-milestone` (now an agent merge with the `Agent-merged rules:` line), `inside-deep-adr` (new line name), `outside-boundary`, `no-record-twoway` and `no-record-oneway` (new), and the corrective-check cases `retro-inside`, `retro-outside` and `unrelated-no-issue` (all three now merge by the one rule; the Retro origin issue's labels decide only whether a Milestone issue applies). `inside-boundary` is unchanged.

Checked: `bash evals/implement/merge-authority/test-fixture.sh` failed before the skill and builder edits (new cases unknown, old `Milestone review:` line and hand-over Expected for `no-milestone`) and passes after, for both flows. Desk check, by the #573 Implementer, who wrote the step 7 text: each case's fixture read against the new step 7 gives the Expected line (empty record when `boundaries.md` is absent; Milestone issue read only when the ticket carries `milestone-1`; Deep and the ADR change never stop a merge; one-way Door with the deletion unallowed by the record, or by an empty one, goes to the user).

Owed: one fresh regular-tier model run of each changed case. It could not happen here: the session has no subagent tool, and starting a separate `claude -p` session to act as the thread was refused by the environment's permission classifier. Run each case per the README (decision-level is enough) and record it above this entry. The Spec pull request merges with these runs still owed, so they are a follow-up after the merge.

Not exercised: everything a model run covers; steps 1 to 6 and the real bump commit and merge in any case.

Pass: n/a (a desk check; model runs owed). Lessons: none yet. The `implement-spec` flow of the same fixture still expects the old skill text until #574 changes `implement-spec`, so its merge-authority runs are not valid until then. [Note: #574 has since landed on the Spec branch, so the spec flow is valid.]

### 2026-11-02, base 1756497f83c5c897abef05db6e192d2cb51d8382, dev-skills 0.43.0: #476 corrective-check membership, red/green decisions

Setup: extended shared merge-authority fixture, `ticket` flow, no forge or CI. The coordinator ran one fresh regular-tier decision subagent against unchanged main skills for the inside case, then a different fresh regular-tier decision subagent against the candidate skills committed with this entry for all three green cases. Thus green has two fresh agents across both build flows, each seeing its own three cases; cases within a flow are not isolated from each other. Prompts came from DECISION.md; agents read the real skills and tracker fixtures, without this README's scoring table. No full Review was delegated.

Red observed: Review outside because the check builds no issue; design Findings go to the user and rebuttals are unavailable. The build retro merge rule instead selects inside from originating Ticket 10's `milestone-1` label, allows the thread to squash-merge the two-way REVIEW.md change and lists it for Milestone review. The first convergence failure still parks attempt 1 on the check PR, with no restart. This reproduces the membership disagreement through actual agent decisions. The red fixture lacked comment/Park tracker operations; these were added before green, so red is decision evidence only.

Green observed (fresh agent's actual decisions, scored against the fixed acceptance expectations):

| Case | Review / merge membership and source | Design / rebuttals | Clean check / first failed attempt |
| --- | --- | --- | --- |
| retro-inside | both `milestone-1`; `.scratch/issues/10-work.md` (Ticket) | premium-tier agent answers within agreement, recorded on origin; eligible rebuttals | thread squash-merges REVIEW.md; lists file and agent answers for Milestone review; failure parks attempt 1 on PR, no restart |
| retro-outside | both outside; same origin Ticket | user answers; no rebuttals | REVIEW.md goes to user; failure parks attempt 1 on PR, no restart |
| unrelated-no-issue | both outside; source none despite incidental reference to labelled work issue | user answers; no rebuttals | REVIEW.md goes to user; failure parks attempt 1 on PR, no restart |

The green agent also selected the `Milestone:` membership/source record and the current-origin/label reread before merge, comparing with the last Round; a change returns to Review without extra budget. Origin attempt history was not imported.

Checks: expanded merge-authority fixture integrity passes all six cases in both flows; `claude plugin validate .`, `bash scripts/check-plugin.sh`, and all 15 disposable packaging tests (`python3 scripts/test-check-plugin.py`) pass. Existing restart and Spec park fixture checks were attempted but their builders stop on macOS BSD `sed -i` (`undefined label`); those separate lifecycle checks are not reported as passed.

Not exercised: actual Finders, Verifiers, design-answer agents or rebuttal decisions; actual Round/answer/attempt comments and park writes; the changed-membership branch as a separate fixture; CI, bump, integration, merge, coordinator callbacks and full build/retro lifecycle. These are bounded decision-level red/green runs, not full execution proof. No new skill dependency was introduced. Not visual; Door: two-way (reverting this text/fixture change undoes it).

Pass: yes for all three membership/merge/first-failure decisions in this flow. Version is the base version, unchanged during review.

### 2026-11-02, ticket-443 after Ticket check 1, dev-skills 0.29.0: carry-over commands, desk check by hand, not a build-flow run

Setup: two scratch git repos outside this repo, run by hand by the Implementer of #443, testing the carry-over commands `implement-spec` step 7 now names (the `implement` split-off uses the same diff).
Steps: shared file: Tickets A and B each changed one line of `f.md` on the Spec branch. Carrying each over with `git diff --no-renames main...spec -- <its files> | git apply --3way` gave "Applied patch to 'f.md' cleanly" twice, but A's commit held both tickets' lines and B's commit failed with nothing staged ("On branch fresh"; the fresh branch had only A). So the rule now keeps a ticket only when no other landed ticket changed its files, and A and B are both rebuilt. Rename: Ticket A ran `git mv old.md new.md` and edited it. `git show --name-only <A>` printed the commit header and listed only `new.md`; `git show --no-renames --name-only --format= <A>` listed `new.md` and `old.md`; the path-limited `--no-renames` diff carried over to a fresh branch from main gave `old.md => new.md | 1 +`, with `old.md` gone from the tree.
Not exercised: the skill text by an agent; the scratch repos stand in for a Spec branch and its attempt head.
Pass: yes. Lessons: the earlier rule (no ticket that is not kept shares a file) let two kept tickets share a file, and `git show --name-only` dropped a rename's old path; both fixed in `implement-spec` step 7, ADR 0005 and the glossary.

### 2026-11-02, commit cade37e (base 76f2239 plus the ticket-443 commits), dev-skills 0.29.0: restart check `inside`, decision-level run of the end of step 6

Setup: the restart fixture, `restart/make-fixture.sh <dir> inside`, built in a scratch directory outside this repo (bare origin, local Markdown tracker, no forge, no CI; Ticket labelled `milestone-1`, pull request 1 open with Rounds 1 to 3, Round 3 `attempt ended: restart (a Finding returned)`, attempt record 1 on the Ticket with `Untouched: docs/adr/0001-greetings-go-to-stdout.md, docs/usage.md`). Driven by the Implementer of #443, which had no Agent tool: one fresh headless `claude -p` session on the premium tier, given only the PROMPT.md text with `<checkout>` set to a `git archive` copy of the branch at cade37e, tools limited to file reads and edits and read-only git.
Steps: restart handled without asking the user: pull request 1 set `State: closed` with a comment linking attempt record 1, `ticket-10` left on origin; of the Untouched files, `docs/usage.md` split off (it documents the existing `hello`) and the ADR 0001 line kept with the rebuild (it describes `bye`); split-off branch `ticket-10-usage` off `origin/main`, a new Implementer briefed word for word to bring the file over with `git diff origin/main...<attempt head> -- docs/usage.md`; pull request 2 names the Ticket and the record, closes nothing, supposed merged, no retro of its own; then a fresh branch `ticket-10-attempt-2` off main after the split-off, a new Implementer briefed with the record's row, Tried and Lesson and the closed pull request (read, not copied); pull request 3 closes the Ticket, links pull request 1 and the record, Review from Round 1. No message about the restart. On the planted `park`: pull request 3 left open, not brought to the user as a merge decision; `parked` on the Ticket's `Labels:` line with a comment listing both attempt records and pull requests 1 and 3; one message to the user (1 in all); no second restart; no retro.
Not exercised: steps 1 to 5 and the Implementers, reviewers and Rounds themselves; the real branches, worktrees, commits and merge (the session named them and changed only tracker files); attempt record 2's content (not given, so the message left its cause and lesson as slots).
Pass: yes (matched the case's Expected line). Lessons: none for the skill. Before the change (a red run on base 76f2239, same fixture, same driving), the session said "the `implement` skill in this checkout has no step for the `restart` outcome" and improvised the rebuild from `agentic-review`'s wording: it reached a similar plan, but nothing in `implement` directed it (no close-with-link, split-off or Round-1 rule to follow), so that run counts as a fail of the check.

### 2026-11-02, commit cade37e (base 76f2239 plus the ticket-443 commits), dev-skills 0.29.0: restart check `outside`, decision-level run of the end of step 6

Setup: the restart fixture, `restart/make-fixture.sh <dir> outside` (no Milestone label, pull request 1 at Round 5 with `5-Round cap reached` and R3-1 open, no attempt record), driven as the `inside` run above.
Steps: no `restart` or `park` outcome, and the Ticket has no label in the record's form, so outside a Milestone; step 7's outside list: the Result `5-Round cap reached` (with R3-1 named) and the ADR 0001 change stop the merge; pull request 1 brought to the user in one message, left open; no file changed, no close, split-off, rebuild, attempt record or `parked` label.
Not exercised: steps 1 to 5, the merge itself.
Pass: yes (today's behaviour, as the Expected line says).

### 2026-11-01, commit e0b1ecf (base) plus the ticket-423 working tree, dev-skills 0.26.0: merge-authority `inside-boundary`, decision-level run of step 7

Setup: the merge-authority fixture, `make-fixture.sh <dir> inside-boundary ticket`, built in a temporary directory outside this repo (bare origin, local Markdown tracker, no forge, no CI). Driven by the Spec thread of #398: one fresh regular-tier subagent, given `implement` from the ticket-423 working tree and told that every step before step 7 was done (Review clean). This is a decision-level run of the merge step (membership, list, decision, words to the user, bump), not a full build-flow run: a subagent cannot start the Implementer and reviewer subagents the earlier steps need.
Steps: membership: the record's form `milestone-<n>`, the ticket labelled `milestone-1`, so inside. Inside list, first bullet: the fixture's `CLAUDE.md` says a merge deploys new migrations, so merging would run `migrations/002_purge_inactive_customers.sql` against production, which is "delete production or customer data", listed in `docs/agents/boundaries.md` as needing approval; Door one-way. Brought to the user, naming the boundary and the record; Deep and the ADR change not given as reasons. No version number asked (no release doc); no `Milestone review:` line (not merging).
Not exercised: steps 1 to 6 (the Implementer, evidence, pull request and Review), and the real bump commit and merge; the subagent said what it would do and changed no branch.
Pass: yes (matched the case's Expected line). Lessons (unclear points the subagent reported, notes for later; the skill is unchanged for them): the numbered merge procedure (steps 1 to 3 of step 7) can read as if it applied only to the merge-yourself path; the skill does not say whether to judge a migration by its effect at deploy time or by the action the pull request itself takes (it used the effect); with no release doc, it does not say whether to tell the user that no bump was made.

### 2026-11-01, commit e0b1ecf (base) plus the ticket-423 working tree, dev-skills 0.26.0: merge-authority `inside-deep-adr`, decision-level run of step 7

Setup: the merge-authority fixture, `make-fixture.sh <dir> inside-deep-adr ticket`, built in a temporary directory outside this repo (bare origin, local Markdown tracker, no forge, no CI). Driven by the Spec thread of #398: one fresh regular-tier subagent, given `implement` from the ticket-423 working tree and told that every step before step 7 was done (Review clean). This is a decision-level run of the merge step (membership, list, decision, words to the user, bump), not a full build-flow run: a subagent cannot start the Implementer and reviewer subagents the earlier steps need.
Steps: membership: ticket labelled `milestone-1`, which matches the record's form; the Milestone issue carries it too and adds "sending any message to customers" as needing approval, not taken here. So inside. No boundary crossed (no migration, Door two-way), no repo rule naming a person merger, clean Review, no late design answer; Deep and the ADR change do not stop it: agent merge. Bump: the release doc says pull requests bump and `src/greet.sh` changed, so it asks the coordinator (`0.4.0`) and has the Implementer add `chore(release): 0.4.0`, changing only `VERSION` (0.3.0 to 0.4.0), as the last commit; then fetch main, merge main in if needed, rerun `bash test.sh`. `Milestone review: docs/adr/0001-greetings-go-to-stdout.md` added to the body before the merge, so it rides the squash message, and named in the step 8 report.
Not exercised: steps 1 to 6 (the Implementer, evidence, pull request and Review), and the real bump commit and merge; the subagent said what it would do and changed no branch.
Pass: yes (matched the case's Expected line). Lessons (unclear points the subagent reported, notes for later; the skill is unchanged for them): the order of the `Milestone review:` line, the bump and saving the body for the commit message is only implied; the skill speaks in `gh pr` terms, so a local Markdown tracker needs mapping (the merge command has no tracker-doc equivalent); "Deep depth alone does not stop the merge" is easy to skim past before its ADR clause.

### 2026-11-01, commit e0b1ecf (base) plus the ticket-423 working tree, dev-skills 0.26.0: merge-authority `no-milestone`, decision-level run of step 7

Setup: the merge-authority fixture, `make-fixture.sh <dir> no-milestone ticket`, built in a temporary directory outside this repo (bare origin, local Markdown tracker, no forge, no CI). Driven by the Spec thread of #398: one fresh regular-tier subagent, given `implement` from the ticket-423 working tree and told that every step before step 7 was done (Review clean). This is a decision-level run of the merge step (membership, list, decision, words to the user, bump), not a full build-flow run: a subagent cannot start the Implementer and reviewer subagents the earlier steps need.
Steps: membership: ticket labelled `enhancement` only (`milestone-1` is on the Milestone issue, not the ticket), so outside. Outside list: Deep and the ADR 0001 change hold; Door two-way. Brought to the user, naming both. No release doc, so no version asked and the bump skipped; no `Milestone review:` line.
Not exercised: steps 1 to 6 (the Implementer, evidence, pull request and Review), and the real bump commit and merge; the subagent said what it would do and changed no branch.
Pass: yes (matched the case's Expected line). Lessons (unclear points the subagent reported, notes for later; the skill is unchanged for them): the skill is silent on a ticket that belongs to the Milestone in theme but has no label (it followed the label rule strictly); "Deep alone does not stop the merge" appears only in the inside form, an asymmetry easy to misread; step 7.1 on the user-merges path is awkward when the bump is skipped; no release doc was read as skip.

### 2026-11-01, commit e0b1ecf (base) plus the ticket-423 working tree, dev-skills 0.26.0: merge-authority desk check, not a build-flow run

Driven by hand by the #423 Implementer, who wrote the step 7 text under test; no fresh session or subagent ran, and no thread, Review or merge happened. For each case of the merge-authority check ([README](README.md#merge-authority-check)) the fixture was built with `make-fixture.sh <dir> <case> ticket` and the edited step 7 was read against its files, writing down the decision the text gives.

- **`no-milestone`:** the Boundary record names the form `milestone-<n>`; the work issue's labels (`enhancement`) hold none, so outside a Milestone. The outside list, unchanged word for word from main (checked with a diff of the bullets), holds on Deep and on the ADR 0001 change: brought to the user, naming both. No release doc, so no bump.
- **`inside-deep-adr`:** the work issue carries `milestone-1`; the Milestone issue `00-milestone.md` carries it too and adds one approval action (messages to customers), which the change does not take. No action needing approval, Door two-way, no repo rule naming a person merger: agent merge. Step 1 then reads the release doc ("pull requests bump", `src/` changed), asks for a number and adds the bump commit; the body gets `Milestone review: docs/adr/0001-greetings-go-to-stdout.md` before the merge, and the step 8 report names it.
- **`inside-boundary`:** inside a Milestone; the fixture's `CLAUDE.md` says a merge runs new migrations against production, so the merge would delete customer rows, the record's "delete production or customer data": brought to the user, naming that boundary and the Boundary record. The ADR change and Deep are not reasons inside a Milestone.

Not exercised: everything a real run does (steps 1 to 6, the Review, the coordinator's answer, the bump commit itself, the merge). The three cases were then run as decision-level runs of the merge step by fresh regular-tier subagents: see the three entries above. Full build-flow runs of the three cases are still to come.

Pass: n/a (a desk check). Lessons: the planted crossing needs the fixture to say the merge itself takes the action (here, deploy on merge); a pull request that only adds a script someone runs later is a weaker plant, since "takes, or its merge would take" may not fire.

### 2026-10-30, commit d183037 (base), dev-skills 0.11.0 (base; the branch under test carries 0.15.0)

Setup: this repo, with a GitHub origin and the GitHub Issues tracker. The input was one real lone Ticket, #34 (regular tier, Standard depth), run by a Ticket thread in a cloud session. The commit and version are main's at the point the Ticket branch was made from; the branch itself bumps the plugin to 0.15.0 (first taken as 0.13.0, then 0.14.0, retaken as main moved).

- **Step 1:** the Ticket and its triage brief were read; no blocking edges; the tier (regular) came from the brief.
- **Step 2:** the Ticket branch was made from the fetched `origin/main` and pushed before any commit. It was the session's preassigned branch name, not a ticket-named branch.
- **Step 3:** one Implementer on the regular tier, briefed with pointers (the Ticket, the brief, the docs to read).
- **Step 4:** the coordinator reran `check-plugin.sh` and `claude plugin validate .` on the branch head; both passed. The evidence covered every acceptance criterion except the run itself.
- **Step 5:** PR #91 was opened with the `pr` skill's body (Closes #34, Evidence from the Implementer's greps and checks, Door two-way). Requesting the user as reviewer failed, because the user is the PR author on GitHub (the session pushes as them).
- **Step 6:** Round 1 (Standard: standards, spec, adversarial contradictions and bugs-and-edge-cases Finders, one Verifier) raised 14 candidates. The Verifier kept 5 Nits (2 fix, 3 skip), dropped the rest, and found no Important. The same Implementer fixed the 2 fix Nits. Main moved (#86 landed) before Round 2; the same Implementer merged origin/main in (conflicts in `plugin.json` and `PATCHES.md`, both kept; numbers stayed 0.13.0, Patch 22, check 24). Round 2 (fresh Finders: standards, spec, adversarial contradictions and removed behaviour; one Verifier) found no Important and confirmed R1-1 and R1-2 fixed; it kept 3 Nits (1 fix, 2 skip) and dropped 3 plus 5 repeats of Round 1 dismissals. The fix Nit went into a last commit no Round reviewed. Main moved twice more before merge (#84, #94); the second merge had conflicts (`PATCHES.md` and `check-plugin.sh`, both sides kept), and the numbers were retaken as 0.14.0, Patch 23, check 25. Round 3 (fresh Finders: standards, spec, adversarial removed behaviour and contradictions; one Verifier) reviewed cfd895e and the merge's resolutions: no Important, nothing lost from either parent; it kept 2 fix Nits (this stale version, and this sentence), fixed in a last commit no Round reviewed. Main moved a third time (#83) after Round 3; that merge also conflicted and numbers were retaken as 0.15.0, Patch 23, check 26; Round 4 (fresh Finders, same four angles; one Verifier) reviewed the resolutions: no Important; it kept 2 fix Nits (the merge had rewritten main's version bullet in PATCHES.md, and this line), fixed in a last commit no Round reviewed.
- **Steps 7 to 9** (merge, report, Retro) happen after this entry is committed, so their outcome is recorded on issue #34 and its pull request, not in this file.

Not exercised: Round 5, the 5-Round cap, an Important Finding, and steps 7 to 9 (merge or hand-off to the user, the final report and the Retro), since they come after this entry is committed. Also not exercised here: a Ticket with blocking edges, Deep depth, and a local-Markdown tracker.

Pass: yes, through step 6; steps 7 to 9 are recorded on #34 and the PR. Lessons so far: none needing a change to `implement`. The Ticket branch name was the session's preassigned name rather than one naming the Ticket.
