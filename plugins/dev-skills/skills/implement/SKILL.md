---
name: implement
description: "Build one lone Ticket as its Ticket thread: an Implementer subagent builds it test-first and shows evidence, you open the pull request with pr, run the agentic-review Rounds, then merge or bring the pull request to the user. Use when you are handed a lone Ticket (a bug fix, chore or small feature under no Spec) to build and ship."
---

You are the **Ticket thread**: you coordinate one lone Ticket from issue to merged pull request. **Implementers write the code.** You brief them, check their evidence, open the pull request, run the Review, talk to the user and merge. You never write or edit code yourself, not even to resolve a merge conflict.

Read the configured project issue-tracker doc before tracker operations. If none was provided, tell the user to run `setup-dev-skills`.

## 1. Read the ticket

Fetch the ticket from the issue tracker and state its title. If the reference is ambiguous, ask.

- If it is a Spec, or a Ticket under one, stop and use `implement-spec` for the Spec instead.
- Use the tracker doc's **Count open blockers** operation and its completion rules. If any blocker remains uncleared, stop and tell the user (or the coordinator) which.
- Read whether the ticket is parked with the tracker doc's **Park** operation. If it is, stop and tell the user (or the coordinator): it waits on the user, and the user lifts the park.

Start at `docs/index.md` and open only the docs that fit the ticket (with no index, fall back to `GLOSSARY.md` or `GLOSSARY-MAP.md`, and `docs/adr/`).

Done when you have stated the title, every blocker is cleared under the tracker doc, and you know the ticket's **Model tier**: premium if the issue says so, otherwise regular.

## 2. Make the Ticket branch

Give the Implementer its own git worktree on the Ticket branch, so nothing you do to read a branch can move the checkout its commits land in. Fetch main (the repo's default branch), then make the worktree yourself, outside your checkout: `git worktree add <path> -b <ticket-branch> origin/<default-branch>`, and push the branch from it (`git -C <path> push -u origin <ticket-branch>`). Your own checkout stays where it is. Done when the branch exists on the remote and the worktree is on it.

## 3. Start one Implementer

Start **one Implementer** subagent on the ticket's tier. Load `model-tiers` by name for the model each tier is in your coding agent; the project's own tier map overrides it. Brief it with pointers, not copies:

- the ticket link, its worktree path and the Ticket branch, and that it commits there and works only in that worktree, running every git command as `git -C <path> ...` (a shell may start each command back in your checkout);
- the worktree is a fresh checkout and may need its dependencies installed again;
- start at `docs/index.md`;
- build test-first with the `tdd` skill, at seams agreed before the first test;
- before each push, check that `git status -sb` shows the Ticket branch (never a detached HEAD), and after it, report that `git rev-parse origin/<branch>` equals `HEAD`, as evidence the push landed;
- leave the version as it is on main until the merge step: the merge step adds any bump the release doc calls for, with a number handed out then;
- report its evidence: the tests that fail before and pass after, the typecheck or the repo's checks, screenshots for anything visual (or "not visual"), and its one-way-door call (would reverting its commits undo everything the change did, including anything outside git?).

Give trivial jobs, such as rerunning a test suite, to a cheap subagent.

Keep this same Implementer, in the same worktree, for every later fix and merge of main on the ticket: continue it by message. Only if it can no longer be reached, start a new Implementer on the same tier with a handoff (ticket, worktree, branch, what is done, what is open), and tell the user you did. If the worktree is gone (for example the machine was reclaimed): fetch, run `git worktree prune`, make it again with `git worktree add <path> <ticket-branch>`, and brief the Implementer that anything it had not pushed is lost.

**You never run `git checkout`, `switch`, `stash` or `reset` in the Implementer's worktree**, because they move the checkout under it: a later commit lands off the branch and its push says "Everything up-to-date". To read the branch's head for a Round or a check, fetch and read: `git fetch origin <ticket-branch>`, then `git show` or `git diff` against `origin/<ticket-branch>`, or `git archive origin/<ticket-branch>` into a scratch directory.

## 4. Check the evidence

Read the Implementer's report against the ticket's acceptance criteria and rerun the checks in the Implementer's worktree (a cheap subagent can, running no git command that moves the checkout). Check that it reports `origin/<branch>` equal to `HEAD` for every push. Anything missing or failing goes back to the Implementer. Done when every acceptance criterion has evidence and the checks pass on the branch's head, or, when the repo has no checks, the evidence says what was checked instead.

## 5. Open the pull request

Write the title and body with the `pr` skill: it closes the ticket (and any other issue it lists, one `Closes #<n>` line each, as `pr` says), carries the evidence in its Evidence section, and the Implementer's call as its Door. Open the pull request; the branch is already pushed, and the Implementer pushes any later commits.

## 6. Review in Rounds

Run the complete `agentic-review` workflow on the pull request in this thread. Supply the Ticket, pull request, Implementer's worktree path, Ticket branch, base and any requested Review depth. Run your git reads with `git -C <path> ...` so they inspect that branch; pass the worktree path to the review workflow for its reviewers.

Before each Round, fetch main. If it moved, have the same Implementer merge main into the Ticket branch (a merge, never a rebase), resolve any conflicts and push. Supply the resulting head and merge context to the review workflow.

Route the workflow's fixes to the same Implementer by message; it fixes, commits and pushes, or, where `agentic-review` allows a rebuttal, sends one with its evidence in place of a fix. Return its commit, evidence and any rebuttals to `agentic-review` and continue that workflow through its completion, including its final fix and filing actions. Review policy and completion belong to `agentic-review`; the merge decision below remains yours.

The workflow reports the outcome `park`, with the link to the attempt record, when the Review will not settle and an earlier attempt has already failed on this Ticket (it does so only inside a Milestone). Then the pull request is **parked**: leave it open and unmerged, skip step 7, and do not bring it to the user as a merge decision. Mark the Ticket parked with the tracker doc's **Park** operation, giving the attempt record and the pull request as the history. Then tell the user once, in one message, which is your step 8 report: that the Ticket is parked, why (the attempt record's cause and lesson, in a line or two), and the links to the pull request and the attempt record. Send no earlier or second message about it. The build ends there as reported; the retro (step 9) waits until the pull request lands.

## 7. Merge, or bring it to the user

First decide whether the pull request is **inside a Milestone**. Read the Boundary record (the one the repo's `CLAUDE.md` or `AGENTS.md` points to, usually `docs/agents/boundaries.md`) for its Milestone label form. The pull request is inside a Milestone when the ticket carries a label in that form; then read the Milestone issue (the issue that carries the same label and holds the Milestone's goal) for allowed or forbidden actions of its own, which win over the record's for this ticket. With no Boundary record, or no label in its form on the ticket, the pull request is outside a Milestone.

**Inside a Milestone**, bring the pull request to the user, and do not merge it, only if any of these holds:

- it crosses a boundary: it takes, or its merge would take, an action that the Milestone issue forbids or says needs the user's approval, or one the Boundary record says needs the user's approval and the Milestone issue does not explicitly allow; or its Door is one-way and, for any of its irreversible actions, the Milestone issue does not explicitly allow agents to take it (or, where the Milestone issue does not mention it, the record does not);
- the repo's own rules (its `CLAUDE.md`, the project instructions, its docs) say a person merges it.

Deep depth alone does not stop the merge, and neither does a change to an ADR, the glossary, a `CLAUDE.md` or a `REVIEW.md`. When you merge such a change yourself, list it for the Milestone review: before the merge, add a line to the pull request body naming each ADR, glossary, `CLAUDE.md` and `REVIEW.md` file it changes (`Milestone review: <files>`), and name them in your report (step 8). When you merge a pull request on which an agent answered design Findings (`agentic-review` lists them, each by its row id and the link to its record), the same line names each answer too (`Milestone review: <files>; design answers: <id> <link>, ...`, without the files part when no such file changed), and so does your report.

**Outside a Milestone**, bring the pull request to the user, and do not merge it, if any of these holds:

- the Review ran at Deep depth;
- its Door is one-way;
- it changes an ADR, the glossary, a `CLAUDE.md` or a `REVIEW.md`, or anything else the repo's own rules (its `CLAUDE.md`, the project instructions, its docs) say a person merges;
- the Review ended with Result "5-Round cap reached" (Round 5 was not clean; a clean Round 5 is a clean Round like any other);
- an agreed answer to a design Finding that changes the pull request came when no Round is left to review it.

When you bring the pull request to the user, name what stops the merge, so the user can decide quickly: the boundary (the action, and whether the Milestone issue or the Boundary record lists it), the repo rule (and the file it is in), the case on the list outside a Milestone, or the Review's Result. The user then merges, or tells you to. Step 1 below runs last, just before the merge, on this path too: when the user tells you to merge, run it, then merge (step 2); when the user will merge it themselves, ask them to tell you first, so you can run it before they do. Otherwise merge it yourself once the Review is clean and CI is green (or the repo has no CI):

1. **Bump the version, where pull requests bump.** Read the release doc (the one the repo's `CLAUDE.md` or `AGENTS.md` points to, usually `docs/agents/release.md`). When it says pull requests bump the version and this pull request changes what it says bumps, ask for the next version number just before the merge (from the coordinator, or from the user when no coordinator runs) and wait for it. Have the Implementer add the bump as the pull request's last commit, with the release doc's bump-commit steps, and push. Where the release doc says Releases bump, or the repo has no release doc, or this pull request changes nothing it says bumps, skip this part and change nothing. Then fetch main. If the Ticket branch lacks commits from main, have the Implementer merge main in (a merge, never a rebase) and push. If that merge had conflicts, return its resolutions to the complete `agentic-review` workflow for a merge-only Round under its depth and completion rules; if its Round budget is exhausted, bring the pull request to the user. Rerun the checks in the worktree, on the branch's head, and wait for CI (if the repo has any). If main moves again before the merge, repeat this step. A repeat keeps an existing bump commit and its number when main's version is unchanged (ask for no new number, add no second bump commit). When main's version changed, ask for a new number; the Implementer merges main in, resolves the version file by taking main's, and redoes the bump as a new commit after the merge, superseding the old bump. "Last commit" means the last of the pull request's own work, so a merge of main after the bump is fine.
2. **Squash-merge** into main, with the pull request's title (typed, as `pr` says) as the commit title and the pull request's body as the commit message, rather than the branch's commit messages joined together. Where the repo's own rules set another title convention, use that. Save the body with `gh pr view <n> --json body --jq .body > <file>`, then `gh pr merge <n> --squash --subject '<title>' --body-file <file>`; the single quotes and the file keep the shell from expanding backticks and `$(...)` in them; in both forms an apostrophe in the title is written as `'\''`. Where `gh pr` fails for lack of GraphQL, read the body with `gh api repos/<owner>/<repo>/pulls/<n> --jq '.body // ""' > <file>` and merge with `gh api --method PUT repos/<owner>/<repo>/pulls/<n>/merge -f merge_method=squash -f commit_title='<title>' -F commit_message=@<file>`.
3. Before completing issues, require `gh api repos/<owner>/<repo>/pulls/<n> --jq .merged` to print `true`, including when the user reports merging the pull request. A failed read or any other result does not authorize completion. Read its body and use the tracker doc's operations to read the state of each issue listed by its closing lines. For absorbed sources, load `issue-absorption` and recheck closure eligibility. For each eligible issue still open, use the tracker doc's **Close** operation with a completed outcome and an explanation naming the pull request. If a read or close fails, stop and tell the user; do not treat it as closed.

## 8. Report

Tell the user (or the coordinator) the pull request link and the outcome: merged with its commit, waiting for the user and why, or parked with the link to its attempt record and why it would not settle (the one message of step 6). Inside a Milestone, also list each ADR, glossary, `CLAUDE.md` and `REVIEW.md` file a merge of yours changed, and each agent design answer on it, for the Milestone review.

## 9. Run the retro

Run the `retro` skill on this thread once the pull request is merged and its issue is closed, so the retro looks back on finished work. A parked pull request has not finished: run no retro until the user lifts the park and it lands. If you handed the pull request to the user, report as in step 8, stay open, and run the retro after they merge it or tell you that it is merged; if they drop it or close it unmerged, ask whether they want a retro on what happened. If it finds a repeated Bug class to turn into a check, a regular-tier Implementer builds the check on a branch off main, in its own worktree made as in step 2, briefed as in step 3 (you still write no code), and you open its pull request with `pr` and run the `agentic-review` Rounds as in steps 5 to 7. Merge it under step 7's two forms, with the ticket's Milestone membership (the check's pull request has no issue of its own): inside a Milestone, a check that changes `REVIEW.md` is merged by you and listed for the Milestone review; outside one, a check that changes `REVIEW.md` goes to the user, not merged by you. Tell the user (or the coordinator) the retro's outcome.
