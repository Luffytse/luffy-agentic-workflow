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
A Skill holding a focused Shared rule that consumers load by name without loading a larger workflow for that rule alone. ADR 0009 records the implemented `docs-index`, `review-record`, `issue-absorption` and `worker-control` Base skills, with menu hiding preferred where supported; existing rules and consistency protections still govern unmigrated shared copies.
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
The label of the optional agent-only triage role: it marks an issue for one coding agent only, and a repo maps the role to one label per agent in its `docs/agents/triage-labels.md` (this repo: `claude-only` and `codex-only`). It is neither a category nor a state role. An agent that sees another agent's label does not work the issue; an issue with none can be taken by any agent. `triage` may apply it, and `to-tickets` copies a Spec's onto each of its Tickets.
_Avoid_: assignee, owner

**Milestone**:
A product goal the user sets (for example "M3 Trip planning"), written down in one Milestone issue: the goal, the features to deliver by its end, in build order, their acceptance criteria, what is excluded, any budget (a limit on one of the project's paid or limited resources, such as a paid API key) and any boundaries beyond the **Boundary record**. The `milestone` skill holds only planning, adding a feature, Startup verification and the report: its planning phase writes that issue with the user; agents may propose a feature, never add one, and a feature added mid-Milestone is planned with the user first, then listed in the issue, then labelled. Delivery starts once planning settles and the latest **Startup verification** result passes, or after a failed one once the user says to go on (recorded on the Milestone issue); the coordinator runs it with the **Team lead** skill, which reads the Milestone issue for the features, their order and the boundaries, and `milestone` reports at its end. It holds one or more Releases, which the agents plan, and it closes when the user accepts it at the Milestone review. An issue belongs to it, and its pull request is **inside the Milestone**, when the issue (for a Spec's pull request, the Spec) carries the Milestone's membership label in the form the **Boundary record** names; the Milestone issue carries the same label. A build thread's no-issue corrective check records `Retro origin: <Ticket or Spec issue link>` in its pull request body; Review and merge read that origin's labels for the same membership, and agent design answers go on that issue. This source is not an issue the check builds: its first failed attempt still parks on the pull request with no restart. Other no-issue pull requests remain outside. The Tickets split from a Milestone's Spec carry the label too, and `to-tickets` publishes their breakdown without asking the user while it keeps the Spec's scope. Inside a Milestone a build thread merges its own pull request unless it crosses a boundary or the repo's own rules say a person merges it (ADR 0004). A pull request review that will not settle, inside a Milestone or outside one, ends its attempt, in a restart the first time and a park the second (see **Parked**), and is not brought to the user; Ticket checks stay as **Parked** says.
_Avoid_: epic, sprint

**Startup verification**:
The check the `milestone` skill records before a Milestone's autonomous delivery starts, in two parts: the **Worker control** check, which proves in this environment, with short bounded **probes**, that workers start, that a worker's state is read from the **Harness**, that a pause holds, that a stopped worker is confirmed stopped by the Harness's own record (not by silence, a sent stop request or a worker merely idle between turns), that an end or failure wakes the coordinator and that a check-in reaches it; and the loaded-skill-version probe, which proves that a fresh thread loads the plugin version on main. Each passes only on evidence observed afterwards, in the agent that will take that action during delivery. The result, with the runtime's permission and sandbox settings, is one comment on the Milestone issue, ending in one Verdict; a failed essential capability is named to the user before delivery starts, and delivery starts after a failed one only on the user's word, recorded there.
_Avoid_: preflight, smoke test

**Harness**:
The tool a coordinator runs its workers in, named by the way workers run there (for example a claude.ai project, whose workers are threads, or one Claude Code session, whose workers are subagents and, on desktop, other sessions). Each way has one reference file in **Worker control**. The Harness's record is the only source of a worker's state; tracker comments are an audit trail.
_Avoid_: runtime adapter, platform

**Worker control**:
The `worker-control` Base skill: it starts, checks, stops, pauses and resumes workers in the **Harness** it runs in, and arranges and ends a check-in; deciding which work starts and when stays with its caller. It detects how workers run from the names of the tools it holds first (a project coordinator has no shell), the session-details record next and a shell's environment only as a second signal, takes the role (coordinator or worker) from an explicit parent only, never from being able to start workers, and loads that way's reference: what the Harness does by itself, and only the methods the coordinator adds, each citing the doc page it comes from or marked runtime-reported. Its short check proves those methods here before unattended work relies on them and names each failed one to the user; in a project it must show a recurring check-in arriving in the coordinator more than once and one thread stopping another and reading the stop back. A Harness with no reference falls back to its own docs, says so and names each method they do not give.
_Avoid_: harness-team (its working name), lifecycle agent

**Team lead**:
The `team-lead` skill: the role the coordinator runs to deliver planned work, a whole Milestone or a lone Release (ADR 0010). It manages the work, not the machinery: it starts build threads in order within the limits and starts Release threads (Release grouping stays `release`'s rule), reacts to what workers and the **Harness** report, holds a check-in only as a safety net (see **Stand-up**), replaces a stalled worker (see **Takeover**), pauses and resumes on the user's word (see **Pause**), follows the merge-time steps the repo's own docs give, and at a Milestone's end hands over to `milestone`'s report. Every worker start, state check, end, stop, pause, resume and check-in goes through **Worker control**; tracker comments are its audit trail, never a worker's state. The check-in is arranged when the first build thread starts (never for a Release thread that only plans; a Release thread is watched by Harness events, and at a check-in only to tell the user once when it has been silent a whole interval) and ends when delivery ends. Records of the earlier `milestone` delivery loop count as their team-lead counterparts (an old delivery-thread record as a start record naming its worker). "Coordinator" stays the name of the project's own agent; the team lead is what it runs.
_Avoid_: delivery loop (the earlier `milestone` section it replaces), manager

**Stand-up**:
What the **Team lead** does at a scheduled check-in, at the **Boundary record**'s interval: the safety net for a worker that is silent but nominally working. It runs the team-lead skill's snapshot command (one row per running build worker: its Harness state from **Worker control**, its last commit, its last comment, its pull request and a verdict: active, silent since a time, nudged and waiting, still silent after its nudge, or pull request ready but not reported; a tracker the command cannot read is read by hand) and acts only on rows that call for it: a ready pull request not reported is acted on as if reported, a silent worker is nudged once (a nudge record on its issue), and one still silent after its nudge is replaced (see **Takeover**); activity counts from the latest resume, so a nudge before a **Pause** is void. A running Release thread is read by hand instead: silent a whole interval with no report, the user is told once, and nothing else is done. A Stand-up that finds nothing writes nothing. Where the Harness pushes worker events it rarely finds anything; where it pushes none it carries more of the load. Stand-up records from the earlier `milestone` delivery loop stay on Milestone issues as history.
_Avoid_: status meeting, ping

**Takeover**:
The **Team lead** replacing a stalled worker (still silent at a **Stand-up** after its one nudge, or ended without its result as the **Harness** reads it) with a fresh worker on the same issue, which resumes from the pushed branch and the tracker; its start record names the worker it takes over from. A silent worker is first stopped through **Worker control** and the stop read back from the Harness's record (a call returning success, silence or an idle worker is not a stop; how a stop is taken, by a stop thread where the coordinator cannot stop one itself, is Worker control's). A stop that does not read back, a fresh start that fails, or the feature's second stall (a replacement started since the issue's latest park record stalls too) parks the work instead (see **Parked**), tells the user once and delivery goes on.
_Avoid_: replacement, restart (a Review's restart is another thing)

**Pause**:
The user's word, to the **Team lead**, to stop spending without losing work. It posts a pause record, starts nothing new and pauses each running worker through **Worker control**: the Harness's own pause where it has one, otherwise a message to push its work and stop at its next natural step. While it is in effect nothing starts, no worker is nudged, replaced or parked, a check-in writes nothing, and merge-time steps run as the repo's own docs say they run during a pause (this repo's version hand-out gives no number and records a request as waiting; a number already out stays and its merge may finish). Resume, also on the user's word, posts a resume record, resumes the workers through Worker control and carries on from the tracker and the branches; activity counts from the resume, and a worker that does not carry on is handled like any silent one. Records of the earlier `milestone` form count too (see **Team lead**).
_Avoid_: freeze, halt

**Release**:
A named step inside a Milestone (for example "Milestone 1 · Release 1"), and the few features it delivers (at most 5 unless the user raises the cap for that Release; a feature is a Spec with its Tickets, a lone Ticket with the issues it absorbs, or a few related issues the user agrees to treat as one), every issue in them labelled `release-m<milestone>-r<n>`, with one release issue holding its goal, notes, start and end commits and the versions it delivered. Its name is not a version: in this repo each skill-changing pull request bumps the version. Not a Milestone, which is the product goal its Releases work toward.
_Avoid_: sprint, version bump

**Release planning**:
The step that picks the next Release's goal and features: the agent proposes, the user decides, and only approved issues get the label. Inside a Milestone (a Boundary record naming a Milestone label form and an open Milestone issue) agents decide it with no approval: the Milestone's planned, open features carrying no release label, not parked and unblocked, in its issue's order (at most 5, the user alone raising the cap) plus the maintenance fixes the Triage batch and Release-end Retro planning chose (outside the cap), after both; a feature the Milestone issue does not list is proposed to the user, never labelled.
_Avoid_: release triage

**Triage batch**:
Inside a Milestone (a Boundary record naming a Milestone label form and an open Milestone issue), the run of `triage` that the caller makes at the end of a Release: agents decide every open `needs-triage` issue against the Milestone without asking the user per issue, record each decision on the issue, and post one `## Triage batch` summary comment on the release issue for the Milestone review. A blocker of a feature being built now and a security or data-loss risk are triaged at once instead: one issue, any time inside a Milestone, by whoever sees it, with no Release named, and listed in the next batch's summary; a decision that crosses a boundary or changes the Milestone's agreement goes to the user. Outside a Milestone `triage` waits on the user as before.

**Release thread**:
A project thread that cuts a Release (its `CHANGELOG.md` entry, the whole-Release check and, where the release doc says Releases bump, the bump pull request) and then runs the next Release planning, with the `release` skill. Inside a Milestone it first runs the Triage batch and the Release-end Retro planning for that Release, so the planning sees their maintenance fixes. The Release thread the coordinator starts to plan a Milestone's first Release (or a later one, once a feature left blocked or parked after the last Release is free) only plans it: there is nothing before it to cut, so it cuts nothing. The coordinator's brief tells each Release thread that, when no planned feature qualifies and no maintenance fix joins, it opens no release issue, labels nothing and reports that it planned no Release.

**Build thread**:
A project thread that builds a Spec or a lone Ticket: a Spec thread or a Ticket thread.

**Spec thread**:
A project thread that builds one Spec with `implement-spec`.

**Ticket thread**:
A project thread that builds one lone Ticket with `implement`.

**Implementer**:
A subagent that builds a Ticket test-first and fixes its Findings. Build threads coordinate; Implementers write the code.
_Avoid_: coder, worker

**Spec branch**:
The long-lived branch a Spec is built on. Its Tickets are squash-merged into it, and it merges into main with a merge commit.
_Avoid_: integration branch, feature branch

**Ticket branch**:
The branch one Ticket is built on. A Spec's Ticket branches start from the Spec branch and stay inside the thread; a lone Ticket's branch starts from main and is pushed.

**Ticket check**:
One Review at Quick depth over a Spec's Ticket before it joins the Spec branch. Not a Round.

## Docs

**Docs index**:
The page `docs/index.md` that lists every doc the skills keep in a repo (not `CLAUDE.md`, `SKILL.md` files or GitHub issues), grouped by Area, each with one line saying when to read it. Agents read it first and open only what their work needs.
_Avoid_: README, table of contents

**Area**:
One part of a project that docs are grouped by in the Docs index, such as site, hub or trip plugin. A large glossary is split into one page per Area.
_Avoid_: section, module

## Code review

**Review**:
One run of the `agentic-review` skill, in three stages: find candidate Findings, verify them, then rank the survivors. It has two entry points: a pull request (reviewed in Rounds), or the diff since a fixed point (a commit, branch, tag or merge-base; it also reads uncommitted work). The second kind is one Review, not a Round; a Ticket check is that kind, one Review at Quick depth over a Ticket branch's diff.

**Round**:
One Review plus the fix commits that follow it (the final text "fix" Nit commit is checked before the clean comment and included if a later merge-only Round's pinned range contains it). Rounds 1 and 2 are **full-PR Rounds**; Rounds 3 to 5 are **commit Rounds**, which review only the commits added since the last Round (for a merge from main, only what it changed in the pull request). A Late design Round and a Late merge-only Round may follow Round 5, and the Rounds belong to one Attempt.
_Avoid_: pass, iteration

**Late design Round**:
The one Round after Round 5 (Round 6) that reviews an agreed design answer that changes the pull request and came when Round 5 was the last Round run and neither late Round had run. At most one per attempt; it keeps the attempt's history.

**Late merge-only Round**:
The one Round after the last Round (Round 6, or Round 7 after a Late design Round) that reviews the resolutions of a merge from main with conflicts, when no Round is left. At most one per attempt; it keeps the attempt's history. If it is not clean, or main brings conflicts again after it ran, the attempt ends; it never goes to the user as a merge decision.

**Convergence check**:
The check after Rank from Round 2 on, inside a Milestone or outside one: an Important caused by the change **returned** when it matches, by Rank's match rule, a row already marked `fixed` (or, across attempts, makes the same claim in the same file as a returned or flipped row of an earlier attempt record), and **flipped** when its fix would undo an earlier row's fix. Either one ends the attempt.
_Avoid_: loop detection

**Attempt**:
One build of a change and the Rounds that review it, inside a Milestone or outside one. It ends when the convergence check finds a returned or flipped Finding, or Round 5, the late design Round or the late merge-only Round is not clean, or main brings conflicts again after the late merge-only Round ran, or, inside a Milestone, an agreed design answer changes the pull request after either late Round ran clean; the Review then reports **restart** (the first attempt) or **park** (a later one; a pull request that builds no issue parks after its first) to its caller. The build thread carries out a restart: it closes the pull request, keeps the untouched parts (a lone Ticket splits off those that stand alone; a Spec keeps, on a fresh Spec branch, the landed Tickets whose files are all untouched and shared with no other landed Ticket, and whose blockers are kept) and rebuilds the rest once from main, in a new pull request whose Rounds start at Round 1. A park is carried out by the build thread too: see **Parked**. A Round 5 that is not clean never goes to the user as a merge decision.

**Attempt record**:
The comment a Review writes on the issue the pull request builds (the lone Ticket, or the Spec) when an attempt ends (on the pull request itself when it builds no issue), in the shape `review-record` owns: the attempt number, the pull request, the Rounds, the Findings it ended on, what was tried, the lesson and the untouched files. It follows the problem: a later attempt reads every earlier one. A Spec thread also writes one on a Ticket it parks after the Ticket's third Ticket check.
_Avoid_: retry log

**Parked**:
The state of an issue whose build gave up because its review would not settle, inside a Milestone or outside one: a pull request whose second attempt ended (the Review's `park` outcome; a pull request that builds no issue parks after its first), or, inside a Milestone, a Ticket whose third Ticket check still has an Important open; or an issue whose stalled worker the **Team lead** could not replace safely, or whose feature stalled a second time (see **Takeover**: the team lead marks it the same way, with a park record naming the reason). The build thread marks the issue (or such a pull request) with the tracker doc's **Park** operation (the `parked` label and a comment linking the attempt history), leaves the pull request unmerged and tells the user once. Other work goes on; the tickets a parked Ticket blocks are not started, and the Team lead skips parked work at every wake. It waits on the user, who lifts it by removing the label. A park the user sets on a feature no build thread has worked on is the user's own: skipped while it stands, and the feature starts normally once it is removed. Once the label is removed, the Team lead resumes the feature in its place in the order with a fresh worker from its pushed branch, its pull request and its attempt history, after reading its last worker's state through **Worker control**: one not ended is stopped and the stop read back first, and one whose stop does not read back parks the issue again, telling the user once. Outside a Milestone a Ticket whose third Ticket check is not clean still goes to the user.
_Avoid_: stuck, shelved, deferred

**Question round**:
One batch of questions a skill (`grilling`, `triage`) puts to the user at once. Not a Round, and not a Review: the skills' "round" without a capital R means this.
_Avoid_: Round (for a batch of questions)

**Merge-only Round**:
A Round 3 to 5 (or the one Late merge-only Round) whose range contains merges from main plus only checked final text-Nit commits from the preceding clean Round and release-doc-required version-only bumps. It reviews that entire pinned range, at Quick depth for text and version-only changes, or the carried depth when a resolution touches logic. Other work requires an ordinary Round within the existing budget; it grants no extra late Round.

**REVIEW.md**:
A short file at a repo's root telling reviewers what Important means there, what to skip, and what to always check.

**Review depth**:
How thorough a Review is: **Quick**, **Standard** (the default), or **Deep**.
_Avoid_: level, mode

**Finder**:
A reviewer agent that looks for problems and reports candidate Findings. The **standards Finder** and **spec Finder** come from Upstream; **adversarial Finders** each take one angle chosen to fit the change under review. On Deep, a **security Finder** is added, and a Gap sweep runs after Verify.
_Avoid_: reviewer (too broad), scanner

**Verifier**:
An agent that checks each candidate Finding against the code and makes the final call on it. On Deep, three Verifiers take different stances: **tracer**, **skeptic** and **spec checker**. Inside a Milestone, a **rebuttal Verifier** (premium tier) decides a fixer's **rebuttal**, its evidence that an open Important is wrong: it dismisses the Finding or upholds it, and an upheld one cannot be rebutted again.
_Avoid_: judge, triage agent

**Finding**:
One problem a Review reports, with a file and line, a Severity, a Bug class, and a Failure scenario.
_Avoid_: issue (that word means a GitHub issue), comment

**Severity**:
How much a Finding matters. **Important** must be fixed before the change is merged or accepted. **Nit** is small and optional. **Pre-existing** is real but not caused by the change under review.
_Avoid_: priority, blocker

**Door**:
How hard a change is to walk back. A **one-way door** is a change that reverting its commits would not fully undo, including anything outside git (a data migration, deleted data, a public interface others depend on, a message sent outside the project, a published release); a **two-way door** is one a revert does undo. Where each pull request bumps the version, the bump merged with it is not a published release: ADR 0008 walks a bad change back with a revert that takes the next number, so the bump alone keeps a pull request two-way; a Release that publishes a version, where Releases bump, is one-way. The `pr` skill records the call as `**Door:**` in the pull request body. Outside a Milestone, a pull request behind a one-way door is not self-merged; inside one, the Milestone issue and then the **Boundary record** decide: a one-way door is an agent merge when, for each of its irreversible actions, the Milestone issue explicitly allows agents to take it or, where the Milestone issue does not mention it, the record does (ADR 0004).
_Avoid_: risk level

**Boundary record**:
A repo's agent doc, `docs/agents/boundaries.md`, written with the user by `setup-dev-skills`: which irreversible actions agents may take, which actions need the user's approval (the list may be empty), the resource budget, the check-in interval (default one hour) and the form of a Milestone's membership label (for example `milestone-<n>`). Inside a Milestone, the build skills read it instead of a fixed list to decide whether a pull request crosses a boundary and so goes to the user; outside one, the build skills' outside-a-Milestone merge list governs (ADR 0004). A Milestone issue may add allowed or forbidden actions for its own issues and wins over the record for them.
_Avoid_: permissions file, policy

**Bug class**:
The kind of problem a Finding is (for example "unescaped user input"), so every place it occurs is fixed together.
_Avoid_: category, type

**Failure scenario**:
The part of a Finding that shows the problem happens: the inputs or state, then the wrong result. A cleanup Finding (a smell, or a Nit with no wrong result) states its cost instead.
_Avoid_: repro, example

**Gap sweep**:
On Deep, one more Finder that runs after Verify, gets the kept Findings, and looks only for what the change is missing. Its Findings go through Verify too.
_Avoid_: second pass, recheck

## Retros

**Retro issue**:
One suggestion from `retro` filed as a GitHub issue labelled `retro`, in the repo where its fix lands. It is never `needs-triage`; Retro planning decides what happens to it.
_Avoid_: retro ticket, action item

**Retro backlog**:
The open Retro issues of one repo.
_Avoid_: retro queue, improvement list

**Retro planning**:
The review of a snapshot of one repo's Retro backlog, which merges duplicates, closes most one-offs and turns at most 3 groups into Tickets. It walks the user through one group at a time and carries out each call at once (inside a Milestone, see **Release-end Retro planning**). Its record issue, labelled `retro-planning`, is open while it runs and closed at its end; later plannings read only closed records.
_Avoid_: retro triage, retro review

**Release-end Retro planning**:
Inside a Milestone (a Boundary record naming a Milestone label form and an open Milestone issue), the Retro planning that the caller runs at the end of a Release, with the Triage batch: agents decide every group without asking the user per group, with no 3-Ticket cap, and record each call and reason in the planning record for the Milestone review. A fix joins the next Release only if it touches a feature of the Milestone or is severe, and does not count toward the Release's feature cap; any other acting group stays open with a reason, and the rest close. A group that crosses a boundary, changes the Milestone's agreement, or would join the next Release but needs a feature-sized fix is proposed to the user, not filed. Outside a Milestone Retro planning is unchanged.

**Spin-off**:
A group of Retro issues the user wants to discuss further, moved out of a Retro planning into a planning thread of its own, which ends by giving each issue a Ticket or a close. It does not count toward the cap and cannot expire meanwhile.
_Avoid_: deferral, parked group
