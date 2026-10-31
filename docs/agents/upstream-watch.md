# Upstream watch

A job that runs every 2 weeks, reads the new commits of Upstream (`mattpocock/skills`, the repo the `dev-skills` skills began as, see [ADR 0001](../adr/0001-dev-skills-is-one-plugin-forked-from-matt-pocock.md)) and files one `needs-triage` issue listing what is worth taking by hand. The skills are ours now, so nothing from Upstream is merged or applied automatically: triage decides each item like any other request.

This prompt is repo-specific, so it lives here and never in plugin skill text. Run it by hand by starting a session in this repo and saying: "Follow `docs/agents/upstream-watch.md` on main."

## Access the job needs

Every session the job starts is scoped to this repo (`Luffytse/luffy-dev-skills`) and needs read access to the public Upstream repo. A cloud session reaches only the repos added to it, and each scheduled firing starts a fresh session, so a repo added by hand to one session is gone in the next. The job therefore starts by calling `add_repo` for `mattpocock/skills` with read access in its own session (the prompt in Schedule says so). To grant it once for all later sessions of the project, the user can instead add `mattpocock/skills` in Project settings, or answer yes when a session calls `add_repo` with `save_to_project: true` (the user is asked to allow that call). Without access, `list_commits` on Upstream is refused with "repository is not configured for this session". If that happens, stop and say so in a report instead of an issue: do not guess commits. The job writes only to this repo: an issue and one small branch.

## The prompt

First call `add_repo` for `mattpocock/skills` with read access in this session. You are the Upstream watch for this repo. Read `CLAUDE.md`, `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md` first. Do not change any skill, ADR or other file except the one README line in step 6.

1. **Read the last commit looked at.** In `plugins/dev-skills/README.md` on main, find the line `Last Upstream commit looked at:`; its first backticked value is the SHA, call it `LAST`. If an open pull request titled `Upstream watch: ...` exists, read the README from its branch instead and use that SHA (an earlier run's record is not merged yet; without this the same commits would be listed twice).
2. **Read Upstream's latest.** With the GitHub tools (`list_commits` on `mattpocock/skills`, default branch; page until `LAST` is reached) list every commit after `LAST`, oldest first, and note the newest one, `LATEST`. If `LAST` is not found in the history (Upstream rewrote it), say so in the issue and list the commits since the date on the README line instead. If there are no new commits, stop: file nothing and say so.
3. **Look at each commit.** For each commit use `get_commit` (file list first; `full_patch` only for a commit that touches a skill) and, when the diff alone does not say, `get_file_contents` at that commit. Judge it against this repo: which `dev-skills` skills exist (`plugins/dev-skills/skills/`), and the decisions in `docs/adr/` (ADR 0001 lists the skills we kept and dropped; ADR 0002 says skills name model tiers, never models). Skip a commit that only touches a skill we dropped (`teach`, `to-questionnaire`, `grill-me`, `wait-what`) or a skill Upstream added that we have no use for, repo housekeeping (CI, README, release notes, formatting, typo fixes in text we have since rewritten), and anything our own text already does better. Take a commit worth reading when it fixes a real fault in a skill we keep, or adds an idea that a skill we keep lacks.
4. **File ONE issue** in `Luffytse/luffy-dev-skills`, labelled `needs-triage` (see `triage-labels.md`; no other label, no release label, no parent), titled `Upstream watch: <LAST short SHA>..<LATEST short SHA> (<date>)`. Body:
   - the range as a link (`https://github.com/mattpocock/skills/compare/<LAST>...<LATEST>`) and the number of commits looked at;
   - `## Worth taking by hand`: one bullet per commit, `<short SHA> <subject> (<link>): <one line on why it is worth taking and which of our skills it would change>`. Or the line `None of these commits are worth taking.` followed by one line per group saying why they were skipped;
   - `## Recorded`: `Last Upstream commit looked at is now <LATEST short SHA>`, and the link to the pull request (added in step 6). The issue is filed first and the link added afterwards (for the comment variant, by a second comment or an edit).
   Search open issues for an `Upstream watch:` issue first; if one is still open and unanswered (no comment from a person since it was filed), comment on it instead of filing a second; the comment carries the commit range, the bullets and the pull request link that the issue body would. File a new issue only when none is open.
5. **Apply nothing.** Do not copy text from Upstream and do not open a pull request that applies a commit's change (step 6's record PR is the only one). Taking an idea is a normal ticket: triage turns an accepted item into a `ready-for-agent` issue, and a change of skill text then goes through the usual build and review. Take care when you write a bullet that it describes an idea, not text to paste: the licence notice (`LICENSE-mattpocock-skills`) covers copied text.
6. **Record the new commit.** Create a branch `upstream-watch-<LATEST short SHA>` off main, change only the README line to `Last Upstream commit looked at: ` followed by `LATEST` short SHA, its subject in quotes and its date (same shape as now), and open a pull request titled `Upstream watch: <LATEST short SHA>` whose body links the issue. Do not merge it, and do not bump any version. Add the PR link to the issue (step 4's `## Recorded`).
7. **Report** the issue and pull request links, or that there were no new commits.

## Why the pull request records the commit

Two ways to record the new last-looked-at commit were open: the issue tells triage to update the README line, or the job opens a small pull request. This repo uses the pull request, because:

- Nothing then depends on a person remembering a chore. An issue instruction could be forgotten, or triage might close the issue as "none worth taking" without touching the README, and the next run would list the same commits again.
- The record is the commit range that was looked at, not the commits that were taken. It is true as soon as the job has looked, so it should not wait for triage to decide the items.
- It changes one line of one README and no skill text, so it needs no version, as ordinary changes under `plugins/` carry none ([ADR 0008](../adr/0008-plugin-versions-change-only-at-a-release.md)), and the job only opens it: the user merges it.
- Step 1 reads an open watch pull request first, so an unmerged one never causes a repeat.

The issue still names the range, so it is the readable record, and the README line is the machine-read one.

## Schedule

The schedule is a scheduled task that starts a fresh session on each firing (the `claude-code-remote` tools: `create_trigger`, `update_trigger`, `delete_trigger`, `fire_trigger`, `list_triggers`). It is created only after the user agrees, since it runs outside this repo.

- **Create**: `create_trigger` with `name` "Upstream watch", `create_new_session_on_fire` true, `cron_expression` `23 14 1,15 * *` (14:23 UTC on the 1st and 15th of each month; cron cannot say "every 14 days", and the gap of 13 to 17 days does no harm because each run starts from the recorded commit), `initiation` `human_request`, and `prompt` "In Luffytse/luffy-dev-skills, follow docs/agents/upstream-watch.md on main." (the doc's prompt starts with the `add_repo` call) Each fired session needs this repo and, read-only, `mattpocock/skills` (see Access above). If the result warns that the scheduled task stores no connectors, read the warning and relay it and its remedy to the user; do not report the task as simply created.
- **Run now**: `fire_trigger` with the trigger id, or follow the prompt by hand as above.
- **Change the time**: `update_trigger` with a new `cron_expression`. Change the job itself by editing this doc; the prompt reads it fresh on each firing.
- **Pause**: `update_trigger` with `enabled` false (`true` resumes). **Stop for good**: `delete_trigger`. Find the id with `list_triggers`.
