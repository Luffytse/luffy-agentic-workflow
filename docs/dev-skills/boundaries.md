# Boundary record

What the user has agreed agents may do on their own in this repo, which actions are the user's to decide, and the limits agents work within. Inside a Milestone, the merge step of `implement` and `implement-spec` reads this record instead of a fixed list: a pull request whose issue (or a no-issue corrective check's recorded `Retro origin`) carries a Milestone label is merged by its thread unless it crosses a boundary here or in the Milestone issue, or the repo's own rules say a person merges it ([ADR 0004](adr/0004-build-threads-coordinate-and-subagents-code.md), "When the user must review"). Outside a Milestone, the skills' outside-a-Milestone merge list governs, and a one-way-door pull request is not self-merged. A merged version bump is not a published release and is no one-way door here (glossary **Door**). The decision is on [#385](https://github.com/Luffytse/luffy-dev-skills/issues/385#issuecomment-6564185667) and in Milestone 1 ([#396](https://github.com/Luffytse/luffy-dev-skills/issues/396), "Boundaries").

- **Irreversible actions agents may take**: any. Nothing here touches user or customer data.
- **Actions that need the user's approval**: none.
- **Budget**: none (no paid or limited resource is used).
- **Check-in interval**: 1 hour.
- **Milestone label form**: `milestone-<n>` (for example `milestone-1`). An issue belongs to a Milestone when it carries that Milestone's label, and the Milestone issue carries the same label.

## Milestone issues

A Milestone issue may name extra allowed or forbidden actions for its own issues. For an issue that belongs to the Milestone, the Milestone issue wins over this record; for every other issue, this record applies as written.
