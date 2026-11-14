# Repeated Bug classes

A **Bug class** that comes up more than once in a pull request is filed as a Retro issue that proposes a check or a `REVIEW.md` line, so a later Review need not catch it again. The retro builds neither: no branch, no pull request.

## Procedure

1. **Load the `review-record` skill by name**, then read every comment on the pull request, all pages, and select the Round and Ticket-check comments that carry a Finding table (a Round 0 line at level None has none). None kept: say so, end this procedure, and go on to the next step of `retro`.
2. **Build the historical view** using `review-record`'s successive-comment interpretation and retrospective inclusion rules.
3. **Group the rows by Bug class.** Merge names that mean the same kind of problem, and say which. A class's **instances** are its distinct locations across all its Findings. It is **repeated** when it has more than one instance, in one Finding or across Findings and Rounds.
4. **File each repeated class** as one Retro issue through [FILING.md](FILING.md), like every other candidate. The issue proposes the check (a mechanical class: a rule, script line, hook or CI job) or one `REVIEW.md` Always-check line (a judgement class), in the form `- **<Bug class>** (files: `glob`, `glob`; from <origin>): what to look for` (`(files: all)` only when it fits every file), and names the Finding ids.
5. **Report a table**, one row per Bug class, the last column giving the issue it went to. Classes with one instance read "not repeated" and need no issue.

| Bug class | Instances | Finding ids | Issue |
| --- | --- | --- | --- |
| Unchecked null from the API client | 3 | R1-2, R2-1 | #41, proposes a lint rule |
| Error messages leak internals | 2 | R1-4 | #42, proposes a `REVIEW.md` line |
| Wrong default in config loader | 1 | R1-1 | Not repeated |
