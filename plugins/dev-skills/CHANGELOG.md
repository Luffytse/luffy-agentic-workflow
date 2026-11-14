# Changelog

What each version of `dev-skills` brought, newest first. Each Release adds one entry here covering everything since the last Release: its goal, the version it delivered (older entries list the versions delivered one per skill pull request), the issues it shipped, and what a project using the plugin must do when something breaks. Entries up to 0.25.0 are one per version, when only a Release bumped it.

## Milestone 4 · Release 2 (2026-11-14)

The delivery core of Milestone 4 lands: the `top` tier, Milestone planning along a graph, a short Milestone report, delivery that follows the graph, a trimmed `merging`, `wayfinder` and `to-tickets` near the inherited text, and `implement` and `implement-spec` rebuilt, so `implement-spec` falls under 4,000 words.

Versions: 3.0.0. Commits: 878771e..66f40a5.

- Add a `top` Model tier for planning a feature with the user, and for advice to Release planning on a dependency graph; Milestone planning stays on premium (#166)
- `wayfinder`'s blocking sentence goes back to the inherited words, and `wayfinder` and `to-tickets` stop offering `setup-project` (#170)
- `merging` checks the review record before a merge, follows the repo's own merge method, and loses merge-time steps, old tracker text and the Retro origin input (#178)
- Milestone planning: name the features, plan each in its own session along a dependency graph, and fix them once planning settles (#167)
- Milestone report: one screen of key points first, and the detail trimmed (#168)
- `to-tickets` goes back near the inherited text: the user approves every split, and the rules added on one sighting leave (#171)
- Spec: delivery follows the Milestone's graph: Release planning takes the next slice, the team lead starts whatever is unblocked, and a parked issue never stops the rest (#173), with its Tickets: the Release cut carries nothing over, a parked issue and what waits with it leave the Release, and a hand-closed issue is checked against main (#174); Release planning takes the next slice of the Milestone's graph with the waiting bugs, and lists each entry with its blockers (#175); `team-lead` starts every unblocked entry with no limit, holds the Milestone review gate, resumes an ended worker first, and loses merge-time steps, old records and most of pause (#176)
- A Ticket with a live step lists what the person provides, and planning checks each item before the build starts (#172)
- `implement`: the Ticket thread builds the lone Ticket itself as a trial, an action waits and a decision parks, and the retro only files (#179)
- `implement-spec`: a regular Spec thread, no owner record, nothing deleted before the merge, and a parked Ticket never stops the others (#180)

### What to do

- A project whose release doc bumps the version per pull request, or whose `CLAUDE.md` or `AGENTS.md` holds steps to take just before a merge: `merging` no longer reads or runs a repo's merge-time steps (#178). Run `setup-dev-skills` again, or copy the release doc's "The bump at merge" steps into the agent instructions yourself, so the thread that merges still takes them.
- A project whose coordinator follows instructions `setup-project` assembled: run `setup-project` again, as `team-lead`, `milestone` and `release` changed (#166, #167, #173). Delivery now starts every unblocked Order entry with no thread limit unless the project sets one, the instructions no longer copy merge-time steps, and feature planning threads run on the `top` tier.
- A project with its own tier map: add a `top` entry, or `model-tiers` falls back to its own map for it (#166).

## Milestone 4 · Release 1 (2026-11-14)

The serial base of Milestone 4 lands: this repo develops itself without model evals, the version is bumped once at the Release cut, the docs index and glossary are short, the plugin targets Claude Code only, shared rules are said once, the environment check is this repo's own test, and the Triage batch and Retro planning run with no human.

Versions: 2.0.0. Commits: ae30934..878771e.

- Spec: this repo develops itself without model evals, names the skills it uses, and holds skill files to 4,000 words (#147), with its Tickets: retire the model evals (#148); lower the skill file size limit to 4,000 words (#149)
- Cloud threads load dev-skills once: remove this repo's skills links (#161)
- Bump the plugin version once, at the Release cut; the version hand-out and the Ticket re-read leave this repo's docs (#150)
- Docs index and plugin README: one short line per doc and per skill, and a check on index line length (#187)
- Glossary: Area pages behind a map, each entry a definition that names the skill owning its rule (#188)
- Spec: the plugin targets Claude Code only for now (#151), with its Tickets: remove the Codex packaging and its checks (#152); remove Codex from the worker, tier and writing skills (#153); remove the agent-only label role and `implement-spec`'s continuation for another agent's Tickets (#154)
- Say the docs reading rule once, in the `CLAUDE.md` block `setup-dev-skills` writes (#155)
- The repo labels rule lives in the triage-labels doc beside its table (#156)
- Spec: the environment check is this repo's own test; a project keeps only a plugin version check (#162), with its Tickets: `milestone` keeps only a plugin version check (#163); the worker control probes leave `worker-control` and become this repo's Environment check (#164); the Claude Code reference says how a cloud environment keeps the plugin current (#165)
- Spec: the Triage batch and Retro planning run at a Release end with no human; `retro` only files (#157), with its Tickets: the Triage batch moves into its own file (#158); `retro` only files, a repeated Bug class becomes a Retro issue (#159); Retro planning becomes one unattended sort (#160)

Also merged: the plugin checks run on a self-hosted runner (#133).

### What to do

- A project that runs the plugin in Codex: the plugin no longer ships Codex packaging (`.codex-plugin/`, `agents/openai.yaml`) or the Codex worker reference, so Codex installs stop updating; use Claude Code (#151).
- Run `setup-dev-skills` again: the agent-only label role is gone, so its section leaves `docs/dev-skills/triage-labels.md` (#154); that doc gains the **Repo labels** rule beside its table (#156); the `## Agent skills` block in `CLAUDE.md` or `AGENTS.md` gets its new reading-rule line (#155).
- A project whose coordinator follows instructions `setup-project` assembled: run `setup-project` again, as `team-lead` and `milestone` changed (#162, #157). A Milestone now starts with a plugin version check only; the worker probes of Startup verification are gone from the skills (#162).
- Retro planning and the Triage batch now run unattended at a Release end, with no walk-through for the user (#157).

## Milestone 3 · Release 2 (2026-11-09)

A skill-loading coordinator closes the Milestone issue once the user accepts the Milestone, so Milestone 3's own end runs the cycle cleanly without Lufei stepping in.

Versions: 1.10.0. Commits: 69de11a..ae30934.

- `milestone` closes the Milestone issue once the user accepts it (#78)

## Milestone 3 · Release 1 (2026-11-08)

Deliver all nine Milestone 3 features in one Release, so the agentic cycle runs cleanly end to end, with this project's coordinator instructions rebuilt from the skills at the end.

Versions: 1.3.0, 1.4.0, 1.5.0, 1.6.0, 1.7.0, 1.8.0, 1.9.0. Commits: ec8e87e..69de11a.

- Repo fixes: test runner cache files, eval scorer rewording, re-read close form (#52)
- `merging` checks the Closes line before the merge (#53)
- `review-rounds` briefs review agents by file path (#54)
- `milestone` planning offers set-aside work and fits features planned in parallel (#55)
- `to-tickets` fixes for features planned in parallel (#56)
- Build skills hand over actions the cloud environment refuses (#57)
- Spec: assemble the whole Milestone cycle for coordinators that cannot load skills (#58), with its Tickets: `team-lead` starts `release` to cut or plan, and names `setup-project` for skill-less coordinators (#75); `setup-project` assembles the whole Milestone cycle for coordinators that cannot load skills (#76)
- Re-run `setup-project` for this project's coordinator (#59)
- Startup verification reuses an earlier passing Harness check (#62)

### What to do

- A project whose coordinator cannot load the plugin's skills: run `setup-project` again. `team-lead/DELIVERY-LOOP.md`, which its instructions copied, is gone; `setup-project` now assembles the whole Milestone cycle from `team-lead` and `milestone`, with a source stamp and a stale check (#58).

## Milestone 2 · Release 1 (2026-11-08)

Ship the review-script and `implement-spec` fixes found by other projects that use the plugin, then the `setup-project` delivery loop and the Retro scope line, so the whole of Milestone 2 lands in one Release.

Versions: 1.0.1, 1.0.2, 1.0.3, 1.0.4, 1.1.0, 1.2.0. Commits: f7c34c4..ec8e87e.

- `review-rounds`: `verify` accepts an explained "Nothing found: <why>" Finder report (#13)
- `implement-spec` deletes a Ticket branch only after its squash landed on the Spec branch (#14)
- One Always-check line form in the `REVIEW.md` template, `retro`, `review-record` and the parser, with a warning for a line with no file scope (#15)
- The Verifier brief names a report file, so its verdicts are on disk as the Finders' are (#17)
- `setup-project` gives a coordinator that cannot load the plugin a delivery loop, so Releases and Retro planning still run inside a Milestone (#31)
- Each Retro carries a Scope line (skill, environment or this repo), and a repo's own lessons go to its own tracker (#32)

Also merged: the public repo's first changes after the move: which issue numbers refer to the archive (f2004b5), the dev-skills-only repo clean-up and the install check from the new URL (bb6c3cd, 2d53308, from pull requests of the repo's first copy, ADR 0014), and the recreate recorded in ADR 0014 (#12).

### What to do

- A `REVIEW.md` whose Always-check lines are plain sentences now gets a warning from the review brief run, and each such line applies to every diff. Rewrite each line in the form `` - **<Bug class>** (files: `<glob>`; from <origin>): <what to look for> ``, or `(files: all)` for a line meant for every diff (#15).
- A project whose coordinator cannot load the plugin's skills: run `setup-project` again, so its coordinator instructions carry the delivery loop (#31).

## Move to a public repo (2026-11-05)

`dev-skills` moved to its own repo, `Luffytse/luffy-agentic-workflow`, with a rewritten history (ADR 0014). Bare issue and pull request numbers in text written before the move on 2026-11-05 (ADRs 0001 to 0013, changelog entries before the move entry, eval results and evidence, and the issues moved from the archive, which link their original) refer to the private archive `Luffytse/luffy-dev-skills`; from the move on, a bare number means this repo's issue, and a reference to an archive issue is written in full as `Luffytse/luffy-dev-skills#<n>`. The commits recorded on past Releases' `Commits:` lines are the archive's IDs, which do not resolve here. The marketplace is now `luffy-agentic-workflow`: a project that installed `dev-skills@luffy-dev` adds the new marketplace and installs `dev-skills@luffy-agentic-workflow`. No skill text changed.

Versions: none, the version stays 1.0.0.

## 1.0.0 (2026-11-04)

The user declared `dev-skills` stable at the end of Milestone 1 (#396): the autonomous Milestone workflow its ten Releases built is 1.0.0. No skill text changes since Milestone 1 · Release 10.

Versions: 1.0.0.

- Version 1.0.0 (#396)

From 1.0.0 on, a breaking change bumps the major version (ADR 0008).

## Milestone 1 · Release 10 (2026-11-04)

The final Release of Milestone 1: build threads confirm their issue still holds on main, setup records repo labels that triage and planning apply, Finders share one report format with the Verifier, already-done issues close as completed, `release` handles carried-over issues, parallel Tickets never edit the same doc lines, and the evals docs and owed eval runs are cleaned up.

Versions: 0.76.0, 0.77.0, 0.78.0, 0.78.1, 0.78.2, 0.79.0, 0.80.0. Commits: 0867a6b..3310320.

- Finders follow one standard report format, shared with the Verifier, and write their own report file (#675, absorbs #674)
- Done work is closed as completed, never as not planned, so its dependents unblock (#680)
- `setup-dev-skills` records repo labels that `triage`, `to-spec`, `to-tickets` and `review-rounds` apply (#690: #691, #692)
- Tickets that build in parallel never edit the same doc lines (#656)
- `release` cuts a fully carried-over Release and gives every carried-over issue a place (#686, absorbs #685)
- Build threads confirm their issue is still true on main before writing code (#671)
- Evals docs: fixture issues carry a claim test, and a run returns its report when it cannot write the file (#681, absorbs #683)
- The eval runs that merged pull requests left owed are run or closed out (#695)

Also merged: the evals guide's regression-guard rule for a case main already passes, from Retro #702 (#705).

## Milestone 1 · Release 9 (2026-11-04)

Release planning checks every open issue against main, `release` handles its empty and carried-over cases, and the team-lead eval, the Verifier-alone brief and `implement-spec`'s cleanup agree with their own rules.

Versions: 0.72.0, 0.73.0, 0.73.1, 0.74.0, 0.75.0, 0.75.1. Commits: b64f8f9..0867a6b.

- Release planning reads every open issue against main and records a verdict for each before ranking (#670)
- `release` opens no release issue when the ranked list is empty (#652)
- Carried-over issues get a fixed section in the release issue that step 5 reads (#653)
- `team-lead` nudge records go on the worker's issue, and its eval fails only a second notice (#654)
- The Verifier-alone brief carries the meaning of Important and the Skip list (#664)
- `implement-spec` step 9 keeps the Ticket branch of an unlanded waiting ticket (#666)

Also merged: CI runs `scripts/run-tests.sh`, committed by hand (7dc6244).

## Milestone 1 · Release 8 (2026-11-04)

Release planning, merging, and skill testing now follow one agreed path: a version-free, command-free `release` that ranks its picks, one `merging` Base skill, CI and evals that test skill changes, a script that builds the review briefs, and command-free, tracker-neutral skills with shorter descriptions.

Versions: 0.61.0, 0.62.0, 0.63.0, 0.64.0, 0.65.0, 0.66.0, 0.67.0, 0.68.0, 0.69.0, 0.70.0, 0.71.0. Commits: f9e3464..b64f8f9.

- `release` runs one version-free, command-free path with a ranked Release planning; the Triage batch sweeps the backlog, Retro planning and `milestone` mark joining issues `next-release`, and every plan is a Milestone (#633: #634, #635, #636, #637, #638)
- A hidden `merging` Base skill owns the finish of every pull request for `implement`, `implement-spec` and `release` (#641: #642, #643, #644)
- CI, evals and review each cover their own part of skill development: one runner for every deterministic test, the evals guide and ADR 0013, Retro planning acts on a confirmed cheap check at its first sighting, `tdd` names an eval as the test for agent instructions (#626: #627, #628, #629, #630, #631, #632)
- A script builds each review Round's Finder and Verifier briefs, and `review-rounds` runs it (#645: #646, #647, #648, #649)
- `setup-dev-skills`, `retro` and `triage` say what to find or do, never which command to run (#639)
- Local-files tracker text is removed from the skills (#623)
- Skill descriptions are trimmed, with a description-selection eval (#621)
- `implement-spec`'s "Done when" agrees with step 9, and `team-lead` no longer reads a reviewing Spec pull request as finished (#602)
- `implement-spec` records which thread owns a Spec, so a second Spec thread stops or takes over instead of building it too (#608)
- `implement-spec` step 3.1 reuses a Ticket branch a dead thread left (#609)

Also merged: `implement-spec` Continuation moved to its own file (#618, #625).

### What to do

- A project that cuts Releases with `release` reruns `setup-dev-skills` so its release doc carries the versioning policy, Release name, size and cut steps, and so the `next-release` label exists; `release` stops and says so when the release doc lacks them.

## Milestone 1 · Release 7 (2026-11-03)

A Spec whose Tickets belong to different agents (Claude and Codex) can now be planned, built and finished without improvising, and the Implementer evidence gap is closed.

Versions: 0.58.0, 0.59.0, 0.60.0. Commits: eea5f8b..f9e3464.

- `to-tickets` labels a Ticket that needs one agent's native runtime for that agent (#512, absorbs #468)
- `implement-spec` builds mixed-agent Spec Tickets through continuations on the one Spec branch, with an ADR 0005 amendment (#513, absorbs #492)
- ADR and skill now agree on when the Spec pull request is marked ready (#324)
- `implement-spec` says who produces evidence an Implementer cannot (#587, absorbs #470)
- Maintenance fix from the Release 6 Triage batch: the version hand-out scan reads records on pull requests too (#590)

Also merged: `REVIEW.md` says what a review rerun does with an earlier record (#610).

The Release 7 Triage batch and Retro planning are recorded on its release issue (#588).

## Milestone 1 · Release 6 (2026-11-03)

The review and release text now says what threads actually need: gaps Release 5's Retro planning (#581) found in delivered pieces were repaired, and small review and checker defects left from earlier Releases were fixed.

Versions: 0.54.0, 0.55.0, 0.56.0, 0.57.0. Commits: ddf9407..eea5f8b.

- Re-read a status before stating it, in grilling and retro-planning drafts (#350, absorbs #264 and #228)
- `release` shipped test ignores negated closing keywords (#419)
- The vendor-name check catches spaced GPT and o-series names (#435)
- Stale size fact in ADR 0006 (#361)
- The Implementer checks its diff against the review rules and walks a new rule's sequences (#586, absorbs #477 and #482)
- Maintenance fixes from Retro planning #581: the asking thread writes the version hand-out record when the coordinator cannot (#582, absorbs #554); a review Round with nothing to verify skips Verify (#583, absorbs #247); each eval README names the run level its cases need (#584, absorbs #428)

The Release 6 Triage batch and Retro planning (#598) filed no Ticket beyond one repo-docs bug, #590 (the hand-out scan reads issues only), which joins Release 7 as a maintenance fix.

## Milestone 1 · Release 5 (2026-11-03)

Every file the skills require in a repo lives in one `docs/dev-skills/` folder, and one merge rule, read from the Boundary record, applies inside and outside a Milestone. The review itself was rebuilt along the way: a Round 0 sizes it, a `review-rounds` skill runs at most 3 Rounds, and `REVIEW.md` is down to 7 Always check lines.

Versions: 0.50.0, 0.51.0, 0.52.0, 0.53.0. Commits: 1a17cd7..ddf9407.

- Spec: keep the files the skills require in docs/dev-skills/ (#551)
- Move every skill-required file to docs/dev-skills/ in one pull request (#552)
- Same merge and approval rules inside and outside a Milestone (#533), built as Spec #572 with Tickets #573, #574 and #575
- Doc fixes after the move: #332, #392, #427, #412, #413

Also merged: Spec for a small, agentic review with Round 0 and at most 3 Rounds (#555, Tickets #556 and #557); flag any skill file over 5,000 words and record the limit as a boundary (#558); cut REVIEW.md to 7 rules with review levels (#559) and narrow its Quick levels (#568); remove the "Retro planning is due" rule from retro (#570).

The planning approvals were split off to their own issue (#576) and are not in this Release.

## Milestone 1 · Release 4 (2026-11-03)

Milestone delivery moved out of the `milestone` skill into a `team-lead` skill and a `worker-control` skill with Claude Code and Codex references, the Milestone's project instructions were slimmed, and a set of review and Release safeguards were repaired.

Versions: 0.43.0, 0.44.0, 0.45.0, 0.46.0, 0.47.0, 0.48.0, 0.49.0. Commits: 7cc9ca0..1a17cd7.

- setup-project: draft only the project-specific parts once the milestone skill runs the coordinator (Milestone 1, piece C5) (#409)
- Spec: split milestone into Milestone planning, a team-lead skill and harness references (Milestone 1, piece C6) (#523)
- Move this repo's version hand-out and Ticket re-read out of the skills (#526)
- Add the worker-control skill with the Claude Code references and its check (#527)
- Add the Codex reference and check to worker-control (#528)
- Move Milestone delivery into a new team-lead skill (#529)
- Slim milestone to planning, add a feature and the report (#530)
- Maintenance fixes: no-issue retro check membership (#476), logic-resolution depth in a merge-only Round (#479), review ranges with a bump or Nit commit (#480), agreed design changes after the last Round (#481), Park respected in Release scope (#487)

Dropped: #491 and #501 (closed as not planned, replaced by Spec #523); the probes #534, #535 and #536 (answered, closed).

## Milestone 1 · Release 3 (2026-11-02)

The `milestone` skill runs a Milestone end to end: it verifies its runtime at startup, plans and delivers the Milestone's Releases, checks in on and safely takes over silent threads, and writes the Milestone report, so the project's instructions keep only what is specific to the project.

Versions: 0.34.0, 0.35.0, 0.36.0, 0.37.0, 0.38.0, 0.39.0, 0.40.0, 0.41.0, 0.42.0. Commits: ace9974..7cc9ca0.

- to-tickets: scope edges, and splitting a Milestone Spec without waiting, with its membership label (#458)
- A stuck review restarts once, then parks, outside a Milestone too (#448)
- Inside a Milestone, a conflict check after Round 5 gets one extra Round instead of going to the user (#447)
- Spec: startup verification before autonomous delivery (Milestone 1, piece C1) (#405)
- Startup verification: milestone skill, result shape, check-in and worker-state probes in Claude Code (#465)
- Startup verification: confirmed-stop and loaded-skill-version probes in Claude Code (#466)
- Startup verification: run in Codex and record both agents (#467)
- Spec: the milestone skill runs a Milestone from planning to delivery (Milestone 1, piece C2) (#406)
- Milestone skill: planning phase and the Milestone issue (#483)
- Milestone skill: delivery loop, Release grouping, version hand-out (#484)
- Spec: startup verification passes in Claude Code and Codex (Milestone 1, before C3) (#473)
- Startup verification: confirmed stop passes in Claude Code (#474)
- Startup verification: check-ins, confirmed stop and installed skill version pass in Codex (#475)
- Spec: stand-up check-ins and safe takeover of a silent thread (Milestone 1, piece C3) (#407)
- milestone: scheduled check-ins reach the coordinator during delivery (C3, Ticket 1 of #407) (#495)
- milestone: a check-in reads real thread state and nudges a silent thread (C3, Ticket 2 of #407) (#496)
- milestone: confirm a silent thread stopped, then take over or park (C3, Ticket 3 of #407) (#497)
- milestone: pause and resume a Milestone, and resume a parked feature (C3, Ticket 4 of #407) (#498)
- milestone: check-ins and takeover pass in Codex (C3, Codex run of #407) (#499)
- milestone: write the Milestone report for the Milestone review (Milestone 1, piece C4) (#408)

Also merged: extend related-text reviews to repository layout, packaging and contributor descriptions (#355); add an Always-check line for state-machine exits (#489).

## Milestone 1 · Release 2 (2026-11-02)

Agents run the end of a Release inside a Milestone: a stuck review restarts once and then parks, and triage, Retro planning and the next Release's scope run as agent batches, so a Release ends without waiting on the user.

Versions: 0.30.0, 0.31.0, 0.32.0, 0.33.0. Commits: 7d04de2..ace9974.

- Spec: a stuck review restarts once, then parks (Milestone 1, piece B4) (#400)
- agentic-review: detect a stuck review, record the attempt, report restart or park (piece B4, Ticket 1) (#440)
- agentic-review: a premium-tier Verifier judges a fixer's rebuttal (piece B4, Ticket 2) (#441)
- implement, implement-spec: park a stuck pull request or Ticket and tell the user once (piece B4, Ticket 3) (#442)
- implement, implement-spec: restart a stuck pull request once from main (piece B4, Ticket 4) (#443)
- triage: inside a Milestone, agents triage in a Release-end batch (Milestone 1, piece B5) (#401)
- retro-planning: inside a Milestone, agents plan the Retro backlog at Release end (Milestone 1, piece B6) (#403)
- release: inside a Milestone, agents plan the next Release (Milestone 1, piece B7) (#404)

## Milestone 1 · Release 1 (2026-11-02)

Per-PR versions are in place and agents merge inside the Milestone's boundaries, so most later pieces of Milestone 1 need nothing from the user.

Versions: 0.26.0, 0.27.0, 0.28.0, 0.29.0. Commits: bdc7696..7d04de2.

- Per-PR skill versions and sprint Releases in ADR 0008 and CLAUDE.md (Milestone 1, piece 0 + A1) (#391)
- release: cut a Release without a bump pull request when pull requests bump the version (Milestone 1, piece A2) (#397)
- Spec: boundaries and merge authority (Milestone 1, piece B1) (#398)
- Per-PR bumps in the build skills (#398, Ticket 1 of 3) (#421), absorbing #416 and #418
- Boundary record (#398, Ticket 2 of 3) (#422)
- Merge authority inside a Milestone (#398, Ticket 3 of 3) (#423)
- agentic-review: inside a Milestone, a premium-tier agent answers design Findings (Milestone 1, piece B3) (#399)
- Ship the Model tier map in the plugin so any agent can look up its model (#344)

Also merged: a `check-plugin.sh` check that every tracker operation a skill cites is a bold bullet in the tracker doc seed (#434).

## 0.25.0 (2026-11-01)

Give shared rules one authoritative home, while fixing review-completion and release-recovery bugs that could undermine the workflow.

- Plan: focused shared contracts and coherent workflow reuse (#348)
- Establish shared-rule ownership guidance and base-skill support (#363)
- Verify skill loading and application in Codex before consumer migration (#360)
- Extract and migrate the focused docs-index base skill (#364)
- Extract the review-record contract while preserving review and retro workflows (#365)
- Extract the shared issue-absorption contract (#368)
- Delegate retro ticket preparation to the full to-tickets workflow (#369)
- Remove redundant review and project-configuration rules from callers (#366)
- Complete the shared-rules migration and reconcile transition guidance (#370)
- Urgent rerun after a partial first run skips labelling the fix (#325)
- Release step 4 shortcut can post another Release's changelog entry (#326)
- Urgent fix says "patch" but allows a bigger cut, against ADR 0008 (#327)
- Result value conflict for Round 1 (#329)
- fix-Nits commit after a design recount (#330)
- CLAUDE.md: the restatement search covers the file you edited too (#338)
- Retro: Implementer misses parallel sentences inside the file it edits (#328)

Also merged: an optional agent-only label role, for issues meant for one coding agent (#339); `dev-skills` installs in Codex from the `luffy-dev` marketplace, with Codex metadata for every skill and README install steps (#340, #342, #343, #345), and the install checks recorded (#346, #356); ADR 0009, shared rules have one owner skill (#359); repo-local skills load live in Codex and Claude Code (#372); the glossary redefines Milestone as the user-set product goal (#388).

## 0.24.1 (2026-10-31)

The review, release and build skills handle the edge cases that 0.24.0's reviews found.

- filed Pre-existing row stays open (#299)
- Result value not tied to Round 5 not clean (#315)
- The cap is named three ways (#316)
- Release label left by a dropped Release is reused on creation (#301)
- Issue merged before an urgent cut is listed in two changelog entries (#302)
- Release skill label queries count pull requests and are not paginated (#303)
- Release skill "highest version" is not defined as a numeric comparison (#304)
- Release skill: first-Release path says "the one just cut" when nothing was cut (#305)
- Release skill: a rerun of an urgent request opens a second urgent release issue (#306)
- Closed carried-over issue becomes a Release candidate (#312)
- Spec PR closes a dropped ticket as completed (#308)
- Tracker doc Close recipe has no REST form or reason (#309)
- REVIEW.md: a wording edge case that needs a new clause is a Nit unless following the text literally gives a wrong result (#266)

## 0.24.0 (2026-10-31)

The review, build and release skills do what they say: no false-clean Rounds, no Ticket started or left open by mistake, release cuts that cannot go wrong, and clearer history and planning.

- ambiguous match across two open rows (#269)
- partial fix of a Nit not covered (#270)
- line shift undefined for renamed or deleted files (#271)
- held open row has no report path (#272)
- earlier row's lines not brought to this head before a check (#273)
- parallel sentence not updated when the closing rule changed (#274)
- A Spec pull request closes the Spec and every Ticket on merge (#289)
- no command to test the state of a Blocked by body-line blocker (#253)
- build-thread blocker steps name no Count open blockers (#254)
- repo tracker doc lacks the merged-change test for an unblocked ticket (#255)
- Open bump pull request not re-checked on rerun or urgent cut (#277)
- Issue closed as completed read as "the fix has merged" (#278)
- Release skill step 3 and the no-release-issue path disagree with other steps (#279)
- Urgent fix cut can ship below main or jump above a planned Release (#280)
- Release planning: the cap counts features, not issues (#287)
- PR titles and merge commit titles use Conventional Commits prefixes (#288)
- to-tickets: a Ticket that absorbs existing issues reads their comments, links them, and marks each one Absorbed by (#267)
- Review subagents read the Implementer's branch without moving its worktree (#290)
- Say whether a clean fifth Round counts as hitting the 5-Round cap (#291)

Also merged: two `REVIEW.md` Always-check lines, on a command that decides a step but was never run on real data, and on a resume test that equality breaks (#307).

## 0.23.0 (2026-10-31)

Plugin versions change only at a Release, and no pull request takes a number another one could take (ADR 0008).

- Spec: plugin versions change only at a Release (#257)
- Switch-over: no plugin pull request takes a version, Patch or check number (#258)
- Add a release skill and its repo release doc (#259)
- Make the forked skills our own: move into skills/, drop PATCHES.md, credit Upstream in the README (#260)
- Trim check-plugin.sh to named structural checks (#261)
- Watch Upstream every 2 weeks and file one triage issue (#262)

Also merged: three `REVIEW.md` Always-check lines, on glossary-term form and on decisions recorded before their rule change lands (from the retro of ADR 0008's pull request #256), and on a step re-entered with state recorded earlier (#282); the Upstream watch now runs from a reminder issue, not a scheduled task (#285); a comment in the plugin-checks CI workflow was updated (#286).

## 0.22.28 and earlier

Before Releases, every merged change to the plugin bumped its version, so the versions up to 0.22.28 have no entries of their own; the repo's git history records each change and its bump. The versions that brought something new:

- **0.2.0**: skills find docs through one docs index, `docs/index.md`. The plugin started as a fork of Matt Pocock's skills, every one model-invoked.
- **0.4.0**: the review skill runs Find, Verify and Rank in Rounds.
- **0.5.0**: `retro` turns repeated Bug classes into checks.
- **0.6.0**: `to-tickets` gives each Ticket a Model tier, and `setup-project` is offered after tickets or a wayfinding map.
- **0.7.0**: `implement` coordinates one lone Ticket.
- **0.8.0**: `implement-spec` coordinates one Spec.
- **0.9.0**: the review skill is renamed `agentic-review`. A project that named `code-review` must use the new name.
- **0.9.3**: `retro` files its suggestions as Retro issues, and `retro-planning` works through them.
- **0.10.0**: `agentic-review` takes the built-in review's strengths.
- **0.12.0**: the formerly user-only skills get model-facing descriptions.
- **0.13.0**: the setup skill becomes `setup-dev-skills`. A project that called it by its old name must use the new one.
- **0.14.0**: `retro-planning` walks one group at a time.
- **0.15.0**: `grilling` asks at most 3 questions per round.
- **0.17.0**: `agentic-review` counts its reports before moving on.
- **0.19.0**: review subagents experiment only in their own copy, and Implementers confirm each push.
- **0.20.0**: `handoff` saves where the next agent can read it.
- **0.21.0**: `grilling` states a rule's purpose and checks a recommendation's facts.
- **0.22.0**: `agentic-review` returns design Findings to the user as grilling.
- **0.22.1 to 0.22.28**: fixes and clarifications, among them `setup-dev-skills` writing a starter `REVIEW.md` (0.22.11) and the tracker doc's REST routes and fallback forms for blocking and sub-issues (0.22.14 to 0.22.27), and `agentic-review` Rank edge cases (matching per location at one head, raising held Findings, partly fixed rows, Verifier dismissals closing earlier Findings; 0.22.28).
