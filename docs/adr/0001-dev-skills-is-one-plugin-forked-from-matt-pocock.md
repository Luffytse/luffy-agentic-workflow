# dev-skills is one plugin, forked from Matt Pocock's skills

Our development skills ship as one plugin, `dev-skills`, in this repo's `luffy-dev` marketplace. It is a fork of Matt Pocock's skills (`mattpocock/skills`), not his own plugin installed as-is, plus skills of our own. We forked because Lufei mostly works through Claude project threads, where a coordinator starts each thread and nobody types slash commands, and 16 of Upstream's 27 skills set `disable-model-invocation: true`, so a thread could never start them. In the fork every skill is model-invoked, at the cost of one description line per skill in each session.

## Considered options

- **Install Upstream's `mattpocock-skills` plugin unchanged.** It updates itself, but threads cannot start `wayfinder`, `to-spec`, `to-tickets`, `implement` and the other user-only skills, and we could not keep local edits such as at most 3 questions each time `grilling` asks.
- **Keep skills in each repo's `.claude/skills/`.** Project threads do not load a repo's skills, agents or `.claude/settings.json` plugins at all; only plugins added in Project settings, or skills on the claude.ai account, reach them.
- **Several plugins (Upstream fork, review, workflow).** Upstream already has a `code-review` skill, so a separate review plugin would put two competing review skills in front of the agent. Our review changes go into the forked `code-review` instead.

## Consequences

- The plugin holds only development skills: from `wayfinder` through implementation to `code-review` and `retro`. It keeps 23 of Upstream's skills: `ask-matt`, `wayfinder`, `grill-with-docs`, `grilling`, `domain-modeling`, `research`, `prototype`, `handoff`, `to-spec`, `to-tickets`, `implement`, `implement-spec`, `tdd`, `code-review`, `pr`, `retro`, `diagnosing-bugs`, `triage`, `improve-codebase-architecture`, `codebase-design`, `setup-matt-pocock-skills`, `wizard` and `writing-for-agents`. We dropped Upstream's `teach`, `to-questionnaire`, `grill-me` (`grill-with-docs` covers it) and `wait-what`, and trimmed `ask-matt` so it no longer names them. Non-development skills can later be separate plugins in the same marketplace.
- Forked skills and our own new skills sit in separate folders inside the plugin, so it is always clear which text came from Upstream.
- This repo is private and separate from luffydev, so the Hub, Wiki and Trip planning repos can use the same plugin.
- Upstream updates are merged by hand. `plugins/dev-skills/PATCHES.md` lists every change we made to Upstream text, so a merge knows what to keep.
- The marketplace stays named `luffy-dev` so the existing `dai-portal-data` install keeps working.
- Upstream is MIT licensed; the fork keeps its licence file.
