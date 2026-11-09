#!/usr/bin/env python3
"""Build one case's scratch repo: python3 make_fixture.py <out-dir> <case>. Local-files tracker, no network, no real issue."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cases import CASES, CHILDREN, UNFILED


def build(out, name):
    case = CASES[name]
    w = lambda rel, text: (os.makedirs(os.path.dirname(os.path.join(out, rel)), exist_ok=True), open(os.path.join(out, rel), "w").write(text))
    w("docs/dev-skills/issue-tracker.md",
      "# Issue tracker: local files\n\nTickets are files under `.scratch/greeter/issues/<NN>-<slug>.md`. A ticket file has a `**Labels:**` line listing its labels, comma-separated. "
      "A source Spec is `.scratch/greeter/SPEC.md` with its own `**Labels:**` line. Blocking: a `**Blocked by:**` line of ticket numbers; a blocker that is not filed yet is named in the ticket's text. No forge; no network.\n")
    w("docs/dev-skills/triage-labels.md", "# Triage labels\n\n| Role | Label |\n| --- | --- |\n| `ready-for-agent` | `ready-for-agent` |\n| `bug` | `bug` |\n| `enhancement` | `enhancement` |\n")
    w("docs/dev-skills/release.md", "# Release\n\nRelease labels start with `release-`.\n")
    w("docs/dev-skills/boundaries.md", "# Boundaries\n\nNothing needs the user's approval. Milestone label form: `milestone-<n>`.\n")
    w("docs/dev-skills/index.md", "# Docs index\n\n- issue-tracker.md, triage-labels.md, release.md, boundaries.md\n")
    spec = ["# Spec: greeter", "", "**Labels:**", "", "A plain-text greeting formatter and a greeting for logged-in users.", "", "## Proposed breakdown (not yet approved)", ""]
    for cid, c in CHILDREN.items():
        blocked = f"the {UNFILED} feature (planned, not filed yet)" if (cid == "02" and case["unfiled_blocker"]) else ("01" if cid == "02" else "")
        spec.append(f"{cid}. {c['title']} (regular tier)" + (f", blocked by {blocked}" if blocked else ""))
        spec += [f"   - {x}" for x in c["criteria"]]
    w(".scratch/greeter/SPEC.md", "\n".join(spec) + "\n")
    prompt = ("Isolated fixture; the tracker is local files. Run `to-tickets` on the Spec `.scratch/greeter/SPEC.md` now: split it, publish the tickets with the configured tracker and label mapping, "
              "then reply with the outcome the skill requires. No interview beyond what the skill requires; no network calls. If you need the user's answer, ask the one question and stop.")
    if case["milestone_statement"]:
        prompt += " You are called by the thread planning a feature of Milestone 2; the Milestone issue is not written yet."
    w("PROMPT.md", prompt + "\n")
    w("REPORT.txt", "")  # the run saves its final reply here before scoring


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CASES:
        sys.exit("usage: make_fixture.py <out-dir> <" + "|".join(CASES) + ">")
    build(sys.argv[1], sys.argv[2])
