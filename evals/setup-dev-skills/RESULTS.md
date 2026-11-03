# Results

One entry per fixture run of `setup-dev-skills`, newest first. Record the commit and the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`. An entry written inside an open pull request names the commit and plugin version it ran on as its base.

## Template

```
### <date>, commit <sha>, dev-skills <version>

Setup: <fixture repo, how the run was driven>
Conversation: <the scripted answers>
File written: <path and content>
Not exercised: <paths of the skill this run did not reach>
Pass: yes | no. Lessons: <what to change, if anything>
```

## Runs

### 2026-11-03, commit 1b5a6ff, dev-skills 0.49.0 (base main 1a17cd7): fresh headless sessions after the docs/dev-skills/ move (#552)

Setup: the README's scratch repo (made-up remote `https://github.com/example-org/scratch-app.git`, `README.md`, `package.json`, one commit) in a temporary directory. Each run was a fresh headless `claude -p` session with the checkout's plugin loaded by `--plugin-dir <checkout>/plugins/dev-skills` (the session's init record lists `dev-skills` at that path), tools limited to reading and writing files and read-only `git`, and the scripted answers given up front in the prompt, so the session logged the questions it would ask rather than holding a live conversation. Run 1 on the regular tier. Run 2, the re-run on run 1's committed result: two attempts on the regular tier stopped early on a model safeguard false positive before writing anything, and the third, on the premium tier, completed.

Conversation: Sections A to F in order, each question with its recommended answer, then the scripted answer (GitHub; default labels, no agent-only labels; single-context; no own rules; Releases no, though it recommended yes for the `package.json` version; Section F's five values, the three given and the two recommended); create `CLAUDE.md`. Run 2 asked nothing new: Section F kept every existing value.

File written (run 1): `docs/dev-skills/issue-tracker.md`, `docs/dev-skills/triage-labels.md`, `docs/dev-skills/domain.md`, `docs/dev-skills/boundaries.md` (the five values and the Milestone-issues section, the three given values in place of the placeholders) and `docs/dev-skills/index.md` (a line for each of the four, `REVIEW.md` linked as `../../REVIEW.md` with its "read when reviewing a change or adding an Always check line" line, and `README.md`); the starter `REVIEW.md` at the repo root; `CLAUDE.md` with the `## Agent skills` block, which starts "Start at `docs/dev-skills/index.md`", points each part at its `docs/dev-skills/` file and has a `### Boundaries` part. Nothing else was written under `docs/` or at the root; no release doc (Section E no); reachability, labels and settings "not checked: fixture".

Re-run (run 2): "no change" for every file (the four `docs/dev-skills/` files, `REVIEW.md`, the `CLAUDE.md` block and `docs/dev-skills/index.md`); it wrote nothing, and `git status` on the scratch repo was clean afterwards.

Also checked, in this repo: a fresh headless session loading the checkout's plugin the same way ran `to-tickets` as a dry run (read-only tools) on a one-line plan. Its first read was `docs/dev-skills/index.md`, then `docs/dev-skills/issue-tracker.md` (and the triage-label, Boundary record and release docs in `docs/dev-skills/`); it quoted the tracker doc's "Create an issue" and "Apply / remove labels" operations and published nothing.

Not exercised: label creation and the settings report (no reachable remote), a live conversation, a re-run with a changed value, a multi-context repo, a glossary split, and the legacy `CONTEXT.md` offer.

Pass: yes. Every file landed under `docs/dev-skills/`, `REVIEW.md` at the root, the block points at `docs/dev-skills/index.md`, and the re-run reported no change. Lessons: as in the 2026-11-01 run, the `### Boundaries` part summarised the approval, budget and check-in values but not the allowed action (that value is in the record only).

### 2026-11-01, commit 8802449 (base), dev-skills 0.26.0 (base): fresh subagent

Setup: a subagent given only a copy of the `setup-dev-skills` folder (SKILL.md and its seeds) and the scripted answers of the README, in a scratch repo with a made-up GitHub remote. The answers were supplied up front, so it logged the questions it would ask rather than holding a live conversation. Run by the coordinator, reported to the Implementer of #422.

Conversation: Section F asked five questions in order, each leading with a recommended answer (actions agents may take: none; approval: none for a repo with no data of value, else the user names them; budget: none; check-in: 1 hour; label form: `milestone-<n>`), then said a Milestone issue may add allowed or forbidden actions for its own issues and wins over the record for them. Other questions: keep default labels (yes), agent-only labels (no), own rules (no), Releases (no), and which of `CLAUDE.md` or `AGENTS.md` to create (the skill gives no wording; the agent made one up).

File written: `docs/agents/boundaries.md`, identical to the file of the entry below (five values, the three given ones filled, the Milestone-issues section). Also written: `CLAUDE.md`, `REVIEW.md`, `docs/index.md` and the issue-tracker, triage-label and domain docs; no release doc (Section E no); no labels created, settings "not checked: fixture". Differences from the seed and the hand-driven run: its `### Boundaries` block listed the approval, budget and check-in values but not the allowed action (that value is only in the record), and it wrote its `docs/index.md` line as a table row, because it was told not to read the `docs-index` skill.

Re-run: a fresh draft from the seed differed from the written record in exactly the three filled lines, which a literal draft-and-diff shows as a revert to placeholders. The skill said to keep earlier values but not how: a skill gap. Fix in Section F: on a re-run the fresh draft is filled from the existing record's values before diffing, and the user is asked again only for a value the record lacks or that the user wants to change. A rerun against the fixed text is not yet done.

Not exercised: label creation and the settings report, a live conversation, a re-run with a changed value, and a re-run against the fixed Section F.

Pass: partly. Section F asked one question per value with a recommended answer, the record holds the five values and the Milestone-issue rule, the block and index line were written; the re-run kept no values until the fix above. Lessons: rerun the re-run with the fixed Section F.

### 2026-11-01, commit 7437f33 (base), dev-skills 0.26.0 (base)

Setup: the scratch repo of the README, in a temporary directory. The Implementer of #422 followed `SKILL.md` and its seeds by hand on its branch: a fresh headless session on the checkout's plugin was refused by the sandbox's permission classifier, so this run is a hand-driven read-through of the skill, not a fresh-runtime run. It does not show that a model, given only the skill text, asks and writes the same way; rerun it as a fresh session when one can be started.

Conversation (user answers, in the order Section F asks):

- Irreversible actions agents may take (recommended: none): "delete test data that agents generate while implementing".
- Actions that need your approval (recommended: none): "delete production or customer data".
- Budget (recommended: none): "at most 20 dollars of API usage a month".
- Check-in interval (recommended: 1 hour): accepted.
- Milestone label form (recommended: `milestone-<n>`): accepted.

(Sections A to E: GitHub accepted, default labels, no agent-only labels, single-context, no own rules, no Releases.)

File written: `docs/agents/boundaries.md`, from the `boundaries.md` seed:

```md
# Boundary record

What the user has agreed agents may do on their own in this repo, which actions are the user's to decide, and the limits agents work within. Skills will read this record instead of a fixed list.

- **Irreversible actions agents may take**: delete test data that agents generate while implementing.
- **Actions that need the user's approval**: delete production or customer data.
- **Budget**: at most 20 dollars of API usage a month.
- **Check-in interval**: 1 hour (how often a running thread checks in with the user).
- **Milestone label form**: `milestone-<n>`. An issue belongs to a Milestone when it carries that Milestone's label, and the Milestone issue carries the same label. Skills read the form from here and never hard-code it.

## Milestone issues

A Milestone issue may name extra allowed or forbidden actions for its own issues. For an issue that belongs to the Milestone, the Milestone issue wins over this record; for every other issue, this record applies as written.
```

Also written: the issue-tracker, triage-label and domain docs, `REVIEW.md`, `CLAUDE.md` with a `## Agent skills` block that has `### Boundaries` ("Agents may delete test data they generate; deleting production or customer data needs the user's approval; budget 20 dollars of API usage a month; check-in every hour; Milestone label `milestone-<n>`. See `docs/agents/boundaries.md`."), and `docs/index.md` with a line for the record.

Re-run: a fresh draft from the seed differs from the written record in exactly three lines (the three placeholders the user filled); the diff showed those three as kept, so a re-run changes nothing ("no change"). This was a hand reading, not a literal draft-and-diff; the entry above shows the literal diff reverting the three values before the Section F fix.

Not exercised: label creation and the GitHub settings report (no reachable remote), a re-run with a changed value, an existing record the user edits by hand, and a fresh-runtime session.

Pass: partly. The text of Section F, the seed and the written file agree; the fresh-runtime asking behaviour is unchecked. Lessons: rerun as a fresh session.
