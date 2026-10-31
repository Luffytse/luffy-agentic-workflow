---
name: release
description: "Cut a Release and plan the next one: check every issue with the release label is closed, pick the patch, minor or major bump from what shipped, open the bump pull request with its changelog entry for the user to merge, then run the Release planning: propose the next Release's goal and scope. Use when the user wants to cut a release, plan the next release, or ship an urgent fix as its own patch Release."
---

# Release

A **Release** is one version of the project and the few issues it ships. Each of those issues carries the Release's **release label**: the release doc's label prefix plus the version, for example `release-1.4.0`. One **release issue**, titled `Release X.Y.Z`, holds the Release's goal in one sentence, its label, its cap, its scope list and, once it is cut, its notes. The release issue itself carries no release label, so it is never counted among the issues the Release ships. Ordinary pull requests merge to main with no version change; only the Release's **bump pull request** changes the version, and the user merges it. Run this thread at the **premium** tier: the bump size and the next scope are judgement calls the user confirms.

## Before you start

Read the repo's **release doc**, `docs/agents/release.md`: its version file, changelog path, label prefix and extra steps for the bump pull request. If the repo has no release doc, tell the user to run `setup-dev-skills`, which writes one, and stop. Do every issue, label and pull request operation with the commands in the tracker doc, `docs/agents/issue-tracker.md` (with none, use the GitHub repo of the checkout's `origin` remote and the `gh api repos/<owner>/<repo>/...` REST routes).

Pick the path:

- The user has a fix that cannot wait for the current Release: go to "Urgent fix".
- No label with the release doc's prefix exists yet (`gh api repos/<owner>/<repo>/labels --paginate --jq '.[].name'`, keeping the names that start with the prefix): this is the repo's first Release, so go straight to step 5.
- Otherwise: steps 1 to 5 in order.

## 1. Check the current Release is done

Find the open issue titled `Release X.Y.Z` (`gh api "repos/<owner>/<repo>/issues?state=open" --paginate --jq '.[] | select(.pull_request == null and (.title | test("^Release [0-9]+\\.[0-9]+\\.[0-9]+$"))) | {number, title}'`): the release doc's prefix plus its `X.Y.Z` is the **current release label**, and its body holds the goal. If two are open (an urgent fix's patch Release beside the current one), the current Release is the one with the higher version; the other is cut through "Urgent fix". With no open release issue, take the release label of the highest version that an open issue carries (list the labels starting with the prefix as above, and for each, `gh api "repos/<owner>/<repo>/issues?labels=<label>&state=open" --jq length`), tell the user the Release has no release issue, and ask them for its goal in one sentence (step 3 needs it).

List every issue carrying the current release label, open and closed (`gh api "repos/<owner>/<repo>/issues?labels=<label>&state=all" --paginate --jq '.[] | select(.pull_request == null) | {number, title, state, state_reason}'`).

- An issue closed as `completed` shipped.
- An issue closed any other way (`not_planned`, `duplicate`) shipped nothing: list it as dropped.
- An open issue blocks the cut. List every open one to the user, who either waits (stop here and say so; rerun this skill once they close) or carries some over to the next Release: remove the label from each carried-over issue and add a line naming them to the release issue. They become candidates in step 5.

Done when every issue with the current release label is closed, each marked shipped or dropped, and any carried-over issue has lost the label.

## 2. Pick the bump size

What ships is everything merged to main since the last Release, not only the labelled issues. Fetch main, find the commit that set the current version (`git log -1 --format=%H -S '<current version>' origin/main -- <version file>`), and read every commit after it (`git log --format='%h %s' <that commit>..origin/main`), with the merged pull request and issue each one came from.

Give each change one size, by what a project using this one must do:

- **patch**: a fix. Something now does what it already promised; no project has to change anything.
- **minor**: something new that breaks nothing, such as a new command, skill, step or option.
- **major**: a breaking change: a project using this one must do something, because a name it calls was renamed or removed, the format of a file it keeps changed, or a label or setting it needs changed.
- **rides along**: typos, decision records and repo-only changes (docs, tests, evals and tooling that do not ship) never decide the size.

The bump is the biggest size among the changes. While the version is below 1.0.0, a breaking change bumps the minor part instead, and the changelog entry gets a "What to do" list. 1.0.0 is cut only when the user declares the project stable; never propose it on your own. The new version is the current one with that part raised and every part after it set to 0.

If the new version is not the one the current release label names, tell the user. Once they confirm the size (in step 3), rename the label (`gh api --method PATCH repos/<owner>/<repo>/labels/<old label> -f new_name=<new label>`; the issues keep it under its new name) and retitle the release issue and fix its Label line, so all three name the version that ships.

Done when every commit since the last Release has a size or rides along, the bump is the biggest of them, and each change above patch has one line on why.

## 3. Open the bump pull request

Make a branch from the fetched main, and in one commit:

- Change the version in the version file to the new version, and nothing else in that file.
- Add an entry at the top of the changelog (create the file with a `# Changelog` heading if it does not exist):

  ```md
  ## X.Y.Z (<yyyy-mm-dd>)

  <the Release's goal, one sentence, from the release issue>

  - <title of each shipped issue> (#<n>)

  Also merged: <one line per change since the last Release that no shipped issue covers; leave this line out when there is none>.

  ### What to do

  <only for a breaking change: each thing a project using this one must do>
  ```

- Carry out every extra step the release doc lists.

Run the checks the repo's rules name before a push, push, and open the pull request with `pr`. Its body names the release issue, gives the bump size with the line on why for each change above patch, lists the dropped issues, and asks the user to confirm the size. Its Door is one-way: a cut version reaches every project that installs it. The user merges it; never merge it yourself. If the user picks another size, change the version, the entry's heading and the label (step 2), and push again.

Done when the bump pull request is open, its checks pass, and the user has been asked to confirm the size and merge.

## 4. Close the Release

Wait for the user to merge the bump pull request; it is merged when `gh api repos/<owner>/<repo>/pulls/<n> --jq .merged` prints `true`. If the thread has to stop first, tell the user to bring it back here once they merge. Then post the changelog entry as a comment on the release issue, as its notes, and close it.

Done when the bump pull request is merged and the release issue is closed with its notes.

## 5. Release planning

Propose the next Release; the user decides it.

The candidates are every open issue labelled `ready-for-agent` (the label the triage label doc gives that role) that carries no release label (`gh api "repos/<owner>/<repo>/issues?labels=<ready-for-agent label>&state=open" --paginate --jq '.[] | select(.pull_request == null) | {number, title, labels: [.labels[].name]}'`, dropping every issue with a label that starts with the prefix), and every issue carried over in step 1. A Spec and its Tickets are one candidate. Issues in any other triage state belong to `triage`, not here.

Put to the user:

- a **goal** in one sentence, the thing this Release makes true;
- a **scope** of at most 5 candidates (a Spec counting as one), each with one line on why it fits the goal, chosen so the Release takes days, not weeks;
- the candidates left out, grouped, with one line each on why;
- the **next version**: the version in the version file on main (the one just cut) with its patch part raised if the scope is fixes only, its minor part raised if anything in it is new or (below 1.0.0) breaking, or its major part raised if anything in it is breaking at 1.0.0 or later. Its label is the release doc's prefix plus that version; step 2 of that Release renames it if what ships turns out bigger or smaller.

The cap is 5 unless the user raises it, and then only for this Release; the release issue records the cap and the user's reason. Iterate until the user approves a scope.

Then create the label if the repo lacks it, apply it to each approved issue and to every open Ticket of an approved Spec (list the Spec's Tickets with the tracker doc's way of checking a sub-issue link: its sub-issues, `gh api --paginate repos/<owner>/<repo>/issues/<spec>/sub_issues --jq '.[] | {number, state}'`, plus any issue whose body has a `Part of #<spec>` line; keep only the open ones), and open the release issue, with no release label of its own:

```md
Title: Release X.Y.Z

**Goal:** <one sentence>

**Label:** `<prefix>X.Y.Z`. Every issue in this Release carries it.

**Cap:** <5, or the raised cap and the user's reason> (a Spec counts as one). Used: <n>.

## Scope

- #<n> <title>

## Notes

Posted as a comment when the Release is cut. Until then, issues filed during this Release wait for the next Release planning, except Tickets split from a Spec in it.
```

Label nothing the user did not approve.

Tell the user that issues filed from now on wait for the next Release planning, apart from Tickets split from a Spec in this Release, which `to-tickets` gives the label.

Done when every approved issue carries the label, no other issue does, and the release issue is open.

## Urgent fix

A fix that cannot wait for the current Release ships as a patch Release of one issue:

1. Once the user confirms it cannot wait, open its release issue (as in step 5), `Release X.Y.Z` with the version on main's patch part raised, with a one-sentence goal and the one issue in scope, and give that issue the label. It is built like any other issue.
2. Once the fix merges, run steps 2 to 4 with that label as the current release label. Step 2 reads everything merged since the last Release, so issues of the current Release already on main ship too. If any of them is bigger than a fix, tell the user: they either cut at that size, with those issues under "Also merged", or wait until the current Release is cut.
3. Skip step 5: the current Release's plan stands. If its label now names a version at or below the one just cut, rename it (as in step 2) to the version just cut with the same part raised that the old label raised (a minor Release stays minor), with its release issue's title and Label line.

Done when the fix's bump pull request is merged, its release issue is closed, and the current release label names a version above it.
