# Releases

How this repo cuts a Release with the `release` skill: how Releases are named and sized, where the changelog goes, what the cut runs, and the repo's versioning policy.

- **Versioning policy**: Releases bump.
- **Release name**: the name `Release <n>`, the label `release-<n>` and the title `Release <n>`.
- **Release size**: 5.
- **Changelog**: `CHANGELOG.md`, newest entry first. One entry per Release, covering everything merged since the last Release, with its start and end commits.
- **Label prefix**: `release-`.
- **Cut steps**: what the cut runs after the changelog entry is written, in order; the policy section below adds its own. None.
- **Whole-Release check**: `npm test`.

## Policy text

 Ordinary pull requests merge to main with no version change. Only a Release's **bump pull request** changes the version, and the user merges it.

- **Version file**: `package.json`, the `"version"` field. A bump changes only this value in it.
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
- **Extra steps in the bump pull request**: None.
