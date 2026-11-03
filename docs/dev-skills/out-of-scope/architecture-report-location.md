# Offering the architecture report somewhere shared

`improve-codebase-architecture` writes its HTML report to the OS temp directory and does not offer it anywhere other threads or machines can read.

## Why this is out of scope

The report is a throwaway view for the user running the skill: the skill opens it for them and tells them the path, and the user then picks one candidate to grill through. Nothing downstream reads the file, so the problem #109 fixed for `handoff` (the document must be readable outside the session's own container) matters little here.

In a cloud or remote session the file stays in the session container and the user cannot open it either. That is accepted, because fixing it means a Patch to Upstream text plus a per-harness definition of "shared", for a report that is thrown away after one use.

If a report ever has to travel, the user can ask for it to be saved or pasted where they can reach it.

## Prior requests

- #132: "Skill saves its output to the OS temp directory (found in review of #129)"
