# luffy-dev marketplace

Personal Claude Code plugin marketplace.

## Plugins

| Plugin | Description |
|--------|-------------|
| [`dai-portal-data`](plugins/dai-portal-data/) | Local DAI Portal Postgres docker lifecycle + verified query cookbook for the `example_db` schema |

## Install

```bash
# Add this marketplace (local path or git URL once pushed)
/plugin marketplace add ~/Projects/luffy-dev-plugin

# Install a plugin from it
/plugin install dai-portal-data@luffy-dev
```

After install, the plugin's skills are namespaced as `dai-portal-data:dai-portal-db-lifecycle` and `dai-portal-data:dai-portal-db-queries`.

## Update

```bash
/plugin marketplace update luffy-dev
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
