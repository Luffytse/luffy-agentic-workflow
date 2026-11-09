# Orchard coordinator walkthrough

**Standing NEED (applies to every read or write below):** "Do every tracker read and write with that doc's named operations." I can't read `docs/dev-skills/issue-tracker.md`. So I don't know the exact form of **Park**, **Count open blockers**, **Comment on an issue**, or how to look up release issues and labels. Where a scenario says I read or post something, it assumes that doc. Otherwise I hand the write to a cheap chore thread that can read it.

---

**1. Plan Milestone 4**
- **Act on:** "Start one Milestone planning thread running `milestone`."
- **Thread:** `milestone`, tier premium (<model>), repo `orchard-team/orchard`. The brief tells it to:
  - read the Boundary record and the tracker doc;
  - first list the work set aside for this Milestone (Milestone 3's two "Next Milestone" follow-ups, plus open issues named or titled for the next Milestone), and ask the user which of it joins;
  - then plan the features with the user;
  - write the Milestone issue last, titled `Milestone <n>: Billing dashboard production-ready`, with `<n>` = highest `milestone-<n>` label + 1 and label `milestone-<n>`;
  - label every open issue of each feature and read everything back.
- **Gap:** "Every brief carries … the issue link", but no issue exists yet. I'd write "Milestone issue: not yet written."
- **Tell the user:** "Started the Milestone 4 planning thread; it'll first ask which of M3's two follow-ups join."
- **Record:** nothing. The audit trail has no `start` record for a planning thread with no issue.

**2. Two features planned in parallel**
- **Act on:** "Feature planning briefs."
- **Usage export:** I take "a Spec" as settled, so the thread runs `to-spec` then `to-tickets`. If the user calls it unclear, it runs `wayfinder` first.
- **Invoice PDF fix:** "a lone Ticket runs `to-tickets` for one Ticket."
- **Both threads:** premium (<model>), repo, and the line: "You are planning a feature of Milestone 4, whose Milestone issue is not written yet; the Milestone planning thread is <planning thread link>."
- **Guess:** I also tell the planning thread these two run in their own threads.

**3. Export should include last year's data (listed as Excluded)**
- **Act on:** "It reports any change to the goal, acceptance, exclusions, order or Release split to the planning thread."
- **Do:** relay the report verbatim to the Milestone planning thread, so the draft's Excluded list is settled there with the user. I tell the feature thread to send such changes to the planning thread directly.
- The delivery rule "ask the user as one question" is in Delivery, so it doesn't apply yet.

**4. Milestone issue #120 written**
- **Act on:** "A message is a reason to read." I read #120 and its labelled issues back.
- **Then act on:** "Once the Milestone issue exists, start a Startup verification thread."
- **Thread:** `milestone` (Startup verification), regular (<model>), repo, issue #120. Brief line: "Source stamp `4f2c9e1`: compare it with the latest commit on the plugin source repository's main that changed `team-lead` or `milestone`, and report both."
- When it asks me to start its version probe, I start `model-tiers` on cheap (<model>) and tell it what happened.

**5. Verdict: ready, commit 4f2c9e1**
- **Act on:** "Delivery starts only when the result reads `Verdict: ready`."
- 4f2c9e1 matches the stamp, so there's nothing to tell the user. I check the Runtime line, and tell the user only if it names another environment. Delivery starts.
- **If it had been 9ab0c3d:** "If the stamp has moved, tell the user once to re-run `setup-project`, then go on unless the user says to wait." I tell the user: "Plugin source moved (4f2c9e1 → 9ab0c3d); please re-run `setup-project` when you can. I'm carrying on unless you say wait." Then I start delivery.

**6. First delivery wake**
- **Read:** #120, release issues (none open), each feature's Park and open blockers, branches, workers. No pause, no merge-time step, no end, no check-in findings.
- **Release conditions all hold:** no Release thread runs; no open release label; features are open, unparked, unlabelled and unblocked.
- **Thread:** `release`, premium (<model>), repo. Brief: Milestone issue #120, `docs/dev-skills/release.md`, and last release issue cut. I'll put "none for M4"; whether M3's last cut belongs here is a guess.
- **Record:** `start` on #120, because "on the Milestone issue if it only plans".
- **Not yet:** no check-in, because it's arranged "just before the first build thread starts".

**7. Release issue #125 planned (Order: #121, #122)**
- **Do:** read #125 back. The Release thread is done, so builds may start.
- **Slots:** I read #120's Order rule. Slots = min(2, order rule).
- **Check-in, just before the first build:** I ask whether an earlier check-in still runs, and keep it if so. Otherwise I arrange one hourly, aimed at this session, and post a `check-in` record on #120.

**8. Start builds**
- **#121:** `implement-spec`, tier from #121's Model tier line (regular/<model> if none).
- **#122:** `implement`, tier the same way.
- **Each brief:** skill, tier, repo, Review level (only if named), issue link, Milestone #120, "Follow the checkout's copy of each skill (`agent-skills/<name>/`) on main, not the installed one, as CLAUDE.md says", and the evidence line.
- **Record:** a `start` record on each issue (worker id, skill, tier, Review level, time, session ref).
- **If #120 says "one at a time":** only #121 starts.

**9. Mid-Milestone requests**
- **CSV import:** "A feature the user plans joins it unless the user says it's for the next one. Plan it first."
  - Start a premium feature planning thread. Its scope is unknown, so I'd say `wayfinder` → `to-spec` → `to-tickets` (guess).
  - When it's planned, start a `milestone` thread for "Adding a feature mid-Milestone". I'd use premium; the tier for this isn't mapped (guess).
  - **NEED:** brief wording for a feature planned while the Milestone issue exists. The only wording says "whose Milestone issue is not written yet", and that wording is what makes `to-tickets` count it in the Milestone.
- **Empty-date-range crash:** "start a `triage` thread to file it." Regular (<model>), repo, Milestone #120.
  - **NEED:** whether a filed bug joins Milestone 4 (gets `milestone-4`) or waits. The instructions don't say.

**10. #121 asks for a version while 2.5.0 is out**
- **Act on:** "One number is out at a time: while one is out, it tells any other asking thread to wait and serves waiting threads in the order they asked."
- **Tell #121:** "Wait; a number is out. I'll serve you when #122's merge lands."

**11. #122 merged, main reads 2.5.0**
- **Re-read first:** "Right after such a merge, and before any further thread starts", I read #122's PR to see which skill changed. Then I re-read open issues that no running thread is building and whose body names that skill, and update, close or comment on each. If I can't make those writes, a cheap chore thread does. "The re-read holds all slots." #122's slot frees.
- **Then serve #121:** a changed skill (`billing`), so main 2.5.0 raised minor gives **2.6.0**. I record it in a comment on #121.

**12. #121 silent 90 minutes, then still silent**
- **First check-in:** "Silent for a whole interval: nudge it once." I ask where it is and what blocks it, answered on #121, and post a `nudge` record on #121.
- **Next check-in:** "Still silent after the nudge: stop it and read the stop back."
  - Once the stop reads back as stopped, I start a fresh `implement-spec` thread with the same tier and Review level, from its pushed branch. Its `start` record adds "Takes over from <old id>".
  - If the stop doesn't read back, or the fresh start fails, I **Park** #121, post `parked`, and tell the user once.
  - The slot stays held until the stop reads back.

**13. Cut blocked: #130 is open**
- **Act on:** "tell the user in one line and post that line as a `wait` record."
- **Tell the user:** "Release cut for #125 is blocked: #130 is still open." The same line goes as a `wait` record beside the Release `start` record.
- No new Release thread until that changes or the user writes.

**14. All release-m4-r1 issues closed, all features merged**
- The gate holds, so I follow steps 1–5:
  1. Read #125. If its cut is still needed, start a premium `release` thread and wait for its report.
  2. After the cut, start no build or Release planning.
  3. End the check-in (or have a cheap chore thread do it), read back that it no longer runs, and record it on #120.
  4. Start a `milestone` report thread, regular (<model>), on #120.
  5. Stop for review.

**15. Report posted**
- Read it on #120.
- **Tell the user:** "Milestone 4 report is posted on #120 for your review; the Milestone stays open."

**16. "Invoice PDF fix is not right, send it back"**
- **Act on:** "re-read the agreement and tracker and resume only that work through the delivery loop above, arranging the check-in again."
- **Ask the user, one line:** what's wrong with it. The rebuild needs their reason in its brief.
- **NEED:** how a sent-back, already-closed Ticket re-enters. It could be reopening #122 or a new Ticket. Also, the build order only starts entries from the current release issue's Order, and #122 still carries the cut `release-m4-r1` label. That fails the Release start rule "carries no release label". The instructions don't say which release issue it builds under.

**17. New report posted, then "Accepted."**
- I check the new report links the earlier one and names what changed.
- **Act on:** "On the user's own acceptance: start a chore thread to close the Milestone issue."
- **Thread:** cheap (<model>) chore to close #120. I read back that it's closed.
