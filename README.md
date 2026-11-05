# luffy-agentic-workflow

Plugin marketplace for Claude Code and Codex, holding one plugin: `dev-skills`, our agentic development workflow (the skill set from specs and tickets to review and release).

## Plugins

| Plugin | Description |
|--------|-------------|
| [`dev-skills`](plugins/dev-skills/) | Development skills: model-invocable skills that began as Matt Pocock's and are now our own (wayfinder, grilling, specs, tickets, TDD, code review) |

## Install

### Claude Code

From inside Claude Code:

```
/plugin marketplace add https://github.com/Luffytse/luffy-agentic-workflow
/plugin install dev-skills@luffy-agentic-workflow
```

Or from the shell:

```bash
claude plugin marketplace add https://github.com/Luffytse/luffy-agentic-workflow
claude plugin install dev-skills@luffy-agentic-workflow
```

After install, the plugin's skills are namespaced, for example `dev-skills:wayfinder`.

### Codex

From the shell (verified with Codex CLI `0.166.0-alpha.5.1`):

```bash
codex plugin marketplace add https://github.com/Luffytse/luffy-agentic-workflow
codex plugin add dev-skills@luffy-agentic-workflow
codex plugin list --marketplace luffy-agentic-workflow --json
```

The list should show `dev-skills` installed and enabled. Start a new Codex session to load the skills. See the [model-tiers skill](plugins/dev-skills/skills/model-tiers/SKILL.md) for the tier-to-model map used for model selection.

## Update

### Claude Code

```bash
# In Claude Code
/plugin marketplace update luffy-agentic-workflow

# Or from the shell
claude plugin marketplace update luffy-agentic-workflow
```

### Codex

For a marketplace installed from GitHub, refresh its checkout and reinstall the current plugin contents:

```bash
codex plugin marketplace upgrade luffy-agentic-workflow
codex plugin add dev-skills@luffy-agentic-workflow
```

Start a new Codex session after updating (restart the desktop app if using it).

## Contributing / local development

### Claude Code

**In this repo:** we develop the skills here, so Claude Code reads them directly
from the checkout. Edits are available without reinstalling the plugin.

- `.claude/skills` links to `plugins/dev-skills/skills` for local skill discovery.
- `.claude/settings.json` disables the cached plugin in this repo to avoid loading duplicate skills.

**Across repos:** point the marketplace at your local clone instead of GitHub:

```bash
claude plugin marketplace add /path/to/luffy-agentic-workflow
claude plugin install dev-skills@luffy-agentic-workflow
```

### Codex

**In this repo:** we develop the skills here, so Codex reads them directly from
the checkout. Edits are available without reinstalling the plugin.

- `.agents/skills` links to `plugins/dev-skills/skills` for local skill discovery.
- `.codex/config.toml` disables the cached plugin in this repo to avoid loading duplicate skills.

**Across repos (CLI):** register your local clone as a user-level marketplace:

```bash
# If luffy-agentic-workflow is already configured from GitHub, remove that source first:
codex plugin marketplace remove luffy-agentic-workflow
codex plugin marketplace add /path/to/luffy-agentic-workflow
codex plugin add dev-skills@luffy-agentic-workflow
```

Codex loads a cached copy, so after editing the clone, repeat `codex plugin add dev-skills@luffy-agentic-workflow` and start a new session (restart the desktop app if using it). `marketplace upgrade` applies to Git sources, not local paths. To return to GitHub, remove the local marketplace source, then repeat the Codex install steps above. See the [official packaging docs](https://developers.openai.com/plugins/build/plugins#how-local-marketplaces-work) for local marketplace behavior.

For `dev-skills`, run `scripts/check-plugin.sh`, `scripts/run-tests.sh` (every `test*` file under `evals/` and `scripts/`; a new test joins by its name) and `claude plugin validate .` before pushing.

## Layout

```
luffy-agentic-workflow/
├── .agents/
│   ├── plugins/
│   │   └── marketplace.json    # Codex catalog (dev-skills only)
│   └── skills -> ../plugins/dev-skills/skills  # Codex skills from this checkout
├── .claude/
│   ├── settings.json           # disable the cached plugin in this repo
│   └── skills -> ../plugins/dev-skills/skills  # Claude Code skills from this checkout
├── .codex/
│   └── config.toml             # disable the cached plugin in this repo
├── .claude-plugin/
│   └── marketplace.json        # Claude Code catalog
├── LICENSE                     # MIT, for our own work
└── plugins/
    └── dev-skills/
        ├── .claude-plugin/
        │   └── plugin.json     # plugin manifest
        ├── .codex-plugin/
        │   └── plugin.json     # Codex manifest, same name and version
        ├── skills/             # shared by both agents
        ├── CHANGELOG.md        # what each version brought
        └── LICENSE-mattpocock-skills  # MIT notice for the skills that began as Matt Pocock's
```
