---
name: implement-spec
description: "Build one Spec as its Spec thread: Implementer subagents build its Tickets test-first in local worktrees off one Spec branch, each Ticket passes a ticket check and is squash-merged in, you open the Spec pull request with pr as a draft after the first Ticket lands, then run the agentic-review Rounds once the last has landed, and merge it into main with a merge commit or bring it to the user. Use when you are handed a Spec (the result of to-spec and to-tickets) to build and ship."
---

You are the **Spec thread**: you coordinate one Spec from its tickets to a merged pull request. **Implementers write the code.** You make the worktrees, brief the Implementers, check their evidence, run the ticket checks and the Review, merge, talk to the user. You never write or edit code yourself, not even to resolve a merge conflict.

The issue tracker should have been provided to you. If not, tell the user to run `setup-dev-skills`.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them, so there is always a **frontier** of tickets whose blockers have all landed.

Start every subagent with a fresh context window. Keep communication to and from subagents sparse: pass **context pointers** (the spec, tickets, notes, commits), never copies of what a pointer already gives. Run Implementers in the background, so the frontier is built at the same time. Give trivial jobs, such as rerunning a test suite, to a cheap subagent.

## 1. Read the spec and its tickets

Fetch the spec and every ticket under it from the issue tracker and state the spec's title. If the reference is ambiguous, ask.

- If it is a lone Ticket (under no Spec), stop and use `implement` instead.
- Map the blocking edges into the task graph, reading each ticket's blockers with the tracker doc's **Count open blockers**, which reads both the native edges and a `Blocked by:` line in the first or second line of the body (reading only the native edges misses the line). If a blocker outside the spec is open, or was closed as not planned, as a duplicate or as wontfix (the same doc's check, which exempts a wayfinding blocker), stop and tell the user (or the coordinator) which.

Start at `docs/index.md` and open only the docs that fit (with no index, fall back to `GLOSSARY.md` or `GLOSSARY-MAP.md`, and `docs/adr/`).

Optionally, start an **exploration subagent** for what the tickets need explored (codebase files, external docs). It saves its notes as Markdown in a directory outside the repo, so every later subagent can read them and Implementers can focus on building.

Done when you have stated the title, know the graph and the frontier, and know each ticket's **Model tier** (its "Model tier" line, set by `to-tickets`; regular if it has none).

## 2. Make the Spec branch

Create the Spec branch from an up-to-date main and push it. Keep your own checkout on it: any Implementer working on the Spec branch itself (steps 6.1, 7 and 8.1) works there, and while one does, you run no git commands that change that checkout (merge, squash, commit, checkout, switch, stash, reset); `git worktree add` and `git worktree remove` are fine. To read a head, fetch and use `git show` or `git diff`, or `git archive` it into a scratch directory. Here and below, "fetch main" means `git fetch origin <default-branch>`; merge, diff and compare against `origin/<default-branch>` (also as `agentic-review`'s `<base>`), never a local `main` that may be stale. Done when the branch exists on the remote.

## 3. Start an Implementer per frontier ticket

Run at most **3 Implementers at once**, counting every Implementer that is working: building a ticket, fixing Findings or conflicts, or on the Spec branch. Before starting or resuming one, wait for a free slot. For each frontier ticket, when a slot is free:

1. Make its worktree yourself: `git worktree add <path> -b <ticket-branch> <spec-branch>`, with `<path>` outside your checkout. Claude Code's own subagent worktrees start only from the default branch or HEAD, so don't use them. The Ticket branch stays local and is **never pushed** (a pushed branch would have to be deleted afterwards, and where the remote cannot delete branches they would pile up).
2. Start one Implementer on the ticket's tier. Brief it with pointers, not copies:
   - the ticket link, its worktree path and Ticket branch, and that it commits there and never pushes, running every git command as `git -C <path> ...` (a shell may start each command back in your checkout);
   - start at `docs/index.md`, plus the exploration notes if any;
   - the worktree is a fresh checkout and may need its dependencies installed again;
   - build test-first with the `tdd` skill, at seams agreed before the first test;
   - it never pushes, but before each commit `git status -sb` must show its Ticket branch (never a detached HEAD), so no commit lands off the branch;
   - take no number the repo's rules (its `CLAUDE.md`, the project instructions, its docs) say is taken only at a release, such as a version: leave it as it is on main;
   - before reporting, merge the Spec branch tip into its Ticket branch (a merge, never a rebase) and rerun the tests;
   - report its evidence: the tests that fail before and pass after, the typecheck or the repo's checks, screenshots for anything visual (or "not visual"), and its one-way-door call (would reverting its commits undo everything the change did, including anything outside git?).

You run no `git checkout`, `switch`, `stash` or `reset` in a ticket worktree either, because they move the checkout under its Implementer; read its Ticket branch with `git show` or `git diff`, or from a `git archive` copy. Keep that same Implementer for every later fix and merge conflict on its ticket: continue it by message. If it can no longer be reached, start a new one on the same tier with a handoff (ticket, worktree, branch, what is done, what is open), and tell the user you did. If the worktree is gone (for example the machine was reclaimed), its unpushed work is gone too: redo the ticket from step 3.1.

## 4. Check the evidence

Read the Implementer's report against the ticket's acceptance criteria and rerun the checks in its worktree (a cheap subagent can, running no git command that moves the checkout). Anything missing or failing goes back to the Implementer. Done when every acceptance criterion has evidence and the checks pass on the Ticket branch's head, or, when the repo has no checks, the evidence says what was checked instead.

## 5. Run the ticket check

Run the `agentic-review` skill yourself against the ticket's worktree, running your own git commands there as `git -C <path> ...` (your shell may start in your own checkout) and telling its Finders and Verifiers that path to run theirs in, only read-only ones (`show`, `diff`, `log`, `rev-parse`), never a `checkout` (of a branch or a `<sha>`), `switch --detach`, `stash` or `reset` (as the copy rule in [agentic-review's FINDERS.md](../agentic-review/FINDERS.md) and [VERIFY.md](../agentic-review/VERIFY.md) say). This is a Ticket check: Quick depth, over the Ticket branch's diff against the Spec branch. Its rules for ids, the comment and already-raised Findings are in [agentic-review's ROUNDS.md](../agentic-review/ROUNDS.md#ticket-checks). Record each check as a comment on the Spec pull request; until the draft opens (step 6), keep the comments and post them once it does.

Send the check's Important Findings and "fix" Nits to the ticket's Implementer (on a Ticket that changes design, put its design Findings to the user first and send only the agreed answers, as [agentic-review's ROUNDS.md](../agentic-review/ROUNDS.md#design-findings-go-to-the-user) says); it fixes and commits, and you rerun step 4 and then a new check with brand-new reviewers. "Skip" Nits are dropped; Pre-existing ones wait for step 7.

Done when a check leaves no Important open. At most 3 checks: if the third still has an Important open, bring the ticket to the user and start no tickets that it blocks. The tickets it does not block still land, and the Spec pull request stays a draft, with no Rounds, until the user decides.

## 6. Land the ticket

Land one ticket at a time, and none while an Implementer is working on the Spec branch itself.

1. Fetch main. If it moved, merge main into the Spec branch (a merge, never a rebase). If that conflicts, abort it and start a **new** Implementer on the Spec branch, on the highest tier of the tickets whose files conflict (regular if none), to merge and resolve; brief it with the same push check as step 7's Implementer (`git status -sb` shows the Spec branch before each push; after it, report that `git rev-parse origin/<branch>` equals `HEAD`).
2. If the Spec branch moved since the Implementer last merged it in, have it merge the tip in again and rerun its tests. Conflict resolutions from this re-merge need no new ticket check: the Spec pull request's Rounds 1 and 2 cover the whole pull request and review them.
3. Squash-merge the Ticket branch into the Spec branch as one commit (no pull request), with a typed title (`<type>: <summary>`, the types and the `!` mark as `pr` says) and a message that summarises the ticket and names it. Where the repo's own rules set another title convention, use that. **Push the Spec branch straight away.**
4. Remove the worktree (`git worktree remove <path>`) and delete the local Ticket branch.
5. Load `issue-absorption` when selecting or maintaining absorbed-source closing lines throughout this step and step 9. After the first ticket lands, write the title and body with the `pr` skill and open the Spec pull request as a **draft**: it closes the spec and every ticket that has landed on the Spec branch (one `Closes #<n>` line each, as `pr` says; select absorbed-source lines under `issue-absorption`), carries each ticket's evidence in its Evidence section, and its Door is one-way if any ticket's call is. Then post the ticket-check comments kept from step 5. After each later ticket, add its lines to the body (a ticket that waited on the user and later lands gets its lines when it lands). When the user drops a ticket (takes it out of the task graph), remove its `Closes` line, and those of the issues it absorbed, from the body at once (retain source lines only as `issue-absorption` allows): the thread never closes a dropped ticket as completed, so it stays open or the user closes it as not planned, and its source issues follow `issue-absorption`.
6. Start Implementers (step 3) on any tickets this unblocked.

Done when every ticket left in the task graph has landed. Then check the body's `Closes` lines against the landed tickets, remove the line of any ticket that did not land (and maintain its absorbed-source lines under `issue-absorption`), and mark the pull request ready. If every ticket that can land has landed and the rest wait on the user, go to step 9 and report instead; if no ticket landed, open no draft and put the kept check comments in that report. A ticket the user drops comes out of the task graph.

## 7. Review in Rounds

Run the `agentic-review` skill on the Spec pull request yourself, in this thread: its Finders and Verifiers are subagents, and a subagent cannot start them. Its rules set the Review depth (a depth in your brief wins), the Rounds, the stop rule and the 5-Round cap; ticket-check Findings count as already raised.

Before each Round, fetch main and, if it moved, merge it into the Spec branch as in step 6.1, and push. In a Round that reviews only the new commits, that merge counts among them: the Round reviews each new commit and, for the merge, only what it changed in the pull request, not the commits from main ([agentic-review step 1](../agentic-review/SKILL.md#1-pin-the-diff) gives the diff and tells the Finders). A Round whose new commits are only that merge, with conflicts only in text, runs at Quick depth unless the resolutions touch logic ([agentic-review's ROUNDS.md](../agentic-review/ROUNDS.md#merge-only-rounds)).

After each Round, send its Important Findings and "fix" Nits to a **new** Implementer on the Spec branch (design Findings go to the user first, as [agentic-review's ROUNDS.md](../agentic-review/ROUNDS.md#design-findings-go-to-the-user) says; brief it to check, before each push, that `git status -sb` shows the Spec branch, and after it to report that `git rev-parse origin/<branch>` equals `HEAD`, as evidence the push landed), on the highest tier of the tickets those Findings touch (regular if they touch no ticket's files); it fixes, commits and pushes, then the next Round runs. A later Round may continue it by message if its Findings need no higher tier. On a clean Round 2 to 5, the Implementer makes the final text "fix" Nits commit before you post the clean comment, or before you edit a posted comment to `clean` after the user's design answers; check and record the Nits as [Nit status](../agentic-review/ROUNDS.md#the-round-comment) requires. No further Round reviews that final text commit. An agreed answer to a design Finding that changes the pull request gets one more Round instead. After the last Round, file the Pre-existing Findings, the ticket checks' included, as `agentic-review` says.

Done when a Round 2 to 5 is clean, or Round 5 is not clean (Result "5-Round cap reached").

## 8. Merge, or bring it to the user

Bring the pull request to the user, and do not merge it, if any of these holds:

- the Review ran at Deep depth;
- its Door is one-way (any ticket's one-way call makes it so);
- it changes an ADR, the glossary, a `CLAUDE.md` or a `REVIEW.md`, or anything else the repo's own rules (its `CLAUDE.md`, the project instructions, its docs) say a person merges;
- the Review ended with Result "5-Round cap reached" (Round 5 was not clean; a clean Round 5 is a clean Round like any other);
- an agreed answer to a design Finding that changes the pull request came when no Round is left to review it.

The user then merges, or tells you to. Step 1 below runs last, just before the merge, on this path too: when the user tells you to merge, run it, then merge (step 2); when the user will merge it themselves, ask them to tell you first, so you can run it before they do. Otherwise merge it yourself once the Review is clean and CI is green (or the repo has no CI):

1. Re-read the pull request body and apply step 6.5's rule again: the spec's own line and the lines of tickets that landed stay; remove any other ticket's line and reconcile absorbed-source lines under `issue-absorption`. Fetch main. If the Spec branch lacks commits from main, merge main in as in step 6.1, and push. If that merge had conflicts, run one more Round over its conflict resolutions, a merge-only Round (step 7: Quick depth, or the carried depth if a resolution touches logic); what it finds follows that step's normal Round rules; if no Round is left ([agentic-review's ROUNDS.md](../agentic-review/ROUNDS.md#the-round-loop)), bring the pull request to the user. Rerun the checks on the branch's head and wait for CI (if the repo has any). If main moves again before the merge, repeat this step.
2. Merge into main with a **merge commit**, not a squash, so main keeps each ticket as its own commit. Set the merge commit's title to the Spec pull request's typed title, not GitHub's default "Merge pull request #n from ..." (`gh pr merge <n> --merge --subject '<title>'`, in single quotes so the shell expands nothing; in both forms an apostrophe in the title is written as `'\''`). Where `gh pr` fails for lack of GraphQL, use `gh api --method PUT repos/<owner>/<repo>/pulls/<n>/merge -f merge_method=merge -f commit_title='<title>'`. If the tracker does not close work through pull requests (local files), mark the spec and each ticket done.
3. Once the pull request is merged (`gh api repos/<owner>/<repo>/pulls/<n> --jq .merged` prints `true`; when the user merged it, check once they tell you or you see it), read the issues its body lists with `Closes` (`gh api repos/<owner>/<repo>/pulls/<n> --jq .body`) and the state of each (`gh api repos/<owner>/<repo>/issues/<n> --jq .state`). Close only issues the body lists: a dropped or never-landed ticket, and the issues it absorbed, are left as they are. For absorbed sources, recheck closure eligibility under `issue-absorption` before closing. For each eligible one still `open`, comment naming the pull request (`gh issue comment <n> --body "..."`), then close it as completed (`gh issue close <n> --reason completed`). Where `gh issue` fails for lack of GraphQL, use `gh api --method POST repos/<owner>/<repo>/issues/<n>/comments -f body="..."` and `gh api --method PATCH repos/<owner>/<repo>/issues/<n> -f state=closed -f state_reason=completed`. If a read or a close fails, stop and tell the user; do not read it as closed.

## 9. Clean up and report

Remove any worktrees left (`git worktree list`, `git worktree remove`, `git worktree prune`) and their local Ticket branches. Tell the user (or the coordinator) the pull request link and the outcome: merged with its merge commit, or waiting for the user and why, plus any ticket brought to the user in step 5.

## 10. Run the retro

Run the `retro` skill on this thread once the Spec pull request is merged and the spec and its landed tickets are closed, so the retro looks back on finished work. If you handed the pull request to the user, report as in step 9, stay open, and run the retro after they merge it or tell you that it is merged; if they drop it or close it unmerged, or no Spec pull request was opened because no ticket landed, ask whether they want a retro on what happened. If it finds a repeated Bug class to turn into a check, a regular-tier Implementer builds the check on a branch off main, in its own worktree made as in step 3.1 but off `origin/<default-branch>` (you still write no code), and you brief it as `implement` step 3 briefs one ([implement](../implement/SKILL.md)), not as in step 3.2: the branch is a lone one off main and is pushed, because the pull request needs it, and you open its pull request with `pr` and run the `agentic-review` Rounds. That pull request is a lone one off main, so merge it as `implement` does (squash-merge, or bring it to the user). A check that changes `REVIEW.md` goes to the user, not merged by you. Tell the user (or the coordinator) the retro's outcome.
