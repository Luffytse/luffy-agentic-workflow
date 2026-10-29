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

## Vendor model names in Upstream text

None in the kept skills at the Base commit, so no Patch was needed for ADR 0002 (checked for ticket #4: grep for `haiku`, `sonnet`, `opus`, `claude-`, `gpt-`, `gemini` over `upstream-skills/`). Some kept skills start subagents (for example `grilling`, `wayfinder`, `code-review`, `implement-spec`), but none picks a model for them. Spec #1 adds tiers in later tickets (the `code-review` Finders and Verifiers, the `implement` and `implement-spec` Implementers, and a tier on each ticket from `to-tickets`); each of those edits gets its own Patch here.

`scripts/check-plugin.sh` now runs the vendor-name grep over `upstream-skills/` too, so an Upstream merge that brings in a model name fails the check and must be patched to a tier.
