**Blind run score: Orchard draft (branch)**

1. **Plan Milestone 4: PASS.** The session started a planning thread running `milestone` at premium, which offers the set-aside work first and writes the Milestone issue last. That matches `milestone`'s Planning steps 1–7.
2. **Two feature planning threads: FAIL.** The briefs carry the Milestone number and the planning thread's link, the acceptance-criteria ending and the scope-change report. But the session named the skills as `to-spec`/`to-tickets` and "`to-tickets` for one lone Ticket", with no `grill-with-docs` (or `grilling`) first. `milestone`'s Planning step 3 gives grilling first. The gap: the draft's "Feature planning briefs" list (wayfinder / to-spec+to-tickets / to-tickets) leaves out the grilling step.
3. **Scope change against Excluded: PASS.** The change is reported to the planning thread, which keeps the draft and settles it with the user, as Planning step 3 says.
4. **Planning settles: PASS.** Before any Build thread, the session started a Startup verification thread at regular, briefed with the Harness check, the Loaded skill version check, the row-reuse limit, asking the coordinator for any action only it can take, and posting on #120. That is what `milestone` says for a coordinator that cannot load the skills. The brief also carries the stamp-compare line.
5. **Verdict ready, stamp unchanged then moved: PASS.** Unchanged: delivery starts. Moved (9ab0c3d): the session tells the user once to re-run `setup-project` and goes on unless the user says to wait, as the coverage list gives.
6. **First Release: FAIL.** The start conditions, the brief and "no Build thread while it runs" match `team-lead` step 2. But the session needed `release` to know the Release thread's tier: the draft's table says "the tier `release` names *(see gaps)*" and has no gaps section. The coverage list says the draft carries every thread kind's tier. The gap: an unfilled Release tier, which should come from `model-tiers`' "Use for" column or be named to the user as unfilled. The session's other NEEDs don't fail this scenario:
   - **Release doc path:** the draft names the release doc but doesn't link it; the Release thread knows it.
   - **Where the `start` record goes:** the session's guess (#120, since the thread only plans) is right by `team-lead`.
7. **#125 planned: PASS.** It reads the state fresh, reads the release issue back, confirms the Release thread has ended, and sets slots to the smaller of 2 and the order rule.
8. **Build threads: PASS.**
   - The check-in is arranged before the first Build start, after checking for one already running, hourly, and recorded on #120.
   - #121 gets `implement-spec` and #122 gets `implement`, each at the issue's tier or regular.
   - Starting #122 depends on the order rule.
   - The briefs carry the main-copy line and `team-lead`'s evidence line, and each start gets a `start` record.
9. **Mid-Milestone feature and bug: FAIL.** The bug half passes: a `triage` thread files it, and it joins only if the user plans it as a feature. The feature half: starting a `milestone` (Adding a feature) thread is right, but the session raised a NEED on whether the feature needs its own planning thread. The draft only says "A feature the user plans joins it… to list it, label it and update the Tickets". It leaves out `milestone`'s Adding steps 1–2: plan it with the user first, in its own thread or there, and ask one question when it changes the goal, acceptance or exclusions. That is a gap in a coverage item.
10. **Version request while 2.5.0 is out: PASS.** #121 is told to wait and queued in the order it asked, from the copied CLAUDE.md merge-time step.
11. **#122 merges, #121 asks again: PASS.** First the re-read of open issues no running thread builds that name the changed skill, holding every slot. Then #121 gets main's 2.5.0 raised: minor (2.6.0) for a new or changed skill, patch for a fix, recorded on #121.
12. **Quiet thread: PASS.**
    - At 90 minutes it nudges once and posts `nudge`.
    - Still silent at the next check-in, it stops the thread, reads the stop back, starts a fresh thread from the pushed branch and records "Takes over from …", parking on the listed conditions.
    - The draft also says the thread holds its slot while the Harness reads it as running.
    - The session's NEED about the version number still out to the stalled thread is not answered by any given skill or the CLAUDE.md quote, so it is a skill/fixture gap, not a draft failure.
13. **Blocked cut: PASS.** It tells the user in one line what waits on what, posts `wait`, and starts no Release thread until that changes or the user writes (`team-lead` step 2).
14. **Last Release closed: PASS.** The review gate checks every feature merged or parked (the CSV import included) and starts the last Release's cut first if needed. Then it ends the check-in, reads it back and records it, starts a report thread running `milestone` at regular, and stops.
15. **Report posted: PASS.** It tells the user the report is on #120 and stops for review.
16. **Feature sent back: PASS.** Only #122's work re-enters delivery, the check-in is arranged again, and a new report linking the earlier one follows, as reporting.md's re-entry rule says. The session's NEED (reopen #122 or file a new issue, and whether a new release label or Release thread is needed) is something no given skill says, so it is a skill gap.
17. **"Accepted.": PASS.** A cheap chore thread closes #120 on the user's own word. The check-in was already ended at the gate before the new report.

**Cross-cutting note (not scored as a failure):** the session marked Review level as a NEED in every brief. The draft lists it as a brief field without its source. `team-lead` adds it only when the issue or the user names one, and the project's own level is a fact the case left out. This is a fixture gap, and the draft could carry `team-lead`'s rule.

Overall: FAIL (scenarios 2, 6, 9)
