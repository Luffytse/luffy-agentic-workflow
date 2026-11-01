# Changelog

What each version of `dev-skills` brought, newest first. Each pull request that changes a skill bumps the version, and each Release adds one entry here covering everything since the last Release: its goal, the versions it delivered, the issues it shipped, and what a project using the plugin must do when something breaks. Entries up to 0.25.0 are one per version, when only a Release bumped it.

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
