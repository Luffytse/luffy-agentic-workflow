# Releases

How this repo cuts a Release with the `release` skill: where the version lives, where the changelog goes, and how the release labels are named. Ordinary pull requests leave the version alone; only a Release's bump pull request changes it.

- **Version file**: `<path to the file that holds the version>`, the `<field or line that holds it>`. The bump pull request changes only this value in it.
- **Changelog**: `<path to CHANGELOG.md>`, newest entry first.
- **Label prefix**: `release-`, so a Release's label is `release-X.Y.Z` (for example `release-1.4.0`) and its release issue is titled `Release X.Y.Z`.

## Extra steps in the bump pull request

None. _(List here anything else this repo's bump pull request must change or run, such as a second file that repeats the version or a check to run before pushing.)_
