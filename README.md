# luffy-dev marketplace

Personal Claude Code plugin marketplace.

## Plugins

| Plugin | Description |
|--------|-------------|
| [`dai-portal-data`](plugins/dai-portal-data/) | Local DAI Portal Postgres docker lifecycle + verified query cookbook for the `example_db` schema |

## Install

From inside Claude Code:

```
/plugin marketplace add https://github.com/Luffytse/luffy-dev-plugin
/plugin install dai-portal-data@luffy-dev
```

Or from the shell:

```bash
claude plugin marketplace add https://github.com/Luffytse/luffy-dev-plugin
claude plugin install dai-portal-data@luffy-dev
```

After install, the plugin's skills are namespaced as `dai-portal-data:dai-portal-db-lifecycle` and `dai-portal-data:dai-portal-db-queries`.

## Update

```bash
# In Claude Code
/plugin marketplace update luffy-dev

# Or from the shell
claude plugin marketplace update luffy-dev
```

## Contributing / local development

If you're hacking on the plugin itself, point the marketplace at your local clone instead of GitHub:

```bash
claude plugin marketplace add /path/to/luffy-dev-plugin
claude plugin install dai-portal-data@luffy-dev
```

## Layout

```
luffy-dev-plugin/
├── .claude-plugin/
│   └── marketplace.json        # marketplace catalog
└── plugins/
    └── dai-portal-data/
        ├── .claude-plugin/
        │   └── plugin.json     # plugin manifest
        └── skills/
            ├── dai-portal-db-lifecycle/SKILL.md
            └── dai-portal-db-queries/SKILL.md
```
