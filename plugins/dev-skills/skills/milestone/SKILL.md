---
name: milestone
description: "Plan a Milestone (a small Release is one), check the plugin version, report; delivery is team-lead's. Use when asked for a Milestone or small Release (cutting one, or planning an open Milestone's next one, is release's), to add a feature to one, or whether one can run unattended, or when a Milestone starts or reaches its review, or a feature is ready."
---

# Milestone

A **Milestone** is a product goal the user sets, written down in one Milestone issue, which agents deliver unattended across one or more Releases. Every plan is a Milestone: a small Release is a Milestone with one Release. Planning always involves the user; everything after it is agentic. This skill holds the parts that are the user's and the record: planning with the user, adding a feature, the Plugin version check and the report. Delivery, the work between them, is the `team-lead` skill's. In order:

1. **Planning**, with the user: the Milestone issue is written and every feature in it is labelled.
2. **The Plugin version check**, once planning settles: one read that threads here load main's plugin text.
3. **Delivery**, run by the coordinator with the `team-lead` skill (see "Delivery"), once both phases before it are done.
4. **The report**, once every feature is merged or parked: it ends with a stop for the user's Milestone review ("Milestone review").

**No Milestone.** A project is inside a Milestone only while its Milestone issue is open: an open issue carrying a label in the Boundary record's Milestone label form, whose body is the Milestone rather than a feature. With none open, no delivery runs: the next plan the user makes starts one.

## Planning

The coordinator runs it with the user, when the user asks for a Milestone or a small Release. The Milestone issue is the user's agreement: everything agents later decide on their own inside the Milestone (who merges, what goes into a Release, how a design question is answered) rests on it, so every field in it comes from the user, from a feature's issue the user planned, or from a default the user agreed in the draft, never from a guess. It holds no boundaries: what agents may do, what needs the user's approval and the budget are the repo's, in the Boundary record, for every Milestone. An action the user wants allowed or reserved is a change to the Boundary record, made with `setup-dev-skills`. A `## Boundaries` section in an earlier Milestone issue is history: the Boundary record decides for its issues too.

**The features are the user's.** A feature is a Spec with its Tickets, a lone Ticket with the issues it absorbs, or a few related issues the user agrees to treat as one. Agents may **propose** a feature: an open issue that serves the goal, or a gap between the goal and the features listed. Ask about each proposal as one question, saying why it might belong. Only the user adds a feature: a proposal the user does not take stays out, and nothing is listed or labelled for it.

**A one-Release Milestone.** When the user asks for a small Release or for one Release's worth of work, rather than for a Milestone, plan a Milestone with one Release: steps 4 and 5 ask nothing and write their defaults into the draft instead: one at a time, in the order the user named the features; Acceptance holds only its first line; Excluded names the set-aside work left out in step 3, or reads `- None.` when there is none. The user sees them in step 6 and may change any of them there; a default the user changes is planned like any other field.

### Steps

1. **Read the setup.** Read the Boundary record (`docs/dev-skills/boundaries.md`) for its Milestone label form, and the tracker doc (`docs/dev-skills/issue-tracker.md`) for its operations. With no Boundary record, or one that names no Milestone label form, tell the user to run `setup-dev-skills`, which writes it, and stop: without the form there is no membership label. Then look for an open Milestone issue. If one exists, carry on from what it holds: to add a feature, go to "Adding a feature mid-Milestone"; to finish an interrupted planning, do only the steps whose result is missing.
2. **Goal.** Ask for the outcome the user wants by the Milestone's end. Done when the user agrees a one-paragraph goal in their own words.
3. **Features.** First list the work already set aside for this Milestone (the last Milestone report's "Next Milestone" proposals, and open issues it names or that are titled for the next Milestone), with number, title and one line each, and ask which join; the ones left out stay set aside, and Excluded says so. Then ask which features deliver the goal. The user plans each one with an agent the usual way: `grill-with-docs` (or `grilling`), then `to-spec` and `to-tickets` for a multi-session feature, or one lone Ticket, in its own thread or here, as the user prefers. An existing issue counts as a feature once the user names it and says it is planned. A Retro the user takes in is absorbed by its feature's Ticket (`issue-absorption`). Parts that must reach main in different Releases are lone Tickets with blockers, not one Spec. A decision ticket is not a feature: the build it feeds gets its own issue with acceptance criteria. A feature planned in its own thread reports any change to the goal, acceptance, exclusions, order or Release split to the planning thread, which keeps the draft. Done when every feature the user named has its own issue holding its acceptance criteria, and the user has answered every proposal.
4. **Order.** Unless the Milestone is a one-Release one (above), ask the build order, and whether features are built one at a time or several at once (and how many).
5. **Acceptance and exclusions.** Unless the Milestone is a one-Release one, ask how the user will accept the Milestone at its review, and what is excluded. "Nothing excluded" is an answer; silence is not. Ask nothing about boundaries or a budget: they are the Boundary record's.
6. **Agree the draft.** Show the user the whole Milestone issue, its title and its label, in the shape below, and change it until the user agrees it.
7. **Write it.** The membership label fills the Boundary record's form with the next Milestone number: one more than the highest number among the labels already in that form (1 when there are none). Create the label if the tracker lacks it. Create the Milestone issue with the tracker doc's **Create an issue** operation, carrying the label, with the agreed text. Then, for each feature in order, apply the label (**Apply / remove labels**) to every open issue it holds (its own issue, its Tickets, the issues it absorbs or its related issues), and make its own issue a sub-issue of the Milestone issue (**Make an issue a sub-issue of a parent**) where it has no parent yet: the label, not the link, makes it a member. Read the Milestone issue and every labelled issue back from the tracker.

Planning **settles** when the Milestone issue reads back as the user agreed it and every open issue of every feature it lists carries the label. Tell the user in one line, with the issue's link, and go on to the Plugin version check. A feature planned after this point joins as "Adding a feature mid-Milestone" says.

### The Milestone issue

Title: `Milestone <n>: <name>`, with the number of its label. Body:

```
## Goal

<the outcome the user wants by the Milestone's end, in the user's words>

## Features, in build order

<One at a time, in this order. | In this order, up to <k> at once.> Each feature is its own issue carrying `<label>`.

| # | Feature | Kind | Accepted when |
| --- | --- | --- | --- |
| 1 | <issue link> <short name> | <Spec, lone Ticket or related issues> | <its acceptance criteria as the user agreed them, in short; its issue holds them in full> |

## Acceptance

- Every feature above is merged and its issue closed.
- <what the user will check at the Milestone review>

## Excluded

- <what is left out, and where it goes instead, if anywhere; or: None.>
```

Keep the headings, their order and the table's first four columns: the skills that run inside the Milestone read its goal, its features in order, their acceptance criteria and its exclusions from them. Extra columns and notes are fine.

### Adding a feature mid-Milestone

A feature the user plans while a Milestone is open **joins that Milestone**, unless the user says it is for the next Milestone. This is how any planning with the user ends while a Milestone is open, in whatever thread it runs: when the user asks to add a feature, takes one an agent proposed, or plans a new one (a Spec, or a lone Ticket that no listed feature holds). Do not ask which Milestone it is for. A feature for the next Milestone waits, unlabelled, for that Milestone's planning.

1. **Plan it with the user first**, as planning step 3 says. Until it is planned, nothing about it changes in the Milestone issue or its labels.
2. **Check the agreement.** When the feature would change the Milestone's goal, acceptance or exclusions (it adds something an exclusion leaves out, or needs a new acceptance line), ask the user one question naming that change. Until the user answers, list and label nothing for the feature; when the user declines, it does not join, and you say so. Ask nothing when it changes none of them.
3. **List it.** Put it where the user says in the order, or last when the user names no place (each Release planning re-orders the features anyway). Rewrite the Milestone issue's body with its row in that place, marked `(added <date> by the user)`, and with any agreement change the user agreed in step 2: read the whole body first, write it whole back with only those changes, and read it back.
4. **Label it**, only after the row is in: apply the label to every open issue it holds and link its own issue as a sub-issue, as in planning step 7.
5. **Update the Tickets it touches.** Read the Milestone's open Tickets (those carrying its label) and find each one the new feature touches: one whose text would be wrong once both have landed, because it names an output, a flag, a file or a behaviour the feature changes (its acceptance criteria or its tests would then check the old one), or because the feature makes its work redundant. Update it to the end state; do not leave the feature's own build to repair it. A Ticket the feature only builds on, or extends later without making its text wrong, is not touched. Leave out a Ticket whose build has started (it, or its Spec, has a pushed branch or an open pull request): it keeps the text it started with, and you name it in the report. For each other one, read its whole body, write it whole back with only the change the feature needs and a closing note, `_Updated for <the feature's issue link> (added to the Milestone <date>): <what changed>._`, and read it back. A change that would alter that Ticket's feature beyond what the user planned is not yours to make: ask the user as one question about that Ticket.

Listing before labelling keeps every labelled issue one the Milestone issue lists. A Release already planned keeps its scope; the new feature waits for the next Release planning. Tell the user in one line what was added, where, and which Tickets were updated or left out. A change to the goal, the acceptance or an exclusion at any other time is the user's too: write it the same way, once the user agrees it.


## Plugin version check

The **Plugin version check** shows threads load main's plugin text. Run it once planning settles.

- **Who:** the session that will run delivery, when it is fresh (started after main's last plugin change) and can load skills. Otherwise it starts one fresh worker at the **cheap** tier (`model-tiers`) through `worker-control`, and no other.
- **Read:** invoke by name a plugin skill that only loads text and read where the runtime says it loaded it from; the plugin root holds that skill's `skills` folder. Compare that root's manifest version with main's on the source repository, read from the remote. A load path inside a source checkout compares the checkout's commit with main's instead. A listed skill name proves nothing.
- **Record:** one comment on the Milestone issue headed `Plugin version check`: the load path and both values, read back.
- **Holds** when they match: one line to the user; delivery starts.
- **Mismatch**, or no load path reported: tell the user the cause (an installed plugin copy older than main runs rules main has changed) and the fix (update the plugin, then start fresh threads). Delivery waits for the user's word, recorded on the Milestone issue.

## Delivery

Delivery is the `team-lead` skill's. Delivery starts once planning has settled and the Plugin version check holds, or the user's word to go on is recorded. Then the coordinator loads `team-lead` by name and runs it (a coordinator that cannot load it follows the project instructions `setup-project` writes for it, and starts a thread for each step that needs a skill, this skill's Plugin version check and report included): it reads this Milestone issue for the features and their order, and the Boundary record for the boundaries, and takes every worker action through `worker-control`. Until then nothing is built, labelled for a Release or started as a build thread for this Milestone.

## Milestone review

The team lead applies this gate at every wake of delivery, after reading the state and before starting work: re-read the latest Milestone agreement and each feature's issues, pull requests and Park state. When every planned feature is merged or is parked (a Spec blocked by its parked Ticket counts as parked, naming that Ticket), delivery stops for review. An open, unparked feature, even one blocked or outside the current Release, keeps this gate closed; a closed issue whose merge evidence is missing needs its merged state checked. Missing acceptance evidence is reported as unverified, not a success claim. A pause keeps reporting on hold until the user resumes. Finish any Release cut already in progress before reporting; an open Release containing parked work need not be falsely closed to reach review. If the final merged Release still needs its cut, the team lead starts that Release worker first and awaits its report; then re-read this gate. Its final checks and maintenance decisions must be available before reporting.

Once the gate holds and any final Release cut has finished, start no further build or Release planning. First read existing report comments: reuse an unchanged pending report as reporting.md's re-entry rule says, taking no duplicate action. For a new report, the team lead first ends the check-in as its "End of delivery" says; then follow [reporting.md](reporting.md) to gather evidence, post the report comment on the Milestone issue and stop for the user's Milestone review. Acceptance belongs to the user: the report marks the Milestone ready for review, leaves it open until the user accepts (reporting.md says what closes it), and makes no acceptance or proof-pass claim.
