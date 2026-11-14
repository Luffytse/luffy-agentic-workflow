---
name: merging
description: "Finish a pull request that is ready to merge: decide from the Boundary record who merges, check its review record, merge, close its issues. Use when a build or release workflow reaches its merge step, or must decide if an action crosses a boundary."
user-invocable: false
---

# Merging

The finish of one pull request, from ready to merge to closed issues. The caller loads this skill at its merge step, follows it to the end, then goes on with its own report. Tracker reads, the merge and closes go through the project's configured tracker doc: this skill owns what they mean and when they happen, not their commands.

## Caller inputs

The caller names:

- **the pull request**, and the issue it builds, or none;
- **the merge method**: a squash or a merge commit, and its title: the pull request's typed title, as `pr` writes it, or the repo's own title convention where its rules set one. Where the repo's rules name a merge method, that one wins over the caller's;
- **who commits**: who makes each commit the finish needs (a merge of main, a conflict resolution). A caller that writes no code names its Implementer, and its worktree where it has one;
- **its own pre-merge step**, if any; it runs first in "Before the merge", every time that part runs.

## Who merges

Read the Boundary record (`docs/dev-skills/boundaries.md`). With no Boundary record, read an empty one: no irreversible action is allowed to agents and no action needs the user's approval. The record applies exactly as written to every pull request, inside a Milestone or not; it is the only source of boundaries (a Milestone issue holds none of its own).

Something **crosses a boundary** when it takes, or its merge would take, an action the Boundary record says needs the user's approval; or when its Door is one-way and the record does not allow agents to take each of its irreversible actions; or when it goes past a budget or other limit the record sets. A fix, a design answer or a bug Ticket crosses a boundary the same way a pull request does.

Bring the pull request to the user, and do not merge it, only if it crosses a boundary, or the repo's own rules (its `CLAUDE.md` or `AGENTS.md`, the project instructions, its docs) say a person merges it. Otherwise you merge it, once it is ready and CI is green (or the repo has no CI). A Deep review alone does not stop the merge, and neither does a change to an ADR, the glossary, a `CLAUDE.md`, an `AGENTS.md` or a `REVIEW.md`.

## The `Agent-merged rules:` line

When you merge such a change yourself, or a pull request on which an agent answered design Findings (`review-rounds` lists them, each by its row id and the link to its record), add one line to the pull request body before the merge:

`Agent-merged rules: <files>; design answers: <id> <link>, ...`

It names each ADR, glossary, `CLAUDE.md`, `AGENTS.md` and `REVIEW.md` file the pull request changes and each agent design answer on it; leave out a part that has none. The caller's report names the same items.

## Bringing it to the user

Name what stops the merge: the boundary (the action, as the Boundary record lists it), the repo rule (and the file it is in), or the Finding whose answer the review waits on. The user then merges, or tells you to.

"Before the merge" runs last, just before any merge, the user's too. When the user tells you to merge, run it, then merge; when the user will merge it themselves, ask them to tell you first. Either way, when the user merges or reports merging it, run "After the merge" then.

## Before the merge

1. Run the caller's own pre-merge step, if it named one.
2. **Check the review record.** A pull request with no review, such as a changelog pull request, is ready when its checks pass. For one that had a review, read its latest Round comment as `review-record` gives it. It is ready only when that comment's Result reads `clean` or `sorted after Round 3`, and the pull request's current head is the `head` the comment names, or is ahead of it only by:
   - a merge of main that had no conflict;
   - the one last commit of "fix" Nits that `review-rounds` has the owner make after a clean Round;
   - a merge of main with conflicts that a later resolutions check covers, with no open Important.

   A Result reading `waiting on a boundary` counts as `clean` only when the merge was what waited and the user's answer is on the pull request after that comment. A Round 0 comment at level None on the current head has no Result line and counts as ready by its checks. In any other case do not merge: go back to the caller's review step.
3. **Check the closing lines.** The pull request's body carries a `Closes #<n>` line for each issue the caller names as built by it, and for each source it absorbs (as `issue-absorption` says); add any missing one by editing the body.
4. **Sync with main.** Fetch main. If the branch lacks commits from main, the committer merges main in (a merge, never a rebase) and pushes. A merge with conflicts has its resolutions reviewed as `review-rounds` says under "Merges from main"; a merge without conflicts needs only the checks.
5. Rerun the checks on the branch's head, in the committer's worktree where it has one, and wait for CI (if the repo has any).
6. If main moves again before the merge, repeat this part from 1.

## The merge

Merge into main with the tracker doc's **Merge a PR** operation, with the method and title above. For a squash, the commit message is the pull request's body as it stands then, not the branch's commit messages joined together. For a merge commit, the title replaces the tracker's default one. A merge the environment refuses is an action for the user: ask once, naming the exact merge, and wait.

## After the merge

1. **Confirm the merge on the tracker.** Read the pull request's merged state with the tracker doc's **Read whether a PR merged** operation, and require it to read merged, including when the user reports merging it. A report alone, a failed read or any other result does not authorize closing: close nothing, and tell the user what the tracker shows.
2. Read the pull request's body and, with the tracker doc's operations, the state of each issue its closing lines list. For absorbed sources, load `issue-absorption` and recheck closure eligibility. For each eligible issue still open, use the tracker doc's **Close** operation with a completed outcome and an explanation naming the pull request. A tracker without pull-request closing support uses its configured completion operation for the issues the caller names instead.
3. If a read or close fails, stop and tell the user; do not treat it as closed.

Done when the pull request is merged and its eligible issues are closed, or it is with the user and you have named what stops it; then "After the merge" waits for the user's merge or report. Hand the outcome back to the caller for its report: merged with its commit, or with the user and why, and the items of the `Agent-merged rules:` line.
