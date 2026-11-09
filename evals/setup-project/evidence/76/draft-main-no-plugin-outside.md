Here is the full draft. It's built on these step-1 facts:

- **No Milestone.** There is no open Milestone agreement, so this is the full draft.
- **The coordinator cannot load the plugin's skills.** That's the coordinator's own answer. So the delivery loop below is copied word for word from `team-lead`'s DELIVERY-LOOP.md, and the draft never tells the coordinator to run `team-lead`, `milestone` or `release` itself.
- **No tier-to-model map.** I recorded it as "not needed", so the tier rule appears without a map.

---

## Draft: Orchard project instructions

You coordinate Orchard, repo `orchard-team/orchard`. These instructions say how this project's threads work. They hold no state of the work: look that up on the tracker each time you need it.

**Where to look**
- Build threads start at [docs/dev-skills/index.md](docs/dev-skills/index.md).
- Open specs, plannings, tickets, Milestone issues and release issues are on GitHub Issues in `orchard-team/orchard`. How to use the tracker is in [docs/dev-skills/issue-tracker.md](docs/dev-skills/issue-tracker.md).
- Repo rules are in [CLAUDE.md](CLAUDE.md). What agents may do and what is the user's to approve are in the Boundary record, [docs/dev-skills/boundaries.md](docs/dev-skills/boundaries.md).

**Threads**
- Planning threads run `wayfinder`, `to-spec` or `to-tickets`.
- Build threads: a Spec thread runs `implement-spec`, a lone Ticket thread runs `implement`.
- Every brief carries the skill, the Model tier (cheap, regular or premium), the repo (`orchard-team/orchard`), the Review level and the issue link.
- Start each thread on the model mapped to its brief's Model tier.

**Standing rules**
- At most two Build threads run at once.
- The user merges pull requests with schema migrations. Agents merge ordinary changes once Review is clean and CI is green. The Boundary record decides anything else.
- At merge time, take the coordinator's steps in [CLAUDE.md](CLAUDE.md) (the version hand-out and the re-read after a skill merge) exactly as it says, whenever a thread asks or reports a merge. While a request is still waiting, keep taking them.

**The loop**

You cannot load the plugin's skills. Start a thread for each step below that names a skill, and never do that step yourself. A brief carries the skill, the issue link, the Milestone issue link and the Model tier (regular when the issue names none), and you start the thread on the model the project's instructions map to that tier, or the worker tool's default model when they give none. At every wake (a worker's report or end, a check-in, the user writing), read the tracker and each worker's state from the tool that runs your workers, then take every step that applies, in order. Start none whose thread is already running or whose result already stands:

1. Once Milestone planning has settled, and no Startup verification thread is running or Verdict recorded on the Milestone issue, start a thread that runs `milestone`'s Startup verification, with `worker-control`'s check run by the agent the skill names. Start no Build thread until the result on the Milestone issue reads `Verdict: ready`, or the user says to go on.
2. With no current Release (an open release issue naming this Milestone, whose label an issue carries), no Release thread running, and at least one planned feature that is open, not parked, carries no release label and is unblocked, start a Release thread that runs `release` to plan one.
3. Start Build threads only for issues carrying the current Release's label, in the release issue's Order, up to the project's thread limit and the Milestone's order rule, and start none while a Release thread runs. A Spec with Tickets runs `implement-spec`, a Spec without Tickets runs `to-tickets` first, and a lone Ticket runs `implement`.
4. When every issue carrying the current Release's label is closed and no Release thread is running, start a Release thread that runs `release` to cut it, run `triage` and `retro-planning`, and plan the next Release.
5. When every feature is merged or parked and no report thread is running or report written, start a thread that runs `milestone` to write its report, then stop for the user's Milestone review.

---

**Gaps you might want to close before approving.** I kept these out of the draft because nothing you confirmed covers them:

1. **Who plans a Milestone.** Step 1 of the loop waits for "Milestone planning has settled", but no confirmed thread kind runs `milestone`'s planning. If nothing else starts one, delivery never begins. One possible line: "When the user asks for a Milestone or small Release, start a planning thread that runs `milestone`."
2. **The tier rule has no models behind it.** With no map, the loop falls back to the worker tool's default model for every tier. A coordinator that can't load `model-tiers` won't use the plugin's default map either.
3. **No check-in timing.** The loop has no check-in step, and the Boundary record names no interval.
4. **Two standing rules have no answer:** how many questions a thread asks the user at once, and how many review Rounds to run. I recorded both as "not needed".

**Where the loop came from:** the plugin at main's version. On that main, the last commit that changed `team-lead` or `milestone` is `4f2c9e1`, which is useful for checking later whether the copy has gone stale.

I've written no files and sent nothing. You can edit the draft or approve it in your own message. Once you approve, I'll send that exact text to the coordinator to save.
