I followed setup-project (and read the milestone and model-tiers skills it points to). Here is the draft. I haven't written any files or sent anything.

**What I found**
- **Existing instructions:** none, so this is a first draft and there's no diff.
- **Docs:** `CLAUDE.md` and `docs/dev-skills/index.md` exist. The tracker is GitHub Issues, described in `docs/dev-skills/issue-tracker.md`.
- **Milestone:** there's no open Milestone agreement, so the project isn't inside a Milestone and the draft covers everything.
- **Coordinator skills:** the coordinator checked its own list and can load `team-lead`, `milestone`, `release` and `worker-control`. That means the draft doesn't need to write out the whole delivery cycle.
- **Model map:** you don't need a custom one, so the draft names the tiers and uses the model-tiers defaults without writing out a map.

---

## Draft project instructions: Orchard

**Repo and tracker.** Orchard's only repo is `orchard-team/orchard`. Its tracker is GitHub Issues, described in [`docs/dev-skills/issue-tracker.md`](docs/dev-skills/issue-tracker.md). When you need open specs, plannings or tickets, look them up on GitHub Issues. These instructions never list open work.

**Docs.** Build threads start at [`docs/dev-skills/index.md`](docs/dev-skills/index.md). Repo rules are in [`CLAUDE.md`](CLAUDE.md).

**Threads and their skills.**
- **Planning threads** run `wayfinder`, `to-spec` or `to-tickets`, depending on the step.
- **Spec threads** run `implement-spec`.
- **Lone Ticket threads** run `implement`.
- **You, the coordinator,** run `team-lead` to deliver planned work: a Release, or a Milestone together with `milestone`.

**Briefs.** Every brief includes the skill, the Model tier (cheap, regular or premium), the repo (`orchard-team/orchard`), the Review level and a link to the issue.

**Models.** Start each thread on the model mapped to its brief's Model tier. Orchard has no map of its own, so use the `model-tiers` defaults.

**Standing rules.**
- Run at most two Build threads at once.
- Ask the user at most one question at a time.
- The user merges schema migrations. Agents merge ordinary changes once Review is clean and CI is green.
- Workers send an explicit callback when they finish. Archive each finished worker.

---

Edit anything you like. I'll treat it as approved only when you say so in your own message. After that, I'll send exactly the approved text to the coordinator to save.
