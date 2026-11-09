You are the top-level session of a code review, at the step where a Round briefs its agents. In this run you cannot start subagents: do not start any, and do not run the Finders or the Verifier yourself. Only write the briefs.

The review skills are under `<plugins>/dev-skills/skills`. Load `review-rounds` (its SKILL.md) and follow it for this Round: Round 1, level Standard, of branch `planted` against `main` in the git repository `<repo>`. The spec is `<repo>/.scratch/SPEC.md`. There are no standards files. The adversarial Finder's angle is bugs and edge cases. Do not edit the repository. Keep any other files you make outside the repository and `<briefs>`.

1. Write the brief for each Finder this Round starts into the directory `<briefs>` (create it; it is outside the repository on purpose).
2. Then suppose the Finders have all reported. Their final messages are in `<messages>`: `standards-finder.txt`, `spec-finder.txt` and `adversarial-finder.txt`, one per Finder of that name. Write the Verifier's brief into the same directory.
3. Last, write into the file `<handoff>` the exact message you would send, as the prompt, to the brand-new subagent you would start for the standards Finder (you cannot start it, so only write the message).

Reply with the files you wrote, the tier of the agent each is for, and the exact commands you ran to make them.
