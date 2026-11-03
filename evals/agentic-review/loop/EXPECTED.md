# Loop cases: expected results

One fresh top-level session per case, given its `PROMPT.md`. Keep this file and `score.py` away from it. After the run, `python3 evals/agentic-review/loop/score.py <case> <out-dir>` checks the outcome from the files the run left; the points below that it cannot see are scored by hand from the session's report and tool calls.

## `merge`: Round 2 after a merge of main

Since Round 1 (head in `.scratch/pulls/1/01-round-1.md`), branch `quota` has one fix commit and one merge of `main`. The merge conflicted in `remaining`, and its resolution reads `max(0, used - limit)`: `remaining(3, 10)` is 0, not 7. `main` itself is right (`max(0, limit - used)`), and it also brought in `app/report.py`, whose `usage_percent` divides by a zero limit: a real bug, but not this pull request's.

A run passes when:

- it posts one Round 2 comment, `round=2`, its head the merge at the tip of `quota` and its base Round 1's head (`score.py`);
- it reviewed the new commits with `git log -p --first-parent --remerge-diff <round-1 head>..HEAD`, or a command that shows the same: the fix commit and the merge's resolution, nothing from `main` (hand, from the tool calls);
- it started one Finder (standards and spec in one, regular tier) and one Verifier, no adversarial Finder (`score.py` reads the Finders line; hand, from the subagents started);
- R1-1 is `fixed`, and an open Important sits on the resolution's line in `app/quota.py` (`score.py`);
- no row names `app/report.py` or `usage_percent` (`score.py`);
- it stops at Round 2's report, or goes on to fix and run Round 3 as the owner; either is right, as long as Round 2's comment is as above.

## `after-round3`: the sort after Round 3

Round 3 of branch `fix` is not clean: R3-1 (`remaining` goes below zero, against the spec's "never below zero") is a real Important at the head, and R3-2 is a "fix" Nit. Nothing was committed since.

A run passes when:

- one brand-new premium-tier agent sorted the open Importants (hand, from the subagents started);
- R3-1 became exactly one issue, labelled `bug` and `ready-for-agent`, naming `app/quota.py:<line of return limit + burst - used>` and linking the pull request; R3-2 was not filed (`score.py`);
- Round 3's comment was edited: R3-1's Note carries `bug Ticket: <the issue's path>`, and the Result reads `sorted after Round 3: 1 bug Ticket, 0 dismissed` (`score.py`);
- no Round 4 was run and nothing new was committed (`score.py`);
- its report says the pull request is ready to merge and the bug Ticket is to be worked straight away, and it asked the user nothing (the Boundary record lists nothing) (hand).

Dismissing R3-1 fails the case: the Finding is real at the head and breaks the spec's acceptance criterion.

Record each run in [`../RESULTS.md`](../RESULTS.md) with `score.py`'s output and the hand-scored points.
