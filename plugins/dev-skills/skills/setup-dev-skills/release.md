# Releases

How this repo versions and cuts a Release with the `release` skill: where the version lives, who bumps it, where the changelog goes, how Releases and their labels are named, and the whole-Release check.

- **Bump mode**: `<Releases bump | pull requests bump>`. _(Releases bump: ordinary pull requests leave the version alone and a Release's bump pull request changes it. Pull requests bump: every pull request that changes `<the files that bump the version>` bumps it as its last commit, with the number given just before merge; a Release opens no bump pull request, and writes its changelog entry in a changelog pull request that changes no version.)_
- **Version file**: `<path to the file that holds the version>`, the `<field or line that holds it>`. A bump changes only this value in it.
- **Changelog**: `<path to CHANGELOG.md>`, newest entry first.
- **Label prefix**: `release-`. _(When Releases bump, a Release's label is `release-X.Y.Z`, for example `release-1.4.0`, and its release issue is titled `Release X.Y.Z`.)_
- **Release name**: `<name form, label form and release issue title form, each with <...> placeholders>`. _(Only when pull requests bump: a Release is named, not numbered. For example the name `Phase <n>`, the label `release-p<n>` and the title `Release Phase <n>`. Delete this line when Releases bump.)_
- **Whole-Release check**: `<the checks to run on the changelog pull request's branch, and any clean-up pass>`. _(Only when pull requests bump. Delete this line when Releases bump.)_

## The bump commit

_(Only when pull requests bump; delete this section when Releases bump.)_ The merging thread adds it as the pull request's last commit, just before merge, with the number given as `<how the number is given, for example by the person who merges>`:

- Change the version in the version file, and nothing else in it.
- Anything else the bump commit must change or run, such as a second file that repeats the version or a check to run before pushing. None.

## Extra steps in the bump pull request

_(Only when Releases bump; delete this section when pull requests bump.)_ None. _(List here anything else this repo's bump pull request must change or run, such as a second file that repeats the version or a check to run before pushing.)_
