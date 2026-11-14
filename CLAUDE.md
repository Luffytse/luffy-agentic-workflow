# luffy-agentic-workflow

A Claude Code plugin marketplace, named `luffy-agentic-workflow`, holding one plugin, `dev-skills`, under `plugins/dev-skills/`. Its catalog, `.claude-plugin/marketplace.json`, lists only `dev-skills`. The plugin is Claude Code only for now (ADR 0001). This repo is public; its history was rewritten when it left the private archive `Luffytse/luffy-dev-skills` (ADR 0014).

- `dev-skills`: the development skill set used across projects, skills that began as Matt Pocock's, now our own, plus our own review pipeline. See `docs/dev-skills/adr/`.

Words used here (Finder, Verifier, Finding, Bug class, Review level, Model tier and so on) are defined on the Area pages that `docs/dev-skills/glossary.md` maps. Decisions are in `docs/dev-skills/adr/`.

## Working rules

- Skills name a **model tier** (cheap, regular, premium, top), never a vendor's model name, because other coding agents may load these plugins. See `docs/dev-skills/adr/0002-skills-name-model-tiers-not-models.md`.
- Rules that only fit this repo live here and never in skill text, because every project that loads the plugin reads the skills. A Harness limit is not a repo rule: it goes in `worker-control`'s Harness reference, not here. A format the plugin ships is fixed in the plugin, not only in this repo's copy.
- A pull request that changes skill text merges when it shows three things (ADR 0015): **CI is green** (the plugin checker, `claude plugin validate .` and the script tests), **the review is done** as `REVIEW.md` says, and **each acceptance line of the issue it builds is shown as met** in the pull request body, one line of evidence per line (a word count, a word diff against the inherited text, a search that finds nothing, a script test).
- No model eval is run in this repo: the evidence that skill text works is the acceptance lines shown in the pull request. A gap a real project finds in a skill comes back as a Retro issue.
- A Retro issue that Retro planning handed to triage and whose fix is in a skill is triaged by one more rule here, which wins over `triage`'s general rule for a handed-over Retro issue. When the fix repairs a **broken** skill, agents build it: `ready-for-agent` with a brief. Broken means the skill does not do what its own text, this repo's docs or a recorded decision say: a script fails, two sentences contradict each other, or a parser rejects the format the skill tells agents to write. When the fix changes what a skill tells agents to do (the skill does what it says, and the Retro wants it to say something else, or to say something where it is silent today), it is not built: triage leaves it at `ready-for-human` with a comment that it waits for the user's next Milestone planning. A fix in this repo's tooling, docs or CI, and a Harness fact, follow the general rule. The rule is here and in no skill because only this repo receives `skill` Retros from every project, and the skills change only when the user plans it (ADR 0007's amendment).
- A pull request never changes the `dev-skills` version, a skill pull request included: it leaves the version as it is on main, asks nobody for a number and merges like any other (this repo has no merge-time steps of its own). The Release's changelog pull request raises it once, in `.claude-plugin/plugin.json`, by the biggest size among the Release's changes: major for a breaking change, minor for a new or changed skill, patch for fixes or reverts only (ADR 0016; 1.0.0 since 2026-11-04). A bad merged skill change is reverted on main at once. A new check in `scripts/check-plugin.sh` takes a name, not a number: the check's `# <name>: <description>` header. `scripts/check-plugin.sh` is this repo's own tooling, outside the plugins: editing it changes no plugin, and the CI workflow line that runs it is committed by the user by hand.
- The **Environment check** (`docs/dev-skills/environment-check.md`) is this repo's own test of the `worker-control` references; no skill names it. It runs at each Milestone's end, after the last Release is cut and before the Milestone report, once in the cloud project and once in a local Claude Code session run through a session on the user's machine; when that machine cannot be reached the local half is reported as not run and nothing waits. A pull request that changes a `worker-control` reference runs the rows its change touches, in the environment that reference describes, before the merge, and shows them in the pull request body with any row it could not run named. The result is one comment on the Milestone issue headed "Environment check", linked from the Milestone report. A failed row is filed as a bug naming the reference line it disproves; it does not hold the report back.
- `release` reads this repo's Release name and cut steps, the version bump among them, from `docs/dev-skills/release.md`.
- When a `dev-skills` skill runs in this repo, follow the checkout's copy (`plugins/dev-skills/skills/<name>/`) on main, not the installed one, because main may be ahead of the installed plugin cache. A pull request that changes a skill is reviewed with main's version of that skill unless the pull request says otherwise.
- Before each push, search the edited file and repository for the changed rule's key terms. For a Shared rule (`docs/dev-skills/shared-skill-rules.md` holds how this plugin shares one), update its owner, consumers, record shapes and descriptions together, including any unmigrated shared copies. Independent policies may differ. For every changed rule, also resolve contradictions in parallel sentences within the skill and stale repository descriptions in the glossary, ADRs, index, READMEs and checker messages. An "as in step N" reference imports every bullet of that step: read it in the caller's context. Update related text in the same commit; a miss found after pushing gets a new commit. `REVIEW.md` checks the same consistency boundary.
- When a plan renames or reworks a skill, the first fact to gather is what every other skill expects of that skill (what they call it, load it for, or rely on it to do).
- Run `claude plugin validate .` (Claude Code's checker for plugin files) before pushing a change to a plugin or to `marketplace.json`. Run `scripts/run-tests.sh` (every `test*` file under `scripts/`: this repo's tooling tests and the tests of the scripts the plugin ships) before pushing a change under `scripts/` or to a script the plugin ships.

## Skills this repo uses

- The whole flow is used: the planning, Milestone, Release, build, review, merge, retro and triage skills.
- A change to skill text or docs is built without `tdd`: edit, check the acceptance lines, review. No test is written that searches for a sentence.
- A change to a script (the scripts the plugin ships, such as `review_briefs.py` and `snapshot.py`, and this repo's own tooling under `scripts/`) is built with `tdd` and a script test under `scripts/`.
- A change that mixes both kinds follows both lines.
- `codebase-design`, `improve-codebase-architecture`, `prototype`, `diagnosing-bugs` and `wizard` run only when the user asks for them.

## Agent skills

Start at `docs/dev-skills/index.md` and open only the docs whose line fits your work.

### Issue tracker

Issues and specs live in this repo's GitHub Issues. See `docs/dev-skills/issue-tracker.md`.

### Triage labels

5 state roles + 2 category roles: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`, `bug`, `enhancement`; plus the `next-release` role; and a Repo labels table, empty here, beside the rule that `triage`, `to-spec`, `to-tickets` and `review-rounds` apply (builders read none). See `docs/dev-skills/triage-labels.md`.

### Domain docs

Single-context: one glossary, split into Area pages behind the map `docs/dev-skills/glossary.md`, and one `docs/dev-skills/adr/`. See `docs/dev-skills/domain.md`.

### Boundaries

The agreed boundary: nothing needs the user's approval, no budget, one-hour check-ins, Milestone label `milestone-<n>`. The `merging` skill, which `implement`, `implement-spec` and `release` load at their merge step, reads it for every pull request, inside a Milestone or not: a pull request crossing no boundary is an agent merge, Deep and ADR, glossary, `CLAUDE.md`, `AGENTS.md` and `REVIEW.md` changes included, unless the repo's own rules say a person merges it (a review still open after Round 3 sorts its open Importants into bug Tickets, not brought to the user), and no Boundary record means an empty one (ADR 0004). See `docs/dev-skills/boundaries.md`.

### Releases

`dev-skills`' canonical version source is `plugins/dev-skills/.claude-plugin/plugin.json`; no pull request changes the version and the Release's changelog pull request raises it once, by the biggest size among its changes, merged by the Release thread; a Release is named, not numbered, with the label `release-m<milestone>-r<n>`, and its changelog entry records its start and end commits and the version it delivered (or that the version stayed). See `docs/dev-skills/release.md`.
