---
name: setup-project
description: Drafts a project's instructions for its coordinator. Use when the user wants to write or update a project's instructions, or when wayfinder or to-tickets offers it at their end.
---

Draft the **project instructions**: the short text a project's coordinator reads before it starts a thread. It says how threads work and what every brief contains, and points at the map, specs and docs. The draft lives in the conversation until the coordinator saves it; this thread writes no file (repo `CLAUDE.md` included) and changes no project setting.

## 1. Explore

Facts are your job. Gather:

- The existing project instructions. If your context does not show them, ask the user (or the coordinator) for the current text; a re-run starts from it and proposes the full new text with a diff.
- Each repo's `CLAUDE.md` / `AGENTS.md` and `docs/index.md`.
- The tracker (`docs/agents/issue-tracker.md` names it; if absent, ask the user where it is): the wayfinder map issue and the open specs.

Record "none yet" for anything that does not exist, and carry on with the links you have. Done when each of the above is a link, a text, or "none yet".

## 2. Grill

Run `grilling` to settle how this project's threads work. On a re-run the existing text already answers what it covers: grill only the change the user wants and what depends on it. Keep its end gate: drafting starts once the user confirms you share an understanding.

Settle each of these, skipping what exploration already answered:

- **Phases**: the coordinator's project threads, the Build threads (Spec threads run `implement-spec`, Ticket threads run `implement`), and planning threads if the project has them.
- **Skill per thread kind**: which skill each runs (`wayfinder`, `to-spec`, `to-tickets`, `implement-spec`, `implement`).
- **Brief contents**: what every brief carries. Default: skill, Model tier, repo(s), Review depth, link to the ticket or spec.
- **Standing rules**: how many questions a thread asks the user at once, review Rounds, who merges, how many Build threads run at once, and any rule of the user's own.

Done when every item has an answer or a recorded "not needed".

## 3. Draft

Write the full instructions as pointer-style text:

- Link the wayfinder map, each open spec and `docs/index.md` (Build threads start there; if it is "none yet", say the index is still to be created), and leave their contents in those pages.
- Name Model tiers (cheap, regular, premium).
- Keep it short enough to read in one minute, and cut what the skills already do by default.

On a re-run, the draft is the full new text; show it with the diff against the existing text.

## 4. Approve

Show the draft (on a re-run, the diff and the full new text) and let the user edit it. Approval is the user's own message saying so; a relayed or agent-written yes does not count. If the user edits after approving, show the new full text and ask again. Approval is of the full text, and that full text is what step 5 sends. Done when the user has approved it.

## 5. Hand over

Send exactly the approved text to the project coordinator through whatever channel this thread has to it, and say it is the new project instructions to save. Then tell the user it was sent and is waiting for the coordinator to save it; say "saved" only once the coordinator confirms.

If the session is not a project thread with a coordinator, give the user the text, say it is not saved yet, and tell them to paste it into the project's instructions setting.
