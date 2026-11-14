# Building: Specs, Tickets and build threads

The words of building one Spec or Ticket and merging it. Each entry says what a word means; the rule's steps stay with the skill or doc it names.

## Language

**Spec**:
The written design of one feature: the problem, user stories, decisions, testing and what is out of scope. It is one GitHub issue.
_Avoid_: PRD, design doc

**Ticket**:
One small, end-to-end slice of work, built and reviewed on its own. Either part of a Spec (a sub-issue of it) or a **lone ticket** under no Spec.
_Avoid_: task, story

**Build thread**:
A project thread that builds a Spec or a lone Ticket: a Spec thread or a Ticket thread. Before it makes anything, on every entry, it makes the **Build check**.

**Build check**:
The check against main a **Build thread** makes on its own issue before it makes anything, on every entry (`implement` and `implement-spec` step 1): the issue read against freshly fetched main, with the **Main check**'s verdicts; the thread's own branches and pull request are not evidence. It catches a merge that fixed or changed an issue after it was planned in; what each verdict does is that step's (ADR 0004).
_Avoid_: validity check, pre-build triage

**Spec thread**:
A project thread that builds one Spec with `implement-spec`. It owns the Spec by an **owner record**: a comment on the Spec naming its thread and how to reach it, left before it builds, so a second thread entering the Spec stops while the first runs.

**Ticket thread**:
A project thread that builds one lone Ticket with `implement`.

**Implementer**:
A subagent that builds a Ticket test-first and fixes its Findings. Build threads coordinate; Implementers write the code (ADR 0004). What it checks and reports before it hands back is in the Implementer brief of `implement` and `implement-spec`.
_Avoid_: coder, worker

**Spec branch**:
The long-lived branch a Spec is built on. Its Tickets are squash-merged into it, and it merges into main with a merge commit (ADR 0005).
_Avoid_: integration branch, feature branch

**Ticket branch**:
The branch one Ticket is built on. A Spec's Ticket branches start from the Spec branch and stay inside the thread; a lone Ticket's branch starts from main and is pushed.

**Ticket check**:
One Quick Round over a Spec's Ticket branch, against the Spec branch, before the Ticket joins it, recorded on the Spec pull request. Its open Findings carry into the Spec pull request's Round 1. Not one of the Spec pull request's Rounds.

**Merging**:
The `merging` Base skill, hidden from the menu: the finish of one pull request that is ready to merge. It decides who merges from the **Boundary record** alone (none means an empty one), runs the repo's merge-time steps, syncs with main, merges, confirms the merge on the tracker and closes the issues. `implement`, `implement-spec` and `release` load it at their merge step, and `review-rounds` defines a boundary crossing by it.
_Avoid_: merge step (a caller's step that loads it), auto-merge
