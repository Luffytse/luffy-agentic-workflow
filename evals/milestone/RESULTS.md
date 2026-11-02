# Results

One entry per run of the `milestone` skill's planning-phase dry run, newest first ([README](README.md) says how to build, run and score it). Record the commit and the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`; an entry written inside an open pull request names the commit and version it ran on as its base. Each run also applies the shape to one real Milestone issue (`score.py --shape`) and names the migration it needs, if any.

## Template

```
### <date>, commit <sha>, dev-skills <version>: <case>

Driven by: <a fresh session at the premium tier | by hand, reading the skill's text>; skill text from <path, branch>
Proposed actions: <the numbered blocks, in short; the Milestone issue body when one was written>
Score: <n>/<m> (`score.py <out-dir> <case>`); questions not covered by the script: <none | list>
Report: <what it said comes next and what delivery waits for>
Before: <the same case run on the skill text before the change, and its score>
Real Milestone issue: <issue>, `score.py --shape`: <result; the migration it needs, or "matches">
Not exercised: <what this run did not reach>
Pass: yes | no. Lessons: <what to change in the skill, if anything>
```

## Runs

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

Not exercised: a fresh session following the skill (the run was by hand, by the skill's author); the user planning a feature inside the run with `grill-with-docs`, `to-spec` or `to-tickets` (the `plan` features were planned beforehand, and the `add-feature` plan was scripted in one answer); a real tracker; Startup verification and delivery, which follow planning.
Pass: yes for both cases, as a by-hand run. Lessons: labelling the issues a feature absorbs was unclear in the first draft ("its Tickets or related issues"); the skill now says every open issue the feature holds, its own, its Tickets, the issues it absorbs or its related issues. A rerun by a fresh premium-tier session is the next evidence to get.
