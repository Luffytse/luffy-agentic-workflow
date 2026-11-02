# milestone eval

Checks of the `milestone` skill's **planning phase**: does the coordinator write the Milestone issue with the user in the skill's shape, label every planned feature with the membership label from the Boundary record's form, add nothing the user did not plan, stop before delivery until Startup verification passes, and add a feature mid-Milestone only after planning it, listing it before labelling it? Startup verification has its own results file, [`../startup-verification/RESULTS.md`](../startup-verification/RESULTS.md). Each run gets an entry in [RESULTS.md](RESULTS.md).

## Fixture

[`make-fixture.sh`](make-fixture.sh) builds one scratch repo per case, outside this repo: `bash evals/milestone/make-fixture.sh <out-dir> <plan|add-feature>`. It makes `<out-dir>/repo` (a git repo, one commit on `main`) and `<out-dir>/PROMPT.md` (the scripted prompt, with the user's answers).

Every case's repo is a tiny shell greeter with a Boundary record (label form `milestone-<n>`; sending messages to customers needs approval; budget none), a release doc where Releases bump `VERSION`, and two planned features that fit one Release: the Spec `10-farewell.md` with its Tickets `11-bye-code.md` and `12-bye-usage.md`, and the lone Ticket `20-quiet.md`. `30-colour.md` is a raw `needs-triage` request nobody has planned.

The **dry run** lives in the fixture's tracker doc (`docs/agents/issue-tracker.md`): reads read the issue files, and every write (creating an issue or a label, editing a body, labelling, linking a sub-issue, commenting, closing, and starting a thread) is appended as a numbered block to `.scratch/proposed-actions.md` instead of being made. The skill needs no dry-run mode of its own: it acts through the tracker doc's operations, and the fixture's tracker doc records them.

| Case | Starting state | The user asks | Expected |
| --- | --- | --- | --- |
| `plan` | no Milestone label or issue | "Let's start a Milestone" (goal, features 10 and 20, order, acceptance, exclusions, budget and one extra boundary scripted) | `milestone-1` created, then one issue `Milestone 1: ...` carrying it, in the skill's shape: farewell then quiet, "up to 2 at once", each row with its acceptance criteria, colour and translations excluded, the registry approval under Boundaries. Then 10, 11, 12 and 20 labelled and 10 and 20 linked as sub-issues (11 and 12 keep their Spec parent). 30 never labelled. No release label, no thread started; the report says Startup verification comes next and delivery waits for its `Verdict: ready`. |
| `add-feature` | Milestone 1 open with features 10 and 20, Startup verification `Verdict: ready`, Release 0.4.0 open with both features | "Add colour output (issue 30) after the quiet flag" | The colour feature is planned first (a Ticket written for it), then the Milestone issue's body is rewritten with a third row marked `(added 2026-11-02 by the user)` and the rest unchanged, and only then does the colour Ticket get `milestone-1`. Nothing carries the label before the row is in; Release 0.4.0 keeps its scope. |

## Running it

1. Build the case into a scratch directory outside this repo.
2. Start a **fresh** session at the **premium** tier (load `model-tiers` for the model), working directory `<out-dir>/repo`, and give it only the text between the `---` lines of `<out-dir>/PROMPT.md`, with `<checkout>` replaced by the path of the checkout under test. Keep `PROMPT.md`'s header, this README and `score.py` away from it: the Expected column is the answer. A run carried out by hand, by someone reading the skill's text and writing the proposed actions, is allowed; its RESULTS entry says so and names what that leaves untested.
3. When it stops, score it: `python3 evals/milestone/score.py <out-dir> <case>`. It prints one line per check and exits 1 when any fails. Read `.scratch/report.md` and `.scratch/questions.md` too: the report must say what delivery waits for, and a question the script did not cover is scored by hand (a guess written into the Milestone issue is a fail).
4. To check a real Milestone issue against the shape (the second case of each recorded run), save its body to a file and run `python3 evals/milestone/score.py --shape <file>`. A miss names the migration that issue needs.
5. Record the run in [RESULTS.md](RESULTS.md) with its template, with the commit and plugin version of the checkout under test.

The fixture also holds what the delivery phase's checks need (two features that fit one Release, a release doc); the `plan` case stops before delivery.
