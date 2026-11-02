# Results

One entry per build-flow check of `implement-spec`, newest first. Rerun when `implement-spec` changes, and record the commit and the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`. An entry written inside an open pull request names the commit and plugin version it ran on as its base; anything that happens after the entry's last commit (later Rounds, merges, the merge itself) is recorded on the pull request, not in the file.

## Template

```
### <date>, commit <sha>, dev-skills <version>

Setup: <repo, origin, tracker, spec and tickets>
Steps: <what each step of SKILL.md did, step by step>
Not exercised: <paths of the skill this run did not reach>
Pass: yes | no. Lessons: <what to change in implement-spec, if anything>
```

## Runs

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
