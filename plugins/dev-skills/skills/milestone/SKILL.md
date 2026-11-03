---
name: milestone
description: "Plan a Milestone with the user and report at its end: write the Milestone issue (goal, features in order with acceptance criteria, exclusions, budget, boundaries, membership label), add a feature mid-Milestone, record Startup verification (the `worker-control` check plus the loaded skill version) before delivery starts, and, once every feature is merged or parked, write the Milestone report and stop for the user's Milestone review. Delivery itself is the `team-lead` skill's. Use when the user asks for a Milestone or to add a feature to one, when a Milestone is about to start, when its delivery reaches the Milestone review, or when the user asks whether this environment can run a Milestone unattended."
---

# Milestone

A **Milestone** is a product goal the user sets, written down in one Milestone issue, which agents deliver unattended across one or more Releases. This skill holds the parts that are the user's and the record: planning with the user, adding a feature, Startup verification and the report. Delivery, the work between them, is the `team-lead` skill's. In order:

1. **Planning**, with the user: the Milestone issue is written and every feature in it is labelled.
2. **Startup verification**, once the Milestone issue exists: proof that this environment can run delivery unattended.
3. **Delivery**, run by the coordinator with the `team-lead` skill (see "Delivery"), once both phases before it are done.
4. **The report**, once every feature is merged or parked: it ends with a stop for the user's Milestone review ("Milestone review").

**No Milestone.** A project is inside a Milestone only while its Milestone issue is open: an open issue carrying a label in the Boundary record's Milestone label form, whose body is the Milestone rather than a feature. Until the user asks for one, this skill changes nothing: the project's own instructions and the other skills behave as they do with no Milestone.

## Planning

The coordinator runs it with the user, when the user asks for a Milestone. The Milestone issue is the user's agreement: everything agents later decide on their own inside the Milestone (who merges, what goes into a Release, how a design question is answered) rests on it, so every field in it comes from the user or from a feature's issue the user planned, never from a guess.

**The features are the user's.** A feature is a Spec with its Tickets, a lone Ticket with the issues it absorbs, or a few related issues the user agrees to treat as one. Agents may **propose** a feature: an open issue that serves the goal, or a gap between the goal and the features listed. Ask about each proposal as one question, saying why it might belong. Only the user adds a feature: a proposal the user does not take stays out, and nothing is listed or labelled for it.

### Steps

1. **Read the setup.** Read the Boundary record (the one the project's `CLAUDE.md` or `AGENTS.md` points to, usually `docs/agents/boundaries.md`) for its Milestone label form, its approvals and its budget, and the tracker doc (`docs/agents/issue-tracker.md`) for its operations. With no Boundary record, or one that names no Milestone label form, tell the user to run `setup-dev-skills`, which writes it, and stop: without the form there is no membership label. Then look for an open Milestone issue. If one exists, carry on from what it holds: to add a feature, go to "Adding a feature mid-Milestone"; to finish an interrupted planning, do only the steps whose result is missing.
2. **Goal.** Ask for the outcome the user wants by the Milestone's end. Done when the user agrees a one-paragraph goal in their own words.
3. **Features.** Ask which features deliver the goal. The user plans each one with an agent the usual way: `grill-with-docs` (or `grilling`), then `to-spec` and `to-tickets` for a multi-session feature, or one lone Ticket, in its own thread or here, as the user prefers. An existing issue counts as a feature once the user names it and says it is planned. Done when every feature the user named has its own issue holding its acceptance criteria, and the user has answered every proposal.
4. **Order.** Ask the build order, and whether features are built one at a time or several at once (and how many).
5. **Acceptance and limits.** Ask how the user will accept the Milestone at its review, what is excluded, the budget (the Boundary record's, or a tighter one for this Milestone), and any boundaries beyond the Boundary record: an action this Milestone's issues may also take, or one that needs the user's approval. "None beyond the Boundary record" is an answer; silence is not.
6. **Agree the draft.** Show the user the whole Milestone issue, its title and its label, in the shape below, and change it until the user agrees it.
7. **Write it.** The membership label fills the Boundary record's form with the next Milestone number: one more than the highest number among the labels already in that form (1 when there are none). Create the label if the tracker lacks it. Create the Milestone issue with the tracker doc's **Create an issue** operation, carrying the label, with the agreed text. Then, for each feature in order, apply the label (**Apply / remove labels**) to every open issue it holds (its own issue, its Tickets, the issues it absorbs or its related issues), and make its own issue a sub-issue of the Milestone issue (**Make an issue a sub-issue of a parent**) where it has no parent yet: the label, not the link, makes it a member. Read the Milestone issue and every labelled issue back from the tracker.

Planning **settles** when the Milestone issue reads back as the user agreed it and every open issue of every feature it lists carries the label. Tell the user in one line, with the issue's link, and go on to Startup verification. A feature planned after this point joins as "Adding a feature mid-Milestone" says.

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

- <what is left out, and where it goes instead, if anywhere>

## Boundaries

- **Budget:** <the limit, or none>
- <each boundary beyond the Boundary record, or: None beyond the Boundary record.>
```

Keep the headings, their order and the table's first four columns: the skills that run inside the Milestone read its goal, its features in order, their acceptance criteria, its exclusions and its boundaries from them. Extra columns and notes are fine.

### Adding a feature mid-Milestone

When the user asks to add a feature while the Milestone runs, or takes one an agent proposed:

1. **Plan it with the user first**, as planning step 3 says. Until it is planned, nothing about it changes in the Milestone issue or its labels.
2. **List it.** Ask where it goes in the order. Rewrite the Milestone issue's body with its row in that place, marked `(added <date> by the user)`: read the whole body first, write it whole back with only that change, and read it back.
3. **Label it**, only after the row is in: apply the label to every open issue it holds and link its own issue as a sub-issue, as in planning step 7.

Listing before labelling keeps every labelled issue one the Milestone issue lists. A Release already planned keeps its scope; the new feature waits for the next Release planning. Tell the user in one line what was added and where. A change to the goal, the acceptance, an exclusion or a boundary is the user's too: write it the same way, once the user agrees it.


## Startup verification

Autonomous delivery assumes the coordinator can start workers, read what they really did, confirm a stop and be woken, and that threads run the skill version on main. **Startup verification** proves this in this environment before delivery starts, each probe one short, bounded action whose pass rests on evidence observed afterwards, never on a call returning success. It has two parts, run by the agent that will start and stop the workers during delivery (the coordinator, or a verification thread started with this skill), at the **regular** tier (load `model-tiers` by name for the model each tier is in your coding agent; the project's own tier map overrides it):

1. **The Harness check.** Load `worker-control` by name and run its check. It detects how workers run here, loads the reference for that Harness (or reads the Harness's own docs where it has none), and proves starting, state, pause and resume, confirmed stop, end or failure notice and the check-in. Its result is the first part of this one.
2. **Loaded skill version**, below.

### Loaded skill version

A **fresh thread** is one whose session started after the plugin's last change on main: it loaded the plugin the way a new delivery thread would. A verification thread started for this run usually is one; check it by comparing its session start time with the time of main's last commit to the plugin. A subagent shares its parent's session, so it reads its parent's load, never a fresh one.

- **Codex:** use a fresh consuming project's runtime skill catalog to identify the enabled plugin's path, then invoke that skill and read its installed root's manifest. Record the consumer's runtime and configuration. A source-checkout path does not pass the installed-plugin check. An isolated installation can test a proposed setup, but its result stays separate from the delivery runtime's result; a stale installed copy there still fails. Bring any required setup to the user during Milestone planning.
- **Action:** in a fresh thread, invoke by name one skill of this plugin that only loads text (for example `model-tiers`), and read where the runtime says it loaded the skill from (its base directory). The plugin's root is the folder that holds that skill's `skills` folder; read the version in the plugin manifest there. Then read the version in the same manifest on the main branch of the plugin's source repository, from the remote: a local checkout may be behind. If the runner is a fresh thread, it does this itself. Otherwise it starts one fresh worker thread at the **cheap** tier, through `worker-control`, briefed to do the reading and post it in one comment on the Milestone issue whose first line is `<!-- startup-verification marker <token> -->` (a fresh token: `sv-version-` and 8 random hex characters), followed by the load path and the version exactly as read; the runner reads that comment back from the tracker, once more a minute later if it is missing.
- **Pass:** the runtime reported a load path, and the version in that plugin root's manifest equals main's. Record the load path, both versions, main's commit and the thread's session start time.
- **Fail:** the versions differ (limit: loaded `<version>`, main `<version>`, a stale cache); the runtime does not say where it loaded the skill from (limit: load path not reported); no fresh thread can be read (limit: not a fresh thread, with the thread's session start time); or main's manifest cannot be read (limit). The skill's name showing in the thread's skill list is not a pass: a stale copy carries the same names.
- **Limits** to record even on a pass: a load path inside a source checkout, rather than an installed or synced plugin folder, means threads here load that checkout, so record its branch and commit and say the version is the checkout's, not an installed one's; equal versions do not show equal text where a skill change can merge without a version bump; a worker thread's reading is its own report of what its runtime said, read from the tracker.

### The result

Post one comment on the Milestone issue, headed `## Startup verification`: the check's Harness, Runtime line and capability rows as it reported them, one more row for Loaded skill version in the same columns (essential: yes), and one Verdict over all the rows: `Verdict: ready`, or `Verdict: not ready: <each failed essential capability>`. Every probe worker has ended and every check-in the run arranged is ended before the comment is posted (the check's clean-up says how).

When an essential capability failed, tell the user before any delivery starts, naming each one with what it means: the check's own text for its capabilities, and for **Loaded skill version** that threads here may run other skill text than main's, so they can follow rules main has since changed, and a stale cache goes unnoticed. Delivery does not start until the user says how to go on; record that word on the Milestone issue, naming each failed capability delivery starts without. With every essential capability passing, say so in one line with a link to the result comment.

## Delivery

Delivery is the `team-lead` skill's. Once planning has settled and the latest Startup verification result reads `Verdict: ready` (or the user's word to go on is recorded, as above), the coordinator loads `team-lead` by name and runs it: it reads this Milestone issue for the features, their order and the boundaries, and takes every worker action through `worker-control`. Until then nothing is built, labelled for a Release or started as a build thread for this Milestone.

## Milestone review

The team lead applies this gate at every wake of delivery, after reading the state and before starting work: re-read the latest Milestone agreement and each feature's issues, pull requests and Park state. When every planned feature is merged or is parked (a Spec blocked by its parked Ticket counts as parked, naming that Ticket), delivery stops for review. An open, unparked feature, even one blocked or outside the current Release, keeps this gate closed; a closed issue whose merge evidence is missing needs its merged state checked. Missing acceptance evidence is reported as unverified, not a success claim. A pause keeps reporting on hold until the user resumes. Finish any Release cut already in progress before reporting; an open Release containing parked work need not be falsely closed to reach review. If the final merged Release still needs its cut, the team lead starts that Release worker first and awaits its report; then re-read this gate. Its final checks and maintenance decisions must be available before reporting.

Once the gate holds and any final Release cut has finished, start no further build or Release planning. First read existing report comments: reuse an unchanged pending report as reporting.md's re-entry rule says, taking no duplicate action. For a new report, the team lead first ends the check-in as its "End of delivery" says; then follow [reporting.md](reporting.md) to gather evidence, post the report comment on the Milestone issue and stop for the user's Milestone review. Acceptance belongs to the user: the report marks the Milestone ready for review, leaves it open, and makes no acceptance or proof-pass claim.
