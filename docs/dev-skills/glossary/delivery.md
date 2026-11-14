# Building: Milestones and delivery

Where the skills run, what a Milestone is, and the words of delivering one: the team lead, its workers and what it does when one stalls. Each entry says what a word means; the rule's steps stay with the skill or doc it names.

## Language

**Project thread**:
One task's Claude session inside a Claude project. A **coordinator** (the project's own Claude) starts each thread with a brief, so nobody types slash commands there; to deliver planned work it runs the **Team lead** skill.
_Avoid_: chat, conversation

**Milestone**:
A product goal the user sets (for example "M3 Trip planning"), written down in one Milestone issue: the goal, the features to deliver by its end in build order, their acceptance criteria and what is excluded. Every plan is one (a small Release is a one-Release Milestone); it holds one or more Releases, which the agents plan, and closes when the user accepts it at the Milestone review. An issue belongs to it, and its pull request is **inside the Milestone**, when the issue (for a Spec's pull request, the Spec) carries the membership label in the form the **Boundary record** names; a build thread's no-issue corrective check records `Retro origin: <issue link>`, and other pull requests that build no issue are outside. Membership plays no part in who merges (ADR 0004). Its features are named, sorted by dependency and each planned in its own session before the Milestone issue is written, and are fixed once planning settles: a feature planned later waits for the next Milestone (ADR 0017). Planning, the **Plugin version check** and the report are `milestone`'s; the **Team lead** decides when delivery stops for the Milestone review; the report is one comment that opens with about a screen of key points (the outcome, what the user must check or decide, the unplanned step-ins as a count, the next Milestone's proposals) and keeps its detail below, with time, tokens and versions one line each; delivery is the **Team lead**'s.
_Avoid_: epic, sprint

**Plugin version check**:
The one read, recorded on the Milestone issue once planning settles, of whether the plugin copy a fresh thread loads matches the plugin on the source repository's main: its manifest version, or its commit where threads load a source checkout. It gates the Milestone's delivery. Owned by `milestone`; it replaced Startup verification, whose worker probes a project no longer runs.
_Avoid_: Startup verification (the replaced check), preflight, smoke test

**Harness**:
The tool a coordinator runs its workers in, named by the way workers run there (for example a claude.ai project, whose workers are threads, or one Claude Code session, whose workers are subagents and, on desktop, other sessions). Each way has one reference file in **Worker control**. The Harness's record is the only source of a worker's state; tracker comments are an audit trail.
_Avoid_: runtime adapter, platform

**Worker control**:
The `worker-control` Base skill: it starts, checks, stops, pauses and resumes workers in the **Harness** it runs in, and arranges and ends a check-in, from one reference per Harness; deciding which work starts and when stays with its caller. How it detects the Harness and its role, and what a reference holds, are its own.
_Avoid_: harness-team (its working name), lifecycle agent

**Environment check**:
This repo's own test of the `worker-control` references: six probes (start a worker, worker state, pause and resume, confirmed stop, end or failure notice, recurring check-in) run in a cloud project and in a local Claude Code session, whose result is one comment on the Milestone issue. It tests worker control only, and no skill names it. Its doc is `docs/dev-skills/environment-check.md`; `CLAUDE.md` says when it runs.
_Avoid_: Worker control check (the earlier check inside the skill), Startup verification, smoke test

**Team lead**:
The `team-lead` skill: the role the coordinator runs to deliver planned work, always a Milestone's (ADR 0010, ADR 0012). It manages the work, not the machinery: it starts a build thread for every Release entry whose blockers have closed, with no limit of its own (a project's instructions may give one), starts Release threads, reacts to what workers and the **Harness** report, holds the **Stand-up**, **Takeover** and **Pause**, and stops delivery for the Milestone review, with every worker action through **Worker control**. "Coordinator" stays the name of the project's own agent; the team lead is what it runs, and a coordinator that cannot load the plugin's skills follows the project instructions `setup-project` assembles instead.
_Avoid_: delivery loop (the earlier `milestone` section it replaces), manager

**Stand-up**:
What the **Team lead** does at a scheduled check-in, at the **Boundary record**'s interval: the safety net for a worker that is silent but nominally working. It reads the snapshot command's row for each running build worker and acts only on rows that call for it (an unreported merged or ready pull request, a silent worker nudged once, one still silent replaced by **Takeover**); a worker recorded as waiting on the user's action is neither nudged nor replaced, and one that finds nothing writes nothing. Owned by `team-lead`.
_Avoid_: status meeting, ping

**Takeover**:
The **Team lead** replacing a stalled worker with a fresh worker on the same issue, which resumes from the pushed branch and the tracker; a silent worker is stopped first, and the stop read back from the Harness's record. A worker that ended without its result is first asked to carry on, where **Worker control** gives a way to message it. When that cannot be done safely, or the feature stalls a second time, the work is **Parked**. Owned by `team-lead`.
_Avoid_: replacement, restart

**Parked**:
The state of an issue the **Team lead** could not take over safely, whose feature stalled a second time, a setup Ticket whose second guiding thread ended with it open, or that the user parked: marked with the tracker doc's **Park** operation (the `parked` label and a comment saying why). Other work goes on; it waits on the user, who lifts it by removing the label. An open issue **waits with** a parked issue when it has at least one open blocker and each is parked, already left the Release for that reason, or itself waits with a parked issue, and a Spec and its open Tickets go together (when one of them is parked or waits with a parked issue through its blockers, the others wait with it); at a Release cut both leave the Release (`release` owns the cut), and for the Milestone review gate both count as done (`team-lead`). Owned by `team-lead`; a Review never parks (ADR 0003).
_Avoid_: stuck, shelved, deferred

**Pause**:
The user's word, to the **Team lead**, to stop spending without losing work: nothing new starts and each running worker is paused through **Worker control** until the user's word to resume. Owned by `team-lead`.
_Avoid_: freeze, halt
