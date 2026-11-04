# triage eval

Checks of the `triage` skill (`plugins/dev-skills/skills/triage/`). Each run gets an entry in [RESULTS.md](RESULTS.md).

## Run level

| Check | Run level |
| --- | --- |
| `backlog-sweep/test_cases.py` | no model session: builds the case and scores a reference run and planted wrong runs |
| the backlog-sweep case | decision-level in a fresh session: every tracker write is a block in `.scratch/proposed-actions.md`, so nothing real is labelled, commented on or closed |
| `repo-labels/test_cases.py` | no model session: builds both cases, checks the rendered files, and scores a reference run and planted wrong runs |
| the repo-labels cases (`table`, `empty`) | decision-level in a fresh regular-tier session, as the backlog-sweep case (dry-run tracker, `.scratch/proposed-actions.md`) |

## Backlog-sweep case

[`backlog-sweep/make_fixture.py`](backlog-sweep/make_fixture.py) builds the case outside this repo: `python3 evals/triage/backlog-sweep/make_fixture.py <out-dir>`. It makes `<out-dir>/repo` and `<out-dir>/PROMPT.md`. The repo is the release eval's tiny shell greeter and dry-run local tracker (`evals/release/ranked-pick/make_fixture.py`), with an `Author:` header on each issue and a `duplicate` close outcome. Milestone 1 (#1) lists #10 Farewell (shipped in Release 3) and #20 Quiet flag. Releases 1, 2 and 3 (#2, #3, #4) are closed, each with an Order, a Left out list and its notes; Release 3 was cut just now and has no end-of-Release record yet. The run is its Triage batch, as `release` step 4 runs it. The case data and the expected outcome are in [`backlog-sweep/sweep_case.py`](backlog-sweep/sweep_case.py).

| Issue | Fixture | Expected |
| --- | --- | --- |
| #30, #31 | two `ready-for-agent` bugs reporting the same `helo` typo in the usage line, still on main; #31 is newer | #31 closed as a duplicate (or not planned), linking #30; #30 stays open |
| #32 | `ready-for-agent` bug: `hello` with no name prints `Hello, !`; main defaults the name to `world` since pull request #8, which did not close it | closed as completed (main already does it), with the reason |
| #33 | `ready-for-agent` bug, still true on main, in the Left out lists of Releases 1, 2 and 3 | closed as not planned, saying "reopen to bring it back" |
| #34 | the same, left out of Releases 2 and 3 only | stays open |
| #36 | the same, left out of Releases 1 and 3, not 2 | stays open |
| #20 | the Milestone's planned feature, left out of all three Releases | stays open (never expired) |
| #40 | `ready-for-agent` bug that blocks #20 | gains `next-release` |
| #41 | new at `needs-triage`: every name is written to a world-readable log (true on main) | `bug`, `ready-for-agent` and `next-release` |
| #50 | new at `needs-triage`: an enhancement an agent found in an audit | `ready-for-human`, not closed, unmarked |
| #51 | an agent-found enhancement left at `ready-for-agent`, in all three Left out lists | `ready-for-human`, `ready-for-agent` removed, not closed |

No other issue gains `next-release`, no release label is applied, every comment starts with the triage disclaimer, and one `## Triage batch` summary on #4 names #31, #32, #33, #40, #41, #50 and #51.

### Running the case

1. Build it into a scratch directory outside this repo.
2. Start a **fresh** session at the **premium** tier (load `model-tiers` for the model), working directory `<out-dir>/repo`, and give it only the text between the `---` lines of `<out-dir>/PROMPT.md`, with `<checkout>` replaced by the checkout under test. Keep this README, `sweep_case.py`, `score.py` and `test_cases.py` away from it: the Expected column is the answer.
3. Score it: `python3 evals/triage/backlog-sweep/score.py <out-dir>`. It prints one line per check and exits 1 when any fails. Read `.scratch/report.md` too. If the run cannot write `.scratch/report.md`, it returns the report text as its final message and the thread writes that text to the file before scoring, the same way for the branch and main runs ([evals guide](../../docs/dev-skills/evals.md#making-model-runs)).
4. Run it on the branch's skill and on main's, and record both in [RESULTS.md](RESULTS.md) with the commit, plugin version and run level; keep each run's `.scratch/proposed-actions.md`, `.scratch/report.md` and score in `backlog-sweep/evidence/<branch|main>/` (`branch/` and `main/` hold the runs of #636; the runs of Ticket #680 are in `680-branch/` and `680-main/`).

### Self-test of the case

`python3 evals/triage/backlog-sweep/test_cases.py` builds the case and scores a reference run written from the expected outcome; the reference must pass, and planted wrong runs (a duplicate closed with no link, an obsolete issue closed with no reason or as not planned, the issue left out twice expired, an expiry without "reopen to bring it back", an agent-found enhancement expired, put at or left at `ready-for-agent`, the planned feature expired, the severe issue or the feature-blocker unmarked, an extra mark, a release label applied, no summary, a comment without the disclaimer) must fail. It proves the builder and scorer agree; it is not a model run of the skill.

## Repo-labels cases

Gap: the `to-spec` whole-Spec rule (a label must fit the whole Spec) has no eval case, because `to-spec` is a conversation-driven synthesis skill with no seam these fixtures can score; it is covered by review of the pointer text only, and the PR's `**Eval:**` line names it.

Checks of the repo labels rule `triage` holds (Roles, **Repo labels**; Spec #690, Ticket #692). [`repo-labels/make_fixture.py`](repo-labels/make_fixture.py) builds a case outside this repo: `python3 evals/triage/repo-labels/make_fixture.py <out-dir> <table|empty>` makes `<out-dir>/repo` and `<out-dir>/PROMPT.md`. The repo is a small orders app (`ui/`, `api/`) on the backlog-sweep case's dry-run local tracker, with Milestone 1 (#1), the closed Release 1 (#2) and five open `needs-triage` issues. The run is part 1 of the Triage batch for Release 1 (the sweep and the summary are skipped). The data and expected outcome are in [`repo-labels/label_case.py`](repo-labels/label_case.py). The tracker's label list also holds `performance`, `security` and `docs`, which the table does not list.

Case `table`: the triage-labels doc has a Repo labels table with `frontend` (work under `ui/`) and `backend` (work under `api/`).

| Issue | Fixture | Expected |
| --- | --- | --- |
| #10 | UI bug: the Pay button text is cut off (`ui/cart.html`) | ends with `frontend`, not `backend` |
| #11 | CONTRIBUTING.md names a test command that does not exist | neither label |
| #12 | the orders list is slow, one query per order (`api/orders.py`) | ends with `backend`, not `frontend`, and none of `performance`, `security`, `docs` |
| #13 | already carries `frontend`; the work is all in `api/export.py` | `frontend` removed, `backend` added, and a comment on #13 that names `frontend` |
| #14 | UI bug (`ui/footer.html`) carrying `backend`; the prompt says the user asked that #14 keep it (the issue also holds the owner's comment as colour) | `backend` still on it (removing it fails) |

No label outside the roles and the table is applied or created, and every comment starts with the triage disclaimer.

Case `empty`: the same backlog and the same labels on the issues, with the Repo labels table empty. No issue gains or loses `frontend` or `backend`, and no label outside the roles is applied (a repo with no Repo labels rows sees no change).

Which cases discriminate: in the first runs neither case separated the branch from main (main's agent applied the table's labels itself), so both are regression guards for the rule, and `empty` guards "no rows, no change". Scorers read outcomes only: each issue's labels after the run's Apply / remove labels blocks, the comments on it and any label created, never how a comment is phrased.

### Running the cases

1. Build each case into its own scratch directory outside this repo.
2. Start a **fresh** session at the **regular** tier (load `model-tiers` for the model), working directory `<out-dir>/repo`, and give it only the text between the `---` lines of `<out-dir>/PROMPT.md`, with `<checkout>` replaced by the checkout under test. Keep this README, `label_case.py`, `score.py` and `test_cases.py` away from it.
3. Score it: `python3 evals/triage/repo-labels/score.py <out-dir> <table|empty>`. It prints one line per check and exits 1 when any fails.
4. Run it on the branch's skill and on main's (`git archive <main sha> plugins | tar -x -C <dir>`, so the session reads the skills but not `evals/`), and record both in [RESULTS.md](RESULTS.md); keep each run's `.scratch/proposed-actions.md` and score in `repo-labels/evidence/<ticket>-<branch|main>-<case>/`.

### Self-test of the cases

`python3 evals/triage/repo-labels/test_cases.py` builds both cases, checks what a session would read (the Repo labels rows are in the doc for `table` and absent for `empty`; #13 carries `frontend` and names only an API file; #14 carries `backend`, names only a UI file and holds the owner's comment; no issue body names a label, and the prompt names only `backend`, in the line where the user asks that #14 keep it; the tracker lists the unlisted labels), then scores a reference run written from the expected outcome. The reference must pass, and planted wrong runs (a UI bug given both labels or none, an unmatched issue given a label, an unlisted label applied or created, the stale label left on, or removed with no comment or one that does not name it, the user-named label removed, a comment without the disclaimer, and for `empty` a repo label applied or removed) must fail. It is not a model run of the skill.
