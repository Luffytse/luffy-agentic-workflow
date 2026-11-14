# luffy-agentic-workflow

Plugin marketplace for Claude Code, holding one plugin: `dev-skills`, our agentic development workflow (the skill set from specs and tickets to review and release).

## Plugins

| Plugin | Description |
|--------|-------------|
| [`dev-skills`](plugins/dev-skills/) | Development skills: model-invocable skills that began as Matt Pocock's and are now our own (wayfinder, grilling, specs, tickets, TDD, code review) |

## Install

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

## Update

```bash
# In Claude Code
/plugin marketplace update luffy-agentic-workflow

# Or from the shell
claude plugin marketplace update luffy-agentic-workflow
```

## Contributing / local development

**In this repo:** we develop the skills here, so start Claude Code from the repo
root with the plugin folder flag and it loads the checkout's plugin directly.
Edits are available without reinstalling the plugin:

```bash
claude --plugin-dir plugins/dev-skills
```

Without the flag, a local session loads no `dev-skills` skill.
`.claude/settings.json` disables the installed marketplace copy in this repo, so
a session never loads a stale cached copy. Cloud threads of this project load
the plugin from the checkout through the cloud environment's plugin folder setting.

**Across repos:** point the marketplace at your local clone instead of GitHub:

```bash
claude plugin marketplace add /path/to/luffy-agentic-workflow
claude plugin install dev-skills@luffy-agentic-workflow
```

For `dev-skills`, run `scripts/check-plugin.sh`, `scripts/run-tests.sh` (every `test*` file under `scripts/`; a new test joins by its name) and `claude plugin validate .` before pushing.

## Layout

```
luffy-agentic-workflow/
├── .claude/
│   └── settings.json           # disable the cached plugin in this repo
├── .claude-plugin/
│   └── marketplace.json        # marketplace catalog
├── LICENSE                     # MIT, for our own work
└── plugins/
    └── dev-skills/
        ├── .claude-plugin/
        │   └── plugin.json     # plugin manifest, the version source
        ├── skills/             # every skill
        ├── CHANGELOG.md        # what each version brought
        └── LICENSE-mattpocock-skills  # MIT notice for the skills that began as Matt Pocock's
```
