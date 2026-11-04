# luffy-dev-skills

A plugin marketplace: the skills coding agents use, packaged so every project and every agent session can load them.

## Packaging

**Marketplace**:
The catalog in this repo (`luffy-dev`) that lists the plugins an agent can install.
_Avoid_: store, registry

**Plugin**:
One installable bundle of skills listed in the Marketplace, turned on as a whole.
_Avoid_: package, extension

**Skill**:
One instruction file (`SKILL.md` plus helper files) that an agent follows for one kind of task.
_Avoid_: command, prompt

**Upstream**:
Matt Pocock's public skills repo (`mattpocock/skills`), where the `dev-skills` skills began. They are our own now; we watch Upstream and take one idea at a time through triage (ADR 0001).
_Avoid_: original, source

**Model tier**:
How strong a model a step needs: **cheap**, **regular**, or **premium**. Each agent maps the tiers to its own models, so a skill names a tier and never a vendor's model. The plugin's default map is the `model-tiers` skill (one column per coding agent); a project's own map overrides it (ADR 0002).
_Avoid_: model size, model class

**Model-invoked skill**:
A Skill the agent may start by itself when a task fits its description. Model reachability is separate from user-menu visibility: `user-invocable: false` can hide it in Claude Code while retaining model access. A **user-only skill** (`disable-model-invocation: true`) starts only when a person types its name.
_Avoid_: auto skill, manual skill

**Shared rule**:
A rule two or more skills must follow the same way, such as a record contract, an invoked workflow's rule or a project configuration rule; independent rules may differ even when their wording matches. This ownership term does not limit consistency review: contradictions within a skill and stale repository descriptions still need fixing. ADR 0009 records the implemented scoped owners and consumers; existing links and unmigrated copies remain in force.
_Avoid_: common rule, duplicated rule

**Base skill**:
A Skill holding a focused Shared rule that consumers load by name without loading a larger workflow for that rule alone. ADR 0009 records the implemented `docs-index`, `review-record`, `issue-absorption` and `worker-control` Base skills, with menu hiding preferred where supported; `merging` (see **Merging**, Spec #641, ADR 0009) is one too; existing rules and consistency protections still govern unmigrated shared copies.
_Avoid_: library skill, helper skill

## Where the skills run

**Project thread**:
One task's Claude session inside a Claude project. A **coordinator** (the project's own Claude) starts each thread with a brief, so nobody types slash commands there; to deliver planned work it runs the **Team lead** skill.
_Avoid_: chat, conversation

## Building

**Spec**:
The written design of one feature: the problem, user stories, decisions, testing and what is out of scope. It is one GitHub issue.
_Avoid_: PRD, design doc

**Ticket**:
One small, end-to-end slice of work, built and reviewed on its own. Either part of a Spec (a sub-issue of it) or a **lone ticket** under no Spec.
_Avoid_: task, story

**Agent label**:
The label of the optional agent-only triage role: it marks an issue for one coding agent only, and a repo maps the role to one label per agent in its `docs/dev-skills/triage-labels.md` (this repo: `claude-only` and `codex-only`). It is neither a category nor a state role. An agent that sees another agent's label does not work the issue; an issue with none can be taken by any agent. `triage` may apply it, and `to-tickets` copies a Spec's onto each of its Tickets; it also gives a Ticket whose acceptance criteria demonstrably require one agent's native runtime that agent's label when the Spec carries none (never one the repo's label doc does not map; a Spec's label for another agent is surfaced, not changed).
_Avoid_: assignee, owner

**Milestone**:
A product goal the user sets (for example "M3 Trip planning"), written down in one Milestone issue: the goal, the features to deliver by its end, in build order, their acceptance criteria and what is excluded. Every plan is a Milestone: a small Release is a one-Release Milestone, planned with defaults for what it does not need (one at a time, nothing excluded). The Milestone issue holds no boundaries or budget of its own: those are the **Boundary record**'s, for every issue (an earlier issue's Boundaries section is history). The `milestone` skill holds only planning, adding a feature, Startup verification and the report: its planning phase writes that issue with the user; agents may propose a feature, never add one. A feature the user plans while a Milestone runs joins it unless the user says it is for the next Milestone: it is planned with the user first, then listed in the issue, then labelled, and the planning thread updates each open Ticket it touches (whole body read, changed, read back, with a note naming the feature); a change to the goal, acceptance or exclusions goes to the user as one question. Delivery starts once planning settles and the latest **Startup verification** result passes, or after a failed one once the user says to go on (recorded on the Milestone issue); the coordinator runs it with the **Team lead** skill, which reads the Milestone issue for the features and their order, and `milestone` reports at its end. It holds one or more Releases, which the agents plan, and it closes when the user accepts it at the Milestone review. An issue belongs to it, and its pull request is **inside the Milestone**, when the issue (for a Spec's pull request, the Spec) carries the Milestone's membership label in the form the **Boundary record** names; the Milestone issue carries the same label. A build thread's no-issue corrective check records `Retro origin: <Ticket or Spec issue link>` in its pull request body; the check's body is its spec. Other no-issue pull requests remain outside. The Tickets split from a Milestone's Spec carry the label too, and `to-tickets` publishes their breakdown without asking the user while it keeps the Spec's scope. A build thread merges its own pull request, inside a Milestone or not, unless it crosses a boundary in the Boundary record or the repo's own rules say a person merges it; membership plays no part in that (ADR 0004). A review stops for the user only when it is **Waiting on a boundary**; after Round 3 what is open is sorted, never brought to the user.
_Avoid_: epic, sprint

**Startup verification**:
The check the `milestone` skill records before a Milestone's autonomous delivery starts, in two parts: the **Worker control** check, which proves in this environment, with short bounded **probes**, that workers start, that a worker's state is read from the **Harness**, that a pause holds, that a stopped worker is confirmed stopped by the Harness's own record (not by silence, a sent stop request or a worker merely idle between turns), that an end or failure wakes the coordinator and that a check-in reaches it; and the loaded-skill-version probe, which proves that a fresh thread loads the plugin version on main. Each passes only on evidence observed afterwards, in the agent that will take that action during delivery. The result, with the runtime's permission and sandbox settings, is one comment on the Milestone issue, ending in one Verdict; a failed essential capability is named to the user before delivery starts, and delivery starts after a failed one only on the user's word, recorded there.
_Avoid_: preflight, smoke test

**Harness**:
The tool a coordinator runs its workers in, named by the way workers run there (for example a claude.ai project, whose workers are threads, or one Claude Code session, whose workers are subagents and, on desktop, other sessions). Each way has one reference file in **Worker control**. The Harness's record is the only source of a worker's state; tracker comments are an audit trail.
_Avoid_: runtime adapter, platform

**Worker control**:
The `worker-control` Base skill: it starts, checks, stops, pauses and resumes workers in the **Harness** it runs in, and arranges and ends a check-in; deciding which work starts and when stays with its caller. It detects how workers run from the names of the tools it holds first (a project coordinator has no shell), the session-details record next and a shell's environment only as a second signal, takes the role (coordinator or worker) from explicit runtime lineage (a parent or Codex task path), never from being able to start workers, and loads that way's reference: what the Harness does by itself, and only the methods the coordinator adds, each citing the doc page it comes from or marked runtime-reported. Its short check proves those methods here before unattended work relies on them and names each failed one to the user; in a project it must show a recurring check-in arriving in the coordinator at least once and one thread stopping another and reading the stop back. A Harness with no reference falls back to its own docs, says so and names each method they do not give.
_Avoid_: harness-team (its working name), lifecycle agent

**Team lead**:
The `team-lead` skill: the role the coordinator runs to deliver planned work, always a Milestone's, a one-Release Milestone included (ADR 0010, ADR 0012). It manages the work, not the machinery: it starts build threads in order within the limits and starts Release threads (Release grouping stays `release`'s rule), reacts to what workers and the **Harness** report, holds a check-in only as a safety net (see **Stand-up**), replaces a stalled worker (see **Takeover**), pauses and resumes on the user's word (see **Pause**), follows the merge-time steps the repo's own docs give, and at a Milestone's end hands over to `milestone`'s report. Every worker start, state check, end, stop, pause, resume and check-in goes through **Worker control**; tracker comments are its audit trail, never a worker's state. The check-in is arranged when the first build thread starts (never for a Release thread that only plans; a Release thread is watched by Harness events, and at a check-in only to tell the user once when it has been silent a whole interval) and ends when delivery ends. Records of the earlier `milestone` delivery loop count as their team-lead counterparts (an old delivery-thread record as a start record naming its worker). "Coordinator" stays the name of the project's own agent; the team lead is what it runs.
_Avoid_: delivery loop (the earlier `milestone` section it replaces), manager

**Stand-up**:
What the **Team lead** does at a scheduled check-in, at the **Boundary record**'s interval: the safety net for a worker that is silent but nominally working. It runs the team-lead skill's snapshot command (one row per running build worker: its Harness state from **Worker control**, its last commit, its last comment, its pull request and a verdict: active, silent since a time, nudged and waiting, still silent after its nudge, or pull request ready but not reported; a tracker the command cannot read is read by hand) and acts only on rows that call for it: a ready pull request not reported is acted on as if reported, a silent worker is nudged once (a nudge record on its issue), and one still silent after its nudge is replaced (see **Takeover**); activity counts from the latest resume, so a nudge before a **Pause** is void. A running Release thread is read by hand instead: silent a whole interval with no report, the user is told once, and nothing else is done. A Stand-up that finds nothing writes nothing. Where the Harness pushes worker events it rarely finds anything; where it pushes none it carries more of the load. Stand-up records from the earlier `milestone` delivery loop stay on Milestone issues as history.
_Avoid_: status meeting, ping

**Takeover**:
The **Team lead** replacing a stalled worker (still silent at a **Stand-up** after its one nudge, or ended without its result as the **Harness** reads it) with a fresh worker on the same issue, which resumes from the pushed branch and the tracker; its start record names the worker it takes over from. A silent worker is first stopped through **Worker control** and the stop read back from the Harness's record (a call returning success, silence or an idle worker is not a stop; how a stop is taken, by a stop thread where the coordinator cannot stop one itself, is Worker control's). A stop that does not read back, a fresh start that fails, or the feature's second stall (a replacement started since the issue's latest park record stalls too) parks the work instead (see **Parked**), tells the user once and delivery goes on.
_Avoid_: replacement, restart

**Parked**:
The state of an issue whose stalled worker the **Team lead** could not replace safely, or whose feature stalled a second time (see **Takeover**), or that the user parked: marked with the tracker doc's **Park** operation (the `parked` label and a comment saying why). Other work goes on; the tickets a parked Ticket blocks are not started, and the Team lead skips parked work at every wake. It waits on the user, who lifts it by removing the label. A park the user sets on a feature no build thread has worked on is the user's own: skipped while it stands, and the feature starts normally once it is removed. Once the label is removed, the Team lead resumes the feature in its place in the order with a fresh worker from its pushed branch and its pull request, after reading its last worker's state through **Worker control**: one not ended is stopped and the stop read back first, and one whose stop does not read back parks the issue again, telling the user once. A Review never parks: until 2026-11-03 a review that would not settle parked its issue, a rule removed with the attempts (ADR 0003).
_Avoid_: stuck, shelved, deferred

**Pause**:
The user's word, to the **Team lead**, to stop spending without losing work. It posts a pause record, starts nothing new and pauses each running worker through **Worker control**: the Harness's own pause where it has one, otherwise a message to push its work and stop at its next natural step. While it is in effect nothing starts, no worker is nudged, replaced or parked, a check-in writes nothing, and merge-time steps run as the repo's own docs say they run during a pause (this repo's version hand-out gives no number and records a request as waiting; a number already out stays and its merge may finish). Resume, also on the user's word, posts a resume record, resumes the workers through Worker control and carries on from the tracker and the branches; activity counts from the resume, and a worker that does not carry on is handled like any silent one. Records of the earlier `milestone` form count too (see **Team lead**).
_Avoid_: freeze, halt

**Release**:
A named step of a Milestone (for example "Milestone 1 · Release 1"; a small Release is a Milestone with one Release), and the items it delivers, at most the **Release size** of them, picked from the top of the **Ranked list**. Every issue in it carries its release label (here `release-m<milestone>-r<n>`), and one release issue holds its goal, its Order with a reason per entry, the size used, what was left out and why, and, once cut, its notes with its start and end commits. Its name is never a version: the `release` skill is version-free, and what a repo does with a version is its release doc's versioning policy and **Cut steps** (here each skill-changing pull request bumps the version, and the changelog entry lists the versions delivered) (ADR 0012). Not a Milestone, which is the product goal its Releases work toward.
_Avoid_: sprint, version bump

**Release size**:
The most items a Release takes, set per repo in the release doc (setup's default 5; this repo 10). Items are counted of any kind: a Spec with its Tickets is 1, a lone Ticket 1, a bug 1. Issues marked `next-release` fill places like any item; only a severe issue (a security hole, lost data, delivery stopped) joins once the size is full.
_Avoid_: cap, feature cap

**Ranked list**:
The one list `release` sorts every candidate for the next Release into, in descending priority: group 1, severe issues and issues marked `next-release`; group 2, the Milestone's planned features, re-ordered each planning (a feature others depend on first, then the one that moves the goal furthest, the Milestone issue's order breaking ties), each preceded by its open blockers; group 3, `ready-for-agent` bugs, oldest first. An issue meeting several conditions goes in its highest group, first within it. A feature the Milestone issue does not list is never ranked; it is proposed to the user.

**Release planning**:
The last step of `release`: sort the candidates into the **Ranked list**, pick from the top up to the **Release size**, open the release issue and label what it takes, clearing `next-release` from it. It runs with no approval; the user's part is planning the Milestone and its features with `milestone`.
_Avoid_: release triage

**Cut steps**:
What a repo's release doc says the cut runs once the changelog entry is written, in order: what its versioning policy adds (a line listing the versions delivered, a bump pull request the user merges), anything else the repo must change or run, and optionally a step between Releases for a fix that cannot wait. A cut step wins over `release`'s own text where they differ, so the skill names no version policy.

**`next-release`**:
The triage label doc's role that marks an issue that must join the next Release. `triage` sets it on a severe issue or one blocking a planned feature, and `retro-planning` on the Ticket of a group that joins; `release` ranks marked issues in group 1 of the **Ranked list** and removes the mark from each it takes. No skill parses another skill's records for this.

**Triage batch**:
The run of `triage` that the Release thread makes at each Release end (`release` step 4), naming the release issue just closed: agents decide every open `needs-triage` issue against the Milestone without asking the user per issue, then make the **Backlog sweep**, record each decision on the issue, and post one `## Triage batch` summary comment on the release issue for the Milestone review. It sets `next-release` on a severe issue or one that blocks a planned feature, and sends an enhancement an agent found (an audit, investigation or retro finding) to `ready-for-human`, which agents never rank, close or expire. A blocker of a feature being built now and a severe issue are triaged at once instead: one issue, any time, by whoever sees it, with no Release named, and listed in the next batch's summary. A decision that crosses a boundary in the Boundary record, changes the Milestone's agreement or needs conflicting state roles settled goes to the user. There is no separate "inside a Milestone" test: run by the user, `triage` waits on the user per issue; run at a Release end, it is the batch.

**Backlog sweep**:
The second part of the **Triage batch**, over every open `ready-for-agent` issue, so that the **Ranked list** ranks a true backlog: an agent-found enhancement moves to `ready-for-human`; a duplicate is closed, linking the kept issue; an issue main's current code made obsolete is closed with the reason; a severe issue or a planned feature's blocker gets `next-release`; and an issue listed under "Left out" in the release issues of the last 3 Releases cut **expires**, closed as not planned with "reopen to bring it back". A planned feature, a Ticket of a planned Spec, a parked issue and a marked one never expire.

**Release thread**:
A project thread that runs `release`: it checks the current Release shipped, writes its `CHANGELOG.md` entry, runs the release doc's **Cut steps** and whole-Release check, merges the changelog pull request as the Boundary record allows, closes the release issue, runs the Triage batch and the Release-end Retro planning, then plans the next Release. The Release thread the coordinator starts to plan a Milestone's first Release (or a later one, once a feature left blocked or parked after the last Release is free, or blocked only by issues an agent can take, which `release` ranks ahead of it) only plans it: there is nothing before it to cut, so it cuts nothing. The coordinator's brief tells each Release thread that, when nothing qualifies, it opens no release issue, labels nothing and reports that it planned no Release.

**Build thread**:
A project thread that builds a Spec or a lone Ticket: a Spec thread or a Ticket thread.

**Spec thread**:
A project thread that builds one Spec with `implement-spec`.

**Ticket thread**:
A project thread that builds one lone Ticket with `implement`.

**Implementer**:
A subagent that builds a Ticket test-first and fixes its Findings. Build threads coordinate; Implementers write the code. Before reporting, an Implementer checks its diff against the repo's review rules file's Always-check lines and, for a new rule that runs over a sequence of Rounds or steps, walks the sequences before Round 1. For a criterion whose run needs tools it does not hold, it drafts the record entry with pending markers and reports the criterion as owed; the build thread produces that evidence.
_Avoid_: coder, worker

**Spec branch**:
The long-lived branch a Spec is built on. Its Tickets are squash-merged into it, and it merges into main with a merge commit.
_Avoid_: integration branch, feature branch

**Ticket branch**:
The branch one Ticket is built on. A Spec's Ticket branches start from the Spec branch and stay inside the thread; a lone Ticket's branch starts from main and is pushed.

**Ticket check**:
One Quick Round over a Spec's Ticket branch, against the Spec branch, before the Ticket joins it, recorded on the Spec pull request. Its open Findings carry into the Spec pull request's Round 1. Not one of the Spec pull request's Rounds.

**Continuation**:
The build of a Spec's Ticket that carries another agent's Agent label, by that agent, off the pushed Spec branch: the Spec thread hands it off and keeps the Spec pull request, and the other agent runs its Ticket check and squash-merges it in. Also the continuation Spec pull request that brings a closed Spec's remaining Tickets to main.

## Docs

**Skill docs folder**:
The one folder in a repo that only the skills use, `docs/dev-skills/`, holding every file they require at a fixed path: the Docs index, the setup files (the tracker, triage label, domain and release docs and the Boundary record), the glossary and its Area pages, ADRs and out-of-scope notes. Files that coding agents, other tools or people expect elsewhere stay outside it: `CLAUDE.md` and `AGENTS.md`, `REVIEW.md` at the root, the changelog at the path the release doc records, and `CONTRIBUTING.md` wherever the repo keeps it (ADR 0011).
_Avoid_: skills folder (the plugin's own `skills/`), agents folder

**Docs index**:
The page `docs/dev-skills/index.md`, in the Skill docs folder, that lists every doc the skills keep in a repo and the repo's own docs an agent may need, inside the folder and outside it (not `CLAUDE.md`, `SKILL.md` files or GitHub issues), grouped by Area, each with one line saying when to read it. Agents read it first and open only what their work needs.
_Avoid_: README, table of contents

**Area**:
One part of a project that docs are grouped by in the Docs index, such as site, hub or trip plugin. A large glossary is split into one page per Area.
_Avoid_: section, module

## Testing skills

A change to skill text is tested in three layers, **CI**, **Eval** and **Review**, sorted by one rule: if a script can catch it, it is CI; if you must watch an agent use the skill, it is an eval; if it needs reading for meaning, it is review. A Bug class that keeps coming back moves to the cheapest layer that can catch it (ADR 0013, `docs/dev-skills/evals.md`).

**CI**:
The layer for questions with one right answer from the files: a script with no model, on every pull request (the plugin checker and `claude plugin validate`; the deterministic tests join it with Ticket #627's runner and until then run by hand). It tests structure, never a skill's wording, so rewording a skill never fails it.

**Eval**:
The layer that shows what a skill makes an agent do: a fresh agent runs the skill on a fixture, and its output is scored by scripts first, a judge only for what scripts cannot see. Its cases live in `evals/<skill>/`. A pull request that changes how a skill behaves runs that skill's cases on its own skill and on main's (the baseline) and links the results; a wording-only, docs, ADR or eval-only change skips the run and says which kind it is. Nothing is left owed: the one allowed gap is a run that cannot be made, stated with its reason. The Implementer of such a change plans an eval, not a grep for a sentence, and chooses its seam without the user; its evidence is the eval run or the stated gap (the rule in `tdd` and the Implementer briefs). The third layer is the **Review**.
_Avoid_: test (for a model run), benchmark

**Case check**:
The check of a new eval case, or a changed expected result, before any model run: a fresh premium-tier subagent reads the whole skill and its workflow and returns keep, fix or drop (valid, fails on main for the right reason, needed); the verdict goes in the pull request body.

## Code review

**Review**:
One review of a change by the `agentic-review` skill: **Round 0** sizes it, and above level None the hidden `review-rounds` skill runs its Rounds. It has two entry points: a pull request (reviewed in up to 3 Rounds), or the diff since a fixed point (a commit, branch, tag or merge-base; it also reads uncommitted work), which runs Round 0 and Round 1 only and posts no comment.

**Round 0**:
The step that sizes a Review before any agent starts, run by the top-level session itself: it pins the diff, reads the changed files, the Boundary record and `REVIEW.md`, picks the **Review level** with a one-line reason, and records it. At None that line is the whole review comment and the project's checks are the review.

**Review level**:
How much review a change gets, picked by Round 0: **None** (version fields, changelog entries, lock files, generated output; the project's checks only), **Quick** (text that does not change what a rule or code does), **Standard** (everything else, the default) or **Deep** (what the Boundary record or `REVIEW.md` marks risky, or the user asks). A "Review levels" section in `REVIEW.md` names a project's own paths per level. Round 0 takes the higher level when unsure, and later Rounds only raise it. Older records call it the Review depth.
_Avoid_: depth, mode

**Round**:
One pass of Find, Verify and Rank over a pull request, its one comment, and the fix commits after it; a pull request gets at most 3. **Round 1** reviews the whole pull request; **Rounds 2 and 3** review only its new commits (for a merge from main, only its conflict resolutions), with one Finder and one Verifier at any level. Verify is skipped, with no Verifier started, when no Finder returned a candidate and no earlier Finding is open; the Round comment says no candidates went to a Verifier. Otherwise the Verifier is a separate agent each Round. A Round is **clean** when no Important is open after its Verify step; a clean Round means ready to merge. After Round 3, what is still open is sorted (see **After-Round-3 sort**).
_Avoid_: pass, iteration

**After-Round-3 sort**:
What happens when Round 3 is not clean: a premium-tier agent turns each open Important into a bug Ticket, worked straight away as its own Ticket, or dismisses it with a reason; open Nits are dropped, and the pull request merges. A merge from main with conflicts after Round 3 gets at most one Quick check of only its resolutions, whose open Importants become bug Tickets the same way.

**Dispute**:
An owner's written case, with evidence (`file:line`, a command and its output), that a Finding is wrong, in place of a fix. The next Round's Verifier decides it; when nothing was committed, that Round is the Verifier alone, on the disputes (an open dispute is an open Finding, so that Verifier runs).
_Avoid_: rebuttal (the earlier, removed rule)

**Design Finding**:
A Finding that questions the design itself (a gap in the agreed behaviour, two rules in conflict, a case left open). A premium-tier agent answers it within what the spec agreed (a pull request that builds no issue is its own spec), recorded as a comment on the spec issue, or on the pull request when it builds no issue: keep the design, or a change fixed in the next Round, or, in or after Round 3, a bug Ticket. The answers are listed on the pull request body's `Agent-merged rules:` line and in the build thread's report; the Milestone report reads that line.

**Waiting on a boundary**:
The one way a Review stops for a person: a fix, a design answer, a bug Ticket or the merge would cross a boundary as the `merging` skill defines it (an action the **Boundary record** says needs the user's approval, a one-way door it does not allow agents, or a limit or budget it sets). The Round comment's Result says what would be crossed, and the build thread brings the pull request to the user. The user's answer clears it, and the step that was waiting goes on.

**Question round**:
One batch of questions a skill (`grilling`, `triage`) puts to the user at once. Not a Round, and not a Review: the skills' "round" without a capital R means this.
_Avoid_: Round (for a batch of questions)

**REVIEW.md**:
A short file at a repo's root telling reviewers what Important means there, what to skip, what to always check (the **Always check** lines: each a Bug class earlier reviews caught, with its origin and file kinds; a line that checks the text for completeness, not for what an agent will do, adds an eval case for a real gap it finds), and optionally its own Review levels.

**Finder**:
A reviewer agent that looks for problems and reports candidate Findings. The **standards Finder** and **spec Finder** come from Upstream; at Standard and Deep one **adversarial Finder** takes the angle that fits the change best ("what the change is missing" is one); at Deep a premium **security Finder** is added. Rounds 2 and 3 run one **later-Round Finder**, standards and spec in one.
_Avoid_: reviewer (too broad), scanner

**Verifier**:
The one agent per Round (none when the Round has no candidates and no open Finding) that checks each candidate Finding, and each open Finding with any dispute of it, against the code, keeps only what it confirmed and makes the final call on it. Premium tier at Deep, regular otherwise.
_Avoid_: judge, triage agent

**Finding**:
One problem a Review reports, with a file and line, a Severity, a Bug class, and a Failure scenario.
_Avoid_: issue (that word means a GitHub issue), comment

**Severity**:
How much a Finding matters. **Important** must be fixed before the change is merged or accepted. **Nit** is small and optional. **Pre-existing** is real but not caused by the change under review.
_Avoid_: priority, blocker

**Door**:
How hard a change is to walk back. A **one-way door** is a change that reverting its commits would not fully undo, including anything outside git (a data migration, deleted data, a public interface others depend on, a message sent outside the project, a published release); a **two-way door** is one a revert does undo. Where each pull request bumps the version, the bump merged with it is not a published release: ADR 0008 walks a bad change back with a revert that takes the next number, so the bump alone keeps a pull request two-way; a Release that publishes a version, where Releases bump, is one-way. The `pr` skill records the call as `**Door:**` in the pull request body. The **Boundary record** alone decides whether a one-way door is self-merged, inside a Milestone or not (a Milestone issue holds no boundaries): it is an agent merge when the record allows agents to take each of its irreversible actions; with no record, none is allowed (ADR 0004).
_Avoid_: risk level

**Boundary record**:
A repo's agent doc, `docs/dev-skills/boundaries.md`, written with the user by `setup-dev-skills`: which irreversible actions agents may take, which actions need the user's approval (the list may be empty), the resource budget, the check-in interval (default one hour) and the form of a Milestone's membership label (for example `milestone-<n>`). `merging` (see **Merging**) reads it for every merge, which `implement`, `implement-spec` and `release` load at their merge step, inside a Milestone or not, instead of a fixed list, to decide whether a pull request crosses a boundary and so goes to the user; with no record they read an empty one (nothing allowed, nothing needing approval; ADR 0004). A repo may add its own limits to its record; this repo's is the skill file size limit (5,000 words, a split-or-redesign decision for the user, enforced by the `skill-file-size` check). It is the only record of boundaries: a Milestone issue holds none of its own (ADR 0004, Spec #633).
_Avoid_: permissions file, policy

**Merging**:
The `merging` Base skill, hidden from the menu: the finish of one pull request that is ready to merge (a review that ended ready to merge, or for a pull request with no review, its checks passing). Its caller names the pull request and its issue, the merge method and title, who makes each commit (its Implementer, with its worktree where it has one, so a build thread still writes no code) and any pre-merge step of its own. It decides who merges from the **Boundary record** alone (none means an empty one): the user gets the pull request only when it crosses a boundary or the repo's own rules say a person merges it, and it names what stops the merge; a Deep review or a change to an ADR, the glossary, a `CLAUDE.md`, an `AGENTS.md` or a `REVIEW.md` never does, and an agent merge of such a change, or of design answers, gets the `Agent-merged rules:` line. Just before any merge, the user's too, it runs the repo's merge-time steps from its own docs (a version bump only where the release doc gives one), syncs with main by a merge and waits for CI, repeating when main moves; then it merges with the caller's method, confirms the merge on the tracker (a report alone never counts) and closes the issues, with `issue-absorption` for absorbed sources. It names no command and no version policy. `implement` (step 7 and the retro check), `implement-spec` (step 8) and `release` (its changelog pull request) load it at their merge step, and `review-rounds` defines a boundary crossing by it.
_Avoid_: merge step (a caller's step that loads it), auto-merge

**Bug class**:
The kind of problem a Finding is (for example "unescaped user input"), so every place it occurs is fixed together.
_Avoid_: category, type

**Failure scenario**:
The part of a Finding that shows the problem happens: the inputs or state, then the wrong result. A cleanup Finding (a smell, or a Nit with no wrong result) states its cost instead.
_Avoid_: repro, example

## Retros

**Retro issue**:
One suggestion from `retro` filed as a GitHub issue labelled `retro`, in the repo where its fix lands. It is never `needs-triage`; Retro planning decides what happens to it.
_Avoid_: retro ticket, action item

**Retro backlog**:
The open Retro issues of one repo.
_Avoid_: retro queue, improvement list

**Retro planning**:
The review of a snapshot of one repo's Retro backlog, which merges duplicates, closes most one-offs and turns at most 3 groups into Tickets (a group seen in one thread acts only if it is severe or its fix is a cheap deterministic check that a **necessity check** confirms). It walks the user through one group at a time and carries out each call at once (at a Release end, see **Release-end Retro planning**). Its record issue, labelled `retro-planning`, is open while it runs and closed at its end; later plannings read only closed records.
_Avoid_: retro triage, retro review

**Necessity check**:
The check a fresh premium-tier subagent makes in a Retro planning before a one-thread group whose fix is a cheap deterministic check (a CI step, a checker rule, a test) is acted on: the check would have failed on the real past mistake the Retro issues describe, and nothing already catches it. The planning record shows its verdict in the group's Verdicts row. Not confirmed, the group takes the one-thread `wontfix`.

**Release-end Retro planning**:
The Retro planning that the caller runs at the end of a Release, with the Triage batch: agents decide every group without asking the user per group, with no 3-Ticket cap, and record each call and reason in the planning record for the Milestone review. A fix joins the next Release only if it blocks a feature of the Milestone or is severe; its Ticket then carries the `next-release` mark, which `release` reads instead of the record; it fills a place in the **Release size** like any item, and only a severe one joins past the size. Any other acting group stays open with a reason, and the rest close. A group that crosses a boundary, changes the Milestone's agreement, or would join the next Release but needs a feature-sized fix is proposed to the user, not filed.

**Spin-off**:
A group of Retro issues the user wants to discuss further, moved out of a Retro planning into a planning thread of its own, which ends by giving each issue a Ticket or a close. It does not count toward the cap and cannot expire meanwhile.
_Avoid_: deferral, parked group
