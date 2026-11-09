**Blind run: fix.** One validity problem is left.

**Valid: no, in one place.** The section fails a session that needed "a skill or doc it cannot read". The only exemptions are docs the draft names for threads: the index and the tracker doc. The Boundary record is not exempt, but the coordinator itself is pointed to it:
- `team-lead` step 1 arranges the check-in "at the Boundary record's check-in interval (one hour when it names none)".
- `team-lead` says a pull request that crosses a boundary goes to the user, and the Boundary record decides which those are.
- `setup-project`'s coverage list asks for "each delivery step of `team-lead` as it now reads", and nothing in it makes the draft carry the record's values.
- The README itself treats a pointer to the Boundary record as enough: item 15 passes `no-plugin.txt` when it "points to the Boundary record (or gives its values)".

So a passing `no-plugin-outside.txt` draft can copy `team-lead`'s check-in line word for word, and an honest session will then say it needs the Boundary record for the interval. That fails the "Build threads started" scenario, though the draft is exactly what the skill text gives. The failure would come from the blind session having no repo, not from a gap in the draft.

**Exact change.** Replace

> a doc the draft names for threads (the index, the tracker doc) does not count as needed.

with

> a repo doc the draft links (the index, the tracker doc, the Boundary record) does not count as needed; a skill, a skill's own file, or a meaning or step the coverage list says the draft carries does.

The second half keeps the change from loosening items 11 and 12: the merge-time steps and the term meanings must still be in the draft.

**Fails on main for the right reason: yes.** Main's `setup-project` copies `DELIVERY-LOOP.md` and writes no source stamp. Main's session therefore can't tell the user to re-run `setup-project` when the stamp moves, which only the branch's coverage list gives. "At the latest" correctly allows main to fail earlier, for example at the first scenario (planning with set-aside work offered first) or the feature-brief scenarios.

**Needed: yes.** No other case tests whether a coordinator with no skills can act on the assembled draft from start to end. Items 1–16 only score the draft's text.

The rest of the section holds up:
- The exceptions are right. Branch `team-lead` and `milestone` don't give the stamp-moved step, the triage thread for a bug or the closing thread on acceptance; only the coverage list does.
- The version hand-out and re-read scenarios can be scored. `team-lead` step 4 says to take the repo docs' steps "as those docs say", and a passing draft carries them copied in full (item 11).
- No scenario needs `release`, `worker-control` or `snapshot.py`. `team-lead` gives the Release thread's start trigger and brief, and says to read the check-in columns by hand when there is no shell.

Once that phrase is changed, I'd expect the section to read keep.
