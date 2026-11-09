Below is the full draft of the Orchard project instructions. I wrote no files and sent nothing.

Three facts shaped it:
- **Orchard is inside a Milestone.** The Boundary record's label form (`milestone-<n>`) finds an open Milestone agreement. So the draft keeps only Orchard's own choices and points to the Boundary record and the skills for the rest.
- **The coordinator cannot load the plugin's skills.** It said so itself. So the draft copies "The loop" from `team-lead`'s `DELIVERY-LOOP.md` word for word, and never tells the coordinator to run `milestone`, `team-lead` or `release`.
- **No custom tier-to-model map**, so the draft adds none.

---

```markdown
# Orchard project instructions

Orchard is built in one repo, orchard-team/orchard. Build threads start at [docs/dev-skills/index.md](docs/dev-skills/index.md); the repo's rules are in [CLAUDE.md](CLAUDE.md).

When you need open specs, plannings, tickets or the Milestone issue, look them up on the tracker: GitHub Issues in orchard-team/orchard, the only tracker. [docs/dev-skills/issue-tracker.md](docs/dev-skills/issue-tracker.md) documents it. What needs the user's approval, the check-in interval and the Milestone label form are in the Boundary record, [docs/dev-skills/boundaries.md](docs/dev-skills/boundaries.md).

## Delivery loop

You cannot load the plugin's skills. Start a thread for each step below that names a skill, and never do that step yourself. A brief carries the skill, the issue link, the Milestone issue link and the Model tier (regular when the issue names none), and you start the thread on the model the project's instructions map to that tier, or the worker tool's default model when they give none. At every wake (a worker's report or end, a check-in, the user writing), read the tracker and each worker's state from the tool that runs your workers, then take every step that applies, in order. Start none whose thread is already running or whose result already stands:

1. Once Milestone planning has settled, and no Startup verification thread is running or Verdict recorded on the Milestone issue, start a thread that runs `milestone`'s Startup verification, with `worker-control`'s check run by the agent the skill names. Start no Build thread until the result on the Milestone issue reads `Verdict: ready`, or the user says to go on.
2. With no current Release (an open release issue naming this Milestone, whose label an issue carries), no Release thread running, and at least one planned feature that is open, not parked, carries no release label and is unblocked, start a Release thread that runs `release` to plan one.
3. Start Build threads only for issues carrying the current Release's label, in the release issue's Order, up to the project's thread limit and the Milestone's order rule, and start none while a Release thread runs. A Spec with Tickets runs `implement-spec`, a Spec without Tickets runs `to-tickets` first, and a lone Ticket runs `implement`.
4. When every issue carrying the current Release's label is closed and no Release thread is running, start a Release thread that runs `release` to cut it, run `triage` and `retro-planning`, and plan the next Release.
5. When every feature is merged or parked and no report thread is running or report written, start a thread that runs `milestone` to write its report, then stop for the user's Milestone review.

(Loop copied from `team-lead`'s DELIVERY-LOOP.md on main; last change to `team-lead` or `milestone`: 4f2c9e1.)

## Orchard's own rules

- **Thread limit:** at most two Build threads at once.
- **Order:** when a backend issue and a dashboard issue are both eligible to start, start the backend one first.
- **Schema migrations:** the user merges any pull request that contains a schema migration. Every Build brief says so: the thread hands that pull request to the user, says plainly that the user must merge it, and does not merge it itself.
- **Merge-time steps:** when a thread asks for a version number before merging a pull request that changes a file under `agent-skills/`, or reports such a merge, follow CLAUDE.md's "Version hand-out" and "Re-read after a skill merge". Start no further thread until the re-read is done.
```

---

There are three points to check before you approve. I didn't add anything for them.

1. **Model tiers.** Because there is no custom map, the loop says to use the worker tool's default model. The coordinator can't load `model-tiers`, so cheap and premium briefs will probably run on the default model too. If you want each tier to run on its own model, add a map now. The plugin's default for Claude Code is: cheap = <model>, regular = <model>, premium = <model>.
2. **Check-ins.** The copied loop wakes on check-ins but says nothing about setting one up. `team-lead`'s rule for arranging one doesn't reach a coordinator that can't load skills. The Boundary record's 45-minute interval won't run unless a thread is told to arrange it, or you add a line here.
3. **Where the loop text came from.** CLAUDE.md says skills in this repo follow the checkout's `agent-skills/<name>/` on main, not the installed copy. I copied the loop from the installed plugin, which is at main's version of the repo its manifest names. I couldn't confirm that this repo is orchard-team/orchard. If it isn't, compare the loop with `agent-skills/team-lead/DELIVERY-LOOP.md` on Orchard's main before saving.

You can edit the draft freely. Once you approve the full text in your own message, I'll send exactly that text to the coordinator to save.
