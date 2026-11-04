# Prompt for case plan-small

Give a fresh session only the text between the lines, with <checkout> replaced by the checkout under test.

---
You are the coordinator of the project in this working directory. Load the `milestone` skill from
<checkout>/plugins/dev-skills/skills/milestone/SKILL.md (that copy, not an installed one) and follow it. Load any other
skill it names from the same checkout's `plugins/dev-skills/skills/`.

This is a dry run. The tracker doc, `docs/dev-skills/issue-tracker.md`, says how every write is recorded in
`.scratch/proposed-actions.md` instead of being made: follow it for every tracker write and every thread you would
start. Change no other file. The user is scripted: append every question you ask the user to `.scratch/questions.md`,
one `- ` line each, then take the answer from "The user's answers" below; when a question is not covered there, add
` (unanswered)` to its line, treat it as unanswered, and do not guess an answer. Today is 2026-11-02.

When you stop, write `.scratch/report.md`: the last message you would send the user, and what the skill says comes
next and what it waits for.

The user's message: "Let's plan a small Release: just the quiet flag (issue 20). I planned it already; its acceptance
criteria are in the issue."

The user's answers:
- Goal: "Scripts can run the greeter silently."
- Any feature an agent proposes: "No."
- The draft Milestone issue: "Yes, that's it. Write it."
- Startup verification: "It has not run in this environment yet."

Stop when the skill would hand over to its next phase.
---
