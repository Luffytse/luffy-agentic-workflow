---
name: implement-spec
description: "Build one Spec as its Spec thread: Implementer subagents build its Tickets test-first in local worktrees off one Spec branch, each Ticket passes a ticket check and is squash-merged in, you open the Spec pull request with pr as a draft after the first Ticket lands, then run the agentic-review Rounds once the last has landed, and merge it into main with a merge commit or bring it to the user. Use when you are handed a Spec (the result of to-spec and to-tickets) to build and ship."
---

You are the **Spec thread**: you coordinate one Spec from its tickets to a merged pull request. **Implementers write the code.** You make the worktrees, brief the Implementers, check their evidence, run the ticket checks and the Review, merge, talk to the user. You never write or edit code yourself, not even to resolve a merge conflict.

Read the configured project issue-tracker doc before tracker operations. If none was provided, tell the user to run `setup-dev-skills`.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them, so there is always a **frontier** of tickets whose blockers have all landed.

Start every subagent with a fresh context window. Keep communication to and from subagents sparse: pass **context pointers** (the spec, tickets, notes, commits), never copies of what a pointer already gives. Run Implementers in the background, so the frontier is built at the same time. Give trivial jobs, such as rerunning a test suite, to a cheap subagent.

## 1. Read the spec and its tickets

Fetch the spec and every ticket under it from the issue tracker and state the spec's title. If the reference is ambiguous, ask.

- If it is a lone Ticket (under no Spec), stop and use `implement` instead.
- Map the blocking edges into the task graph using the tracker doc's **Count open blockers** operation and its completion rules. If any blocker outside the Spec remains uncleared, stop and tell the user (or the coordinator) which.

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
   - leave the version as it is on main until the merge step: a Ticket never bumps, and the merge step adds any bump the release doc calls for to the Spec pull request, with a number handed out then;
   - before reporting, merge the Spec branch tip into its Ticket branch (a merge, never a rebase) and rerun the tests;
   - report its evidence: the tests that fail before and pass after, the typecheck or the repo's checks, screenshots for anything visual (or "not visual"), and its one-way-door call (would reverting its commits undo everything the change did, including anything outside git?).

You run no `git checkout`, `switch`, `stash` or `reset` in a ticket worktree either, because they move the checkout under its Implementer; read its Ticket branch with `git show` or `git diff`, or from a `git archive` copy. Keep that same Implementer for every later fix and merge conflict on its ticket: continue it by message. If it can no longer be reached, start a new one on the same tier with a handoff (ticket, worktree, branch, what is done, what is open), and tell the user you did. If the worktree is gone (for example the machine was reclaimed), its unpushed work is gone too: redo the ticket from step 3.1.

## 4. Check the evidence

Read the Implementer's report against the ticket's acceptance criteria and rerun the checks in its worktree (a cheap subagent can, running no git command that moves the checkout). Anything missing or failing goes back to the Implementer. Done when every acceptance criterion has evidence and the checks pass on the Ticket branch's head, or, when the repo has no checks, the evidence says what was checked instead.

## 5. Run the ticket check

Run the complete `agentic-review` Ticket-check entry point in this thread. Supply the Ticket and Spec, the Ticket worktree path and branch, the Spec branch as diff base, Quick depth, and prior Ticket-check Findings. Run your git reads as `git -C <path> ...`; pass the worktree path to the review workflow for its reviewers. Record each check on the Spec pull request; until the draft opens (step 6), keep the comments and post them once it does.

Route the workflow's fixes to the ticket's same Implementer; it fixes and commits. Rerun step 4, then request a new Ticket check through `agentic-review`. Carry the check records forward to step 7, including Pre-existing Findings.

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

Run the complete `agentic-review` workflow on the Spec pull request in this thread. Supply the Spec and Tickets, pull request, Spec worktree path and branch, base, any requested Review depth, and all Ticket-check records, including Pre-existing Findings.

Before each Round, fetch main and, if it moved, merge it into the Spec branch as in step 6.1, and push. Supply the resulting head and merge context to the review workflow.

Route the workflow's fixes to a **new** Implementer on the Spec branch, on the highest tier of the tickets those Findings touch (regular if they touch no ticket's files). Brief it to check before each push that `git status -sb` shows the Spec branch, and afterwards report that `git rev-parse origin/<branch>` equals `HEAD`. It fixes, commits and pushes; a later Round may continue it by message if its Findings need no higher tier. Return its commit and evidence to `agentic-review` and continue that workflow through its completion, including its final fix and filing actions. Review policy and completion belong to `agentic-review`; the merge decision below remains yours.

## 8. Merge, or bring it to the user

First decide whether the pull request is **inside a Milestone**. Read the Boundary record (the one the repo's `CLAUDE.md` or `AGENTS.md` points to, usually `docs/agents/boundaries.md`) for its Milestone label form. The pull request is inside a Milestone when the Spec carries a label in that form; then read the Milestone issue (the issue that carries the same label and holds the Milestone's goal) for allowed or forbidden actions of its own, which win over the record's for this Spec. With no Boundary record, or no label in its form on the Spec, the pull request is outside a Milestone.

**Inside a Milestone**, bring the pull request to the user, and do not merge it, only if any of these holds:

- it crosses a boundary: it takes, or its merge would take, an action that the Milestone issue forbids or says needs the user's approval, or one the Boundary record says needs the user's approval and the Milestone issue does not explicitly allow; or its Door is one-way (any ticket's one-way call makes it so) and, for any of its irreversible actions, the Milestone issue does not explicitly allow agents to take it (or, where the Milestone issue does not mention it, the record does not);
- the repo's own rules (its `CLAUDE.md`, the project instructions, its docs) say a person merges it;
- the Review ended with Result "5-Round cap reached" (Round 5 was not clean; a clean Round 5 is a clean Round like any other);
- an agreed answer to a design Finding that changes the pull request came when no Round is left to review it.

Deep depth alone does not stop the merge, and neither does a change to an ADR, the glossary, a `CLAUDE.md` or a `REVIEW.md`. When you merge such a change yourself, list it for the Milestone review: before the merge, add a line to the pull request body naming each ADR, glossary, `CLAUDE.md` and `REVIEW.md` file it changes (`Milestone review: <files>`), and name them in your report (step 9).

**Outside a Milestone**, bring the pull request to the user, and do not merge it, if any of these holds:

- the Review ran at Deep depth;
- its Door is one-way (any ticket's one-way call makes it so);
- it changes an ADR, the glossary, a `CLAUDE.md` or a `REVIEW.md`, or anything else the repo's own rules (its `CLAUDE.md`, the project instructions, its docs) say a person merges;
- the Review ended with Result "5-Round cap reached" (Round 5 was not clean; a clean Round 5 is a clean Round like any other);
- an agreed answer to a design Finding that changes the pull request came when no Round is left to review it.

When you bring the pull request to the user, name what stops the merge, so the user can decide quickly: the boundary (the action, and whether the Milestone issue or the Boundary record lists it), the repo rule (and the file it is in), the case on the list outside a Milestone, or the Review's Result. The user then merges, or tells you to. Step 1 below runs last, just before the merge, on this path too: when the user tells you to merge, run it, then merge (step 2); when the user will merge it themselves, ask them to tell you first, so you can run it before they do. Otherwise merge it yourself once the Review is clean and CI is green (or the repo has no CI):

1. Re-read the pull request body and apply step 6.5's rule again: the spec's own line and the lines of tickets that landed stay; remove any other ticket's line and reconcile absorbed-source lines under `issue-absorption`. **Bump the version, where pull requests bump.** Read the release doc (the one the repo's `CLAUDE.md` or `AGENTS.md` points to, usually `docs/agents/release.md`). When it says pull requests bump the version and the Spec pull request changes what it says bumps, ask for the next version number just before the merge (from the coordinator, or from the user when no coordinator runs) and wait for it. Have an Implementer on the Spec branch (step 7's, or a new one briefed as there) add the bump as the pull request's last commit, with the release doc's bump-commit steps, and push. Only the Spec pull request bumps; a Ticket never did. Where the release doc says Releases bump, or the repo has no release doc, or the pull request changes nothing it says bumps, skip this part and change nothing. Then fetch main. If the Spec branch lacks commits from main, merge main in as in step 6.1, and push. If that merge had conflicts, return its resolutions to the complete `agentic-review` workflow for a merge-only Round under its depth and completion rules; if its Round budget is exhausted, bring the pull request to the user. Rerun the checks on the branch's head and wait for CI (if the repo has any). If main moves again before the merge, repeat this step. A repeat keeps an existing bump commit and its number when main's version is unchanged (ask for no new number, add no second bump commit). When main's version changed, ask for a new number; the Implementer merges main in, resolves the version file by taking main's, and redoes the bump as a new commit after the merge, superseding the old bump. "Last commit" means the last of the pull request's own work, so a merge of main after the bump is fine.
2. Merge into main with a **merge commit**, not a squash, so main keeps each ticket as its own commit. Set the merge commit's title to the Spec pull request's typed title, not GitHub's default "Merge pull request #n from ..." (`gh pr merge <n> --merge --subject '<title>'`, in single quotes so the shell expands nothing; in both forms an apostrophe in the title is written as `'\''`). Where `gh pr` fails for lack of GraphQL, use `gh api --method PUT repos/<owner>/<repo>/pulls/<n>/merge -f merge_method=merge -f commit_title='<title>'`.
3. Before completing issues, require `gh api repos/<owner>/<repo>/pulls/<n> --jq .merged` to print `true`, including when the user reports merging the pull request. A failed read or any other result does not authorize completion. Read its body and use the tracker doc's operations to read the state of each issue listed by its closing lines. For a tracker without pull-request closing support, use its configured completion operation for the Spec and each landed Ticket instead. Leave dropped or never-landed tickets and their sources unchanged. For absorbed sources, load `issue-absorption` and recheck closure eligibility. For each eligible issue still open, use the tracker doc's **Close** operation with a completed outcome and an explanation naming the pull request. If a read or close fails, stop and tell the user; do not treat it as closed.

## 9. Clean up and report

Remove any worktrees left (`git worktree list`, `git worktree remove`, `git worktree prune`) and their local Ticket branches. Tell the user (or the coordinator) the pull request link and the outcome: merged with its merge commit, or waiting for the user and why, plus any ticket brought to the user in step 5. Inside a Milestone, also list each ADR, glossary, `CLAUDE.md` and `REVIEW.md` file a merge of yours changed, for the Milestone review.

## 10. Run the retro

Run the `retro` skill on this thread once the Spec pull request is merged and the spec and its landed tickets are closed, so the retro looks back on finished work. If you handed the pull request to the user, report as in step 9, stay open, and run the retro after they merge it or tell you that it is merged; if they drop it or close it unmerged, or no Spec pull request was opened because no ticket landed, ask whether they want a retro on what happened. If it finds a repeated Bug class to turn into a check, a regular-tier Implementer builds the check on a branch off main, in its own worktree made as in step 3.1 but off `origin/<default-branch>` (you still write no code), and you brief it as `implement` step 3 briefs one ([implement](../implement/SKILL.md)), not as in step 3.2: the branch is a lone one off main and is pushed, because the pull request needs it, and you open its pull request with `pr` and run the `agentic-review` Rounds. That pull request is a lone one off main, so merge it as `implement` does (squash-merge, or bring it to the user, under the two forms of step 8), with the Spec's Milestone membership (the check's pull request has no issue of its own): inside a Milestone, a check that changes `REVIEW.md` is merged by you and listed for the Milestone review; outside one, a check that changes `REVIEW.md` goes to the user, not merged by you. Tell the user (or the coordinator) the retro's outcome.
