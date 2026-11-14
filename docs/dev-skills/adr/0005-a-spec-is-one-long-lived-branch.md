# A spec is one long-lived branch; tickets squash into it

Each spec is built on its own **spec branch** off main. Each ticket under it is built on a **ticket branch** off the spec branch, in its own git worktree so several Implementers can work at the same time. A finished ticket (tests passing, its ticket check's Findings fixed or disputed, see [ADR 0004](0004-build-threads-coordinate-and-subagents-code.md)) is squash-merged into the spec branch as one commit, with no pull request, and the thread pushes the spec branch straight away. The full review happens on the spec's pull request. That pull request opens as a draft when the first ticket lands, is marked ready once every ticket left in the task graph has landed (a dropped ticket leaves the graph; if the remaining tickets wait on the user, it stays a draft and the thread reports), then gets the review of [ADR 0003](0003-code-review-runs-find-verify-rank-in-rounds.md), closes the spec issue and every ticket that landed on it (a dropped ticket's `Closes` line is removed, so it is never closed as completed), and merges into main with a **merge commit**, so main keeps each ticket as its own commit. A lone ticket works on its own branch off main and squash-merges into main, the squash commit taking the pull request's typed title and its body as the message.

A spec's ticket branches stay inside the build thread and are never pushed; only spec branches and lone-ticket branches go to GitHub. Before each ticket merge and before each Round, the spec thread fetches main; if it moved, the thread merges main into the spec branch, with an Implementer resolving any conflicts; it never rebases, so ticket worktrees started from the spec branch stay valid. For Rounds 2 and 3, which review only new commits, such a merge counts among them, but only its conflict resolutions are reviewed, not the commits that came from main.

Amended 2026-11-03 (Spec #555): a section here described restarting a spec on a fresh spec branch when its review would not settle (2026-11-02, Spec #400). The review no longer has attempts or a restart ([ADR 0003](0003-code-review-runs-find-verify-rank-in-rounds.md)), so the section is removed.

Amended 2026-11-03 (#513): a Ticket that carries another coding agent's agent-only label is built by that agent on the same spec branch, not by the spec thread and not through a pull request to main. The spec thread hands it off with a comment on the Ticket and keeps the spec pull request, its review and its merge; the other agent builds the Ticket off the pushed spec branch, runs its ticket check, squash-merges it into the spec branch and pushes, and the spec thread reads that check instead of repeating it. The spec pull request does not merge until that Ticket has landed or the user drops it. If the spec closed with such a Ticket still open, the spec is reopened and the remaining Tickets reach main through a continuation spec pull request on a spec branch of the same name, recreated from main.

*Amendment note, 2026-11-14, Ticket #154 (Spec #151).* The amendment of 2026-11-03 (#513) above no longer applies: the plugin is Claude Code only for now (ADR 0001), the agent-only label role is gone, and `implement-spec` has no continuation path. Every Ticket of a Spec is built by its Spec thread on the spec branch, and a thread handed one Ticket under a Spec says so and stops.

## Why

- A live test in a cloud thread (2026-10-29) showed two subagents can each work in their own worktree off a spec branch, commit, and be squash-merged back, in parallel.
- Claude Code's built-in worktree option for subagents starts only from the default branch or the current HEAD, never from a named branch, so `implement-spec` creates ticket worktrees itself with `git worktree add` from the spec branch.
- The cloud's GitHub connection refuses to delete branches, so pushed ticket branches would pile up. Keeping them local avoids that. The cost: if the cloud machine is reclaimed mid-ticket, that ticket's unfinished work is lost and is redone.

## Consequences

- The repo should turn on GitHub's "Automatically delete head branches", so merged spec and lone-ticket branches clean themselves up.
- Each worktree is a full checkout, sharing the thread's 30 GB disk, and may need its dependencies installed again.
