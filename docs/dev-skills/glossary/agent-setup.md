# Agent setup

The labels and records a repo keeps so the skills can work in it, and the Door call they read. Each entry says what a word means; the rule's steps stay with the skill or doc it names.

## Language

**Repo label**:
A label the repo records in the **Repo labels** table of its `docs/dev-skills/triage-labels.md`, with a one-line "when it applies" (this repo's table is empty). It is not a triage role; builders read none and it routes no work. The doc's **Repo labels** section holds the rule that applies it, which `triage`, `to-spec`, `to-tickets` and `review-rounds` follow; `setup-dev-skills` records the table.
_Avoid_: custom role

**`next-release`**:
The triage label doc's role marking an issue that the next Release planning takes first among the waiting issues, after severe ones and while the size has room. `triage` alone sets it; `release` takes marked issues (a severe one past the size) and clears the mark from each it takes, so no skill parses another skill's records for this (ADR 0012).

**Boundary record**:
A repo's `docs/dev-skills/boundaries.md`, written with the user by `setup-dev-skills`: which irreversible actions agents may take, which actions need the user's approval and the resource budget (the three the user is asked), the check-in interval and the form of a Milestone's membership label (written as defaults, the user edits the file), plus any limits of the repo's own. It is the only record of boundaries (a Milestone issue holds none), and `merging` reads it, as an empty one when there is none, to decide whether a pull request goes to the user (ADR 0004).
_Avoid_: permissions file, policy

**Door**:
How hard a change is to walk back. A **one-way door** is a change that reverting its commits would not fully undo, anything outside git included; a **two-way door** is one a revert does undo. The `pr` skill records the call as `**Door:**`; whether a one-way door is an agent merge is the Boundary record's alone, applied by `merging` (ADR 0004).
_Avoid_: risk level
