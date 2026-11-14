---
name: implement
description: "Build one lone Ticket as its Ticket thread: build it test-first, pull request, review, merge. Use when you are handed a lone Ticket (a bug fix, chore or small feature under no Spec) to build and ship."
---

You are the **Ticket thread**: you build one lone Ticket yourself, in your own checkout, and take it from issue to merged pull request. Read the project's issue-tracker doc before any tracker operation; if there is none, tell the user to run `setup-dev-skills`.

**When you need the user.** Ask: do I already know exactly what I will do once the user says yes?

- **Yes: it is an action** (an approval to run on their device, a step the environment refuses, a credential, a merge that is theirs). Ask once, as soon as you know it, naming the exact action. Comment on the Ticket that you wait and for what, and tell the coordinator if one runs. Go on with everything that does not depend on it, then wait. The Ticket is not parked.
- **No: it is a decision** (the Ticket cannot be built as written, or a choice it does not settle would change what was agreed or cannot be undone). Push your work, park the Ticket with the tracker doc's **Park** operation, giving the question, the options and your recommendation, tell the user (or the coordinator) and stop. The user's answer lifts the park.

A choice inside what the Ticket agreed that can be undone is yours: make it and name it in the pull request. Never split the Ticket.

## 1. Read the ticket

Fetch the ticket from the issue tracker and state its title; if the reference is ambiguous, ask. A Spec goes to `implement-spec`, carrying the Spec. A Ticket under a Spec is its Spec thread's: say so to whoever handed it to you and stop. Stop and tell the user (or the coordinator) when the tracker doc's **Count open blockers** operation finds a blocker uncleared, its **Park** operation reads the ticket parked, or the ticket carries the `ready-for-human` role.

### Check against main

Before you make anything, on every entry, read the ticket against freshly fetched main: its code and docs, and what merged since the ticket was written. Your own branch and pull request are not evidence. Give one verdict:

- **still valid**: go on.
- **already fixed** or **obsolete**: write no code. Give the coordinator (the user, when none runs) the evidence on main, the file and the commit or pull request, and stop; it closes or re-plans the ticket.
- **changed scope** or **cannot tell**: give the coordinator what changed or what is missing, with the same evidence, comment on the Ticket that you wait for its answer, and build nothing. With no coordinator it is a decision for the user: park as "When you need the user" says. On the answer, or the lifted park, re-enter at step 1, checking again only what merged since.

## 2. Build

Make the Ticket branch off freshly fetched main in your own checkout and push it; where the harness gives the thread one designated branch, that branch is the Ticket branch. On re-entry, go on from the pushed branch and its pull request.

Build with `tdd`, at seams agreed before the first test. A bug whose cause is not known goes to `diagnosing-bugs` first, then to `tdd` for the fix; a bug whose failing test is its reproduction goes straight to `tdd`. Run each new test and see it fail before the fix: a failure inferred or read off the code is not evidence. A run you cannot make yourself is asked of the user, as an action. Give trivial or noisy jobs, such as rerunning a test suite, to a cheap-tier subagent (`model-tiers` maps the tier), so your context stays small.

Before the pull request, check your diff against each Always-check line of the repo's review rules file, if it has one, as the reviewer will.

## 3. Open the pull request

Write its title and body with the `pr` skill: its closing lines, its Evidence (each new test's observed failure, the checks, screenshots for anything visual) and its Door. Open it.

## 4. Review

Run `agentic-review` on the pull request: its Round 0 picks the level and, above None, hands over to `review-rounds`. Supply the Ticket, the pull request, the branch, the base and any level the user asked for.

Before each Round, fetch main; if it moved, merge it into the Ticket branch (a merge, never a rebase), resolve any conflicts and push. Fix each open Finding, or dispute it with evidence, as `review-rounds` says, to the review's end. After Round 3, report each bug Ticket its sort filed; you build none of them.

## 5. Merge

Load `merging` by name and follow it to its end. Give it the pull request and the Ticket it builds; the method, a **squash-merge** into main titled with the pull request's typed title; yourself as the committer; and no pre-merge step of your own.

## 6. Report

Tell the user (or the coordinator) the pull request link and the outcome as `merging` hands it back: merged with its commit, or with the user and what stops it, with each bug Ticket the review filed.

If the pull request is with the user, stay open. Once they merge it or tell you it is merged, run `merging`'s "After the merge", then step 7; if they close it unmerged, ask whether they want a retro.

## 7. Run the retro

Run `retro` once the pull request is merged and its issue is closed; it files issues and builds nothing.
