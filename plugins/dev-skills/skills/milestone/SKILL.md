---
name: milestone
description: "Plan a Milestone (a small Release is one), check the plugin version, report; delivery is team-lead's. Use when asked for a Milestone or small Release (cutting one, or planning an open Milestone's next one, is release's), or whether one can run unattended, or when a Milestone starts or reaches its review, or a feature is ready."
---

# Milestone

A **Milestone** is a product goal the user sets, written down in one Milestone issue, which agents deliver unattended across one or more Releases. Every plan is a Milestone: a small Release is a Milestone with one Release. Planning always involves the user; everything after it is agentic. This skill holds the parts that are the user's and the record: planning with the user, the Plugin version check and the report. Delivery, the work between them, is the `team-lead` skill's. In order:

1. **Planning**, with the user: the features are named, sorted and planned, then the Milestone issue is written and every feature in it is labelled.
2. **The Plugin version check**, once planning settles: one read that threads here load main's plugin text.
3. **Delivery**, run by the coordinator with the `team-lead` skill (see "Delivery"), once both phases before it are done.
4. **The report**, once every feature is merged or parked: it ends with a stop for the user's Milestone review ("Milestone review").

**No Milestone.** A project is inside a Milestone only while its Milestone issue is open: an open issue carrying a label in the Boundary record's Milestone label form, whose body is the Milestone rather than a feature. With none open, no delivery runs: the next plan the user makes starts one.

## Planning

A Milestone planning session runs it with the user, at the **premium** tier (`model-tiers`): it names, sorts and dispatches; the feature sessions, at **top**, do the design work. The Milestone issue is the user's agreement: everything agents later decide inside the Milestone rests on it, so every field comes from the user, a feature's issue the user planned or a default agreed in the draft, never a guess. It holds no boundaries, and planning asks about none: what agents may do, what needs the user's approval and the budget are the Boundary record's (`setup-dev-skills` changes it); a `## Boundaries` section in an earlier Milestone issue is history.

**The features are the user's.** A feature is a Spec with its Tickets, a lone Ticket with the issues it absorbs, or a few related issues the user agrees to treat as one. Agents may **propose** one (an open issue that serves the goal, or a gap between the goal and the features listed), each as one question saying why it might belong. A proposal the user does not take stays out, unlisted and unlabelled.

A feature is **planned** when its Spec and its Tickets are published, or, for a lone Ticket or each of a few related issues, when its issue holds an agent-ready brief with acceptance criteria. An existing issue the user names and says is planned counts, and needs no session.

**A one-Release Milestone.** For a small Release or one Release's worth of work, plan a Milestone with one Release: step 7 asks nothing and writes its defaults into the draft: one at a time, in an order that respects the graph of the features the user named; Acceptance holds only its first line; Excluded names the set-aside work left out in step 3, or `- None.`. The user may change any of them in step 8; a changed default is planned like any other field.

### Steps

1. **Read the setup.** Read the Boundary record (`docs/dev-skills/boundaries.md`) for its Milestone label form, and the tracker doc (`docs/dev-skills/issue-tracker.md`) for its operations. With no Boundary record, or one that names no Milestone label form, tell the user to run `setup-dev-skills` and stop: without the form there is no membership label. With an open Milestone issue, do only the planning steps whose result is missing; once its planning has settled, tell the user a feature asked for waits, as "Planning settles" says.
2. **Goal.** Ask for the outcome the user wants by the Milestone's end. Done when the user agrees a one-paragraph goal in their own words.
3. **Name the features.** First list the work set aside for this Milestone, with number, title and one line each: the last Milestone report's proposals for the next Milestone, open issues it names or that are titled for the next Milestone, and open `retro` issues at the `ready-for-human` role whose comment says they wait for the user's next Milestone planning. Ask which join; the rest stay set aside, and Excluded says so. Then ask which features deliver the goal. A Retro the user takes in is absorbed by its feature's Ticket (`issue-absorption`). Parts that must reach main in different Releases are lone Tickets with blockers, not one Spec; a decision ticket is not a feature, the build it feeds is. Done when the user has named every feature and answered every proposal.
4. **First dependency graph.** Sort the named features by dependency: a feature waits for another whose work it builds on. Show it, one line per feature naming those it waits for (or none), and change it until the user agrees it.
5. **One planning session per feature.** Plan no feature here. Ask the coordinator (where none runs, the user) to start one planning session per feature not yet planned, in graph order: a feature starts once each one it waits for has reported; independent features may run side by side. Each brief carries the Milestone's number (the one step 9's label carries), this session's link, the goal, the graph, what earlier sessions settled that it builds on, the planning skills (`grill-with-docs`, or `grilling` with no repo, loaded by name before the first question; then `to-spec` and `to-tickets`, or one lone Ticket) and the **top** tier. Each session reports its Spec and Ticket numbers, each Ticket's blockers, and any change to the goal, acceptance, exclusions or another feature, which you bring to the user; you keep the draft. On a resumed planning, read what each feature has published and ask the coordinator which sessions still run; restart only one that ended without its report. Done when every session has reported and every feature is planned.
6. **Second dependency graph.** Build the graph again from the Tickets' blockers: a feature waits for another when one of its issues is blocked by one of the other's. Show the user each dependency that changed since step 4.
7. **Build limit, acceptance and exclusions.** Unless the Milestone is a one-Release one, ask whether features are built one at a time or several at once (and how many), how the user will accept the Milestone at its review, and what is excluded. "Nothing excluded" is an answer; silence is not.
8. **Agree the draft.** Only once every named feature is planned, show the user the whole Milestone issue with its title and label, in the shape below, its rows ordered by the step 6 graph, and change it until the user agrees it.
9. **Write it.** The membership label fills the Boundary record's form with the next Milestone number: one more than the highest among the labels already in that form (1 when there are none); create it if the tracker lacks it. Create the Milestone issue (**Create an issue**), carrying the label, with the agreed text. Then, for each feature in order, apply the label (**Apply / remove labels**) to every open issue it holds (its own issue, its Tickets, the issues it absorbs or its related issues), and make its own issue a sub-issue of the Milestone issue (**Make an issue a sub-issue of a parent**) where it has no parent yet: the label, not the link, makes it a member. Read the Milestone issue and every labelled issue back.

Planning **settles** when the Milestone issue reads back as the user agreed it and every open issue of every feature it lists carries the label. Tell the user in one line, with the issue's link, and go on to the Plugin version check. From then on the Milestone's features are fixed until it ends: a feature planned later waits, unlabelled and titled for the next Milestone, where planning lists it first.

### The Milestone issue

Title: `Milestone <n>: <name>`, with the number of its label. Body:

```
## Goal

<the outcome the user wants by the Milestone's end, in the user's words>

## Features, in build order

<One at a time, in this order. | In this order, up to <k> at once.> Each feature is its own issue carrying `<label>`.

| # | Feature | Kind | Accepted when | After |
| --- | --- | --- | --- | --- |
| 1 | <issue link> <short name> | <Spec, lone Ticket or related issues> | <its acceptance criteria as the user agreed them, in short; its issue holds them in full> | <the # of each feature it waits for, or none> |

## Acceptance

- Every feature above is merged and its issue closed.
- <what the user will check at the Milestone review>

## Excluded

- <what is left out, and where it goes instead, if anywhere; or: None.>
```

Keep the headings, their order and the table's first four columns: the skills that run inside the Milestone read its goal, its features in order, their acceptance criteria and its exclusions from them. "After" holds the graph; the Tickets' blocker links in the tracker stay the detailed record. Extra columns and notes are fine.

## Plugin version check

The **Plugin version check**, run once planning settles, shows threads load main's plugin text.

- **Who:** the delivery session, when fresh (started after main's last plugin change) and able to load skills. Otherwise it starts one fresh **cheap**-tier worker (`model-tiers`) through `worker-control`, and no other.
- **Read:** invoke by name a plugin skill that only loads text; read where the runtime says it loaded it from; the plugin root holds that skill's `skills` folder. Compare that root's manifest version with main's, read from the source repository's remote. A load path inside a source checkout compares the checkout's commit with main's instead. A listed skill name proves nothing.
- **Record:** one Milestone issue comment headed `Plugin version check`: the load path and both values, read back.
- **Holds** if they match: one line to the user; delivery starts.
- **Mismatch**, or no load path reported: tell the user the cause (an installed plugin older than main runs rules main has changed) and the fix (update the plugin, then start fresh threads; in a Claude Code cloud environment, see `worker-control`'s Claude Code reference, "Keeping the plugin current in a cloud environment"). Delivery waits for the user's word, recorded on the Milestone issue.

## Delivery

Delivery is the `team-lead` skill's. Delivery starts once planning has settled and the Plugin version check holds, or the user's word to go on is recorded. Then the coordinator loads `team-lead` by name and runs it (a coordinator that cannot load it follows the project instructions `setup-project` writes for it, and starts a thread for each step that needs a skill, this skill's Plugin version check and report included): it reads this Milestone issue for the features and their order, and the Boundary record for the boundaries, and takes every worker action through `worker-control`. Until then nothing is built, labelled for a Release or started as a build thread for this Milestone.

## Milestone review

The team lead applies this gate at every wake of delivery, after reading the state and before starting work: re-read the latest Milestone agreement and each feature's issues, pull requests and Park state. When every planned feature is merged or is parked (a Spec blocked by its parked Ticket counts as parked, naming that Ticket), delivery stops for review. An open, unparked feature, even one blocked or outside the current Release, keeps this gate closed; a closed issue whose merge evidence is missing needs its merged state checked. Missing acceptance evidence is reported as unverified, not a success claim. A pause keeps reporting on hold until the user resumes. Finish any Release cut already in progress before reporting; an open Release containing parked work need not be falsely closed to reach review. If the final merged Release still needs its cut, the team lead starts that Release worker first and awaits its report; then re-read this gate. Its final checks and maintenance decisions must be available before reporting.

Once the gate holds and any final Release cut has finished, start no further build or Release planning. First read existing report comments: reuse an unchanged pending report as reporting.md's re-entry rule says, taking no duplicate action. For a new report, the team lead first ends the check-in as its "End of delivery" says; then follow [reporting.md](reporting.md) to gather evidence, post the report comment on the Milestone issue and stop for the user's Milestone review. Acceptance belongs to the user: the report marks the Milestone ready for review, leaves it open until the user accepts (reporting.md says what closes it), and makes no acceptance or proof-pass claim.
