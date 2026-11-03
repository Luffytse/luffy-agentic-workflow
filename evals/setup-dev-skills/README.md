# setup-dev-skills eval

A fixture run that checks `setup-dev-skills` asks for the Boundary record's values and writes the record from its seed, and that every file it writes lands in `docs/dev-skills/` with only `REVIEW.md` and the `CLAUDE.md` block at the root. Rerun when the skill's Section F, its `boundaries.md` seed, the paths it writes or its re-run diff changes.

## Fixture

A scratch git repo outside this one, with a made-up GitHub remote (`https://github.com/example-org/scratch-app.git`), a `README.md`, a `package.json` and one commit. No `CLAUDE.md`, `AGENTS.md`, `docs/` or `REVIEW.md`. The remote cannot be reached, so the run skips the reachability call, label creation and the GitHub settings check and says "not checked: fixture".

## Scripted conversation

The user answers in section order, the way the skill asks:

- Section A: accept GitHub.
- Section B: keep the default labels; no agent-only labels.
- Section C: single-context.
- Section D: no rules of its own.
- Section E (Releases): no.
- Section F (Boundaries): irreversible actions agents may take, "delete test data that agents generate while implementing"; actions needing approval, "delete production or customer data"; budget, "at most 20 dollars of API usage a month"; check-in interval and Milestone label form, accept the recommended answers.
- Approve every draft; create `CLAUDE.md`.

## Pass

- Section F asks one question per value, each leading with a recommended answer.
- `docs/dev-skills/boundaries.md` holds the five values and the Milestone-issue rule; the three values the user gave replace the seed's placeholders, and the check-in interval and label form stay at the recommended answers.
- The `## Agent skills` block has a `### Boundaries` part, and `docs/dev-skills/index.md` lists the record with a "read when" line.
- Every file written lands under `docs/dev-skills/` (the issue-tracker, triage-label and domain docs, the Boundary record and `index.md`), except the starter `REVIEW.md` at the repo root and the `CLAUDE.md` block; the block points at `docs/dev-skills/index.md`, and nothing else is written under `docs/` or at the root.
- A re-run shows no change to the three values the user gave, asks again only for a value the record lacks, and reports "no change" for every file.
