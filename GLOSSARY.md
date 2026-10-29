# luffy-dev-skills

Lufei's plugin marketplace: the skills Lufei's coding agents use, packaged so every project and every agent session can load them.

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
One run of the `code-review` skill over a pull request (or, for a Ticket check, over a Ticket branch's diff), in three stages: find candidate Findings, verify them, then rank the survivors.

**Round**:
One Review plus the fix commits that follow it (the final commit of "fix" Nits is not reviewed by another Round). Rounds 1 and 2 are **full-PR rounds**; rounds 3 to 5 are **commit rounds**, which review only the commits added since the last Round.
_Avoid_: pass, iteration

**REVIEW.md**:
A short file at a repo's root telling reviewers what Important means there, what to skip, and what to always check.

**Review depth**:
How thorough a Review is: **Quick**, **Standard** (the default), or **Deep**.
_Avoid_: level, mode

**Finder**:
A reviewer agent that looks for problems and reports candidate Findings. The **standards Finder** and **spec Finder** come from Upstream; **adversarial Finders** each take one angle chosen for the pull request. On Deep, a **security Finder** is added.
_Avoid_: reviewer (too broad), scanner

**Verifier**:
An agent that checks each candidate Finding against the code and makes the final call on it. On Deep, three Verifiers take different stances: **tracer**, **skeptic** and **spec checker**.
_Avoid_: judge, triage agent

**Finding**:
One problem a Review reports, with a file and line, a Severity, and a Bug class.
_Avoid_: issue (that word means a GitHub issue), comment

**Severity**:
How much a Finding matters. **Important** must be fixed before merge. **Nit** is small and optional. **Pre-existing** is real but not caused by this pull request.
_Avoid_: priority, blocker

**Bug class**:
The kind of problem a Finding is (for example "unescaped user input"), so every place it occurs is fixed together.
_Avoid_: category, type
