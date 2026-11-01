# Results

## 2026-10-31 — #368 local candidate migration

Baseline source: `8ff823f913b951cb3c48b476ec1eda08c35d4601`, archived from git. Candidate: that source plus the #368 working-tree extraction. Each case's `provenance.json` records every installed skill file's SHA-256, CLI identity, discovered names and selected caller. The actual tested `issue-absorption`, `retro-planning`, `to-tickets` and `pr` bodies match the delivered candidate; subsequent edits only completed builder load points and repository documentation. Installed locally into four separate empty homes; this is not the final GitHub install gate.

All four fresh app-server turns completed successfully using `regular Codex tier from plugins/dev-skills/README.md at 8ff823f913b951cb3c48b476ec1eda08c35d4601`, provider fallback disabled. Only the caller skill item was injected. Baseline discovered 26 plugin skills, candidate cases 27; no missing, disabled or discovery-error entries. Completed tool items show each candidate consumer reading the installed `issue-absorption/SKILL.md` before producing its artifact. Exact turns and full completed command/file-change items are retained, with temporary-root paths replaced by `<isolated>`. Authentication and reasoning are excluded.

| Case | Observed result |
| --- | --- |
| Open Ticket | #11 and #15 wait on #31 and remain ineligible for closure. |
| Completed Ticket | #12 and #17 are eligible for a later user-approved mechanical close with #32. |
| Abandoned/not-planned and duplicate | #13 and #14 remain in the backlog with two votes, neither waiting nor failed-fix candidates. |
| Later absorption | #15's newer open absorber wins over completed #35; #17's newer completed absorber wins over open #31. |
| Recurrence | #16 retains three votes and becomes a failed-fix candidate, not a mechanical close. |
| Unrelated report | #18 remains in the backlog. |
| PR selection | Exactly #100, #31, #32, #11, #12, #15, #17 receive separate closing lines. Superseded, dropped, unlanded and unrelated sources are excluded; a later abandoned absorber excludes #13 despite old landed #31 criteria. |
| Writer | Both source-body requirements and comment requirements appear in acceptance criteria: decimals, blanks, timezones and DST offsets. Links replace copied briefs; separate criteria and exact absorption comments cover #21 and #22. Already-closed #23 is absent; no parent linkage was written. |

Baseline and candidate lifecycle artifacts agree on all eight source statuses, authoritative Tickets, retained votes and closure eligibility. This is a behavior-preserving extraction: no red failure is claimed. The first scorer run rejected the optional `## Closes` heading; its artifact reader was corrected to select closing-keyword lines and check their count, without changing the runtime output. The independent scorer passes against the observed artifacts. Consumer inventory: `to-tickets` writes, `retro-planning` reads and writes, `pr` selects closing lines, `implement-spec` maintains them and completes closure, `implement` completes closure. Builder load points were inspected; their full build/merge workflows were not executed. `release` uses absorption only for feature membership, and `prototype` uses an unrelated word sense, so neither migrated.

`check-plugin.sh`, all five packaging tests, `claude plugin validate .` and whitespace checks pass. No visual surface changed. Claude menu hiding is requested by `user-invocable: false`; Codex implicit invocation is enabled. Menus were not inspected, so visibility is unmeasured and is not inferred from discovery. No real issue was closed, no external comment was posted, and no release version changed. **Door: two-way** — reverting the source change restores the prior instructions; evaluation writes were isolated fixture artifacts.
