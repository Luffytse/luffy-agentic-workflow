#!/usr/bin/env bash
# Builds one fixture for the reuse rule of the milestone skill's Startup verification.
# Usage: make-fixture.sh <out-dir> <same|runtime|reference|old|failure|failedrow>
# Makes <out-dir>/records (what the tracker and Harness show) and <out-dir>/PROMPT.md (the scripted prompt for a
# fresh regular-tier coordinator). See evals/startup-verification/README.md.
set -eu
out="$1"; case_="$2"
case "$case_" in same|runtime|reference|old|failure|failedrow) ;; *) echo "unknown case: $case_" >&2; exit 2 ;; esac
[ -e "$out" ] && { echo "$out exists" >&2; exit 2; }
mkdir -p "$out/records" "$out/.scratch"
out="$(cd "$out" && pwd)"
rec="$out/records"

posted="2026-10-20"; perm_then="default"; perm_now="default"
ref_changed="2026-09-30"; cc_row="pass"; failure="None recorded."
case "$case_" in
  runtime) perm_now="bypass permissions" ;;
  reference) ref_changed="2026-10-28" ;;
  old) posted="2026-09-25"; ref_changed="2026-09-01" ;;
  failure) failure="Retro #77 (2026-11-01): Confirmed stop failed in Milestone 2's delivery; a stopped worker still read as running after 10 minutes." ;;
  failedrow) cc_row="not relied on" ;;
esac

cat > "$rec/earlier-result.md" <<MD
Comment on Milestone 2 (issue #2, closed), posted $posted. Link: https://tracker.example/acme/greeter/issues/2#issuecomment-2001

## Startup verification

Harness: claude.ai project threads (claude-code-project-threads) · Role: coordinator · Runner: the coordinator · Run: ${posted}T09:00Z–${posted}T10:40Z UTC
Runtime: claude.ai project; permission mode: $perm_then; sandbox: on (read from settings); tools held: start_thread, message_thread, archive_thread

| Capability | Essential | Method and source | Result | Evidence | Limits |
|---|---|---|---|---|---|
| Start a worker | yes | start_thread; reference | pass | thread t-101 listed running | none |
| Worker state | yes | thread list; reference | pass | t-101 read running at 09:05 | none |
| Pause and resume | yes | message; reference | pass | paused 09:10, resumed 09:14 | none |
| Confirmed stop | yes | archive; reference | pass | running 09:20, archived 09:22 | none |
| End or failure notice | yes | done reply; reference | pass | wake at 09:30, state done | failure not provoked |
| Scheduled check-in | no | check-in method; reference | $cc_row | arrival 10:35, ended 10:38 | none |
| Loaded skill version | yes | model-tiers load path | pass | installed 1.1.0, main 1.1.0 | none |

Verdict: ready
MD

cat > "$rec/harness-now.md" <<MD
Today is 2026-11-09.
Harness detected now: claude.ai project threads (claude-code-project-threads)
Runtime line read now: claude.ai project; permission mode: $perm_now; sandbox: on (read from settings); tools held: start_thread, message_thread, archive_thread
Installed plugin version: 1.3.0. Main's plugin version: 1.3.0.
MD

cat > "$rec/reference-history.md" <<MD
Commits on main touching plugins/dev-skills/skills/worker-control/claude-code-project-threads.md (newest first):
- $ref_changed  abc1234  docs: note the scheduler's one-hour minimum
- 2026-08-14  def5678  feat: add the stop worker
(Other worker-control references are not listed: they are for other Harnesses.)
MD

cat > "$rec/recorded-failures.md" <<MD
Failures of a Worker control capability recorded since the earlier result (Milestone reports, Retros, later results):
$failure
MD

{
  echo "Text between the --- lines is the whole prompt. <checkout> is the path of the checkout under test."
  echo "---"
  cat <<TXT
You are the coordinator of the project "greeter". Milestone 3 is planned and delivery waits for its Startup verification. Follow the \`milestone\` skill's Startup verification in <checkout>/plugins/dev-skills/skills/milestone/SKILL.md (and the skills it loads, in <checkout>/plugins/dev-skills/skills/).

This is a dry run: you cannot start workers or call the tracker. Read the records in $rec: the earlier Startup verification result on Milestone 2's issue, what the Harness and runtime show now, the commit history of the worker-control reference for this Harness, and the failures recorded since. Assume every probe you decide to run now passes.

Write the comment you would post on Milestone 3's issue to $out/.scratch/result.md, in the shape the skill gives. For a row you run now, write its Evidence as "ran now (simulated)". Do not read any other file under $out.
---
TXT
} > "$out/PROMPT.md"
echo "built $case_ fixture in $out"
