# Prompt for case add-feature

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

The user's message, in a planning thread: "I want colour output (issue 30). Let's plan it."

The user's answers:
- When asked to plan issue 30: "Colour the name in `hello` green only when standard output is a terminal;
  `--no-color` turns it off, and the usage line becomes exactly `usage: greet.sh [--no-color] hello|bye <name>`.
  Accepted when a test covers
  the terminal case and `--no-color`. It is one lone Ticket."
- Its place in the order: "Third, after the quiet flag."
- Whether it joins the open Release 0.4.0: "Leave that to the rules."

Stop when the feature is added, or when the skill says it must wait.
---
