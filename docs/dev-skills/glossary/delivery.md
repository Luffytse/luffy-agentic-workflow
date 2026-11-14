# Building: Milestones and delivery

Where the skills run, what a Milestone is, and the words of delivering one: the team lead, its workers and what it does when one stalls. Each entry says what a word means; the rule's steps stay with the skill or doc it names.

## Language

**Project thread**:
One task's Claude session inside a Claude project. A **coordinator** (the project's own Claude) starts each thread with a brief, so nobody types slash commands there; to deliver planned work it runs the **Team lead** skill.
_Avoid_: chat, conversation

**Milestone**:
A product goal the user sets (for example "M3 Trip planning"), written down in one Milestone issue: the goal, the features to deliver by its end in build order, their acceptance criteria and what is excluded. Every plan is one (a small Release is a one-Release Milestone); it holds one or more Releases, which the agents plan, and closes when the user accepts it at the Milestone review. An issue belongs to it, and its pull request is **inside the Milestone**, when the issue (for a Spec's pull request, the Spec) carries the membership label in the form the **Boundary record** names; a build thread's no-issue corrective check records `Retro origin: <issue link>`, and other pull requests that build no issue are outside. Membership plays no part in who merges (ADR 0004). Planning, adding a feature, Startup verification and the report are `milestone`'s; delivery is the **Team lead**'s.
_Avoid_: epic, sprint

**Startup verification**:
The check `milestone` records on the Milestone issue before a Milestone's autonomous delivery starts: the **Worker control** check, proving in this environment with short bounded **probes** that workers start, are read, pause, stop and wake the coordinator and that a check-in arrives, and the loaded-skill-version probe, proving that a fresh thread loads the plugin version on main. It ends in one Verdict, and delivery starts after a failed one only on the user's word. Its probes, evidence and reuse rules are `milestone`'s.
_Avoid_: preflight, smoke test

**Harness**:
The tool a coordinator runs its workers in, named by the way workers run there (for example a claude.ai project, whose workers are threads, or one Claude Code session, whose workers are subagents and, on desktop, other sessions). Each way has one reference file in **Worker control**. The Harness's record is the only source of a worker's state; tracker comments are an audit trail.
_Avoid_: runtime adapter, platform

**Worker control**:
The `worker-control` Base skill: it starts, checks, stops, pauses and resumes workers in the **Harness** it runs in, and arranges and ends a check-in, from one reference per Harness; deciding which work starts and when stays with its caller. Its short check proves those methods here before unattended work relies on them. How it detects the Harness and its role, and what a reference holds, are its own.
_Avoid_: harness-team (its working name), lifecycle agent

**Team lead**:
The `team-lead` skill: the role the coordinator runs to deliver planned work, always a Milestone's (ADR 0010, ADR 0012). It manages the work, not the machinery: it starts build and Release threads, reacts to what workers and the **Harness** report, and holds the **Stand-up**, **Takeover** and **Pause**, with every worker action through **Worker control**. "Coordinator" stays the name of the project's own agent; the team lead is what it runs, and a coordinator that cannot load the plugin's skills follows the project instructions `setup-project` assembles instead.
_Avoid_: delivery loop (the earlier `milestone` section it replaces), manager

**Stand-up**:
What the **Team lead** does at a scheduled check-in, at the **Boundary record**'s interval: the safety net for a worker that is silent but nominally working. It reads the snapshot command's row for each running build worker and acts only on rows that call for it (an unreported merged or ready pull request, a silent worker nudged once, one still silent replaced by **Takeover**); one that finds nothing writes nothing. Owned by `team-lead`.
_Avoid_: status meeting, ping

**Takeover**:
The **Team lead** replacing a stalled worker with a fresh worker on the same issue, which resumes from the pushed branch and the tracker; a silent worker is stopped first, and the stop read back from the Harness's record. When that cannot be done safely, or the feature stalls a second time, the work is **Parked**. Owned by `team-lead`.
_Avoid_: replacement, restart

**Parked**:
The state of an issue the **Team lead** could not take over safely, whose feature stalled a second time, or that the user parked: marked with the tracker doc's **Park** operation (the `parked` label and a comment saying why). Other work goes on; it waits on the user, who lifts it by removing the label. Owned by `team-lead`; a Review never parks (ADR 0003).
_Avoid_: stuck, shelved, deferred

**Pause**:
The user's word, to the **Team lead**, to stop spending without losing work: nothing new starts and each running worker is paused through **Worker control** until the user's word to resume. Owned by `team-lead`.
_Avoid_: freeze, halt
