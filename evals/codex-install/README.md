# Codex install check

Run this manual check after Codex packaging changes and again before the Spec pull request leaves draft. Record each independent run in [RESULTS.md](RESULTS.md), including failures. The seam is the real GitHub install, discovery in a new Codex runtime, and a completed conversational `grilling` interview. A manifest check or an agent saying it knows a skill does not establish success.

## Install from a clean setup

Read the [plugin README](../../plugins/dev-skills/README.md)'s Codex install steps. Record the local date and timezone, `codex --version`, the plugin version and the immutable Git commit actually fetched.

Use a new temporary directory for each run, with an empty `home/` and empty `fixture/`. Set `CODEX_HOME` to that temporary `home/` for **every** command and runtime below. Authenticate that isolated home using the supported login flow, or securely copy existing authentication into it with restrictive permissions. Never put credentials in the repo, terminal output, or results. Do not copy the live config, installed plugins, or skill cache. Leave the user's live Codex setup alone.

Follow the README's actual GitHub install commands:

```sh
codex plugin marketplace add https://github.com/Luffytse/luffy-dev-skills --json
codex plugin add dev-skills@luffy-dev --json
codex plugin list --marketplace luffy-dev --json
```

Before the Spec merges, add `--ref <current-Spec-branch>` to `marketplace add` (equivalently use `Luffytse/luffy-dev-skills@<current-Spec-branch>`). For Spec #348, use `codex/spec-348-shared-base` and verify that the fetched SHA is the actual current candidate containing all integrated migrations; the earlier #360 loading-gate SHA alone does not establish the final Spec result. Say explicitly that this checks the remote Spec ref and leaves default-ref verification pending merge. Do not substitute a local checkout and call it a GitHub install. Record the fetched commit with `git -C "$CODEX_HOME/.tmp/marketplaces/luffy-dev" rev-parse HEAD` on the CLI version used here; if its cache layout changes, locate the fetched repository first. Confirm `dev-skills@luffy-dev` is installed and enabled and that no Claude-only plugin is offered (`list --available --marketplace luffy-dev --json` shows the catalog too).

## Discover in a new runtime

Start a new Codex session in `fixture/` with that same isolated home. Inspect the runtime's skill list and compare it with every folder under `plugins/dev-skills/skills/` at the fetched commit. Record every discovered name, missing or unexpected plugin skills, disabled skills and discovery errors. Names in this CLI are prefixed `dev-skills:`; normalize that prefix when comparing folder names.

For an observable protocol-based check, start a fresh `codex app-server --stdio` process. Exchange newline-delimited JSON-RPC: `initialize` with `clientInfo` and `capabilities.experimentalApi: true`, send the `initialized` notification, then request `skills/list` with `{"cwds":["<absolute fixture path>"],"forceReload":true}`. Inspect `data[].skills` (`name`, `path`, `enabled`) and `data[].errors`. Count only skills whose paths belong to this isolated plugin's cache; built-in skills are not plugin skills. Generate version-matched bindings with `codex app-server generate-ts --experimental --out <temporary directory>` if field names change.

## Run the interview to completion

Use the same fresh runtime and the installed `grilling` skill, with this prompt:

```text
$grilling Interview me about this small sample plan only; do not write files or implement anything. I want a personal Saturday reading habit. This is a hypothetical plan with no external facts to research. Help me settle a realistic routine and how I will judge it. Ask questions and wait for my answers; reach shared understanding before acting.
```

A human or an evaluator acting as the simulated user answers each actual round with concrete test-only decisions. Never invent assistant responses or predeclare an interview complete. Check that the skill asks focused frontier questions, recommends answers, waits between rounds, carries decisions into later questions and the final summary, then requests and receives explicit shared-understanding confirmation. Preserve exact user and assistant turns, including the final acknowledgement. A single answer, a blocked turn, or a summary without user confirmation is incomplete.

With app-server, create `thread/start` in the fixture with `ephemeral: true`, `approvalPolicy: "never"`, `sandbox: "read-only"` and a recorded available model; use `allowProviderModelFallback: false` when asserting model identity. Send `turn/start` input containing the prompt as a `text` item and a `skill` item with the **discovered** name (`dev-skills:grilling`) and installed path. For later answers, send text items on the same thread. Capture completed `agentMessage` items, check every `turn/completed` status and error, and handle any server input requests explicitly. Do not count a failed input adapter as successful interaction. Read-only permissions protect the fixture; also inspect completed tool items and fixture contents to verify the requested interview-only behavior.

## Record and clean up

Add a dated entry to RESULTS with source/ref/SHA, CLI and model versions, install/list observations, the complete discovered set and comparison, exact interview turns, completion status, limitations, and issue links. File each actual portability problem in the user's tracker with `needs-triage` and `codex-only` when appropriate; follow [the tracker rules](../../docs/dev-skills/issue-tracker.md), apply no release label, and fix no skill text in this eval change. If none occurs, say none; do not infer that unexercised skills work.

Repeat with a second newly created home and fixture. Stop app-server processes and remove temporary authentication and other test material after recording sanitized evidence. Cleanup is reversible test housekeeping; the live installation remains untouched. No extra automated tests are needed for these documentation records.
