# Patches to Upstream text

Everything under `upstream-skills/` is copied from Matt Pocock's `mattpocock/skills` ("Upstream", MIT; see `LICENSE-mattpocock-skills`). This file lists every change we made to that text, so an Upstream update can be merged by hand: take Upstream's new text, then re-apply each Patch below.

## Base

- Upstream repo: https://github.com/mattpocock/skills
- Upstream commit: `a496f55` ("implement-spec: a fresh implementer subagent per ticket (#1342)", 2026-10-29)
- Upstream plugin: `mattpocock-skills` version `1.3.2`
- Upstream layout: skills sit in `skills/engineering/` and `skills/productivity/`; here they are flat in `upstream-skills/<name>/`.
- Kept: 22 skills (ADR 0001). Dropped, not copied: `teach`, `to-questionnaire`, `grill-me`, `wait-what`. Upstream's `setup-matt-pocock-skills` was copied at first and later moved out as our own `setup-dev-skills` (Patch 22).
- Copied whole, including each skill's helper files (`agents/openai.yaml`, `scripts/`, other `.md`). Not copied: Upstream's `in-progress`, `misc` and `deprecated` skills, and its `README.md`, `CHANGELOG.md` and changesets.
- The copy in luffydev's `.claude/skills/` was Upstream `5beb35b`, 10 days behind; we copied from `a496f55` instead. That copy's one local edit (at most 3 questions per round in `grilling`) was not in the copy we took; Patch 23 applies it.

## How to merge an Upstream update

1. Diff Upstream's skill folder against `upstream-skills/<name>/` to see what is new.
2. Take Upstream's text, then re-apply the Patches listed under that skill below.
3. Update the commit and version under Base.

## Patch 1: every skill is model-invoked (all kept skills)

Why: project threads have no slash commands, and a skill with `disable-model-invocation: true` can never be started by an agent (ADR 0001).

What: delete the `disable-model-invocation: true` line from the frontmatter. Upstream sets it on these 12 of the 23 skills first kept (11 of the 22 kept now: `setup-matt-pocock-skills` left `upstream-skills/` in Patch 22), all changed:

- `ask-matt`
- `grill-with-docs`
- `handoff`
- `implement`
- `implement-spec`
- `improve-codebase-architecture`
- `retro`
- `setup-matt-pocock-skills` (removed in Patch 22)
- `to-spec`
- `to-tickets`
- `triage`
- `wayfinder`

The other 11 (`grilling`, `domain-modeling`, `research`, `prototype`, `tdd`, `code-review`, `pr`, `diagnosing-bugs`, `codebase-design`, `wizard`, `writing-for-agents`) already had no such line. No kept skill sets `user-invocable`, `allowed-tools` or any other key that stops model invocation.

Also, in the same 12 skills, `agents/openai.yaml` (metadata for other coding agents) sets `allow_implicit_invocation: false`; changed to `true` so those agents can start the skill too.

Not changed: `writing-for-agents/SKILL-MECHANICS.md` mentions `disable-model-invocation` only to explain the setting. It stays as written.

Open point: the 12 skills above have human-facing one-line descriptions with the trigger lists stripped (Upstream's rule for user-invoked skills). They are now model-invoked but their descriptions do not say when to fire. Rewriting them is not part of this Patch. `implement` (Patch 8) and `implement-spec` (Patch 11) now have agent-facing descriptions that say when to use them; the other 10 still have Upstream's. Patch 21 later rewrites 9 of those 10 (`setup-matt-pocock-skills` is left out, as ticket #77 replaces it) and `grilling`'s.

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

- `code-review/SKILL.md` (step 3; Patch 5 later rewrote the skill and carries this into its step 2): the standards-sources search starts with the shared phrase, then searches for every file that documents how code should be written, including `CLAUDE.md`/`AGENTS.md`, which the index does not list.
- `diagnosing-bugs/SKILL.md`: "read `GLOSSARY.md` ... check ADRs" replaced by the shared phrase.
- `domain-modeling/GLOSSARY-FORMAT.md`: new section "Single glossary, or one page per Area"; the map example links `docs/glossary/<area>.md` (with a note for Upstream's `src/<context>/` links); a map into `src/` is multi-context and a map at `docs/glossary/` lists Area pages; the "which context" question becomes "which Area (or, in a multi-context repo, which context)".
- `domain-modeling/SKILL.md`: "reading the glossary" instead of "reading `GLOSSARY.md`"; a third "File structure" tree for the per-Area split; multi-context now means a root `GLOSSARY-MAP.md` that points into `src/`; a root `GLOSSARY.md` is created only if neither it nor a map exists; frontmatter description says "the glossary (GLOSSARY.md, GLOSSARY-MAP.md or its pages)"; new sections "Splitting the glossary" (only from a single root `GLOSSARY.md` over about 10 KB, `git mv` into the first Area's page at `docs/glossary/<area>.md`, `GLOSSARY-MAP.md` at the root, index line swapped, `docs/index.md` created if missing, one `docs/adr/` kept; with any existing map a term goes to the page the map points to) and "Keeping the docs index current" (create a doc, or edit one whose subject changed: update its index line in the same commit); "challenge" and "update inline" sections say "the glossary" and "the Area page `GLOSSARY-MAP.md` points to".
- `grill-with-docs/SKILL.md`: adds the shared phrase and says glossary and ADR edits follow `domain-modeling`, including updating `docs/index.md` in the same commit.
- `implement-spec/SKILL.md` (step 1): adds the shared phrase (Patch 11 later rewrote the skill; the line is now in its step 1, "Read the spec and its tickets").
- `implement/SKILL.md`: adds the shared phrase (for the ticket) before the `tdd` line (Patch 8 later rewrote the skill; the line is now in its step 1).
- `improve-codebase-architecture/SKILL.md`: intro, vocabulary rule and grilling-loop bullets say "the glossary (`GLOSSARY.md`, or the Area page `GLOSSARY-MAP.md` points to)" and create a root `GLOSSARY.md` only if neither exists; the explore step uses the shared phrase; a new bullet says to update `docs/index.md` in the same commit after writing any doc.
- `pr/SKILL.md`: "domain language from `GLOSSARY.md`" replaced by the shared phrase.
- `research/SKILL.md`: new step 4, add the note's line to `docs/index.md` if it is committed to a branch that will merge; no line for a throwaway branch.
- `retro/SKILL.md` ("Files" list): new "Index" bullet, update `docs/index.md` in the same commit when adding or editing `REVIEW.md`, `CODING_STANDARDS.md` or any other doc.
- `setup-matt-pocock-skills/SKILL.md` (removed in Patch 22; the work carried over to `skills/setup-dev-skills/SKILL.md`): the "Domain docs" summary mentions `docs/index.md`; exploring also looks for `docs/index.md` and the docs it should list; the later glossary split is noted in the `domain.md` seed; the draft includes the index; a final write step creates `docs/index.md` if missing, or updates it, listing every `docs/agents/` file written and every doc found.
- `setup-matt-pocock-skills/domain.md` (removed in Patch 22; carried over to `skills/setup-dev-skills/domain.md`; becomes `docs/agents/domain.md`): "Before exploring" starts at `docs/index.md`, with the old glossary and ADR reads as the fallback; "Single-context repo" is relabelled "Small repo" and its tree adds `docs/index.md`; a new tree for the per-Area split; multi-context means a map that points into `src/`; "use the term as defined in the glossary"; one sentence says any skill that writes a doc adds or fixes its line in `docs/index.md` in the same commit (no link, since the rule file is not reachable from a consumer repo).
- `tdd/SKILL.md`: "read `GLOSSARY.md` (if it exists) ... respect ADRs" replaced by the shared phrase.
- `to-spec/SKILL.md` (step 1): adds the shared phrase before the glossary-vocabulary sentence.
- `to-tickets/SKILL.md`: adds the shared phrase before the glossary-vocabulary sentence.
- `triage/OUT-OF-SCOPE.md`: new step 7 in the write flow (new file gets a line, an edited file's line is fixed only if its subject changed); deleting an `.out-of-scope/` file also removes its index line.
- `triage/SKILL.md`: step 1 explores with "Explore the codebase: start at `docs/index.md` (...), open only the docs that fit, and respect ADRs in the area"; the grill step says to update "the glossary (`GLOSSARY.md`, or the Area page `GLOSSARY-MAP.md` points to) and ADRs inline" and that any doc written, including `.out-of-scope/` files, gets its index line in the same commit.
- `wayfinder/SKILL.md`: adds the shared phrase before "Plan, don't do".

Also in this Patch:

- `.claude-plugin/plugin.json`: version 0.1.2 to 0.2.0.
- `scripts/check-plugin.sh` check 7: `domain-modeling/DOCS-INDEX.md` exists; each writer file mentions `DOCS-INDEX.md` (`SKILL.md` of `domain-modeling`, `improve-codebase-architecture`, `triage`, `retro`, `setup-matt-pocock-skills` (removed in Patch 22; now `setup-dev-skills`), `research` and `grill-with-docs`, plus `triage/OUT-OF-SCOPE.md`); each of the 12 readers' `SKILL.md` contains "start at `docs/index.md`" (case-insensitive) and `GLOSSARY-MAP.md` (readers: `tdd`, `diagnosing-bugs`, `improve-codebase-architecture`, `pr`, `to-spec`, `to-tickets`, `triage`, `grill-with-docs`, `wayfinder`, `implement`, `implement-spec`, `code-review`); `domain.md` mentions `docs/index.md`.

Not changed here: the drift check in `code-review` (ADR 0006's last bullet) came with Patch 5.

## Patch 5: `code-review` runs Find, Verify and Rank in Rounds (`code-review/`)

Why: ADR 0003. Upstream's two-axis review reports raw Findings side by side with no false-positive check, and runs once. We want parallel Finders, a Verifier that makes the final call on each Finding, ranking by Severity, Review depths, and pull-request Rounds that stop once nothing Important is open. ADR 0006 adds the docs index drift check, and ADR 0004 the Ticket check.

What:

- `SKILL.md` rewritten whole: new model-facing description; two entry points (a pull request reviewed in Rounds, or one Review over a diff since a fixed point, which also serves the Ticket check); a rule that the Review runs in the top-level session (a subagent cannot start the Finders and Verifiers; if no subagents can be started, stop and tell the user); the depth and tier table; process steps Pin the diff, Find the sources, Find, Verify, Rank and report. Upstream text kept, with these changes:
  - The issue-tracker line: unchanged.
  - Step 1 (pin the fixed point): reworded into "Pin the diff", with the Round 1-2 and Round 3-5 diffs added; the `git rev-parse` and non-empty-diff fail-early check kept in substance.
  - Step 2 (spec source): item 1 also reads the pull request body; item 4 says "the spec Finder is skipped and the Review says" for "the **Spec** sub-agent will skip and report".
  - Step 3 (standards sources, as Patch 4 left it): split over step 2 of the rewrite. Patch 4's shared reader phrase now opens step 2 for both spec and standards sources ("Start at `docs/index.md` and open only the docs whose line fits the change (with no index, fall back to ...)"); the standards line keeps "search the repo for every file that documents how code should be written, including `CLAUDE.md`/`AGENTS.md`, which the index does not list" and that `CODING_STANDARDS.md` and `CONTRIBUTING.md` must be on the list "when they exist"; `REVIEW.md` and the default meaning of Important added. The smell baseline moved to `FINDERS.md` (below).
  - Step 4 (spawn both sub-agents): replaced by the Find step and the briefs in `FINDERS.md` (below).
  - Step 5 (aggregate): dropped, with "do not merge or rerank" and the side-by-side `## Standards` / `## Spec` report, since Findings are now verified and ranked together, each tagged with its Finder.
  - "Why two axes" became "Why the Finders stay separate": the two bullets kept with `→` replaced by `:` and "Standards pass, Spec fail" lowercased to "standards pass, spec fail" (likewise the second); the closing sentence "Reporting them separately stops one axis from masking the other" replaced by two sentences on separate contexts and Findings meeting only after Verify.
- New `FINDERS.md`: the Finder briefs (standards, spec, two adversarial with an angle list, Deep's security Finder) and the one fixed Finding format. Upstream text moved here from `SKILL.md`, with these changes:
  - Smell baseline (step 3): moved word for word except "the Standards axis always carries" became "the standards Finder always carries".
  - Standards brief (step 4): "Report, per file/hunk where relevant, (a)" became "Report (a)"; "(file + the rule); and (b)" became "(file and rule); (b)"; added "(c) any docs index drift"; "Distinguish hard violations from judgement calls: documented-standard breaches can be hard, but baseline smells" became "Documented-standard breaches can be hard; baseline smells"; "Skip anything tooling enforces" moved into the instructions shared by every Finder; "Under 400 words" dropped (the Finding format bounds the output).
  - Spec brief (step 4): added "(d) anything that contradicts an ADR or the glossary"; "Quote the spec line for each finding" became "Quote the spec line, or the ADR or glossary line, as the evidence for each Finding"; "Under 400 words" dropped.
  - Each prompt's "should include" list (diff command, commit list, sources) became one shared list at the top of the file.
  - Added: the docs index drift check, the adversarial and security Finders, the Finding format.
- New `VERIFY.md`: the Verifier brief (four calls with one line of reasoning each, re-checking open Importants) and Deep's three stances with the 2-of-3 rule and the cautious tie-break.
- New `ROUNDS.md`: the Rank rules, the Round comment format (a `<!-- code-review kind=round ... -->` marker line and a Findings table with ids and status), the Round loop and stop rule, the 5-Round cap, filing Pre-existing Findings as one `needs-triage` issue per Bug class, and the Ticket-check record.
- `agents/openai.yaml`: `short_description` now "Find, verify and rank review Findings, in Rounds".
- `.claude-plugin/plugin.json`: version 0.3.0 to 0.4.0.

Our own, not Upstream: `evals/code-review/` (the planted-bugs fixture, `EXPECTED.md`, `RESULTS.md`) and the code-review check in `scripts/check-plugin.sh`.

Merging an Upstream update: Upstream's `code-review/SKILL.md` is replaced whole, so diff Upstream's old and new text and carry any change over by hand: smell-baseline edits go into `FINDERS.md`, spec- and standards-source lookup edits into `SKILL.md` step 2.

## Patch 6: `retro` turns repeated Bug classes into checks (`retro/`)

Why: ADR 0003. A Bug class that comes up more than once in a pull request should become a deterministic check or a `REVIEW.md` line, so later Reviews do not have to catch it again. Upstream's `retro` never reads Round comments.

What:

- `retro/SKILL.md`: new step 3, "If the session reviewed or built a pull request with `code-review` Rounds (or the user names one), turn its repeated Bug classes into checks: [BUG-CLASSES.md](BUG-CLASSES.md)."; Upstream's steps 3 and 4 become 4 and 5; the new step 5 (step 6 since Patch 16; Upstream's "Present these candidates to the user, in order of severity.") gains the sentence "Report repeated Bug classes as done, with the link to the retro's pull request." Every other line is Upstream's.
- New `retro/BUG-CLASSES.md` (ours, not Upstream): reads every Round and Ticket-check comment of a pull request, merges them into one row per Finding id, groups by Bug class, and for each repeated class repairs an existing guardrail, adds a deterministic check, or adds a `REVIEW.md` Always-check line; the changes go in their own pull request, which a person merges when it touches `REVIEW.md`.
- `scripts/check-plugin.sh`: `retro/BUG-CLASSES.md` joins the `writers` list of check 7; new check 9 (retro-bug-classes: `BUG-CLASSES.md` exists, `retro/SKILL.md` links it, `BUG-CLASSES.md` and `code-review/ROUNDS.md` both contain the `<!-- code-review kind=round` and `<!-- code-review kind=ticket-check` markers, `BUG-CLASSES.md` mentions `REVIEW.md`).
- `.claude-plugin/plugin.json`: version 0.4.0 to 0.5.0.

Merging an Upstream update: carry Upstream's `retro/SKILL.md` changes over by hand and re-apply the step 3 insertion and the step 6 sentence (step 5 before Patch 16).

## Patch 7: `to-tickets` gives each ticket a Model tier; `to-tickets` and `wayfinder` offer `setup-project` (ADR 0004)

Why: ADR 0004. Each ticket's Implementer runs on the tier `to-tickets` gave it, and the project instructions `setup-project` writes must keep up when planning changes what threads need. Upstream has neither.

What:

- `to-tickets/SKILL.md`:
  - Step 3, after the blocking-edges paragraph: new paragraph "Give each ticket a **model tier**, the tier its Implementer runs on: **regular** by default, **premium** for heavy or tricky work (a subtle design call, wide-reaching changes, concurrency, security or money logic). Name the tier, never a vendor's model."
  - Step 4: the per-ticket list gains "**Model tier**: regular or premium, and for premium one line on why" after **Blocked by**; the questions gain "Does each ticket's model tier fit its difficulty?".
  - `<local-ticket-template>`: a "**Model tier:** this ticket's tier as agreed with the user: `regular` or `premium`." line after **Blocked by**.
  - `<issue-template>`: a "**Model tier:** this ticket's tier as agreed with the user: `regular` or `premium`." line at the end of `## What to build`.
  - New step 6, "Offer `setup-project`": once published, if the tickets changed what threads need (a new spec or map to point at, a new repo, a new kind of thread, a new standing rule), offer `setup-project` in one line; run it only after the user says yes; say nothing if nothing changed.
- `wayfinder/SKILL.md`: new section "Offer `setup-project`" at the end (same rule, with "build threads to start" once the way is clear); "Chart the map" step 6 becomes "Offer `setup-project`, then stop: ..."; "Work through the map" gains step 6, "Offer `setup-project`".
- `scripts/check-plugin.sh`: new check 10 (ticket-templates: both `to-tickets` templates carry a `**Model tier:**` line; `to-tickets` and `wayfinder` both name `` `setup-project` ``).
- `.claude-plugin/plugin.json`: version 0.5.0 to 0.6.0.

Merging an Upstream update: carry Upstream's changes to both files over by hand and re-apply the lines above.

## Patch 8: `implement` coordinates one lone Ticket (`implement/`)

Why: ADR 0004. Upstream's `implement` has the session build the work and commit to the current branch itself, with no pull request. A Ticket thread coordinates instead: one Implementer subagent builds test-first and fixes the Findings, the thread checks its evidence, opens the pull request with `pr`, runs the `code-review` Rounds, and merges or brings the pull request to the user. A lone ticket squash-merges into main (ADR 0005).

What:

- `SKILL.md` rewritten whole as eight steps (read the ticket, make the Ticket branch, start one Implementer, check the evidence, open the pull request, review in Rounds, merge or bring it to the user, report), with a new agent-facing description that says when to use it. Upstream lines, and what became of each:
  - "Implement the work described by the user in the spec or tickets.": replaced by the coordinator paragraph; a Spec goes to `implement-spec` (step 1).
  - "If the user passes a ticket reference, fetch it ... state its title before starting. If the reference is ambiguous, ask.": kept in step 1 as "Fetch the ticket from the issue tracker and state its title. If the reference is ambiguous, ask."
  - Patch 4's reader line ("Start at `docs/index.md` and open only the docs that fit the ticket ..."): kept word for word in step 1.
  - "Call the Skill tool with "tdd" where possible, at pre-agreed seams.": moved into the Implementer's brief (step 3) as "build test-first with the `tdd` skill, at seams agreed before the first test".
  - "Run typechecking regularly, single test files regularly, and the full test suite once at the end.": dropped; the Implementer's evidence (step 3) and the thread's check (step 4) cover it.
  - "Once done, call the Skill tool with "code-review" to review the work.": replaced by step 6, which runs `code-review` in Rounds from the thread and sends Findings to the Implementer.
  - "Commit your work to the current branch.": replaced by the pushed Ticket branch from main (step 2), the Implementer committing there (step 3), and the squash-merge (step 7).
  - Added: the issue-tracker line from `implement-spec` and `code-review`; blocking edges; Model tier (regular unless the issue says premium); cheap subagents for trivial jobs such as rerunning tests or the checks (steps 3 and 4); keeping one Implementer by message, or a new one with a handoff, telling the user you did; the fallback when a repo has no checks or no CI; a Review depth in the brief wins; fetching main before each Round and having the Implementer merge it in (never rebasing), so a Round reviews the conflict resolutions; the final "fix" Nits commit on a clean Round 2 to 5; filing Pre-existing Findings as `code-review` says; the self-merge rules of ADR 0004; at merge time, merging main in if the Ticket branch lacks its commits, running one more Round over that merge's conflict resolutions if it had conflicts and the 5-Round cap allows, otherwise bringing the pull request to the user, and rerunning the checks and CI on the final head; the summary squash-merge message; the final report.
- `agents/openai.yaml`: `short_description` now "Coordinate one lone ticket: Implementer, PR, review Rounds, merge".
- `scripts/check-plugin.sh`: new check 11 (implement-coordinator: `implement/SKILL.md` names `` `tdd` ``, `` `pr` `` and `` `code-review` ``, says Implementer, and says squash).
- `.claude-plugin/plugin.json`: version 0.6.0 to 0.7.0.

Merging an Upstream update: Upstream's `implement/SKILL.md` is replaced whole, so diff Upstream's old and new text and carry any change over by hand into the step it maps to above (ticket fetching into step 1, building advice into the Implementer's brief in step 3, review into step 6). Keep Patch 4's reader line and the words check 11 looks for.

## Patch 9: `code-review` applies `REVIEW.md`'s Always check lines (`code-review/`)

Why: issue #23. `retro` (Patch 6) turns repeated judgement Bug classes into Always check lines in `REVIEW.md`, but Patch 5's briefs only told Finders and Verifiers to apply `REVIEW.md`'s skip list, so nothing made a Review check those lines. The check goes to the standards Finder because it runs at every depth, a Ticket check included; the other Finders still get `REVIEW.md`.

What:

- `FINDERS.md`: the standards Finder is also given the new `REVIEW.md` Always check section when `REVIEW.md` has at least one Always check line (else (d) is dropped from the brief); its brief, the Upstream standards prompt as Patch 5 left it, gains "(d) every `REVIEW.md` Always check line the diff breaks, reported once under (d) and not again under (a)"; new section "`REVIEW.md` Always check" after "Docs index drift": check every line against the whole diff (the whole pull request in Rounds 3 to 5), one Finding per broken line under the Bug class the line names, and a closing `clear`-or-Finding list of every line.
- `VERIFY.md`: the Verifier is told `REVIEW.md` comes with its Always check lines, and that a Finding raised from one is real when the code breaks that line as written.
- `SKILL.md` step 2: "always-check list" became "Always check list", and the `REVIEW.md` paragraph says the standards Finder checks each Always check line, linking the new `FINDERS.md` section.
- `scripts/check-plugin.sh`: new check 12 (always-check: `FINDERS.md`, `VERIFY.md` and `SKILL.md` mention Always check; `FINDERS.md` has the section).
- `.claude-plugin/plugin.json`: version 0.7.0 to 0.7.1.

Merging an Upstream update: the standards brief is Upstream text, so when Upstream changes its standards prompt, carry the change into `FINDERS.md` (Patch 5's note) and keep the "(d)" clause. The rest of this Patch edits text that is ours.

## Patch 10: `ask-matt` describes `implement` and `code-review` as they now work (`ask-matt/`)

Why: issue #28. Patch 2 trimmed `ask-matt`, but its text still described `implement` and `code-review` as Upstream wrote them. Since Patches 5 and 8, `implement` coordinates one lone Ticket (ADR 0004) and `code-review` runs Find, Verify and Rank in Rounds (ADR 0003).

What:

- `SKILL.md`, step 3 of the main flow. Upstream lines, and what became of each:
  - "**`/implement`** per ticket, **`/clear`ing context between each one**.": now "**each in its own fresh thread**", because each lone ticket gets its own Ticket thread.
  - "**No** → **`/implement`** right here, in the same context window.": now says `/implement` runs a lone ticket: its thread starts an Implementer subagent, opens a pull request with `/pr`, runs the `/code-review` Rounds, then merges it or brings it to the user.
  - "closes out with **`/code-review`**, a two-axis review (Standards + Spec) of the diff. `/implement` runs both per ticket;": now describes Finders, a Verifier and ranking by Severity, run in Rounds on a pull request, and says that in `/implement` the Implementer drives `/tdd` and the thread runs `/code-review`.
  - "Each `/implement` then starts fresh, working from the ticket." (Context hygiene): now "starts in its own fresh thread".
- Left as Upstream wrote them, for ticket #11: the `/implement-spec` bullet ("integration branch"), and the clause "`/implement-spec`'s implementers each drive `/tdd`, and it runs one `/code-review` over the integration branch". Patch 11 (ticket #11) has since rewritten both.
- The Yes-branch's routing of a Spec's tickets to `/implement` was left open here; Patch 12 fixed it.
- Checked and kept as they are, because they still fit: Context hygiene's `/clear` before `/retro` (it is about clearing a session, not about `/implement`); the wayfinder on-ramp's "go straight to `/implement`" (its "`/to-tickets` and `/implement` as usual" was later changed to `/implement-spec` by Patch 12); the triage line ("which **`/implement`** later picks up").
- `scripts/check-plugin.sh`: new check 13 (ask-matt-routing: `ask-matt/SKILL.md` must not say "same context window" or "two-axis", and must mention Rounds).
- `.claude-plugin/plugin.json`: version 0.7.1 to 0.7.2.

Merging an Upstream update: carry Upstream's changes to step 3 and Context hygiene over by hand and re-apply the lines above. The two `implement-spec` lines are Patch 11's now; merge Upstream changes to them there.

## Patch 11: `implement-spec` coordinates one Spec (`implement-spec/`)

Why: ADR 0004 and ADR 0005. Upstream's `implement-spec` lands every ticket on one "integration branch" through a merger subagent and runs one `code-review` at the end, with an optional draft pull request. A Spec thread coordinates instead: Implementer subagents build each ticket test-first in a local worktree off one pushed Spec branch, each ticket gets a Quick ticket check and is squash-merged into the Spec branch, the Spec pull request opens as a draft with `pr`, gets the full `code-review` Rounds, and merges into main with a merge commit, or goes to the user.

What:

- `SKILL.md` rewritten whole as nine steps (read the spec and its tickets, make the Spec branch, start an Implementer per frontier ticket, check the evidence, run the ticket check, land the ticket, review in Rounds, merge or bring it to the user, clean up and report), with a new agent-facing description that says when to use it. Upstream lines, and what became of each:
  - "You have been provided a spec. This spec should have tickets associated with it ...": replaced by the coordinator paragraph and step 1 (fetch the spec and every ticket, state the title, ask if ambiguous); a lone Ticket goes to `implement`.
  - The issue-tracker line: kept word for word.
  - "The goal is the entire spec implemented on a single **integration branch** ...": replaced by the pushed Spec branch from main (step 2) and the merge commit into main (step 8); a tracker that does not close work through pull requests (local files) gets the spec and tickets marked done after the merge.
  - The **task graph** and **frontier** paragraph: kept, reworded as the frontier of tickets whose blockers have all landed; step 1 maps the blocking edges and stops on an unmerged blocker outside the spec.
  - "Start every subagent with a fresh context window.", the sparse communication through **context pointers**, and running Implementers in the background: kept together in one paragraph near the top.
  - Step 1 (read the spec and tickets) with Patch 4's reader line ("Start at `docs/index.md` and open only the docs that fit (with no index, fall back to `GLOSSARY.md` or `GLOSSARY-MAP.md`, and `docs/adr/`)"): kept in step 1, the reader line word for word.
  - Step 2 (optional **exploration subagent** saving Markdown notes outside the repo): kept in step 1; the Implementer's brief points at the notes.
  - Step 3 (create the integration branch; open a draft PR after the first merge, closing the spec and tickets): split into step 2 (Spec branch from up-to-date main, pushed) and step 6.5 (the draft opens with `pr` after the first ticket lands, closes the spec and every ticket, carries per-ticket Evidence and a Door that is one-way if any ticket is, and its body is updated as tickets land). It is no longer optional.
  - Step 4 (a fresh implementer per ticket in its own worktree; confirm the base and reset; `tdd`; merge the integration branch tip before reporting): replaced by step 3. The thread makes each worktree with `git worktree add` from the Spec branch onto a local Ticket branch that is never pushed (Claude Code's subagent worktrees start only from the default branch or HEAD, and the cloud's GitHub connection cannot delete branches), so the base check and reset are dropped. The brief keeps `tdd` (at seams agreed before the first test) and the merge of the Spec branch tip before reporting (a merge, never a rebase), and adds the docs index, reinstalling dependencies in the worktree, and the evidence with the one-way-door call.
  - Step 5 (a **merger subagent** merges each finished ticket): replaced by step 6. The thread lands one ticket at a time: fetch main and merge it into the Spec branch if it moved (never a rebase; conflicts go to a new Implementer on the highest tier of the tickets touched), have the ticket's Implementer merge the Spec branch tip in again if it moved, squash-merge the Ticket branch into the Spec branch as one commit with no pull request, push the Spec branch straight away, and remove the worktree.
  - Step 6 (start more implementers as the frontier changes): kept as step 6.6, with at most 3 Implementers at once (step 3).
  - Step 7 (one `code-review` over the integration branch; one fresh implementer fixes everything): replaced by step 5 (a Quick ticket check per ticket over its diff against the Spec branch, pointing at `code-review/ROUNDS.md#ticket-checks`; the ticket's Implementer fixes Importants and "fix" Nits; fresh reviewers each check; at most 3 checks, then the user; each check recorded as a comment on the Spec pull request) and step 7 (the full Rounds run by the thread on the Spec pull request; main fetched and merged in before each Round; ticket-check Findings count as already raised; Findings go to a new Implementer on the Spec branch on the highest tier of the tickets they touch, regular if none; a merge from main in a commits-only Round counts among the new commits but only its conflict resolutions are reviewed; Pre-existing Findings, the ticket checks' included, filed after the last Round).
  - Step 8 (mark the draft ready, or resolve each ticket and report the branch): the draft is marked ready once every ticket has landed (end of step 6); resolving the tickets moved into step 8.2.
  - Step 9 (clean up the worktrees): kept as step 9, with `git worktree remove`/`prune` and deleting the local Ticket branches.
  - Added: the Model tier of each ticket from its "Model tier" line (regular if none); cheap subagents for trivial jobs; keeping one Implementer per ticket by message, or a new one with a handoff, telling the user you did; redoing a ticket whose worktree was lost when the machine was reclaimed; checking the evidence (step 4), with the fallback when a repo has no checks; the self-merge rules of ADR 0004, as in `implement` step 7; at merge time, merging main in, one more Round over that merge's conflict resolutions if it had conflicts and the 5-Round cap allows, otherwise the user, and rerunning the checks and CI; the merge commit into main; the final report. Also added: the thread never writes code, not even to resolve a merge conflict; the cap of 3 counts every working Implementer (building, fixing, or on the Spec branch), and the thread waits for a free slot before starting or resuming one; a Spec-branch Implementer works in the thread's own checkout, where the thread runs no git commands meanwhile; tickets land one at a time, and none while a Spec-branch Implementer works; a conflicting merge of main into the Spec branch is aborted and handed to a new Implementer; after a third ticket check with an Important open, the tickets it blocks are not started, the others still land, and the Spec pull request stays a draft with no Rounds until the user decides; a step-7 Implementer may be continued by message when later Findings need no higher tier; the final "fix" Nits commit on a clean Round 2 to 5. Judgement on ADR 0005's "ticket check clean": conflict resolutions from a ticket's re-merge of the Spec tip (step 6.2) get no new ticket check, because the Spec pull request's Rounds 1 and 2 review the whole pull request, including them.
- `agents/openai.yaml`: `short_description` now "Coordinate one spec: worktree Implementers, ticket checks, spec PR, Rounds".
- After the build-flow check: step 2 says "fetch main" means `git fetch origin main` and comparing against `origin/main`, never a stale local `main`; step 6.2 says conflict resolutions from the ticket's re-merge are reviewed by the Spec pull request's Rounds 1 and 2, with no new ticket check.
- New file (ours, not Upstream text): `evals/implement-spec/RESULTS.md`, one entry per build-flow check of `implement-spec`.
- `ask-matt/SKILL.md` (the `/implement-spec` bullet under "Is this a multi-session build?" and the paragraph after it): "integration branch" becomes "spec branch"; the bullet now says Implementers work in their own worktrees, each ticket gets a Quick ticket check and is squash-merged into the spec branch, whose pull request gets the full review and a merge commit into main; the next paragraph says `/implement-spec` runs `/code-review` as a ticket check per ticket and in Rounds over the spec branch's pull request. No other text in `ask-matt` changed. These are the two lines Patch 10 left as Upstream wrote them for this ticket; Patch 10's rewording of the rest of step 3 is kept, and its open point on the Yes-branch routing a Spec's tickets to `/implement` was not part of this Patch; Patch 12 fixed it.
- `scripts/check-plugin.sh`: new check 14 (implement-spec-coordinator: `implement-spec/SKILL.md` names `` `tdd` ``, `` `pr` `` and `` `code-review` ``, says Implementer, `git worktree add` and merge commit, and does not say "integration branch"; `ask-matt/SKILL.md` does not say "integration branch").
- `.claude-plugin/plugin.json`: version 0.7.2 to 0.8.0.

Merging an Upstream update: Upstream's `implement-spec/SKILL.md` is replaced whole, so diff Upstream's old and new text and carry any change over by hand into the step it maps to above (reading the spec and the task graph into step 1, worktree and building advice into step 3, merging into step 6, review into steps 5 and 7, cleanup into step 9). Keep Patch 4's reader line and the words check 14 looks for. Upstream changes to the `/implement-spec` lines in `ask-matt` are merged the same way, keeping "spec branch".

## Patch 12: `ask-matt` sends a Spec's tickets to `implement-spec` (`ask-matt/`)

Why: issue #28. After Patch 11, `implement` step 1 sends a Ticket under a Spec to `implement-spec` (ADR 0004), but `ask-matt` still offered `/implement` per ticket for a Spec's tickets.

What:

- `SKILL.md`. Lines as they stood after Patches 10 and 11, and what became of each:
  - The Yes-branch's two bullets ("Then work the tickets one of two ways:", "**`/implement`** per ticket, **each in its own fresh thread**. On a local tracker that's one file per ticket ... the last one's context is disposable." and "**`/implement-spec`** for the whole spec in one run. ... Reach for it when you'd rather orchestrate the build than drive each ticket yourself."): merged into one. The local-tracker and native-links sentence moves up beside the blocking edges; `/implement-spec` runs in its own fresh thread, with Patch 11's description of it kept, minus its last sentence; and a closing sentence says not to hand a spec's tickets to `/implement` one by one. Dropped with the two bullets: "worked blockers-first by hand", "so any ticket whose blockers are done can be grabbed", "Each ticket is self-contained, so the last one's context is disposable.", and "Reach for it when you'd rather orchestrate the build than drive each ticket yourself."
  - "Each `/implement` then starts in its own fresh thread, working from the ticket." (Context hygiene): now "The build then starts in its own fresh thread: `/implement-spec` for a spec, `/implement` for a lone ticket, each working from the tickets."
  - "then `/to-tickets` and `/implement` as usual." (wayfinder on-ramp): now `/implement-spec`. Its "go straight to `/implement` only when the effort turned out genuinely small" stays, since a small effort is a lone ticket.
  - The "Either way" paragraph and the triage line (issues `/implement` later picks up) still fit and are unchanged.
- `scripts/check-plugin.sh`: check 13 now also fails if `ask-matt/SKILL.md` contains "`/implement`** per ticket".
- `.claude-plugin/plugin.json`: version 0.8.0 to 0.8.1.

Merging an Upstream update: carry Upstream's changes to step 3, Context hygiene and the wayfinder on-ramp over by hand and re-apply the lines above.

## Patch 13: the `code-review` skill is renamed `agentic-review` (`agentic-review/` and every skill that names it)

Why: issue #50. Our skill shared its name with Claude Code's built-in `code-review`, so a plain `/code-review` or "run the `code-review` skill" reached the built-in, which has no Rounds, posts no Round comment and records no Ticket check. A rename only: the Review behaves as before. Patches 1 to 12 above still say `code-review`, as the skill was then named.

What (Upstream text changed):

- Folder `upstream-skills/code-review/` becomes `upstream-skills/agentic-review/` (git mv). Its `SKILL.md` frontmatter `name:` is now `agentic-review`; `agents/openai.yaml` `display_name` is now "Agentic Review"; the one-line links in `FINDERS.md`, `ROUNDS.md` and `VERIFY.md` name `agentic-review`.
- Every other mention of the skill name in `implement`, `implement-spec`, `ask-matt`, `retro` (`SKILL.md`, `BUG-CLASSES.md`) and `tdd` is now `agentic-review`.
- Not changed: the `<!-- code-review kind=round ... -->`, `kind=ticket-check` and `kind=pre-existing` marker lines. They are a data format that `retro` reads out of Round comments already posted on past pull requests, so renaming them would hide those Rounds.
- Outside Upstream text: `evals/code-review/` becomes `evals/agentic-review/`; GLOSSARY.md, `docs/index.md`, READMEs, ADRs 0001, 0003, 0004, 0006 and 0007 and `plugin.json` keywords follow. ADR 0003 keeps its filename so existing links hold. ADR 0001 still says Upstream has a `code-review` skill, which is true.
- `scripts/check-plugin.sh`: checks 7 to 14 use the new name; new check 15 (no-code-review-skill) fails if any skill file under `upstream-skills/` or `skills/` tells an agent to run `code-review` (`` `code-review` ``, `dev-skills:code-review`, `/code-review`, "the code-review skill", `name: code-review`) or the old folder exists.
- `.claude-plugin/plugin.json`: version 0.8.1 to 0.9.0.

Merging an Upstream update: Upstream's skill is still `code-review`. Merge its text into `agentic-review/` and keep the name `agentic-review`.

## Patch 14: no person's name in skill text (no Upstream text changed)

Why: issue #49. The plugin will be shared, so skill and doc text says "the user", never the maintainer's name.

What:

- No text under `upstream-skills/` changed: it contained no person's name, so there is nothing to re-apply when merging an Upstream update.
- `scripts/check-plugin.sh`: new check 16 (no-person-names) fails if `upstream-skills/`, `skills/` or the plugin `README.md` contains "Lufei" or "Luffy" (case-insensitive), after removing `luffy-dev-skills`, `luffy-dev`, `Luffytse` and `luffydev`. It matches file contents only, not paths.
- `.claude-plugin/plugin.json`: version 0.9.0 to 0.9.1, and the description no longer says whose skills they are.

## Patch 15: check 16 also scans the repo's doc text (no Upstream text changed)

Why: retro of the issue #49 pull request. "A person's name left in doc text" came up twice in review (`CLAUDE.md` and ADR 0001), and check 16 only looked at skill text.

What:

- No text under `upstream-skills/` changed.
- `scripts/check-plugin.sh`: check 16 now also scans the repo's `CLAUDE.md`, `GLOSSARY.md` and all of `docs/` (including `adr/` and `agents/`), with the same exemptions and the same relative `file:line` output. The manifests (author fields) and `dai-portal-data` stay out of scope.
- `.claude-plugin/plugin.json`: version 0.9.1 to 0.9.2.

## Patch 16: `retro` files its suggestions as Retro issues; `triage` skips them (ADR 0007)

Why: ADR 0007 and issue #40. Upstream's `retro` hands every suggestion to the user in its report, where it is read once and lost. Suggestions that are not repeated Bug classes now become Retro issues, or "seen again" votes on open ones, so a backlog can show which problems repeat. `triage` must skip them, since they carry no `needs-triage` label and would look untriaged.

What:

- `retro/SKILL.md`: new step 5, "File every candidate that is not a repeated Bug class as a Retro issue, or vote on an open one that covers it, and check whether Retro planning is due: [FILING.md](FILING.md)."; Patch 6's step 5 (Upstream's "Present these candidates...") becomes step 6 and gains "For each other candidate, give the issue it went to; add the due notice from step 5 when it applies." Every other line is as Patch 6 left it.
- New `retro/FILING.md` (ours, not Upstream): routing (skill or workflow problems to the repo in the plugin manifest's `repository` field, a project's own problems to its tracker from `docs/agents/issue-tracker.md`, else the `origin` remote), votes (`Seen again in <thread link>`), the `retro` label and `Retro:` title, the can't-write fallback, the thresholds (10 open; 2 weeks with at least 4 open) and the trigger clock from the newest closed `retro-planning` record, and what the report lists. Since one retro can file into both repos, the due check runs once per repo that was filed or voted into, and the report's due notice names each repo that is due.
- `triage/SKILL.md`: in "Show what needs attention", a sentence after the three buckets, "Skip issues labelled `retro`: they are Retro issues, planned in batches, not untriaged work."; in "Triage a specific issue or PR" step 1, a leading sentence "If the issue is labelled `retro`, stop: it is a Retro issue, planned in batches, so skip it." before "Read the full", which becomes "Otherwise read the full". Every other line is Upstream's.
- `scripts/check-plugin.sh`: new check 17 (retro-filing: `plugin.json` has a `repository` GitHub URL; `retro/FILING.md` exists, `retro/SKILL.md` links it, and it names `retro`, `Retro:`, "seen again" and `retro-planning`; `triage/SKILL.md` skips `retro`; no forked or own skill text names a project, repo or person).
- `.claude-plugin/plugin.json`: a new `repository` field, and version 0.9.2 to 0.9.3, one bump shared by Patches 16 to 18 and the CI workflow below, which shipped together (spec #38).

Merging an Upstream update: carry Upstream's `retro/SKILL.md` and `triage/SKILL.md` changes over by hand and re-apply the lines above.

## Patch 17: `implement` and `implement-spec` end by running `retro` (ADR 0004, ADR 0007)

Why: issue #42. Each build thread knows its own Review, so it ends by running `retro` on itself and every build feeds the Retro backlog. The build thread still writes no code: a check the retro proposes is built by an Implementer.

What:

- `implement/SKILL.md`: new step 9, "Run the retro", after the report. `implement-spec/SKILL.md`: new step 10, "Run the retro", after "Clean up and report". Each says: run `retro` on the thread whether the pull request was merged or handed to the user; for a repeated Bug class, a regular-tier Implementer builds the check on a branch off main, and the thread opens the pull request with `pr`, runs the `agentic-review` Rounds and merges it as a lone pull request (squash-merge, or brings it to the user); a check that changes `REVIEW.md` goes to the user; add the outcome to the report. Every other line is as Patches 8 and 11 left it.
- `scripts/check-plugin.sh`: new check 18 (retro-last-step: the last step of both skills names `` `retro` `` and `REVIEW.md`).
- `.claude-plugin/plugin.json`: no bump of its own; covered by Patch 16's 0.9.2 to 0.9.3.

Merging an Upstream update: both `SKILL.md` files are already replaced whole by Patches 8 and 11, so after carrying Upstream's changes over, re-append the final retro step and keep it last, since check 18 reads the last `## ` section.

## Patch 18: `ask-matt` routes a due Retro backlog to `retro-planning` (ADR 0007)

Why: ADR 0007 and issue #41. `retro` now files Retro issues and says when Retro planning is due; the new skill of our own, `retro-planning` (under `skills/`, not Upstream), works through the backlog, and `ask-matt` must route to it.

What:

- `ask-matt/SKILL.md`: step 4 (the `/retro` item, as Patch 10 left it) gains a closing sentence: "Suggestions it doesn't act on straight away pile up as Retro issues; when its report says your Retro backlog is due, start a thread for **`/retro-planning`**, which groups the backlog by root cause, closes one-offs, and turns the most repeated problems into tickets." Every other word of the item is unchanged.
- New `skills/retro-planning/SKILL.md` (ours, not Upstream): ADR 0007's Retro planning steps and the record format.
- `scripts/check-plugin.sh`: new check 20 (retro-planning: `skills/retro-planning/SKILL.md` exists and names `retro-planning`, `Retro planning <yyyy-mm-dd>`, "at most 3", `wontfix` and `ready-for-agent`; `ask-matt/SKILL.md` names `/retro-planning`).
- `.claude-plugin/plugin.json`: no bump of its own; covered by Patch 16's 0.9.2 to 0.9.3.

Merging an Upstream update: carry Upstream's changes to the `/retro` item over by hand and re-append the sentence above.

## Not a Patch: CI workflow and check 19

Our own, not Upstream: `.github/workflows/plugin-checks.yml` (issue #39) runs `scripts/check-plugin.sh` and `claude plugin validate .` on pull requests and pushes to main. `scripts/check-plugin.sh` gets check 19 (the workflow exists, triggers on `pull_request` and pushes to main, installs `@anthropic-ai/claude-code`, and runs both commands). No Upstream text changed. `.claude-plugin/plugin.json`: no bump of its own; covered by Patch 16's 0.9.2 to 0.9.3.

## Not a Patch: check 21 (PATCHES.md and the script agree on check numbers)

Our own, not Upstream. `scripts/check-plugin.sh` gets check 21, from the retro of PR #56 (PATCHES.md describing a change wrongly after renumbering came up 5 times): every "new check N" in this file names a check whose `# N.` header is in the script (later, see Not a Patch: `check-plugin.sh` gives the same result however it runs, and catches numbering and name drift: compared as number and name pairs), no N is claimed as "new check" twice, and every check from 9 up is named as "check N" somewhere in this file (case-insensitive). No Upstream text changed. `.claude-plugin/plugin.json`: 0.9.3 to 0.9.4.

## Patch 19: `agentic-review` takes the built-in review's strengths (`agentic-review/`)

Why: issue #51. A comparison with Claude Code's built-in review found six things it does that ours did not: it reads uncommitted work, every finding states how it fails, it hunts more angles, finders pass on what they half believe, its verifier keeps rare but real paths, and it looks for what is missing. Everything ours already did better (Rounds, the spec Finder, Bug classes, Pre-existing, Deep's three-stance vote, `REVIEW.md`, Model tiers, stopping when subagents cannot start) is unchanged.

What (Upstream-derived text changed):

- `SKILL.md`: the depth table's Deep row adds a gap sweep Finder (premium) after Verify and a second 3 Verifiers for its Findings; step 1's fixed-point diff is now `git diff --merge-base <fixed-point>` (the working tree, so staged and unstaged work counts) plus the untracked new files, read whole, and the commit list, and says pull-request Rounds review commits only; the non-empty check counts the untracked files; step 4 says a failure scenario the Verifier corrected replaces the Finder's, and adds a paragraph that runs the gap sweep on Deep; step 5's report adds each Finding's failure scenario.
- `FINDERS.md`: the shared brief lists the untracked new files for a fixed point, and its quoted instruction adds "Give each Finding a failure scenario" and passing on half-believed candidates marked `(unsure)`; the adversarial brief says unchanged lines inside a touched function are in scope, and drops "Cite the input, path or sequence of events that makes each problem happen" (the Failure scenario line does that now); five new angles (Removed behaviour, Cross-file callers, Language pitfalls, Wrappers and proxies, Altitude); new section "Gap sweep (premium tier, Deep only)"; the Finding format's Claim is now "what is wrong", and a new Failure scenario line follows it (a cleanup Finding states its cost).
- `VERIFY.md`: call 1 corrects a real Finding's wrong failure scenario instead of dropping it, and the answer returns the corrected one; keeps realistic rare paths, judges a cleanup Finding by its cost and an `(unsure)` one like any other; the tracer shows the failure scenario happens; new section "Gap sweep": a second Deep Verify of the gap sweep's Findings with three brand-new Verifiers and the same rules.
- `ROUNDS.md`: "Filing Pre-existing Findings" step 2 now lists every location "with its claim, failure scenario and evidence" (was "with its claim and evidence"), since the Claim no longer says what goes wrong. The `<!-- code-review kind=... -->` marker lines are unchanged.
- Outside Upstream text: `GLOSSARY.md` gains Failure scenario and Gap sweep, and its Finder and Finding lines name them; ADR 0003 amended in place (intro, Find, Verify, Deep, uncommitted work, and a considered option on the gap sweep's tier).
- `scripts/check-plugin.sh`: new check 22 (agentic-review-strengths: `SKILL.md` says untracked and gap sweep; `FINDERS.md` has the Failure scenario line, `(unsure)`, the five angles and the Gap sweep section; `VERIFY.md` says gap sweep, failure scenario and rare; `GLOSSARY.md` and ADR 0003 name Gap sweep and Failure scenario).
- `.claude-plugin/plugin.json`: version 0.9.4 to 0.10.0.

Merging an Upstream update: of Patch 5's Upstream-moved text, this Patch edits only the shared brief list at the top of `FINDERS.md` (the untracked new files) and `SKILL.md` step 1 (the fixed-point diff), both listed above; the smell baseline, the standards and spec briefs and the step-2 source lookup are untouched. Carry Upstream changes over as Patch 5 says and re-apply the lines above.

## Patch 20: `ask-matt`'s tracker and routing text matches the skills it routes to (`ask-matt/`)

Why: issue #32, Pre-existing Findings from the review of PR #31. Three sentences in `ask-matt` (four points; blocking edges and the local path share one) said more, or less, than `to-tickets`, `implement`, `implement-spec` and the local issue-tracker setup do.

What:

- `ask-matt/SKILL.md`, step 3's Yes-branch: "On a local tracker that's one file per ticket under `.scratch/<feature>/issues/`; on a real tracker the edges become native blocking links." is now "On a local tracker the spec is `.scratch/<feature-slug>/spec.md` and the tickets are one file per ticket under `.scratch/<feature-slug>/issues/`, each with a "Blocked by" line; on a real tracker the edges are native blocking links where the tracker has them, and a "Blocked by" line otherwise."
- `ask-matt/SKILL.md`, triage on-ramp: "which **`/implement`** later picks up" is now "which **`/implement-spec`** (for an issue under a Spec) or **`/implement`** (for a lone one) later picks up".
- `ask-matt/SKILL.md`, wayfinder on-ramp: "go straight to `/implement` only when the effort turned out genuinely small." now continues ": write one lone ticket first (for example with `/to-tickets`), then run `/implement` on it."
- `scripts/check-plugin.sh`: new check 23 (ask-matt-tracker: `ask-matt/SKILL.md` no longer says "become native blocking links", and names the "Blocked by" line, `.scratch/<feature-slug>/spec.md`, "write one lone ticket", and `/implement-spec` in the triage bullet).
- `.claude-plugin/plugin.json`: version 0.10.0 to 0.11.0.

Merging an Upstream update: carry Upstream's changes to step 3, the triage on-ramp and the wayfinder on-ramp over by hand and re-apply the lines above.

## Patch 21: the formerly user-only skills get model-facing descriptions (`ask-matt/`, `grilling/`, `grill-with-docs/`, `handoff/`, `improve-codebase-architecture/`, `retro/`, `to-spec/`, `to-tickets/`, `triage/`, `wayfinder/`, `diagnosing-bugs/`)

Why: issue #15. Upstream's formerly `disable-model-invocation: true` skills kept one-line, human-facing descriptions with no trigger branches, but they are model-invoked here, and `writing-for-agents/SKILL-MECHANICS.md` says a model-invoked skill needs a model-facing description. `implement` and `implement-spec` were done in Patches 8 and 11 and are unchanged. `setup-matt-pocock-skills` is left out: PR #84 (ticket #77) replaces it with `setup-dev-skills`, which has its own description. Each new description says what the skill does and "Use when ..." with words a user types, and no two claim the same trigger (`grill-with-docs` vs `grilling`, split on whether the work is in a repo: `grill-with-docs` when working in a repo, `grilling` when there is no working directory to record in or only the interview is wanted; `to-spec` vs `to-tickets` vs `wayfinder`, `retro` vs `retro-planning`, `improve-codebase-architecture` vs `codebase-design`).

What (Upstream-derived text changed; only the `description:` frontmatter line of each skill, no bodies):

- `ask-matt/SKILL.md` `description`: "Ask which skill or flow fits your situation. A router over the skills in this repo." is now "Route the user to the right skill or flow for their situation, from idea to ship. Use when the user asks which skill to use, where to start a new piece of work, or how the skills fit together."
- `grilling/SKILL.md` `description`: "Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases." is now "Grill the user relentlessly about a plan, decision, or idea. Use when there is no working directory to record in, or the user wants only the interview with nothing written down; in a repo, grill-with-docs is the default."
- `grill-with-docs/SKILL.md` `description`: "A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go." is now "Interview the user relentlessly about a plan or design, recording glossary terms and ADRs as decisions settle. Use when the user says "grill me" or wants a plan or design stress-tested while working in a repo."
- `handoff/SKILL.md` `description`: "Compact the current conversation into a handoff document for another agent to pick up." is now "Compact the current conversation into a handoff document for a fresh agent to continue from. Use when the user says "handoff" or "hand off", or the work moves to a new harness, directory or colleague, or a side task forks off mid-phase."
- `improve-codebase-architecture/SKILL.md` `description`: "Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick." is now "Scan a whole codebase for refactors that turn shallow modules into deep ones, present them as a visual HTML report, then grill through the one the user picks. Use when the user asks to improve the architecture, find refactoring candidates, or review the codebase's structure."
- `retro/SKILL.md` `description`: "Conduct a retrospective on a coding session." is now "Review a finished coding session or pull request and propose improvements to the agent's environment (navigation pointers, automated checks, coding standards, docs). Use when the user asks for a retro or retrospective on a session or pull request, or what went wrong in it and how to stop it recurring; the Retro backlog is retro-planning."
- `to-spec/SKILL.md` `description`: "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed." is now "Synthesise the current conversation into a spec and publish it to the issue tracker, with no interview. Use when the user says "write the spec", "turn this into a spec" or "make a PRD" once the plan is settled."
- `to-tickets/SKILL.md` `description`: "Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real tracker)." is now "Split a plan, spec or conversation into tracer-bullet tickets, each declaring what blocks it, and publish them to the tracker. Use when the user says "break this into tickets" or "split into issues", or asks for vertical slices of an existing spec."
- `triage/SKILL.md` `description`: "Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs." is now "Move issues and external PRs through the triage roles (category and state), verify them, and write agent-ready briefs. Use when the user says "triage" or asks to look at incoming issues or external PRs."
- `wayfinder/SKILL.md` `description`: "Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear." is now "Chart work too big for one agent session as a map of decision tickets on the issue tracker, and resolve them one at a time until the route is clear. Use when the user has a large, foggy effort too big for one session (for example "wayfind this" or "map this out"), before any spec exists."
- `diagnosing-bugs/scripts/hitl-loop.template.sh`: file mode 100644 to 100755, since its header says to run it directly. No content change.
- `.claude-plugin/plugin.json`: version 0.11.0 to 0.12.0.

Merging an Upstream update: keep our description line for each skill above and take Upstream's body changes; keep the template script executable.

## Patch 22: `setup-matt-pocock-skills` becomes our own `setup-dev-skills` (`skills/setup-dev-skills/`)

Why: issue #77. The forked setup skill was never reworked for our skill set (GitHub only, the labels the skills use, GitHub settings the build skills rely on, cloud sessions without GraphQL `gh`). It is now our own skill, derived from Upstream's, in `skills/` where our own skills live. ADR 0001 keeps 22 Upstream skills.

Removed from Upstream text: the whole folder `upstream-skills/setup-matt-pocock-skills/` (`SKILL.md`, `domain.md`, `issue-tracker-github.md`, `issue-tracker-gitlab.md`, `issue-tracker-local.md`, `triage-labels.md`, `agents/openai.yaml`). It is now `skills/setup-dev-skills/`, which keeps Patch 1 (model-invoked) and Patch 4 (the docs index and the index-first `domain.md`), drops `agents/openai.yaml`, the GitLab and local seeds and the "Other" tracker option, and credits Upstream and `LICENSE-mattpocock-skills`. Its description gains a "Use when ..." trigger in the style of Patch 21's descriptions. The note about `domain-modeling` splitting a large glossary now lives only in the `domain.md` seed, not in `SKILL.md` Section C. Merging an Upstream update to the setup skill: diff Upstream's folder against `skills/setup-dev-skills/` and take over by hand what still fits.

Upstream text changed in other skills:

- `ask-matt/SKILL.md`: "run `/setup-matt-pocock-skills`" in the setup entry becomes `setup-dev-skills`, and "Custom issue trackers also work." becomes "It supports GitHub repos only for now."
- `wayfinder/SKILL.md` (tracker paragraph): the rename, with "and stop" added, and the sentence "If no tracker has been provided, default to the local-markdown tracker." deleted.
- `implement/SKILL.md`, `implement-spec/SKILL.md`, `agentic-review/SKILL.md`, `to-spec/SKILL.md`, `triage/SKILL.md`: `/setup-matt-pocock-skills` becomes `setup-dev-skills`.
- `to-tickets/SKILL.md`: the same rename in both places (the opening line and step 5's "depends on the tracker ... configured").

Left as Upstream wrote them: the local and GitLab mentions in `to-tickets`, `agentic-review`, `implement-spec` and `ask-matt` (its local-tracker line, which Patch 20 reworded but left about a local tracker).

Also in this Patch:

- `scripts/check-plugin.sh`: check 1 expects 22 skills (the kept list drops `setup-matt-pocock-skills`); check 7 takes `setup-dev-skills/SKILL.md` and `setup-dev-skills/domain.md` from `skills/`; new check 24 (setup-dev-skills: the old folder is gone; the own skill has `SKILL.md`, the seeds, no `agents/openai.yaml` and no GitLab or local seed; `SKILL.md` credits `LICENSE-mattpocock-skills`, names `wayfinder:map` and says settings are never changed).
- ADR 0001 and ADR 0006 and the plugin `README.md` name `setup-dev-skills`; this repo's `docs/agents/` and `CLAUDE.md` match what a re-run writes, apart from repo-specific examples (real ADR names, the ADR 0007 link).
- `.claude-plugin/plugin.json`: version 0.12.0 to 0.13.0 (a skill name was removed).

## Not a Patch: `retro-planning` walks one item at a time (issue #70)

Our own, not Upstream. `skills/retro-planning/SKILL.md` now snapshots the backlog at the start, files its record as an open issue then and closes it at the end (a planning whose record is open is resumed from it), walks the user through one group at a time and carries out each call at once, frees a cap slot when a proposed Ticket is closed or spun off, lets only the user raise the cap for one planning, and sends a group that needs more discussion to its own planning thread (via the coordinator, or the user). The record gains Snapshot, Cap, Spun off, Arrived during this planning and Spun off, waiting sections. ADR 0007's Retro planning steps, `GLOSSARY.md` (Retro planning, new Spin-off) and the plugin README match. No Upstream text changed. `ask-matt`'s routing sentence still holds. `retro/FILING.md` is unchanged, but its clock, which runs from the creation of the newest closed record, now runs from the start of the last planning rather than its end, since the record is filed at the start.

- `scripts/check-plugin.sh`: new check 25 (retro-planning-record: the record template keeps its Snapshot, Cap, Spun off, Spun off, waiting, Arrived during this planning, Held back by the cap, plannings-without-a-new-vote and Waiting on open Tickets sections; the skill files the record as an **open** issue, walks one at a time, and has the spin-off comment and the "Running a spun-off planning" section).
- `.claude-plugin/plugin.json`: version 0.13.0 to 0.14.0.

## Patch 23: `grilling` asks at most 3 questions per round (`grilling/`)

Why: issue #34. The base note above deferred the 3-question rule "for a later ticket" that was never filed, while ADR 0001 and ADR 0004 assume `grilling` already follows it and only `setup-project` overrode Upstream's "whole frontier" rule.

What:

- `grilling/SKILL.md`: "Ask the whole frontier in one round: number each question and give your recommended answer." is now "Ask at most **3** frontier questions in a round: number each question and give your recommended answer. When the frontier holds more than 3, ask the 3 whose answers unblock the most other decisions, and keep the rest for later rounds; they go first in the next round, ahead of questions the user's answers newly unblock." Later in the file, "ask the rest of the frontier now" is now "ask the rest of this round's questions now". The recommended answers and the round format are unchanged.
- `setup-project/SKILL.md` (our own skill, not Upstream text): drops its override of "whole frontier per round", since `grilling` now carries the rule. `grill-with-docs` and the other skills built on `grilling` inherit it and needed no edit.
- `scripts/check-plugin.sh`: new check 26 (grilling-round-cap: `grilling/SKILL.md` says at most 3 questions and keeps the rest for later rounds, and no longer says "whole frontier"; `setup-project/SKILL.md` no longer says it overrides).
- New file (ours, not Upstream text): `evals/implement/RESULTS.md`, one entry per build-flow check of `implement`, listed in `docs/index.md`.
- `.claude-plugin/plugin.json`: version 0.14.0 to 0.15.0.

Merging an Upstream update: take Upstream's `grilling` text, then re-apply the two edits above.

## Not a Patch: check 27 (version bumps in PATCHES.md agree with plugin.json)

Our own, not Upstream. `scripts/check-plugin.sh` gets check 27, from the retro of PR #91 (stale or duplicated version numbers after renumbering came up 4 times): no "version X to Y" bump in this file has the same target Y twice, and the highest Y is `plugin.json`'s version. A gap-free chain is not required, since history has gaps (0.2.0 to 0.3.0, 0.9.3 to 0.9.4). `REVIEW.md` gains an Always check line, "results entry out of date with its own PR". No Upstream text changed. `.claude-plugin/plugin.json`: version 0.15.1 to 0.16.0.

## Patch 24: `agentic-review` counts reports before moving on (`agentic-review/`)

Why: issue #102 (absorbs #44). In five threads a cheap-tier Finder ended without returning its report and the Review went on, or was caught only because the thread counted by hand. A brief line alone did not stop it, so the thread carries out a count.

What:

- `agentic-review/SKILL.md`: step 3 (Find), step 4 (Verify) and the gap sweep paragraph each have the thread count reports (one report from each Finder or Verifier started), ask again for a missing one, start a new agent on the same brief if it cannot be reached, and not go on without it. The counts gate the next step: Verify (after Find), then the gap sweep on Deep or Rank (after Verify), then the second Verify (after the sweep Finder) and Rank (after the second Verifiers).
- `agentic-review/FINDERS.md`: each of the 5 briefs (standards, spec, adversarial, security, gap sweep) ends with "Your last action is to return your full report."
- `agentic-review/VERIFY.md`: the Verifier brief ends with the same line.
- `scripts/check-plugin.sh`: new check 28 (report-counts: every Finder brief and the Verifier brief end with that line; `SKILL.md` keeps each of the four count gates as a literal phrase: Finders before Verify, Verifiers before the next step, the gap sweep Finder before the second Verify, the second Verifiers before Rank).
- `.claude-plugin/plugin.json`: version 0.16.0 to 0.17.0.

Merging an Upstream update: take Upstream's text, then re-apply the four count gates (check 28 lists their phrases) and the closing line on each brief (the closing line on each brief is now Patch 32's, guarded by check 38; check 28 keeps only the four gates).

## Patch 25: numbers are taken at merge time, and merge-only Rounds run at Quick (`implement/`, `implement-spec/`, `agentic-review/`)

Why: issue #106 (Retro issues #64, #67, #69). Parallel branches took the same version, Patch and check numbers and were renumbered again and again (spec #38's Spec build, PRs #51 and #82), a renumbering-only merge from main got a full-depth Round, and in #50 the user-merges path never re-ran the "bring it up to date" step. Now the numbers are taken once, last, after the final merge of main. The version bump itself stays required: only *when* it is chosen moved.

What (Upstream-derived text changed):

- `implement/SKILL.md`: step 3's Implementer brief gains a bullet: leave every number the repo's rules say to take at merge time as the placeholder `TBD-N`, or as it is on main where a placeholder would break the file. Step 4's Done line adds that a check failing only on a placeholder or an unbumped version is expected until step 7. Step 6's "Before each Round" paragraph adds that a Round whose new commits are only that merge, with conflicts only in numbers or text, runs at Quick unless the resolutions touch logic. Step 7: after "The user then merges, or tells you to." it says steps 1 and 2 run last on that path too (when the user says to merge, run them, then merge; when the user will merge, ask them to tell the thread first); step 1 now only merges main in; new step 2 "Take the numbers" (the Implementer reads the repo's rules, takes the next free numbers as of main, replaces every `TBD-N`, never skips a required bump; one more Round over the conflict resolutions and that commit, at Quick unless they touch logic, if the merge had conflicts and the cap allows; rerun the checks, wait for CI; repeat if main moves again); the squash-merge is now step 3.
- `implement-spec/SKILL.md`: step 3.2's brief gains the same placeholder bullet, ending "the Spec thread has the real numbers taken once, in step 8". Step 4's Done line adds the same expected-failure sentence (until step 8). Step 7's "Before each Round" paragraph gains the same merge-only Quick sentence. Step 8 gets the same three-step shape as `implement` step 7: the user-merges sentence, step 1 merges main in, new step 2 starts a new regular-tier Implementer on the Spec branch (the thread writes no code) to take the numbers once for the whole Spec and replace the tickets' placeholders, updates the pull request body if it names them, and runs the same Round and checks; the merge commit is now step 3.
- `agentic-review/SKILL.md`: "Depth and tiers" adds the exception after "later Rounds reuse it unless the user changes it": a merge-only Round runs at Quick unless the resolutions touch logic, and the Round after it goes back to the carried depth. Step 1's list of what earlier comments give says the carried depth is the one in the latest comment that is not a merge-only Round's.
- `agentic-review/ROUNDS.md`: the Round comment's `Reviewed:` line gains a third form, `the merge from main <base>..<head> (merge-only Round)`; a new bullet says the marker's and heading's depth is the depth that Round ran at; new section "Merge-only Rounds" (what one is, Quick unless a resolution touches logic, its comment says so, the next Round takes the carried depth from the latest comment that is not merge-only, and it counts toward the cap). The `<!-- code-review kind=... -->` marker shape is unchanged, so `retro/BUG-CLASSES.md`, which keys on the marker prefix and not on its depth, needs no edit.
- Outside Upstream text: `CLAUDE.md` gains the working rule (every plugin change bumps its version; version, Patch and check numbers are taken at merge time; `TBD-N` until then); `GLOSSARY.md` gains Placeholder number and Merge-only Round; ADR 0003 amended in place (the depth stays the same across Rounds except for a merge-only Round); `.github/workflows/plugin-checks.yml` checks out with `fetch-depth: 0` so `origin/main` exists in CI for check 29b (the user committed it to main in 8886bcf, since the agents' GitHub access cannot push workflow files).
- `scripts/check-plugin.sh`: new check 29 (placeholders-and-bumps). (a) Fails on a leftover placeholder: `TBD-N` after Patch, check, version or "to" (bare, in backticks or in parentheses) in `PATCHES.md`, the plugin READMEs, `README.md`, `CLAUDE.md`, `GLOSSARY.md` and `docs/`, a `# TBD-N` header in the script, or a `"version": "TBD...` in a manifest. (b) For every plugin under `plugins/` with a `plugin.json`, if any file under it differs from `origin/main` (committed since the merge-base, `git diff --name-only origin/main...HEAD`, plus staged, unstaged and untracked work), its working-tree version must be strictly higher than `origin/main`'s (dot-separated fields compared as numbers); a plugin new on this branch is skipped, and without `origin/main` (b) is skipped with a note, not a failure. On a push to main, `HEAD` is `origin/main`, so (b) passes.
- `.claude-plugin/plugin.json`: version 0.17.0 to 0.18.0.

This Patch was built before its own rule applied, so its numbers were written in place, then re-taken when main moved: #103 took check 27 and 0.16.0, then #105 took Patch 24, check 28 and 0.17.0, so this Patch is Patch 25, check 29 and 0.18.0.

Merging an Upstream update: `implement` and `implement-spec` are already replaced whole by Patches 8 and 11, so re-apply the lines above after carrying Upstream's changes over. For `agentic-review`, carry Upstream's "Depth and tiers", step 1 and `ROUNDS.md` changes over by hand and re-apply the exception, the step-1 clause, the `Reviewed:` form, the Depth bullet and the "Merge-only Rounds" section.

## Patch 26: review subagents experiment only in their own copy; Implementers confirm each push (`agentic-review/`, `implement/`, `implement-spec/`)

Why: issue #104 (absorbs Retro issues #60 and #63). A Finder that ran `git checkout <sha>` in the shared tree left it on a detached HEAD under the Implementer, and in two threads an Implementer's fix commit landed off the branch and its `git push` sent nothing.

What:

- `agentic-review/FINDERS.md`: the shared brief list gains a **copy rule** bullet, pasted into every Finder's brief: to try something out, work in your own copy (`git archive <head> | tar -x -C <a new scratch directory>` or a throwaway `git worktree`); never run `git checkout`, `switch`, `stash` or `reset` in the shared tree; leave it on its branch, clean.
- `agentic-review/VERIFY.md`: the Verifier brief gains the same copy rule, in the same words, as the paragraph before its answer-format paragraph (the brief's closing line is guarded by check 38).
- `implement/SKILL.md` (step 3): the Implementer brief gains a bullet: before each push, check `git status -sb` shows the Ticket branch; after it, report `git rev-parse origin/<branch>` equals `HEAD`. Step 4 checks that report.
- `implement-spec/SKILL.md`: the Ticket-branch Implementer brief (step 3) gains a bullet to check `git status -sb` shows its Ticket branch before each commit (it never pushes); the Spec-branch Implementers (step 6.1's merge-and-resolve one and step 7's fix one) are briefed to run the same push check as `implement`.
- `scripts/check-plugin.sh`: new check 30 (review-own-copy: `FINDERS.md` and `VERIFY.md` keep the copy rule: own copy, `git archive`, `git worktree`, and the ban on `checkout`, `switch`, `stash` and `reset` in the shared tree, and leaving it on its branch). The Implementer's push check is not scripted.
- `.claude-plugin/plugin.json`: version 0.18.0 to 0.19.0.

Merging an Upstream update: take Upstream's `FINDERS.md`, `VERIFY.md`, `implement` and `implement-spec` text, then re-apply the bullets above.

## Patch 27: `handoff` saves where the next agent can read it (`handoff/`)

Why: issue #109 (absorbs #35). `handoff` wrote to the OS temp directory, which in a cloud or remote session is that session's own container; no other thread, session or project can open it. In two threads the handoff went to the tracker or the project's shared files instead.

What:

- `handoff/SKILL.md`: "Save to the temporary directory of the user's OS (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows) - not the current workspace." is now a save-location rule. By default the handoff is an issue on the tracker `docs/agents/issue-tracker.md` names, linked from the work it continues; with no tracker configured the skill says so and asks the user for a location. A shared folder is used only when the user names one; the temp directory only when the next agent runs on the same machine; the skill ends by telling the user where the handoff is (issue link or path). The suggested skills section, the no-duplication rule, redaction and arguments are unchanged. Patch 21's edit to the `description` needed no change.
- `ask-matt/SKILL.md` and `ask-matt/PHASE-BOUNDARIES.md` (Upstream text): where they called a handoff a "portable markdown file" ("open a fresh session against that file", "a file that travels"), they now say it is a document the next agent can read (a tracker issue by default), a session that reads the handoff, and a document that travels. The portability point is unchanged.
- `scripts/check-plugin.sh`: new check 31 (handoff-location: `handoff/SKILL.md` keeps the tracker default, shared folder only when the user names one, temp directory only when the next agent runs on the same machine, the ask when no tracker is configured and the closing report of the location, and no longer makes the temp directory the default).
- `.claude-plugin/plugin.json`: version 0.19.0 to 0.20.0.

Merging an Upstream update: take Upstream's `handoff`, `ask-matt/SKILL.md` and `ask-matt/PHASE-BOUNDARIES.md` text, then re-apply the save-location rule above (check 31 lists its phrases) and the `ask-matt` and `PHASE-BOUNDARIES` wording edits listed above.

## Patch 28: `grilling` states a rule's purpose and checks a recommendation's facts; `grill-with-docs` gathers what other skills expect (`grilling/`, `grill-with-docs/`)

Why: issue #108, absorbing Retro issues #80 and #81. A question about a rule went out without saying what the rule is for, a recommendation went out on unchecked facts, and `grilling`'s fact-finding line was read as too soft to count as the skill asking for a subagent.

What:

- `grilling/SKILL.md`: after "Word each question so "yes" accepts your recommended answer." two paragraphs are added: a question that changes or extends an existing rule opens, before the options, with one line saying what the rule does today and why it exists, citing the ADR or doc; and a recommendation that rests on a fact nobody has checked waits for that fact, or is marked as a guess. After "don't ask the user for anything you could look up yourself." a sentence says a fact-finding sub-agent counts as this skill asking for a sub-agent, however light the lookup looks; a few greps do not replace it. The 3-question round format is unchanged.
- `grill-with-docs/SKILL.md`: a closing paragraph says that when the plan renames or reworks a skill, the first fact to gather is what every other skill expects of that skill.
- `scripts/check-plugin.sh`: new check 32 (grilling-facts: one distinctive phrase per new sentence plus two clause pins, so a revert fails: five on `grilling` for the rule purpose, citing the ADR or doc, the checked-fact-or-marked-guess rule, the sub-agent counting as asked for, and a few greps not replacing it; one on `grill-with-docs`).
- `.claude-plugin/plugin.json`: version 0.20.0 to 0.21.0.

Merging an Upstream update: take Upstream's `grilling` and `grill-with-docs` text, then re-apply the edits above.

## Patch 29: `agentic-review` returns design Findings to the user as grilling (`agentic-review/`, `implement/`, `implement-spec/`)

Why: issue #112 (absorbs #43). On two pull requests that changed design (#37's ADR, and #83, a Ticket that also edited ADR 0007), the thread fixed Findings that questioned the design by writing new rules into the ADR, which the user had never agreed. For code the thread fixes Findings; for design the decisions are the user's.

What:

- `agentic-review/ROUNDS.md`: the Round loop's "fixed and committed by whoever owns the code" paragraph gains a sentence pointing to a new section, `## Design Findings go to the user`, placed after the Round loop. On a pull request that changes design (adds or edits an ADR, the glossary, a spec or a design doc), each Important and "fix" Nit is sorted as design (a Finding that questions the design; when unsure, design) or text (wording, citations and index lines included, fixed as usual). Design Findings go to the user as grilling questions, each with a recommended answer, at most 3 at a time, until the user says nothing more is worth settling; only the agreed answer is committed, and the next Round reviews it. A design kept as it is makes the Finding `dismissed`. Waiting on answers is not a Round. An agreed answer that changes the pull request gets one more Round within the 5-Round cap, even after a clean Round (a design "fix" Nit goes to the user, not into the unreviewed last commit); at Round 5 it is committed and the pull request goes to the user, saying plainly that the change is unreviewed. When the user keeps the design on every open design Finding, the Round counts as clean. The rule also covers Ticket checks. The Round loop's clean "Round 2 to Round 5" bullet gains a sentence pointing to this.
- `implement/SKILL.md` (step 6) and `implement-spec/SKILL.md` (steps 5 and 7): the sentence that sends Findings to the Implementer gains a parenthesis: design Findings go to the user first, linking the new section. In `implement` step 6 and `implement-spec` step 7, the clean-Round "final "fix" Nits commit" sentence is followed by "An agreed answer to a design Finding that changes the pull request gets one more Round instead."
- `docs/adr/0003-code-review-runs-find-verify-rank-in-rounds.md` (ours, not Upstream text): its Rounds section gains a paragraph recording the rule, the extra Round for an agreed change, the Round 5 path and the all-kept clean Round; its Rank stage, clean test, clean-Round bullet and Round 5 bullet gain the same short exceptions.
- `agentic-review/ROUNDS.md`, outside the new section: Rank step 2's "already dismissed" parenthesis, the clean-Round test in the Round loop, the Nit status bullet ("is `dismissed` once the user keeps the design") and the Ticket checks section's "stay open until confirmed fixed" also accept a design Finding the user settled by keeping the design (`dismissed`, not left open or posted `fixed`); the clean test also says a design Finding raised this Round that the user kept counts as no new Important; the Round 1 bullet says it leads to Round 2 even when the user keeps the design on every design Finding. Inside the section, once the user answers, the thread edits that Round's own comment, or a Ticket check's, with `gh api -X PATCH` or the GitHub tool it has (a comment not posted yet is posted already settled): kept rows become `dismissed`, the `<n> Important open` count is recounted, and from Round 2 on `Result:` becomes `clean` if none is left; and the all-kept case counts as clean only when no other Important is open, from Round 2 on.
- `agentic-review/SKILL.md` (step 1): Ticket-check Importants stay open until confirmed fixed, "or until they are dismissed because the user kept the design".
- `retro/BUG-CLASSES.md` (ours, not Upstream text): step 2 keeps `dismissed` rows whose Note says "user keeps the design", since they were real.
- `docs/adr/0004-build-threads-coordinate-and-subagents-code.md` (ours, not Upstream text): the Fixes bullet and the Ticket-check bullet say design Findings go to the user first.
- `scripts/check-plugin.sh`: new check 33 (design-findings: `ROUNDS.md` has the section heading and its key phrases, including the Round 5 "saying plainly that the change is unreviewed", "the Round counts as clean" and "edit that Round's own comment", and at least 3 links to the section in the file (the Nit status bullet, the Round loop's fixes paragraph and its clean "Round 2 to Round 5" bullet); `implement/SKILL.md` links it at least once and `implement-spec/SKILL.md` at least twice, for steps 5 and 7).
- `.claude-plugin/plugin.json`: version 0.21.0 to 0.22.0.

Merging an Upstream update: take Upstream's text, then re-append the section to `ROUNDS.md`, re-add the two pointer sentences to its Round loop (after the fixes paragraph and on the clean "Round 2 to Round 5" bullet), the "user kept the design" clauses (Rank step 2, the clean test, Nit status, the Round 1 bullet, Ticket checks, and `SKILL.md` step 1), and in `implement` and `implement-spec` the three parentheses and the two "one more Round instead" sentences. Check 33 fails if the section heading or one of its key phrases is missing, if `ROUNDS.md` has fewer than 3 links to the section, or if `implement` has fewer than 1 or `implement-spec` fewer than 2; it does not check the "user kept the design" clauses.

## Patch 30: `to-tickets` and `wayfinder` offer `setup-project` only for a new repo, kind of thread or standing rule (`to-tickets/`, `wayfinder/`)

Why: issue #142 (absorbs #120 and #121). `setup-project` now writes how the project works and never the state of its work (open specs, the map), so a new spec or map is no reason to offer it.

What:

- `to-tickets/SKILL.md` (step 6) and `wayfinder/SKILL.md` ("Offer `setup-project`"): the list of what counts as a change to what threads need drops "a new spec or map to point at" (wayfinder: "a new map to point at" and "(when the way to the destination is now clear) build threads to start"); it is now only a new repo, a new kind of thread or a new standing rule. Both still name `` `setup-project` `` (check 10).
- `scripts/check-plugin.sh`: new check 34 (setup-project-state: `setup-project/SKILL.md` tells the coordinator to find open specs, plannings and tickets on the tracker, asks for the tier-to-model map, carries the rule to start each thread on its tier's model, no longer links the map or open specs or says "pointers stay current", and names no vendor model; `to-tickets` and `wayfinder` no longer offer it for a new spec or map).
- Our own text, not Upstream: `setup-project/SKILL.md`, `setup-dev-skills/SKILL.md` (offers `setup-project` only if the project's instructions do not yet cover the repo), the plugin `README.md` and ADR 0004.
- `.claude-plugin/plugin.json`: version 0.22.1 to 0.22.2.

Merging an Upstream update: carry Upstream's changes to both files over by hand and re-apply the narrowed list above.

## Patch 31: `codebase-design` drops the survey trigger; `ask-matt` says where a prototype lives (`codebase-design/`, `ask-matt/`)

Why: issues #92 and #133 (bundled in #145). `codebase-design`'s description claimed "find deepening opportunities", which belongs to `improve-codebase-architecture`, so both skills matched that request. `ask-matt` justified the prototype detour's `/handoff` with "a prototype lives in its own directory", while `prototype` commits it to a throwaway branch.

What:

- `codebase-design/SKILL.md`: the description loses "find deepening opportunities".
- `ask-matt/SKILL.md` (step 2 of the idea flow): "a prototype lives in its own directory" becomes "a prototype is a side task forked mid-phase, with its code on a throwaway branch out of main", matching `prototype/SKILL.md` and the Phase boundaries text.
- Not Upstream text: `GLOSSARY.md` gains **Question round** (the "round" of `grilling` and `triage`, so none of those skills changed) and its **Review** entry names the two `agentic-review` entry points, a pull request and a diff since a fixed point; the heading `## Not a Patch: retro-planning...` gains a blank line before it.
- `.claude-plugin/plugin.json`: version 0.22.2 to 0.22.3.

Merging an Upstream update: take Upstream's text, then drop "find deepening opportunities" from the `codebase-design` description again and re-apply the `ask-matt` wording.

## Patch 35: the Ticket thread never moves the Implementer's checkout (`implement/`, `implement-spec/`)

Why: issue #155 (absorbs Retro issue #135; follows Patch 26). The Ticket thread and its Implementer shared one checkout, and the thread's `git checkout origin/<branch>` to read a head for a Round left it detached: the Implementer's fix was committed off the branch and its push said "Everything up-to-date" (PR #119, again in PR #131). Patch 26 fenced off the review subagents and added the Implementer's push check, but not the thread.

What:

- `implement/SKILL.md` (step 2): the thread makes the Ticket branch in its own git worktree, outside its checkout (`git worktree add <path> -b <ticket-branch> origin/main`) and pushes it from there; its own checkout stays where it was.
- `implement/SKILL.md` (step 3): the Implementer brief gains the worktree path and that it works only there, and that the worktree may need its dependencies installed again. The "keep this same Implementer" paragraph says it keeps the same worktree for every later fix, merge of main and numbering, the handoff names the worktree, and a reclaimed machine means making the worktree again. A new paragraph says the thread never runs `git checkout`, `switch` or `reset` in that worktree, and reads a head by `git fetch` plus `git show` or `git diff`, or a `git archive` copy. Patch 26's push check is unchanged.
- `implement/SKILL.md` (steps 4, 5, 6, 7.2, 9): the checks rerun in the worktree, by a subagent that runs no git command that moves it; step 5 opens the pull request (the branch is already pushed); step 6 runs `agentic-review` from the worktree with read-only git commands, so its `HEAD` is the Ticket branch's head; the retro check's Implementer gets its own worktree as in step 2. `implement-spec/SKILL.md` step 10's retro check line says the same, with its branch pushed. Both briefs tell the Implementer to run every git command as `git -C <path> ...`, and the Review's Finders and Verifiers get the worktree path to do the same; `implement`'s reclaim path runs `git worktree prune` first. The new and edited lines name the default branch as `origin/<default-branch>`, not `origin/main`, and the reclaim and "never pushed" notes no longer assume a cloud environment. The thread runs its own Review git commands as `git -C <path> ...` too. The retro check's Implementer is briefed as in step 3 of `implement`, in both skills (it is a lone pull request off main whose branch is pushed), not as in `implement-spec` step 3.2.
- `implement-spec/SKILL.md`: checked for the same gap. Its ticket worktrees are already made by the thread, but nothing said how it reads a head without moving one. Step 2 adds `switch` and `reset` to the commands the Spec thread runs in its own checkout while an Implementer works there, and says to read a head with fetch plus `git show` or `git diff`, or a `git archive` copy; step 3 says the same of the ticket worktrees.
- `scripts/check-plugin.sh`: new check 40 (ticket-thread-keeps-out-of-worktree: `implement` keeps the worktree step and the ban on `checkout`, `switch` and `reset` in it, with `git archive`; `implement-spec` keeps the same ban for ticket worktrees).
- `.claude-plugin/plugin.json`: version 0.22.8 to 0.22.9.

Merging an Upstream update: `implement` and `implement-spec` are already replaced whole by Patches 8 and 11, so re-apply the lines above after carrying Upstream's changes over.

## Patch 33: the numbering step retakes numbers when main moves again (`implement/`, `implement-spec/`)

Why: issue #154 (absorbs #67 and #127). After the first numbering pass no `TBD-N` is left, so "repeat steps 1 and 2" had nothing to replace and never said to move numbers already real; Implementers renumbered only when the thread messaged them the new numbers, and one pass left a stale cross-reference.

What:

- `implement/SKILL.md` step 7.2 and `implement-spec/SKILL.md` step 8.2: "If main moves again before the merge, repeat steps 1 and 2" now continues: on a repeat no `TBD-N` is left, so the Implementer retakes every number the branch took under the repo's rules (such as the version and the numbers of the new entries its diff against main adds) as if afresh on top of main's current numbers: each at the next free one in the same order, counting the ones it has just moved (a number already the next free one stays), and a version above main's; it rewrites the branch's own cross-references to a changed number from the old-to-new list (in the pull request body too); its report names each old and new number, or says none changed.
- `.claude-plugin/plugin.json`: version 0.22.6 to 0.22.7.

Merging an Upstream update: re-apply the repeat sentence at the end of the "Take the numbers" step in both skills.

## Patch 34: skill text cites no ADR number of this repo, does not say "Upstream", and leaves this repo's own merge rule to its `CLAUDE.md` (`implement/`, `implement-spec/`, `retro/`, `domain-modeling/`)

Why: issue #177. Every project that loads the plugin reads its skill text, and in another repo "ADR 0004" names another decision or nothing, and "Upstream" is a word only this repo's glossary defines. The merge list in `implement` and `implement-spec` likewise named the `agentic-review` skill, whose source is changed only in this repo; the user chose to move that rule to this repo's `CLAUDE.md`.

What:

- `implement/SKILL.md` and `implement-spec/SKILL.md` (opening paragraph): drop "(ADR 0004)" and "(ADR 0004, ADR 0005)".
- `retro/BUG-CLASSES.md` (opening paragraph): drop "(ADR 0003)".
- `domain-modeling/SKILL.md` ("Splitting the glossary") and `domain-modeling/GLOSSARY-FORMAT.md` (two places): "Upstream's multi-context layout" / "repos" and "an Upstream multi-context repo" become "a multi-context layout", "multi-context repos" and "a multi-context repo".
- Our own text, not Upstream: `setup-dev-skills/SKILL.md` says it is derived from Matt Pocock's setup skill instead of "Our own skill, derived from Upstream's setup skill".
- `scripts/check-plugin.sh`: new check 39 (repo-free-skill-text: no `ADR NNNN` and no capitalised `Upstream` in `*.md` and `*.yaml` under `upstream-skills/` and `skills/`; an example docs index line linking its own ADR file is exempt).
- `implement/SKILL.md` (step 7) and `implement-spec/SKILL.md` (step 8): the list of when the pull request goes to the user drops "or the `agentic-review` skill", whose source is changed only in this repo, and gains "or anything else the repo's own rules (its `CLAUDE.md`, the project instructions, its docs) say a person merges". Not Upstream text: this repo's `CLAUDE.md` gains the `agentic-review` rule, and ADR 0004 says the same in the paragraph after its list.
- `.claude-plugin/plugin.json`: version 0.22.7 to 0.22.8.

Merging an Upstream update: take Upstream's text, then drop any ADR citation it adds (Upstream's own ADR numbers mean nothing here either); check 39 fails until it is gone.

## Not a Patch: `setup-dev-skills` seed text (issue #144)

Our own, not Upstream. The `setup-dev-skills` skill's `SKILL.md` step 1 names both remote URL forms, the GitHub seed gives REST routes for pull requests and open blockers, and the seed files name skills without a leading slash.

- `.claude-plugin/plugin.json`: version 0.22.0 to 0.22.1.

## Not a Patch: `check-plugin.sh` gives the same result however it runs, and catches numbering and name drift

Our own, not Upstream; no Upstream text changed. Why: issue #143 (absorbs #130, #76, #123, #78, #61 and #62). Under `bash -e` the script exited 123 with no output (the no-match `grep` in the vendor-name check aborted it); through a symlink it looked for the plugin tree next to the link; two Patches could share a number; a "new check N" line could point at another check's number without check 21 noticing; and nothing compared a skill's `name:` or `display_name` with its folder.

What (all in `scripts/check-plugin.sh` and this file; no skill text changed):

- The script sets `set +e` after `set -u`, so `bash -e` and `SHELLOPTS=errexit` give the same output and exit code as a plain run (every failure goes through `bad()`; a no-match `grep` is an answer, not an error). It resolves its own path with plain `readlink`, one symlink hop at a time (absolute or relative links, chains), not the GNU-only `readlink -f`; running by real path is unchanged.
- Every check header now reads `# N. <name>: <description>`, and every "new check N" line in this file reads "new check N (<name>...". Check 21 compares the pairs: a "new check" line whose number and name match no header fails, even when that number is named elsewhere; a header without a name fails; a "new check" mention without a name fails; a pair claimed twice fails, and so does a number claimed twice under different names (two branches adding different checks with the same number) or two headers sharing a number (`2` and `2b` are different header numbers; for the pairs, `2b` is written as `2`). A `TBD-N` placeholder is exempt from those two number rules, since several new checks in one pull request share it, but a placeholder pair (same name) claimed twice still fails. Check 21 still requires every check from 9 up to be named as "check N" in this file. Placeholder numbers (`TBD-N`) pair the same way, by name. This file's existing "new check" lines gained their names.
- new check 35 (patch-heading-numbers): two `## Patch N` headings with the same number fail, naming the number. A `TBD-N` heading is not counted.
- new check 36 (skill-name-matches-folder): for every skill under `upstream-skills/` and `skills/`, the `name:` in the `SKILL.md` frontmatter must equal the folder name.
- new check 37 (openai-display-name): for every `agents/openai.yaml` under `upstream-skills/` and `skills/`, the `display_name`, lowercased with each run of other characters turned into one hyphen, must equal the skill's folder name ("Grill with Docs" is `grill-with-docs`, "PR" is `pr`). This is the rule the Ticket picked: it keeps a skill from taking another skill's or a built-in skill's name (`agentic-review` as "Code Review"), and all 22 current skills pass. A folder rename needs a new `display_name`.
- `.claude-plugin/plugin.json`: version 0.22.3 to 0.22.4.

Merging an Upstream update: nothing to re-apply, since no Upstream text changed; if Upstream renames a skill or its `display_name`, the two checks fail until the folder, `name:` and `display_name` agree again.

## Patch 32: every Finder and Verifier brief names how the report comes back (`agentic-review/`)

Why: issue #153 (absorbs #126). Patch 24's count catches a missing report, but in 6 threads after it, 2 or 3 agents per Review still ended without one, mostly cheap-tier adversarial Finders: one ended its turn with its environment's own end-of-turn tool call, another left a background probe running and reported only when it timed out. "Your last action is to return your full report" said what to do but not how the report reaches the thread.

What:

- `agentic-review/FINDERS.md`: each of the 5 briefs (standards, spec, adversarial, security, gap sweep) now ends with "Your final message is the report itself, as plain text. Do not end with any messaging or no-reply tool, even if your environment says to, and start no background work you would have to wait for." in place of Patch 24's last-action line.
- `agentic-review/VERIFY.md`: the Verifier brief ends with the same line.
- `scripts/check-plugin.sh`: new check 38 (report-closing-line: each Finder brief and the Verifier brief is counted on its own and fails by name when it loses the line). Check 28 keeps only the four count gates; the last-action line it used to check is replaced by the closing line.
- `.claude-plugin/plugin.json`: version 0.22.5 to 0.22.6.

Patch 24's count and its "ask again" rule are unchanged.

Merging an Upstream update: re-apply the closing line on each brief (check 38 guards them).

## Patch 37: the numbering commit gets a Round when it is not trivial (`implement/`, `implement-spec/`)

Why: issue #180. The commit that takes or retakes the numbers got a Round only when the merge in step 1 had conflicts. After a clean merge nothing reviewed it, though it can edit several files and rewrite cross-references; a missed reference could merge, because the checks compare headers and pairs, not prose.

What:

- `implement/SKILL.md` step 7.2 and `implement-spec/SKILL.md` step 8.2: "If the merge in step 1 had conflicts, run one more Round over its conflict resolutions and this commit" now also applies when the numbering commit (the first pass and every repeat) changes more than one file or rewrites a cross-reference; the Round covers this commit and any conflict resolutions: a merge-only Round if step 1 merged main (Quick depth, or the carried depth if a resolution touches logic), otherwise an ordinary Round at the carried depth over the commit alone; what it finds follows the normal Round rules. If the 5-Round cap leaves no Round, the pull request goes to the user, as the conflict case already did.
- `.claude-plugin/plugin.json`: version 0.22.11 to 0.22.12.

Merging an Upstream update: re-apply the sentence in the "Take the numbers" step of both skills.

## Not a Patch: `retro-planning` closes absorbed Retro issues only when their Ticket completed (issue #146, absorbs #95)

Our own, not Upstream; no Upstream text changed. `skills/retro-planning/SKILL.md` treats an absorbed Retro issue as closing with its Ticket, or as a failed-fix candidate, only when the Ticket closed as completed; a Ticket closed any other way (not planned, duplicate, abandoned) leaves the issue in the backlog with its votes, and step 2 marks that Ticket "not fixed". ADR 0007 step 4 and the plugin README say the same.

- `.claude-plugin/plugin.json`: version 0.22.4 to 0.22.5.

## Patch 36: a Round's diff after a merge from main, per-file line numbers, and Pre-existing filing data (`agentic-review/`, `implement/`, `implement-spec/`)

Why: issue #147 (absorbs #124, #98 and #73). A Round 3 to 5 pinned `git diff <last-head>..HEAD`, which after a merge from main holds every commit main brought in, so Finders could raise Findings on code main had already reviewed; only `implement-spec` step 7 said to review the resolutions alone. In the eval runs for #27, two Verifiers "corrected" Locations to line numbers counted across their own concatenated listing of several files. And the filing step asked for each Pre-existing location's claim, failure scenario and evidence, while the Round comment, the only record a fresh session has, carried only a one-line Note.

What:

- `agentic-review/SKILL.md` (step 1): the Round 3 to 5 bullet says that when the new commits include a merge from main (`git log --merges`), the diff is `git log -p --first-parent --remerge-diff <last-head>..HEAD`, which shows each new commit and, for the merge, only its conflict resolutions, and the Finders are told so. This is the one place the diff rule lives. The skill's opening Pull request bullet adds "(for a merge from main, only what it changed in the pull request)" after "Rounds 3 to 5 review only the commits added since the last Round".
- `agentic-review/FINDERS.md`: the shared brief's diff bullet adds the sentence the Finders get when a Round's new commits include a merge from main: review every new commit as the diff shows it, and for the merge only what it changed in the pull request. The Finding format's Locations line says each line is counted within its file at the Review's head (as `grep -n` gives it), never a position in the diff output or a listing of several files.
- `agentic-review/VERIFY.md`: the Verifier brief's call 1, after "Fix the Locations list...", says every location is `file:line` counted within that file at the Review's head, never a line of the diff output or of a listing, and a Location changes only when the Finder's line is wrong in the file itself.
- `agentic-review/ROUNDS.md`: "Merge-only Rounds" drops its own `git show --remerge-diff <merge>` example and points to `SKILL.md` step 1. The Note bullet says a Pre-existing row's Note gives its claim and failure scenario in short; the example table's Pre-existing row does so. "Filing Pre-existing Findings" says the filing session takes claim, failure scenario and evidence from the Review's own Findings when it still has them, otherwise the claim and scenario from the Note and the evidence by quoting the code at the locations.
- `implement/SKILL.md` (step 6) and `implement-spec/SKILL.md` (step 7): the "Before each Round" paragraph says that in a Round that reviews only the new commits, the merge counts among them: the Round reviews each new commit and, for the merge, only what it changed in the pull request, not the commits from main; it points to `agentic-review` step 1 for the diff and the Finders' line (`implement-spec` drops its own `--remerge-diff` example and "say so to the Finders"; `implement`'s "so the Round reviews the resolutions" goes).
- `scripts/check-plugin.sh`: new check 41 (review-diff-and-lines: `agentic-review`'s `SKILL.md` keeps `--remerge-diff` and "not the commits that came in from main", `FINDERS.md` the merge sentence ("for the merge only what it changed") and the per-file line rule, `VERIFY.md` the per-file line rule and "only when the Finder's line is wrong", `ROUNDS.md` the Pre-existing Note and "from its Note"; `implement` and `implement-spec` link `agentic-review/SKILL.md#1-pin-the-diff`).
- Not Upstream text: `GLOSSARY.md`'s **Round** entry adds the same parenthesis to its commit Rounds.
- `.claude-plugin/plugin.json`: version 0.22.9 to 0.22.10.

Merging an Upstream update: take Upstream's text, then re-apply the step 1 merge clause and the opening bullet's parenthesis, the Finder sentence, the two line-counting rules, the Note and filing sentences and the example Note, and in `implement` and `implement-spec` the pointer to `agentic-review` step 1. Check 41 lists the phrases.

## Not a Patch: the skill evals move out of the plugin to `evals/` (issue #195)

Our own, not Upstream; no Upstream text changed and no skill text changed (no skill points at the evals). The evals folder moves out of the plugin directory (`plugins/dev-skills/`) to `evals/` at the repo root, so the evals are no longer shipped in the plugin and only fit this repo. Older entries in this file that name `evals/<skill>/` mean that folder as it was inside the plugin directory; it is now at the repo root. `docs/index.md`, the plugin `README.md` folder tree and the fixture `README.md` follow. The repo's `CLAUDE.md` says a change that touches only `evals/` is not a plugin change. This move still bumps the plugin version, because `README.md` and this file are under `plugins/`.

- `.claude-plugin/plugin.json`: version 0.22.12 to 0.22.13.

## Not a Patch: the GitHub tracker seed gets REST routes (issues #160, #161)

Our own, not Upstream; no Upstream text changed. `skills/setup-dev-skills/issue-tracker-github.md` writes a REST route (`gh api repos/<owner>/<repo>/...`) next to every `gh issue` command that lacked one (create, read, list, comment, labels, close, assign yourself, and the wayfinding map, Frontier query, Claim and Resolve), leads the fork check with the REST route, and tidies the opening paragraph so it no longer says both that the subcommands fail and that REST works. The blocker rule now says a ticket is unblocked when every blocker is closed by a merged change, with the by-hand check for a blocker closed without a merge. `implement` and `implement-spec` are unchanged.

- `.claude-plugin/plugin.json`: version 0.22.13 to 0.22.14.

## Patch 38: `ask-matt` routes to `setup-project`, `diagnosing-bugs` stops calling debug harnesses prototypes (`ask-matt/`, `diagnosing-bugs/`)

Why: issues #164 and #167. `ask-matt` described `setup-dev-skills` but had no entry for `setup-project`, so a user asking which skill writes a project's instructions got no answer. `diagnosing-bugs`' cleanup checklist told the agent to delete "throwaway prototypes", while `prototype` keeps its code as a primary source on a throwaway branch.

What:

- `ask-matt/SKILL.md` (Precondition): a `setup-project` entry after the `setup-dev-skills` one, in the same style.
- `diagnosing-bugs/SKILL.md` (Phase 6): "Throwaway prototypes deleted" becomes "Debug harnesses and scratch code deleted".
- Not Upstream text: `GLOSSARY.md`'s **Finder** and **Severity** entries drop the pull-request wording, and a new **Door** entry is added.
- `.claude-plugin/plugin.json`: version 0.22.14 to 0.22.15.

Merging an Upstream update: re-apply the `setup-project` entry and the checklist wording.

## Vendor model names in Upstream text

None in the kept skills at the Base commit, so no Patch was needed for ADR 0002 (checked for ticket #4: grep for `haiku`, `sonnet`, `opus`, `claude-`, `gpt-`, `gemini` over `upstream-skills/`). Some kept skills start subagents (for example `grilling`, `wayfinder`, `code-review`, `implement-spec`), but none picks a model for them. Spec #1 adds tiers in later tickets (the `code-review` Finders and Verifiers, and the `implement` and `implement-spec` Implementers; the tier on each ticket from `to-tickets` is Patch 7, the `implement` Implementer's tier is Patch 8, and the `implement-spec` Implementers' tiers are Patch 11); each of those edits gets its own Patch here.

`scripts/check-plugin.sh` now runs the vendor-name grep over `upstream-skills/` too, so an Upstream merge that brings in a model name fails the check and must be patched to a tier.

## Not a Patch: `setup-dev-skills` writes a starter `REVIEW.md` (issue #188)

Our own, not Upstream; no Upstream text changed. `skills/setup-dev-skills/` gains the seed `review.md` (the three sections `retro` creates: what Important means with the default applying, Skip, and an empty Always check list). `SKILL.md` explores for an existing `REVIEW.md`, asks whether the repo has rules of its own for the build threads (recorded in its `CLAUDE.md`, `AGENTS.md` or `REVIEW.md`, never in skill text), drafts the file in the draft-and-diff step, and, on a first run or a re-run alike, never drafts the seed over an existing one: nothing in it is removed or rewritten, and a missing section is offered alone as a diff. The `docs/index.md` it writes lists `REVIEW.md`. The plugin `README.md` line for the skill names the starter `REVIEW.md`.

- `scripts/check-plugin.sh`: new check 42 (setup-review-seed: the seed has the three sections and an empty list, and `SKILL.md` links it and says the repo's own rules never go into skill text).
- `.claude-plugin/plugin.json`: version 0.22.10 to 0.22.11.
