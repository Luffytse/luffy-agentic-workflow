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

Open point: the 12 skills above have human-facing one-line descriptions with the trigger lists stripped (Upstream's rule for user-invoked skills). They are now model-invoked but their descriptions do not say when to fire. Rewriting them is not part of this Patch. `implement` (Patch 8) and `implement-spec` (Patch 11) now have agent-facing descriptions that say when to use them; the other 10 still have Upstream's.

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

- `retro/SKILL.md`: new step 3, "If the session reviewed or built a pull request with `code-review` Rounds (or the user names one), turn its repeated Bug classes into checks: [BUG-CLASSES.md](BUG-CLASSES.md)."; Upstream's steps 3 and 4 become 4 and 5; the new step 5 (Upstream's "Present these candidates to the user, in order of severity.") gains the sentence "Report repeated Bug classes as done, with the link to the retro's pull request." Every other line is Upstream's.
- New `retro/BUG-CLASSES.md` (ours, not Upstream): reads every Round and Ticket-check comment of a pull request, merges them into one row per Finding id, groups by Bug class, and for each repeated class repairs an existing guardrail, adds a deterministic check, or adds a `REVIEW.md` Always-check line; the changes go in their own pull request, which a person merges when it touches `REVIEW.md`.
- `scripts/check-plugin.sh`: `retro/BUG-CLASSES.md` joins the `writers` list of check 7; new check 9 (`BUG-CLASSES.md` exists, `retro/SKILL.md` links it, `BUG-CLASSES.md` and `code-review/ROUNDS.md` both contain the `<!-- code-review kind=round` and `<!-- code-review kind=ticket-check` markers, `BUG-CLASSES.md` mentions `REVIEW.md`).
- `.claude-plugin/plugin.json`: version 0.4.0 to 0.5.0.

Merging an Upstream update: carry Upstream's `retro/SKILL.md` changes over by hand and re-apply the step 3 insertion and the step 5 sentence.

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
- `scripts/check-plugin.sh`: new check 10 (both `to-tickets` templates carry a `**Model tier:**` line; `to-tickets` and `wayfinder` both name `` `setup-project` ``).
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
- `scripts/check-plugin.sh`: new check 11 (`implement/SKILL.md` names `` `tdd` ``, `` `pr` `` and `` `code-review` ``, says Implementer, and says squash).
- `.claude-plugin/plugin.json`: version 0.6.0 to 0.7.0.

Merging an Upstream update: Upstream's `implement/SKILL.md` is replaced whole, so diff Upstream's old and new text and carry any change over by hand into the step it maps to above (ticket fetching into step 1, building advice into the Implementer's brief in step 3, review into step 6). Keep Patch 4's reader line and the words check 11 looks for.

## Patch 9: `code-review` applies `REVIEW.md`'s Always check lines (`code-review/`)

Why: issue #23. `retro` (Patch 6) turns repeated judgement Bug classes into Always check lines in `REVIEW.md`, but Patch 5's briefs only told Finders and Verifiers to apply `REVIEW.md`'s skip list, so nothing made a Review check those lines. The check goes to the standards Finder because it runs at every depth, a Ticket check included; the other Finders still get `REVIEW.md`.

What:

- `FINDERS.md`: the standards Finder is also given the new `REVIEW.md` Always check section when `REVIEW.md` has at least one Always check line (else (d) is dropped from the brief); its brief, the Upstream standards prompt as Patch 5 left it, gains "(d) every `REVIEW.md` Always check line the diff breaks, reported once under (d) and not again under (a)"; new section "`REVIEW.md` Always check" after "Docs index drift": check every line against the whole diff (the whole pull request in Rounds 3 to 5), one Finding per broken line under the Bug class the line names, and a closing `clear`-or-Finding list of every line.
- `VERIFY.md`: the Verifier is told `REVIEW.md` comes with its Always check lines, and that a Finding raised from one is real when the code breaks that line as written.
- `SKILL.md` step 2: "always-check list" became "Always check list", and the `REVIEW.md` paragraph says the standards Finder checks each Always check line, linking the new `FINDERS.md` section.
- `scripts/check-plugin.sh`: new check 12 (`FINDERS.md`, `VERIFY.md` and `SKILL.md` mention Always check; `FINDERS.md` has the section).
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
- `scripts/check-plugin.sh`: new check 13 (`ask-matt/SKILL.md` must not say "same context window" or "two-axis", and must mention Rounds).
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
- `scripts/check-plugin.sh`: new check 14 (`implement-spec/SKILL.md` names `` `tdd` ``, `` `pr` `` and `` `code-review` ``, says Implementer, `git worktree add` and merge commit, and does not say "integration branch"; `ask-matt/SKILL.md` does not say "integration branch").
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

## Patch 13: `retro` files its suggestions as Retro issues; `triage` skips them (ADR 0007)

Why: ADR 0007 and issue #40. Upstream's `retro` hands every suggestion to the user in its report, where it is read once and lost. Suggestions that are not repeated Bug classes now become Retro issues, or "seen again" votes on open ones, so a backlog can show which problems repeat. `triage` must skip them, since they carry no `needs-triage` label and would look untriaged.

What:

- `retro/SKILL.md`: new step 5, "File every candidate that is not a repeated Bug class as a Retro issue, or vote on an open one that covers it, and check whether Retro planning is due: [FILING.md](FILING.md)."; Patch 6's step 5 (Upstream's "Present these candidates...") becomes step 6 and gains "For each other candidate, give the issue it went to; add the due notice from step 5 when it applies." Every other line is as Patch 6 left it.
- New `retro/FILING.md` (ours, not Upstream): routing (skill or workflow problems to the repo in the plugin manifest's `repository` field, a project's own problems to its tracker from `docs/agents/issue-tracker.md`, else the `origin` remote), votes (`Seen again in <thread link>`), the `retro` label and `Retro:` title, the can't-write fallback, the thresholds (10 open; 2 weeks with at least 4 open) and the trigger clock from the newest closed `retro-planning` record, and what the report lists.
- `triage/SKILL.md`: in "Show what needs attention", a sentence after the three buckets, "Skip issues labelled `retro`: they are Retro issues, planned in batches, not untriaged work."; in "Triage a specific issue or PR" step 1, a leading sentence "If the issue is labelled `retro`, stop: it is a Retro issue, planned in batches, so skip it." before "Read the full". Every other line is Upstream's.
- `scripts/check-plugin.sh`: new check 15 (`plugin.json` has a `repository` GitHub URL; `retro/FILING.md` exists, `retro/SKILL.md` links it, and it names `retro`, `Retro:`, "seen again" and `retro-planning`; `triage/SKILL.md` skips `retro`; no forked or own skill text names a project, repo or person).
- `.claude-plugin/plugin.json`: version 0.8.1 to 0.8.2, and a new `repository` field.

Merging an Upstream update: carry Upstream's `retro/SKILL.md` and `triage/SKILL.md` changes over by hand and re-apply the lines above.

## Patch 14: `implement` and `implement-spec` end by running `retro` (ADR 0004, ADR 0007)

Why: issue #42. Each build thread knows its own Review, so it ends by running `retro` on itself and every build feeds the Retro backlog. The build thread still writes no code: a check the retro proposes is built by an Implementer.

What:

- `implement/SKILL.md`: new step 9, "Run the retro", after the report. `implement-spec/SKILL.md`: new step 10, "Run the retro", after "Clean up and report". Each says: run `retro` on the thread whether the pull request was merged or handed to the user; for a repeated Bug class, a regular-tier Implementer builds the check on a branch off main, and the thread opens the pull request with `pr`, runs the `code-review` Rounds and merges it as a lone pull request (squash-merge, or brings it to the user); a check that changes `REVIEW.md` goes to the user; add the outcome to the report. Every other line is as Patches 8 and 11 left it.
- `scripts/check-plugin.sh`: new check 16 (the last step of both skills names `` `retro` `` and `REVIEW.md`).
- `.claude-plugin/plugin.json`: version 0.8.2 to 0.8.3.

Merging an Upstream update: both `SKILL.md` files are already replaced whole by Patches 8 and 11, so after carrying Upstream's changes over, re-append the final retro step and keep it last, since check 16 reads the last `## ` section.

## Vendor model names in Upstream text

None in the kept skills at the Base commit, so no Patch was needed for ADR 0002 (checked for ticket #4: grep for `haiku`, `sonnet`, `opus`, `claude-`, `gpt-`, `gemini` over `upstream-skills/`). Some kept skills start subagents (for example `grilling`, `wayfinder`, `code-review`, `implement-spec`), but none picks a model for them. Spec #1 adds tiers in later tickets (the `code-review` Finders and Verifiers, and the `implement` and `implement-spec` Implementers; the tier on each ticket from `to-tickets` is Patch 7, the `implement` Implementer's tier is Patch 8, and the `implement-spec` Implementers' tiers are Patch 11); each of those edits gets its own Patch here.

`scripts/check-plugin.sh` now runs the vendor-name grep over `upstream-skills/` too, so an Upstream merge that brings in a model name fails the check and must be patched to a tier.
