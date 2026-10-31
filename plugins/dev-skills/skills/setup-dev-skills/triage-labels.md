# Triage Labels

The skills speak in terms of 5 state roles + 2 category roles. This file maps those roles to the actual label strings used in this repo's issue tracker.

| Role in `dev-skills` | Label in our tracker | Meaning                                  |
| -------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`       | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`         | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`    | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`    | `ready-for-human`    | Requires human implementation            |
| `wontfix`            | `wontfix`            | Will not be actioned                     |
| `bug`                | `bug`                | Something is broken                      |
| `enhancement`        | `enhancement`        | New feature or improvement               |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

## Other labels

`retro` and `retro-planning` are not triage roles. A `retro` issue carries no `needs-triage` and is left out of triage. The `wayfinder:*` labels mark a wayfinder map and its tickets; see `issue-tracker.md`. In a repo that cuts Releases, the release labels (the label prefix in `release.md` plus a version) mark the issues of one Release; see `release.md`.
