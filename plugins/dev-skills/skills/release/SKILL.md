---
name: release
description: "Cut a Release and plan the next: changelog, cut steps, close it, pick the next Release's issues. Use when the user wants to cut a release or plan the next one, or every issue of the current Release has closed, is parked or waits with a parked one."
---

# Release

A **Release** is one named step of a Milestone and the items it ships. An **item** is one piece of work: a Spec with its Tickets, a lone Ticket, or a bug, each counted as 1. Every issue in a Release carries its **release label**. One **release issue** holds its goal, its label, its Milestone, the size used, its Order with each entry's blockers, what was left out, the verdicts of its check against main, the issues that left it at the cut and, once it is cut, its notes; the release issue carries no release label itself. Run this thread at the **premium** tier; only for a dependency graph or another special planning case, ask a **top**-tier subagent's advice. Load `model-tiers` by name for each tier's model; the project's own map overrides it.

The user plans the Milestone and its features with `milestone`; everything in this skill runs without waiting for a reply, except where a step says to stop. A feature the Milestone issue does not list waits for the next Milestone's planning. A fix that cannot wait for the next Release is built and merged like any issue; the next changelog entry lists it.

## Before you start

Read the repo's **release doc**, `docs/dev-skills/release.md`: its Release name (the name, label and release issue title forms), Release size, changelog path, **cut steps** (with what its versioning policy section adds to them) and whole-Release check. With no release doc, or one missing the name forms or the Release size, tell the user to run `setup-dev-skills`, which writes them, and stop. Read the triage label doc for the label of each role (`ready-for-agent`, `bug`, `enhancement`, `next-release`), and the tracker doc (`docs/dev-skills/issue-tracker.md`) for its traps and its named operations. Work the tracker and pull requests with the tools you already use.

The **Milestone** is the one the last release issue's `**Milestone:**` line names, or else the open Milestone issue (the issue `milestone` wrote, carrying a label in the Boundary record's Milestone label form).

The **heading test**: the changelog has an entry for a Release when it has a line `## <name>` followed by a space or the end of the line, so `## Release 1 (2026-11-01)` counts for `Release 1` and `## Release 10` does not.

### Find where you are

Every run, first or rerun, starts here, from freshly fetched main and the tracker; take the first case that fits:

1. An open release issue whose Order lists nothing, or lists an issue that does not carry its label or still carries `next-release` (or a Spec with an open Ticket without the label), is a planning that stopped part way: go to step 5, whose "Rerun first" finishes it. An issue listed under that release issue's `## Left the Release` (step 1), and an open Ticket of a Spec listed there, left on purpose and makes this case not fit.
2. An open release issue whose Order issues each carry its label or are listed under its `## Left the Release` is the **current Release**. If the changelog on main has its entry (the heading test), its changelog pull request merged: go to step 3. Otherwise go to step 1. If several are open, take the oldest and say so in your report.
3. Otherwise, the last release issue is the closed one cut most recently. Go to step 4 unless it holds both end-of-Release records, and then to step 5. With no release issue at all, this is the repo's first Release: go to step 5.

## 1. Check the current Release is done

List every issue carrying the current release label, open and closed (where the tracker lists pull requests with issues, leave them out).

- An issue closed as completed **shipped** when a merged pull request into the default branch closes it with a closing keyword in its body (`Closes #<n>`, `Fixes #<n>`, `Resolves #<n>` and their other tenses). A Ticket merged into a Spec branch shipped when the Spec's pull request, merged into the default branch, closes the Ticket that way. A commit or pull request that only mentions the issue, a negated keyword ("does not close #<n>"), or a close by hand does not count.
- An issue closed any other way (not planned, duplicate) shipped nothing: list it as **dropped**.
- An issue closed as completed that fails the shipped test was closed by hand: check it against main yourself, as the check against main reads any issue (its code and docs, and the changes merged since it was written; open the evidence yourself). If main has the work, it counts as **shipped**, and the release issue's `## Checked against main` section gets the line `- #<n> <title>: closed by hand, shipped: <evidence on main>` (skip an issue it already lists: a rerun counts it shipped). If main does not have the work, reopen the issue with a comment starting `Checked against main:` that says what is missing; it is then an open issue. Ask the user nothing.
- An open issue either leaves the Release or stops the cut. A **parked** issue (the tracker doc's **Park** operation), and an issue that **waits with** it, **leave the Release**. An issue waits with a parked issue when it is open, carries the label, and has at least one open blocker (the tracker doc's **Count open blockers** operation), each of which is parked, is listed under `## Left the Release`, or itself waits with a parked issue. A Spec and its open Tickets (its sub-issues, as step 5 finds them) go together: when the Spec, or one of its Tickets, is parked or waits with a parked issue through its blockers, the others wait with that parked issue. Write its line to the current Release's release issue first, `- #<n> <title>: parked: <why, from its park comment>` or `- #<n> <title>: waits with #<the parked issue>`, under a `## Left the Release` heading of its own (made when the first issue leaves, added to after that; skip an issue the section already lists), then remove its release label. Do nothing else to it: it is not unparked. A rerun lists issues by label and reads that section: an entry whose label is still on gets it removed, so a stop between the two writes loses nothing.
- Any **other** open issue that carries the label **stops the cut**: tell the user which, and stop; a rerun starts once it is closed or parked.

Once every issue left with the label is shipped or dropped, the Release is cut and closed as usual, also when no issue carries the label any more: step 2 then ships what merged since the last Release.

Done when every issue with the current release label is shipped or dropped (also when none is left), and every issue that left has lost the label and is listed under `## Left the Release` in the release issue.

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

With no shipped issue, the list is one line saying that nothing shipped. List a change once, in the first entry that ships it: leave out every `#<n>` that a list line or "Also merged" line of an earlier entry already names (step 1 still counts those issues as shipped).

Then carry out the release doc's **cut steps**, in order, on this branch: they may add to the entry (a line naming versions, for example), change other files, or say how the pull request is titled and who merges it. Where a cut step says something different from this step, the cut step wins. Run the release doc's whole-Release check on the branch (with none named, the checks the repo's rules name before a push). A failure blocks the cut: report it, have each fix built as its own pull request, and rerun this skill once they merge.

Open the pull request with `pr`, titled `docs(release): <name>` unless a cut step or the repo's own title rule says otherwise, keeping the name in the title. Its body names the release issue without a closing keyword (this merge must not close it; step 3 closes it with the notes), gives the start and end commits, lists the dropped issues and gives the check's result; its Door is two-way unless a cut step says otherwise. Merge it by loading `merging` by name, naming this thread as the committer of each commit the finish needs: the pull request is the changelog pull request and it builds no issue, so `merging` closes none; the merge is a squash with the pull request's body as the commit message, titled as the pull request is titled, its checks passing make it ready (it has no review), and its pre-merge step is to fetch main: if main moved past the end commit, update the branch onto it, redo the end commit, the entry and the cut steps, and rerun the check, so no merge falls between two Releases. Where `merging` brings the pull request to the user, or a cut step says a person merges it, stop until it merges (the rerun finds its entry on main and goes to step 3).

Done when the changelog pull request, with its entry, its cut steps and a passing whole-Release check, is merged.

## 3. Close the Release

Fetch main. From the changelog on main take the entry headed with this Release's name (the heading test), through the line before the next `## ` heading or the end of the file; if it is missing, stop and tell the user, and never substitute another entry. Post it as a comment on the release issue, as its notes, and close the issue.

Done when the release issue is closed with its notes.

## 4. Run the end-of-Release pass

Load `retro-planning` by name and run its Retro planning for the Release just closed; then load `triage` and run its Triage batch (`TRIAGE-BATCH.md`), naming the release issue. Both run before the planning, so it sees what they changed.

After each one, comment on the closed release issue, first line `<!-- release end-of-Release pass -->`, second line `retro-planning ran for this Release: <its record's link>.` (or `triage ran for this Release.`). If one cannot run, write `<skill> could not run: <why>.` instead and go on: the planning reads what the tracker shows, and your report names the pass that did not run. A rerun skips each skill that already has its record.

Done when the closed release issue holds a record for `triage` and one for `retro-planning`.

## 5. Plan the next Release

With no open Milestone, plan nothing: tell the user the next Release needs a Milestone, planned with `milestone` (a small Release is a Milestone with one Release), list any severe or `next-release` issues waiting, and stop. Otherwise read the Milestone issue: its goal, its features table in order with its "After" column, its acceptance criteria and its exclusions.

**Rerun first.** When "Find where you are" found an open release issue whose planning stopped part way, write into that issue and open no second one. If its Order lists entries, that Order stands: plan and check nothing again, finish the labels and marks "Write it down" applies (an entry that now reads parked is labelled too; the cut takes it out), and report. If its Order lists nothing, plan into it as below.

### What planning reads

- The **features** are the issues of the Milestone issue's features table, in its order; a Ticket of a listed Spec belongs to its Spec.
- The **waiting issues** are the other open issues at `ready-for-agent` or marked `next-release`, whatever their category label (a bug, a chore, a `retro` issue with its brief), that carry no release label, do not read parked (the tracker doc's **Park** operation) and do not belong to a later Milestone (one the Milestone issue leaves to the next). One is **severe** when it is a security hole, lost data, or delivery stopped (nothing can merge or ship).
- An **unplanned feature** (a Spec, or another issue that adds a feature, that the table does not list; never a `retro` issue) is no waiting issue: it is not taken and not proposed, and waits for the next Milestone's planning. No other issue is taken.
- An issue's **open blockers** are those the tracker doc's **Count open blockers** operation counts (a blocker closed without the work done stays open); a Spec's are those of the Spec and of its Tickets that lie outside it.

### Check against main

Before taking a feature or a waiting issue, and nothing else, check it against freshly fetched main: its code and docs, and the changes merged since it was written. Give each one verdict:

- **still valid**: main still has the problem, or does not yet do what the issue asks;
- **already fixed** or **obsolete**: main no longer has the problem or already does what it asks, or what it is about is gone from main (the Obsolete test of `triage`'s sweep, test 3, confirmed as that test says);
- **changed scope**: part of it still holds, or it holds in another place or form;
- **cannot tell**: the issue or main does not say enough; say what is missing.

Any other verdict carries its evidence on main: the file or text, and the commit or pull request when you find it. For more than 5 issues, batches may go to **premium**-tier subagents that only read and return verdicts with evidence. Open that evidence yourself before acting, make every write yourself, and read an issue again just before writing to it; if it changed, check it again.

- **Already fixed or obsolete**: close it as completed, with the reason and where on main, which unblocks what it blocks. A feature or a Ticket of a planned Spec is not closed (that would change the Milestone's agreement): it goes to the user as one question, and the feature is left out.
- **Changed scope**: write the issue's whole body back with only that change and a one-line note naming what on main changed it, and read it back. A change to the Milestone's goal, acceptance criteria or exclusions is not made: it goes to the user as one question, and that feature is left out.
- **Cannot tell**: no write; the issue is not taken, and the release issue lists it as unchecked.
- **Still valid**: no write.

A question to the user is a comment on the issue and a line in your report; nothing waits on the reply. The close reason, the note and the question each start `Checked against main:`, and each verdict goes in the release issue's `## Checked against main` section. A rerun skips an issue with a verdict in this planning's release issue, or with a `Checked against main:` note or question written since the last Release was closed.

### The slice

Go down the features table in its order, never re-ordered, and take each feature that is open, carries no release label and does not read parked, until the items taken reach the release doc's **Release size**: stop at the first feature that, with the waiting issues the pass below would place before it, no longer fits.

A feature whose open blocker is parked, waits with a parked issue, is an unplanned feature or is one no agent can take (at another role, or a feature left out) is **left out**, naming that blocker (a Spec with a parked Ticket is left out naming that Ticket); so, through it, is every later feature that depends on it. One blocker leaves no feature out: a **setup Ticket** for the person (an issue at `ready-for-human` that planning published for an account, product or credential a live step needs). The feature is taken, its `After:` line names that Ticket, and only the Tickets it blocks wait for the person.

**The bug dependency pass.** Before taking a feature, decide for each waiting issue not yet placed whether it blocks that feature: a blocker link says so, or the feature's work would be built on the fault the issue describes. Place each one that does just before the feature, in the order below, and record the blocker link with the tracker doc's **Blocking** operation where it is missing. A placed waiting issue's own open blockers are placed before it the same way, in the order they must land; when one of them is not a waiting issue (parked, waiting with a parked issue, or one no agent can take), place none of them and leave the feature out, naming it. A feature is taken once each of its open blockers is in the Order or is a setup Ticket.

**After the features**, take the other waiting issues: severe, then marked `next-release`, then the rest, oldest first within each, until the size is full. Every severe issue still waiting then joins past the size; nothing else does. A waiting issue is placed only when its own open blockers are in the Order, placed before it as the pass places them; otherwise it is left out, naming them. Each issue appears once; a Spec is one entry standing for its Tickets. Every feature and waiting issue not taken is **left out**, with why: the size was reached, the blocker it names, or its check against main.

### When nothing qualifies

When nothing is taken, open no release issue and write nothing to the tracker beyond what the check against main did (an open release issue found by "Rerun first" stays as it is). Tell the user why, naming each feature left out with its blocker, each question the check raised and each issue unchecked, and stop.

### Name it

Fill the release doc's name, label and title forms for the next Release: the last Release's values with the last placeholder raised by one, unless the release doc gives another rule (such as a new Milestone starting again at 1). If a closed issue already carries that label, a dropped Release used the name: take the next value instead. Write the goal in one sentence: what this Release makes true, toward the Milestone's goal.

### Write it down

When at least one entry is taken, open the release issue, with no release label of its own:

```md
Title: <the title form, filled>

**Goal:** <one sentence>

**Label:** `<label>`. Every issue in this Release carries it.

**Milestone:** #<n>

**Size:** <the release doc's size>. Used: <items taken within the size>.<, plus <k> severe past the size>

## Order

1. #<n> <title>: <why it is here: its row of the table, the feature it blocks, severe, the mark's reason, or its age>. After: <#<n>, #<n>: its open blockers when planned, or none>

## Left out

- #<n> <title>: <why: the size was reached, the blocker it names, or its check against main>

## Checked against main

Main at `<commit>`.

- #<n> <title>: <verdict>: <evidence, or what is missing; leave it out when the verdict is still valid>

## Notes

Posted as a comment when the Release is cut. Issues filed from now on wait for the next planning, apart from Tickets added to a Spec in this Release.
```

The tracker's blocker links stay the record; the `After:` line is for reading. Write `None.` under a heading with nothing in it. Then create the label if the repo lacks it, and apply it to each issue in the Order and to every open Ticket of a Spec in it (its sub-issues, by the tracker doc's way of checking a sub-issue link, and any issue whose body has a `Part of #<spec>` line). Remove `next-release` from each taken issue that carries it, once it carries the release label; an issue left out keeps its mark. Label nothing outside the Order.

Report to the user the Order, the size used, what was left out and why, and each question the check against main raised; nothing waits on a reply.

Done when nothing was taken, nothing was written beyond the check's own writes, and the user was told why; or else the release issue is open with its sections, each Order entry with its `After:` line and each issue taken with a verdict, every issue in its Order (and every open Ticket of a Spec in it) carries the label, no other issue does, and no taken issue still carries `next-release`.
