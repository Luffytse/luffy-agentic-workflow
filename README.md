# luffy-dev marketplace

Personal plugin marketplace for Claude Code and Codex. Codex offers `dev-skills`; `dai-portal-data` is Claude Code only.

## Plugins

| Plugin | Description |
|--------|-------------|
| [`dai-portal-data`](plugins/dai-portal-data/) | Local DAI Portal Postgres docker lifecycle + verified query cookbook for the `example_db` schema |
| [`dev-skills`](plugins/dev-skills/) | Development skills: model-invocable skills that began as Matt Pocock's and are now our own (wayfinder, grilling, specs, tickets, TDD, code review) |

## Install

### Claude Code

From inside Claude Code:

```
/plugin marketplace add https://github.com/Luffytse/luffy-dev-skills
/plugin install dai-portal-data@luffy-dev
/plugin install dev-skills@luffy-dev
```

Or from the shell:

```bash
claude plugin marketplace add https://github.com/Luffytse/luffy-dev-skills
claude plugin install dai-portal-data@luffy-dev
claude plugin install dev-skills@luffy-dev
```

After install, the plugins' skills are namespaced, for example `dai-portal-data:dai-portal-db-lifecycle` and `dev-skills:wayfinder`.

### Codex

From the shell (verified with Codex CLI `0.166.0-alpha.5.1`):

```bash
codex plugin marketplace add https://github.com/Luffytse/luffy-dev-skills
codex plugin add dev-skills@luffy-dev
codex plugin list --marketplace luffy-dev --json
```

The list should show `dev-skills` installed and enabled. Start a new Codex session to load the skills. See the [dev-skills Model tiers](plugins/dev-skills/README.md#model-tiers) for model selection.

## Update

### Claude Code

```bash
# In Claude Code
/plugin marketplace update luffy-dev

# Or from the shell
claude plugin marketplace update luffy-dev
```

### Codex

For a marketplace installed from GitHub, refresh its checkout and reinstall the current plugin contents:

```bash
codex plugin marketplace upgrade luffy-dev
codex plugin add dev-skills@luffy-dev
```

Start a new Codex session after updating (restart the desktop app if using it).

## Contributing / local development

### Claude Code

If you're hacking on a plugin itself, point the marketplace at your local clone instead of GitHub:

```bash
claude plugin marketplace add /path/to/luffy-dev-skills
claude plugin install dai-portal-data@luffy-dev
claude plugin install dev-skills@luffy-dev
```

### Codex

Use the local clone as the marketplace source:

```bash
# If luffy-dev is already configured from GitHub, remove that source first:
codex plugin marketplace remove luffy-dev
codex plugin marketplace add /path/to/luffy-dev-skills
codex plugin add dev-skills@luffy-dev
```

Codex loads a cached copy, so after editing the clone, repeat `codex plugin add dev-skills@luffy-dev` and start a new session (restart the desktop app if using it). `marketplace upgrade` applies to Git sources, not local paths. To return to GitHub, remove the local marketplace source, then repeat the Codex install steps above. See the [official packaging docs](https://developers.openai.com/plugins/build/plugins#how-local-marketplaces-work) for local marketplace behavior.

For `dev-skills`, run `scripts/check-plugin.sh` and `claude plugin validate .` before pushing.

## Layout

```
luffy-dev-skills/
├── .agents/plugins/
│   └── marketplace.json        # Codex catalog (dev-skills only)
├── .claude-plugin/
│   └── marketplace.json        # Claude Code catalog
└── plugins/
    ├── dai-portal-data/
    │   ├── .claude-plugin/
    │   │   └── plugin.json     # plugin manifest
    │   └── skills/
    │       ├── dai-portal-db-lifecycle/SKILL.md
    │       └── dai-portal-db-queries/SKILL.md
    └── dev-skills/
        ├── .claude-plugin/
        │   └── plugin.json     # plugin manifest
        ├── .codex-plugin/
        │   └── plugin.json     # Codex manifest, same name and version
        ├── skills/             # shared by both agents
        ├── CHANGELOG.md        # what each version brought
        └── LICENSE-mattpocock-skills  # MIT notice for the skills that began as Matt Pocock's
```
