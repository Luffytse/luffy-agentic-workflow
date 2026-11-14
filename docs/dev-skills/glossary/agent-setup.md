# Agent setup

The labels and records a repo keeps so the skills can work in it, and the Door call they read. Each entry says what a word means; the rule's steps stay with the skill or doc it names.

## Language

**Agent label**:
The label of the optional agent-only triage role, marking an issue for one coding agent only; a repo maps the role to one label per agent in `docs/dev-skills/triage-labels.md` (this repo: `claude-only` and `codex-only`). It is neither a category nor a state role: an agent that sees another agent's label does not work the issue, and an issue with none can be taken by any agent. `triage` and `to-tickets` own when it is set.
_Avoid_: assignee, owner

**Repo label**:
A label the repo records in the **Repo labels** table of its `docs/dev-skills/triage-labels.md`, with a one-line "when it applies" (this repo's table is empty). It is neither a triage role nor an Agent label; builders read none and it routes no work. `triage` owns the rule that applies it, which `to-spec`, `to-tickets` and `review-rounds` follow; `setup-dev-skills` records the table.
_Avoid_: custom role

**`next-release`**:
The triage label doc's role marking an issue that must join the next Release. `triage` and `retro-planning` set it; `release` ranks marked issues first and clears the mark from each it takes, so no skill parses another skill's records for this (ADR 0012).

**Boundary record**:
A repo's `docs/dev-skills/boundaries.md`, written with the user by `setup-dev-skills`: which irreversible actions agents may take, which actions need the user's approval, the resource budget, the check-in interval and the form of a Milestone's membership label, plus any limits of the repo's own. It is the only record of boundaries (a Milestone issue holds none), and `merging` reads it, as an empty one when there is none, to decide whether a pull request goes to the user (ADR 0004).
_Avoid_: permissions file, policy

**Door**:
How hard a change is to walk back. A **one-way door** is a change that reverting its commits would not fully undo, anything outside git included; a **two-way door** is one a revert does undo. The `pr` skill owns the test and records the call as `**Door:**`; whether a one-way door is an agent merge is the Boundary record's alone, applied by `merging` (ADR 0004; this repo's version bump: ADR 0016).
_Avoid_: risk level
