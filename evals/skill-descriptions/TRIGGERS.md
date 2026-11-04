# Trigger branches: old text -> new text

For the pull request body (Ticket #621). Every "Use when" branch and every cross-reference that separates a skill from its neighbour in the old description, and where it stands in the new one. Words: old -> new (`build_listing.py --counts`). Total 1810 -> 1198 words (-34%); longest 163 -> 60. A skill not listed here (and `grilling`, `domain-modeling`, `diagnosing-bugs`, `tdd`, `pr`, `prototype`, `docs-index`, `issue-absorption`, `review-record`, `writing-for-agents`) keeps its description unchanged.

| Skill (words) | Old branch | New text |
| --- | --- | --- |
| agentic-review (81 -> 42) | review a PR | "review a PR" |
| | a branch or work-in-progress changes | "branch or work-in-progress changes" |
| | run a ticket check | "run a ticket check" |
| | "review since X" | `"review since X"` |
| | changes since a fixed point (commit, branch, tag, merge-base) | kept |
| | Round 0 sizes the review; review-rounds runs it | "Round 0 sizes it, review-rounds runs it" |
| | level None / Quick / Standard / Deep, Finders, Verifier, 3 Rounds | body only (review-rounds' own description) |
| ask-matt (39 -> 33) | which skill to use; where to start new work; how the skills fit together | same three branches |
| codebase-design (37 -> 36) | design or improve a module's interface; decide where a seam goes; testable or AI-navigable; another skill needs the vocabulary | same four branches |
| grill-with-docs (36 -> 34) | "grill me"; plan or design stress-tested in a repo | same two branches ("plan or design" is in the first clause; the branch says "a plan") |
| handoff (42 -> 38) | "handoff" or "hand off"; work moves to a new harness, directory or colleague; a side task forks off mid-phase | same three branches |
| implement (61 -> 35) | handed a lone Ticket (bug fix, chore, small feature under no Spec) to build and ship | same branch; steps (Implementer, pull request, review, merge) in one clause |
| implement-spec (89 -> 34) | handed a Spec (the result of to-spec and to-tickets) to build and ship | same branch |
| improve-codebase-architecture (45 -> 36) | improve the architecture; find refactoring candidates; review the codebase's structure | same three branches |
| merging (70 -> 43) | a build or release workflow reaches its merge step | same branch |
| | must decide whether an action crosses a boundary | same branch |
| milestone (163 -> 60) | asks for a Milestone | "when asked for a Milestone" |
| | wants new work planned as a small Release | "or small Release", "(a small Release is one)" |
| | cutting one, or planning an open Milestone's next one, is release's | "(cutting one, or planning an open Milestone's next one, is release's)" |
| | add a feature to one (mid-Milestone) | "to add a feature to one" |
| | a feature the user planned is ready while a Milestone is open | "a feature is ready" (shortened; "the user planned" and "while a Milestone is open" are gone) |
| | a Milestone is about to start | "when a Milestone starts" |
| | record Startup verification (the worker-control check plus the loaded skill version) before delivery starts | "verify startup" (the worker-control check and the skill version are body only) |
| | its delivery reaches the Milestone review; write the Milestone report and stop for the review | "reaches its review", "report" ("at its end", "stop for the user's review" and "Milestone" before "review" are gone) |
| | asks whether this environment can run a Milestone unattended | "whether one can run unattended" ("this environment" is gone) |
| | delivery itself is team-lead's | "delivery is team-lead's" |
| model-tiers (41 -> 32) | a skill tells you to run a step or subagent on a tier | same branch (the "need to know which model" clause is the purpose, in the first sentence) |
| release (68 -> 40) | wants to cut a release or plan the next one | same branch |
| | every issue of the current Release has closed | same branch |
| research (39 -> 36) | topic researched; docs or API facts gathered; reading legwork delegated to a background agent | same three branches |
| retro (55 -> 39) | asks for a retro or retrospective on a session or pull request | "asks for a retro or retrospective" |
| | what went wrong and how to stop it recurring | same branch |
| | the Retro backlog is retro-planning | same cross-reference |
| retro-planning (95 -> 38) | asks for Retro planning | "for Retro planning" |
| | when a Release ends | same branch |
| | resume one whose record is still open | same branch |
| | at a Release end agents decide every group | body only (the branch "when a Release ends" stays) |
| review-rounds (52 -> 32) | Round 0 hands over a Round or a Ticket check | same branch |
| | once agentic-review's Round 0 has picked a level | same |
| setup-dev-skills (74 -> 41) | the user sets up a repo for these skills | same branch |
| | the repo has no issue tracker or triage labels configured | "it has no tracker or triage labels configured" |
| | asks to update the tracker, label, domain-doc, release-doc or Boundary-record files | "or those files need updating" |
| setup-project (46 -> 37) | write or update a project's instructions | "write or update them" (first clause names the coordinator instructions) |
| | a new repo, kind of thread or standing rule means they are out of date | "a new repo, thread kind or standing rule makes them stale" |
| team-lead (124 -> 52) | planning is done and a Milestone's delivery starts | same branch |
| | at every wake while it runs (a worker reporting, a Harness notice, a check-in, the user writing) | same branch, same four wakes |
| | the user asks to pause or resume it | "on a request to pause or resume delivery" |
| to-spec (39 -> 38) | "write the spec"; "turn this into a spec"; "make a PRD" once the plan is settled | same three phrases |
| to-tickets (42 -> 37) | "break this into tickets"; "split into issues"; vertical slices of an existing spec | same three branches |
| triage (56 -> 37) | the user says "triage" | same branch |
| | asks to look at incoming issues or external PRs | same branch |
| | a Release thread runs the Triage batch | same branch |
| wayfinder (56 -> 41) | large, foggy effort too big for one session ("wayfind this", "map this out"), before any spec exists | same branch, same examples |
| wizard (47 -> 40) | provisioning infrastructure; credentials or CI secrets; an unfamiliar third-party dashboard; a one-off migration or cutover | same four branches ("unfamiliar" dropped) |
| | don't invoke it for steps the agent can perform itself | "not for steps the agent can do" |
| worker-control (84 -> 38) | a coordinator starts, reads, stops, pauses or schedules workers | same branch |
| | a caller needs the check that proves them | "a caller needs that check" |
