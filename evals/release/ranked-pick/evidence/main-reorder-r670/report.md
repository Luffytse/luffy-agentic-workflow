# Release thread report (2026-11-04)

Release 2 is closed with its notes, and its triage and retro-planning records are both there, so this run planned the next Release. Nothing waits on your reply.

**Release 3** (label `release-3`, release issue #27, Milestone #1)

Goal: the greeter reads its config file and prints JSON and coloured output from it, so scripts can use it.

Size: 5. Used: 3.

Order:
1. #26 Config file loader: moved up from third in the Milestone's order, because #24 and #25 are both blocked by it.
2. #25 JSON output for scripts: moves the Milestone's goal (usable from scripts) furthest; its blocker #26 is placed above.
3. #24 Colour output: the last planned feature; it does less for script use than #25.

The build order differs from the Milestone issue's (#24, #25, #26), because #26 blocks the other two.

Left out: none. Proposed to you: none (no unplanned features). There are no severe, `next-release` or `ready-for-agent` bug issues.

Dry run: the release issue, the new `release-3` label and the three label changes are written to `.scratch/proposed-actions.md`.
