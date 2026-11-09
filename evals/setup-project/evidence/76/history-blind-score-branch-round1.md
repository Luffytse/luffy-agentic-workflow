**Blind run score: Orchard draft (branch `no-plugin-outside.txt`)**

Overall: FAIL (scenario 2). Sixteen of the 17 scenarios pass. Scenario 2 fails on a gap in the draft: its feature-planning row doesn't say which skill each feature thread runs.

1. **PASS.** The session starts a planning thread with `milestone` on premium and has it offer Milestone 3's set-aside proposals first, as `milestone` Planning step 3 says. Its NEED about where a `start` record goes before any Milestone issue exists is a skill gap: `team-lead`'s audit trail covers delivery only, and no skill records planning threads.
2. **FAIL.** The feature brief line is right: Milestone number, planning-thread link, an issue with acceptance criteria, and scope changes reported to the planning thread. But the session raised a NEED for which skill each thread runs, and guessed. The gap is the draft's row "Feature planning | `wayfinder`, `to-spec`, `to-tickets`". `milestone` step 3 gives `grill-with-docs` (or `grilling`), then `to-spec` and `to-tickets` for a Spec, or one lone Ticket for a small feature. The draft names `wayfinder`, which step 3 doesn't use, leaves out the grilling skill, and doesn't match any skill to a feature kind. Mapping each thread kind to its skill is something the draft must carry. A separate skill gap: no given skill names which skill writes a lone Ticket.
3. **PASS.** The session sends the exclusion change to the planning thread, which keeps the draft. This matches `milestone` step 3.
4. **PASS.** It reads #120 back, then starts a regular verification thread with `milestone`, briefed with the stamp `4f2c9e1` and told to compare it with main's. It starts the probe worker on cheap when asked.
5. **PASS.** With the stamp unchanged, `Verdict: ready` starts delivery. With the stamp moved (9ab0c3d), it tells the user once to re-run `setup-project` and carries on, as the coverage list says.
6. **PASS.** It checks the three Release conditions as `team-lead` gives them and starts a `release` thread briefed with the Milestone issue, the release doc and the last cut. It starts no Build thread while that runs.
7. **PASS.** It reads release issue #125 back and sets slots to the smaller of 2 and the order rule.
8. **PASS.** It arranges and records the check-in before the first Build start, picks `implement-spec` for #121 and `implement` for #122, takes the tier from each issue's Model tier line (regular if none), and puts the evidence line and the main's-copy line in both briefs.
9. **PASS.** The CSV import goes to a `milestone` thread to join the Milestone. The bug goes to a `triage` thread, as the coverage list gives.
10. **PASS.** One version number is out at a time, so #121 is told to wait and queued.
11. **PASS.** It re-reads before any further start, then serves #121 from main's 2.5.0. It frees #122's slot and starts no Release thread, since #121 still carries the open release label.
12. **PASS.** It nudges once and records it. At the next check-in it stops the thread, reads the stop back, and starts a replacement from the pushed branch, with the right park conditions. The silent thread keeps its slot (the draft says so). Its open question about the replacement inheriting #121's issued version is a skill gap: `team-lead` doesn't cover a stall after a version was handed out.
13. **PASS.** It tells the user in one line, posts a `wait` record, and starts no Release thread until something changes or the user writes.
14. **PASS.** It finishes or starts the final cut and waits, stops starting builds, ends the check-in with a read-back and record, and starts the report thread. Its NEED for the release doc doesn't count, because the draft links that doc. Under the Releases rule the Release thread decides cut or plan anyway.
15. **PASS.** It gives the user the link and waits for review.
16. **PASS.** It follows report re-entry: re-read the agreement, resume only that work, arrange the check-in again, and have a new report link the earlier one. Its NEED about how a closed, cut Ticket re-enters delivery (who reopens it, and whether it needs a new release issue or Order entry) is a skill gap: neither `milestone`'s re-entry rule nor `team-lead` says.
17. **PASS.** On the user's own "Accepted." it starts a thread to close #120, as the coverage list gives.

**Fixture or skill gaps (not draft failures):**
- **Review level:** the draft says every brief carries one but gives no value, and the session flagged it. `team-lead` adds a Review level only when the issue or the user names one, so the draft should say that or carry the project's value.
- **Planning-thread `start` record** (scenario 1).
- **Lone-Ticket skill** (scenario 2).
- **Version number held by a replaced thread** (scenario 12).
- **Re-entry of a closed, cut Ticket** (scenario 16).
