# Build threads coordinate; subagents write the code

Every piece of work starts as a GitHub issue: a spec is one issue, its tickets are sub-issues of it, and a milestone groups the specs and tickets for one goal. The project coordinator hands each one to its own thread: a **spec** goes to a **spec thread**, which runs `implement-spec`, and a **lone ticket** (a ticket under no spec, such as a bug fix, a chore or CI/CD work) goes to a **ticket thread**, which runs `implement`. A build thread never writes code itself, not even to resolve a merge conflict. It starts **Implementer** subagents to build test-first and to fix, runs the review Rounds of [ADR 0003](0003-code-review-runs-find-verify-rank-in-rounds.md) with fresh reviewer subagents, talks to the user, and merges. We chose this because it keeps the thread's own context small enough to stay sharp for coordinating, and because each piece of work gets its own thread that the user can watch and steer.

## How a build thread works

- **Model tier.** `to-tickets` marks each ticket regular or premium (premium for heavy or tricky work), and its Implementer runs on that tier. A lone ticket runs on the regular tier unless its issue says premium. Spec-PR fixes that touch no ticket's files also run on the regular tier. Trivial jobs, such as running a test suite, go to cheap subagents.
- **Fixes.** The Implementer that built a ticket also fixes its review Findings, because it already knows the code; on a change that changes design, design Findings go to the user first and the Implementer commits only the agreed answers ([agentic-review's ROUNDS.md](../../plugins/dev-skills/upstream-skills/agentic-review/ROUNDS.md#design-findings-go-to-the-user)). Findings on a spec's pull request, which can span tickets whose Implementers have finished, go to a new Implementer working on the spec branch, on the highest tier of the tickets the Finding touches. Merge conflicts go to an Implementer the same way. Reviewers stay fresh every Round.
- **Evidence.** Before a lone ticket's pull request opens, or before a spec's ticket is squash-merged, the Implementer shows that the work works: test output, the typecheck, and screenshots for anything visual. The thread checks it, and it goes into the pull request's Evidence section (the `pr` skill); a spec's pull request sums up each ticket's evidence there.
- **Inside a spec thread.** Each ticket gets its tests and a **ticket check** before it joins the spec branch, so problems surface while the ticket is fresh. A ticket check is one Review at Quick depth over the ticket branch's diff against the spec branch. It is not a Round: the Implementer fixes (design Findings on a ticket that changes design go to the user first) and the check runs again, with fresh reviewers, until no Important is open, at most 3 times; after a third check that still has an Important open, the thread brings the ticket to the user. The Implementer also fixes "fix" Nits; "skip" Nits are dropped. Pre-existing Findings wait and are filed once, after the spec pull request's last Round. The spec pull request's Rounds treat ticket-check Findings as already raised, so they are never repeated. Each check's Findings are recorded as a comment on the spec's pull request (the first ticket's once the draft opens), so `retro` sees them. The full Rounds then run once over the spec's pull request.
- **Parallel work.** Up to 3 build threads run at once, so usage stays predictable and pull requests don't pile up conflicts. Implementer subagents inside a thread don't count toward this; a spec thread runs at most 3 Implementers at once.

## When the user must review

The thread merges its own pull request once the review is clean and CI is green, unless any of these holds; then it brings the pull request to the user:

- it ran at Deep depth (security, money, deleting data);
- it is a **one-way door**: reverting the change would not undo it (a data migration, deleted data, a public interface others depend on, a message sent outside the project). Each Implementer says so with its evidence, the `pr` skill marks it on the pull request, and a spec's pull request is a one-way door if any of its tickets is;
- it changes an ADR, the glossary, a `CLAUDE.md` or a `REVIEW.md`, or anything else the repo's own rules (its `CLAUDE.md`, the project instructions, its docs) say a person merges;
- the review hit the 5-Round cap.

In this repo, the rules add a change to the `agentic-review` skill (this repo's `CLAUDE.md`); the skills name only the general case, because a change to that skill is only ever made in this repo.

The user then merges, or tells the thread to. This follows the Claude Code team's practice of setting human review by the risk of the change, not by who wrote it.

## Considered options

- **Upstream's `implement` as-is:** the session builds and commits to the current branch itself, with no pull request. Its context fills with code, and nothing reaches the user for review.
- **Dropping `implement-spec`** in favour of one thread per ticket: the user preferred one thread per spec, with subagents doing the tickets and one review over the whole spec.
- **Always asking the user to merge:** safe, but the user becomes the bottleneck on low-risk work.

## Consequences

- `implement` and `implement-spec` are rewritten as coordinator skills. `to-tickets` adds a model tier to each ticket, `pr` gains an Evidence section and a one-way-door marker, and `to-tickets` and `wayfinder` end by offering `setup-project`. All of these are Patches (`PATCHES.md`).
- A new skill, `setup-project`, writes the project instructions that tell the coordinator how to brief build threads (which skill, model tier, repo, review depth). It runs `grilling` inside, so it asks at most 3 questions at a time. The user runs it by hand, and `wayfinder` and `to-tickets` offer it to the user at their end only when planning added a repo, a kind of thread or a standing rule. The instructions say how threads work and carry the user's tier-to-model map; they never hold the state of the work, and tell the coordinator to find open specs, plannings and tickets on the tracker. Once the user approves the text, the thread sends it to the coordinator, which saves it.
