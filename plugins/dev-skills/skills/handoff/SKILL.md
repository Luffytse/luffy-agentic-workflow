---
name: handoff
description: "Compact the current conversation into a handoff document for a fresh agent to continue from. Use when the user says \"handoff\" or \"hand off\", or the work moves to a new harness, directory or colleague, or a side task forks off mid-phase."
argument-hint: "What will the next session be used for?"
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save it where the next agent can read it. In a cloud or remote session the temporary directory is that session's own container, which no other thread or session can open, so it is not the default:

- By default, save the handoff as an issue on the tracker that the repo's `docs/agents/issue-tracker.md` names, and link it from the work it continues (a comment on that issue or pull request), since every thread and project can read the tracker. If the repo has no issue tracker configured, say so and ask the user where to save it; do not guess.
- Use a shared folder only when the user names one.
- Use the temporary directory only when the next agent runs on the same machine, and then save it to the temporary directory of the user's OS (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows), never the current workspace.

End by telling the user where the handoff is: the issue link, or the path.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
