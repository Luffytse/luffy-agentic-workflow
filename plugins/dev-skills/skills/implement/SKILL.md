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
- leave the version as it is on main until the merge step: the merge step adds any bump the release doc calls for, with the number the repo's own docs say how to get;
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

The review ends **ready to merge**, or **waiting on a boundary** when a fix, a design answer, a bug Ticket or the merge would cross the Boundary record: then the merge waits, and you bring the pull request to the user as step 7 says, naming the Finding and the boundary. Each bug Ticket the after-Round-3 sort creates is built straight after this pull request merges, as a lone Ticket of its own, with this skill from step 1.

## 7. Merge, or bring it to the user

Read the Boundary record (`docs/dev-skills/boundaries.md`). With no Boundary record, read an empty one: no irreversible action is allowed to agents and no action needs the user's approval. The record applies exactly as written to every merge, inside a Milestone or not: a Milestone issue holds no boundaries of its own, and a `## Boundaries` section in an earlier one is history.

Bring the pull request to the user, and do not merge it, only if any of these holds:

- it crosses a boundary: it takes, or its merge would take, an action the Boundary record says needs the user's approval; or its Door is one-way and the record does not allow agents to take each of its irreversible actions;
- the repo's own rules (its `CLAUDE.md`, the project instructions, its docs) say a person merges it.

A Deep review alone does not stop the merge, and neither does a change to an ADR, the glossary, a `CLAUDE.md`, an `AGENTS.md` or a `REVIEW.md`. When you merge such a change yourself, or a pull request on which an agent answered design Findings (`review-rounds` lists them, each by its row id and the link to its record), list it: before the merge, add one line to the pull request body, `Agent-merged rules: <files>; design answers: <id> <link>, ...`, naming each ADR, glossary, `CLAUDE.md`, `AGENTS.md` and `REVIEW.md` file the pull request changes and each agent design answer on it (leave out the files part, or the design-answers part, when there is none), and name the same items in your report (step 8).

When you bring the pull request to the user, name what stops the merge, so the user can decide quickly: the boundary (the action, as the Boundary record lists it), the repo rule (and the file it is in), or the Finding whose fix or answer the review is waiting on. The user then merges, or tells you to. Step 1 below runs last, just before the merge, on this path too: when the user tells you to merge, run it, then merge (step 2); when the user will merge it themselves, ask them to tell you first, so you can run it before they do. Otherwise merge it yourself once the review is ready to merge and CI is green (or the repo has no CI):

1. **Follow the repo's merge-time steps.** Read the repo's own docs for steps to take just before a merge (the repo's `CLAUDE.md` or `AGENTS.md`, and the release doc, `docs/dev-skills/release.md`) and take each one, in the order they give. **Bump the version, where pull requests bump:** when the release doc says pull requests bump the version and this pull request changes what it says bumps, get the next version number just before the merge the way those docs say (from the user when they say nothing) and wait for it. Have the Implementer add the bump as the pull request's last commit, with the release doc's bump-commit steps, and push. Where the release doc says Releases bump, or the repo has no release doc, or this pull request changes nothing it says bumps, skip this part and change nothing. Then fetch main. If the Ticket branch lacks commits from main, have the Implementer merge main in (a merge, never a rebase) and push. If main was merged since the last Round's recorded head and that merge had conflicts, its resolutions are reviewed as `review-rounds` says under "Merges from main" (the next Round, or after Round 3 its one resolutions check, whose open Importants become bug Tickets); a merge without conflicts needs only the checks. Rerun the checks in the worktree, on the branch's head, and wait for CI (if the repo has any). If main moves again before the merge, repeat this step. A repeat keeps an existing bump commit and its number when main's version is unchanged (get no new number, add no second bump commit). When main's version changed, get a new number; the Implementer merges main in, resolves the version file by taking main's, and redoes the bump as a new commit after the merge, superseding the old bump. "Last commit" means the last of the pull request's own work, so a merge of main after the bump is fine.
2. **Squash-merge** into main, with the pull request's title (typed, as `pr` says) as the commit title and the pull request's body as the commit message, rather than the branch's commit messages joined together. Where the repo's own rules set another title convention, use that. Save the body with `gh pr view <n> --json body --jq .body > <file>`, then `gh pr merge <n> --squash --subject '<title>' --body-file <file>`; the single quotes and the file keep the shell from expanding backticks and `$(...)` in them; in both forms an apostrophe in the title is written as `'\''`. Where `gh pr` fails for lack of GraphQL, read the body with `gh api repos/<owner>/<repo>/pulls/<n> --jq '.body // ""' > <file>` and merge with `gh api --method PUT repos/<owner>/<repo>/pulls/<n>/merge -f merge_method=squash -f commit_title='<title>' -F commit_message=@<file>`.
3. Before completing issues, require `gh api repos/<owner>/<repo>/pulls/<n> --jq .merged` to print `true`, including when the user reports merging the pull request. A failed read or any other result does not authorize completion. Read its body and use the tracker doc's operations to read the state of each issue listed by its closing lines. For absorbed sources, load `issue-absorption` and recheck closure eligibility. For each eligible issue still open, use the tracker doc's **Close** operation with a completed outcome and an explanation naming the pull request. If a read or close fails, stop and tell the user; do not treat it as closed.

## 8. Report

Tell the user (or the coordinator) the pull request link and the outcome: merged with its commit, waiting on a boundary (the Finding and the boundary), or waiting for the user and why (step 7's case), with any bug Tickets the review created. For every merge of yours, also list each ADR, glossary, `CLAUDE.md`, `AGENTS.md` and `REVIEW.md` file it changed, and each agent design answer on it: the items of the `Agent-merged rules:` line.

## 9. Run the retro

Run the `retro` skill on this thread once the pull request is merged and its issue is closed, so the retro looks back on finished work. If you handed the pull request to the user, report as in step 8, stay open, and run the retro after they merge it or tell you that it is merged; if they drop it or close it unmerged, ask whether they want a retro on what happened. If it finds a repeated Bug class to turn into a check, a regular-tier Implementer builds the check on a branch off main, in its own worktree made as in step 2, briefed as in step 3 (you still write no code), and you open its pull request with `pr`, its body recording `Retro origin: <Ticket issue link>`; the check builds no issue, so its body is its spec. Review it as in step 6. At merge, step 7's rule applies: a check that changes `REVIEW.md` is merged by you (squash-merge) unless step 7 stops it, and listed on its `Agent-merged rules:` line. Tell the user (or the coordinator) the retro's outcome.
