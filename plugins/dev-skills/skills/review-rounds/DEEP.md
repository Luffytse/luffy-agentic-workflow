# Deep

What Deep adds in [`review-rounds`](SKILL.md), for a change that touches what the project marks risky.

- **Round 1:** Standard's three Finders, plus the security Finder below on the premium tier. Pick the adversarial Finder's angle for the risk; **what the change is missing** fits a change that moves or removes code.
- **The Verifier** runs on the premium tier and gets the security Finder's Findings with the rest.
- **Rounds 2 and 3:** the later-Round Finder and the Verifier run on the premium tier, and the Finder also gets the security brief.

## Security Finder (premium tier)

It gets what every Finder gets ([FINDERS.md](FINDERS.md)) and the spec.

Brief: "Review this change for security and privacy only, in depth. Trace every input an outside party controls from where it enters to where it is used (HTML, SQL, shell, file paths, URLs, logs, other services), and check authentication, authorisation, secrets, personal data, deleting data, migrations and new dependencies. Cite the source-to-sink path for each Finding."
