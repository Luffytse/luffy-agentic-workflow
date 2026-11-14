# Releases

How this repo cuts a Release with the `release` skill: how Releases are named and sized, where the changelog goes, what the cut runs and the whole-Release check.

- **Release name**: `<name form, label form and release issue title form, each with <...> placeholders>`. _(A Release is named, never numbered by a version. Default: the name `Release <n>`, the label `release-<n>` and the title `Release <n>`; `<n>` counts up.)_
- **Release size**: `<number of items>`. _(Default 5. A Release takes at most this many items, counted of any kind: a Spec with its Tickets is 1, a lone Ticket is 1, a bug is 1. A severe issue joins past it.)_
- **Changelog**: `<path to CHANGELOG.md>`, newest entry first. One entry per Release, covering everything merged since the last Release, with its start and end commits.
- **Label prefix**: `release-`. _(The label form above starts with it.)_
- **Cut steps**: what the cut runs after the changelog entry is written, in order. `<none>` _(List here anything this repo's cut must change or run, such as a version bump. Optionally a between-Releases step, for a fix that cannot wait for the next Release.)_
- **Whole-Release check**: `<the checks to run on the changelog pull request's branch, and any clean-up pass>`. _(Recommended: the repo's own checks.)_
