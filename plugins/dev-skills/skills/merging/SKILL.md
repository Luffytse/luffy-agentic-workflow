---
name: merging
description: Finish a pull request that is ready to merge: decide from the Boundary record whether you merge it or bring it to the user, write the `Agent-merged rules:` line, run the repo's merge-time steps, sync with main, merge with the caller's method, then confirm the merge and close its issues. Use when a build or release workflow reaches its merge step, or must decide whether an action crosses a boundary.
user-invocable: false
---

# Merging

The finish of one pull request, from ready to merge to closed issues. The caller loads this skill at its merge step, follows it to the end, then goes on with its own report. Tracker reads, the merge and closes go through the project's configured tracker doc: this skill owns what they mean and when they happen, not their commands.

## Caller inputs

The caller names:

- **the pull request**, and the issue it builds; for a pull request that builds no issue, the origin its body records (such as a `Retro origin:` line), or none;
- **the merge method**: a squash or a merge commit, and its title: the pull request's typed title, as `pr` writes it, or the repo's own title convention where its rules set one;
- **who commits**: who makes each commit the finish needs (a merge of main, a conflict resolution, a commit a merge-time step asks for). A caller that writes no code names its Implementer;
- **what makes it ready**: a review that ended ready to merge, or, for a pull request with no review, its checks passing;
- **its own pre-merge step**, if any; it runs first in "Before the merge", every time that part runs.

## Who merges

Read the Boundary record (`docs/dev-skills/boundaries.md`). With no Boundary record, read an empty one: no irreversible action is allowed to agents and no action needs the user's approval. The record applies exactly as written to every pull request, inside a Milestone or not; it is the only source of boundaries (a Milestone issue holds none of its own).

Something **crosses a boundary** when it takes, or its merge would take, an action the Boundary record says needs the user's approval; or when its Door is one-way and the record does not allow agents to take each of its irreversible actions. A fix, a design answer or a bug Ticket crosses a boundary the same way a pull request does.

Bring the pull request to the user, and do not merge it, only if any of these holds:

- it crosses a boundary;
- the repo's own rules (its `CLAUDE.md` or `AGENTS.md`, the project instructions, its docs) say a person merges it.

Otherwise you merge it, once it is ready and CI is green (or the repo has no CI). A Deep review alone does not stop the merge, and neither does a change to an ADR, the glossary, a `CLAUDE.md`, an `AGENTS.md` or a `REVIEW.md`.

## The `Agent-merged rules:` line

When you merge such a change yourself, or a pull request on which an agent answered design Findings (`review-rounds` lists them, each by its row id and the link to its record), list it: before the merge, add one line to the pull request body,

`Agent-merged rules: <files>; design answers: <id> <link>, ...`

naming each ADR, glossary, `CLAUDE.md`, `AGENTS.md` and `REVIEW.md` file the pull request changes and each agent design answer on it. Leave out the files part, or the design-answers part, when there is none. The caller's report names the same items.

## Bringing it to the user

Name what stops the merge, so the user can decide quickly: the boundary (the action, as the Boundary record lists it), the repo rule (and the file it is in), or the Finding whose fix or answer the review is waiting on. The user then merges, or tells you to.

"Before the merge" runs last, just before any merge, the user's too. When the user tells you to merge, run it, then merge. When the user will merge it themselves, ask them to tell you first, so you can run it before they do. Either way, when the user merges or reports merging it, run "After the merge" then.

## Before the merge

1. Run the caller's own pre-merge step, if it named one.
2. **Follow the repo's merge-time steps.** Read the repo's own docs for steps to take just before a merge (its `CLAUDE.md` or `AGENTS.md`, and the release doc, `docs/dev-skills/release.md`) and take each one, in the order they give. A step that waits for something, such as a number, waits for it; a commit a step asks for is made by the committer the caller named. Take only the steps those docs give: where they give none, there is none.
3. **Sync with main.** Fetch main. If the branch lacks commits from main, the committer merges main in (a merge, never a rebase) and pushes. If main was merged since the last Round's recorded head and that merge had conflicts, its resolutions are reviewed as `review-rounds` says under "Merges from main" (the next Round, or after Round 3 its one resolutions check, whose open Importants become bug Tickets); a merge without conflicts needs only the checks.
4. Rerun the checks on the branch's head, and wait for CI (if the repo has any).
5. If main moves again before the merge, repeat this part from 1. What a repeat keeps or redoes of a merge-time step's commit is the repo's docs' to say.

## The merge

Merge into main with the tracker doc's **Merge a PR** operation, with the caller's method and title. For a squash, the commit message is the pull request's body, as it stands then, rather than the branch's commit messages joined together. For a merge commit, the title replaces the tracker's default one. A tracker doc with no such operation was written before it: merge as the tracker's own docs say, and tell the user to re-run `setup-dev-skills`.

## After the merge

1. **Confirm the merge on the tracker.** Read the pull request's merged state with the tracker doc's **Read whether a PR merged** operation (or, in a tracker doc without it, its pull-request read), and require it to read merged, including when the user reports merging it. A report alone, a failed read or any other result does not authorize closing: close nothing, and tell the user what the tracker shows.
2. Read the pull request's body and, with the tracker doc's operations, the state of each issue its closing lines list. For absorbed sources, load `issue-absorption` and recheck closure eligibility. For each eligible issue still open, use the tracker doc's **Close** operation with a completed outcome and an explanation naming the pull request. A tracker without pull-request closing support uses its configured completion operation for the issues the caller names instead.
3. If a read or close fails, stop and tell the user; do not treat it as closed.

Done when the pull request is merged and its eligible issues are closed, or it is with the user and you have named what stops it; then "After the merge" waits for the user's merge or report. Hand the outcome back to the caller for its report: merged with its commit, or with the user and why, and the items of the `Agent-merged rules:` line.
