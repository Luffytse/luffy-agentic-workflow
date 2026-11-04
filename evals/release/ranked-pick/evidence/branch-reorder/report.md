# Release thread report (2026-11-04)

Where I started: no open release issue, and the last one, Release 2 (#2), is closed with its notes and both end-of-Release records (triage, retro-planning). So nothing was cut this run; I went straight to planning the next Release.

## Release 3 planned (release issue #27, label `release-3`)

Goal: Scripts can configure the greeter from a config file and parse its output as JSON, with colour output from the same config.

Size: 5. Used: 3 (every candidate fit).

Order:
1. #26 Config file loader: moved up from third in the Milestone's order, because #24 and #25 both depend on it.
2. #25 JSON output for scripts: does most for the Milestone's goal (usable from scripts), so it goes ahead of #24.
3. #24 Colour output: also needs #26, does less for scripts; last.

Left out: none.
Proposed to you (unplanned features): none.

Nothing waits on your reply. The tracker writes are in `.scratch/proposed-actions.md` (dry run): create #27, create label `release-3`, label #26, #25 and #24 with it. None of them carried `next-release`.
