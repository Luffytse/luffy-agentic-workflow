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
Matt Pocock's public skills repo (`mattpocock/skills`), which `dev-skills` is forked from.
_Avoid_: original, source

**Patch**:
One change we made to text that came from Upstream, recorded in `PATCHES.md`.
_Avoid_: customization, override

**Model tier**:
How strong a model a step needs: **cheap**, **regular**, or **premium**. Each agent maps the tiers to its own models, so a skill names a tier and never a vendor's model.
_Avoid_: model size, model class

**Model-invoked skill**:
A Skill the agent may start by itself when a task fits its description. A **user-only skill** (`disable-model-invocation: true`) starts only when a person types its name.
_Avoid_: auto skill, manual skill

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

**Milestone**:
A project goal (for example "M3 Trip planning") that groups the Specs and Tickets needed to reach it.

**Release**:
One version of a plugin and the few issues it ships, each labelled `release-X.Y.Z`, with one release issue holding its goal and notes. Not a Milestone, which is a project goal.
_Avoid_: sprint, version bump

**Release planning**:
The step that picks the next Release's goal and issues: the agent proposes, the user decides, and only approved issues get the label.
_Avoid_: release triage

**Release thread**:
A project thread that cuts a Release (the bump pull request and its `CHANGELOG.md` entry) and then runs the next Release planning.

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
One Review plus the fix commits that follow it (the final commit of "fix" Nits is not reviewed by another Round). Rounds 1 and 2 are **full-PR Rounds**; Rounds 3 to 5 are **commit Rounds**, which review only the commits added since the last Round (for a merge from main, only what it changed in the pull request).
_Avoid_: pass, iteration

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
An agent that checks each candidate Finding against the code and makes the final call on it. On Deep, three Verifiers take different stances: **tracer**, **skeptic** and **spec checker**.
_Avoid_: judge, triage agent

**Finding**:
One problem a Review reports, with a file and line, a Severity, a Bug class, and a Failure scenario.
_Avoid_: issue (that word means a GitHub issue), comment

**Severity**:
How much a Finding matters. **Important** must be fixed before the change is merged or accepted. **Nit** is small and optional. **Pre-existing** is real but not caused by the change under review.
_Avoid_: priority, blocker

**Door**:
How hard a change is to walk back. A **one-way door** is a change that reverting its commits would not fully undo, including anything outside git (a data migration, deleted data, a public interface others depend on, a message sent outside the project, a published release); a **two-way door** is one a revert does undo. The `pr` skill records the call as `**Door:**` in the pull request body, and a pull request behind a one-way door is not self-merged.
_Avoid_: risk level

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
