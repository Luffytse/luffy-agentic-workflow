I've reviewed this re-run against setup-project's rules. You're inside a Milestone and the coordinator can load `team-lead`, `milestone`, `release` and `worker-control`, so the new text only points to the skills that own the shared rules. It keeps your project-specific choices and drops the work-status lines. I wrote no files and sent nothing.

## New project instructions (full text)

> You coordinate Orchard in orchard-team/orchard. Build threads start from [docs/dev-skills/index.md](docs/dev-skills/index.md) and [CLAUDE.md](CLAUDE.md). The project uses GitHub Issues only, documented in [docs/dev-skills/issue-tracker.md](docs/dev-skills/issue-tracker.md). Find the open Milestone, Releases, specs and tickets there when you need them.
>
> Run `milestone` for the Milestone and `team-lead` for its delivery. Boundaries, the check-in interval and the budget are in the Boundary record, [docs/dev-skills/boundaries.md](docs/dev-skills/boundaries.md).
>
> Project rules:
> - Run at most two Build threads at once. Where a backend feature and a dashboard feature are both eligible, start the backend one first.
> - The user merges schema migrations.
> - Brief every worker to send an explicit completion callback to you when it finishes.
> - Archive each worker once it has finished.
> - After every merge, pull main and reload any changed skills.

## Diff against the existing text

```diff
-You coordinate Orchard in orchard-team/orchard. Use GitHub Issues, documented in docs/dev-skills/issue-tracker.md, and start from docs/dev-skills/index.md and CLAUDE.md.
+You coordinate Orchard in orchard-team/orchard. Build threads start from docs/dev-skills/index.md and CLAUDE.md. The project uses GitHub Issues only, documented in docs/dev-skills/issue-tracker.md. Find the open Milestone, Releases, specs and tickets there when you need them.
+
+Run `milestone` for the Milestone and `team-lead` for its delivery. Boundaries, the check-in interval and the budget are in the Boundary record, docs/dev-skills/boundaries.md.
+
+Project rules:
-Run at most two Build threads at once, backend before dashboard where both are eligible.
+- Run at most two Build threads at once. Where a backend feature and a dashboard feature are both eligible, start the backend one first.
-Spec threads run implement-spec and Ticket threads run implement.
-Brief every build with its skill, issue, Milestone issue and Model tier; name Review level only if requested.
-Start on the tier's mapped model.
-Group planned features into Releases.
-Check in every 45 minutes and nudge silent workers, then confirm a stop before taking over.
-User approval is needed for production deploys; budget is 100 credits.
-User merges schema migrations.
+- The user merges schema migrations.
-Hand out versions just before merge where PRs bump.
-Pull main and reload changed skills after every merge.
-Re-read open Tickets after each skill merge.
-Run retro after a finished build.
-Workers must send explicit completion callbacks; archive finished workers.
+- Brief every worker to send an explicit completion callback to you when it finishes.
+- Archive each worker once it has finished.
+- After every merge, pull main and reload any changed skills.
-Current Milestone is #7; build #31 next; #32 is blocked.
```

## What was cut and where it lives now

- **Work status** ("Milestone #7, build #31 next, #32 blocked"): removed. The instructions never hold work status; the coordinator reads it from GitHub Issues.
- **Which skill each thread kind runs, what a brief carries, starting each thread on its tier's model:** these are `team-lead`'s "Start work" rules. You have no custom tier-to-model map, so nothing is added for tiers.
- **Grouping features into Releases:** owned by `release`, which `team-lead` starts.
- **Check-ins, nudging silent workers, confirming a stop before taking over:** these are in `team-lead`. The 45-minute interval comes from the Boundary record.
- **Production deploy approval and the 100-credit budget:** both are in the Boundary record.
- **Handing out versions before merge, re-reading open Tickets:** `team-lead` runs these merge-time steps from the repo's own docs (CLAUDE.md, release.md), so they go through that pointer.
- **Retro after a finished build:** dropped, because your confirmed list has no other additions. If the instruction is still needed, it should live in a skill or repo doc, not here.

**Kept as project-specific:** the two-thread limit and backend-first order, the schema-migration merge gate, completion callbacks, archiving finished workers, and pulling main and reloading skills after merges. `team-lead` and `milestone` don't cover any of these.

**One thing to consider (no change made):** `milestone` says an action the user wants to keep for themselves belongs in the Boundary record. If you'd like the schema-migration gate there next to production deploys, it can move there through `setup-dev-skills`, and this line would then go.

**No delivery loop is included,** because the coordinator reported that it can load the skills.

Please approve the full text above in your own message, or tell me what to edit. Once you approve, I'll send exactly that text to the coordinator to save.
