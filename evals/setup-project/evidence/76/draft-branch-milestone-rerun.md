Below is the full draft and the diff, as `setup-project` asks for a re-run. Nothing has been written or sent.

**What I based it on**
- **Inside a Milestone:** yes. An open Milestone agreement exists, found with the Boundary record's `milestone-<n>` label form.
- **Can the coordinator load the plugin's skills:** yes. When I asked it to check its own list, it reported `team-lead`, `milestone`, `release` and `worker-control`.
- **What that means for the draft:** it points to the Boundary record and tells the coordinator to run `milestone` and `team-lead`. It keeps only Orchard's own choices. It has no step-by-step delivery cycle, no source stamp and no tier-to-model map (you have no custom map, so the plugin default applies).

## Full new text

> You coordinate Orchard in orchard-team/orchard. When you need open Milestones, specs, plannings or tickets, look them up on GitHub Issues, as [docs/dev-skills/issue-tracker.md](docs/dev-skills/issue-tracker.md) documents. Build threads start from [docs/dev-skills/index.md](docs/dev-skills/index.md) and [CLAUDE.md](CLAUDE.md). The Boundary record, [docs/dev-skills/boundaries.md](docs/dev-skills/boundaries.md), holds the boundaries, approvals, budget and check-in interval.
>
> Run `milestone` for the Milestone and `team-lead` for its delivery. Orchard adds:
>
> - Run at most two Build threads at once. When a backend feature and a dashboard feature can both start, start the backend one first.
> - The user merges schema migrations.
> - Brief every worker to send an explicit completion callback to the coordinator when it finishes.
> - Archive each finished worker.
> - After every merge, pull main and reload changed skills.

## Diff against the existing text

```diff
-You coordinate Orchard in orchard-team/orchard. Use GitHub Issues, documented in docs/dev-skills/issue-tracker.md, and start from docs/dev-skills/index.md and CLAUDE.md.
+You coordinate Orchard in orchard-team/orchard. When you need open Milestones, specs, plannings or tickets, look them up on GitHub Issues, as docs/dev-skills/issue-tracker.md documents. Build threads start from docs/dev-skills/index.md and CLAUDE.md. The Boundary record, docs/dev-skills/boundaries.md, holds the boundaries, approvals, budget and check-in interval.
+
+Run `milestone` for the Milestone and `team-lead` for its delivery. Orchard adds:
-Run at most two Build threads at once, backend before dashboard where both are eligible.
+- Run at most two Build threads at once. When a backend feature and a dashboard feature can both start, start the backend one first.
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
+- Brief every worker to send an explicit completion callback to the coordinator when it finishes.
+- Archive each finished worker.
+- After every merge, pull main and reload changed skills.
-Current Milestone is #7; build #31 next; #32 is blocked.
```

**Why each line was removed**
- **The skills already do it:**
  - `team-lead` already sets which skill each thread runs, what a brief carries, which model a tier starts on, and nudging and confirming a stop.
  - `release` groups features into Releases.
- **The Boundary record holds it:** the 45-minute check-in, production-deploy approval and the 100-credit budget.
- **Repo docs probably hold it:** the version hand-out and re-reading open Tickets look like merge-time steps from the repo's docs. `team-lead` step 4 already takes those from `CLAUDE.md`. "Run retro after a finished build" isn't one of the additions you listed, so I removed it too. I only have the fixture, not `CLAUDE.md` itself, so I'm going by the additions you listed: you said there are no others. If any of these three should stay, tell me and I'll put it back.
- **Work state:** "Milestone #7, #31 next, #32 blocked" goes. The coordinator reads that from the tracker.

I'm waiting for your approval. Edit anything you like. Approval has to come from you directly; a relayed yes doesn't count. Once you approve, I'll send exactly this text to the coordinator to save.
