---
name: implement
description: "Build one lone Ticket as its Ticket thread: an Implementer subagent builds it test-first and shows evidence, you open the pull request with pr, run the agentic-review Rounds, then merge or bring the pull request to the user. Use when you are handed a lone Ticket (a bug fix, chore or small feature under no Spec) to build and ship."
---

You are the **Ticket thread**: you coordinate one lone Ticket from issue to merged pull request. **Implementers write the code.** You brief them, check their evidence, open the pull request, run the Review, talk to the user and merge. You never write or edit code yourself, not even to resolve a merge conflict.

The issue tracker should have been provided to you. If not, tell the user to run `setup-dev-skills`.

## 1. Read the ticket

Fetch the ticket from the issue tracker and state its title. If the reference is ambiguous, ask.

- If it is a Spec, or a Ticket under one, stop and use `implement-spec` for the Spec instead.
- Check its blocking edges. If any blocker is not merged, stop and tell the user (or the coordinator) which.

Start at `docs/index.md` and open only the docs that fit the ticket (with no index, fall back to `GLOSSARY.md` or `GLOSSARY-MAP.md`, and `docs/adr/`).

Done when you have stated the title, every blocker is merged, and you know the ticket's **Model tier**: premium if the issue says so, otherwise regular.

## 2. Make the Ticket branch

Give the Implementer its own git worktree on the Ticket branch, so nothing you do to read a branch can move the checkout its commits land in. Fetch main (the repo's default branch), then make the worktree yourself, outside your checkout: `git worktree add <path> -b <ticket-branch> origin/<default-branch>`, and push the branch from it (`git -C <path> push -u origin <ticket-branch>`). Your own checkout stays where it is. Done when the branch exists on the remote and the worktree is on it.

## 3. Start one Implementer

Start **one Implementer** subagent on the ticket's tier. Brief it with pointers, not copies:

- the ticket link, its worktree path and the Ticket branch, and that it commits there and works only in that worktree, running every git command as `git -C <path> ...` (a shell may start each command back in your checkout);
- the worktree is a fresh checkout and may need its dependencies installed again;
- start at `docs/index.md`;
- build test-first with the `tdd` skill, at seams agreed before the first test;
- before each push, check that `git status -sb` shows the Ticket branch (never a detached HEAD), and after it, report that `git rev-parse origin/<branch>` equals `HEAD`, as evidence the push landed;
- leave every number the repo's rules (its `CLAUDE.md`, the project instructions, its docs) say to take at merge time, such as a version or the number of a new numbered entry, as the placeholder `TBD-N`, or as it is on main where a placeholder would break the file (a manifest's version); the real numbers come in step 7;
- report its evidence: the tests that fail before and pass after, the typecheck or the repo's checks, screenshots for anything visual (or "not visual"), and its one-way-door call (would reverting its commits undo everything the change did, including anything outside git?).

Give trivial jobs, such as rerunning a test suite, to a cheap subagent.

Keep this same Implementer, in the same worktree, for every later fix, merge of main and numbering on the ticket: continue it by message. Only if it can no longer be reached, start a new Implementer on the same tier with a handoff (ticket, worktree, branch, what is done, what is open), and tell the user you did. If the worktree is gone (for example the machine was reclaimed): fetch, run `git worktree prune`, make it again with `git worktree add <path> <ticket-branch>`, and brief the Implementer that anything it had not pushed is lost.

**You never run `git checkout`, `switch` or `reset` in the Implementer's worktree**, because they move the checkout under it: a later commit lands off the branch and its push says "Everything up-to-date". To read the branch's head for a Round or a check, fetch and read: `git fetch origin <ticket-branch>`, then `git show` or `git diff` against `origin/<ticket-branch>`, or `git archive origin/<ticket-branch>` into a scratch directory.

## 4. Check the evidence

Read the Implementer's report against the ticket's acceptance criteria and rerun the checks in the Implementer's worktree (a cheap subagent can, running no git command that moves the checkout). Check that it reports `origin/<branch>` equal to `HEAD` for every push. Anything missing or failing goes back to the Implementer. Done when every acceptance criterion has evidence and the checks pass on the branch's head, or, when the repo has no checks, the evidence says what was checked instead. A check that fails only because a number is still a placeholder (or a version is not yet bumped) is expected until step 7.

## 5. Open the pull request

Write the body with the `pr` skill: it closes the ticket, carries the evidence in its Evidence section, and the Implementer's call as its Door. Open the pull request; the branch is already pushed, and the Implementer pushes any later commits.

## 6. Review in Rounds

Run the `agentic-review` skill on the pull request yourself, in this thread: its Finders and Verifiers are subagents, and a subagent cannot start them. Run it against the Implementer's worktree with git commands that do not move it (fetch first; `git -C <path> diff`, `log` and `rev-parse`, since your shell may start in your own checkout), so its `HEAD` is the Ticket branch's head, and tell its Finders and Verifiers the worktree path to run their git commands in (`git -C <path> ...`). Its rules set the Review depth (a depth in your brief wins), the Rounds, the stop rule and the 5-Round cap.

Before each Round, fetch main. If it moved, have the Implementer merge main into the Ticket branch (a merge, never a rebase), resolve any conflicts and push. In a Round that reviews only the new commits, that merge counts among them: the Round reviews each new commit and, for the merge, only what it changed in the pull request, not the commits from main ([agentic-review step 1](../agentic-review/SKILL.md#1-pin-the-diff) gives the diff and tells the Finders). A Round whose new commits are only that merge, with conflicts only in numbers or text, runs at Quick depth unless the resolutions touch logic ([agentic-review's ROUNDS.md](../agentic-review/ROUNDS.md#merge-only-rounds)).

After each Round, send its Important Findings and "fix" Nits to the Implementer by message (on a pull request that changes design, put its design Findings to the user first and send only the agreed answers, as [agentic-review's ROUNDS.md](../agentic-review/ROUNDS.md#design-findings-go-to-the-user) says); it fixes, commits and pushes, then the next Round runs. On a clean Round 2 to 5, the Implementer makes the final "fix" Nits commit before you post that Round's comment; no further Round reviews it. An agreed answer to a design Finding that changes the pull request gets one more Round instead. After the last Round, file Pre-existing Findings as `agentic-review` says.

Done when a Round 2 to 5 is clean, or the 5-Round cap is hit.

## 7. Merge, or bring it to the user

Bring the pull request to the user, and do not merge it, if any of these holds:

- the Review ran at Deep depth;
- its Door is one-way;
- it changes an ADR, the glossary, a `CLAUDE.md` or a `REVIEW.md`, or anything else the repo's own rules (its `CLAUDE.md`, the project instructions, its docs) say a person merges;
- the Review hit the 5-Round cap.

The user then merges, or tells you to. Steps 1 and 2 below run last, just before the merge, on this path too: when the user tells you to merge, run them, then merge (step 3); when the user will merge it themselves, ask them to tell you first, so you can run them before they do. Otherwise merge it yourself once the Review is clean and CI is green (or the repo has no CI):

1. Fetch main. If the Ticket branch lacks commits from main, have the Implementer merge main in (a merge, never a rebase).
2. **Take the numbers.** Have the Implementer read the repo's rules (its `CLAUDE.md`, the project instructions, its docs) for what a change must number or update when it merges, such as a version bump or the number of a new numbered entry, take the next free ones as of main, and replace every `TBD-N` placeholder; it commits and pushes. A bump the rules require is never skipped. Update the pull request body if it names those numbers. If the merge in step 1 had conflicts, or this commit (the first pass and every repeat) changes more than one file or rewrites a cross-reference, run one more Round over this commit and any conflict resolutions (step 6): a merge-only Round if step 1 merged main (Quick depth, or the carried depth if a resolution touches logic), otherwise an ordinary Round at the carried depth over this commit alone; what it finds follows that step's normal Round rules; if the 5-Round cap leaves no Round, bring the pull request to the user. Rerun the checks in the worktree, on the branch's head, and wait for CI (if the repo has any). If main moves again before the merge, repeat steps 1 and 2. On a repeat no `TBD-N` is left, so the Implementer retakes every number the branch took under the repo's rules (such as the version and the numbers of the new entries its diff against main adds), as if afresh on top of main's current numbers: each at the next free one in the same order, counting the ones it has just moved (a number already the next free one stays), and a version above main's. It rewrites the branch's own cross-references to a changed number from the old-to-new list (in the pull request body too), and its report names each old and new number, or says none changed.
3. **Squash-merge** into main, with a commit message you write that summarises the final change and names the ticket, rather than the branch's commit messages joined together.

## 8. Report

Tell the user (or the coordinator) the pull request link and the outcome: merged with its commit, or waiting for the user and why.

## 9. Run the retro

Run the `retro` skill on this thread once the pull request is merged and its issue is closed, so the retro looks back on finished work. If you handed the pull request to the user, report as in step 8, stay open, and run the retro after they merge it or tell you that it is merged; if they drop it or close it unmerged, ask whether they want a retro on what happened. If it finds a repeated Bug class to turn into a check, a regular-tier Implementer builds the check on a branch off main, in its own worktree made as in step 2, briefed as in step 3 (you still write no code), and you open its pull request with `pr` and run the `agentic-review` Rounds as in steps 5 to 7. A check that changes `REVIEW.md` goes to the user, not merged by you. Tell the user (or the coordinator) the retro's outcome.
