---
name: implement-spec
description: "Build one Spec as its Spec thread: Implementers build its Tickets, then Spec pull request, review, merge. Use when you are handed a Spec (the result of to-spec and to-tickets) to build and ship."
---

You are the **Spec thread**: you coordinate one Spec from its Tickets to a merged pull request. **Implementers write the code.** You make the worktrees, brief the Implementers, check their evidence, run the Ticket checks and the review, merge and talk to the user. You never write or edit code yourself, not even to resolve a merge conflict. You run on the regular tier whatever the Spec or its Tickets say; each Implementer runs on its own Ticket's tier. Read the project's issue-tracker doc before any tracker operation; if there is none, tell the user to run `setup-dev-skills`.

The Tickets are a **task graph** with blocking edges, not a list of steps, so there is always a **frontier** of Tickets whose blockers have all landed. Start every subagent with a fresh context and pass it **context pointers** (the Spec, Tickets, notes, commits), never copies. Run Implementers in the background, so the frontier is built at the same time. Give trivial jobs, such as rerunning a test suite, to a cheap-tier subagent.

**When you need the user.** Ask: do I already know exactly what I will do once the user says yes?

- **Yes: it is an action** (an approval to run on their device, a step the environment refuses, a credential, a merge that is theirs). Ask once, as soon as you know it, naming the exact action. Comment on the Ticket that you wait and for what, and tell the coordinator if one runs. Go on with everything that does not depend on it, then wait. The Ticket is not parked.
- **No: it is a decision** (the Ticket cannot be built as written, or a choice it does not settle would change what was agreed or cannot be undone). Push your work, park the Ticket with the tracker doc's **Park** operation, giving the question, the options and your recommendation, tell the user (or the coordinator) and stop. The user's answer lifts the park.

In a Spec, a Ticket parked on a decision leaves the frontier and the other Tickets go on; "stop" is that Ticket's. A Ticket blocked by a **setup Ticket** (one at the `ready-for-human` role, waiting for the person to provide something) is passed over the same way and built once that Ticket closes. When only parked Tickets, and the Tickets they block, are left, park the Spec with the same question and stop. Nothing is merged in part: the Spec pull request merges only once every Ticket of its graph has landed or the user has dropped it (taken it out of the graph). A choice inside what the Spec agreed that can be undone is yours: make it and name it in the pull request.

## 1. Read the Spec and its Tickets

Fetch the Spec and every Ticket under it and state the Spec's title; if the reference is ambiguous, ask. A lone Ticket goes to `implement`. If you were handed one Ticket under a Spec, say so to whoever handed it to you and stop: a Spec's Tickets are built by its Spec thread.

- Map the blocking edges with the tracker doc's **Count open blockers** operation. A blocker outside the Spec still open stops you (tell the user, or the coordinator, which), unless it is a setup Ticket: then pass over only the Tickets it blocks.
- Read with **Park** whether the Spec or a Ticket is parked. A parked Spec: stop and tell the user (or the coordinator). A parked Ticket is not on the frontier, and the Tickets it blocks stay blocked while it is open. A Ticket at the `ready-for-human` role is not on the frontier either; it counts as landed when the person closes it as completed.
- A Ticket is **landed** when the pushed Spec branch or main holds its squash commit (the message names the Ticket), or a merged pull request's body closes it. A landed Ticket is never rebuilt or checked again.
- On every entry, fetch the Spec branch if it exists and read the tracker before starting anything: each Ticket's state and comments, and the Spec pull request with its Ticket-check comments.
- If the Spec's comments show another thread building it that your brief does not say you replace, stop and ask the coordinator, or the user when none runs.
- Note each Ticket's **Model tier** line (regular if it has none).

Optionally, start an exploration subagent for what the Tickets need explored; it saves its notes as Markdown outside the repo, for every later subagent to read.

### Check against main

Before you make anything, on every entry, read the Spec and each Ticket not landed against freshly fetched main: its code and docs, and what merged since it was written. This Spec's own branches and pull request are not evidence. Give the Spec one verdict:

- **still valid**: go on.
- **already fixed** or **obsolete**: write no code. Give the coordinator (the user, when none runs) the evidence on main, the file and the commit or pull request, and stop; it closes or re-plans the Spec.
- **changed scope** (main already has part of it included) or **cannot tell**: give the coordinator what changed or what is missing, with the same evidence, comment on the Spec that you wait for its answer, and build nothing. With no coordinator it is a decision for the user: park the Spec as "When you need the user" says. On the answer, or the lifted park, re-enter at step 1, checking again only what merged since.

## 2. Make the Spec branch

Create the Spec branch from freshly fetched main and push it; on re-entry, use the pushed one. Keep your own checkout on it: an Implementer working on the Spec branch itself works there. "Fetch main" means `git fetch origin <default-branch>`; merge, diff and compare against `origin/<default-branch>` (also the review's base), never a local `main`.

**Nobody moves a checkout an Implementer works in.** While an Implementer works in your checkout or a Ticket worktree, run there nothing that moves or changes it (checkout, switch, stash, reset, merge, squash, commit); `git worktree add` and `git worktree remove` are fine. Read a branch by fetching and `git show` or `git diff`, or `git archive` it into a scratch directory. Every reviewer and cheap subagent you start keeps the same rule.

## 3. Start an Implementer per frontier Ticket

Run at most **3 Implementers at once**, counting each one that is working: building a Ticket, fixing Findings or conflicts, or on the Spec branch. For each frontier Ticket not landed, when a slot is free:

1. Make its worktree yourself, outside your checkout: `git worktree add <path> -b <ticket-branch> <spec-branch>` (Claude Code's own subagent worktrees start only from the default branch or HEAD, so don't use them). The Ticket branch stays local and is never pushed. On re-entry, a local Ticket branch left by an earlier thread for a Ticket not landed is reused: add the worktree on it, have its Implementer merge the Spec branch tip in first, and brief it with a handoff (what is done, what is open); a landed Ticket's leftover waits for step 9.
2. Start one Implementer on the Ticket's tier (load `model-tiers` by name for the model; the project's own tier map overrides it). Brief it with:
   - the Ticket link, its worktree path and Ticket branch; it commits there and never pushes, runs every git command as `git -C <path> ...`, and checks before each commit that `git status -sb` shows its Ticket branch;
   - start at `docs/dev-skills/index.md`, plus the exploration notes if any; the worktree is a fresh checkout and may need its dependencies installed;
   - build test-first with `tdd`, at seams agreed before the first test; each new test is run and seen failing before the fix, never inferred;
   - wait for a slow check (a test suite, a build) in the same turn, and report only once it has finished;
   - a criterion whose run needs tools it does not hold (a recorded run only the top-level session can make): build the rest and report that criterion as **owed**;
   - before reporting, check its diff against each Always-check line of the repo's review rules file, if any, then merge the Spec branch tip in (a merge, never a rebase) and rerun the tests;
   - report its evidence: each new test's failure and pass, the repo's checks, screenshots for anything visual (or "not visual"), and its one-way-door call (would reverting its commits undo everything the change did, including anything outside git?).

Keep that Implementer for every later fix and conflict on its Ticket, continuing it by message. If it can no longer be reached, start a new one on the same tier with a handoff, and tell the user. If the worktree and the Ticket branch are both gone (the machine was reclaimed), the unpushed work is gone: redo the Ticket from step 3.1.

## 4. Check the evidence

Read the report against the Ticket's acceptance criteria and rerun the checks in its worktree (a cheap subagent can). Anything missing or failing goes back to the Implementer. For a criterion reported as owed, make the run yourself (it is evidence, not code) and message the Implementer the output as observed to record; a run that fails or contradicts the entry goes back as a fix, and after any fix that could change what it showed, make it again. A run you cannot make either is an action for the user. Done when every criterion has evidence and the checks pass on the Ticket branch's head (or, with no checks, the evidence says what was checked).

## 5. Run the Ticket check

Run `agentic-review`'s Ticket check in this thread: one Quick Round, as `review-rounds` says, on the Ticket branch against the Spec branch. Supply the Ticket and Spec, the worktree path and branch, the Spec branch as base, and any earlier Ticket-check Findings on this Ticket. Record it on the Spec pull request; until the draft opens, keep the comment and post it once it does.

Route its open Importants and "fix" Nits to the Ticket's Implementer, which fixes and commits or disputes a Finding with its evidence; then step 4 again. Done when each open Important is fixed or disputed: the Ticket lands, and the Spec pull request's Round 1 carries the check's open Findings and decides them.

## 6. Land the Ticket

Land one Ticket at a time, and none while an Implementer works on the Spec branch itself.

1. Fetch main. If it moved, merge it into the Spec branch (a merge, never a rebase). On a conflict, abort and start a **new** Implementer on the Spec branch, on the highest tier of the Tickets whose files conflict (regular if none), to merge and resolve. Brief it, as every Spec-branch Implementer, to check before each push that `git status -sb` shows the Spec branch, and to report afterwards that `git rev-parse origin/<branch>` equals `HEAD`.
2. If the Spec branch moved since the Implementer last merged it in, have it merge the tip again and rerun its tests; the Spec pull request's Round 1 reviews those resolutions.
3. Squash-merge the Ticket branch into the Spec branch as one commit, with a typed title (`<type>: <summary>`, as `pr` says, or the repo's own title convention) and a message that summarises the Ticket and names it. Push the Spec branch at once.
4. Remove the Ticket's worktree (`git worktree remove <path>`). Keep its local Ticket branch until step 9.
5. After the first Ticket lands, write the title and body with `pr` and open the Spec pull request as a **draft**: one `Closes` line for the Spec and for each landed Ticket, and for the sources they absorb (load `issue-absorption`), each Ticket's evidence, and a one-way Door if any Ticket's call is. Post the kept Ticket-check comments. Add each later Ticket's lines when it lands. When the user drops a Ticket, remove its lines and those of its sources at once; you never close a dropped Ticket as completed.
6. Start Implementers (step 3) on the Tickets this unblocked.

Done when every Ticket that can land has landed. When all of the graph has, mark the pull request ready. When the rest wait on the user or a setup Ticket, report as step 9 says and stay open; if none landed, open no draft and put the kept check comments in that report.

## 7. Review

Run `agentic-review` on the Spec pull request in this thread: its Round 0 picks the level and, above None, hands over to `review-rounds`. Supply the Spec and Tickets, the pull request, your checkout's path and the Spec branch, the base, any level the user asked for, and every Ticket-check record. Before each Round, fetch main and merge it as in step 6.1, and push.

Route each Round's open Importants and "fix" Nits to a **new** Implementer on the Spec branch, on the highest tier among the Tickets whose files they touch (regular if none), briefed as in step 6.1 and with a handoff of any owed criterion. It fixes, commits and pushes, or disputes a Finding with its evidence, as `review-rounds` says; a later Round may continue it by message if it needs no higher tier. After a fix that could change an owed run, make the run again (step 4) before the next Round. After Round 3, report each bug Ticket its sort filed; you build none of them.

## 8. Merge

Load `merging` by name and follow it to its end. Give it the Spec pull request and the Spec it builds (the Spec and the landed Tickets as the issues to close, where the tracker has no pull-request closing support); the method, a **merge commit** titled with the pull request's typed title, so main keeps each Ticket as its own commit (`merging` applies the repo's own merge rule where it names one); a Spec-branch Implementer as the committer, briefed as in step 6.1; and no pre-merge step of your own.

## 9. Clean up and report

Once the Spec pull request has merged, remove what is left (`git worktree list`, `git worktree remove`, `git worktree prune`) and delete the local Ticket branches. Until then delete nothing, a dropped Ticket's branch included: while you wait on the user every branch is kept.

Tell the user (or the coordinator) the pull request link and the outcome as `merging` hands it back: merged with its merge commit, or with the user and what stops it, with each bug Ticket the review filed and each Ticket still waiting. A report of waiting is not your end: stay open and re-enter at step 1 on the answer, the lifted park or the closed setup Ticket. If the pull request is with the user, once they merge it or tell you it is merged, run `merging`'s "After the merge", then clean up and go to step 10; if they close it unmerged, ask whether they want a retro.

## 10. Run the retro

Run `retro` once the Spec pull request is merged and the Spec and its landed Tickets are closed; it files issues and builds nothing.
