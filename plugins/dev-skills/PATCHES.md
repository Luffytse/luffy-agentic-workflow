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

## Vendor model names in Upstream text

None found in the kept skills (grep for haiku, sonnet, opus, claude-, gpt-). Nothing to patch for ADR 0002 yet; the model-tier Patches come with later tickets.
