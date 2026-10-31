# Changelog

What each version of `dev-skills` brought, newest first. A version changes only when a Release is cut, and each Release adds one entry here: its goal, the issues it shipped, and what a project using the plugin must do when something breaks.

## 0.22.28 and earlier

Before Releases, every merged change to the plugin bumped its version, so the versions up to 0.22.28 have no entries of their own; the repo's git history records each change and its bump. The versions that brought something new:

- **0.2.0**: skills find docs through one docs index, `docs/index.md`. The plugin started as a fork of Matt Pocock's skills, every one model-invoked.
- **0.4.0**: the review skill runs Find, Verify and Rank in Rounds.
- **0.5.0**: `retro` turns repeated Bug classes into checks.
- **0.6.0**: `to-tickets` gives each Ticket a Model tier, and `setup-project` is offered after tickets or a wayfinding map.
- **0.7.0**: `implement` coordinates one lone Ticket.
- **0.8.0**: `implement-spec` coordinates one Spec.
- **0.9.0**: the review skill is renamed `agentic-review`. A project that named `code-review` must use the new name.
- **0.9.3**: `retro` files its suggestions as Retro issues, and `retro-planning` works through them.
- **0.10.0**: `agentic-review` takes the built-in review's strengths.
- **0.12.0**: the formerly user-only skills get model-facing descriptions.
- **0.13.0**: the setup skill becomes `setup-dev-skills`. A project that called it by its old name must use the new one.
- **0.14.0**: `retro-planning` walks one group at a time.
- **0.15.0**: `grilling` asks at most 3 questions per round.
- **0.17.0**: `agentic-review` counts its reports before moving on.
- **0.19.0**: review subagents experiment only in their own copy, and Implementers confirm each push.
- **0.20.0**: `handoff` saves where the next agent can read it.
- **0.21.0**: `grilling` states a rule's purpose and checks a recommendation's facts.
- **0.22.0**: `agentic-review` returns design Findings to the user as grilling.
- **0.22.1 to 0.22.28**: fixes and clarifications, among them `setup-dev-skills` writing a starter `REVIEW.md` (0.22.11) and the tracker doc's REST routes and fallback forms for blocking and sub-issues (0.22.14 to 0.22.27), and `agentic-review` Rank edge cases (matching per location at one head, raising held Findings, partly fixed rows, Verifier dismissals closing earlier Findings; 0.22.28).
