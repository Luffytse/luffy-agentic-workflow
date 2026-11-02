# Results

One entry per run of the `milestone` skill's dry run (the planning cases and the `deliver` case), newest first ([README](README.md) says how to build, run and score it). Record the commit and the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`; an entry written inside an open pull request names the commit and version it ran on as its base. Each planning run also applies the shape to one real Milestone issue (`score.py --shape`) and names the migration it needs, if any; each `deliver` run also applies the loop, read-only, to one real Milestone and names the thread it would start next and the next Release it would plan.

## Template

```
### <date>, commit <sha>, dev-skills <version>: <case>

Driven by: <a fresh session at the premium tier | by hand, reading the skill's text>; skill text from <path, branch>
Proposed actions: <the numbered blocks, in short; the Milestone issue body when one was written>
Score: <n>/<m> (`score.py <out-dir> <case>`); questions not covered by the script: <none | list>
Report: <what it said comes next and what delivery waits for>
Before: <the same case run on the skill text before the change, and its score>
Real Milestone issue: <issue>, `score.py --shape`: <result; the migration it needs, or "matches"> (deliver: the loop applied to it, read-only)
Not exercised: <what this run did not reach>
Pass: yes | no. Lessons: <what to change in the skill, if anything>
```

## Runs

### 2026-11-02, commit d85f265 (base), dev-skills 0.37.0 (base): `deliver`, with Milestone 1 as the second case

Driven by: by hand, by the Implementer of the delivery-loop Ticket, reading this branch's `plugins/dev-skills/skills/milestone/SKILL.md` ("Delivery") step by step against a fresh fixture built with `make-fixture.sh <out-dir> deliver`, running `.scratch/world.sh <k>` before each event from event 2 on (the fixture is built in event 1's state) and reading the state from the fixture's tracker each time. No fresh session ran it (the Implementer was not allowed to start further agents), and the person driving the run also wrote the skill text: that is this entry's main limit.

Proposed actions, by event (re-run after Ticket checks 1 and 2, on the twelve-event fixture, and after Round 2 of the pull request review, on the fourteen-event fixture):

1. Read: no release issue names the Milestone and no Release thread record, so step 1. Grouping: 10 (with 11 and 12), then 20, both open, unlabelled for a Release, with no open blocker; 25 is left out, blocked by the open `35-readme-tool.md`; 2 of the cap of 5. (1) Start a thread, `release`, briefed with the Milestone issue, the release doc, Milestone 1 · Release 1 (`release-m1-r1`), the grouping in order, and "no Release of this Milestone has been cut yet, so the plan is the feature scope only"; (2) its delivery-thread record on the Milestone issue. No build thread.
2. Read: `40-release-m1-r1.md` names the Milestone and its label is on 10, 11, 12 and 20, as grouped. Slots: the smaller of the project's 3 and the Milestone's "One at a time", so 1, none taken. Next in build order: 10, a Spec with its Tickets filed. (3) Start a thread, `implement-spec`, for 10, with the Milestone issue, model tier regular and Review depth Deep (10's own lines), and the repo; (4) its record on 10. 20 waits for 10 to close.
3. Read: #7 changes `skills/greeting/SKILL.md`, which the release doc says bumps (a changed skill rule: minor); main's `VERSION` reads 0.3.0 and no hand-out record is out. (5) Comment on 10: `<!-- milestone version hand-out -->`, `Version 0.4.0 for #7: merge it next, ...`; (6) message the Spec thread its number. No start: 10 still holds the one slot.
4. Read: #10 builds no issue and changes `skills/greeting/SKILL.md`, so it bumps; 0.4.0 is out for #7 (main has not reached it, #7 is open, 10's thread runs). (7) Comment on #10 itself: `Waiting: #10 asked while 0.4.0 was out.`; (8) tell the thread to hold #10.
5. Read: #7 closed unmerged, so its record is void and nothing is out; main still reads 0.3.0. #10's waiting request has no number after it and asked first. (9) Comment on #10: `Version 0.4.0 for #10 ...`, saying #7's record is void; (10) comment on 10: `Waiting: #9 asked while 0.4.0 was out.`; (11) message the thread both.
6. Read: main's `VERSION` reads 0.4.0, the number #10 got, so nothing is out; #10 changed the `greeting` skill (a wording rule), so a re-read is due. (12) Comment on 20: re-read after #10, still fits. #9's waiting request has no number after it: (13) comment on 10, `Version 0.5.0 for #9 ...`; (14) message the thread its number. No start: 10 holds the slot.
7. Read: main's `VERSION` reads 0.5.0, the number handed out; #9 changed the `greeting` skill, so a re-read is due before any start. 20 is the one open Milestone issue no running thread builds whose body names the skill; against main's new skill text (every message goes through one `say` function, farewells included) its criteria miss the farewell. (15) Edit 20's body, whole, adding `greet.sh --quiet bye Ada` prints nothing and exits 0 and a re-read note (inside the agreement: the Milestone's own acceptance already runs `greet.sh --quiet bye Ada`). 20 has no open blocker; 10 is closed, so the slot is free. (16) Start a thread, `implement`, for 20, tier regular, with no Review depth (20 names none, so `agentic-review` chooses); (17) its record on 20.
8. Read: #8 changes only `src/greet.sh` and `test.sh`, nothing the release doc says bumps. (18) Message the Ticket thread: no number, merge with no bump.
9. Read: #8 changed no skill, so no re-read; every issue labelled `release-m1-r1` is closed, and no Release thread is running. (19) Start a thread, `release`, for `40-release-m1-r1.md` and the Milestone issue (Triage batch, Release-end Retro planning, the cut, the next planning); (20) its record on the release issue. 25 is in no Release, so no build thread.
10. Read: the Release thread's record on 40 has no ended record after it and no newer release issue exists, so it is running: step 5 starts none, step 1 does not apply (40 is still open). No action.
11. Read: 40 is closed with its notes; the thread reports it planned nothing. (21) The ended record on 40. Step 1: no open release issue, no Release thread running, but the grouping is empty (25 still blocked), so nothing starts; the user would hear that 25 waits on 35.
12. Read: 35 is closed, so 25 is unblocked and the grouping holds it. (22) Start a thread, `release`, to plan Milestone 1 · Release 2 with 25, briefed with the last release issue cut (40) for its Triage batch and Release-end Retro planning, and, like the briefs of events 1 and 9, with "if no planned feature qualifies and no maintenance fix joins, open no release issue, label nothing, and report that it planned no Release"; (23) its record on the Milestone issue.
13. Read: `41-release-m1-r2.md` names the Milestone but no issue carries `release-m1-r2`, so it is empty: no current Release, and never done or cut; 25 is blocked again by the open `36-readme-style.md`, so the grouping is empty. (24) The ended record on the Milestone issue. Step 5 starts no Release thread for 41; step 1 has nothing to plan; the user would hear in one line that 41 holds no issue and that 25 waits on 36.
14. Read: the same state. No action: 41 is still empty, so no second Release thread starts.

Score: 42/42 (`score.py <out-dir> deliver`; an empty `proposed-actions.md` scores 16/42). Questions: none. Report: none written (the case has no user turn); the user hears only the Release planning differing from the grouping, a re-read that would change the agreement, a feature left blocked or parked, or delivery ending.

Before: the same case run by hand on the base's skill text, whose Delivery section said its steps were "not part of this skill yet" and to deliver "as the project's own instructions say". The fixture's project instructions hold only a thread limit (3), the tier map and "no `triage`", so the run started 10's and 20's build threads at event 1 (within the limit of 3, with no Review depth in their briefs; 25 is blocked) and, for events 2 to 14, wrote no action (no rule names the Release thread, the hand-out, the re-read or the Release boundary): 16/42. The 16 are the checks a run that does nothing passes (no extra thread, no number, no label). Scorer guards, on copies of the passing run: starting 20 in event 2 as well fails 2 checks; handing #8 the number 0.6.0 fails "no version handed out for a pull request that changes no skill"; starting 20's thread before its re-read fails "20-quiet re-read against the changed skill before its thread starts", and so does a copy whose only comment on 20 before its start is the delivery-thread record; a brief for 20 carrying `Review depth: Standard` fails "its brief carries no Review depth"; leaving #10 waiting at event 5 because main never read the void 0.4.0 fails "#7's number is void, so the waiting #10 gets 0.4.0", and so does keeping #7's number out; a second Release thread at event 10 fails "no thread started while the Release thread is running"; no Release thread at event 12 fails "a Release thread started to plan the next Release with 25-hello-doc"; a Release thread started at event 13 or at event 14 to cut the empty `41-release-m1-r2.md` fails that event's "no thread started" check; Release thread briefs without the open-no-release-issue line fail "each Release thread's brief says to open no release issue when nothing qualifies".

Real Milestone issue: Milestone 1 (#396), its open Release 3 (#459, `release-m1-r3`) and the release doc `docs/agents/release.md` (pull requests bump; a pull request changing `plugins/dev-skills/skills/` bumps), read on 2026-11-02 with main at 0.37.0; the loop applied read-only, nothing written:

- **Delivery gate.** The latest Startup verification result on #396 (2026-11-02T06:39:07Z) reads `not ready` (Scheduled check-in, Confirmed stop, and in its planted run Real worker state), and no go-on from the user is recorded on #396. Under the skill, delivery for Milestone 1 waits on the user's rerun or go-on, so everything below is what the loop would do once one is recorded, not what it would do now.

- **State.** Order rule "one at a time, in this order". Release 3's maintenance fixes #458, #448 and #447 are closed, and so is #405. Open: #406 (this Spec; its thread is running), then #473, #407 and #408, each blocked by the one before it (#473 by #406, #407 by #406 and #473, #408 by #407). Release 3's real build order matches the loop's: its release issue puts #458 first, then #405, #406, #473, #407, #408, so #473 and #407 come after #406, as the row 10a note on #396 says.
- **Next thread.** None now: #406 holds the one slot. Once #406 closes, #473 (a Spec with its Tickets #474 and #475 filed) gets a Spec thread with `implement-spec`, with no Review depth in its brief unless #473 or the user names one; after it, #407 first gets a `to-tickets` planning thread (its Tickets are not filed), then its Spec thread; then #408, a lone Ticket, with `implement`.
- **Version hand-out.** When #406's Spec pull request asks just before its merge, it changes the `milestone` skill, a changed skill: minor, so 0.38.0 if main still reads 0.37.0 and no other number is out, recorded on #406.
- **Re-read after that merge.** The open Milestone 1 issues no running thread builds that name the `milestone` skill or its files: #473, #474, #475, #407, #408 and #409. This repo runs `triage`, so a `triage` thread does the re-read, before #473's thread starts.
- **Release boundary and the next Release.** When every `release-m1-r3` issue is closed (#406, #483, #484, #473, #474, #475, #407, #408), a Release thread with `release` cuts Milestone 1 · Release 3. Its planning, by the rule step 1 groups with, takes **Milestone 1 · Release 4** (`release-m1-r4`): #409 (piece C5, the one planned feature left; its blocker #408 is closed by then), 1 of the cap of 5, plus the maintenance fixes the Release 3 Triage batch and Release-end Retro planning mark `joins the next Release` (not known yet). Once Release 4 is cut, no planned feature is left open, so delivery is done and the Milestone review follows.
- **Migration it needs.** Delivery-thread and version hand-out records start with this skill: the running #406 thread, and the threads before it, have none, so the first wake under the new text adds a delivery-thread record to #406, as the skill says for a feature already being built, before counting slots; without it the slot would read as free and #473 would start early. The feature table's columns still need the planning entry's migration (`Piece` to `Feature`, an `Accepted when` column); the loop reads only the order and the issues from it, so it runs either way.

Not exercised: a fresh session following the skill (the run was by hand, by its author); a real tracker and real threads (events were scripted and the threads' work was played by `world.sh`); the delivery gate (a `not ready` verdict, the user's rerun, and a go-on recorded on the Milestone issue): the fixture starts at `Verdict: ready`, and live #396 reads `not ready` now with no go-on recorded; a Spec with no Tickets yet (the `to-tickets` thread), maintenance fixes in a Release, a parked feature, the `triage` path of the re-read, and Releases bump; and these delivery branches: a repeat request after main's version moved (step 3.4), the post-merge version check finding main wrong (step 3.5), the patch bump branch (every hand-out here is minor), the step 4 question to the user over a change to the agreement and its close-as-obsolete outcome, related issues treated as one feature, the cap of 5 (no grouping here reaches it), and the Milestone done ending (no features left open).
Pass: yes, as a by-hand run. Lessons: Ticket check 1 found that a default Review depth of Standard kept Deep from ever reaching `agentic-review`, that a closed or parked pull request kept its number out for good, that step 5 lacked step 1's guard against a second Release thread, and that nothing re-planned features left blocked after the last Release; the skill now carries a depth only when one is named, voids such numbers, guards step 5 and runs step 1 again once a left-out feature is free, and the fixture's events 4, 5 and 10 to 12 check each. Ticket check 2 found that a waiting request was served only once main read the number ahead of it, which never happens when that number goes void; the skill now serves waiters at any wake with no number out, and events 4 to 6 check it. The first draft also started threads in "the Milestone issue's order", which leaves a Release's maintenance fixes unplaced; the skill now builds them first, in the release issue's order, as Release 3 did with #458. The missing records for threads started before this skill are the migration above. Round 2 of the pull request review found that a Release planning with nothing to plan still opened a release issue, which step 5 then read as a done Release, cutting empty Releases again and again; every Release thread's brief now says to open no release issue when nothing qualifies, an empty release issue is never done or cut, and events 12 to 14 check both. A rerun by a fresh premium-tier session is the next evidence to get.

### 2026-11-02, commit b14efe5 (base), dev-skills 0.37.0 (base): `plan` and `add-feature`, with Milestone 1 as the second case

Driven by: by hand, by the Implementer of the planning-phase Ticket, reading this branch's `plugins/dev-skills/skills/milestone/SKILL.md` step by step against fresh fixtures built with `make-fixture.sh`, taking each answer from the fixture's scripted user. The Implementer was not allowed to start further agents, so no fresh session ran it; the person driving the run also wrote the skill text, which is the main limit of this entry.

**`plan`.** Step 1 read the Boundary record (label form `milestone-<n>`), the tracker doc and `.scratch/labels.md`: no label in the form and no Milestone issue, so planning starts from the goal. Steps 2 to 6 took the scripted goal, features (10 and 20, both already planned), order ("two at once"), acceptance, exclusions, budget and extra boundary; `30-colour.md` was not proposed, as it does not serve the goal, and the user's answer to any proposal was "no" anyway. Step 7 took Milestone number 1 (no label in the form yet). Proposed actions, in order:

1. Create a label `milestone-1`.
2. Create an issue `Milestone 1: goodbye and quiet`, labelled `milestone-1`, with this body:

   ```
   ## Goal

   By the end, the greeter can say goodbye and can run silently in scripts, so it can ship as 1.0.

   ## Features, in build order

   In this order, up to 2 at once. Each feature is its own issue carrying `milestone-1`.

   | # | Feature | Kind | Accepted when |
   | --- | --- | --- | --- |
   | 1 | `10-farewell.md` Add a farewell command | Spec | `greet.sh bye Ada` prints `Goodbye, Ada!` and exits 0; no name greets the world; `bash test.sh` covers both |
   | 2 | `20-quiet.md` Add a --quiet flag | lone Ticket | `--quiet` prints nothing and keeps the exit code (0 for `hello`, 2 for an unknown command) |

   ## Acceptance

   - Every feature above is merged and its issue closed.
   - At the Milestone review the user runs `greet.sh --quiet bye Ada` and sees nothing.

   ## Excluded

   - Colour output (`30-colour.md`).
   - Translations.

   ## Boundaries

   - **Budget:** none.
   - Also needs the user's approval: publishing a release to the package registry.
   ```

3. to 8. Label `10-farewell.md`, then link it as a sub-issue of the Milestone issue; label `11-bye-code.md` and `12-bye-usage.md` (they keep their Spec parent); label `20-quiet.md`, then link it as a sub-issue.

Score: 24/24. Questions not covered by the script: none. Report: "Next is Startup verification, which has not run here yet; delivery starts only once its result on the Milestone issue reads Verdict: ready." No Release label and no thread were proposed.

**`add-feature`.** Step 1 found Milestone 1 open, so the run went to "Adding a feature mid-Milestone". Proposed actions, in order: (1) create the Ticket `50-colour-terminal.md` from the user's scripted plan (green only on a terminal, `--no-color`, a test for both), absorbing `30-colour.md`, labelled `enhancement` only; (2) a comment on `30-colour.md` pointing to it; (3) rewrite the Milestone issue body with a third row, `` `50-colour-terminal.md` Colour the name on a terminal (added 2026-11-02 by the user) | lone Ticket | the name is green only when standard output is a terminal; `--no-color` turns it off; a test covers both ``, every other line unchanged; (4, 5) label `50-colour-terminal.md` and `30-colour.md` with `milestone-1`; (6) link the Ticket as a sub-issue. No `release-0.4.0` label. Score: 17/17. Report: Release 0.4.0 keeps its scope; colour waits for the next Release planning.

Before: the same two cases run on the base's skill text (it said it held only Startup verification and to "go no further"), which writes no Milestone issue and edits none: an empty `proposed-actions.md`, scoring 0/2 on `plan` and 0/2 on `add-feature`. Scorer guards: a copy of the `add-feature` run with `30-colour.md` labelled before the row was in fails 2 checks ("labelled after the Milestone issue lists it", "nothing carries the Milestone label before it is listed"); a copy of the `plan` run that labels `30-colour.md` fails "30-colour never labelled"; a copy of the `add-feature` run whose rewritten body drops the second line of Acceptance fails only "goal, acceptance, exclusions and boundaries unchanged" (the scorer compares each of those sections whole).

Real Milestone issue: Milestone 1 (#396, body as of 2026-11-02T07:46:11Z, label `milestone-1`), `score.py --shape`: 6 of 7 checks pass. Its headings (Goal; Features, in build order; Acceptance; Excluded; Boundaries) are the shape's, in order; the order rule ("one at a time, in this order") comes before the table; Boundaries holds the Budget line and lines beyond it; its mid-Milestone row 10a is marked with its date and who added it, as the shape's added rows are. Migration it needs: its feature table's columns are `# | Piece | Kind | What it changes | Who merges`. Rename `Piece` to `Feature` and add an `Accepted when` column after `Kind`, holding each piece's acceptance criteria in short, from its own issue. `What it changes` and `Who merges` can stay as extra columns. The issue was not edited: this run only names the migration.

Not exercised: a fresh session following the skill (the run was by hand, by the skill's author); the user planning a feature inside the run with `grill-with-docs`, `to-spec` or `to-tickets` (the `plan` features were planned beforehand, and the `add-feature` plan was scripted in one answer); a real tracker; Startup verification and delivery, which follow planning, including the delivery gate (a `not ready` verdict, a rerun, a go-on recorded on the Milestone issue: live #396 reads `not ready` now with no go-on recorded) and the delivery branches the `deliver` entry above lists as not exercised.
Pass: yes for both cases, as a by-hand run. Lessons: labelling the issues a feature absorbs was unclear in the first draft ("its Tickets or related issues"); the skill now says every open issue the feature holds, its own, its Tickets, the issues it absorbs or its related issues. A rerun by a fresh premium-tier session is the next evidence to get.
