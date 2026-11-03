# Filing suggestions as Retro issues

Every candidate from step 4 that is not a repeated Bug class becomes a **Retro issue** in the repo where its fix lands, or a "seen again" vote on one that already covers it. Do this before presenting the report.

## Route

- A skill or workflow problem (skill text, review rules, how threads run) goes to the repo named by the `repository` field of the plugin manifest. Read that manifest at the plugin root, two directories above this `retro` folder (the one holding the skills folders): `.claude-plugin/plugin.json`.
- A problem only this project has (its CI, its docs, its steering files) goes to this project's tracker. Find it in `docs/dev-skills/issue-tracker.md`. With no such file, use the GitHub repo of the checkout's `origin` remote, and say so in the report.
- A suggestion goes to one repo, never both. When the two repos are the same, there is nothing to choose.

## Vote or file

1. Search the target repo's open issues labelled `retro` for one that covers the suggestion.
2. On a match, comment `Seen again in <thread link>` plus one line on what happened this time. Do not open a duplicate.
3. Otherwise file an issue. Label `retro`; create the label first if the repo lacks it. Title `Retro: <the problem>`. Never apply `needs-triage`. The body names the source thread (link), what went wrong, and the suggested fix.

If this thread cannot write to the target repo, do not file. Put the full issue text (title, labels, body) in the report so the coordinator can file it.

## Report

List each suggestion with the issue it went to (filed or voted on, with the link), and the full text of any issue you could not file.
