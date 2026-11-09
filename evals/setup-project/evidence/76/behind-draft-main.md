I've written the full draft below. **I don't recommend approving it as it stands.** The plugin this thread runs from is out of date, and the delivery-loop text the draft copies has since been removed from the source repository's main.

## Before you approve: the plugin is behind main

- **Version gap.** This thread runs plugin 2.3.0. The source repository's main is at 2.4.0, and its last change to `team-lead` or `milestone` is commit `4f2c9e1`.
- **The loop is gone on main.** Because the coordinator can't load the plugin's skills, my copy of `setup-project` says to copy "The loop" from `team-lead/DELIVERY-LOOP.md` word for word, and the draft does that. Main no longer has that file. Main's `team-lead` now says only that such a coordinator "follows the project instructions `setup-project` writes for it". Main's `setup-project` isn't readable here, so I can't tell what text it would write instead.
- **Main changed the Release rule.** On main, a Release thread starts when no open, unparked issue still carries the current Release's label. That thread then decides whether to cut the Release or plan the next one. Main also adds a `wait` record when a cut is blocked or nothing could be planned, and Build order skips issues that no longer carry the Release label. The copied loop (steps 2 and 4) only starts a cut once every issue in the Release is closed. So a Release with a parked issue would never be cut, and delivery would stall there.
- **What I recommend:** update the plugin cache to 2.4.0 and re-run this draft from main's `setup-project`. Startup verification's "Loaded skill version" check would fail in this environment for the same reason.

## Draft project instructions (Orchard)

```markdown
# Orchard project instructions

Repo: orchard-team/orchard. Build threads start at [docs/dev-skills/index.md](docs/dev-skills/index.md).
Repo rules and merge-time steps: [CLAUDE.md](CLAUDE.md). Boundaries, check-in interval and the
Milestone label form: [docs/dev-skills/boundaries.md](docs/dev-skills/boundaries.md).

Find the open Milestone issue, Releases, specs and tickets on the tracker when you need them:
GitHub Issues on orchard-team/orchard, documented in
[docs/dev-skills/issue-tracker.md](docs/dev-skills/issue-tracker.md).

## The loop

You cannot load the plugin's skills. Start a thread for each step below that names a skill, and never do that step yourself. A brief carries the skill, the issue link, the Milestone issue link and the Model tier (regular when the issue names none), and you start the thread on the model the project's instructions map to that tier, or the worker tool's default model when they give none. At every wake (a worker's report or end, a check-in, the user writing), read the tracker and each worker's state from the tool that runs your workers, then take every step that applies, in order. Start none whose thread is already running or whose result already stands:

1. Once Milestone planning has settled, and no Startup verification thread is running or Verdict recorded on the Milestone issue, start a thread that runs `milestone`'s Startup verification, with `worker-control`'s check run by the agent the skill names. Start no Build thread until the result on the Milestone issue reads `Verdict: ready`, or the user says to go on.
2. With no current Release (an open release issue naming this Milestone, whose label an issue carries), no Release thread running, and at least one planned feature that is open, not parked, carries no release label and is unblocked, start a Release thread that runs `release` to plan one.
3. Start Build threads only for issues carrying the current Release's label, in the release issue's Order, up to the project's thread limit and the Milestone's order rule, and start none while a Release thread runs. A Spec with Tickets runs `implement-spec`, a Spec without Tickets runs `to-tickets` first, and a lone Ticket runs `implement`.
4. When every issue carrying the current Release's label is closed and no Release thread is running, start a Release thread that runs `release` to cut it, run `triage` and `retro-planning`, and plan the next Release.
5. When every feature is merged or parked and no report thread is running or report written, start a thread that runs `milestone` to write its report, then stop for the user's Milestone review.

## Orchard's own rules

- Thread limit: at most two Build threads at once.
- Order: where a backend issue and a dashboard issue are both eligible to start, start the backend one first.
- Schema migrations: the user merges any pull request with a schema migration. Tell its thread to leave
  the merge to the user and say so plainly.
- Merge-time steps: when a thread asks or reports at a merge, take the coordinator steps CLAUDE.md gives
  ("Version hand-out", "Re-read after a skill merge") as it states them.
```

## Notes on the draft

- **Left out on purpose.** The 45-minute check-in, production-deploy approval and the `milestone-<n>` label are kept only in the Boundary record, which the draft links. There is no tier-to-model map because you have no custom one, so threads start on the worker tool's default model. If you want each tier on its own model, the plugin's Claude Code default map is cheap→<model>, regular→<model>, premium→<model>, and I can add it.
- **Merge-time pointer.** A coordinator without the skills would never be told to read CLAUDE.md's merge-time steps, so the draft adds one line pointing to them rather than restating them.
- **Schema migrations.** This is a boundary. `milestone` says actions reserved for you belong in the Boundary record (changed with `setup-dev-skills`), not in project instructions. Moving it there would let every thread see it. It stays in the draft for now because you confirmed it.
- **Check-in gap.** The copied loop never tells the coordinator to set up the 45-minute check-in. I didn't write my own wording for that, because the skill says the loop is copied unchanged.

Nothing has been written or sent. Do you want to approve this text, edit it, or (as I recommend) update to 2.4.0 and re-draft first?
