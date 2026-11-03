# dev-skills is one plugin, started from Matt Pocock's skills

Our development skills ship as one plugin, `dev-skills`, in this repo's `luffy-dev` marketplace. It began as a copy of Matt Pocock's skills (`mattpocock/skills`), not his own plugin installed as-is, and the skills are ours now (see the last Consequence). We copied because the user mostly works through Claude project threads, where a coordinator starts each thread and nobody types slash commands, and 16 of Upstream's 27 skills set `disable-model-invocation: true`, so a thread could never start them. In our copy every skill is model-invoked, at the cost of one description line per skill in each session.

## Considered options

- **Install Upstream's `mattpocock-skills` plugin unchanged.** It updates itself, but threads cannot start `wayfinder`, `to-spec`, `to-tickets`, `implement` and the other user-only skills, and we could not keep local edits such as at most 3 questions each time `grilling` asks.
- **Keep skills in each repo's `.claude/skills/`.** Project threads do not load a repo's skills, agents or `.claude/settings.json` plugins at all; only plugins added in Project settings, or skills on the claude.ai account, reach them.
- **Several plugins (Upstream fork, review, workflow).** Upstream already has a `code-review` skill, so a separate review plugin would put two competing review skills in front of the agent. Our review changes go into our `agentic-review` instead.

## Consequences

- The plugin holds only development skills: from `wayfinder` through implementation to `agentic-review` and `retro`. It keeps 22 of Upstream's skills: `ask-matt`, `wayfinder`, `grill-with-docs`, `grilling`, `domain-modeling`, `research`, `prototype`, `handoff`, `to-spec`, `to-tickets`, `implement`, `implement-spec`, `tdd`, `agentic-review`, `pr`, `retro`, `diagnosing-bugs`, `triage`, `improve-codebase-architecture`, `codebase-design`, `wizard` and `writing-for-agents`. We dropped Upstream's `teach`, `to-questionnaire`, `grill-me` (`grill-with-docs` covers it) and `wait-what`, and trimmed `ask-matt` so it no longer names them. `setup-dev-skills` is our own skill, derived from Upstream's setup skill and kept in `skills/`, not one of the 22. Non-development skills can later be separate plugins in the same marketplace.
- All skills sit in one folder inside the plugin, `skills/`. (Until the Spec "plugin versions change only at a Release" (#257) they sat in two, `upstream-skills/` for the copied ones, so it was clear which text came from Upstream.)
- This repo is private and separate from luffydev, so the Hub, Wiki and Trip planning repos can use the same plugin.
- The skills are ours, not a fork merged by hand. Changed by #257: `PATCHES.md` is gone and Upstream updates are no longer merged. The README records the last Upstream commit we looked at; the 2-week Upstream watch reads Upstream's new commits and takes an idea one at a time through triage, like any other issue.
- The marketplace stays named `luffy-dev` so the existing `dai-portal-data` install keeps working.
- Upstream is MIT licensed; we keep its licence file, `LICENSE-mattpocock-skills`, and credit Matt Pocock in the README.
