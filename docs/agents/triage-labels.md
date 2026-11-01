# Triage Labels

The skills speak in terms of 5 state roles + 2 category roles, plus one optional agent-only role. This file maps those roles to the actual label strings used in this repo's issue tracker.

| Role in `dev-skills` | Label in our tracker | Meaning                                  |
| -------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`       | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`         | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`    | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`    | `ready-for-human`    | Requires human implementation            |
| `wontfix`            | `wontfix`            | Will not be actioned                     |
| `bug`                | `bug`                | Something is broken                      |
| `enhancement`        | `enhancement`        | New feature or improvement               |

The agent-only role is optional and is neither a state nor a category role: an issue carries at most one agent label besides its one category and one state, and most carry none. It marks an issue for one coding agent only, and this repo has one label per agent:

| Role in `dev-skills` | Label in our tracker | Meaning                                       |
| -------------------- | -------------------- | --------------------------------------------- |
| `agent-only`         | `claude-only`        | Only Claude Code works this issue             |
| `agent-only`         | `codex-only`         | Only Codex works this issue                   |

An agent that sees another agent's label does not work the issue. An issue with no agent label can be taken by any agent.

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

## Other labels

`retro` and `retro-planning` are not triage roles. A `retro` issue carries no `needs-triage` and is left out of triage; see [ADR 0007](../adr/0007-retro-issues-pile-up-per-repo-and-are-planned-in-batches.md). The `wayfinder:*` labels mark a wayfinder map and its tickets; see `issue-tracker.md`. The `release-m<milestone>-r<n>` labels (`release-X.Y.Z` up to 0.25.0) mark the issues of one Release; see `release.md`.
