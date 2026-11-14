---
name: ask-matt
description: "Route the user to the right skill or flow, from idea to ship. Use when the user asks which skill to use, where to start new work, or how the skills fit together."
---

# Ask Matt

You don't remember every skill, so ask.

Before stating what a skill does or recommending a step be skipped, read that skill's SKILL.md: the summaries here are for orientation only.

A **flow** is a path through the skills. Most paths run along one **main flow**, and two **on-ramps** merge onto it. Everything else is standalone, or a vocabulary layer that runs underneath.

## The main flow: idea → ship

The route most work travels. You have an idea and want it built.

1. **`/grill-with-docs`** sharpens the idea by interview. Start here whenever you are **working in a working directory**: it's stateful, retaining what it learns in the glossary (`docs/dev-skills/glossary.md`) and ADRs. (No working directory? Use `/grilling` instead, covered under Standalone. `grill-with-docs` runs the same `/grilling` primitive and also leaves a paper trail, which makes it the better choice whenever a repo is there to leave it in.)
2. **Branch: can you settle every question in conversation?** If a question needs a runnable answer (state, business logic, a UI you have to see), detour through a prototype, bridged by **`/handoff`** in both directions (a prototype is a side task forked mid-phase, with its code on a throwaway branch out of main, which is exactly what `/handoff` is for; see Phase boundaries):
   - **`/handoff`** out, then open a fresh session that reads the handoff,
   - **`/prototype`** to answer the question with throwaway code,
   - **`/handoff`** back what you learned, and reference it from the original idea thread.
3. **Branch: is this a multi-session build?**
   - **Yes** → **`/to-spec`** (turn the thread into a spec), then **`/to-tickets`** to split it into tracer-bullet tickets, each declaring its **blocking edges**. The edges are native blocking links where the tracker has them, and a "Blocked by" line otherwise. Then **`/implement-spec`**, in its own fresh thread, builds the whole spec in one run. It reads the tickets as a **task graph**, runs Implementer subagents across the ready **frontier** in parallel, each in its own worktree, gives each ticket a Quick ticket check, and squash-merges it into one **spec branch**, whose pull request gets the full review and merges into main with a merge commit. Don't hand a spec's tickets to `/implement` one by one: it sends a ticket under a spec here, and a ticket labelled for another coding agent is handed to that agent, which lands it on the same spec branch.
   - **No** → **`/implement`** as a lone ticket. Its thread coordinates: it starts an Implementer subagent to build the ticket, opens a pull request with `/pr`, runs `/agentic-review`, then merges it or brings it to you.

   Either way, the code gets built by driving **`/tdd`** (one red-green slice at a time) and closes out with **`/agentic-review`**: Finders look for problems, a Verifier checks each one, and the survivors are ranked by Severity. It first sizes the review from the changed files (a version bump gets only the project's checks), then runs at most 3 Rounds on a pull request, each posting one comment. In `/implement` the Implementer drives `/tdd` and the thread runs `/agentic-review`; `/implement-spec`'s implementers each drive `/tdd`, and it runs `/agentic-review` as one Quick ticket check per ticket and then over the spec branch's pull request. For a change to a skill, a prompt or an agent instructions file, `/tdd`'s test is an eval (a fresh agent run on a fixture, compared with the default branch's version), not a grep for a sentence. Reach for **`/tdd`** on its own when you just want to build a concrete behaviour test-first without a full spec, and **`/agentic-review`** on its own whenever you want to review a branch or PR against a fixed point.

   When the work goes up as a pull request, **`/pr`** writes the title (a Conventional Commits type, so main's history reads cleanly) and shapes the body: the smallest visual that shows the change, before/after evidence that it works, and a one-way or two-way door call. It's model-invoked, so the agent reaches for it whenever it writes a PR.

4. **`/retro`** closes the loop. After a build, and especially one that went sideways, it looks back over the session and suggests changes to the agent's **environment**, not the code: navigation pointers, automated checks, the coding standards `/agentic-review` enforces, steering files, tooling. Mechanical mistakes become deterministic checks; judgement calls become coding standards. The next build then starts from a better environment. Its suggestions pile up as Retro issues. **`/retro-planning`** sorts that backlog with no questions, at every Release end or when you ask: it groups it by root cause, closes one-offs and hands repeated or severe problems to `/triage`, which briefs them for agents.

### Context hygiene

Keep steps 1–3 in **one unbroken context window** (don't compact or clear until after `/to-tickets`) so the grilling, spec, and tickets all build on the same thinking. The build then starts in its own fresh thread: `/implement-spec` for a spec, `/implement` for a lone ticket, each working from the tickets. Run `/retro` in the session it's looking back on, before you clear; after clearing, point it at that session's log instead.

The limit on this is the **[smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone)**: the window (~150k tokens on state-of-the-art models) within which the model still reasons sharply. If a session approaches it before `/to-tickets`, don't push on degraded; `/compact` at the nearest phase boundary and carry on (see Phase boundaries).

## On-ramps

A starting situation that generates work, then merges onto the main flow.

- **Bugs and requests piling up** → **`/triage`**. It moves issues through triage roles and produces agent-ready issues, which **`/implement-spec`** (for an issue under a Spec) or **`/implement`** (for a lone one) later picks up.

  Triage is only for issues **you didn't create**: bug reports, incoming feature requests, anything that arrives raw. Tickets that `/to-tickets` produced are already agent-ready, so **don't triage them**. At each Release end, `/release` runs triage as an agent-decided batch that also sweeps the backlog (duplicates, obsolete issues, issues left out of 3 Releases) and sends enhancements an agent found to you at `ready-for-human`; the skill says how.

- **Something's broken** → **`/diagnosing-bugs`**. For the hard ones: the bug that resists a first glance, the intermittent flake, the regression that crept in between two known-good states. It refuses to theorise until it has a **tight feedback loop** (one command that already goes red on *this* bug), then fixes with a regression test. Once the fix is in, run **`/retro`** in the same session to ask what would have prevented the bug; where the real finding is that there's no good seam to lock it down, that's a job for **`/improve-codebase-architecture`**.

- **A huge, foggy effort: a greenfield project or a huge feature build, too big for one session** → **`/wayfinder`**, the most cognitively demanding flow here. When the way from here to the destination isn't visible yet, it charts a **shared map** of **decision tickets** on the issue tracker and resolves them one at a time, producing **decisions, not deliverables**, until the fog is pushed back and the way is clear. Where **`/grill-with-docs`** sharpens an idea you can hold in one session, wayfinder is for the idea you can't, and it's slower and denser, so save it for exactly that, never a well-scoped feature.

  When the map clears, **it hands off, it doesn't build**: merge onto the main flow at **`/to-spec`**, which collapses the map's linked decisions into a buildable plan, then `/to-tickets` and `/implement-spec` as usual. Looping the map straight into `/implement` skips that collapse and throws the linked detail away, so go straight to `/implement` only when the effort turned out genuinely small: write one lone ticket first (for example with `/to-tickets`), then run `/implement` on it.

## Codebase health

Not feature work, just upkeep.

- **`/improve-codebase-architecture`** runs whenever you have a spare moment to keep the codebase good for agents to operate in. It surfaces **deepening opportunities**; picking one _generates an idea_ you can take into the main flow at `/grill-with-docs`. It's the survey that finds the candidates; **`/codebase-design`** (below) is the bench you design the chosen one on.

## Releases

For a repo that cuts Releases, versioned or not, **`/release`** ships a few items at a time. Its release doc (`docs/dev-skills/release.md`) holds the repo's **versioning policy** (none, pull requests bump, or Releases bump) as the cut steps `/release` runs, so the skill itself knows no version: where pull requests bump, each pull request adds the bump at merge with the number the repo's own docs say how to get (`/implement` and `/implement-spec` follow them). Start a thread for `/release` when no open issue still carries the open release issue's label: it writes the changelog entry, runs the cut steps and the whole-Release check, closes the Release, runs `/retro-planning` and `/triage`, then plans the next Release with no approval: the next features of the Milestone issue's table, in its order, and the waiting bugs (one that blocks a feature goes just before it), up to the release doc's Release size. You plan the features, through a Milestone (a small Release is a Milestone with one Release); a fix that cannot wait is built like any issue and listed in the next changelog. The coordinator delivers the planned Release's issues with **`/team-lead`**, which starts and watches the build threads and the Release threads; a coordinator that cannot load the plugin's skills follows the project instructions `setup-project` writes for it, which have it start those threads.

## Milestones

When you want agents to deliver planned work unattended, a whole product goal across several Releases or one small Release, start a **Milestone** with **`/milestone`**: every plan is one. You name the features and agree their dependency graph; each feature is then planned through the main flow in its own session, in graph order, and agents may propose a feature but never add one. Once every feature is planned, `/milestone` writes the Milestone issue with you (goal, features in order with their acceptance criteria and what each waits for, exclusions; boundaries stay the Boundary record's). Once planning settles the features are fixed: a feature you plan while a Milestone runs waits for the next one. `/milestone` then runs the Plugin version check, one read that threads load main's plugin text, before any delivery starts. Delivery itself is **`/team-lead`**'s (or, for a coordinator that cannot load it, the instructions `/setup-project` assembles for it): the coordinator runs it to start the Release threads and the build threads in order, react to what they report, check in on a silent one and replace it, and follow the merge-time steps the repo's own docs give. At the end `/milestone` writes the report for your Milestone review. With no Milestone open, the build skills work as described here; delivery and Release planning wait for one.

## Vocabulary underneath

Two model-invoked references that run *beneath* the other skills, each the single source of truth for its vocabulary. Reach for them directly when the **words**, not the process, are the problem; or let the skills above pull them in.

- **`/domain-modeling`**: sharpen the project's *domain* language: challenge a fuzzy term, resolve an overloaded word ("account" doing three jobs), record a hard-to-reverse decision as an ADR. It's the active discipline `/grill-with-docs` drives to keep `docs/dev-skills/glossary.md` a clean glossary.
- **`/codebase-design`** is the deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality) for designing a module's *shape*: a lot of behaviour behind a small interface at a clean seam. `/tdd` and `/improve-codebase-architecture` both speak it.

## Phase boundaries

A **phase** is a chunk of work inside a session: the grilling, the implementation, the QA. At the **boundary** between two of them you have five options, and picking between them is the fuzziest decision in this whole map:

- **Continue**: stay put. Costs nothing, loses nothing.
- **`/clear`**: empty the window, when nothing here matters to what's next.
- **`/handoff`** writes a document the next agent can read (a tracker issue by default). Narrow: only for a **new harness**, a **new directory**, a **colleague**, or forking a side task **mid-phase**. What it buys is portability.
- **Subagent**: send a tightly-scoped task to its own window and get a report back.
- **`/compact`** compresses this context and seeds a fresh session with it. The **default**, at the bottom of the tree rather than the first reach.

Read [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) for the ordered tree: the five questions, the reasoning behind each branch, and why the primary-source cost makes **Continue** the one to rule out first. Make the decision **at** a boundary; mid-phase, continue or split the rest into subagents.

## Standalone

Off the main flow entirely.

- **`/grilling`** is the interview primitive itself: rounds, the frontier, facts are the agent's job and decisions are yours. `/grill-with-docs` is the named way in when there is a repo, and `/triage`, `/wayfinder` and `/improve-codebase-architecture` all run it internally. Reach for it directly when there is no working directory, or when you want the interview with no wrapper around it.
- **`/prototype`** is a small, throwaway program that answers one design question: does this state model feel right, or what should this UI look like. Throwaway is a constraint on how the code is written, not a promise to destroy it: the answer folds into the real code, and the prototype itself is kept as a **primary source** on a `prototype/<name>` branch out of main, pointed at from the implementation issue. It's the detour in step 2 of the main flow, but reach for it any time a design question is hard to settle on paper.
- **`/research`**: delegate reading legwork to a **background agent**: it investigates a question against **primary sources**, then leaves a cited Markdown file in the repo. Keep working while it reads. The file it produces is something to take *into* the main flow at `/grill-with-docs`, since research feeds the thinking rather than replacing it.
- **`/wizard`** is for the steps only a **human** can take: provisioning infrastructure, setting up credentials or CI secrets, clicking through an unfamiliar third-party dashboard, running a one-off migration or cutover. It generates an interactive bash script that opens each URL, captures each value, and writes it into `.env` and GitHub secrets, so the procedure stops being something you re-explain to an agent every time. Model-invoked, so the agent reaches for it the moment it hits a wall only you can pass. If the agent could just do it itself, it should; this is for where a human is genuinely in the loop.
- **`/writing-for-agents`** is the reference for writing documents agents consume: skills, AGENTS.md, pointed-at docs.

## Precondition

**`setup-dev-skills`**: run before your first engineering flow to configure the issue tracker, triage labels, and doc layout the other skills assume, the Boundary record of what the user allows agents to do, and the release doc `/release` reads. It supports GitHub repos only for now.

**`setup-project`**: run to write or update a project's instructions, the short text its coordinator reads before it starts a thread (how its threads work and what every brief carries, never the state of its work; for a coordinator that cannot load the plugin's skills, also the whole Milestone cycle it follows instead). Use it when a new repo, kind of thread or standing rule means they are out of date.
