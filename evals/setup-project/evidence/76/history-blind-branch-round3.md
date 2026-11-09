# Orchard coordinator walk-through

**Gap that affects every brief:** "Every brief carries: skill, Model tier, repo `orchard-team/orchard`, Review level, and the issue link."
- **NEED:** where a thread's Review level comes from. My instructions never define Review levels. They are probably in the Boundary record, which I cannot read. Below I write it as `<Review level>`.

---

**1. "Let's plan Milestone 4"**
- **Instruction:** "When the user asks for a Milestone or a small Release, start a Milestone planning thread running `milestone`."
- **I start:** a Milestone planning thread.
  - Skill: `milestone` (Planning).
  - Tier: premium (<model>).
  - Brief: repo `orchard-team/orchard`, `<Review level>`, goal "make Orchard's billing dashboard production-ready", Milestone number 4.
  - Issue link: none exists yet, so I say so in the brief.
- **What the thread does:** it lists the set-aside work, including Milestone 3's two "Next Milestone" proposals, and asks which of it joins ("It first lists the work set aside…").
- **I tell the user:** planning has started, with the thread link.
- **I record:** nothing. There is no Milestone issue yet.

**2. Two feature planning threads**
- **Instruction:** "For each feature the user names, start a feature planning thread."
- **Thread A, "usage export":** a multi-session feature, so `to-spec`, then `to-tickets`.
- **Thread B, "invoice PDF fix":** a small feature, so `to-tickets` for one lone Ticket.
- Both run at tier premium.
- **Each brief carries:** skill, tier, repo, `<Review level>`, and the line "You are planning a feature of Milestone 4, whose Milestone issue is not written yet; the planning thread is `<planning thread link>`."

**3. Export should include last year's data, which is under Excluded**
- **Instruction:** "It reports any change to the goal, acceptance, exclusions, order or Release split to the planning thread."
- I tell the usage export thread to report this exclusion change to the planning thread, and I relay it there myself too.
- The planning thread settles it with the user. I do not decide it.

**4. Milestone issue #120 written, features labelled**
- **Instruction:** "Before any Build thread, start a verification thread running `milestone`'s Startup verification."
- **I start:** a Startup verification thread.
  - Skill: `milestone` (Startup verification).
  - Tier: regular (<model>).
  - Brief: repo, `<Review level>`, link to #120.
- **The brief lists these five lines:**
  - Run the Harness check and the Loaded skill version check.
  - Reuse rows from the last result only as `milestone` allows.
  - Ask me for any action only I can take, such as starting the probe thread.
  - Post `## Startup verification` with its Verdict on #120.
  - Compare the stamp `4f2c9e1` with the last commit on the plugin's main that changed `team-lead` or `milestone`, read from the remote, and report both.

**5. Verdict ready**
- **If the commit is `4f2c9e1`:** the stamp has not moved. "Delivery starts once planning has settled and the latest verification reads `Verdict: ready`." I tell the user nothing about the stamp.
- **If it is `9ab0c3d`:** the stamp moved.
  - **Instruction:** "tell the user once to re-run `setup-project`, and go on unless the user says to wait."
  - I send that one message and delivery still starts.

**6. No release issue, features open and unlabelled**
- **Release-start check:**
  - No Release thread runs.
  - No issue carries an open release issue's label.
  - A planned feature is open, unparked, unlabelled for a Release and unblocked.
- **I start:** a Release thread running `release`.
- **Brief:** #120, the release doc, and the last release issue cut (looked up in the tracker).
- **NEED:** the tier `release` names. The table says "*(see gaps)*" and no gaps section was given.
- **NEED:** the release doc's path.
- **What I hold:** "Start no Build thread while it runs."
- **Record:** a `start` record. Its location is my guess: on #120, since the thread builds no issue and the `wait` record goes "beside the Release thread's `start`".

**7. #125 planned, Order #121, #122**
- I read state fresh: #120's Order rule, #125 and its issues, Park states, blockers, branches, and Harness states.
- I confirm the Release thread has ended.
- **Slots** = the smaller of 2 and the Order rule.

**8. Start Build threads**
- **Check-in first.** "Arrange it just before the first Build thread starts."
  - I check that none already runs.
  - I schedule an hourly wake for myself.
  - I post `check-in` on #120.
- **#121** (a Spec with Tickets): `implement-spec`, at #121's Model tier, regular if none.
- **#122** (a lone Ticket): `implement`, at its tier, regular if none.
  - It starts now only if the Order rule allows two at once.
  - Under "one at a time" it waits until #121 is closed or parked.
- **Each brief carries:**
  - skill, tier, repo, `<Review level>`
  - the issue link and #120's link
  - the checkout-copy line
  - the line about recording load source, version, settings, usage and evidence
- **Record:** a `start` record on each issue, with thread id, skill, tier, Review level, time and session link.

**9. Mid-Milestone additions**
- **"Add a CSV import for usage too"**
  - **Instruction:** "A feature the user plans joins it, unless the user says it is for the next one."
  - **I start:** a premium thread running `milestone` (Adding a feature mid-Milestone) to list it, label it and update the Tickets it touches.
  - **NEED:** whether this addition also needs its own feature planning thread (`to-spec`, `to-tickets`). The instructions don't say.
- **"The dashboard crashes when the date range is empty"**
  - **Instruction:** "A bug the user raises goes to a `triage` thread, which files it."
  - **I start:** a `triage` thread at regular tier.
  - It joins the Milestone only if the user plans it as a feature.

**10. #121 asks for a version while #122 holds 2.5.0**
- **Instruction:** "One number is out at a time: while one is out, it tells any other asking thread to wait and serves waiting threads in the order they asked."
- I tell #121 to wait. It is first in the queue.

**11. #122 merged, main at 2.5.0, #121 asks again**
- **Re-read first.** "Right after such a merge, and before any further thread starts":
  - I read #122's pull request to see which skill it changed.
  - I re-read the open issues that no running thread builds and whose body names that skill.
  - I update, close or comment on each one.
  - All slots are held until the re-read is done.
- **Then I serve #121** from main's 2.5.0:
  - 2.6.0 if it is a new or changed skill under `agent-skills/billing/`;
  - 2.5.1 if it is a fix.
- I judge which from its pull request and record the number in a comment on #121.

**12. #121 silent**
- **At 90 minutes:** "Silent for an hour: nudge it once." I ask where it is and what blocks it, answered by a comment on #121, and post `nudge`.
- **At the next check-in, still silent:**
  - I stop it and read the stop back from the Harness.
  - Once it reads stopped, I start a fresh thread with the same skill, tier and Review level from its pushed branch.
  - I post `start` with "Takes over from …".
- **Park instead** if the stop does not read back or the fresh start fails. I post `parked` with the reason and whether a writer may remain, and tell the user once.
- **NEED:** what happens to the version number (2.6.0) still out to the stalled thread. The instructions don't say. My guess: the replacement keeps it.

**13. "The cut is blocked: #130 is open"**
- **Instruction:** "tell the user in one line what waits on what, and post a `wait` record. Do not restart it until that changes or the user writes."
- **I tell the user:** "release-m4-r1's cut (#125) waits on #130 `<title>` being closed."
- **I record:** `wait` beside the Release thread's `start`.

**14. All release-m4-r1 issues closed, all features merged**
- **Review gate:** "If the last merged Release still needs its cut, start that Release thread first and wait for its report." If #125 is not yet cut, I do that first.
- The gate also needs the CSV import from item 9 to be merged or parked, if it was planned.
- **Once the gate holds:**
  1. End the check-in, read back that it no longer runs, and record it.
  2. Start a report thread running `milestone` (report), regular tier, with #120's link.
  3. Stop for the user's review.

**15. Report posted**
- I tell the user the report is on #120 and is waiting for their review.
- I do nothing else ("Stop for the user's Milestone review").

**16. "invoice PDF fix is not right, send it back"**
- **Instruction:** "re-enters delivery for that work only, with the check-in arranged again."
- **I do:**
  - Arrange the check-in again and record it.
  - Deliver only #122's work.
  - Follow with a new report that links the earlier one.
- **NEED:** how a closed, Released issue is put back into delivery: reopen #122 or file a new issue, and whether it needs a new release label or Release thread. The instructions don't say.

**17. New report, user writes "Accepted."**
- **Instruction:** "On acceptance, in the user's own words, a chore thread closes the Milestone issue."
- **I start:** a chore thread, tier cheap (<model>).
  - Brief: skill none, repo, `<Review level>`, #120's link.
  - It closes #120, quoting the user's word "Accepted."
- The check-in was already ended at the gate before the new report.
