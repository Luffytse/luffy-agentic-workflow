# Release thread report (2026-11-04)

**Where it started.** No open release issue and no open issue carrying a release label. The last release issue, #2 (Release 2), is closed with its notes and both end-of-Release records (triage and retro-planning), so this run went straight to planning the next Release (step 5). Nothing was cut.

**Planned: Release 3** (label `release-3`, release issue to be opened as #27), for Milestone #1 "Make the greeter usable from scripts".

Goal: the greeter reads a config file and prints JSON output that scripts can parse, with colour on top.

Order:
1. #26 Config file loader: #24 and #25 both depend on it, so it goes first. It has no blockers.
2. #25 JSON output for scripts: moves the Milestone's goal (use from scripts) furthest. I put it ahead of #24 even though the Milestone issue lists #24 first.
3. #24 Colour output: adds least to script use.

This differs from the Milestone issue's build order (#24, #25, #26). #26 moved up because the others are blocked on it, and #25 moved ahead of #24 because it serves the goal more directly.

Size: 5. Used: 3. No severe issues.

Left out: none.

Checked against main (`b5280c5`): #24, #25 and #26 are all still valid. `src/greet.sh` has only `hello`: there is no config loader, no `--json` and no colour.

Questions from the check: none. Unplanned features proposed: none. Nothing waits on a reply.
