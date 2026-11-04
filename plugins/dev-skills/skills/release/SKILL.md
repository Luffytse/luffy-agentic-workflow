---
name: release
description: "Cut a Release and plan the next one: check its issues shipped, write the changelog entry, run the release doc's cut steps and whole-Release check, close it, run triage and retro-planning, then rank every candidate and pick the next Release up to the Release size. Use when the user wants to cut a release or plan the next one, or every issue of the current Release has closed."
---

# Release

A **Release** is one named step of a Milestone and the items it ships. An **item** is one piece of work: a Spec with its Tickets, a lone Ticket, or a bug, each counted as 1. Every issue in a Release carries its **release label**. One **release issue** holds its goal, its label, its Milestone, the size used, its ranked order, what was left out and, once it is cut, its notes; the release issue carries no release label itself. Run this thread at the **premium** tier: the ranking and the reruns are judgement calls. Load `model-tiers` by name for the model each tier is in your coding agent; the project's own tier map overrides it.

The user plans the Milestone and its features with `milestone`; everything in this skill runs without waiting for a reply, except where a step says to stop. A feature to plan is proposed to the user, and nothing waits on the answer. A fix that cannot wait for the next Release is built and merged like any issue; the next changelog entry lists it.

## Before you start

Read the repo's **release doc**, `docs/dev-skills/release.md`: its Release name (the name, label and release issue title forms), Release size, changelog path, **cut steps** (with what its versioning policy section adds to them) and whole-Release check. With no release doc, or one missing the name forms or the Release size, tell the user to run `setup-dev-skills`, which writes them, and stop. Read the triage label doc for the label of each role (`ready-for-agent`, `bug`, `enhancement`, `next-release`), and the tracker doc (`docs/dev-skills/issue-tracker.md`) for its traps and its named operations. Work the tracker and pull requests with the tools you already use.

The **Milestone** is the one the last release issue's `**Milestone:**` line names, or else the open Milestone issue (the issue `milestone` wrote, carrying a label in the Boundary record's Milestone label form).

The **heading test**: the changelog has an entry for a Release when it has a line `## <name>` followed by a space or the end of the line, so `## Release 1 (2026-11-01)` counts for `Release 1` and `## Release 10` does not.

### Find where you are

Every run, first or rerun, starts here, from freshly fetched main and the tracker; take the first case that fits:

1. An open release issue whose Order lists nothing, or lists an issue that does not carry its label or still carries `next-release` (or a Spec with an open Ticket without the label), is a planning that stopped part way: go to step 5, whose "Rerun first" finishes it. A release issue written before the Order list (a `## Scope` list and no `## Order`) whose label an issue carries is not one: it is the current Release of case 2, and the issues carrying its label are its scope.
2. An open release issue whose label its issues carry is the **current Release**. If the changelog on main has its entry (the heading test), its changelog pull request merged: go to step 3. Otherwise go to step 1. If several are open, take the oldest and say so in your report.
3. No open release issue, but open issues carry a release label that no release issue names: a planning stopped before its release issue was opened: go to step 5.
4. Otherwise, the last release issue is the closed one cut most recently. Go to step 4 unless it holds both end-of-Release records, and then to step 5. With no release issue at all, this is the repo's first Release: go to step 5.

## 1. Check the current Release is done

List every issue carrying the current release label, open and closed (where the tracker lists pull requests with issues, leave them out).

- An issue closed as completed **shipped** when a merged pull request into the default branch closes it with a closing keyword in its body (`Closes #<n>`, `Fixes #<n>`, `Resolves #<n>` and their other tenses). A Ticket merged into a Spec branch shipped when the Spec's pull request, merged into the default branch, closes the Ticket that way. A commit or pull request that only mentions the issue, a negated keyword ("does not close #<n>"), or a close by hand does not count.
- An issue closed any other way (not planned, duplicate) shipped nothing: list it as **dropped**.
- An open issue, or one closed as completed that fails the shipped test, **blocks the cut**. Stop and report each one to the user, who waits (rerun once they close) or carries some over. A carried-over issue loses the release label, and the release issue gains a line naming it; a closed issue that failed the shipped test is carried over only after the user reopens it, or counts as shipped once the user confirms the fix is on main. Carried-over issues are candidates in step 5.

Done when every issue with the current release label is shipped or dropped, and every carried-over issue has lost the label.

## 2. Write the changelog entry and run the cut steps

What ships is everything merged to main since the last Release, not only the labelled issues. Find the commit where the last Release ended: the end commit of the top changelog entry's `Commits: <start>..<end>` line; for a top entry with no such line, the commit that added its heading line; with no entry, everything on main ships. The **start commit** is that commit and the **end commit** is main's tip. Read every commit in between, with the pull request and issue each came from. The last Release's own changelog merge rides along unlisted.

An open pull request whose body names this release issue is this Release's changelog pull request from an earlier run: update it, and open no second one. Otherwise make a branch from the fetched main and add an entry at the top of the changelog (create the file with a `# Changelog` heading if it does not exist):

```md
## <name> (<yyyy-mm-dd>)

<the Release's goal, one sentence, from the release issue>

Commits: <start>..<end>.

- <title of each shipped issue> (#<n>)

Also merged: <one item per change since the last Release that no shipped issue covers, each with its #<n> (the issue's, or the pull request's when no issue covers it); leave this line out when there is none>.

### What to do

<only for a change that makes a project using this one do something: each thing it must do; leave the section out otherwise>
```

List a change once, in the first entry that ships it: leave out every `#<n>` that a list line or "Also merged" line of an earlier entry already names (step 1 still counts those issues as shipped).

Then carry out the release doc's **cut steps**, in order, on this branch: they may add to the entry (a line naming versions, for example), change other files, or say how the pull request is titled and who merges it. Where a cut step says something different from this step, the cut step wins. Run the release doc's whole-Release check on the branch (with none named, the checks the repo's rules name before a push). A failure blocks the cut: report it, have each fix built as its own pull request, and rerun this skill once they merge.

Open the pull request with `pr`, titled `docs(release): <name>` unless a cut step or the repo's own title rule says otherwise, keeping the name in the title. Its body names the release issue without a closing keyword (this merge must not close it; step 3 closes it with the notes), gives the start and end commits, lists the dropped issues and gives the check's result; its Door is two-way unless a cut step says otherwise. Merge it by loading `merging` by name, naming this thread as the committer of each commit the finish needs: the pull request is the changelog pull request and it builds no issue, so `merging` closes none; the merge is a squash with the pull request's body as the commit message, titled as the pull request is titled, its checks passing make it ready (it has no review), and its pre-merge step is to fetch main: if main moved past the end commit, update the branch onto it, redo the end commit, the entry and the cut steps, and rerun the check, so no merge falls between two Releases. Where `merging` brings the pull request to the user, or a cut step says a person merges it, stop until it merges (the rerun finds its entry on main and goes to step 3).

Done when the changelog pull request, with its entry, its cut steps and a passing whole-Release check, is merged.

## 3. Close the Release

Fetch main. From the changelog on main take the entry headed with this Release's name (the heading test), through the line before the next `## ` heading or the end of the file; if it is missing, stop and tell the user, and never substitute another entry. Post it as a comment on the release issue, as its notes, and close the issue.

Done when the release issue is closed with its notes.

## 4. Run the end-of-Release pass

Load `triage` by name and run its Triage batch for the Release just closed, naming its release issue; then load `retro-planning` by name and run its Release-end Retro planning for the same Release. Both run before the planning, so it sees what they closed and marked `next-release`.

After each one, comment on the closed release issue, first line `<!-- release end-of-Release pass -->`, second line `triage ran for this Release.` (or `retro-planning ran ...`). If one cannot run (it fails, or the thread cannot start it), write `<skill> could not run: <why>.` instead and go on: the planning ranks what the tracker shows, and your report names the pass that did not run. A rerun skips each skill that already has its record.

Done when the closed release issue holds a record for `triage` and one for `retro-planning`.

## 5. Plan the next Release

With no open Milestone, plan nothing: tell the user the next Release needs a Milestone, planned with `milestone` (a small Release is a Milestone with one Release), list any severe or `next-release` issues waiting, and stop. Otherwise read the Milestone issue: its goal, features in order, acceptance criteria and exclusions.

**Rerun first.** If "Find where you are" found an open release issue whose planning stopped part way: when its Order lists issues, that order stands; rank nothing again and finish only what is missing (see "Write it down"). When its Order lists nothing, plan it as below and write the result into that issue instead of opening another. If open issues carry a release label that no release issue names, those issues are the scope so far: keep each, count it toward the size, rank the rest around them, and open the release issue for the whole set. On every rerun path, an issue in the scope that now reads parked (the tracker doc's **Park** operation) stays in it and is reported as parked and skipped for building; remove no release label.

### The candidates

Every open issue that carries no release label and does not read parked, of these kinds:

- a **severe** issue (a security hole, lost data, or delivery stopped: nothing can merge or ship), at `ready-for-agent` or marked `next-release`;
- an issue marked `next-release`;
- a **planned feature**: one the Milestone issue lists (including any added since the last Release), together with its open blockers (the tracker doc's **Count open blockers** operation); a Ticket of a listed Spec belongs to its Spec;
- a `ready-for-agent` bug;
- every issue carried over in step 1.

A parked issue is left out, waiting on the user to lift its park. An **unplanned feature** (an enhancement, or any other feature-sized issue, that the Milestone issue does not list) is never ranked, whatever its label or whoever suggested it: propose each one to the user in one line, saying the Milestone issue does not list it; the user plans it with `milestone` or not. Any other issue, such as one at `needs-triage`, `needs-info`, `ready-for-human` or `wontfix`, is not a candidate.

### The ranked list

Sort every candidate into one list, in descending priority:

1. **Group 1**: severe issues, then issues marked `next-release`; within each, oldest first.
2. **Group 2**: the planned features, in the order you set this planning (below), each preceded by its open blockers in the order they must land. A blocker already placed higher stays where it is. A feature with a blocker an agent cannot take (parked, not at `ready-for-agent`, or closed as not planned, duplicate or `wontfix`, which never clears) is left out, naming that blocker.
3. **Group 3**: `ready-for-agent` bugs, oldest first.

An issue that meets several conditions goes in its highest group, and first within it: a severe issue also marked `next-release` comes before the other severe issues; a bug that blocks a planned feature goes before that feature in group 2, not in group 3. Each issue appears once. A Spec is one entry, standing for its Tickets.

**Re-order the planned features** at every planning, starting from the Milestone issue's order: a feature that others depend on comes first; then the one that moves the Milestone's goal furthest; the Milestone issue's order breaks ties. Write one line of reason for each feature's place, and for every other entry one line on why it is in its group (the harm, the mark's reason, the feature it unblocks, the bug's age).

### Pick from the top

Take entries from the top, one item at a time, until the items taken reach the release doc's **Release size**. Once the size is full, every severe issue still in the list joins anyway, past the size; nothing else does. Every ranked candidate not taken is **left out**, with why: the size was reached, a blocker an agent cannot take, or parked.

### Name it

Fill the release doc's name, label and title forms for the next Release: the last Release's values with the last placeholder raised by one, unless the release doc gives another rule (such as a new Milestone starting again at 1). If a closed issue already carries that label, a dropped Release used the name: take the next value instead. Write the goal in one sentence: what this Release makes true, toward the Milestone's goal.

### Write it down

Open the release issue, with no release label of its own:

```md
Title: <the title form, filled>

**Goal:** <one sentence>

**Label:** `<label>`. Every issue in this Release carries it.

**Milestone:** #<n>

**Size:** <the release doc's size>. Used: <items taken within the size>.<, plus <k> severe past the size>

## Order

1. #<n> <title>: <one line of reason>

## Left out

- #<n> <title>: <why>

## Proposed to the user

- #<n> <title>: <an unplanned feature; the Milestone issue does not list it>

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets split from a Spec in this Release.
```

Write `None.` under a heading with nothing in it. Then create the label if the repo lacks it, and apply it to each issue in the Order and to every open Ticket of a Spec in it (its sub-issues, by the tracker doc's way of checking a sub-issue link, and any issue whose body has a `Part of #<spec>` line). Remove `next-release` from each taken issue that carries it, once it carries the release label; an issue left out keeps its mark. Label nothing outside the Order.

Report to the user the Order with its reasons, the size used, what was left out and why, and the features proposed; nothing waits on a reply.

When the caller asks for a dry run, run this step read-only: write nothing to the tracker and return the Release it would plan.

Done when the release issue is open with its Goal, Size, Order, Left out and Proposed sections, every issue in its Order (and every open Ticket of a Spec in it) carries the label, no other issue does, and no taken issue still carries `next-release`.
