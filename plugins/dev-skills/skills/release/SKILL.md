---
name: release
description: "Cut a Release and plan the next one: check every issue with the release label is closed, pick the patch, minor or major bump from what shipped, open the bump pull request with its changelog entry for the user to merge, then run the Release planning: propose the next Release's goal and scope. Use when the user wants to cut a release, plan the next release, or ship an urgent fix as its own patch Release."
---

# Release

A **Release** is one version of the project and the few features it ships. A **feature** is one piece of work the user would name as one thing: a Spec with all its Tickets, a lone Ticket with the issues it absorbs, or a few related issues the user agrees to treat as one. Each issue in a feature carries the Release's **release label**: the release doc's label prefix plus the version, for example `release-1.4.0`. One **release issue**, titled `Release X.Y.Z`, holds the Release's goal in one sentence, its label, its cap on features, its scope list and, once it is cut, its notes. The release issue itself carries no release label, so it is never counted among the issues the Release ships. Ordinary pull requests merge to main with no version change; only the Release's **bump pull request** changes the version, and the user merges it. Run this thread at the **premium** tier: the bump size and the next scope are judgement calls the user confirms.

## Before you start

Read the repo's **release doc**, `docs/agents/release.md`: its version file, changelog path, label prefix and extra steps for the bump pull request. If the repo has no release doc, tell the user to run `setup-dev-skills`, which writes one, and stop. Do every issue, label and pull request operation with the commands in the tracker doc, `docs/agents/issue-tracker.md` (with none, use the GitHub repo of the checkout's `origin` remote and the `gh api repos/<owner>/<repo>/...` REST routes).

Pick the path:

- The user has a fix that cannot wait for the current Release: go to "Urgent fix".
- An open release issue has the `**Urgent fix:**` line (step 1's command lists it with `urgent` true): read the `#<n>` after `**Urgent fix:** ships` in its body (`gh api repos/<owner>/<repo>/issues/<release issue> --jq .body`), then that issue (`gh api repos/<owner>/<repo>/issues/<n> --jq '{state, state_reason}'`). Closed as `completed` and shipped (the shipped test in step 1): first fetch main and see whether its bump pull request has merged: the version file on main equals that release issue's version, or the changelog on main already has an entry headed with that version (a heading line `## <version>` followed by a space or the end of the line, so `## 0.23.1 (2026-10-31)` counts and `## 0.23.10 (2026-11-02)` does not; a later Release may have been cut on top). If so, go to step 4; otherwise go to item 2 of "Urgent fix" for that Release. Closed any other way (`not_planned`, `duplicate`): the fix shipped nothing, so tell the user and ask whether to drop the urgent Release by closing its release issue, instead of cutting it. Still open, or closed as `completed` but not shipped: read on (step 1 treats it as open).
- No label with the release doc's prefix exists yet (`gh api repos/<owner>/<repo>/labels --paginate --jq '.[].name'`, keeping the names that start with the prefix): this is the repo's first Release, so go straight to step 5.
- Otherwise: steps 1 to 5 in order.

## 1. Check the current Release is done

Find the open issue titled `Release X.Y.Z` (`gh api "repos/<owner>/<repo>/issues?state=open" --paginate --jq '.[] | select(.pull_request == null and (.title | test("^Release [0-9]+\\.[0-9]+\\.[0-9]+$"))) | {number, title, urgent: ((.body // "") | contains("**Urgent fix:**"))}'`): the release doc's prefix plus its `X.Y.Z` is the **current release label**, and its body holds the goal. Fetch main, then read the version from the field the release doc names for the version file on main and compare it whole (exact equality) with the release issue's version: if they are equal, or the changelog on main has an entry headed with that version (the heading test in "Pick the path"), its bump pull request has merged, so go straight to step 4. An urgent fix's release issue (one with `urgent` true, whose body has the `**Urgent fix:**` line that "Urgent fix" writes) is never the current Release here: it is cut only through "Urgent fix". If more than one without that line is open, list them and ask the user which to cut. When no release issue is open, or only urgent fixes', take the release label of the highest version that an open issue carries, leaving out every urgent fix's label (list the labels starting with the prefix as above, and for each, `gh api "repos/<owner>/<repo>/issues?labels=<label>&state=open" --jq length`), tell the user the Release has no release issue, and ask them for its goal in one sentence (step 3 needs it), then open the release issue for it with the template in step 5 (scope: the labelled issues), so steps 3 and 4 have one to name, comment on and close. If no open issue carries such a label either, there is no current Release to cut: tell the user so and go to step 5.

The **open Releases' versions** are every version that the title of an open `Release X.Y.Z` issue names (the command above lists them, urgent or not) plus every version that a release label carried by an open issue names (listed as above). Count both: a Release whose labelled issues have all closed but whose bump pull request is not merged yet is still open, and only its release issue's title shows it. Steps 2 and 5 take a new version above all of these (step 2 leaves out the current Release's own version), and "Urgent fix" takes the next free patch on main's version, so no two open Releases ever share a version, title or label.

List every issue carrying the current release label, open and closed (`gh api "repos/<owner>/<repo>/issues?labels=<label>&state=all" --paginate --jq '.[] | select(.pull_request == null) | {number, title, state, state_reason}'`).

- An issue closed as `completed` shipped only if a pull request that closes it is merged into the default branch (the **shipped test**: list the merged pull requests whose body closes it, `gh api --paginate repos/<owner>/<repo>/issues/<n>/timeline --jq '.[] | select(.event == "cross-referenced" and .source.issue.pull_request.merged_at != null and ((.source.issue.body // "") | test("(^|[^A-Za-z])(close[sd]?|fix(e[sd])?|resolve[sd]?):? +#<n>\\b"; "i"))) | .source.issue.number'`, and for each, `gh api repos/<owner>/<repo>/pulls/<p> --jq '{merged, base: .base.ref}'` must read `merged` true and the default branch as `base`. A Ticket merged into a Spec branch has no such pull request of its own; the Spec's pull request is the one found, when its body closes the Ticket with a keyword directly before its number). A commit that only mentions the issue does not count. An issue closed as `completed` that fails the shipped test, such as one closed by hand, is not shipped: treat it as open and tell the user, who either confirms the fix is on main (then it counts as shipped) or carries it over.
- An issue closed any other way (`not_planned`, `duplicate`) shipped nothing: list it as dropped.
- An open issue, or one closed as `completed` that fails the shipped test, blocks the cut. List every open one to the user, who either waits (stop here and say so; rerun this skill once they close) or carries some over to the next Release: remove the label from each carried-over issue and add a line naming them to the release issue. They become candidates in step 5.

Done when every issue with the current release label is closed, each marked shipped or dropped, and any carried-over issue has lost the label.

## 2. Pick the bump size

What ships is everything merged to main since the last Release, not only the labelled issues. Fetch main, find the commit that set the current version (`git log -1 --format=%H -S '<current version>' origin/main -- <version file>`), and read every commit after it (`git log --format='%h %s' <that commit>..origin/main`), with the merged pull request and issue each one came from.

Give each change one size, by what a project using this one must do:

- **patch**: a fix. Something now does what it already promised; no project has to change anything.
- **minor**: something new that breaks nothing, such as a new command, skill, step or option.
- **major**: a breaking change: a project using this one must do something, because a name it calls was renamed or removed, the format of a file it keeps changed, or a label or setting it needs changed.
- **rides along**: typos, decision records and repo-only changes (docs, tests, evals and tooling that do not ship) never decide the size.

The bump is the biggest size among the changes. While the version is below 1.0.0, a breaking change bumps the minor part instead, and the changelog entry gets a "What to do" list. 1.0.0 is cut only when the user declares the project stable; never propose it on your own. The new version is the highest of the current version and the open Releases' versions (step 1) other than the current Release's own, with that part raised and every part after it set to 0.

If the new version is not the one the current release label names, tell the user. Once they confirm the size (in step 3), rename the label with `gh api --method PATCH repos/<owner>/<repo>/labels/<old label> -f new_name=<new label>` (the issues keep it under its new name; if a label with the new name already exists, left from a dropped Release, ask the user and delete it first) and retitle the release issue and fix its Label line, so all three name the version that ships.

Done when every commit since the last Release has a size or rides along, the bump is the biggest of them, and each change above patch has one line on why.

## 3. Open the bump pull request

First do the open-bump check below. Then make a branch from the fetched main, and in one commit:

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

The open-bump check: a bump pull request's title has the word "release" followed by the version as a whole number (`chore(release): <version>`, so a rerun can find it), so look for one already open for this release issue (`gh api "repos/<owner>/<repo>/pulls?state=open" --paginate --jq '.[] | select(.title | test("release\\S*\\s+v?<version>($|[^0-9])"; "i")) | {number, title, body}'`, for this version (write its dots as `\\.` in the pattern) and for the version the label named before a size change). A title match counts only if its body contains `#<issue number>` of this release issue as a whole number; one whose body does not is no match. When nothing matches (a repo whose own title rule leaves out the word "release" is not found by title), list the open pull requests whose body names it (`gh api "repos/<owner>/<repo>/pulls?state=open" --paginate --jq '.[] | select((.body // "") | test("#<issue number>($|[^0-9])")) | {number, title}'`); if you cannot tell which is the bump pull request, ask the user. If one is open, do not open a second: tell the user, and update that one (its branch, entry and, after a size change, its title) instead, using its `number` in step 4.

Run the checks the repo's rules name before a push, push, and open the pull request with `pr`, titled by the same rule, `chore(release): <version>` (where the repo's own rules set another title convention, use that, keeping the version in it). Its body names the release issue, gives the bump size with the line on why for each change above patch, lists the dropped issues, and asks the user to confirm the size. Its Door is one-way: a cut version reaches every project that installs it. The user merges it; never merge it yourself. If the user picks another size, change the version, the entry's heading, the label, the release issue's title and its Label line (step 2) and this pull request's title, and push again.

Done when the bump pull request is open, its checks pass, and the user has been asked to confirm the size and merge.

## 4. Close the Release

Wait for the user to merge the bump pull request; it is merged when `gh api repos/<owner>/<repo>/pulls/<n> --jq .merged` prints `true`. If the thread has to stop first, tell the user to bring it back here once they merge. Then post the changelog entry as a comment on the release issue, as its notes, and close it. When you arrive by the shortcut that skips step 3 (the bump pull request had already merged), there is no pull request to poll: the entry to post is the top entry of the changelog file on main, and the release issue is the one whose version the version file names. When you came from the urgent bullet, it is the urgent release issue, and the entry to post is the changelog entry headed with its version, not the top one.

Done when the bump pull request is merged and the release issue is closed with its notes.

## 5. Release planning

Propose the next Release; the user decides it.

The candidates are every open issue labelled `ready-for-agent` (the label the triage label doc gives that role) that carries no release label (`gh api "repos/<owner>/<repo>/issues?labels=<ready-for-agent label>&state=open" --paginate --jq '.[] | select(.pull_request == null) | {number, title, labels: [.labels[].name]}'`, dropping every issue with a label that starts with the prefix), and every issue carried over in step 1. A Spec and its Tickets are one feature; so is a lone Ticket with the issues it absorbs. Issues in any other triage state belong to `triage`, not here.

Put to the user:

- a **goal** in one sentence, the thing this Release makes true;
- a **scope** of at most 5 features (fewer is fine), each naming the feature, the issues in it and one line on why it fits the goal, chosen so the Release takes days, not weeks. Group related candidates into one feature only when the user would name them as one thing, and say so in the line;
- the candidates left out, grouped, with one line each on why;
- the **next version**: the highest of the version in the version file on main (the one just cut) and the open Releases' versions (step 1), with its patch part raised if the scope is fixes only, its minor part raised if anything in it is new or (below 1.0.0) breaking, or its major part raised if anything in it is breaking at 1.0.0 or later. Its label is the release doc's prefix plus that version; step 2 of that Release renames it if what ships turns out bigger or smaller.

The cap is 5 features unless the user raises it, and then only for this Release; the release issue records the cap and the user's reason, and the next Release goes back to 5. Iterate until the user approves a scope.

Then create the label if the repo lacks it, apply it to each approved issue and to every open Ticket of an approved Spec (list the Spec's Tickets with the tracker doc's way of checking a sub-issue link: its sub-issues, `gh api --paginate repos/<owner>/<repo>/issues/<spec>/sub_issues --jq '.[] | {number, state}'`, plus any issue whose body has a `Part of #<spec>` line; keep only the open ones), and open the release issue, with no release label of its own:

```md
Title: Release X.Y.Z

**Goal:** <one sentence>

**Label:** `<prefix>X.Y.Z`. Every issue in this Release carries it.

**Cap:** <5 features, or the raised cap and the user's reason>. Used: <n>.

## Scope

- **<feature>**: <one line on why it fits the goal>
  - #<n> <title>

## Notes

Posted as a comment when the Release is cut. Until then, issues filed during this Release wait for the next Release planning, except Tickets split from a Spec in it.
```

Label nothing the user did not approve.

Tell the user that issues filed from now on wait for the next Release planning, apart from Tickets split from a Spec in this Release, which `to-tickets` gives the label.

Done when every approved issue carries the label, no other issue does, and the release issue is open.

## Urgent fix

A fix that cannot wait for the current Release ships as a patch Release of one issue:

1. Once the user confirms it cannot wait, take the version: the version on main with its patch part raised by one, because an urgent fix is nearly always a patch on what is on main and planned Releases usually change the major or minor part. If an open Release already holds that exact version (the open Releases' versions, step 1), raise the patch part again until the version is free. Never move above a planned minor or major Release's version: with a planned `1.5.0` open and main at `1.4.0`, the fix is `1.4.1`, not `1.5.1` (a planned patch Release at `1.4.1` only makes the fix `1.4.2`). So the fix never shares a version, title or label with another open Release, and the planned Release keeps its own. Open its release issue (as in step 5), `Release X.Y.Z` with that version, with a one-sentence goal, the one issue in scope, and this line under the goal: `**Urgent fix:** ships #<n> on its own, outside the planned Release.` Give that issue the label, and remove any other release label it carries, so it is not counted in the planned Release too. It is built like any other issue.
2. Once the fix is on main (the shipped test), run steps 2 to 4 with this urgent release issue and its own label as the current Release, never the planned one. Step 2 reads everything merged since the last Release, so issues of the planned Release already on main ship too. If any of them is bigger than a fix, tell the user: they either cut at that size, with those issues under "Also merged", or wait until the planned Release is cut. Here step 2 works from the version on main read at cut time, not the highest of the open Releases' versions. For a fix, keep the version its release issue names only while it is above main's version; if main has reached it or passed it (a planned or sibling Release was cut first), take main's version with its patch part raised by one, and again until no open Release holds it, and rename the label and retitle as step 2 says. For a bigger size, raise that part of main's version; if an open Release already holds the result, do not raise the patch past it: wait until that Release is cut, then work again from main. So the urgent Release never takes a planned Release's version or label, never sets the version file below main's, and never jumps above a planned Release.
3. Skip step 5: the planned Release's plan stands. While the planned Release is still open, leave its label, its release issue's title and its Label line as they are, even if they now name a version at or below the one just cut; its own step 2 moves them above the cut version when it is cut. If its bump pull request is open, it now conflicts with the urgent one (both edit the version file and the changelog's top) and sets a version at or below the cut: tell the user not to resolve it by hand, and to bring the planned Release back here, whose step 2 takes a version above the cut and whose step 3 updates that open pull request (the open-bump check) with the version, the entry's heading, the label, the release issue's title and its Label line together.

Done when the fix's bump pull request is merged, its release issue is closed, and the planned Release, if still open, keeps its label and title, and the user has been told to rerun it if its bump pull request is open.
