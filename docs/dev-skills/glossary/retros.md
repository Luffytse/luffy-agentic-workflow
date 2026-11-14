# Retros

The words of filing Retro issues and working through them. Each entry says what a word means; the rule's steps stay with the skill or doc it names.

## Language

**Retro issue**:
One suggestion from `retro`, filed as a GitHub issue labelled `retro` in the repo its **Scope** sends it to: `skill` (what the plugin ships) and `environment` (a limit of the coding agent or Harness) go where the plugin's Retros go, `this repo` to that repo's own tracker. A repeated Bug class is filed the same way, proposing the check or the `REVIEW.md` line: a retro only files and builds nothing. It is never `needs-triage`; **Retro planning** decides what happens to it. A closed one is reopened when seen again. Owned by `retro` (ADR 0007).
_Avoid_: retro ticket, action item

**Retro backlog**:
The open Retro issues of one repo.
_Avoid_: retro queue, improvement list

**Retro planning**:
The review of a snapshot of one repo's Retro backlog by `retro-planning`, which merges duplicates, closes most one-offs and files at most 3 Tickets (the cap), walking the user through one group at a time (at a Release end, see **Release-end Retro planning**). Its record issue, labelled `retro-planning`, is open while it runs and closed at its end.
_Avoid_: retro triage, retro review

**Necessity check**:
The check a fresh premium-tier subagent makes in a Retro planning before a one-thread group whose fix is a cheap deterministic check (a CI step, a checker rule, a test) is acted on: that the check would have failed on the real past mistake and that nothing already catches it. Owned by `retro-planning`.

**Release-end Retro planning**:
The Retro planning that the caller runs at the end of a Release, with the Triage batch: agents decide every group without asking the user per group, with no 3-Ticket cap, and record each call and reason in the planning record for the Milestone review. Which fixes join the next Release, and what goes to the user, are `retro-planning`'s.

**Spin-off**:
A group of Retro issues the user wants to discuss further, moved out of a Retro planning into a planning thread of its own, which ends by giving each issue a Ticket or a close. It does not count toward the cap and cannot expire meanwhile.
_Avoid_: deferral, parked group
