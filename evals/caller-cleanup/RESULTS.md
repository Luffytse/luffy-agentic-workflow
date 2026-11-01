# Caller cleanup results

## 2026-10-31 — #366

Pre-migration baseline: `9b98dfec4cf92df1e354d542a4961d4216b45054`. Candidate: the four caller edits recorded with this evidence on top of that commit. Six clean local installs and fresh app-server processes; model `regular Codex tier from plugins/dev-skills/README.md at 9b98dfec4cf92df1e354d542a4961d4216b45054`, provider `openai`, fallback disabled. Each discovered all 29 plugin skills, with no missing/disabled entries or discovery errors. Menu visibility is unmeasured.

All six turns completed without error. The baseline already passed custom tracker behavior; this is a preservation refactor, with no claimed red behavioral failure. Each case folder retains exact user/assistant turns, sanitized completed tool events, discovery, cache SHA-256 hashes and observed artifacts.

| Case | Observed result |
| --- | --- |
| baseline | One configured finish for T3; no duplicate T4 operation; T1 blocks despite being closed, T2 clears. |
| implement | Same tracker outcomes; read installed agentic-review SKILL/ROUNDS/FINDERS/VERIFY and review-record; existing A gets text fixes; commit/evidence returned; final text Nit committed before clean status, agreed design change gets Round 4, Deep goes to user. |
| implement-spec | Same tracker outcomes and installed workflow reads; new premium Implementer on Spec branch, push evidence and permitted continuation; prior checks and Pre-existing context carried; Quick Ticket-check input/destination preserved; Standard uses merge commit and Deep goes to user. |
| local-completion | With no PR closing lines/support, configured operations closed Spec S1 and landed T1; dropped T2 remained open. |
| to-spec | Created published.json using configured operation and robot-queue mapping. |
| to-tickets | Created published.json using configured operation and robot-queue mapping; one regular Ticket, no blockers. |

CLI: `codex-cli 0.166.0-alpha.5.1`.

Installed snapshots matched source at installation. Provenance comparisons saved after the run flag only `implement-spec/SKILL.md` in candidate installs: a trailing space was removed and the existing no-PR-closing-support completion path was restored explicitly through configured operations. The sixth `local-completion` run tests this final wording and has no source mismatches; baseline also has none. The candidate snapshot hashes preserve the tested bytes.

Limitations: prompts resume bounded operations and explicitly request a fixture-only review coordination plan, so these results prove actual dependency reads, decisions and local configured writes, not end-to-end reviewer dispatch, remote tracker transport, merge execution or the full five-Round lifecycle. These checks do not replace the final integrated Spec's full review and clean remote-install eval. No real tracker write, branch creation, reviewer dispatch or retro occurred.

Repository checks, all five packaging tests, Claude plugin validation pass. The initial whitespace check covered only the tracked working-tree diff, so it did not inspect the then-untracked eval files. Not visual. Reversible documentation/eval artifacts only; no one-way door. Isolated credentials and raw runtime data are removed after evidence extraction; the live installation is untouched.

Validation note: the first post-evidence check rejected literal model names in the eval record. The record now pins the model through the immutable README tier table, matching existing eval practice; no checker exemption was added.

The pre-review committed Ticket diff check found renderer-added blank separators at EOF in all six `transcript.txt` files. Those final newline runs are normalized to one final newline; all user/assistant message text and internal separators are preserved. The full committed Ticket diff (`git diff --check codex/spec-348-shared-base...HEAD`) passes after this formatting correction. No behavioral rerun was needed.

## Ticket check 1 correction — positive merged-state gate

Finding T366.1-1 identified that the caller cleanup had removed the concrete merged-state command. Both builders again require `gh api repos/<owner>/<repo>/pulls/<n> --jq .merged` to print `true` before completing issues, including the user-merged resume path. Reads that fail or return anything else do not authorize completion. Configured issue reads and Close/completion operations remain unchanged.

The exact decision command was run read-only on actual repository history:

| Command | Output | Outcome |
| --- | --- | --- |
| `gh api repos/Luffytse/luffy-dev-skills/pulls/375 --jq .merged` | `true` (exit 0) | Merged; passes the gate. |
| `gh api repos/Luffytse/luffy-dev-skills/pulls/157 --jq .merged` | `false` (exit 0) | Closed unmerged; does not pass the gate. |

Both examples have `state: closed` in the PR listing, demonstrating why closed state alone is insufficient. No issue was modified. The earlier fixture probes started after a stipulated verified merge and remain evidence for downstream configured operations; these real-history command checks cover the restored preceding gate.
