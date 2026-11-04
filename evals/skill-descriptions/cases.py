"""Cases of the skill-descriptions eval: realistic prompts or caller situations, each with the one skill a session
that sees only the skill listing should load first (or "none"). Prompts never name the expected skill (the one
exception list is ALLOW_NAME_IN_PROMPT: the user's own trigger word, as the description quotes it).

kind: trigger   - taken from a description's trigger branch, a caller that loads the skill by name, or a real
                  thread request; the expected skill is the obvious pick
      near-miss - sits next to a neighbour skill; the wording decides between the two
      none      - no skill applies
"""

# (id, kind, expected, prompt)
CASES = [
    # agentic-review
    ("agentic-review-t1", "trigger", "agentic-review", "Can you review PR 412 before we merge it?"),
    ("agentic-review-t2", "trigger", "agentic-review", "Review everything on this branch since the v2.3 tag."),
    ("agentic-review-t3", "trigger", "agentic-review", "The work for ticket 88 is done on its branch. Run the ticket check on it before we land it."),
    ("agentic-review-t4", "trigger", "agentic-review", "Review my uncommitted changes before I commit."),
    ("nm-review-rounds-1", "near-miss", "review-rounds", "Round 0 picked level Standard for pull request 77. Hand over now and run the first Round: the Finders and the Verifier."),
    # ask-matt
    ("ask-matt-t1", "trigger", "ask-matt", "I have a vague idea for a new feature. Which of your skills should I start with?"),
    ("ask-matt-t2", "trigger", "ask-matt", "How do these dev skills fit together, from idea to ship?"),
    ("ask-matt-t3", "trigger", "ask-matt", "I'm new to this plugin. Where do I begin on a new piece of work?"),
    # codebase-design
    ("codebase-design-t1", "trigger", "codebase-design", "I want to redesign the interface of our payment module so it is deeper and hides more behind fewer methods."),
    ("codebase-design-t2", "trigger", "codebase-design", "Where should the seam go between the parser and the renderer so each is easier to test?"),
    ("codebase-design-t3", "trigger", "codebase-design", "How can I make the cache module easier for AI agents to navigate and easier to test?"),
    ("nm-codebase-design-1", "near-miss", "codebase-design", "Just the Storage module: how should it expose its methods so that callers only see a small surface and the complexity stays inside?"),
    # diagnosing-bugs
    ("diagnosing-bugs-t1", "trigger", "diagnosing-bugs", "Users report the checkout endpoint throws a 500 intermittently. Can you debug this?"),
    ("diagnosing-bugs-t2", "trigger", "diagnosing-bugs", "The nightly import got three times slower since last week and I don't know why."),
    ("diagnosing-bugs-t3", "trigger", "diagnosing-bugs", "The login page just hangs after I click submit. Something is broken and I have no idea what."),
    ("nm-diagnosing-bugs-1", "near-miss", "diagnosing-bugs", "The CI run fails on a test that passes locally, and I can't tell whether it is the code or the environment. Find out."),
    # docs-index (hidden)
    ("docs-index-t1", "trigger", "docs-index", "A document-writing workflow is about to add a new page under docs/ and needs the documentation-index format and its update requirements."),
    ("docs-index-t2", "trigger", "docs-index", "A checker is assessing whether the documentation index has drifted from the files on disk. What does the contract require?"),
    ("docs-index-t3", "trigger", "docs-index", "I just added three new documents. What must be updated in the documentation index so it stays correct, and in what format?"),
    ("nm-docs-index-1", "near-miss", "docs-index", "We added a new ADR file; make sure the documentation index lists it the way the contract requires."),
    # domain-modeling
    ("domain-modeling-t1", "trigger", "domain-modeling", "Add a glossary entry for the term 'Finder' to our glossary."),
    ("domain-modeling-t2", "trigger", "domain-modeling", "We just decided to use a merge commit for Spec pull requests. Record this decision as an ADR."),
    ("domain-modeling-t3", "trigger", "domain-modeling", "Our team uses 'ticket' and 'issue' interchangeably and it keeps causing confusion. Let's pin down our terminology."),
    # grill-with-docs
    ("grill-with-docs-t1", "trigger", "grill-with-docs", "Grill me on my design for the new billing service. We're in the repo, and I want terms and decisions recorded as they settle."),
    ("grill-with-docs-t2", "trigger", "grill-with-docs", "Stress-test my plan to split the monolith while we work in this repo, and update the glossary and ADRs as we settle things."),
    ("grill-with-docs-t3", "trigger", "grill-with-docs", "grill me about the plan to migrate our auth. We're working in the project directory."),
    ("nm-grill-with-docs-1", "near-miss", "grill-with-docs", "Poke holes in my caching plan. We're in the repo."),
    # grilling
    ("grilling-t1", "trigger", "grilling", "I'm on my phone with no project open. Grill me on whether I should quit my job to start a company. Don't write anything down."),
    ("grilling-t2", "trigger", "grilling", "Interview me about this idea, but I only want the questions: no files, no notes saved anywhere."),
    ("grilling-t3", "trigger", "grilling", "There is no working directory in this session. Poke holes in my plan to relocate the team to Lisbon."),
    ("nm-grilling-1", "near-miss", "grilling", "Grill me on this plan in the repo, but don't record anything at all, not even glossary terms."),
    # handoff
    ("handoff-t1", "trigger", "handoff", "Hand off this conversation so a fresh agent can pick it up tomorrow."),
    ("handoff-t2", "trigger", "handoff", "I'm moving this work to a new directory and a different harness. Write up where we are so it can continue there."),
    ("handoff-t3", "trigger", "handoff", "Fork this side task off. Compact what we have done so far for another agent to continue from."),
    ("nm-handoff-1", "near-miss", "handoff", "Write up where this branch stands so my colleague can carry on tomorrow."),
    # implement
    ("implement-t1", "trigger", "implement", "You are the Ticket thread for issue #214, a bug fix that sits under no Spec. Build it and ship it."),
    ("implement-t2", "trigger", "implement", "Here is a lone ticket: a small chore to rename the config key. Take it from the issue to a merged pull request."),
    ("implement-t3", "trigger", "implement", "Take issue #305, a small feature under no Spec. Have it built test-first, review the pull request and merge it."),
    ("nm-implement-1", "near-miss", "implement", "Issue #77 is a lone bug fix. Write the failing test first, fix it, open the pull request, get it reviewed and merged."),
    # implement-spec
    ("implement-spec-t1", "trigger", "implement-spec", "You've been handed Spec #130 with its five Tickets already split out. Build it and ship it."),
    ("implement-spec-t2", "trigger", "implement-spec", "Spec thread: coordinate the Tickets of Spec #98 off one Spec branch and open the Spec pull request."),
    ("implement-spec-t3", "trigger", "implement-spec", "The Tickets of Spec #51 are published. Build each one in its own worktree and bring the Spec pull request to a merge."),
    ("nm-implement-spec-1", "near-miss", "implement-spec", "Build everything in Spec #200 and its Tickets, then merge it into main with a merge commit."),
    # improve-codebase-architecture
    ("improve-codebase-architecture-t1", "trigger", "improve-codebase-architecture", "Find refactoring candidates across the whole codebase."),
    ("improve-codebase-architecture-t2", "trigger", "improve-codebase-architecture", "Review the structure of this codebase and give me an HTML report of what to improve."),
    ("improve-codebase-architecture-t3", "trigger", "improve-codebase-architecture", "Improve the architecture of this project: show me your options, I'll pick one to dig into."),
    ("nm-improve-codebase-architecture-1", "near-miss", "improve-codebase-architecture", "Scan our whole repo and tell me which modules are worth turning from shallow into deep ones."),
    # issue-absorption (hidden)
    ("issue-absorption-t1", "trigger", "issue-absorption", "I am publishing a Ticket that absorbs issues #101 and #102. I need the record shape for that."),
    ("issue-absorption-t2", "trigger", "issue-absorption", "I'm reading the absorption records on this Ticket to see which issues it absorbed."),
    ("issue-absorption-t3", "trigger", "issue-absorption", "A pull request is about to merge. Select which absorbed issues belong in its closing lines and get closed."),
    # merging (hidden)
    ("merging-t1", "trigger", "merging", "A build workflow has reached its merge step: the review is done and the pull request is ready to go."),
    ("merging-t2", "trigger", "merging", "I must decide whether this action crosses a boundary or whether I can simply do it myself."),
    ("merging-t3", "trigger", "merging", "The review is finished. Write the Agent-merged rules line, sync with main and land the pull request."),
    ("nm-merging-1", "near-miss", "merging", "This pull request is ready to merge. Decide from the Boundary record who merges it, then confirm it landed and close its issues."),
    # milestone
    ("milestone-t1", "trigger", "milestone", "Plan a Milestone for the next set of features with me."),
    ("milestone-t2", "trigger", "milestone", "A feature came up mid-Milestone. Add it and update the Tickets it touches."),
    ("milestone-t3", "trigger", "milestone", "Every feature of the open Milestone is merged or parked. Write its report and stop for my review."),
    ("milestone-t4", "trigger", "milestone", "Can this environment run a Milestone unattended? Record the startup verification before delivery begins."),
    ("nm-milestone-1", "near-miss", "milestone", "I want to plan some new work as a small Release with goal, features in order, acceptance criteria and exclusions."),
    # model-tiers (hidden)
    ("model-tiers-t1", "trigger", "model-tiers", "A skill tells me to run this step on the premium tier. Which model is that in this coding agent?"),
    ("model-tiers-t2", "trigger", "model-tiers", "I need to start a subagent on the cheap tier and don't know which model that maps to."),
    ("model-tiers-t3", "trigger", "model-tiers", "Which model should I use for the regular tier here?"),
    # pr
    ("pr-t1", "trigger", "pr", "Write the title and body for this pull request."),
    ("pr-t2", "trigger", "pr", "Draft the description for the changes on my branch so I can open the pull request."),
    ("pr-t3", "trigger", "pr", "I pushed two more commits; update the pull request's title and body to match."),
    # prototype
    ("prototype-t1", "trigger", "prototype", "Before we commit to this state model for the shopping cart, build a throwaway version so I can see if it feels right."),
    ("prototype-t2", "trigger", "prototype", "I'm unsure what this settings screen should look like. Sketch a few UI variations I can click through."),
    ("prototype-t3", "trigger", "prototype", "Can you hack together a quick throwaway version of the undo logic so I can sanity-check it?"),
    ("nm-prototype-1", "near-miss", "prototype", "Don't build the real thing yet. Make something disposable that answers whether this interaction design works."),
    # release
    ("release-t1", "trigger", "release", "Every issue of the current Release has closed. Cut it."),
    ("release-t2", "trigger", "release", "Write the changelog entry for what we shipped and plan what goes in the next Release."),
    ("release-t3", "trigger", "release", "We're done with this Release: run the cut steps, close it and pick the next one up to the Release size."),
    ("nm-release-1", "near-miss", "release", "The Milestone's first Release has shipped. Plan its next Release from the ranked candidates."),
    # research
    ("research-t1", "trigger", "research", "Investigate how Stripe's idempotency keys work, using their official docs only, and save the findings as a Markdown file in the repo."),
    ("research-t2", "trigger", "research", "Gather the facts about Postgres logical replication limits from primary sources."),
    ("research-t3", "trigger", "research", "Hand the reading legwork on the OAuth device flow to a background agent while I keep working."),
    # retro
    ("retro-t1", "trigger", "retro", "Let's look back at this session. What went wrong, and how do we stop it recurring?"),
    ("retro-t2", "trigger", "retro", "Do a retrospective on pull request #310 and propose improvements to the agent's environment."),
    ("retro-t3", "trigger", "retro", "That session is finished. Which navigation pointers or automated checks would have helped it?"),
    ("nm-retro-1", "near-miss", "retro", "That session went badly. Propose changes to the docs and checks so it doesn't happen again."),
    # retro-planning
    ("retro-planning-t1", "trigger", "retro-planning", "Work through our Retro backlog with me."),
    ("retro-planning-t2", "trigger", "retro-planning", "A Release just ended. Group the open Retro issues by root cause and decide each group."),
    ("retro-planning-t3", "trigger", "retro-planning", "Pick up the planning pass over the Retro issues whose record is still open."),
    ("nm-retro-planning-1", "near-miss", "retro-planning", "Group our open retro issues by root cause and decide which ones become Tickets."),
    # review-record (hidden)
    ("review-record-t1", "trigger", "review-record", "I am writing the comment for Round 1 of a review. What shape does it take?"),
    ("review-record-t2", "trigger", "review-record", "Read back the earlier Round and Ticket-check comments on this pull request."),
    ("review-record-t3", "trigger", "review-record", "Explain to the reviewers what each Bug class and each Always-check means."),
    # review-rounds (hidden)
    ("review-rounds-t1", "trigger", "review-rounds", "Round 0 picked Deep for pull request 200. Run the Rounds, then sort what is still open after Round 3."),
    ("review-rounds-t2", "trigger", "review-rounds", "Round 0 handed over a Ticket check. Run it with Finders and a Verifier."),
    ("review-rounds-t3", "trigger", "review-rounds", "This is Round 2 of 3: run Finders, the Verifier, Rank, and post the one comment."),
    ("nm-agentic-review-1", "near-miss", "agentic-review", "Review this pull request. First size the review from the files it changes and decide how deep it needs to go."),
    # setup-dev-skills
    ("setup-dev-skills-t1", "trigger", "setup-dev-skills", "Set up this GitHub repo for the dev-skills plugin. It has no issue tracker or triage labels configured."),
    ("setup-dev-skills-t2", "trigger", "setup-dev-skills", "Update our repo's release doc and Boundary record files."),
    ("setup-dev-skills-t3", "trigger", "setup-dev-skills", "Create the labels these skills use and check the GitHub settings the build skills rely on."),
    ("nm-setup-dev-skills-1", "near-miss", "setup-dev-skills", "We added a new repo to this project. Set it up so the skills' tracker, labels and Boundary record work there."),
    # setup-project
    ("nm-setup-project-1", "near-miss", "setup-project", "We added a second repo to this project; the coordinator's instructions must cover how threads work there."),
    ("setup-project-t1", "trigger", "setup-project", "Write the project instructions my coordinator should read before it starts a thread."),
    ("setup-project-t2", "trigger", "setup-project", "We added a new kind of thread. Update our project's instructions so they still match."),
    ("setup-project-t3", "trigger", "setup-project", "Draft the instructions for this new project: how its threads work, not what state its work is in."),
    # tdd
    ("tdd-t1", "trigger", "tdd", "Build this feature test-first, with red-green-refactor."),
    ("tdd-t2", "trigger", "tdd", "Fix this bug test-first: write the failing test before you touch the code."),
    ("tdd-t3", "trigger", "tdd", "I want integration tests driving the new API endpoint, written before the implementation."),
    ("nm-tdd-1", "near-miss", "tdd", "Add the discount calculation, writing a failing test first and then making it pass."),
    # team-lead
    ("team-lead-t1", "trigger", "team-lead", "Planning is done and the Milestone's delivery starts now. Start the build workers in order."),
    ("team-lead-t2", "trigger", "team-lead", "A worker just reported that its pull request merged. React to it and start the next one within the limits."),
    ("team-lead-t3", "trigger", "team-lead", "The hourly check-in woke you. One worker has been silent for a long time; nudge it once, then replace it or park its work."),
    ("team-lead-t4", "trigger", "team-lead", "The user wrote: pause everything. Delivery is running."),
    ("team-lead-t5", "trigger", "team-lead", "Delivery was paused; the user just wrote: carry on."),
    ("nm-team-lead-1", "near-miss", "team-lead", "A Harness notice says a worker's thread ended while delivery runs. Decide what happens to its work."),
    # to-spec
    ("to-spec-t1", "trigger", "to-spec", "Write the spec from what we've discussed."),
    ("to-spec-t2", "trigger", "to-spec", "The plan is settled. Turn this conversation into a spec."),
    ("to-spec-t3", "trigger", "to-spec", "Make a PRD out of this conversation and publish it to the issue tracker."),
    ("nm-to-spec-1", "near-miss", "to-spec", "No more questions. Just synthesise everything we've agreed into a spec on the tracker."),
    # to-tickets
    ("to-tickets-t1", "trigger", "to-tickets", "Break this into tickets."),
    ("to-tickets-t2", "trigger", "to-tickets", "Split the spec into issues, as vertical slices."),
    ("to-tickets-t3", "trigger", "to-tickets", "Turn this plan into tracer-bullet tickets, each saying what blocks it, and publish them."),
    # triage
    ("triage-t1", "trigger", "triage", "Go through the incoming issues: sort each into bug or enhancement and set its state."),
    ("triage-t2", "trigger", "triage", "Look at the external pull requests that came in and tell me which are real."),
    ("triage-t3", "trigger", "triage", "A Release thread reached the Triage batch: sweep the backlog."),
    ("nm-triage-1", "near-miss", "triage", "Label these new issues as bug or enhancement and write an agent-ready brief for the ones that are clear."),
    # wayfinder
    ("wayfinder-t1", "trigger", "wayfinder", "This effort is far too big for one session and I can't even see the route. Wayfind this."),
    ("wayfinder-t2", "trigger", "wayfinder", "Map this out: we want to move everything to a new platform, nothing is clear and no spec exists yet."),
    ("wayfinder-t3", "trigger", "wayfinder", "Chart this foggy migration as a set of decision tickets and resolve them one at a time."),
    ("nm-wayfinder-1", "near-miss", "wayfinder", "I have a huge vague idea and nothing written down. Help me find the route before anyone writes a spec."),
    # wizard
    ("wizard-t1", "trigger", "wizard", "Walk me through setting up the CI secrets. These are steps only I can do."),
    ("wizard-t2", "trigger", "wizard", "Generate a guided script that takes me through provisioning the cloud infrastructure by hand."),
    ("wizard-t3", "trigger", "wizard", "I must do a one-off cutover with manual steps in a third-party dashboard. Make me an interactive guide for it."),
    # worker-control (hidden)
    ("worker-control-t1", "trigger", "worker-control", "The coordinator needs to start a worker. Detect how workers run in the tool we are in."),
    ("worker-control-t2", "trigger", "worker-control", "A caller needs the short check that proves the start, state, end and stop methods work here."),
    ("worker-control-t3", "trigger", "worker-control", "Schedule a check-in for the running workers and tell me how to stop or pause one in this tool."),
    ("nm-worker-control-1", "near-miss", "worker-control", "Which tools does this runtime give for starting and stopping workers, and how does a check-in get scheduled?"),
    # writing-for-agents
    ("writing-for-agents-t1", "trigger", "writing-for-agents", "I'm creating a new skill. Guide me on how to word it so the agent behaves predictably."),
    ("writing-for-agents-t2", "trigger", "writing-for-agents", "Edit our AGENTS.md so the agent takes the same process every run."),
    ("writing-for-agents-t3", "trigger", "writing-for-agents", "This skill file spends too much context. Rework its wording."),
    ("nm-writing-for-agents-1", "near-miss", "writing-for-agents", "Tighten the wording of the testing rules in this repo's CLAUDE.md."),
    # more near-misses: the neighbour pairs the issue names, in the other direction
    ("nm-to-tickets-1", "near-miss", "to-tickets", "The spec is published. Split it into issues the team can pick up one by one."),
    ("nm-domain-modeling-1", "near-miss", "domain-modeling", "Add the new term 'Round' to the glossary and note why we chose it."),
    # none
    ("none-1", "none", "none", "What's the capital of Australia?"),
    ("none-2", "none", "none", "Rename the variable x to count in utils.py."),
    ("none-3", "none", "none", "Explain what a closure is in JavaScript."),
    ("none-4", "none", "none", "Add a CSS rule that centres the login box on the page."),
    ("none-5", "none", "none", "Run the database migration script now; you have the credentials and it needs nothing from me."),
    ("none-6", "none", "none", "Translate this error message into plain English: ECONNREFUSED 127.0.0.1:5432."),
]

# Cases whose prompt carries the skill's own name because the description quotes it as the user's trigger word.
ALLOW_NAME_IN_PROMPT = {
    "milestone-t1", "milestone-t2", "milestone-t3", "milestone-t4",
    "release-t1", "release-t2", "release-t3", "nm-release-1",
    "triage-t3",
}


def load():
    """Returns the cases as dicts with keys id, kind, expected, prompt."""
    return [dict(id=i, kind=k, expected=e, prompt=p) for i, k, e, p in CASES]
