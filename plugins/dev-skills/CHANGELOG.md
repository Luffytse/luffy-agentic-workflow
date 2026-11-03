# Changelog

What each version of `dev-skills` brought, newest first. Each pull request that changes a skill bumps the version, and each Release adds one entry here covering everything since the last Release: its goal, the versions it delivered, the issues it shipped, and what a project using the plugin must do when something breaks. Entries up to 0.25.0 are one per version, when only a Release bumped it.

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
