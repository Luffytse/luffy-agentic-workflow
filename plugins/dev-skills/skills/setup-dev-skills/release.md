# Releases

How this repo cuts a Release with the `release` skill: how Releases are named and sized, where the changelog goes, what the cut runs, and the repo's versioning policy.

- **Versioning policy**: `<none | pull requests bump | Releases bump>`. _(Keep only the matching "Policy:" section below and delete the other two. Delete every italic note in parentheses when you fill this in.)_
- **Release name**: `<name form, label form and release issue title form, each with <...> placeholders>`. _(A Release is named, never numbered by a version. Default: the name `Release <n>`, the label `release-<n>` and the title `Release <n>`; `<n>` counts up.)_
- **Release size**: `<number of items>`. _(Default 5. A Release takes at most this many items, counted of any kind: a Spec with its Tickets is 1, a lone Ticket is 1, a bug is 1. A severe issue joins past it.)_
- **Changelog**: `<path to CHANGELOG.md>`, newest entry first. One entry per Release, covering everything merged since the last Release, with its start and end commits.
- **Label prefix**: `release-`. _(The label form above starts with it.)_
- **Cut steps**: what the cut runs after the changelog entry is written, in order; the policy section below adds its own. `<none>` _(List here anything else this repo's cut must change or run. Optionally a between-Releases step, for a fix that cannot wait for the next Release.)_
- **Whole-Release check**: `<the checks to run on the changelog pull request's branch, and any clean-up pass>`. _(Recommended: the repo's own checks.)_

## Policy: none

_(Keep this section only when the policy is none; otherwise delete it.)_ This repo keeps no version. A Release's changelog entry lists no versions, and no cut step changes a version.

## Policy: pull requests bump

_(Keep this section only when the policy is pull requests bump; otherwise delete it.)_ Each pull request that changes `<the files that bump the version>` bumps the version as its last commit, with the number given as `<how the number is given, for example by the person who merges>`. A Release opens no pull request to bump: its changelog pull request changes no version.

- **Version file**: `<path to the file that holds the version>`, the `<field or line that holds it>`. A bump changes only this value in it.
- **Extra cut step**: the changelog entry carries the line `Versions: <the versions delivered, oldest first, each once, or "none, the version stays X.Y.Z">. Commits: <start>..<end>.` under the goal. The versions delivered are each value the version file reached since the last Release's end commit.

### The bump at merge

A merge-time step: the merging thread takes it just before the merge of each pull request that changes `<the files that bump the version>`, the user's merge too. A pull request that changes none of them gets no number and no bump.

1. Get the next version number just before the merge, as this doc says it is given (from the user when it says nothing), and wait for it.
2. Have the committer the merge names add the bump as the pull request's last commit, with the bump commit's steps below, and push.
3. If main moves before the merge and the merge-time steps run again: while main's version is unchanged, keep the bump commit and its number (get no new number, add no second bump commit). When main's version changed, get a new number; the committer merges main in, resolves the version file by taking main's, and redoes the bump as a new commit after that merge, superseding the old bump.

"Last commit" means the last of the pull request's own work, so a merge of main after the bump is fine.

### The bump commit

- Change the version in the version file, and nothing else in it.
- Anything else the bump commit must change or run, such as a second file that repeats the version or a check to run before pushing. None.

## Policy: Releases bump

_(Keep this section only when the policy is Releases bump; otherwise delete it.)_ Ordinary pull requests merge to main with no version change. Only a Release's **bump pull request** changes the version, and the user merges it.

- **Version file**: `<path to the file that holds the version>`, the `<field or line that holds it>`. A bump changes only this value in it.
- **Size of each change**, by what a project using this one must do:
  - **patch**: a fix. Something now does what it already promised; no project has to change anything.
  - **minor**: something new that breaks nothing, such as a new command, skill, step or option.
  - **major**: a breaking change: a project using this one must do something, because a name it calls was renamed or removed, the format of a file it keeps changed, or a label or setting it needs changed.
  - **rides along**: typos, decision records and repo-only changes (docs, tests, evals and tooling that do not ship) never decide the size.
- **The new version**: the biggest size among the changes since the last Release, raised on the current version with every part after it set to 0. While the version is below 1.0.0, a breaking change bumps the minor part instead, and the changelog entry gets a "What to do" list for it. 1.0.0 is cut only when the user declares the project stable; never propose it on your own.
- **Extra cut steps**, in order:
  1. Read every change since the last Release's end commit, give it a size, and write one line on why for each change above patch.
  2. Change the version in the version file, and add the changelog entry, whose line under the goal reads `Versions: <the new version>. Commits: <start>..<end>.`
  3. Open the **bump pull request** with the changelog entry, titled `chore(release): <name>` (or by the repo's own title convention, keeping the name in it). Its body names the release issue, gives the size with the line on why for each change above patch, lists the dropped issues, and asks the user to confirm the size. Its Door is one-way: a cut version reaches every project that installs it.
  4. The user merges it; never merge it yourself. If the user picks another size, change the version, the entry and the pull request's title, and push again.
- **Extra steps in the bump pull request**: None. _(List here anything else it must change or run, such as a second file that repeats the version or a check to run before pushing.)_
