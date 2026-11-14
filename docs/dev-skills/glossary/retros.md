# Retros

The words of filing Retro issues and working through them. Each entry says what a word means; the rule's steps stay with the skill or doc it names.

## Language

**Retro issue**:
One suggestion from `retro`, filed as a GitHub issue labelled `retro` in the repo its **Scope** sends it to: `skill` (what the plugin ships) and `environment` (a limit of the coding agent or Harness) go where the plugin's Retros go, `this repo` to that repo's own tracker. A repeated Bug class is filed the same way, proposing the check or the `REVIEW.md` line: a retro only files and builds nothing. It carries no state role until **Retro planning** hands it to triage with `needs-triage`. A closed one is reopened when seen again. Owned by `retro` (ADR 0007).
_Avoid_: retro ticket, action item

**Retro backlog**:
The open Retro issues of one repo that **Retro planning** still sorts: those with no state role that no open Ticket absorbs.
_Avoid_: retro queue, improvement list

**Retro planning**:
The unattended sort of one repo's Retro backlog by `retro-planning`, run by the Release thread at each Release end before the **Triage batch**, and the same way when anyone asks for one. It groups the issues by Scope and root cause, merges duplicates, closes a group seen in one thread and not severe (a new sighting reopens it), and hands a group seen in two or more threads, a severe one, or one reopened after its fix merged to triage. It asks nobody, files no Ticket and sets no `next-release`. Its record issue, labelled `retro-planning`, is closed at the run's end and linked from the release issue (ADR 0007).
_Avoid_: retro triage, retro review

**Handed-over Retro issue**:
A Retro issue that **Retro planning** gave the `needs-triage` role, keeping its `retro` label. The Triage batch triages it as the Ticket itself, by `triage`'s rule for it, and `release` ranks it once it reaches `ready-for-agent`. A repo's own rules may add to that rule, as this repo's `CLAUDE.md` does for a fix in a skill.
