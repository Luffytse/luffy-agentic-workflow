#!/usr/bin/env bash
# Focused overlay on the existing delivery tracker; see README.md.
set -eu
out="$1"
bash "$(dirname "$0")/make-fixture.sh" "$out" deliver
cat >> "$out/repo/.scratch/issues/00-milestone.md" <<'MD'

## Comment start-helper (10:00Z)
<!-- milestone delivery thread -->
check-helper; skill milestone; tier cheap; arrange check-ins.

## Comment start-planner (10:01Z)
<!-- milestone delivery thread -->
release-planner; skill release; tier regular; plan the first Release.
MD
cat > "$out/PROMPT.md" <<'MD'
# Thread end identity dry run

---
Read <checkout>/plugins/dev-skills/skills/milestone/SKILL.md and this repo's
CLAUDE.md and tracker doc. Continue delivery of 00-milestone.md in dry-run mode.
The two recorded threads already run. Preserve the fixture's tracker reads and
numbered proposed-action blocks, separated by `## Event <k>` headings. Do not
run world.sh; this case keeps the tracker state fixed except your own records.

- Event 1 (10:02Z): check-helper reports that the scheduler refused its target.
  release-planner has not reported; there is still no release issue.
- Event 2 (10:03Z): the user says "Continue delivery." No thread has reported.
- Event 3 (10:04Z): release-planner reports that it planned no Release.
  Re-read the tracker: the features remain open and eligible, with no release
  issue, so take whatever steps delivery now calls for.

Stop after event 3. Record all actions; do not perform real starts or writes.
---
MD
