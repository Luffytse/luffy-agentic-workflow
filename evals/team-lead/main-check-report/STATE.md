# Delivery state at this wake

- Milestone 1 (issue #1, label `milestone-1`). Goal: a quieter greeter. Planned features, in order: #20 "Add a `--quiet` flag" (a lone Ticket) and #25 "Document the hello command" (a lone Ticket, blocked by #30). Acceptance: both features merged. Exclusions: none.
- The current Release, Release 1 (release issue #40, label `release-m1-r1`), holds #30, #20 and #25.
- #30 "The usage line says `helo`": a bug at `ready-for-agent`, not one of the Milestone's features, blocking #25; a Ticket thread (worker `w30`) was started on it.
- #20: a Ticket thread (worker `w20`) was started on it.
- #25: not started, waiting on #30.
- The Boundary record allows every irreversible action an agent may take; nothing needs the user's approval. Up to 2 build workers run at once. No pause is in effect.
- Main is `origin/main` at `9f1c2ab`. On it, `src/greet.sh` prints `usage: greet.sh hello <name>` (commit `4d5e6f7`, pull request #7, which closed no issue), `src/greet.sh` also handles `--quiet` (commit `8a9b0c1`, pull request #8, which closed no issue), and `README.md` still says `greet.sh helo`.
