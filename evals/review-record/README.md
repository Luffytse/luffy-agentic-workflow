# Review record interpretation fixture

The seam is the comment record that a continuing review and `retro` read back. `comments.json` holds one Ticket check, three Rounds and two comments that are not records (a discussion and a Pre-existing filing note), in the shapes `review-record` keeps: an id kept across comments, a Finding that gains a location and is later fixed, a Verifier's dismissal, a skipped Nit, a kept design, a Pre-existing Finding that gains a location, an Important that became a bug Ticket after Round 3 and one dismissed after Round 3. It tests reading only, not running a review or choosing a guardrail.

`bash evals/review-record/test-score.sh` checks the fixture and the scorer without an agent: the comments use only the kept shapes, `expected.json` covers every id, and `score.py` passes the expected answer and fails planted wrong ones.

## Run

1. Copy `comments.json` into a fresh directory of its own; keep `expected.json` outside it.
2. Start a fresh session there on the regular tier with only the `review-record` skill available, and send `prompt.txt`, adding "First load the review-record skill by name and apply its contract". Do not give it the expected answer.
3. Require an observed read of the skill body, a completed turn and no file changed.
4. Save its JSON answer and run `python3 evals/review-record/score.py <answer.json>`. The scorer compares the current state, the retrospective view (latest Severity and Status, every location the id was ever listed at, dismissed rows left out unless a skipped Nit, a kept design or dismissed after Round 3) and the ignored ids, as unordered sets.

## History

The 2026-10-31 baseline and candidate runs (Codex app-server sessions on the regular tier, both matching every field) read the earlier fixture, which also held merged rows, partly fixed rows and a Nit raised to Important. Their answers, evidence and that fixture are at commit `9b98dfe` (`git show 9b98dfe:evals/review-record/README.md`). This fixture has not been run by a model yet.
