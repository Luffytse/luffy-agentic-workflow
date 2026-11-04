# Boundary record

What the user has agreed agents may do on their own in this repo, which actions are the user's to decide, and the limits agents work within. The `merging` skill, which `implement`, `implement-spec` and `release` load at their merge step, reads this record for every pull request, inside a Milestone or not, instead of a fixed list: the thread merges its pull request unless it crosses a boundary here or the repo's own rules say a person merges it ([ADR 0004](adr/0004-build-threads-coordinate-and-subagents-code.md), "When the user must review"). A merged version bump is not a published release and is no one-way door here (glossary **Door**). The decision is on [#385](https://github.com/Luffytse/luffy-dev-skills/issues/385#issuecomment-6564185667) and in Milestone 1 ([#396](https://github.com/Luffytse/luffy-dev-skills/issues/396), "Boundaries").

- **Irreversible actions agents may take**: any. Nothing here touches user or customer data.
- **Actions that need the user's approval**: none.
- **Budget**: none (no paid or limited resource is used).
- **Check-in interval**: 1 hour.
- **Skill file size**: a change that pushes any skill file (a `SKILL.md` or a reference file under a skill) past 5,000 words brings the user into planning, to decide on a split or a redesign. It is enforced by the `skill-file-size` check in `scripts/check-plugin.sh`, which CI runs on the pull request; a Round does not weigh it, and the pull request does not merge until the user has decided.
- **Milestone label form**: `milestone-<n>` (for example `milestone-1`). An issue belongs to a Milestone when it carries that Milestone's label, and the Milestone issue carries the same label.

## Milestone issues

A Milestone issue holds no boundaries of its own: this record applies to every issue, inside a Milestone or not (Spec #633). To allow or reserve an action for a Milestone, change this record. The `## Boundaries` section of an earlier Milestone issue, such as Milestone 1's, is history.
