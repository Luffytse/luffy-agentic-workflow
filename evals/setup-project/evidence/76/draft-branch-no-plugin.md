I've finished the draft. Nothing was written to disk and no messages were sent.

**Facts and checks behind it.** Orchard is inside a Milestone: an open Milestone issue was found under the Boundary record's `milestone-<n>` label. The coordinator **cannot** load the plugin's skills (its own answer, which you relayed). So the draft has to spell out the whole cycle, and it never tells the coordinator to run `milestone`, `team-lead` or `release` itself. The plugin I read from is at main's version on its source repository, so I didn't need to stop and warn you before drafting. The source stamp is `4f2c9e1`.

---

## Draft: Orchard project instructions

**Orchard, repo `orchard-team/orchard`.** These instructions say how the project's threads work. They hold no state: find open Milestones, specs, plannings, releases and tickets on **GitHub Issues** in `orchard-team/orchard`, using the operations documented in [`docs/dev-skills/issue-tracker.md`](docs/dev-skills/issue-tracker.md). Build threads start at [`docs/dev-skills/index.md`](docs/dev-skills/index.md). The repo's own rules are in [`CLAUDE.md`](CLAUDE.md). Boundaries, the check-in interval and the Milestone label form are in the Boundary record, [`docs/dev-skills/boundaries.md`](docs/dev-skills/boundaries.md). Every Milestone and every issue follows it.

You cannot load this plugin's skills, so these instructions are your loop. For every step that needs a skill, start a thread for it. Where you can't make a tracker write yourself, start a cheap chore thread to make it.

**Source stamp:** `4f2c9e1`. This is the last commit on the plugin source repository's main that changed `team-lead` or `milestone`.

### Terms
- **Milestone issue**: an open issue carrying a `milestone-<n>` label whose body is the Milestone itself, not a feature. While one is open, the project is inside that Milestone. Its **order rule** is the line under "Features, in build order": either "one at a time" or "up to k at once".
- **Release / Order**: a Release is one named step of a Milestone. Its release issue's `## Order` list gives the issues the Release builds, ranked. Build in that order.
- **Parked**: an issue marked with the tracker doc's **Park** operation. Skip it until the user removes the label. A lifted issue keeps its place in the order.
- **Slot**: room for one build thread. Slots = the smaller of **2** and the order rule. A thread that still reads as running holds its slot, even while it is quiet.
- **Report re-entry**: after the report is posted, the user may send a feature back or lift a park. Only that work goes back into delivery, and a new report follows that links the earlier one and says what changed.

### Thread kinds and tiers
Start each thread on the model mapped to its brief's Model tier: **cheap = <model>, regular = <model>, premium = <model>** (the plugin default for Claude Code).

| Thread | Runs | Tier |
|---|---|---|
| Milestone planning | `milestone` Planning | premium |
| Feature planning / add a feature | `grill-with-docs`, then `to-spec` + `to-tickets` (multi-session feature) or `to-tickets` for one lone Ticket; adding a feature also runs `milestone` "Adding a feature mid-Milestone" | premium |
| Startup verification | `milestone` Startup verification | regular (its version-probe worker: cheap) |
| Release | `release` | premium |
| Build | Spec with Tickets → `implement-spec`; Spec without Tickets → `to-tickets` first, same slot; lone Ticket → `implement`; related issues → `implement` one after another in one slot | the issue's Model tier line, else regular |
| Bug the user raises | `triage` (files it) | regular |
| Report | `milestone` report (its reporting.md) | regular |
| Chore (a tracker write you can't make, closing the Milestone issue, arranging or ending the check-in) | none | cheap |

### Planning (when the user asks for a Milestone or a small Release)
1. Start a planning thread on `milestone` Planning. A small Release is a one-Release Milestone and gets the same full cycle.
2. Before asking for new features, it first offers the work set aside for this Milestone: the last report's "Next Milestone" proposals and the issues titled for it.
3. It writes the Milestone issue **last**, only after every feature is planned and you have agreed the draft. Then it labels every open issue each feature holds.
4. When it asks for a feature thread, start one with this brief: *"Plan a feature of Milestone <n>, whose Milestone issue is not written yet; planning thread: <link>. Run `grill-with-docs`, then `to-spec` and `to-tickets` (or one lone Ticket). End with an issue holding its acceptance criteria. Report any change to the goal, acceptance, exclusions, order or Release split to the planning thread."*

**While a Milestone is open:**
- **A feature the user plans** joins that Milestone unless the user says it's for the next one. Start a feature thread to plan it, then have it add the feature with `milestone` "Adding a feature mid-Milestone": list the feature first, then label it, then update the Tickets it touches.
- **A bug the user raises** goes to a `triage` thread, which files it.

### Startup verification (before any Build thread)
Start a verification thread. It asks you for any action only you can take, such as starting its probe worker; do those and tell it the result. Brief line: *"Compare the source stamp `4f2c9e1` with the last commit on the plugin source's main that changed `team-lead` or `milestone`, and report both."* If the stamp has moved, tell the user once to re-run `setup-project`, then carry on unless they say to wait.

Delivery starts only once the result on the Milestone issue reads `Verdict: ready`. If an essential capability failed, tell the user what each failure means and wait for their word on how to go on. Record that word on the Milestone issue, naming each capability it starts without.

### Delivery: at every wake
A wake is any of these: a thread reports or asks, a harness notice, the check-in, or the user writes. At each wake, read the state afresh: the Milestone issue, the current release issue and its issues (park state and open blockers), the branches, and each thread's own state. A thread's message is a reason to read, not the state itself. Then act, in this order:

1. **Pause or resume**, on the user's word only. Each gets a `<!-- team-lead pause -->` or `<!-- team-lead resume -->` comment on the Milestone issue quoting the user. While paused, start, nudge, replace and park nothing.
2. **Merge-time steps.** Every build thread merges its own pull request, except one containing a **schema migration**: that one the user merges. The thread says plainly that the user must merge it, and keeps its slot until the merge. Production deploys need the user's approval (Boundary record). From `CLAUDE.md`, quoted in full:
   > **Version hand-out.** A thread about to merge a pull request that changes a file under `agent-skills/` asks the coordinator for its version number just before merging. The coordinator gives main's version raised minor for a new or changed skill, patch for a fix, and records it in a comment on the issue the pull request builds. One number is out at a time: while one is out, it tells any other asking thread to wait and serves waiting threads in the order they asked. **Re-read after a skill merge.** Right after such a merge, and before any further thread starts, the coordinator re-reads the open issues no running thread is building whose body names the changed skill, and updates, closes or comments on each.
3. **End of delivery.** Check this gate at every wake: every planned feature is merged or parked (a Spec blocked by a parked Ticket counts as parked). If a Release cut is in progress, or the last merged Release still needs its cut, start or await that Release thread first. Only after the last cut has reported:
   - start nothing more;
   - end the check-in, read back that it no longer runs, and record it;
   - start the report thread.

   If a report for this state is already waiting, do nothing more.
4. **Check-in findings** (below).
5. **Next starts.** Start nothing while paused or while a merge-time step is still open.
   - **Releases:** start a Release thread only when all of these hold:
     - none is running;
     - no open, unparked issue carries an open release issue's label;
     - either a release issue naming this Milestone is open, or an open, unparked planned feature with no release label is unblocked (or blocked only by issues `release` ranks ahead of it).

     Brief it with the Milestone issue, `docs/dev-skills/release.md` and the last release issue cut. Start no Build thread while it runs. Never nudge or replace it. If it reports that the cut is blocked, or that it planned nothing while features are still open, tell the user in one line, post that as a `wait` comment, and don't start another Release thread until something changes or the user writes.
   - **Builds:** while a slot is free, start the first Order entry that still carries the release label and is open, unparked, unblocked and has no thread. An entry that was started before, whose thread ended or whose park was lifted, goes before one that never started. **When a backend issue and a dashboard issue are both eligible, start the backend one first.** Under "one at a time", the next starts only once every one before it has closed or is parked.
   - **Build brief:** the skill, the issue link, the Milestone issue link, the Model tier, and a Review level only if the issue or the user names one. Also these lines: *"When a skill runs in this repo, follow the checkout's copy (`agent-skills/<name>/`) on main, not the installed one."* and *"Record in your issue report the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference; write 'unknown' where you can't read one."* Post a `<!-- team-lead start -->` comment on the issue with the thread id, skill, tier, Review level, start time and session link.

**Reacting.**
- **A report or question:** read the thread's issue, branch and pull request.
  - A finished build frees its slot.
  - If its check against main finds the issue already fixed or obsolete, open the evidence, then close or re-plan the issue. Closing a planned feature, or changing the goal, acceptance or exclusions, goes to the user as one question.
  - Answer questions that fall within the boundaries. A question that crosses a boundary goes to the user.
- **No report:** a pull request that is merged, or ready with no comment or push since, counts as reported. Tell the thread what you decided.
- **A thread ended without its result:** start a fresh thread from its pushed branch. This counts as a stall.

### The check-in
At the wake where the first Build thread starts, before starting it, arrange a check-in at the Boundary record's interval. Keep any check-in that is still running. Do it yourself if Startup verification showed you can schedule; otherwise use a chore thread. Arrange it again at the first build start after it was ended, and at a resume that finds builds running and no check-in. Record each arrange and end. If it can't be arranged, tell the user once.

At each check-in, read every running Build thread's last commit, last comment and pull request, then act:
- **Ready but unreported:** react as above.
- **Silent for a full interval:** nudge it once, asking for an answer as a comment on its issue, and post a `nudge` comment.
- **Still silent after the nudge:** stop it and read the stop back. Then start a fresh thread with the same skill, tier and Review level, briefed to resume from the pushed branch it names.
- **Park instead** when the stop doesn't read back, when this is the feature's second stall, or when the fresh start fails. Post a `parked` comment with the reason, whether a writer may remain, and links. Tell the user once.

If a Release thread is silent for a whole interval, tell the user once, with the link. A quiet check-in writes nothing.

### Report and review
The report thread posts the report on the Milestone issue and stops. It leaves the Milestone open; acceptance is the user's alone.
- **The user accepts:** a chore thread closes the Milestone issue.
- **The user sends a feature back or lifts a park:** re-read the agreement and the tracker, and put only that work back into delivery. Re-arrange the check-in at the first build start. Then a new report follows that links the earlier one.

---

**Gaps for you to check:**
1. **Tiers I chose myself.** The skills don't name a tier for the triage, report and chore threads, so I picked regular, regular and cheap. Planning and feature threads are premium because of `model-tiers`' "planning, grilling" use.
2. **Thread start/stop and the check-in are worded generally.** I wasn't given `worker-control`, so this part rests on your fact that the coordinator runs in Claude Code. Whether the coordinator can schedule the check-in itself is left to the Startup verification result.
3. **Check-in done by hand.** I left out `team-lead`'s `snapshot.py`, since the coordinator can't reach the skill's folder.
4. **Length.** The draft is well over a one-minute read. That's unavoidable when the coordinator can't load the skills and the instructions have to carry the whole cycle.
5. **No Boundary record values copied.** The draft points to the 45-minute interval and the production-deploy approval rather than copying the values, so a change to the Boundary record needs no re-run. Tell me if you'd rather have them written in.

Edit anything you like. When you approve the full text in your own message, I'll send exactly that text to the coordinator to save.
