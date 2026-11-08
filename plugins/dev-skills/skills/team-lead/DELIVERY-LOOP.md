# Delivery loop

The delivery loop for a coordinator that cannot load this plugin's skills. This file owns its text: `setup-project` copies "The loop" below into such a coordinator's project instructions, and no other skill restates it. A coordinator that can load `team-lead` follows `team-lead` and does not need it.

A coordinator without the skills cannot run `team-lead`, `release` or `milestone` itself, so the loop has it start a thread for each step that needs one. That thread loads the skill, does the step and reports.

## The loop

You cannot load the plugin's skills. Start a thread for each step below that names a skill, briefed with the skill, the issue links and its Model tier, and never do that step yourself. At every wake (a worker's report or end, a check-in, the user writing), read the tracker and each worker's state from the tool that runs your workers, then take every step that applies, in order:

1. Once Milestone planning has settled, start a thread that runs `milestone`'s Startup verification, with `worker-control`'s check run by the agent the skill names. Start no Build thread until its result on the Milestone issue reads `Verdict: ready`, or the user says to go on.
2. With no current Release (an open release issue naming this Milestone, whose label an issue carries) and no Release thread running, start a Release thread that runs `release` to plan one.
3. Start Build threads only for issues carrying the current Release's label, in the release issue's Order, up to the project's thread limit and the Milestone's order rule, and start none while a Release thread runs.
4. When every issue carrying the current Release's label is closed, start a Release thread that runs `release` to cut it, run `triage` and `retro-planning`, and plan the next Release.
5. When every feature is merged or parked, start a thread that runs `milestone` to write its report, then stop for the user's Milestone review.
