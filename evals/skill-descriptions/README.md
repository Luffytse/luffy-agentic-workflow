# skill-descriptions eval

Tests which skill a session picks from the plugin's skill **descriptions** alone (Ticket #621). The harness loads the name and description of every skill into every session before any skill body, so a change to a description changes which skill gets loaded. This eval measures that: given only the listing, does a session pick the right skill for a realistic prompt or caller situation, and does a new set of descriptions pick it as often as main's.

It lives outside the plugin (`evals/`), so changing it bumps no version.

## What it tests

- [`cases.py`](cases.py): each case has an id, a prompt, the expected skill (or `none`) and a kind:
  - `trigger`: at least 3 per skill, for all 35 skills, taken from each description's trigger branches, from callers that load the skill by name, and from real thread requests. The hidden skills (`user-invocable: false`: `docs-index`, `issue-absorption`, `merging`, `model-tiers`, `review-record`, `review-rounds`, `worker-control`) are listed to the model with their descriptions like any other, so they have caller situations ("a build workflow reached its merge step").
  - `near-miss`: the wording decides between two neighbours (`grilling` / `grill-with-docs`, `retro` / `retro-planning`, `implement` / `implement-spec`, `to-spec` / `wayfinder`, `agentic-review` / `review-rounds`, `docs-index` / `domain-modeling`, `setup-dev-skills` / `setup-project`, and more). The case's expected skill is the right one of the pair.
  - `none`: no skill applies.
- Prompts never name the expected skill. The only exceptions are the ids in `ALLOW_NAME_IN_PROMPT`, where the name is the ordinary word the description quotes as the user's trigger (`Milestone`, `Release`, `Triage`); `test_cases.py` fails any other prompt that carries the name.
- A new case, or a changed expected result, gets the **Case check** of [`docs/dev-skills/evals.md`](../../docs/dev-skills/evals.md#case-check) before it is used in a run.

## Run level and tier

| Check | Run level | Tier |
| --- | --- | --- |
| `test_cases.py` | no model session: the listing builder, cases, batches, scorer and comparator on planted input | none |
| the batches | decision-level: a fresh subagent given only the skill listing and a few prompts; it answers which skill it would load first | regular |

The decision is the whole test: the subagent never loads a skill. A run at the real harness level (a top-level session with the plugin installed) is not part of this eval.

## Run it

All commands run from the repo root. `<skills-dir>` is a checkout's `plugins/dev-skills/skills`, or the same folder inside a `git archive` of main; never the installed plugin cache.

1. Get main's skills: `git archive origin/main plugins/dev-skills/skills | tar -x -C <scratch>/main-src`. The branch's are the checkout's folder.
2. Look at the listing and the word counts: `python3 evals/skill-descriptions/build_listing.py <skills-dir>` prints one `- dev-skills:<name>: <description>` line per skill, descriptions read from each `SKILL.md` frontmatter; add `--counts` for the words per description and the total.
3. Build the batches into one folder per run, so main's and the branch's sit side by side: `python3 evals/skill-descriptions/make_batches.py <skills-dir> <scratch>/base` and again with the branch's folder into `<scratch>/new`. It writes `listing.txt`, `batch-NN.md` (the listing plus 7 prompts, no expected answers), `batches.json` (batch -> {situation label: case id}) and an empty `answers/`. Each prompt is headed by an opaque label (`S1`, `S2`, ...) and never its case id, because ids hold the expected skill's name. The shuffle uses a fixed seed, so both runs get the same batches.
4. Start fresh **regular**-tier subagents in **one parallel batch**, one per batch file per version (main's and the branch's, all sent together), as [`docs/dev-skills/evals.md`](../../docs/dev-skills/evals.md#making-model-runs) says. Best: paste each subagent the text of its `batch-NN.md` and nothing else, so it needs no file access. The recorded runs used the weaker method: each subagent was told to read exactly one batch file from the run folder. It holds a read tool, so the folder is reachable, and `batches.json` there maps labels to case ids, which carry the expected skill. This is a known limitation, mitigated only because the instruction names a single file; paste the text in future runs. Either way give no subagent `cases.py` or the scorer. Each replies with one JSON object `{situation label: skill}`. Save each reply as `<scratch>/<run>/answers/batch-NN.json`.
5. Score a run: `python3 evals/skill-descriptions/score.py <scratch>/new` (the run folder; it reads `batches.json` to turn labels back into case ids) prints overall accuracy, accuracy per expected skill and the confusion pairs (expected -> got) of every miss. A case with no answer, and a JSON null or other non-string answer, is a miss.
6. Compare: `python3 evals/skill-descriptions/compare.py <scratch>/base <scratch>/new`. The new run **passes** when it picks the expected skill
   - at least as often as the baseline overall,
   - at least as often as the baseline on the cases of every skill, and
   - with no new near-miss confusion pair: no miss (expected -> got) on a near-miss case that the baseline did not also make.

   A pair that is new but comes from a trigger case, and a drop on the `none` cases, print as warnings and do not fail the run. Exit status 0 is a pass.
7. Record both runs in [RESULTS.md](RESULTS.md) with the commit, plugin version, tier, run level, word counts and the score and comparison output.

Model answers vary between runs. A baseline miss that flips on a rerun is noise; when a comparison fails on one case, rerun that case's batch on both versions before treating it as a regression.

## Self-test

`python3 evals/skill-descriptions/test_cases.py` (run by `scripts/run-tests.sh`) needs no model. It checks the listing builder on a planted folder and on the real one (35 skills, hidden ones included), that the cases cover all 35 skills with at least 3 trigger prompts each, that every expected name is a real skill, that no prompt names its expected skill, that a batch holds the listing and the prompts under opaque labels and never an expected answer, a case id or a skill name in a header, and that the scorer and comparator give the right verdict on planted answers (same, better, worse overall, worse for one skill, a new near-miss pair).
