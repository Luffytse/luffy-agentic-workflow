---
name: implement-spec
description: "Build one Spec as its Spec thread: Implementer subagents build its Tickets test-first in local worktrees off one Spec branch, each Ticket passes a ticket check and is squash-merged in, you open the Spec pull request with pr as a draft after the first Ticket lands, then run the code-review Rounds once the last has landed, and merge it into main with a merge commit or bring it to the user. Use when you are handed a Spec (the result of to-spec and to-tickets) to build and ship."
---

You are the **Spec thread**: you coordinate one Spec from its tickets to a merged pull request (ADR 0004, ADR 0005). **Implementers write the code.** You make the worktrees, brief the Implementers, check their evidence, run the ticket checks and the Review, merge, talk to the user. You never write or edit code yourself, not even to resolve a merge conflict.

The issue tracker should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them, so there is always a **frontier** of tickets whose blockers have all landed.

Start every subagent with a fresh context window. Keep communication to and from subagents sparse: pass **context pointers** (the spec, tickets, notes, commits), never copies of what a pointer already gives. Run Implementers in the background, so the frontier is built at the same time. Give trivial jobs, such as rerunning a test suite, to a cheap subagent.

## 1. Read the spec and its tickets

Fetch the spec and every ticket under it from the issue tracker and state the spec's title. If the reference is ambiguous, ask.

- If it is a lone Ticket (under no Spec), stop and use `implement` instead.
- Map the blocking edges into the task graph. If a blocker outside the spec is not merged, stop and tell the user (or the coordinator) which.

Start at `docs/index.md` and open only the docs that fit (with no index, fall back to `GLOSSARY.md` or `GLOSSARY-MAP.md`, and `docs/adr/`).

Optionally, start an **exploration subagent** for what the tickets need explored (codebase files, external docs). It saves its notes as Markdown in a directory outside the repo, so every later subagent can read them and Implementers can focus on building.

Done when you have stated the title, know the graph and the frontier, and know each ticket's **Model tier** (its "Model tier" line, set by `to-tickets`; regular if it has none).

## 2. Make the Spec branch

Create the Spec branch from an up-to-date main and push it. Keep your own checkout on it: any Implementer working on the Spec branch itself (steps 6.1 and 7) works there, and while one does, you run no git commands that change that checkout (merge, squash, commit, checkout); `git worktree add` and `git worktree remove` are fine. Here and below, "fetch main" means `git fetch origin main`; merge, diff and compare against `origin/main` (also as `code-review`'s `<base>`), never a local `main` that may be stale. Done when the branch exists on the remote.

## 3. Start an Implementer per frontier ticket

Run at most **3 Implementers at once**, counting every Implementer that is working: building a ticket, fixing Findings or conflicts, or on the Spec branch. Before starting or resuming one, wait for a free slot. For each frontier ticket, when a slot is free:

1. Make its worktree yourself: `git worktree add <path> -b <ticket-branch> <spec-branch>`, with `<path>` outside your checkout. Claude Code's own subagent worktrees start only from the default branch or HEAD, so don't use them. The Ticket branch stays local and is **never pushed** (the cloud's GitHub connection cannot delete branches, so pushed ones would pile up).
2. Start one Implementer on the ticket's tier. Brief it with pointers, not copies:
   - the ticket link, its worktree path and Ticket branch, and that it commits there and never pushes;
   - start at `docs/index.md`, plus the exploration notes if any;
   - the worktree is a fresh checkout and may need its dependencies installed again;
   - build test-first with the `tdd` skill, at seams agreed before the first test;
   - before reporting, merge the Spec branch tip into its Ticket branch (a merge, never a rebase) and rerun the tests;
   - report its evidence: the tests that fail before and pass after, the typecheck or the repo's checks, screenshots for anything visual (or "not visual"), and its one-way-door call (would reverting its commits undo everything the change did, including anything outside git?).

Keep that same Implementer for every later fix and merge conflict on its ticket: continue it by message. If it can no longer be reached, start a new one on the same tier with a handoff (ticket, worktree, branch, what is done, what is open), and tell the user you did. If the machine was reclaimed, the worktree and its unpushed work are gone: redo the ticket from step 3.1.

## 4. Check the evidence

Read the Implementer's report against the ticket's acceptance criteria and rerun the checks in its worktree (a cheap subagent can). Anything missing or failing goes back to the Implementer. Done when every acceptance criterion has evidence and the checks pass on the Ticket branch's head, or, when the repo has no checks, the evidence says what was checked instead.

## 5. Run the ticket check

Run the `code-review` skill yourself, from the ticket's worktree, as a Ticket check: Quick depth, over the Ticket branch's diff against the Spec branch. Its rules for ids, the comment and already-raised Findings are in [code-review's ROUNDS.md](../code-review/ROUNDS.md#ticket-checks). Record each check as a comment on the Spec pull request; until the draft opens (step 6), keep the comments and post them once it does.

Send the check's Important Findings and "fix" Nits to the ticket's Implementer; it fixes and commits, and you rerun step 4 and then a new check with brand-new reviewers. "Skip" Nits are dropped; Pre-existing ones wait for step 7.

Done when a check leaves no Important open. At most 3 checks: if the third still has an Important open, bring the ticket to the user and start no tickets that it blocks. The tickets it does not block still land, and the Spec pull request stays a draft, with no Rounds, until the user decides.

## 6. Land the ticket

Land one ticket at a time, and none while an Implementer is working on the Spec branch itself.

1. Fetch main. If it moved, merge main into the Spec branch (a merge, never a rebase). If that conflicts, abort it and start a **new** Implementer on the Spec branch, on the highest tier of the tickets whose files conflict (regular if none), to merge and resolve.
2. If the Spec branch moved since the Implementer last merged it in, have it merge the tip in again and rerun its tests. Conflict resolutions from this re-merge need no new ticket check: the Spec pull request's Rounds 1 and 2 cover the whole pull request and review them.
3. Squash-merge the Ticket branch into the Spec branch as one commit (no pull request), with a message that summarises the ticket and names it. **Push the Spec branch straight away.**
4. Remove the worktree (`git worktree remove <path>`) and delete the local Ticket branch.
5. After the first ticket lands, write the body with the `pr` skill and open the Spec pull request as a **draft**: it closes the spec and every ticket, carries each ticket's evidence in its Evidence section, and its Door is one-way if any ticket's call is. Then post the ticket-check comments kept from step 5. After each later ticket, update the body.
6. Start Implementers (step 3) on any tickets this unblocked.

Done when every ticket has landed. Then mark the pull request ready. If every ticket that can land has landed and the rest wait on the user, go to step 9 and report instead; if no ticket landed, open no draft and put the kept check comments in that report. A ticket the user drops comes out of the task graph.

## 7. Review in Rounds

Run the `code-review` skill on the Spec pull request yourself, in this thread: its Finders and Verifiers are subagents, and a subagent cannot start them. Its rules set the Review depth (a depth in your brief wins), the Rounds, the stop rule and the 5-Round cap; ticket-check Findings count as already raised.

Before each Round, fetch main and, if it moved, merge it into the Spec branch as in step 6.1, and push. In a Round that reviews only the new commits, that merge counts among them, but only its conflict resolutions are reviewed, not the commits from main (for example `git show --remerge-diff <merge>`); say so to the Finders.

After each Round, send its Important Findings and "fix" Nits to a **new** Implementer on the Spec branch, on the highest tier of the tickets those Findings touch (regular if they touch no ticket's files); it fixes, commits and pushes, then the next Round runs. A later Round may continue it by message if its Findings need no higher tier. On a clean Round 2 to 5, the Implementer makes the final "fix" Nits commit before you post that Round's comment; no further Round reviews it. After the last Round, file the Pre-existing Findings, the ticket checks' included, as `code-review` says.

Done when a Round 2 to 5 is clean, or the 5-Round cap is hit.

## 8. Merge, or bring it to the user

Bring the pull request to the user, and do not merge it, if any of these holds:

- the Review ran at Deep depth;
- its Door is one-way (any ticket's one-way call makes it so);
- it changes an ADR, the glossary, a `CLAUDE.md`, a `REVIEW.md` or the `code-review` skill;
- the Review hit the 5-Round cap.

The user then merges, or tells you to. Otherwise merge it yourself once the Review is clean and CI is green (or the repo has no CI):

1. Fetch main. If the Spec branch lacks commits from main, merge main in as in step 6.1. If that merge had conflicts, run one more Round over its conflict resolutions (step 7) if the 5-Round cap allows; otherwise bring the pull request to the user. Rerun the checks on the branch's head and wait for CI (if the repo has any).
2. Merge into main with a **merge commit**, not a squash, so main keeps each ticket as its own commit. If the tracker does not close work through pull requests (local files), mark the spec and each ticket done.

## 9. Clean up and report

Remove any worktrees left (`git worktree list`, `git worktree remove`, `git worktree prune`) and their local Ticket branches. Tell the user (or the coordinator) the pull request link and the outcome: merged with its merge commit, or waiting for the user and why, plus any ticket brought to the user in step 5.
