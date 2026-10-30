---
name: implement
description: "Build one lone Ticket as its Ticket thread: an Implementer subagent builds it test-first and shows evidence, you open the pull request with pr, run the code-review Rounds, then merge or bring the pull request to the user. Use when you are handed a lone Ticket (a bug fix, chore or small feature under no Spec) to build and ship."
---

You are the **Ticket thread**: you coordinate one lone Ticket from issue to merged pull request (ADR 0004). **Implementers write the code.** You brief them, check their evidence, open the pull request, run the Review, talk to the user and merge. You never write or edit code yourself, not even to resolve a merge conflict.

The issue tracker should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

## 1. Read the ticket

Fetch the ticket from the issue tracker and state its title. If the reference is ambiguous, ask.

- If it is a Spec, or a Ticket under one, stop and use `implement-spec` for the Spec instead.
- Check its blocking edges. If any blocker is not merged, stop and tell the user (or the coordinator) which.

Start at `docs/index.md` and open only the docs that fit the ticket (with no index, fall back to `GLOSSARY.md` or `GLOSSARY-MAP.md`, and `docs/adr/`).

Done when you have stated the title, every blocker is merged, and you know the ticket's **Model tier**: premium if the issue says so, otherwise regular.

## 2. Make the Ticket branch

Create the Ticket branch from an up-to-date main and push it. Done when the branch exists on the remote.

## 3. Start one Implementer

Start **one Implementer** subagent on the ticket's tier. Brief it with pointers, not copies:

- the ticket link and the Ticket branch, and that it commits there;
- start at `docs/index.md`;
- build test-first with the `tdd` skill, at seams agreed before the first test;
- report its evidence: the tests that fail before and pass after, the typecheck or the repo's checks, screenshots for anything visual (or "not visual"), and its one-way-door call (would reverting its commits undo everything the change did, including anything outside git?).

Give trivial jobs, such as rerunning a test suite, to a cheap subagent.

Keep this same Implementer for every later fix and merge conflict on the ticket: continue it by message. Only if it can no longer be reached, start a new Implementer on the same tier with a handoff (ticket, branch, what is done, what is open), and tell the user you did.

## 4. Check the evidence

Read the Implementer's report against the ticket's acceptance criteria and rerun the checks (a cheap subagent can). Anything missing or failing goes back to the Implementer. Done when every acceptance criterion has evidence and the checks pass on the branch's head, or, when the repo has no checks, the evidence says what was checked instead.

## 5. Open the pull request

Write the body with the `pr` skill: it closes the ticket, carries the evidence in its Evidence section, and the Implementer's call as its Door. Push and open the pull request.

## 6. Review in Rounds

Run the `code-review` skill on the pull request yourself, in this thread: its Finders and Verifiers are subagents, and a subagent cannot start them. Its rules set the Review depth (a depth in your brief wins), the Rounds, the stop rule and the 5-Round cap.

Before each Round, fetch main. If it moved, have the Implementer merge main into the Ticket branch (a merge, never a rebase), resolve any conflicts and push, so the Round reviews the resolutions.

After each Round, send its Important Findings and "fix" Nits to the Implementer by message; it fixes, commits and pushes, then the next Round runs. On a clean Round 2 to 5, the Implementer makes the final "fix" Nits commit before you post that Round's comment; no further Round reviews it. After the last Round, file Pre-existing Findings as `code-review` says.

Done when a Round 2 to 5 is clean, or the 5-Round cap is hit.

## 7. Merge, or bring it to the user

Bring the pull request to the user, and do not merge it, if any of these holds:

- the Review ran at Deep depth;
- its Door is one-way;
- it changes an ADR, the glossary, a `CLAUDE.md`, a `REVIEW.md` or the `code-review` skill;
- the Review hit the 5-Round cap.

The user then merges, or tells you to. Otherwise merge it yourself once the Review is clean and CI is green (or the repo has no CI):

1. Fetch main. If the Ticket branch lacks commits from main, have the Implementer merge main in (a merge, never a rebase). If that merge had conflicts, run one more Round over the merge's conflict resolutions (step 6) if the 5-Round cap allows; otherwise bring the pull request to the user. Rerun the checks on the branch's head and wait for CI (if the repo has any).
2. **Squash-merge** into main, with a commit message you write that summarises the final change and names the ticket, rather than the branch's commit messages joined together.

## 8. Report

Tell the user (or the coordinator) the pull request link and the outcome: merged with its commit, or waiting for the user and why.

## 9. Run the retro

Whether the pull request was merged or handed to the user, run the `retro` skill on this thread. If it finds a repeated Bug class to turn into a check, a regular-tier Implementer builds the check on a branch off main (you still write no code), and you open its pull request with `pr` and run the `code-review` Rounds as in steps 5 to 7. A check that changes `REVIEW.md` goes to the user, not merged by you. Add the retro's outcome to your report.
