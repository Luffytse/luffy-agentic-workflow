Each scenario below gives what I do, the line I act on, and any **NEED** where my instructions run out.

**One gap affects every brief.** "Every brief carries: … Review level". My instructions never say what the Review level is. **NEED:** the Review level value. It is probably in the Boundary record or CLAUDE.md, and I can't read either.

---

**1. "Plan Milestone 4"**
- **Act on:** "Start a planning thread with `milestone`." The table row "Milestone planning … | `milestone` | premium".
- **Start:** one thread on <model>.
  - Brief: skill `milestone`; Model tier premium; repo `orchard-team/orchard`; Review level (NEED); goal "make Orchard's billing dashboard production-ready".
  - There is no issue link yet, because no Milestone issue exists.
- **Tell the user:** the planning thread has started. It will first offer Milestone 3's two "Next Milestone" proposals ("It first offers work set aside…").
- **Record:** **NEED:** where a `start` record goes before any Milestone issue exists.

**2. Two features planned in parallel**
- **Act on:** the "Feature planning | `wayfinder`, `to-spec`, `to-tickets` | premium" row.
- **Start:** two threads on <model>. Each brief carries the required line: "You are planning a feature of Milestone 4, whose Milestone issue is not written yet; the planning thread is <link>. End with an issue holding its acceptance criteria. Report any change to the goal, acceptance, exclusions, order or Release split to the planning thread."
- **NEED:** which of the three skills each thread uses. My guess is `to-spec` for usage export, but I don't know the skill for a lone Ticket.

**3. Last year's data is listed under Excluded**
- **Act on:** the brief line "Report any change to … exclusions … to the planning thread."
- **Do:** tell the feature thread to send this to the planning thread (link). The planning thread owns the Milestone draft, so I don't decide it myself.

**4. Milestone issue #120 written and labelled**
- **Do first:** read #120 back ("A message is a reason to read, not the state itself").
- **Act on:** "Once the Milestone issue exists, start a verification thread with `milestone`."
- **Start:** one thread on <model> (regular).
  - Brief: `milestone` (Startup verification); regular; repo; Review level; #120 link.
  - Plus: "Source stamp: `4f2c9e1`. Compare it with the last commit on the plugin source repository's main that changed `team-lead` or `milestone`, and report both."
  - If it asks for a probe worker, I start one on <model> (cheap) and tell it what happened.
- **Record:** `start` on #120.

**5. Verdict: ready**
- **Commit 4f2c9e1:** the stamp has not moved. I act on "`Verdict: ready` means start delivery." I say nothing about `setup-project`.
- **Commit 9ab0c3d:** the stamp has moved. I act on "tell the user once to re-run `setup-project`, and carry on unless the user says to wait." I tell the user once and continue delivery. `setup-project` is the user's to run.

**6. Nothing running, no release issue open**
- **Act on:** all three Release conditions hold:
  - no Release thread is running;
  - no open, unparked issue carries an open release label;
  - a planned feature is open, unparked, unlabelled and unblocked.
- **Start:** a `release` thread on <model> (regular).
  - Brief: `release`; regular; repo; Review level; #120; `docs/dev-skills/release.md`; the last release issue cut, which I look up on GitHub Issues.
- **Record:** `start`.
- **Then:** "Start no Build thread while a Release thread runs."

**7. Release #125 planned**
- **Act on:** "Read the release issue back when it reports."
- **Do:** read #125, check its Order, and read #120's Order rule.
- **Slots:** min(2, Order rule).

**8. Start the Build threads**
- **Check-in first:** "Arrange an hourly check-in … before the first Build thread starts." I schedule my own hourly wake and post a `check-in` record on #120.
- **#121:** "Spec with Tickets: `implement-spec`". Tier comes from the issue's Model tier line, or regular if it has none.
- **#122:** "Lone Ticket: `implement`". Tier is chosen the same way. It starts now only if the Order rule allows 2 at once. Under "one at a time" it waits for #121.
- **Each brief carries:** skill, tier, repo, Review level, issue link, the #120 link, and both required build lines (load source and version, and following the checkout's `agent-skills/<name>/`).
- **Record:** `start` on each issue.

**9. Mid-Milestone requests**
- **CSV import:** "A feature the user plans joins that Milestone, unless the user says it's for the next one. Start a `milestone` thread to add it." I start a `milestone` thread on <model> (premium).
- **Empty-date crash:** "A bug the user raises goes to a `triage` thread, which files it." I start a `triage` thread on <model> (regular).
- **Record:** `start` for both.

**10. #121 asks for a version while #122's is out**
- **Act on:** "While one is out, it tells any other asking thread to wait and serves waiting threads in the order they asked."
- **Do:** tell #121 to wait; it is first in the queue.
- **Aside:** "patch for a fix" means a fix should get 2.4.1, not 2.5.0. I'd check whether #122 actually changed a skill.

**11. #122 merged; main reads 2.5.0**
- **Re-read first:** "Re-read after a skill merge … before any further thread starts." I re-read the open issues no running thread is building whose body names the changed skill, and update, close or comment on each.
- **Then serve #121** from main's 2.5.0, as the version line says:
  - **2.6.0** if billing is a new or changed skill;
  - **2.5.1** if #121 is a fix.
- **Record:** a comment on #121.
- **Slots:** #122's slot frees. Nothing else is in Order, and #121 still holds the open Release label, so I start no Release thread.

**12. #121 silent**
- **First check-in (90 minutes silent):** "Silent for an interval: nudge it once and record it." I nudge #121 and post a `nudge` record.
- **Next check-in, still silent:**
  1. I stop the thread and read the stop back from my harness. A success return is not enough.
  2. I start a replacement: `implement-spec`, same tier and Review level, from its pushed branch. I post a `start` record.
- **Park instead** if the stop doesn't read back or the fresh start fails. I'd then tell the user once.
- **Open question:** #121's version number is still out. I'd tell the replacement it holds 2.6.0 (or 2.5.1). My instructions don't cover this case.

**13. "The cut is blocked: #130 is open"**
- **Act on:** "tell the user in one line, post a `wait` record, and start no Release thread until something changes or the user writes."
- **Do:** read the release issue back, tell the user in one line, and post `wait`.

**14. Everything labelled is closed and merged**
- **Act on:** the review gate holds, so I follow the four steps:
  1. Finish the cut. If the final Release still needs it, start a `release` thread and wait.
  2. Start no more builds or Release planning.
  3. End the check-in, read back that it stopped, and record it.
  4. Start a `milestone` report thread on <model> (regular).
- **NEED:** how to tell whether a merged Release "still needs its cut". That is in `docs/dev-skills/release.md`, which I can't read.

**15. Report posted**
- **Act on:** "It stops for the user's review."
- **Do:** give the user the link and wait.

**16. "Invoice PDF fix is not right, send it back"**
- **Act on:** report re-entry: "re-read the agreement, resume only that work through delivery (re-arranging the check-in), and have a new report posted that links the prior one and names what changed."
- **Do:** ask the user one question: what is wrong? I re-arrange the check-in and record it.
- **NEED:** how a closed Ticket under a cut Release re-enters delivery. I don't know who reopens it, or whether it needs a new release issue and Order entry.

**17. New report posted, "Accepted."**
- **Act on:** "On acceptance (the user's own word), start a thread to close the Milestone issue." That is the row "closing the accepted Milestone | `milestone` | regular".
- **Start:** a `milestone` thread on <model> to close #120.
- **Record:** `start`.
