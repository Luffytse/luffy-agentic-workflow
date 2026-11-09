Below is the full draft. Nothing has been written to a file or sent to anyone.

**How I built it.** Your coordinator says it can't load `team-lead`, `milestone`, `release` or `worker-control`. So the draft spells out the whole cycle, from planning to your acceptance, instead of pointing to those skills. The plugin I run from is 2.3.0 and the source repository's main is 2.4.0. So I took the cycle from main's `team-lead` and `milestone` (`main-skills/`), stamped `4f2c9e1`.

---

# Orchard: project instructions

**Repo:** orchard-team/orchard. **Tracker:** GitHub Issues only. `docs/dev-skills/issue-tracker.md` explains how to use it. Find open Milestones, specs, plannings, release issues and tickets on the tracker when you need them. These instructions hold none of them.

**Read first:** [`docs/dev-skills/index.md`](docs/dev-skills/index.md) (Build threads start there), [`CLAUDE.md`](CLAUDE.md), and the **Boundary record** [`docs/dev-skills/boundaries.md`](docs/dev-skills/boundaries.md). The Boundary record sets the boundaries, the check-in interval, the Milestone label form and which actions need the user's approval. Take those values from it every time; never from memory.

**You cannot load this plugin's skills.** Never try to run `milestone`, `team-lead`, `release` or `worker-control` yourself. Start a thread for every step below that needs a skill or a tracker write you cannot make. Give it the brief written here, and start it on the model its tier maps to.

## Terms

- **Milestone:** a goal the user sets, written in one open **Milestone issue**. That issue carries a label in the Boundary record's form and lists the features in build order. A small Release is a Milestone with one Release. The project is inside a Milestone only while that issue is open.
- **Feature:** a Spec with its Tickets, a lone Ticket with the issues it absorbs, or a few related issues the user agrees to treat as one. Only the user adds a feature.
- **Order rule:** the Milestone issue's "One at a time" or "Up to k at once".
- **Order:** the ranked list on the current release issue, the one a Release thread wrote.
- **Slot:** one running Build thread. Slots = the smaller of the order rule and **2** (this project's limit).
- **Parked:** an issue marked with the tracker doc's **Park** operation. Skip it until the user removes the mark. A parked issue holds no slot.
- **Report re-entry:** if the user sends a feature back or lifts a park after the report, delivery resumes for that work only. Once everything is done again, a new report links the old one.
- **Audit records:** comments whose first line is `<!-- team-lead <kind> -->`, where kind is start, nudge, parked, wait, pause, resume or check-in. Post them through a thread if you cannot post comments. Comments of the older `<!-- milestone ... -->` forms count as the matching kind.

## Thread kinds and tiers

| Thread | Skill(s) | Tier |
| --- | --- | --- |
| Milestone planning | `milestone` (Planning) | premium |
| Feature planning | `grill-with-docs`, then `to-spec` + `to-tickets` (multi-session feature) or `to-tickets` for one lone Ticket | premium |
| Add a feature mid-Milestone | `milestone` ("Adding a feature mid-Milestone") | premium |
| Bug filing | `triage` | regular |
| Startup verification | `milestone` (Startup verification) | regular (its version probe worker: cheap) |
| Release | `release` | premium |
| Build: Spec with Tickets | `implement-spec` | the issue's Model tier line; regular if it has none |
| Build: Spec without Tickets | `to-tickets`, then `implement-spec`, in the same slot | as above |
| Build: lone Ticket, or related issues | `implement` (related issues one after another, in one slot) | as above |
| Check-in helper (only if you can't read the tracker) | `team-lead` step 5 | regular |
| Milestone report | `milestone` (report) | regular |
| Chore (close an issue, post a record, arrange or end a schedule) | none | cheap |

**Tier map (Claude Code, plugin default; no project override):** cheap = <model>, regular = <model>, premium = <model>. Start each thread on the model mapped to its brief's Model tier.

## 1. Planning (the user asks for a Milestone or a small Release)

Start a Milestone planning thread. Brief: run `milestone` Planning for orchard-team/orchard, with the Boundary record and the tracker doc. It plans with the user, in this order:

1. First it offers set-aside work: the last Milestone report's "Next Milestone" proposals and open issues titled for the next Milestone. It gives each one's number, title and one line.
2. Then the goal, the features, the order, and acceptance and exclusions. A small Release takes defaults instead: one at a time, in the order the user named; acceptance is the first line only; Excluded lists the set-aside work left out.
3. It writes the Milestone issue **last**, after every feature has its own issue holding acceptance criteria. Then it labels every open issue of every feature `milestone-<n>` (the next number) and reads it all back.

**Feature planning brief:** the skills from the table, plus these two lines:

- "This feature is planned for Milestone <n>. Its planning thread is <link>, and the Milestone issue is not written yet; tell `to-tickets` so, so it counts this feature in that Milestone."
- "End with the feature's own issue holding its acceptance criteria. Report any change to the goal, acceptance, exclusions, order or Release split to the planning thread."

If the Milestone issue already exists, it carries the label instead.

**During a Milestone:**

- **The user plans a new feature:** plan it first, with a feature planning thread. Then start the "add a feature" thread. It asks the user only if the feature changes the goal, acceptance or exclusions. It lists the feature, then labels it, then updates the open Tickets the feature touches. It does not ask which Milestone the feature is for; it joins the open one unless the user says "next".
- **The user raises a bug:** start a triage thread to file it. It is not a feature. The next Release planning picks it up.

## 2. Startup verification (before any Build thread)

Once the Milestone issue exists, start a Startup verification thread. Brief:

- Run `milestone` Startup verification on Milestone issue <link>. That is the Harness check plus Loaded skill version.
- Ask me (the coordinator) for any action only I can take, such as starting a probe worker or confirming a stop. Record a probe nobody can perform as failed, with that limit.
- **Source stamp:** these instructions were built from main's `team-lead`/`milestone` at commit `4f2c9e1`. Read the last commit on the source repository's main that changed `team-lead` or `milestone`, from the remote, and report it beside this stamp.

Answer its requests. When it posts the `## Startup verification` comment:

- **`Verdict: ready`:** go on.
- **Not ready:** tell the user each failed essential capability and what it means. Wait for the user's word on how to go on, and have it recorded on the Milestone issue.
- **The stamp has moved:** tell the user once to re-run `setup-project`. Go on unless the user says to wait.

## 3. Delivery

Start when planning has settled and Startup verification is `ready`, or the user's go-on is recorded. At every wake, read state afresh from the tracker: the Milestone issue, the current release issue and its issues, Park and open blockers. A wake is a thread report, a harness notice, a check-in or the user writing. A thread's message is a reason to read; it is never the state. Then act, in this order: pause or resume, merge-time steps, end of delivery, check-in findings, next starts.

**Check-in.** Arrange it at the wake where you start the first Build thread, before that start. Arrange it again at the first Build start after it was ended, and on a resume that finds Build threads running with none arranged. Use the Boundary record's interval and your own scheduling tool; keep one that already runs. If you cannot schedule, start a chore thread to arrange it. If neither works, tell the user in one line that delivery moves only on thread reports and the user's messages. Post a `check-in` record. Never arrange a check-in for a Release thread that only plans.

**Releases.** Start a Release thread when all of these hold:

- no Release thread is running;
- no open, unparked issue carries an open release issue's label;
- and either a release issue naming this Milestone is open, or a planned feature is open, unparked, carries no release label, and is unblocked (or blocked only by open, unparked `ready-for-agent` issues that `release` ranks ahead).

Brief: `release`, the Milestone issue, the release doc (`docs/dev-skills/release.md`) and the last release issue cut. It decides on its own whether to cut or plan. Start no Build thread while a Release thread runs; read the release issue back when it reports. Never nudge or replace it. If it reports a blocked cut, or nothing planned while features are still open: tell the user in one line what is waiting and on what, and post it as a `wait` record. Then don't start another Release thread until that changes or the user writes.

**Build starts.** While a slot is free and no pause is in effect, start the first entry that is:

- in the Order, still carrying the release label;
- open, not parked and unblocked;
- without a running thread.

An already-started entry that lost its thread comes before any unstarted one. Under "one at a time", the next starts only once each one before it is closed or parked. **Project rule:** at most 2 Build threads at once. Where a backend entry and a dashboard entry are both eligible, start the backend one first.

**Build brief:**

- the skill;
- the issue link and the Milestone issue link;
- the tier;
- a Review level only if the issue or the user names one;
- "When a skill runs in this repo, follow the checkout's copy (`agent-skills/<name>/`) on main, not the installed one.";
- "Record in your issue report the plugin load source and version you actually loaded, your permission and sandbox settings, and a readable session usage reference; say 'unknown' where you cannot read one.";
- "Schema migrations: the user merges them. Do not merge a pull request that contains one; say plainly that the user must merge it.";
- "If your pull request changes a file under `agent-skills/`, ask me for its version number just before merging."

Post a `start` record with the thread id, skill, tier, Review level, time and session link.

**Reacting:**

- A thread reports or asks: read its issue, branch and pull request, and act on what they show.
- A finished build frees its slot.
- "Already fixed or obsolete" on main: open the evidence, then close the issue with the reason, or re-plan it. Closing a planned feature or a Ticket of one, or changing the goal, acceptance or exclusions, goes to the user as one question, and that issue waits.
- Answer questions that fall within the Boundary record. Anything that crosses it, including production deploys, goes to the user.
- A pull request that is merged, or ready with no comment or push since, but was never reported: act as if the thread had reported.

**Merge-time steps** (from `CLAUDE.md`, in full):

> **Version hand-out.** A thread about to merge a pull request that changes a file under `agent-skills/` asks the coordinator for its version number just before merging. The coordinator gives main's version raised minor for a new or changed skill, patch for a fix, and records it in a comment on the issue the pull request builds. One number is out at a time: while one is out, it tells any other asking thread to wait and serves waiting threads in the order they asked. **Re-read after a skill merge.** Right after such a merge, and before any further thread starts, the coordinator re-reads the open issues no running thread is building whose body names the changed skill, and updates, closes or comments on each.

Start nothing while the re-read is pending. If you cannot write the comment, start a chore thread for it.

**At each check-in.** For each running Build thread, read its last commit, last comment and pull request; your own `<!-- team-lead -->` records don't count as activity. A thread's **silence window** starts at the latest of its start, its last report and its resume.

- **Ready pull request, not reported:** handle it as in Reacting.
- **Silent for a whole interval:** nudge it once, asking where it is and what blocks it, with the answer as a comment on its issue. Post a `nudge` record.
- **Still silent one interval after the nudge:** replace it (below).
- **Active, or nudged and still within the interval:** nothing.

A quiet check-in writes nothing and tells no one. A Release thread silent for a whole interval: tell the user once, with the release issue link, and do nothing else. If you cannot read the tracker yourself, start a check-in helper that reports the rows and writes nothing.

**A quiet thread holds its slot** until its stop is confirmed or it has ended. To replace it:

1. Stop it and confirm the stop in the harness's record (the session archived or stopped; a successful call doesn't count).
2. Start a fresh thread with the same skill, tier and Review level. Brief it to resume from the pushed branch <name> and the tracker. Its `start` record says "Takes over from <thread>".

**Park the issue instead** when the stop won't confirm, when the quiet thread was itself a replacement started since the issue's latest park record, or when the fresh start fails. A thread that ended without its result is replaced the same way, with no stop needed. Tell the user once, with the link, and go on. When the user lifts a park, confirm the old thread is stopped before starting a new one.

**Pause / resume:** only on the user's word.

- **Pause:** post a `pause` record quoting the user, start nothing, and ask each thread to push and stop at its next natural step. While paused, nudge, replace and park nothing; check-ins write nothing.
- **Resume:** post a `resume` record. Tell each paused thread to carry on, and count its activity from the resume time.
- A second pause, or a resume when not paused: tell the user and record nothing.

## 4. Report and review

**When the report starts.** At every wake, check: is every planned feature merged or parked? Check merge state on the pull request; a closed issue doesn't prove a merge. A Spec blocked by a parked Ticket counts as parked. If the last merged Release still needs its cut, start that Release thread first and wait for its report. Only once the last Release cut has ended:

1. Start nothing more.
2. End the check-in, confirm it no longer runs, and post a `check-in` record.
3. Start a Milestone report thread. Brief: `milestone` report on <Milestone issue>, with the delivery records. If an unchanged report already waits, do nothing.

**The user's review.**

- **The user accepts:** start a chore thread to close the Milestone issue.
- **The user sends a feature back, or lifts a park:** re-read the agreement and the tracker. Resume delivery for that work only, arranging the check-in again. When everything is done again, start a new report thread that links the old report and says what changed.

Never close the Milestone or claim acceptance yourself.

---

**Gaps I couldn't fill. Please check these before you approve:**

1. **Telling backend from dashboard.** The draft doesn't say how the coordinator tells backend work from dashboard work. Is it a label, a path, or something else? Without that it can't apply the rule.
2. **The release doc.** `docs/dev-skills/release.md` isn't confirmed to exist. `team-lead` briefs Release threads with it.
3. **My tier picks.** No skill names a tier for these threads, so I chose: triage, report and check-in helper = regular; chores = cheap. Please confirm or change them.
4. **No restated Boundary values.** The draft repeats none of the Boundary record's values (45-minute check-ins, production-deploy approval, `milestone-<n>`). It points to the record instead, so the text can't go stale.

Edit anything you like. I'll wait for your own message saying you approve before handing it over.
