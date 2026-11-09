---
name: setup-project
description: "Drafts a project's coordinator instructions: how its threads work, never the state of its work. Use when the user wants to write or update them, or a new repo, thread kind or standing rule makes them stale."
---

Draft the **project instructions**: the short text a project's coordinator reads before it starts a thread. It points to thread workflows and docs, and carries the project's own choices. It never holds the state of the work (the map, open specs, plannings or tickets): those change faster than the instructions, so it tells the coordinator where to look them up. The draft lives in the conversation until the coordinator saves it; this thread writes no file (repo `CLAUDE.md` included) and changes no project setting.

## 1. Explore

Facts are your job. Gather:

- The existing project instructions. If your context does not show them, ask the user (or the coordinator) for the current text; a re-run starts from it and proposes the full new text with a diff.
- Each repo's `CLAUDE.md` / `AGENTS.md` and `docs/dev-skills/index.md`.
- Which tracker the project uses (`docs/dev-skills/issue-tracker.md` names it; if absent, ask the user where it is). Do not gather the map, open specs or tickets: they are state, and the coordinator looks them up.
- Whether the project is inside a Milestone. Load `milestone` by name and apply its **No Milestone** test: read the Boundary record for its label form and look up only the open Milestone agreement, not its work list. With no Boundary record, no label form or no open Milestone agreement, keep the full draft below.
- Whether the coordinator can load the plugin's skills. If you are the coordinator, read your own skill list; otherwise ask the coordinator to check its own and report whether `team-lead`, `milestone`, `release` and `worker-control` are in it, and never guess from your own list. Record "can", "cannot" or "unknown" (unknown counts as "cannot").

Record "none yet" for anything that does not exist, and carry on with the links you have. Done when each of the above is a link, a text, or "none yet".

## 2. Grill

Run `grilling` to settle how this project's threads work. On a re-run the existing text already answers what it covers: grill only the change the user wants and what depends on it. Keep its end gate: drafting starts once the user confirms you share an understanding.

Inside a Milestone, settle only the project-specific choices: repos, thread limit and order, extra merge gates, any tier-to-model override and other additions not already held by `milestone`, `team-lead`, the skills it invokes or the Boundary record. Read those owners to distinguish an addition from a shared default; leave their procedures with them.

Outside a Milestone, settle each of these, skipping what exploration already answered:

- **Phases**: the coordinator's project threads, the Build threads (Spec threads run `implement-spec`, Ticket threads run `implement`), and planning threads if the project has them.
- **Skill per thread kind**: which skill each runs (`wayfinder`, `to-spec`, `to-tickets`, `implement-spec`, `implement`); the coordinator itself runs `team-lead` to deliver planned work (a Release, or a Milestone with `milestone`).
- **Brief contents**: what every brief carries. Default: skill, Model tier, repo(s), Review level, link to the ticket or spec.
- **Tier-to-model map**: ask the user which model each Model tier (cheap, regular, premium) maps to in their harness. Vendor model names go only into the user's drafted instructions, never into skill text (the `model-tiers` skill holds the plugin default; the user's map overrides it). If the user has no map yet, record "not needed" and draft the rule without the map.
- **Standing rules**: how many questions a thread asks the user at once, review Rounds, who merges, how many Build threads run at once, and any rule of the user's own.

Done when every item has an answer or a recorded "not needed".

## 3. Draft

Write the full instructions as pointer-style text:

- Link `docs/dev-skills/index.md` (Build threads start there; if it is "none yet", say the index is still to be created), and leave its contents in that page.
- Tell the coordinator to find open specs, plannings and tickets on the tracker when it needs them: name the tracker (and the repo, if the project has several) and say `docs/dev-skills/issue-tracker.md` is where it is documented, so the coordinator is not sent to a file that may be absent or unreadable. Link no map, spec or ticket as state.
- Keep it short enough to read in one minute (the assembled cycle below is exempt), and cut what the skills already do by default.

**A coordinator that cannot load the plugin's skills** (recorded "cannot" or "unknown"), inside a Milestone or not, cannot read the cycle it runs, so the draft carries it. Read `team-lead`, and `milestone`'s Planning, Startup verification, Delivery and Milestone review parts, from the plugin you run from, or, when its version is behind main's on the source repository its manifest names, from that main (read from the remote), so the text matches the stamp below. From them and the project's facts, write what this coordinator does at each point, from the user's ask to plan to the user's acceptance. It starts a thread for each step that needs a skill or a write it cannot make, so never tell it to run `milestone`, `team-lead` or `release` itself. Before showing the draft, check that it covers each item below, and name to the user any you could not fill:

- how planning starts, as `milestone`'s Planning gives it (set-aside work offered first, the Milestone issue written last, after the features are planned);
- feature planning briefs: the skills a feature thread runs for each kind of feature (the project's own, or `milestone`'s Planning's where it names none); the Milestone number and the planning thread's link, worded so `to-tickets` counts the feature in that Milestone, ending with an issue holding acceptance criteria, and a scope change reported to the planning thread;
- a feature the user plans mid-Milestone (planned first, then added as `milestone` says), and a bug the user raises then (a `triage` thread files it);
- Startup verification before any Build thread;
- each delivery step of `team-lead` as it now reads, its Releases rule included, and the thread limit;
- the check-in as `team-lead` arranges and ends it (on when Build threads start, off as the report starts), through a thread where the coordinator cannot do it;
- build briefs: `team-lead`'s evidence line, and main's copy of each skill where the repo's docs say so;
- a thread that goes quiet, and whether it still holds its slot;
- the report, started only once the last Release cut has ended; then the user's review: on acceptance a thread closes the Milestone issue, and a feature sent back goes back into delivery, as `milestone`'s report re-entry says;
- thread kinds and their tiers, chore threads included, and the tier map, always written (`model-tiers`' map for its harness where the user has none);
- the coordinator-facing merge-time steps of each repo's `CLAUDE.md` or `AGENTS.md`, copied in full;
- each term the steps use that only the skills define (parked, Order, order rule, report re-entry), with its meaning;
- a source stamp, the commit on the source repository's main that last changed `team-lead` or `milestone` (read from the remote), and a Startup verification brief line: that thread compares the stamp with main's and reports it, and when it moved the coordinator tells the user once to re-run `setup-project` and goes on unless the user says to wait.

Where the coordinator can load them, add none of this.

Inside a Milestone, point to the Boundary record, and tell a coordinator that can load them to run `milestone` for the Milestone and `team-lead` for its delivery. For it, keep only the project-specific choices settled in step 2, including a tier-to-model map only where the user overrides the default. Leave the coordinator loop, the invoked skills' rules and the Boundary record's values in their owners rather than restating them.

Outside a Milestone, keep the full instructions settled in step 2 (for a coordinator that cannot load the skills, without the line that has it run `team-lead`). Name Model tiers (cheap, regular, premium), write the user's tier-to-model map, and add the rule: "start each thread on the model mapped to its brief's Model tier".

On a re-run, the draft is the full new text; show it with the diff against the existing text. A re-run also removes any state lines the existing text holds (open specs, plannings, the map), and, inside a Milestone, shared rules now reached through the owner pointers. It also drops the assembled cycle where the coordinator can now load the plugin's skills, adds it where it can no longer, and otherwise rebuilds it, with a new stamp, from the skills as they now read.

## 4. Approve

Show the draft (on a re-run, the diff and the full new text) and let the user edit it. Approval is the user's own message saying so; a relayed or agent-written yes does not count. If the user edits after approving, show the new full text and ask again. Approval is of the full text, and that full text is what step 5 sends. Done when the user has approved it.

## 5. Hand over

Send exactly the approved text to the project coordinator through whatever channel this thread has to it, and say it is the new project instructions to save. Then tell the user it was sent and is waiting for the coordinator to save it; say "saved" only once the coordinator confirms.

If the session is not a project thread with a coordinator, give the user the text, say it is not saved yet, and tell them to paste it into the project's instructions setting.
