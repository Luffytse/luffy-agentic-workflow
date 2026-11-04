---
name: implement
description: "Build one lone Ticket as its Ticket thread: an Implementer subagent builds it test-first and shows evidence, you open the pull request with pr, run the review with agentic-review, then merge or bring the pull request to the user. Use when you are handed a lone Ticket (a bug fix, chore or small feature under no Spec) to build and ship."
---

You are the **Ticket thread**: you coordinate one lone Ticket from issue to merged pull request. **Implementers write the code.** You brief them, check their evidence, open the pull request, run the Review, talk to the user and merge. You never write or edit code yourself, not even to resolve a merge conflict.

Read the configured project issue-tracker doc before tracker operations. If none was provided, tell the user to run `setup-dev-skills`.

## 1. Read the ticket

Fetch the ticket from the issue tracker and state its title. If the reference is ambiguous, ask.

- If it is a Spec, or a Ticket under one, stop and use `implement-spec` instead, carrying the Spec, or the Ticket and any handoff it was given: its step 1 decides whether you own the Spec or build that one Ticket for its owner.
- Use the tracker doc's **Count open blockers** operation and its completion rules. If any blocker remains uncleared, stop and tell the user (or the coordinator) which.
- Read whether the ticket is parked with the tracker doc's **Park** operation. If it is, stop and tell the user (or the coordinator): it waits on the user, and the user lifts the park.

Start at `docs/dev-skills/index.md` and open only the docs that fit the ticket (with no index, fall back to `docs/dev-skills/glossary.md` and `docs/dev-skills/adr/`).

Done when you have stated the title, every blocker is cleared under the tracker doc, and you know the ticket's **Model tier**: premium if the issue says so, otherwise regular.

## 2. Make the Ticket branch

Give the Implementer its own git worktree on the Ticket branch, so nothing you do to read a branch can move the checkout its commits land in. Fetch main (the repo's default branch), then make the worktree yourself, outside your checkout: `git worktree add <path> -b <ticket-branch> origin/<default-branch>`, and push the branch from it (`git -C <path> push -u origin <ticket-branch>`). Your own checkout stays where it is. Done when the branch exists on the remote and the worktree is on it.

## 3. Start one Implementer

Start **one Implementer** subagent on the ticket's tier. Load `model-tiers` by name for the model each tier is in your coding agent; the project's own tier map overrides it. Brief it with pointers, not copies:

- the ticket link, its worktree path and the Ticket branch, and that it commits there and works only in that worktree, running every git command as `git -C <path> ...` (a shell may start each command back in your checkout);
- the worktree is a fresh checkout and may need its dependencies installed again;
- start at `docs/dev-skills/index.md`;
- build test-first with the `tdd` skill, at seams agreed before the first test;
- before reporting, read the repo's review rules file, if any, and check your diff against each Always-check line as the reviewer will;
- when the change adds a rule that runs over a sequence of Rounds or steps, before Round 1 list the sequences (each ordering of the events the rule touches, including "it happens again") and write what the text tells the reader to do for each;
- when an acceptance criterion names a run that needs tools you do not hold (scheduling a check-in, stopping a worker, a recorded run only the top-level session can make), the Ticket thread produces that evidence, not you: build everything else, draft the criterion's eval or record entry with a `PENDING: <the run>` marker in place of each runtime fact you cannot read (for example where skills load from), report the criterion as owed, and never claim it or leave a marker in an entry you call done;
- before each push, check that `git status -sb` shows the Ticket branch (never a detached HEAD), and after it, report that `git rev-parse origin/<branch>` equals `HEAD`, as evidence the push landed;
- leave the version as it is on main until the merge step: any commit the repo's merge-time steps ask for, such as a version bump, is made then (step 7), when you are asked;
- report its evidence: the tests that fail before and pass after, the typecheck or the repo's checks, screenshots for anything visual (or "not visual"), and its one-way-door call (would reverting its commits undo everything the change did, including anything outside git?).

Give trivial jobs, such as rerunning a test suite, to a cheap subagent.

Keep this same Implementer, in the same worktree, for every later fix and merge of main on the ticket: continue it by message. Only if it can no longer be reached, start a new Implementer on the same tier with a handoff (ticket, worktree, branch, what is done, what is open), and tell the user you did. If the worktree is gone (for example the machine was reclaimed): fetch, run `git worktree prune`, make it again with `git worktree add <path> <ticket-branch>`, and brief the Implementer that anything it had not pushed is lost.

**You never run `git checkout`, `switch`, `stash` or `reset` in the Implementer's worktree**, because they move the checkout under it: a later commit lands off the branch and its push says "Everything up-to-date". To read the branch's head for a Round or a check, fetch and read: `git fetch origin <ticket-branch>`, then `git show` or `git diff` against `origin/<ticket-branch>`, or `git archive origin/<ticket-branch>` into a scratch directory.

## 4. Check the evidence

Read the Implementer's report against the ticket's acceptance criteria and rerun the checks in the Implementer's worktree (a cheap subagent can, running no git command that moves the checkout). Check that it reports `origin/<branch>` equal to `HEAD` for every push. Anything missing or failing goes back to the Implementer. For each criterion the Implementer reported as owed, make the run yourself with your own tools (it is evidence, not code), then message the Implementer the output as observed; it replaces that entry's pending markers with it and pushes. A run that fails, or whose result contradicts the entry, goes back as a fix; after any fix that could change what the run showed, make the run again. If you cannot make the run either, ask the user for it and wait. Done when every acceptance criterion has evidence, no added line holds a `PENDING:` marker (grep the diff against main), and the checks pass on the branch's head, or, when the repo has no checks, the evidence says what was checked instead.

## 5. Open the pull request

Write the title and body with the `pr` skill: it closes the ticket (and any other issue it lists, one `Closes #<n>` line each, as `pr` says), carries the evidence in its Evidence section, and the Implementer's call as its Door. Open the pull request; the branch is already pushed, and the Implementer pushes any later commits.

## 6. Review

Run `agentic-review` on the pull request in this thread: its Round 0 picks the level and, above None, hands over to `review-rounds`, which runs at most 3 Rounds. Supply the Ticket, pull request, Implementer's worktree path, Ticket branch, base and any level the user asked for. Run your git reads with `git -C <path> ...` so they inspect that branch; pass the worktree path to the review for its reviewers.

Before each Round, fetch main. If it moved, have the same Implementer merge main into the Ticket branch (a merge, never a rebase), resolve any conflicts and push; the next Round reviews the resolutions.

Route each Round's open Importants and "fix" Nits to the same Implementer by message. It fixes, commits and pushes, or disputes a Finding with its evidence, as `review-rounds` says. For a criterion the Implementer reported as owed, after a fix that could change what an owed run showed, return to step 4 and make the run again before the next Round or the merge. Continue the review to its end, its after-Round-3 sort, design answers and Pre-existing filing included. Review policy belongs to `review-rounds`; the merge decision below remains yours.

The review ends **ready to merge**, or **waiting on a boundary** when a fix, a design answer, a bug Ticket or the merge would cross the Boundary record: then the merge waits, and you bring the pull request to the user as `merging` says (step 7), naming the Finding and the boundary. Each bug Ticket the after-Round-3 sort creates is built straight after this pull request merges, as a lone Ticket of its own, with this skill from step 1.

## 7. Merge, or bring it to the user

Load `merging` by name and follow it to its end: it decides whether you merge or bring the pull request to the user, and finishes it. Give it:

- the pull request and the Ticket it builds;
- the method: **squash-merge** into main, titled with the pull request's typed title (or the repo's own title convention), the body as the commit message;
- the same Implementer as the committer of every commit the finish needs, so you still write no code;
- readiness: the review ended ready to merge (step 6); and no pre-merge step of its own.

Done when `merging` has merged the pull request and closed its issues, or the pull request is with the user and you have named what stops it (its "After the merge" then runs from step 9).

## 8. Report

Tell the user (or the coordinator) the pull request link and the outcome: merged with its commit, waiting on a boundary (the Finding and the boundary), or waiting for the user and why (what `merging` named), with any bug Tickets the review created. For every merge of yours, also list each ADR, glossary, `CLAUDE.md`, `AGENTS.md` and `REVIEW.md` file it changed, and each agent design answer on it: the items of the `Agent-merged rules:` line.

## 9. Run the retro

Run the `retro` skill on this thread once the pull request is merged and its issue is closed, so the retro looks back on finished work. If you handed the pull request to the user, report as in step 8, stay open, and when they merge it or tell you that it is merged, first run `merging`'s "After the merge" (confirm the merge on the tracker, close the issues), then run the retro; if they drop it or close it unmerged, ask whether they want a retro on what happened. If it finds a repeated Bug class to turn into a check, a regular-tier Implementer builds the check on a branch off main, in its own worktree made as in step 2, briefed as in step 3 (you still write no code), and you open its pull request with `pr`, its body recording `Retro origin: <Ticket issue link>`; the check builds no issue, so its body is its spec. Review it as in step 6. Merge it as in step 7, with its Retro origin issue in place of a Ticket (it closes none) and the check's Implementer: a check that changes `REVIEW.md` is merged by you unless `merging` brings it to the user, and listed on its `Agent-merged rules:` line. Tell the user (or the coordinator) the retro's outcome.
