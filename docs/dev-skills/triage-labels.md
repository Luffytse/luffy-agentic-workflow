# Triage Labels

The skills speak in terms of 5 state roles + 2 category roles, plus the `next-release` role. This file maps those roles to the actual label strings used in this repo's issue tracker.

| Role in `dev-skills` | Label in our tracker | Meaning                                  |
| -------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`       | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`         | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`    | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`    | `ready-for-human`    | Requires human implementation            |
| `wontfix`            | `wontfix`            | Will not be actioned                     |
| `bug`                | `bug`                | Something is broken                      |
| `enhancement`        | `enhancement`        | New feature or improvement               |

The `next-release` role is neither a state nor a category role. It marks an issue that must join the next Release. `triage` sets it on a severe issue or one that blocks a planned feature, and `retro-planning` on the Ticket of a group that joins; `release` takes marked issues into the next Release and removes the mark once they carry the release label.

| Role in `dev-skills` | Label in our tracker | Meaning                                       |
| -------------------- | -------------------- | --------------------------------------------- |
| `next-release`       | `next-release`       | Must join the next Release                    |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

## Repo labels

Labels this repo records for its own kinds of work, each with one line saying when it applies. They are not triage roles. `triage`, `to-spec`, `to-tickets` and `review-rounds` apply them, by the rule `triage` holds: a label whose line fits the issue, and any label the user names; builders read none. An empty table means the repo has none.

| Label in our tracker | When it applies |
| -------------------- | --------------- |

## Other labels

`retro` and `retro-planning` are not triage roles. A `retro` issue carries no `needs-triage` and is left out of triage; see [ADR 0007](adr/0007-retro-issues-pile-up-per-repo-and-are-planned-in-batches.md). The `wayfinder:*` labels mark a wayfinder map and its tickets; see `issue-tracker.md`. `parked` marks an issue that, inside a Milestone, had a stalled thread that could not be taken over safely or a feature that stalled twice, or that the user parked, and now waits on the user; it is the tracker doc's **Park** operation's label, set and read there. The `release-m<milestone>-r<n>` labels (`release-X.Y.Z` up to 0.25.0) mark the issues of one Release; see `release.md`.
