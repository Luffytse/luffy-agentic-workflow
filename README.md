# luffy-dev marketplace

Personal Claude Code plugin marketplace.

## Plugins

| Plugin | Description |
|--------|-------------|
| [`dai-portal-data`](plugins/dai-portal-data/) | Local DAI Portal Postgres docker lifecycle + verified query cookbook for the `example_db` schema |
| [`dev-skills`](plugins/dev-skills/) | Development skills: a model-invocable fork of Matt Pocock's skills plus our own (wayfinder, grilling, specs, tickets, TDD, code review) |

## Install

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

## Update

```bash
# In Claude Code
/plugin marketplace update luffy-dev

# Or from the shell
claude plugin marketplace update luffy-dev
```

## Contributing / local development

If you're hacking on a plugin itself, point the marketplace at your local clone instead of GitHub:

```bash
claude plugin marketplace add /path/to/luffy-dev-skills
claude plugin install dai-portal-data@luffy-dev
claude plugin install dev-skills@luffy-dev
```

For `dev-skills`, run `scripts/check-plugin.sh` and `claude plugin validate .` before pushing, and record any change to Upstream text in `plugins/dev-skills/PATCHES.md`.

## Layout

```
luffy-dev-skills/
├── .claude-plugin/
│   └── marketplace.json        # marketplace catalog
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
        ├── upstream-skills/    # forked from Matt Pocock's skills
        ├── skills/             # our own skills
        └── PATCHES.md          # changes to Upstream text
```
