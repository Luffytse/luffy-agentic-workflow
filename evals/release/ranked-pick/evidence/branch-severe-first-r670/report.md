# Release thread report (2026-11-04)

**Where it started.** No open release issue and no open issue carries a release label. The last release issue, #2 (Release 2), is closed with its notes and holds both end-of-Release records (triage, retro-planning), so this run went straight to step 5: plan the next Release under Milestone #1.

**Release 3 planned** (release issue to be opened as #36, label `release-3`, which is created). Size 5, used 5; nothing joined past the size.

Order:
1. #31 greet.sh writes every name to a world-readable log: severe (security hole: names, some of them email addresses, go to `/tmp/greet.log` at mode 0666).
2. #35 test.sh takes 10 s: marked `next-release` by Release 2's Retro planning (the mark is removed once it carries `release-3`).
3. #10 Farewell command (Spec, with Tickets #11, #12): planned feature; a new command moves the Milestone's goal furthest; first in the Milestone's order.
4. #20 Quiet flag: planned feature; nothing depends on it; second in the Milestone's order.
5. #30 Typo in usage text: `ready-for-agent` bug, the oldest (2026-09-01).

Left out: none.

Checked against main (`41bd115`): all seven open issues (#10, #11, #12, #20, #30, #31, #35) are still valid. On main, `src/greet.sh` still appends `$2` to `/tmp/greet.log` and runs `chmod 0666` on it, the usage line still says `helo`, there is no `bye` command and no `-q`, and `test.sh` still has `sleep 10`. Nothing was closed or edited, and no questions came up.

Proposed to you: no unplanned features.

Notes:
- The skill says to give a check of more than 5 issues to premium-tier subagents. This thread had no way to start subagents, so I checked all seven myself against main.
- There is no remote, so the local `main` stood in for freshly fetched main.
- Dry run: every write is recorded in `.scratch/proposed-actions.md` (actions 1-10). The tracker files were not changed, and no commit or branch was made.
