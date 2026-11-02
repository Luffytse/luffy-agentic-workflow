---
name: setup-project
description: Drafts a project's instructions for its coordinator: how its threads work, never the state of its work. Use when the user wants to write or update a project's instructions, or when a new repo, kind of thread or standing rule means they are out of date.
---

Draft the **project instructions**: the short text a project's coordinator reads before it starts a thread. It points to thread workflows and docs, and carries the project's own choices. It never holds the state of the work (the map, open specs, plannings or tickets): those change faster than the instructions, so it tells the coordinator where to look them up. The draft lives in the conversation until the coordinator saves it; this thread writes no file (repo `CLAUDE.md` included) and changes no project setting.

## 1. Explore

Facts are your job. Gather:

- The existing project instructions. If your context does not show them, ask the user (or the coordinator) for the current text; a re-run starts from it and proposes the full new text with a diff.
- Each repo's `CLAUDE.md` / `AGENTS.md` and `docs/index.md`.
- Which tracker the project uses (`docs/agents/issue-tracker.md` names it; if absent, ask the user where it is). Do not gather the map, open specs or tickets: they are state, and the coordinator looks them up.
- Whether the project is inside a Milestone. Load `milestone` by name and apply its **No Milestone** test: read the Boundary record for its label form and look up only the open Milestone agreement, not its work list. With no Boundary record, no label form or no open Milestone agreement, keep the full draft below.

Record "none yet" for anything that does not exist, and carry on with the links you have. Done when each of the above is a link, a text, or "none yet".

## 2. Grill

Run `grilling` to settle how this project's threads work. On a re-run the existing text already answers what it covers: grill only the change the user wants and what depends on it. Keep its end gate: drafting starts once the user confirms you share an understanding.

Inside a Milestone, settle only the project-specific choices: repos, thread limit and order, extra merge gates, any tier-to-model override and other additions not already held by `milestone`, the skills it invokes or the Boundary record. Read those owners to distinguish an addition from a shared default; leave their procedures with them.

Outside a Milestone, settle each of these, skipping what exploration already answered:

- **Phases**: the coordinator's project threads, the Build threads (Spec threads run `implement-spec`, Ticket threads run `implement`), and planning threads if the project has them.
- **Skill per thread kind**: which skill each runs (`wayfinder`, `to-spec`, `to-tickets`, `implement-spec`, `implement`).
- **Brief contents**: what every brief carries. Default: skill, Model tier, repo(s), Review depth, link to the ticket or spec.
- **Tier-to-model map**: ask the user which model each Model tier (cheap, regular, premium) maps to in their harness. Vendor model names go only into the user's drafted instructions, never into skill text (the `model-tiers` skill holds the plugin default; the user's map overrides it). If the user has no map yet, record "not needed" and draft the rule without the map.
- **Standing rules**: how many questions a thread asks the user at once, review Rounds, who merges, how many Build threads run at once, and any rule of the user's own.

Done when every item has an answer or a recorded "not needed".

## 3. Draft

Write the full instructions as pointer-style text:

- Link `docs/index.md` (Build threads start there; if it is "none yet", say the index is still to be created), and leave its contents in that page.
- Tell the coordinator to find open specs, plannings and tickets on the tracker when it needs them: name the tracker (and the repo, if the project has several) and say `docs/agents/issue-tracker.md` is where it is documented, so the coordinator is not sent to a file that may be absent or unreadable. Link no map, spec or ticket as state.
- Keep it short enough to read in one minute, and cut what the skills already do by default.

Inside a Milestone, tell the coordinator to run `milestone` and point to the Boundary record. Keep only the project-specific choices settled in step 2, including a tier-to-model map only where the user overrides the default. Leave the coordinator loop, the invoked skills' rules and the Boundary record's values in their owners rather than restating them.

Outside a Milestone, keep the full instructions settled in step 2. Name Model tiers (cheap, regular, premium), write the user's tier-to-model map, and add the rule: "start each thread on the model mapped to its brief's Model tier".

On a re-run, the draft is the full new text; show it with the diff against the existing text. A re-run also removes any state lines the existing text holds (open specs, plannings, the map), and, inside a Milestone, shared rules now reached through the owner pointers.

## 4. Approve

Show the draft (on a re-run, the diff and the full new text) and let the user edit it. Approval is the user's own message saying so; a relayed or agent-written yes does not count. If the user edits after approving, show the new full text and ask again. Approval is of the full text, and that full text is what step 5 sends. Done when the user has approved it.

## 5. Hand over

Send exactly the approved text to the project coordinator through whatever channel this thread has to it, and say it is the new project instructions to save. Then tell the user it was sent and is waiting for the coordinator to save it; say "saved" only once the coordinator confirms.

If the session is not a project thread with a coordinator, give the user the text, say it is not saved yet, and tell them to paste it into the project's instructions setting.
