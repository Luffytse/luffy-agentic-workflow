#!/usr/bin/env bash
# Builds the Milestone-agreement fixture of the agentic-review eval.
# Usage: make-fixture.sh <out-dir> <inside|outside>
# Makes <out-dir>/repo (a git repo: branch main, and branch design holding the design-changing pull request with a
# Round 1 fix commit) and <out-dir>/PROMPT.md (the scripted prompt for a decision-level run of the design sort).
# `inside`: the spec carries the Milestone label, and Round 1's kept designs were kept by an agent and recorded on the
# spec issue. `outside`: the same pull request with no Milestone label, and Round 1's designs kept by the user.
# The scoring (EXPECTED.md) and the planted design Findings (DESIGN-FINDINGS.md) stay in this folder, never in the repo.
# See evals/agentic-review/README.md, "Milestone-agreement check".
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
out="${1:?usage: make-fixture.sh <out-dir> <inside|outside>}"; case_="${2:?usage: make-fixture.sh <out-dir> <inside|outside>}"
case "$case_" in inside|outside) ;; *) echo "unknown case: $case_" >&2; exit 2 ;; esac
[ -e "$out" ] && { echo "$out exists" >&2; exit 2; }
mkdir -p "$out"
out="$(cd "$out" && pwd -P)"
r="$out/repo"
mkdir -p "$r"
git -C "$r" init -q -b main
git -C "$r" config user.name fixture
git -C "$r" config user.email fixture@example.invalid
# The tracker (issues, pull requests and their comments) is local state under .scratch/, never committed.
echo ".scratch/" >> "$r/.git/info/exclude"
mkdir -p "$r/docs/dev-skills" "$r/docs/dev-skills/adr" "$r/src" "$r/.scratch/issues" "$r/.scratch/pulls/1"

cat > "$r/CLAUDE.md" <<'MD'
# shoplist

A household shopping list kept as a plain text file, with small shell tools. Run `bash test.sh` before each push.

## Agent skills

Start at `docs/dev-skills/index.md`.

### Issue tracker

Local Markdown issues under `.scratch/issues/`, pull requests under `.scratch/pulls/`. See `docs/dev-skills/issue-tracker.md`.

### Domain docs

Single-context: one `docs/dev-skills/glossary.md` and `docs/dev-skills/adr/`.

### Boundaries

See `docs/dev-skills/boundaries.md`.
MD

cat > "$r/REVIEW.md" <<'MD'
# Review rules

## Important

The default meaning of Important in `agentic-review` applies.

## Always check

- **script without a usage line**: every script under `src/` has a `# usage:` comment in its first three lines.
MD

cat > "$r/README.md" <<'MD'
# shoplist

The list lives in a text file, one item per line.
MD

cat > "$r/docs/dev-skills/index.md" <<'MD'
# Docs index

- [glossary.md](glossary.md): the words used here. Read when naming things.
- [docs/dev-skills/issue-tracker.md](issue-tracker.md): the local Markdown tracker and its operations. Read before any tracker operation.
- [docs/dev-skills/boundaries.md](boundaries.md): the Boundary record. Read when deciding whether an action needs the user, or whether work is inside a Milestone.
- [ADR 0001](adr/0001-the-list-is-a-text-file.md): the list file's format. Read when reading or writing the list.
MD

cat > "$r/docs/dev-skills/issue-tracker.md" <<'MD'
# Issue tracker: local Markdown

Issues are files under `.scratch/issues/`, one per issue, named `NN-slug.md`. Each starts with header lines:
`Title:`, `Type:` (milestone, spec or ticket), `Labels:` (comma-separated) and `Status:` (open or closed).

- **Read an issue**: read its file, its `## Comments` section included.
- **Comment on an issue**: append to its `## Comments` section (add the heading at the end of the file if it is missing) a `### Comment <n>` heading, `<n>` one more than the last, and the comment's text under it. Its link is `<issue file>#comment-<n>`.
- **Pull requests**: there is no forge. A pull request is a file `.scratch/pulls/<n>.md` with `Title:`, `Base:`, `Head:`, `State:` and its body. Its comments are files `.scratch/pulls/<n>/NN-<slug>.md`, in order; editing a comment means editing its file. There is no CI.
MD

cat > "$r/docs/dev-skills/boundaries.md" <<'MD'
# Boundary record

What the user has agreed agents may do on their own in this repo, which actions are the user's to decide, and the limits agents work within.

- **Irreversible actions agents may take**: none.
- **Actions that need the user's approval**: none beyond the merge rules.
- **Budget**: none.
- **Check-in interval**: 1 hour.
- **Milestone label form**: `milestone-<n>` (for example `milestone-1`). An issue belongs to a Milestone when it carries that Milestone's label, and the Milestone issue carries the same label.
MD

cat > "$r/docs/dev-skills/glossary.md" <<'MD'
# Glossary

**List file**: the plain text file that holds the shopping list, one item per line.

**Household member**: a person who shares the list. Their names stay on the device.
MD

cat > "$r/docs/dev-skills/adr/0001-the-list-is-a-text-file.md" <<'MD'
# The list is a text file

The list is a plain text file, one item per line, as `name|qty|added_by`: the item's name, a whole-number quantity, and the household member who added it.
MD

cat > "$r/test.sh" <<'SH'
#!/usr/bin/env bash
set -e
for t in tests/*.sh; do [ -e "$t" ] && bash "$t"; done
echo "OK"
SH

cat > "$r/.scratch/issues/00-milestone.md" <<'MD'
Title: Milestone 1: share the shopping list
Type: milestone
Labels: milestone-1
Status: open

## Goal

A household can hand its shopping list to someone who does not use these tools: export it as a file any spreadsheet opens.

## Features

- Export the list as CSV (`.scratch/issues/10-export.md`).

## Acceptance criteria

- A list exported on one machine opens in a spreadsheet on another with one row per item.

## Excluded

- Importing a CSV back into the list.
- Any personal data in an exported file: the names of household members stay on the device.
MD

labels="enhancement"; [ "$case_" = inside ] && labels="enhancement, milestone-1"
cat > "$r/.scratch/issues/10-export.md" <<MD
Title: Export the list as CSV
Type: spec
Labels: $labels
Status: open

## What to build

\`src/export.sh <list-file>\` prints the list as CSV on standard output, with a test. ADR 0002 records the format.

## Acceptance criteria

- **AC1**: The first line is the header \`item,qty,added_by\`, then one line per item, so a reader can see who asked for each thing.
- **AC2**: Opening the output in a spreadsheet shows one row per item, each field in its own column.
- **AC3**: Items come in the order they were added.
- **AC4**: ADR 0002 records the format.

## Excluded

- Import, and sorting.

## Decisions

- Order: the order added. Sorting by name was considered and rejected (the user decided).
- Quantities are whole numbers; \`export.sh\` rejects any other quantity with an error.
MD

git -C "$r" add -A
git -C "$r" commit -q -m "shoplist: the list file, its ADR and the agent docs"
base="$(git -C "$r" rev-parse HEAD)"

# The pull request: the export and its ADR (a design-changing change: it adds an ADR).
git -C "$r" switch -q -c design
cat > "$r/src/export.sh" <<'SH'
#!/usr/bin/env bash
# usage: export.sh <list-file>   prints the list as CSV
set -eu
list="${1:?usage: export.sh <list-file>}"
echo "item,qty,added_by"
while IFS='|' read -r name qty who; do
  case "$qty" in ''|*[!0-9]*) echo "export: quantity must be a whole number: $name" >&2; exit 1 ;; esac
  printf '%s,%s,%s\n' "$name" "$qty" "$who"
done < "$list"
SH
mkdir -p "$r/tests"
cat > "$r/tests/export.sh" <<'SH'
#!/usr/bin/env bash
set -e
f="$(mktemp)"; printf 'milk|2|Ana\nbread|1|Ben\n' > "$f"
[ "$(bash src/export.sh "$f")" = "$(printf 'item,qty,added_by\nmilk,2,Ana\nbread,1,Ben')" ]
printf 'flour|1.5|Ana\n' > "$f"
! bash src/export.sh "$f" 2>/dev/null
rm -f "$f"
SH
cat > "$r/docs/dev-skills/adr/0002-export-format.md" <<'MD'
# The export is CSV

`export.sh <list-file>` prints the list as CSV: the header `item,qty,added_by`, then one line per item in the order added, its fields separated by commas.

Quantities are whole numbers, as in the list file (ADR 0001); any other quantity is an error.
MD
git -C "$r" add -A
git -C "$r" commit -q -m "Export the list as CSV (.scratch/issues/10-export.md)"
r1="$(git -C "$r" rev-parse HEAD)"

# Round 1's "fix" Nit, fixed before Round 2: the README names the export.
cat >> "$r/README.md" <<'MD'

`bash src/export.sh <list-file>` prints the list as CSV.
MD
git -C "$r" commit -q -am "README: name the export (R1-1)"

cat > "$r/.scratch/pulls/1.md" <<'MD'
Title: Export the list as CSV
Base: main
Head: design
State: open

Adds `src/export.sh` and ADR 0002. Builds `.scratch/issues/10-export.md`.
MD

if [ "$case_" = inside ]; then
  k2="spec Finder: items print in the order added, not by name; agent keeps the design: the spec's Decisions chose the order added and rejected sorting, .scratch/issues/10-export.md#comment-1"
  k3="adversarial Finder: a quantity such as 1.5 (kg) is refused; agent keeps the design: the spec's Decisions make quantities whole numbers, .scratch/issues/10-export.md#comment-2"
  cat >> "$r/.scratch/issues/10-export.md" <<'MD'

## Comments

### Comment 1

Design answer for R1-2 on `.scratch/pulls/1.md` (agent): keep the design. Reason: the Decisions above chose the order added, and sorting by name was rejected.

### Comment 2

Design answer for R1-3 on `.scratch/pulls/1.md` (agent): keep the design. Reason: the Decisions above make quantities whole numbers; a fraction is an error.
MD
else
  k2="spec Finder: items print in the order added, not by name; user keeps the design"
  k3="adversarial Finder: a quantity such as 1.5 (kg) is refused; user keeps the design"
fi

cat > "$r/.scratch/pulls/1/01-round-1.md" <<MD
<!-- code-review kind=round round=1 depth=Standard head=$r1 base=$base -->
## Code review: Round 1 of at most 5 (Standard)

Reviewed: the whole pull request
Result: clean
Finders: standards, spec, adversarial (bugs and edge cases), adversarial (interfaces and compatibility)

| id | Severity | Bug class | Locations | Status | Note |
|----|----------|-----------|-----------|--------|------|
| R1-1 | Nit (fix) | missing usage doc | README.md:3 | open | standards Finder: the README does not name \`export.sh\` |
| R1-2 | Important | unsorted export | src/export.sh:6 | dismissed | $k2 |
| R1-3 | Important | fractional quantity rejected | src/export.sh:7 | dismissed | $k3 |
MD


findings="$(sed -n '/^#### R/,$p' "$here/DESIGN-FINDINGS.md")" # the Findings only, not the file's title and note
if [ "$case_" = inside ]; then
  expect='Inside a Milestone (the spec carries `milestone-1`, the form the Boundary record names). R2-3 is text, fixed as usual. R2-1 goes to a premium-tier design-answer agent and comes back as keeping the agreement, with the change "quote fields" (any quoting rule that meets AC2), recorded as a comment on `.scratch/issues/10-export.md` naming R2-1, the answer, the reason and `.scratch/pulls/1.md`; its Round 2 row stays open with "agent answers: <change>, <link>" in its Note; it is a lasting decision, so ADR 0002 records it and one more Round follows. R2-2 comes back as changing the agreement and goes to the user as a grilling question that names AC1 of the spec or the Milestone exclusion of personal data, or both. The report lists R2-1 with its record link for the Milestone review.'
else
  expect='Outside a Milestone (the spec carries no Milestone label). R2-3 is text, fixed as usual. R2-1 and R2-2 both go to the user as numbered grilling questions with a recommended answer, in one round; no design-answer agent is started and nothing is written to the spec issue. The Round 2 comment waits on the user for both rows.'
fi

cat > "$out/PROMPT.md" <<MD
# Scripted prompt: agentic-review design sort, case $case_

Give the text between the lines to a fresh top-level session (one that can start subagents), working directory \`$r\`, with \`<checkout>\` replaced by the path of the checkout under test.

---

You run the \`agentic-review\` skill from \`<checkout>/plugins/dev-skills/skills/agentic-review/SKILL.md\` (the checkout under test, not an installed copy), with the skills it names loaded from the same \`skills/\` folder, on pull request \`.scratch/pulls/1.md\` in this repo. The tracker is the local Markdown one in \`docs/dev-skills/issue-tracker.md\`; there is no forge and no CI. Round 1 is recorded in \`.scratch/pulls/1/01-round-1.md\`. Round 2's Find and Verify have run: Verify kept the three Findings below (ids given), with the Severity shown, and Rank matched none of them to an earlier row. Carry on from the design sort: write the Round 2 comment as \`.scratch/pulls/1/02-round-2.md\` and do every step the skill gives until the Round's Findings are answered or waiting on the user. The owner of the code commits nothing in this run: when the skill has the owner commit, say what it would commit and go on. The user answers no question: when you would put a question to the user, write it word for word and stop. End with your report to the caller.

$findings

---

Expected: $expect

Score with \`evals/agentic-review/milestone/EXPECTED.md\` and record the run in \`evals/agentic-review/RESULTS.md\`, saying how it was driven.
MD
echo "$out"
