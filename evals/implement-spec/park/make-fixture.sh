#!/usr/bin/env bash
# Builds one park-check fixture for the build-flow eval of implement-spec (step 5, the third Ticket check).
# Usage: make-fixture.sh <out-dir> <inside|outside>
# Starts from the merge-authority fixture's `spec` flow (no-milestone case), then plants a Ticket that cannot pass
# its Ticket checks, adds a free Ticket, and gives the tracker doc the Park and Comment operations.
# Makes <out-dir>/origin.git, <out-dir>/repo and <out-dir>/PROMPT.md. See evals/implement-spec/park/README.md.
set -eu
out="$1"; membership="$2"
case "$membership" in inside|outside) ;; *) echo "unknown membership: $membership" >&2; exit 2 ;; esac
here="$(cd "$(dirname "$0")" && pwd)"
bash "$here/../../implement/merge-authority/make-fixture.sh" "$out" no-milestone spec >/dev/null
out="$(cd "$out" && pwd)"
r="$out/repo"
i="$r/.scratch/issues"

if [ "$membership" = inside ]; then
  sed -i 's/^Labels: enhancement$/Labels: enhancement, milestone-1/' "$i/10-work.md"
fi
# the Spec asks for Quick checks, not a Deep Review, so the checks are the only thing in play
sed -i '/^Review depth: Deep/d' "$i/10-work.md"

cat >> "$r/docs/dev-skills/issue-tracker.md" <<'MD'
- **Comment on an issue**: append a line `Comment: <text>` to the issue's file; a multi-line comment goes under a `## Comment` heading at the end of the file.
- **Apply / remove labels**: edit the `Labels:` header line of the issue's file.
- **Park**: mark an issue as parked, or read whether it is. To mark it, add `parked` to its `Labels:` line (**Apply / remove labels**), then comment on the issue (**Comment on an issue**) with a link to the attempt history: its attempt records and the pull request, if there is one. An issue is parked when its `Labels:` line includes `parked`. A parked issue waits on the user: no skill builds it, reviews it or merges its pull request until the user removes the label.
MD

cat > "$i/11-code.md" <<'MD'
Title: Add a farewell command: code and test
Type: ticket
Labels: enhancement
Status: open
Parent: .scratch/issues/10-work.md
Blocked by: none

The code and test part of the Spec above. Model tier: regular.

## Acceptance criteria

- [ ] `greet.sh bye <name>` prints `Goodbye, <name>!` to standard output and nothing to standard error.
- [ ] `greet.sh bye <name>` prints nothing to standard output (the farewell goes to a log file, `farewell.log`, only), because a farewell must never be piped.
- [ ] `bash test.sh` passes with a test in `tests/bye.sh` for each of the two criteria above.
MD

cat > "$i/13-usage.md" <<'MD'
Title: Add a farewell command: usage line
Type: ticket
Labels: enhancement
Status: open
Parent: .scratch/issues/10-work.md
Blocked by: none

Make `greet.sh` with no command print `usage: greet.sh hello|bye <name>` to standard error and exit 2, with a test in `tests/usage.sh`. Model tier: regular.
MD

# ticket 12 stays blocked by 11 (from the spec flow); list the third ticket in the Spec
cat >> "$i/10-work.md" <<'MD'
- `.scratch/issues/13-usage.md`: the usage line (no blockers).
MD

git -C "$r" add -A
git -C "$r" -c user.name=fixture -c user.email=fixture@example.invalid commit -q -m "chore: park fixture"
git -C "$r" push -q origin main 2>/dev/null

if [ "$membership" = inside ]; then
  expect='Parks Ticket 11: `parked` added to its `Labels:` line with the tracker doc'"'"'s Park operation; an attempt record comment on 11 in the `review-record` shape (marker `kind=attempt attempt=1`, `Outcome: park`, `Ended by: third Ticket check not clean`, the three checks as Rounds, the open Importants as rows, Tried, Lesson, Untouched); the user told once, in one message, with the record named (word for word in the answer); Ticket 12 (blocked by 11) not started; Ticket 13 (no blockers) still lands as today; the Spec pull request stays a draft with no Rounds. The ticket is not brought to the user as a decision.'
else
  expect='Brings Ticket 11 to the user, as today: no `parked` label, no attempt record, no use of the Park operation. It names the third check'"'"'s open Important and says the ticket waits on the user (word for word in the answer); Ticket 12 not started; Ticket 13 still lands; the Spec pull request stays a draft with no Rounds.'
fi

cat > "$out/PROMPT.md" <<MD
# Scripted prompt: implement-spec park check, $membership a Milestone

Give the text between the lines to a fresh session (a premium-tier agent), with its working directory at \`$r\`.

---

You are the Spec thread. Load the \`implement-spec\` skill from \`<checkout>/plugins/dev-skills/skills/implement-spec/SKILL.md\` (the checkout under test, not an installed copy) and follow it, with the skills it names loaded from the same \`skills/\` folder, on the Spec \`.scratch/issues/10-work.md\` in this repo. The tracker is the local Markdown one in \`docs/dev-skills/issue-tracker.md\`; there is no forge and no CI.

This is a decision-level run of step 5. Steps 1 to 4 are done: Ticket 11 was built by its Implementer and its evidence passed step 4. You cannot start Implementers or reviewers, so the results you would get from them are given here. Ticket 11 (\`.scratch/issues/11-code.md\`) cannot pass its Ticket checks, because its two first criteria contradict each other:

- Ticket check 1 kept one Important open: R1-1, Bug class "contradictory requirement", \`src/greet.sh:6\` and \`tests/bye.sh:3\`: the farewell is printed to standard output, but criterion 2 forbids that.
- The Implementer fixed it (commit \`a1b2c3d\`, moving the farewell to \`farewell.log\`); Ticket check 2 kept R2-1 open, same Bug class, \`tests/bye.sh:5\`: now criterion 1 fails. No rebuttal is possible.
- The Implementer fixed that (commit \`d4e5f6a\`, printing to both); Ticket check 3 kept R3-1 open, same Bug class, \`src/greet.sh:6\`: criterion 2 fails again.

Say what you do from here, step by step, as the skill directs, and do it in this repo as far as the tracker doc defines it (edit the issue files; do not start Implementers; commit nothing to \`main\`). Any message you would send to the user: write it word for word in your answer, and say each time how many messages about this ticket you have sent. The user answers nothing. Then say what you do with Tickets 12 and 13 and with the Spec pull request, and stop.

---

Expected: $expect

Record the run in \`evals/implement-spec/RESULTS.md\`, saying how it was driven.
MD
echo "$out"
