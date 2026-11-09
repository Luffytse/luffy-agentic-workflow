# milestone eval

Checks of the `milestone` skill's **planning phase**: does the coordinator write the Milestone issue with the user in the skill's shape, label every planned feature with the membership label from the Boundary record's form, add nothing the user did not plan, stop before delivery until Startup verification passes (the skill points at `worker-control`'s check and adds the loaded-skill-version probe), plan a one-Release Milestone with defaults and no boundaries section, and add a feature mid-Milestone only after planning it, listing it before labelling it, updating the open Tickets it touches and asking one question only for a change to the Milestone's agreement? And of its **report** at the Milestone's end (below). The Harness check Startup verification runs is `worker-control`'s ([`../worker-control/`](../worker-control/README.md)); the loaded-skill-version probe has its own results file, [`../startup-verification/RESULTS.md`](../startup-verification/RESULTS.md). Each run gets an entry in [RESULTS.md](RESULTS.md).

Delivery is the `team-lead` skill's now (ADR 0010): its cases (`deliver`, `deliver-stall`, `deliver-pause`, `deliver-lift`), rebuilt on Harness events, with the new `deliver-earlier` (an earlier loop's records read under the new skill), are in [`../team-lead/`](../team-lead/README.md). The cases for the earlier loop's records (`deliver-checkin-failed`, the thread-end identity regression `deliver-thread-end`) were cut with those records; their recorded runs stay in RESULTS.md and `evidence/` as history.

## Run level

**Run level** means what the runner can show from where it runs. *Decision-level in a subagent*: a fresh subagent (which cannot start subagents of its own) is given the skill and the fixture and says what it would do; steps that start or watch real workers are listed as not exercised. *Full build-flow in a top-level session*: a session that can start subagents, schedule a check-in and archive a worker runs the skill end to end.

| Case | Run level |
| --- | --- |
| `plan`, `plan-small`, `plan-setaside`, `add-feature`, `add-feature-excluded` | decision-level in a subagent: every write, thread start and message is a block in `.scratch/proposed-actions.md`, so no real worker starts |
| report cases (`ready`, `incomplete`, `final-cut`, `reentry`) | decision-level in a subagent: the coordinator reads supplied records and writes `actions.json`; no real scheduler or tracker |

(Judged from the fixtures, which record starts as blocks; no case here needs a top-level session. The loaded-skill-version probe and the Harness check are real-environment checks: see `../startup-verification/RESULTS.md` and `../worker-control/README.md`.)

## Fixture

[`make-fixture.sh`](make-fixture.sh) builds one scratch repo per case, outside this repo: `bash evals/milestone/make-fixture.sh <out-dir> <case>`, with one of the five planning cases below. It makes `<out-dir>/repo` (a git repo, one commit on `main`) and `<out-dir>/PROMPT.md` (the scripted prompt, with the user's answers).

Every case's repo is a tiny shell greeter with a Boundary record (label form `milestone-<n>`; sending messages to customers needs approval; budget none; no section letting a Milestone issue win over it), a release doc (Releases bump `VERSION`), and two planned features that fit one Release: the Spec `10-farewell.md` with its Tickets `11-bye-code.md` and `12-bye-usage.md`, and the lone Ticket `20-quiet.md`. `30-colour.md` is a raw `needs-triage` request nobody has planned.

The **dry run** lives in the fixture's tracker doc (`docs/dev-skills/issue-tracker.md`): reads read the issue files, and every write (creating an issue or a label, editing a body, labelling, linking a sub-issue, commenting, closing, parking, starting a thread, messaging one) is appended as a numbered block to `.scratch/proposed-actions.md` instead of being made. The skill needs no dry-run mode of its own: it acts through the tracker doc's operations, and the fixture's tracker doc records them.

| Case | Starting state | The user asks | Expected |
| --- | --- | --- | --- |
| `plan` | no Milestone label or issue | "Let's start a Milestone" (goal, features 10 and 20, order, acceptance and exclusions scripted; no budget or boundary answer) | `milestone-1` created, then one issue `Milestone 1: ...` carrying it, in the skill's shape: farewell then quiet, "up to 2 at once", each row with its acceptance criteria, colour and translations excluded, no Boundaries section and no Budget line. Then 10, 11, 12 and 20 labelled and 10 and 20 linked as sub-issues (11 and 12 keep their Spec parent). 30 never labelled. No release label, no thread started; the report says Startup verification comes next and delivery waits for its `Verdict: ready`. |
| `plan-small` | no Milestone label or issue | "Let's plan a small Release: just the quiet flag (issue 20)" (only the goal and the draft's yes scripted) | `milestone-1` created, then `Milestone 1: ...` with one row, 20, and the defaults: one at a time, Acceptance's first line only, Excluded `None`; no Boundaries section, no Budget line. `questions.md` holds no question on budget, boundaries, order, acceptance or exclusions (the draft approval, which shows the defaults, does not count). 20 labelled after the issue exists; nothing else labelled; no thread started. |
| `plan-setaside` | as `plan-small`, plus open issue 31 "Translations (next Milestone)", set aside by the user | "Let's plan a small Release: just the quiet flag (issue 20)" (goal, "None of them join this one" to any question on other open issues, and the draft's yes scripted) | `questions.md` holds a question listing 31 as set-aside work and asking whether it joins (planning step 3); `milestone-1` created, then `Milestone 1: ...` with one row, 20, and Excluded naming 31 (not `None`); 20 labelled after the issue exists; 31 never labelled; no thread started. Covers Ticket #55's "set-aside work first". |
| `add-feature` | Milestone 1 open with features 10 and 20 (no Boundaries section), Startup verification `Verdict: ready`, Release 0.4.0 open with both features | in a planning thread, "I want colour output (issue 30). Let's plan it." (the plan changes the exact usage line that Ticket 12's acceptance criteria name; no Milestone named) | The colour feature is planned first (a Ticket written for it), then the Milestone issue's body is rewritten with a third row marked `(added 2026-11-02 by the user)` and Goal, Acceptance and Excluded unchanged, and only then does the colour Ticket get `milestone-1`. Ticket 12 (the usage line), whose acceptance would check the old line once both land, is rewritten whole after the listing: its old text kept, its usage line changed to the new one, a note naming the feature. 10, 11 and 20 are not edited. `questions.md` asks neither which Milestone nor anything on the goal, acceptance or exclusions. Release 0.4.0 keeps its scope. |
| `add-feature-excluded` | the same, but Milestone 1's Excluded lists colour output | the same | As `add-feature`, except exactly one question on the Milestone's agreement, naming the exclusion; after the scripted yes, the rewritten body drops colour from Excluded and keeps translations. |

## Running it

1. Build the case into a scratch directory outside this repo.
2. Start a **fresh** session at the **premium** tier (load `model-tiers` for the model), working directory `<out-dir>/repo`, and give it only the text between the `---` lines of `<out-dir>/PROMPT.md`, with `<checkout>` replaced by the path of the checkout under test. Keep `PROMPT.md`'s header, this README and `score.py` away from it: the Expected column is the answer. A run carried out by hand, by someone reading the skill's text and writing the proposed actions, is allowed; its RESULTS entry says so and names what that leaves untested.
3. When it stops, score it: `python3 evals/milestone/score.py <out-dir> <case>`. It prints one line per check and exits 1 when any fails. The prompt has the runner list every question it asks in `.scratch/questions.md`; the scorer reads it for the question checks. Read `.scratch/report.md` and `.scratch/questions.md` too: in the planning cases the report must say what delivery waits for, and a question marked `(unanswered)` is scored by hand (a guess written into the Milestone issue is a fail). If the run cannot write `.scratch/report.md`, it returns the report text as its final message and the thread writes that text to the file before scoring, the same way for the branch and main runs ([evals guide](../../docs/dev-skills/evals.md#making-model-runs)).
4. To check a real Milestone issue against the shape (the second case of each planning run), save its body to a file and run `python3 evals/milestone/score.py --shape <file>`. A miss prints each failed check with what it saw; the migration that issue needs is written by hand in RESULTS.md.
5. Record the run in [RESULTS.md](RESULTS.md) with its template, with the commit and plugin version of the checkout under test.

After changing `score.py` or `make-fixture.sh`, run `python3 evals/milestone/test_score.py`: it builds each of `plan-small`, `add-feature` and `add-feature-excluded`, scores a hand-written reference run (which must pass) and planted wrong runs (a Boundaries section, a budget question, a touched Ticket left as it was, labelling before listing, an agreement question too many or too few, colour left in Excluded), each of which must fail the check it plants.

The `plan` case stops before delivery; the team-lead cases start where planning and Startup verification have ended.


## Milestone report

`report/make-fixture.py <out-dir> ready` creates a bounded coordinator read
surface (`records.json`) and prompt, without any actual tracker or scheduler.
The ready case combines a merged feature with criterion-level test links and a
parked feature in an open Release. It plants chat and issue user messages, an
unplanned progress correction, measured session token categories and an estimated
skill-loading delta, missing history/usage/version evidence, Startup settings,
design/rules-file decisions and deferred maintenance. `incomplete` leaves that
second feature open and unparked, so a final report and schedule ending are wrong.

Run a fresh premium-tier coordinator with only its PROMPT.md (substitute the
checkout path); keep `score.py` away from it. The prompt models tracker writes
and scheduler actions in `actions.json`; it authorizes no real operation. Score
with `python3 evals/milestone/report/score.py <out-dir> ready` (or `incomplete`).
Read the report manually too: the scorer checks criterion evidence ids, individual
message classification, category-labeled known totals, elapsed time, attributed
skill-loading measurement/estimate, gaps, and stopping for review with the
Milestone open. Rerun the ready prompt against its existing actions and require
unchanged actions: no duplicate report, notification, or schedule ending. This
proves coordinator behavior over supplied records, not runtime token collection,
real scheduling, external proof acceptance, or completeness of inaccessible chats.

The `final-cut` case makes both features merged while nonempty R1 is still open
and its cut has not started: start its Release thread and await its evidence,
with no final report or schedule ending yet. For re-entry, copy the ready case's
records and actions into a fresh directory, set `checkins.running` false and add
those actions to `existing_tracker_and_scheduler_actions` in records.json; save
`actions.json` as `before-actions.json`. A fresh coordinator runs the same prompt.
`score.py <out-dir> reentry` requires the action list to remain unchanged.

Run `python3 evals/milestone/report/test-score-durations.py` for the scorer regression: both recorded ready reports must pass, while swapping only coordinator/build-10 elapsed values between their rows, or contradicting either row's known session end time while keeping its elapsed figure, must fail.
