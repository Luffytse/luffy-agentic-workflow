# Patches to Upstream text

Everything under `upstream-skills/` is copied from Matt Pocock's `mattpocock/skills` ("Upstream", MIT; see `LICENSE-mattpocock-skills`). This file lists every change we made to that text, so an Upstream update can be merged by hand: take Upstream's new text, then re-apply each Patch below.

## Base

- Upstream repo: https://github.com/mattpocock/skills
- Upstream commit: `a496f55` ("implement-spec: a fresh implementer subagent per ticket (#1342)", 2026-10-29)
- Upstream plugin: `mattpocock-skills` version `1.3.2`
- Upstream layout: skills sit in `skills/engineering/` and `skills/productivity/`; here they are flat in `upstream-skills/<name>/`.
- Kept: 23 skills (ADR 0001). Dropped, not copied: `teach`, `to-questionnaire`, `grill-me`, `wait-what`.
- Copied whole, including each skill's helper files (`agents/openai.yaml`, `scripts/`, other `.md`). Not copied: Upstream's `in-progress`, `misc` and `deprecated` skills, and its `README.md`, `CHANGELOG.md` and changesets.
- The copy in luffydev's `.claude/skills/` was Upstream `5beb35b`, 10 days behind; we copied from `a496f55` instead. That copy's one local edit (at most 3 questions per round in `grilling`) is not carried over; it is a separate Patch for a later ticket.

## How to merge an Upstream update

1. Diff Upstream's skill folder against `upstream-skills/<name>/` to see what is new.
2. Take Upstream's text, then re-apply the Patches listed under that skill below.
3. Update the commit and version under Base.

## Patch 1: every skill is model-invoked (all kept skills)

Why: project threads have no slash commands, and a skill with `disable-model-invocation: true` can never be started by an agent (ADR 0001).

What: delete the `disable-model-invocation: true` line from the frontmatter. Upstream sets it on these 12 of the 23 kept skills, all changed:

- `ask-matt`
- `grill-with-docs`
- `handoff`
- `implement`
- `implement-spec`
- `improve-codebase-architecture`
- `retro`
- `setup-matt-pocock-skills`
- `to-spec`
- `to-tickets`
- `triage`
- `wayfinder`

The other 11 (`grilling`, `domain-modeling`, `research`, `prototype`, `tdd`, `code-review`, `pr`, `diagnosing-bugs`, `codebase-design`, `wizard`, `writing-for-agents`) already had no such line. No kept skill sets `user-invocable`, `allowed-tools` or any other key that stops model invocation.

Also, in the same 12 skills, `agents/openai.yaml` (metadata for other coding agents) sets `allow_implicit_invocation: false`; changed to `true` so those agents can start the skill too.

Not changed: `writing-for-agents/SKILL-MECHANICS.md` mentions `disable-model-invocation` only to explain the setting. It stays as written.

Open point: the 12 skills above have human-facing one-line descriptions with the trigger lists stripped (Upstream's rule for user-invoked skills). They are now model-invoked but their descriptions do not say when to fire. Rewriting them is not part of this Patch.

## Patch 2: trim the dropped skills out of `ask-matt` (`ask-matt/SKILL.md`)

Why: `ask-matt` routes to skills in this plugin; it must not name skills we dropped (ADR 0001).

What:

- In the `grill-with-docs` entry of the main flow, the "No working directory? Use `/grill-me`" aside now says to use `/grilling` instead and describes `grill-with-docs` as the same primitive plus a paper trail.
- Standalone section: deleted the `/grill-me`, `/to-questionnaire`, `/wait-what` and `/teach` bullets.
- Standalone `/grilling` bullet: "`/grill-me` and `/grill-with-docs` are the two named ways in" became "`/grill-with-docs` is the named way in when there is a repo", and "Reach for it directly only when you want the interview with no wrapper around it" became "Reach for it directly when there is no working directory, or when you want the interview with no wrapper around it".

No other kept skill mentions a dropped skill (checked with grep for `teach`, `to-questionnaire`, `grill-me`, `wait-what`), so no other edit was needed.

## Patch 3: Evidence and one-way doors (`pr/SKILL.md`)

Why: ADR 0004 makes Evidence a required part of every pull request and a one-way door a reason for a human to merge.

What. In the template:

- Under `## Evidence`, replace the two lines `- **Before:** <screenshot/output/failing test run>` and `  **After:** <screenshot/output/passing test run>` with:

  ```text
  - **Tests:** <the exact test that fails before and passes after, or what was checked instead>
  - **Checks:** <typecheck output, or the repo's checks (lint, validate script)>
  - **Screenshots:** <before and after for anything visual, or "not visual", or why not captured>

  <a spec's PR: repeat these bullets per ticket, under the ticket's number; else delete this line>
  ```

- Under `## Merge Danger`, replace `**Door:** <one-way or two-way>` with `**Door:** <one-way or two-way; a spec's PR: one-way (#a, #b) if any ticket is>`, and replace `<optional: description>` with `<if one-way: one line on what a revert would not undo; else delete this line>`.

In `### Evidence`:

- Replace "Concrete evidence that the change works. Show a before and after." with "Concrete evidence that the change works: what failed before now passes."
- Replace "Screenshots are S-tier - when the environment is set up for it and the change is visual." with "Screenshots are S-tier - for anything visual. If the environment can't take them, say so."
- In the A-tier paragraph, replace "Show the exact test that now fails and passes, using pseudocode." with "Show the exact test that fails before and passes after, using pseudocode. Include the typecheck output, or the output of the repo's checks (a lint or validate script)."
- After that paragraph, add these two paragraphs:

  > When something can't be shown (a docs-only change has no tests), say what was checked instead; never leave an Evidence line empty.
  >
  > A PR that collects several tickets (a spec's PR) carries each ticket's evidence into its body.

In `### Merge Danger`, after Upstream's door paragraph (ending "...are one-way doors.") and before "The blast radius is...", add these two paragraphs:

> Decide with one test: would reverting the PR's commits undo everything the change did, including anything outside git? If not, it is a one-way door. For example: a data migration, deleted data, a public interface others depend on, a message sent outside the project, a published release. Mark it plainly as `**Door:** one-way`, with one line on what a revert would not undo, so a reader or merging agent can find it. A one-way door is not self-merged.
>
> A PR that collects several tickets (a spec's PR) carries each ticket's Door call into its body, and is one-way if any ticket's Door is, naming those tickets.

Summary section: unchanged.

## Patch 4: docs are found through the docs index (ADR 0006)

Why: the docs Upstream's skills write keep growing, and most skills read the whole glossary or list `docs/adr/` to find the few that matter. Each repo gets one `docs/index.md`; writing skills keep it current and reading skills start there (ADR 0006).

New file (ours, not Upstream text): `domain-modeling/DOCS-INDEX.md`, the index format, what is and is not listed, how agents read it, and the update rule (including creating a missing `docs/index.md` with a line for every doc of the listed kinds that already exists).

Shared reader phrase, used by every reader below: "start at `docs/index.md` and open only the docs that fit (with no index, fall back to `GLOSSARY.md` or `GLOSSARY-MAP.md`, and `docs/adr/`)". Where the old text read the glossary or ADRs, that sentence is replaced by the phrase; otherwise one line with it is added where the skill explores the repo.

Changed Upstream files, by skill:

- `code-review/SKILL.md` (step 3): the standards-sources search starts with the shared phrase, then searches for every file that documents how code should be written, including `CLAUDE.md`/`AGENTS.md`, which the index does not list.
- `diagnosing-bugs/SKILL.md`: "read `GLOSSARY.md` ... check ADRs" replaced by the shared phrase.
- `domain-modeling/GLOSSARY-FORMAT.md`: new section "Single glossary, or one page per Area"; the map example links `docs/glossary/<area>.md` (with a note for Upstream's `src/<context>/` links); a map into `src/` is multi-context and a map at `docs/glossary/` lists Area pages; the "which context" question becomes "which Area (or, in a multi-context repo, which context)".
- `domain-modeling/SKILL.md`: "reading the glossary" instead of "reading `GLOSSARY.md`"; a third "File structure" tree for the per-Area split; multi-context now means a root `GLOSSARY-MAP.md` that points into `src/`; a root `GLOSSARY.md` is created only if neither it nor a map exists; frontmatter description says "the glossary (GLOSSARY.md, GLOSSARY-MAP.md or its pages)"; new sections "Splitting the glossary" (only from a single root `GLOSSARY.md` over about 10 KB, `git mv` into the first Area's page at `docs/glossary/<area>.md`, `GLOSSARY-MAP.md` at the root, index line swapped, `docs/index.md` created if missing, one `docs/adr/` kept; with any existing map a term goes to the page the map points to) and "Keeping the docs index current" (create a doc, or edit one whose subject changed: update its index line in the same commit); "challenge" and "update inline" sections say "the glossary" and "the Area page `GLOSSARY-MAP.md` points to".
- `grill-with-docs/SKILL.md`: adds the shared phrase and says glossary and ADR edits follow `domain-modeling`, including updating `docs/index.md` in the same commit.
- `implement-spec/SKILL.md` (step 1): adds the shared phrase.
- `implement/SKILL.md`: adds the shared phrase (for the ticket) before the `tdd` line.
- `improve-codebase-architecture/SKILL.md`: intro, vocabulary rule and grilling-loop bullets say "the glossary (`GLOSSARY.md`, or the Area page `GLOSSARY-MAP.md` points to)" and create a root `GLOSSARY.md` only if neither exists; the explore step uses the shared phrase; a new bullet says to update `docs/index.md` in the same commit after writing any doc.
- `pr/SKILL.md`: "domain language from `GLOSSARY.md`" replaced by the shared phrase.
- `research/SKILL.md`: new step 4, add the note's line to `docs/index.md` if it is committed to a branch that will merge; no line for a throwaway branch.
- `retro/SKILL.md` ("Files" list): new "Index" bullet, update `docs/index.md` in the same commit when adding or editing `REVIEW.md`, `CODING_STANDARDS.md` or any other doc.
- `setup-matt-pocock-skills/SKILL.md`: the "Domain docs" summary mentions `docs/index.md`; exploring also looks for `docs/index.md` and the docs it should list; Section C notes the later glossary split; the draft includes the index; a final write step creates `docs/index.md` if missing, or updates it, listing every `docs/agents/` file written and every doc found.
- `setup-matt-pocock-skills/domain.md` (becomes `docs/agents/domain.md`): "Before exploring" starts at `docs/index.md`, with the old glossary and ADR reads as the fallback; "Single-context repo" is relabelled "Small repo" and its tree adds `docs/index.md`; a new tree for the per-Area split; multi-context means a map that points into `src/`; "use the term as defined in the glossary"; one sentence says any skill that writes a doc adds or fixes its line in `docs/index.md` in the same commit (no link, since the rule file is not reachable from a consumer repo).
- `tdd/SKILL.md`: "read `GLOSSARY.md` (if it exists) ... respect ADRs" replaced by the shared phrase.
- `to-spec/SKILL.md` (step 1): adds the shared phrase before the glossary-vocabulary sentence.
- `to-tickets/SKILL.md`: adds the shared phrase before the glossary-vocabulary sentence.
- `triage/OUT-OF-SCOPE.md`: new step 7 in the write flow (new file gets a line, an edited file's line is fixed only if its subject changed); deleting an `.out-of-scope/` file also removes its index line.
- `triage/SKILL.md`: step 1 explores with "Explore the codebase: start at `docs/index.md` (...), open only the docs that fit, and respect ADRs in the area"; the grill step says to update "the glossary (`GLOSSARY.md`, or the Area page `GLOSSARY-MAP.md` points to) and ADRs inline" and that any doc written, including `.out-of-scope/` files, gets its index line in the same commit.
- `wayfinder/SKILL.md`: adds the shared phrase before "Plan, don't do".

Also in this Patch:

- `.claude-plugin/plugin.json`: version 0.1.2 to 0.2.0.
- `scripts/check-plugin.sh` check 7: `domain-modeling/DOCS-INDEX.md` exists; each writer file mentions `DOCS-INDEX.md` (`SKILL.md` of `domain-modeling`, `improve-codebase-architecture`, `triage`, `retro`, `setup-matt-pocock-skills`, `research` and `grill-with-docs`, plus `triage/OUT-OF-SCOPE.md`); each of the 12 readers' `SKILL.md` contains "start at `docs/index.md`" (case-insensitive) and `GLOSSARY-MAP.md` (readers: `tdd`, `diagnosing-bugs`, `improve-codebase-architecture`, `pr`, `to-spec`, `to-tickets`, `triage`, `grill-with-docs`, `wayfinder`, `implement`, `implement-spec`, `code-review`); `domain.md` mentions `docs/index.md`.

Not changed: the drift check in `code-review` (ADR 0006's last bullet) is a separate ticket.

## Vendor model names in Upstream text

None in the kept skills at the Base commit, so no Patch was needed for ADR 0002 (checked for ticket #4: grep for `haiku`, `sonnet`, `opus`, `claude-`, `gpt-`, `gemini` over `upstream-skills/`). Some kept skills start subagents (for example `grilling`, `wayfinder`, `code-review`, `implement-spec`), but none picks a model for them. Spec #1 adds tiers in later tickets (the `code-review` Finders and Verifiers, the `implement` and `implement-spec` Implementers, and a tier on each ticket from `to-tickets`); each of those edits gets its own Patch here.

`scripts/check-plugin.sh` now runs the vendor-name grep over `upstream-skills/` too, so an Upstream merge that brings in a model name fails the check and must be patched to a tier.
