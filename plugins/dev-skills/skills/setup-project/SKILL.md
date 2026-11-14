---
name: setup-project
description: "Drafts a project's coordinator instructions: how its threads work, never the state of its work. Use when the user wants to write or update them, or a new repo, thread kind or standing rule makes them stale."
---

Draft the **project instructions**: the short text a project's coordinator reads before it starts a thread. It points to thread workflows and docs and carries the project's own choices. It never holds the state of the work (the map, open specs, plannings or tickets), which changes faster than the instructions; it says where to look that up. The draft lives in the conversation until the coordinator saves it; this thread writes no file (repo `CLAUDE.md` included) and changes no project setting.

## 1. Explore

Facts are your job. Gather:

- The existing project instructions. If your context does not show them, ask the user (or the coordinator) for the current text; a re-run starts from it.
- Each repo's `CLAUDE.md` / `AGENTS.md` and `docs/dev-skills/index.md`.
- Which tracker the project uses (`docs/dev-skills/issue-tracker.md` names it; if absent, ask the user). Gather no map, spec or ticket: they are state.
- Whether the coordinator can load the plugin's skills. If you are the coordinator, read your own skill list; otherwise ask the coordinator whether `team-lead`, `milestone`, `release` and `worker-control` are in its own, and never guess from yours. Record "can", "cannot" or "unknown" (unknown counts as "cannot").
- The size limit of the instructions. It belongs to the tool the coordinator runs in, not to the project: read it from `worker-control`'s reference for that tool where the reference states one, otherwise ask the user. Record the limit and its unit, or "none known".

Record "none yet" for anything that does not exist. Done when each item is a link, a text, or "none yet".

## 2. Grill

Run `grilling` to settle the project's own choices: repos, any thread limit, extra merge gates, any tier-to-model override, and other rules of the user's own that `milestone`, `team-lead`, the skills they invoke and the Boundary record do not already hold. Read those owners to tell an addition from a shared default, and leave their procedures with them. Vendor model names go only into the drafted instructions, never into skill text. On a re-run, grill only the change the user wants and what depends on it. Keep the end gate of `grilling`: drafting starts once the user confirms you share an understanding.

## 3. Draft

Write the full instructions as pointer-style text:

- Link `docs/dev-skills/index.md`, where Build threads start (if it is "none yet", say it is still to be created).
- Name the tracker (and the repo, if the project has several) and `docs/dev-skills/issue-tracker.md` as where it is documented, for the coordinator to look up open specs, plannings and tickets; link none of them as state.
- Point to the Boundary record, and keep only the choices settled in step 2, a tier-to-model map only where the user overrides the default.
- Keep it short enough to read in one minute (the assembled cycle below is exempt), and cut what the skills already do by default.

A coordinator that can load the skills is told to run `milestone` for the Milestone and `team-lead` for its delivery, and gets nothing more.

**A coordinator that cannot load the plugin's skills** ("cannot" or "unknown") gets the cycle in the draft. Read `team-lead`, `milestone`'s Planning, Plugin version check and Delivery parts with its `reporting.md`, and the tier each thread's skill names, from the plugin you run from or, when its version is behind main's on the source repository its manifest names, from that main, so the text matches the stamp. Write what this coordinator does at each point, from the user's ask to plan to the user's acceptance. It starts a thread for each step that needs a skill or a write it cannot make, so never tell it to run `milestone`, `team-lead` or `release` itself. Before showing the draft, check that it covers each point below as the skills give it, and name to the user any you could not fill:

- planning, a feature asked for once it has settled, and a bug the user raises (a `triage` thread files it);
- the check before delivery starts;
- delivery: each step of `team-lead`, with its records and briefs, and main's copy of each skill where the repo's docs ask for it;
- the check-in, through a thread where the coordinator cannot arrange it;
- the report;
- the user's review;
- thread kinds and their tiers, a chore thread for each record or Harness action the coordinator cannot take, and the tier map (`model-tiers`' map for its harness where the user has none);
- each term the steps use that only the skills define, with its meaning;
- a source stamp, the commit on the source repository's main that last changed `team-lead` or `milestone` (read from the remote), and a line in the brief of the thread making the check before delivery: it compares the stamp with main's and reports both; when it moved, the coordinator tells the user once to re-run `setup-project` and goes on unless told to wait.

**Size.** With a limit known, count the draft in the limit's unit before showing it, leaving about a tenth of the limit for the user's own edits. Over that, shorten in this order, each step only as far as needed:

1. Reasons, examples and sentences that repeat another.
2. Repeated forms: terms gathered into one line of meanings, short sections merged.
3. Detail a started thread reads in its own skill (what a planning, Release or report thread does inside it), keeping what the coordinator decides and what the brief carries.
4. The wording of the coordinator's own steps, thinned and never dropped.

No point is dropped without telling the user. Beside the draft (on a re-run, beside the diff too), give the count, the limit and what each step shortened. A draft that cannot fit with every point goes to the user as that, naming the points that do not fit, and is never sent over the limit. With no limit known, give the draft's size and say it could not be checked.

**On a re-run** the draft is the full new text, shown with its diff against the existing text. It removes state lines and shared rules now reached through the owner pointers. It drops the assembled cycle where the coordinator can now load the skills, adds it where it no longer can, and otherwise rebuilds it, with a new stamp, from the skills as they now read.

## 4. Approve

Show the draft (on a re-run, the diff and the full new text) and let the user edit it. Approval is the user's own message saying so; a relayed or agent-written yes does not count. If the user edits after approving, show the new full text, counted again, and ask again. Done when the user has approved the full text, which is what step 5 sends.

## 5. Hand over

Send exactly the approved text to the project coordinator through whatever channel this thread has to it, as the new project instructions to save. Tell the user it was sent and waits to be saved; say "saved" only once the coordinator confirms.

If the session is not a project thread with a coordinator, give the user the text, say it is not saved yet, and tell them to paste it into the project's instructions setting.
