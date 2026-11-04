# Prompt for case plan

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

The user's message: "Let's start a Milestone. I want the greeter to say goodbye and to stay quiet in scripts."

The user's answers:
- Goal: "By the end, the greeter can say goodbye and can run silently in scripts, so it can ship as 1.0."
- Features: "Two: the farewell command (issue 10, a Spec, already split into Tickets 11 and 12) and the quiet flag
  (issue 20, a lone Ticket). I planned both already; their acceptance criteria are in the issues."
- Any feature an agent proposes: "No, not in this Milestone."
- Order: "Farewell first, then quiet. Two at once is fine."
- Milestone acceptance: "Both merged and closed, and at the review I run `greet.sh --quiet bye Ada` and see nothing."
- Excluded: "Colour output (issue 30) and translations."
- The draft Milestone issue: "Yes, that's it. Write it."
- Startup verification: "It has not run in this environment yet."

Stop when the skill would hand over to its next phase.
---
