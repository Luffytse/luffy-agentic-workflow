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
A Skill holding a focused Shared rule that consumers load by name without loading a larger workflow for that rule alone. ADR 0009 records the implemented `docs-index`, `review-record` and `issue-absorption` Base skills, with menu hiding preferred where supported; existing rules and consistency protections still govern unmigrated shared copies.
_Avoid_: library skill, helper skill

## Where the skills run

**Project thread**:
One task's Claude session inside a Claude project. A **coordinator** (the project's own Claude) starts each thread with a brief, so nobody types slash commands there.
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
A product goal the user sets (for example "M3 Trip planning"), written down in one Milestone issue: the goal, the features to deliver by its end, their acceptance criteria, what is excluded and any budget (a limit on one of the project's paid or limited resources, such as a paid API key). It holds one or more Releases, which the agents plan, and it closes when the user accepts it at the Milestone review. An issue belongs to it, and its pull request is **inside the Milestone**, when the issue (for a Spec's pull request, the Spec) carries the Milestone's membership label in the form the **Boundary record** names; the Milestone issue carries the same label. Inside a Milestone a build thread merges its own pull request unless it crosses a boundary or the repo's own rules say a person merges it (ADR 0004). A review that will not settle there is parked, not brought to the user.
_Avoid_: epic, sprint

**Release**:
A named step inside a Milestone (for example "Milestone 1 · Release 1"), and the few features it delivers (at most 5 unless the user raises the cap for that Release; a feature is a Spec with its Tickets, a lone Ticket with the issues it absorbs, or a few related issues the user agrees to treat as one), every issue in them labelled `release-m<milestone>-r<n>`, with one release issue holding its goal, notes, start and end commits and the versions it delivered. Its name is not a version: in this repo each skill-changing pull request bumps the version. Not a Milestone, which is the product goal its Releases work toward.
_Avoid_: sprint, version bump

**Release planning**:
The step that picks the next Release's goal and features: the agent proposes, the user decides, and only approved issues get the label.
_Avoid_: release triage

**Release thread**:
A project thread that cuts a Release (its `CHANGELOG.md` entry, the whole-Release check and, where the release doc says Releases bump, the bump pull request) and then runs the next Release planning, with the `release` skill.

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
One Review plus the fix commits that follow it (the final commit of "fix" Nits is not reviewed by another Round). Rounds 1 and 2 are **full-PR Rounds**; Rounds 3 to 5 are **commit Rounds**, which review only the commits added since the last Round (for a merge from main, only what it changed in the pull request). Inside a Milestone a Late design Round may follow Round 5, and the Rounds belong to one Attempt.
_Avoid_: pass, iteration

**Late design Round**:
Inside a Milestone, the one Round after Round 5 (Round 6) that reviews an agreed design answer that changes the pull request and came when Round 5 had run. At most one per attempt; it keeps the attempt's history.

**Convergence check**:
Inside a Milestone, the check after Rank from Round 2 on: an Important caused by the change **returned** when it matches, by Rank's match rule, a row already marked `fixed` (or, across attempts, makes the same claim in the same file as a returned or flipped row of an earlier attempt record), and **flipped** when its fix would undo an earlier row's fix. Either one ends the attempt.
_Avoid_: loop detection

**Attempt**:
Inside a Milestone, one build of a change and the Rounds that review it. It ends when the convergence check finds a returned or flipped Finding, or Round 5 or the late design Round is not clean; the Review then reports **restart** (the first attempt) or **park** (a later one) to its caller. A park is carried out by the build thread: see **Parked**.

**Attempt record**:
The comment a Review writes on the issue the pull request builds (the lone Ticket, or the Spec) when an attempt ends, in the shape `review-record` owns: the attempt number, the pull request, the Rounds, the Findings it ended on, what was tried, the lesson and the untouched files. It follows the problem: a later attempt reads every earlier one. A Spec thread also writes one on a Ticket it parks after the Ticket's third Ticket check.
_Avoid_: retry log

**Parked**:
Inside a Milestone, the state of an issue whose build gave up because its review would not settle: a pull request whose second attempt ended (the Review's `park` outcome), or a Ticket whose third Ticket check still has an Important open. The build thread marks the issue with the tracker doc's **Park** operation (the `parked` label and a comment linking the attempt history), leaves the pull request unmerged and tells the user once. Other work goes on; the tickets a parked Ticket blocks are not started. It waits on the user, who lifts it by removing the label. Outside a Milestone nothing is parked: the pull request or Ticket goes to the user.
_Avoid_: stuck, shelved, deferred

**Question round**:
One batch of questions a skill (`grilling`, `triage`) puts to the user at once. Not a Round, and not a Review: the skills' "round" without a capital R means this.
_Avoid_: Round (for a batch of questions)

**Merge-only Round**:
A Round 3 to 5 whose new commits are only a merge from main. When the merge's conflicts were only text, it runs at Quick depth, not the carried one, unless a resolution touches logic.

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
The review of a snapshot of one repo's Retro backlog, which merges duplicates, closes most one-offs and turns at most 3 groups into Tickets. It walks the user through one group at a time and carries out each call at once. Its record issue, labelled `retro-planning`, is open while it runs and closed at its end; later plannings read only closed records.
_Avoid_: retro triage, retro review

**Spin-off**:
A group of Retro issues the user wants to discuss further, moved out of a Retro planning into a planning thread of its own, which ends by giving each issue a Ticket or a close. It does not count toward the cap and cannot expire meanwhile.
_Avoid_: deferral, parked group
