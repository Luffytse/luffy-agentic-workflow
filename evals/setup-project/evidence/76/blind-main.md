Walk-through as the Orchard coordinator, using only the draft instructions.

**Gaps that affect every brief:**
- **NEED: the tier-to-model mapping.** The draft says "Start each thread on the model mapped to its brief's Model tier" but gives no mapping. I fall back on "the worker tool's default model when they give none."
- **NEED: what the Review level values are and how to choose one.** "Every brief carries … the Review level", but nothing defines it.
- **What I record:** the draft says the instructions "hold no state of the work: look that up on the tracker." So I record nothing myself. State lives in what threads write on GitHub.

---

**1. "Let's plan Milestone 4…"**
- **NEED: which skill plans a Milestone.** "Planning threads run `wayfinder`, `to-spec` or `to-tickets`" doesn't say which one, and Loop step 1 starts *after* "Milestone planning has settled." My guess is `wayfinder` or `milestone`, marked as a guess.
- **NEED: what to do with Milestone 3's two proposed follow-ups.** No line covers them. I'd tell the user they exist and ask whether they belong in Milestone 4.
- **Brief (if I start the thread):** skill (NEED), tier regular ("regular when the issue names none"), repo `orchard-team/orchard`, Review level (NEED), no issue link yet.
- **To the user:** "Starting Milestone 4 planning. Milestone 3 proposed two follow-ups: include them?"

**2. Two features in parallel**
- **"usage export":** a thread running `to-spec`, tier regular, repo, Review level (NEED), Milestone issue link.
- **"invoice PDF fix":** **NEED: which skill plans a lone Ticket.** It's probably `to-tickets`, but that's a guess.
- The draft sets no limit on planning threads ("At most two Build threads" covers Build only), so both can run at once.

**3. Export should include last year's data, which the draft lists as Excluded**
- No line covers a scope conflict. "What is the user's to approve are in the Boundary record" → **NEED: boundaries.md.**
- I don't decide it. I relay it to the user verbatim: "The usage export thread says you want last year's data included, but the Milestone draft lists it under Excluded. Move it in?"
- Then I pass the answer back to the thread.

**4. #120 written, features labelled**
- I take this as "planning has settled," but the draft doesn't define "settled". I also check the tracker that no planning thread is still running.
- **Loop step 1:** start a thread running `milestone`'s Startup verification.
  - Brief: skill `milestone` (Startup verification), issue link #120, Milestone issue link #120, tier regular, repo, Review level (NEED).
- **NEED: "`worker-control`'s check run by the agent the skill names".** I can't read `milestone` to know which agent, so I can only pass the line on verbatim in the brief.

**5. Verdict ready, commit 4f2c9e1 (or 9ab0c3d)**
- I check that `Verdict: ready` is actually *on the Milestone issue*, per "Start no Build thread until the result on the Milestone issue reads `Verdict: ready`". The thread's report alone isn't enough.
- **NEED: what the commit hash is for.** It looks like a reuse or staleness check, but no line says what to compare it against. So I can't say whether 4f2c9e1 and 9ab0c3d lead to different actions. Without a rule, both cases are treated the same: ready.

**6. No release issue, two eligible features, nothing running**
- **Loop step 2:** "With no current Release … start a Release thread that runs `release` to plan one."
- Brief: skill `release`, Milestone issue link #120, tier regular, repo, Review level (NEED).

**7. #125 planned, Order #121, #122**
- I re-read the tracker and confirm both issues carry `release-m4-r1` and no Release thread is still running.
- **NEED: "the Milestone's order rule".** The draft doesn't say where it lives. My guess is the Milestone issue #120, which I'd read.

**8. Start Build threads (Loop step 3; limit "At most two Build threads")**
- **#121:** "A Spec with Tickets runs `implement-spec`." Brief: `implement-spec`, #121 link, #120 link, tier as #121 names or regular, repo, Review level (NEED).
- **#122:** "a lone Ticket runs `implement`." Same brief lines with #122.
- Two threads: at the limit.

**9. Mid-Milestone requests (CSV import; crash on empty date range)**
- **NEED: how to add a feature or bug mid-Milestone.** The loop's only planning point is before step 1, and `triage` runs only at a Release cut (step 4).
- To the user: "CSV import is new scope and the empty-range crash is a bug. My instructions have no step for adding either mid-Milestone. Should I start a planning thread now, or hold them for triage at the next cut?"
- I don't start threads on a guess.

**10. #121 asks for a version; #122 holds 2.4.0 → 2.5.0, still open**
- I act on "take the coordinator's steps in CLAUDE.md (the version hand-out …) exactly as it says" and "While a request is still waiting, keep taking them."
- **NEED: CLAUDE.md's hand-out steps.** I can't tell whether #121 waits, gets 2.6.0, or something else.
- To #121: "Request noted; I'll answer once I can apply the hand-out rule." I keep the request open.

**11. #122 merged (main 2.5.0); #121 asks again**
- **NEED: CLAUDE.md.** It holds the hand-out and "the re-read after a skill merge". I can't tell whether #122's merge counts as a skill merge that triggers a re-read, or what #121 gets (2.6.0 would be a guess).
- Also, #121 changes `agent-skills/billing/`, so a re-read may apply once it merges. Same NEED.
- Since the step is still waiting, I keep re-checking it at every wake.

**12. #121 silent for 90 minutes, then still silent**
- No line covers stalled threads. I can only read its state from the worker tool. "Start none whose thread is already running" forbids a replacement while it runs.
- I message the thread asking for status. At the second silent check-in, I tell the user. I don't stop or restart it without a rule.

**13. "The cut is blocked: #130 is open."**
- I re-read the tracker. If #130 carries `release-m4-r1`, step 4's condition ("every issue carrying the current Release's label is closed") was never met. Step 3 then applies: build #130 within the limit, with its skill by type.
- If #130 doesn't carry the label, **NEED: the `release` skill's blocked-cut handling.** I'd tell the user.

**14. All labelled issues closed, every feature merged**
- **Step 4:** a Release thread running `release` to cut #125.
- **Step 5:** a report thread running `milestone`. "Take every step that applies, in order" means I start both.
- **Two ambiguities:**
  - Does "run `triage` and `retro-planning`" mean the Release thread runs them, or I start separate threads ("Start a thread for each step … that names a skill")? I'd start separate threads, marked as a guess.
  - Should the report wait for the cut? The draft doesn't say. Also, "plan the next Release" has nothing to plan.

**15. Report posted**
- Step 5: "then stop for the user's Milestone review."
- To the user: "Milestone 4 report is posted on #120 (link). Please review." I start nothing.

**16. "invoice PDF fix is not right, send it back."**
- **NEED: what a rejected review does.** Options include reopening #122, a new Ticket, or a new Release. And "report written" now blocks step 5 from re-running.
- I confirm with the user what "not right" means and ask how they want it sent back, rather than guessing.

**17. New report posted; user: "Accepted."**
- **NEED: the post-acceptance steps.** Who closes #120, and what's next (Milestone 5 planning)? No line covers them.
- To the user: "Noted, Milestone 4 accepted. Should I close #120?"

---

**Top fixes for the draft:**
- the Milestone-planning skill and how Spec vs lone Ticket planning is chosen;
- the tier-to-model map and Review levels;
- inline the CLAUDE.md coordinator steps, since the coordinator can't read CLAUDE.md;
- the Startup verification commit rule and the agent `worker-control` uses;
- mid-Milestone additions, stalled threads and blocked cuts;
- review rejection and acceptance;
- whether triage and retro run in their own threads.
