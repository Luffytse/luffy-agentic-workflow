# Filing suggestions as Retro issues

Every candidate from step 4 that is not a repeated Bug class becomes a **Retro issue** in the repo its Scope sends it to, or a "seen again" vote on one that already covers it. Do this before presenting the report.

## Scope and route

Give each candidate a **Scope**, decided by one question: would this happen in a fresh repo using the skills, in the same environment? Write the answer in one clause.

- `skill`: yes, because of a skill's behaviour, or a template, script or format the plugin ships. Filed where the plugin's Retros go.
- `environment`: yes, because of a limit or behaviour of the coding agent or Harness the threads run in, true for any repo run there. Filed where the plugin's Retros go.
- `this repo`: no, it is true only of the repo the session ran in (its CI, its docs, its steering files). Filed in that repo's own tracker, proposing a fix in that repo's own files.

A candidate that mixes scopes is split, one per Scope. A format the plugin ships, even when this repo's copy of it also needs the fix, is `skill`.

- The plugin's Retros go to the repo named by the `repository` field of the plugin manifest. Read that manifest at the plugin root, two directories above this `retro` folder (the one holding the skills folders): `.claude-plugin/plugin.json`.
- This project's tracker is named in `docs/dev-skills/issue-tracker.md`. With no such file, use the GitHub repo of the checkout's `origin` remote, and say so in the report.
- A suggestion goes to one repo, never both. When the two repos are the same, there is nothing to choose.

## Vote or file

1. Search the target repo's open issues labelled `retro` for one that covers the suggestion.
2. On a match, comment `Seen again in <thread link>` plus one line on what happened this time. Do not open a duplicate.
3. Otherwise file an issue. Label `retro`; create the label first if the repo lacks it. Title `Retro: <the problem>`. Never apply `needs-triage`. The body opens with the line `Scope: <value>, <the one-clause reason>`, then names the source thread (link), what went wrong, and the suggested fix.

If this thread cannot write to the target repo, do not file. Put the full issue text (title, labels, body) in the report so the coordinator can file it.

## Report

List each suggestion with the issue it went to (filed or voted on, with the link), and the full text of any issue you could not file.
