# milestone eval

Checks of the `milestone` skill's **planning phase**: does the coordinator write the Milestone issue with the user in the skill's shape, label every planned feature with the membership label from the Boundary record's form, add nothing the user did not plan, stop before delivery until Startup verification passes (the skill points at `worker-control`'s check and adds the loaded-skill-version probe), and add a feature mid-Milestone only after planning it, listing it before labelling it? And of its **report** at the Milestone's end (below). The Harness check Startup verification runs is `worker-control`'s ([`../worker-control/`](../worker-control/README.md)); the loaded-skill-version probe has its own results file, [`../startup-verification/RESULTS.md`](../startup-verification/RESULTS.md). Each run gets an entry in [RESULTS.md](RESULTS.md).

Delivery is the `team-lead` skill's now (ADR 0010): its cases (`deliver`, `deliver-stall`, `deliver-pause`, `deliver-lift`), rebuilt on Harness events, with the new `deliver-earlier` (an earlier loop's records read under the new skill), are in [`../team-lead/`](../team-lead/README.md). The cases for the earlier loop's records (`deliver-checkin-failed`, the thread-end identity regression `deliver-thread-end`) were cut with those records; their recorded runs stay in RESULTS.md and `evidence/` as history.

## Run level

**Run level** means what the runner can show from where it runs. *Decision-level in a subagent*: a fresh subagent (which cannot start subagents of its own) is given the skill and the fixture and says what it would do; steps that start or watch real workers are listed as not exercised. *Full build-flow in a top-level session*: a session that can start subagents, schedule a check-in and archive a worker runs the skill end to end.

| Case | Run level |
| --- | --- |
| `plan`, `add-feature` | decision-level in a subagent: every write, thread start and message is a block in `.scratch/proposed-actions.md`, so no real worker starts |
| report cases (`ready`, `incomplete`, `final-cut`, `reentry`) | decision-level in a subagent: the coordinator reads supplied records and writes `actions.json`; no real scheduler or tracker |

(Judged from the fixtures, which record starts as blocks; no case here needs a top-level session. The loaded-skill-version probe and the Harness check are real-environment checks: see `../startup-verification/RESULTS.md` and `../worker-control/README.md`.)

## Fixture

[`make-fixture.sh`](make-fixture.sh) builds one scratch repo per case, outside this repo: `bash evals/milestone/make-fixture.sh <out-dir> <plan|add-feature>`. It makes `<out-dir>/repo` (a git repo, one commit on `main`) and `<out-dir>/PROMPT.md` (the scripted prompt, with the user's answers).

Every case's repo is a tiny shell greeter with a Boundary record (label form `milestone-<n>`; sending messages to customers needs approval; budget none), a release doc (Releases bump `VERSION`), and two planned features that fit one Release: the Spec `10-farewell.md` with its Tickets `11-bye-code.md` and `12-bye-usage.md`, and the lone Ticket `20-quiet.md`. `30-colour.md` is a raw `needs-triage` request nobody has planned.

The **dry run** lives in the fixture's tracker doc (`docs/dev-skills/issue-tracker.md`): reads read the issue files, and every write (creating an issue or a label, editing a body, labelling, linking a sub-issue, commenting, closing, parking, starting a thread, messaging one) is appended as a numbered block to `.scratch/proposed-actions.md` instead of being made. The skill needs no dry-run mode of its own: it acts through the tracker doc's operations, and the fixture's tracker doc records them.

| Case | Starting state | The user asks | Expected |
| --- | --- | --- | --- |
| `plan` | no Milestone label or issue | "Let's start a Milestone" (goal, features 10 and 20, order, acceptance, exclusions, budget and one extra boundary scripted) | `milestone-1` created, then one issue `Milestone 1: ...` carrying it, in the skill's shape: farewell then quiet, "up to 2 at once", each row with its acceptance criteria, colour and translations excluded, the registry approval under Boundaries. Then 10, 11, 12 and 20 labelled and 10 and 20 linked as sub-issues (11 and 12 keep their Spec parent). 30 never labelled. No release label, no thread started; the report says Startup verification comes next and delivery waits for its `Verdict: ready`. |
| `add-feature` | Milestone 1 open with features 10 and 20, Startup verification `Verdict: ready`, Release 0.4.0 open with both features | "Add colour output (issue 30) after the quiet flag" | The colour feature is planned first (a Ticket written for it), then the Milestone issue's body is rewritten with a third row marked `(added 2026-11-02 by the user)` and the rest unchanged, and only then does the colour Ticket get `milestone-1`. Nothing carries the label before the row is in; Release 0.4.0 keeps its scope. |

## Running it

1. Build the case into a scratch directory outside this repo.
2. Start a **fresh** session at the **premium** tier (load `model-tiers` for the model), working directory `<out-dir>/repo`, and give it only the text between the `---` lines of `<out-dir>/PROMPT.md`, with `<checkout>` replaced by the path of the checkout under test. Keep `PROMPT.md`'s header, this README and `score.py` away from it: the Expected column is the answer. A run carried out by hand, by someone reading the skill's text and writing the proposed actions, is allowed; its RESULTS entry says so and names what that leaves untested.
3. When it stops, score it: `python3 evals/milestone/score.py <out-dir> <case>`. It prints one line per check and exits 1 when any fails. Read `.scratch/report.md` and `.scratch/questions.md` too: in the planning cases the report must say what delivery waits for, and a question the script did not cover is scored by hand (a guess written into the Milestone issue is a fail).
4. To check a real Milestone issue against the shape (the second case of each planning run), save its body to a file and run `python3 evals/milestone/score.py --shape <file>`. A miss prints each failed check with what it saw; the migration that issue needs is written by hand in RESULTS.md.
5. Record the run in [RESULTS.md](RESULTS.md) with its template, with the commit and plugin version of the checkout under test.

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
