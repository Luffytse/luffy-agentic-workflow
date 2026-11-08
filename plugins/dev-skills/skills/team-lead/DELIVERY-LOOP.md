# Delivery loop

The delivery loop for a coordinator that cannot load this plugin's skills. This file owns its text: `setup-project` copies "The loop" below into such a coordinator's project instructions, and no other skill restates it. A coordinator that can load `team-lead` follows `team-lead` and does not need it.

A coordinator without the skills cannot run `team-lead`, `release` or `milestone` itself, so the loop has it start a thread for each step that needs one. That thread loads the skill, does the step and reports.

## The loop

You cannot load the plugin's skills. Start a thread for each step below that names a skill, and never do that step yourself. A brief carries the skill, the issue link, the Milestone issue link and the Model tier (regular when the issue names none), and you start the thread on the model the project's instructions map to that tier, or the worker tool's default model when they give none. At every wake (a worker's report or end, a check-in, the user writing), read the tracker and each worker's state from the tool that runs your workers, then take every step that applies, in order. Start none whose thread is already running or whose result already stands:

1. Once Milestone planning has settled, and no Startup verification thread is running or Verdict recorded on the Milestone issue, start a thread that runs `milestone`'s Startup verification, with `worker-control`'s check run by the agent the skill names. Start no Build thread until the result on the Milestone issue reads `Verdict: ready`, or the user says to go on.
2. With no current Release (an open release issue naming this Milestone, whose label an issue carries), no Release thread running, and at least one planned feature that is open, not parked, carries no release label and is unblocked, start a Release thread that runs `release` to plan one.
3. Start Build threads only for issues carrying the current Release's label, in the release issue's Order, up to the project's thread limit and the Milestone's order rule, and start none while a Release thread runs. A Spec with Tickets runs `implement-spec`, a Spec without Tickets runs `to-tickets` first, and a lone Ticket runs `implement`.
4. When every issue carrying the current Release's label is closed and no Release thread is running, start a Release thread that runs `release` to cut it, run `triage` and `retro-planning`, and plan the next Release.
5. When every feature is merged or parked and no report thread is running or report written, start a thread that runs `milestone` to write its report, then stop for the user's Milestone review.
