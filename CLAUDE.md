# luffy-agentic-workflow

A Claude Code and Codex plugin marketplace, named `luffy-agentic-workflow`, holding one plugin, `dev-skills`, under `plugins/dev-skills/`. Both catalogs, `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`, list only `dev-skills`. This repo is public; its history was rewritten when it left the private archive `Luffytse/luffy-dev-skills` (ADR 0014).

- `dev-skills`: the development skill set used across projects, skills that began as Matt Pocock's, now our own, plus our own review pipeline. See `docs/dev-skills/adr/`.

Words used here (Finder, Verifier, Finding, Bug class, Review level, Model tier and so on) are defined in `docs/dev-skills/glossary.md`. Decisions are in `docs/dev-skills/adr/`. Start at `docs/dev-skills/index.md`, which says which doc to read for what.

## Working rules

- Skills name a **model tier** (cheap, regular, premium), never a vendor's model name, because other coding agents may load these plugins. See `docs/dev-skills/adr/0002-skills-name-model-tiers-not-models.md`.
- Rules that only fit this repo live here and never in skill text, because every project that loads the plugin reads the skills. A Harness limit is not a repo rule: it goes in `worker-control`'s Harness reference, not here. A format the plugin ships is fixed in the plugin, not only in this repo's copy.
- A change that touches only `evals/` (the skill evals, at the repo root, outside the plugin) is not a plugin change: it changes no skill and takes no version bump.
- A pull request that changes skill text or `evals/` is tested as `docs/dev-skills/evals.md` says (ADR 0013): its `**Eval:**` line names the kind of change, and a behaviour change runs the skill's eval cases on its own skill and on main's before it merges.
- Every pull request that changes a file under `plugins/dev-skills/skills/` bumps the `dev-skills` version: major for a breaking change, minor for a new or changed skill, patch for a fix or a revert (ADR 0008; 1.0.0 since 2026-11-04). During review the branch leaves the version as it is on main. The bump is this repo's merge-time step, not a skill's: see "Merge-time steps" below. `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` keep the same version, and the bump changes both together. Any other pull request, under `plugins/<name>/` or not, leaves the version as it is on main; its plugin files ride along with the next bump. A bad merged skill change is reverted on main at once, and the revert takes the next number. A Release here opens no bump pull request. A new check in `scripts/check-plugin.sh` takes a name, not a number: the check's `# <name>: <description>` header. `scripts/check-plugin.sh` is this repo's own tooling, outside the plugins: editing it changes no plugin, and the CI workflow line that runs it is committed by the user by hand.
- `release` reads this repo's bump mode ("pull requests bump") and Release name from `docs/dev-skills/release.md`.
- When a `dev-skills` skill runs in this repo, follow the checkout's copy (`plugins/dev-skills/skills/<name>/`) on main, not the installed one, because main may be ahead of the installed plugin cache. A pull request that changes a skill is reviewed with main's version of that skill unless the pull request says otherwise.
- Before each push, search the edited file and repository for the changed rule's key terms. For a Shared rule, update its owner, consumers, record shapes and descriptions together, including any unmigrated shared copies. Independent policies may differ. For every changed rule, also resolve contradictions in parallel sentences within the skill and stale repository descriptions in the glossary, ADRs, index, READMEs and checker messages. An "as in step N" reference imports every bullet of that step: read it in the caller's context. Update related text in the same commit; a miss found after pushing gets a new commit. `REVIEW.md` checks the same consistency boundary.
- Run `claude plugin validate .` (Claude Code's checker for plugin files) before pushing a change to a plugin or to `marketplace.json`. Run `scripts/run-tests.sh` (every `test*` file under `evals/` and `scripts/`) before pushing a change under `evals/` or `scripts/`.

## Merge-time steps

Skills tell a thread to follow the merge-time steps the repo's own docs give. These two are this repo's, for this period, and no skill states them. The coordinator (the user, when no coordinator runs) follows them; `docs/dev-skills/release.md` has the record forms.

**Version hand-out.** A thread about to merge a pull request that changes a file under `plugins/dev-skills/skills/` asks the coordinator for its version number just before merging; a pull request that changes no such file gets none and merges with no bump.
- The coordinator gives the number: main's version (the `version` field of `plugins/dev-skills/.claude-plugin/plugin.json`, freshly fetched), raised minor for a new or changed skill and patch for a fix or a revert (ADR 0008). It records the number first, in a comment on the issue the pull request builds (a Spec pull request: the Spec; a pull request that builds no issue: the pull request itself), then tells the thread. The thread adds the bump as the pull request's last commit and merges.
- If the coordinator cannot write to the tracker, it gives the number in a message and the asking thread writes the record in its place, as soon as it gets the number and before it merges, on the same issue or pull request, naming the coordinator as the giver and the time of the hand-out; "one at a time" reads it like any other record (record form: `docs/dev-skills/release.md`).
- A record under the earlier marker `<!-- milestone version hand-out -->` counts as a hand-out record too.
- Skill-changing pull requests merge one at a time. A number is **out** while main's version has not reached it, its pull request is open and the thread it was given to is running. While one is out the coordinator gives none: it records the request as waiting and tells the thread to wait. At the first wake with no number out, it gives numbers to the waiting requests in the order they asked. A number is void, not out, when its pull request closed unmerged or is parked or its thread has ended.
- A thread that asks again because main's version moved under it gets a new number from the new main, recorded the same way; its earlier record is void.
- While the user's pause is in effect the coordinator gives no number: it records a request as waiting and tells the thread to wait. A number already out stays out and its merge may finish.
- The coordinator serves waiting requests at any wake, a check-in included, not only on a merge report: a number can go void with no report.
- After the merge the coordinator reads the version on main. If it is not the number given, it gives no further number and tells the merging thread to put main right first.

**Ticket re-read after a skill merge.** Right after a pull request that changed a file under `plugins/dev-skills/skills/` merges, and before any further thread starts, the coordinator re-reads the open issues that no running thread is building and whose body names the changed skill or a changed file (inside a Milestone, only those carrying its membership label). Each is read against main's new text of the skill, with one of three outcomes:
- the change makes it wrong or incomplete: update the issue (read the whole body, write it whole back with only that change and a one-line note naming the merge, read it back); a change that would alter a Milestone's agreement (goal, acceptance or exclusions) goes to the user as one question and that feature waits for the answer;
- the change makes it obsolete: close it with a note naming the merge;
- otherwise: comment that it was re-read after the merge and still fits.

Then it reads the blockers again and takes the next start from what they now say. A running thread keeps the skill version it started with until its Ticket or Spec is done. The coordinator may hand the re-read to a `triage` thread, briefed with the merge, the changed skill, main's version and the issues, and start nothing further until it reports.

## Agent skills

Start at `docs/dev-skills/index.md`; it says which doc to read for what.

### Issue tracker

Issues and specs live in this repo's GitHub Issues. See `docs/dev-skills/issue-tracker.md`.

### Triage labels

5 state roles + 2 category roles: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`, `bug`, `enhancement`; plus the `next-release` role and the optional agent-only role, mapped to `claude-only` and `codex-only` (an agent that sees the other agent's label leaves the issue alone); and a Repo labels table, empty here, that `triage`, `to-spec`, `to-tickets` and `review-rounds` apply (builders read none). See `docs/dev-skills/triage-labels.md`.

### Domain docs

Single-context: one `docs/dev-skills/glossary.md` and `docs/dev-skills/adr/`. See `docs/dev-skills/domain.md`.

### Boundaries

The agreed boundary: nothing needs the user's approval, no budget, one-hour check-ins, Milestone label `milestone-<n>`. The `merging` skill, which `implement`, `implement-spec` and `release` load at their merge step, reads it for every pull request, inside a Milestone or not: a pull request crossing no boundary is an agent merge, Deep and ADR, glossary, `CLAUDE.md`, `AGENTS.md` and `REVIEW.md` changes included, unless the repo's own rules say a person merges it (a review still open after Round 3 sorts its open Importants into bug Tickets, not brought to the user), and no Boundary record means an empty one (ADR 0004). See `docs/dev-skills/boundaries.md`.

### Releases

`dev-skills`' canonical version source is `plugins/dev-skills/.claude-plugin/plugin.json`; `plugins/dev-skills/.codex-plugin/plugin.json` keeps a synchronized version copy; a skill-changing pull request bumps the version and a Release does not; a Release is named, not numbered, with the label `release-m<milestone>-r<n>`, and its changelog entry records its start and end commits and the versions it delivered. See `docs/dev-skills/release.md`.
