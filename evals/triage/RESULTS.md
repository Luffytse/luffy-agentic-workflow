# Results

One entry per run of a `triage` eval case, newest first. Rerun when a pull request changes how `triage` behaves, as the [evals guide](../../docs/dev-skills/evals.md) says, and record the commit and the plugin version from `plugins/dev-skills/.claude-plugin/plugin.json`. An entry written inside an open pull request names the commit and plugin version it ran on as its base; anything after the entry's last commit is recorded on the pull request, not in the file.

## Template

```
### <date>, commit <sha>, dev-skills <version>

Setup: <case, skill under test (branch or main), run level>
Result: <score.py's line count and every FAIL, with what the run did>
Pass: yes | no. Lessons: <what to change in triage, if anything>
```

## Runs

### 2026-11-04, branch `claude/project-thread-gpmghz` (Ticket #680), commit 5fb3c74, dev-skills 0.75.1 (base, main d66fb5b): backlog-sweep case

Setup: the backlog-sweep case's expected result for the obsolete #32 changes from closed (any outcome) to closed as **completed**, with the reason. The skill change: sweep test 3 (Obsolete) and the single-issue "already implemented" outcome close as completed, not as not planned or `wontfix`, so a planned feature such an issue blocks is unblocked. Run level: decision-level in fresh subagents, premium tier, each given only the `PROMPT.md` text with `<checkout>` replaced (the branch's worktree at 5fb3c74, or a `git archive` of main d66fb5b). The Implementer built the case; the Ticket thread made the runs.

- **Self-test:** `python3 evals/triage/backlog-sweep/test_cases.py`: 16 tests OK (the reference closes #32 as completed; a planted close of #32 as not planned fails).
- **Case check:** fresh premium subagent: keep on all three questions. Its note: #32 blocks nothing in this fixture, so the unblocking is not watched here directly; the release main-check case covers it.
- **Branch's skill, premium: 16/16, pass.** #32 closed as completed, naming #8 (6ab449a). Evidence: `backlog-sweep/evidence/680-branch/`.
- **Main's skill (d66fb5b), premium: 15/16, fail, for the right reason:** only "obsolete #32 closed as completed" fails; main's sweep test 3 closed it as not planned. Evidence: `backlog-sweep/evidence/680-main/`.
- **report.md:** the subagent's write was refused in the branch run (#694); the Ticket thread wrote `680-branch/report.md` from the run's final text, and its first line says so. The main run wrote its own.
- Each score was reproduced by rebuilding the fixture and rescoring the kept files.
- **Eval:** behaviour change, so the case ran on the branch's skill and on main's (ADR 0013).

### 2026-11-04, branch `ticket-636`, dev-skills 0.61.0 (base): backlog-sweep case

Setup: the backlog-sweep case (`evals/triage/backlog-sweep/`), written before the skill text. Run by the Implementer of #636. Run level: `test_cases.py` (no model session) and a literal walkthrough against the pre-#636 `triage` (the branch's base, the same text as main's). The Implementer could not start fresh sessions; the coordinator made the model runs (below).

- **Self-test:** `python3 evals/triage/backlog-sweep/test_cases.py`: 15 tests OK (the reference run passes; every planted wrong run fails). An empty run scores 3/16.
- **Pre-#636 skill, literal (red):** its "Inside a Milestone" batch takes only `needs-triage` issues, so it decides #41 (joins the next Release, no mark: it has no `next-release` step) and #50 (a feature outside the agreement: goes to the user). It sweeps nothing: #31, #32 and #33 stay open, #40 and #51 are untouched. Expected FAILs: the duplicate, obsolete and expiry checks, `next-release`, both `ready-for-human` checks and the summary's list.
- **Branch's skill, literal (green):** part 1 makes #41 a `bug` at `ready-for-agent` with `next-release` (severe) and sends #50 to `ready-for-human` (agent-found). The sweep: #51 to `ready-for-human` (test 1, before expiry); #31 closed as a duplicate of #30 (#30 older, the same typo); #32 closed as obsolete (main defaults the name to `world` since #8); #40 marked (blocks the planned #20); #33 expired (left out of Releases 1, 2 and 3); #34 and #36 not in all three lists; #20 a planned feature, never expired. One `## Triage batch` summary on #4. This matches every expected row.
- **Fresh runs (2026-11-04, made by the coordinator):** one run each in a fresh premium-tier subagent given only the PROMPT.md text, with `<checkout>` set to a `git archive` copy (evals/ removed) of this branch at 1fbb97b or of main at c29d3b1, on a fixture from `make_fixture.py`, scored with `score.py`. The outputs and scores are in `backlog-sweep/evidence/<branch|main>/`; the Implementer rescored both run directories, with the same results.
  - **Branch: 16/16, no FAIL.**
  - **Main: 5/16, red.** 11 FAILs: #31, #32 and #33 not closed (6 checks); no `next-release` set (saw none, want #40, #41); the agent-found #50 put at `ready-for-agent`, no enhancement sent to `ready-for-human`, `ready-for-agent` left on #51; the summary leaves out #31, #32, #33 and #51.
  - **Correction:** the literal walkthrough above predicted main would send #50 to the user. It put #50 at `ready-for-agent` instead.
