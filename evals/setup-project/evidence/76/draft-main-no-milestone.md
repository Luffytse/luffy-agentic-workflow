**Project instructions draft: Orchard**

What I found:
- **Existing instructions:** none yet, so this is a first draft rather than a re-run with a diff.
- **Docs:** `CLAUDE.md`, [docs/dev-skills/index.md](docs/dev-skills/index.md) and [docs/dev-skills/issue-tracker.md](docs/dev-skills/issue-tracker.md) exist. The tracker is GitHub Issues only.
- **Milestone:** there is no open Milestone agreement, so Orchard is outside a Milestone. The draft therefore carries the full rules, not just the project-specific choices.
- **Can the coordinator load the skills?** Yes. It checked its own skill list and can load `team-lead`, `milestone`, `release` and `worker-control`. So the delivery loop is not copied in, and the coordinator runs `team-lead` itself.
- **Model map:** not needed. The draft names the tiers and the rule, and `model-tiers` supplies the default models.

---

```markdown
# Orchard: project instructions

Repo: orchard-team/orchard. Build threads start at [docs/dev-skills/index.md](docs/dev-skills/index.md); repo rules are in [CLAUDE.md](CLAUDE.md).

## Where work lives
Find open specs, plannings and tickets on GitHub Issues (orchard-team/orchard) when you need them; how the tracker is used is documented in [docs/dev-skills/issue-tracker.md](docs/dev-skills/issue-tracker.md). These instructions hold no work state.

## Threads
- Planning threads: start them with `wayfinder`, `to-spec` or `to-tickets`, whichever the work needs.
- Build threads: Spec threads run `implement-spec`; lone Ticket threads run `implement`.
- You run `team-lead` to deliver planned work (a Release, or a Milestone with `milestone`).

## Briefs
Every brief carries: the skill, the Model tier (cheap, regular or premium), the repo, the Review level, and the link to the issue.
Start each thread on the model mapped to its brief's Model tier (the `model-tiers` default map; Orchard has no override).

## Standing rules
- At most two Build threads run at once.
- Merging: the user merges schema migrations. Agents merge ordinary changes after a clean Review and green CI.
- Ask the user at most one question at a time.
- Workers send an explicit completion callback when they finish; archive each finished worker.
```

---

Please approve this or edit it. I've written no files and sent nothing. Once you approve it in your own message, I'll send exactly that text to the coordinator to save. I'll only call it saved after the coordinator confirms.
