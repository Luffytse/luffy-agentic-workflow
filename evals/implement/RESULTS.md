# Results

One entry per build-flow check of `implement`, newest first. Rerun when `implement` changes, and record the commit and the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`. An entry written inside an open pull request names the commit and plugin version it ran on as its base; anything that happens after the entry's last commit (later Rounds, merges, the merge itself) is recorded on the pull request, not in the file.

## Template

```
### <date>, commit <sha>, dev-skills <version>

Setup: <repo, origin, tracker, ticket>
Steps: <what each step of SKILL.md did, step by step>
Not exercised: <paths of the skill this run did not reach>
Pass: yes | no. Lessons: <what to change in implement, if anything>
```

## Runs

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
