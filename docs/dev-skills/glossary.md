# Glossary Map

The words used in luffy-agentic-workflow, a plugin marketplace: the skills coding agents use, packaged so every project and every agent session can load them. One page per Area of the docs index; Building has three. Each entry says what a word means and names the skill or doc that owns its rule.

## Contexts

- [Packaging](./glossary/packaging.md): the marketplace, plugin, skills, Upstream, Model tier, Shared rule and Base skill
- [Agent setup](./glossary/agent-setup.md): Repo labels, `next-release`, the Boundary record and the Door
- [Building: Milestones and delivery](./glossary/delivery.md): project threads, Milestone, Startup verification, Harness, Worker control, Team lead and what it does when a worker stalls
- [Building: Releases](./glossary/releases.md): Release, its size, planning, Main check, Ranked list, cut, Triage batch and Release thread
- [Building: Specs, Tickets and build threads](./glossary/building.md): Spec, Ticket, the build threads and branches, Build check, Implementer and Merging
- [Code review](./glossary/code-review.md): how skill changes are tested (CI), and Review, Rounds, Finders, Verifier and Findings
- [Retros](./glossary/retros.md): Retro issues, the backlog and Retro planning
- [Docs](./glossary/docs.md): the Skill docs folder, the Docs index and Area

## Relationships

- **Delivery → Releases → Building**: a Milestone holds Releases; the Team lead starts Release threads, which plan the issues that build threads then build.
- **Building → Code review**: every build thread's pull request gets a Review before `merging` finishes it.
- **Agent setup → Building, Code review**: the Boundary record decides who merges and when a Review waits on a boundary.
- **Code review → Retros**: `retro` looks back on a finished, reviewed pull request and only files Retro issues, repeated Bug classes included.
