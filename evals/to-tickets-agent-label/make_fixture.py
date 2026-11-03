#!/usr/bin/env python3
"""Build one case's scratch repo: python3 make_fixture.py <out-dir> <case>. Local-files tracker, no network, no real issue."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cases import CASES, CHILDREN, MAPPING, READY


def child_text(cid, labels, case):
    c = CHILDREN[cid]
    out = [f"# {cid}: {c['title']}", "", f"**Labels:** {', '.join(labels)}", ""]
    if c.get("blocked_by"):
        out += [f"**Blocked by:** {', '.join(c['blocked_by'])}", ""]
    out += [f"- [ ] {x}" for x in c["criteria"]]
    return "\n".join(out) + "\n"


def build(out, name):
    case = CASES[name]
    w = lambda rel, text: (os.makedirs(os.path.dirname(os.path.join(out, rel)), exist_ok=True), open(os.path.join(out, rel), "w").write(text))
    w("docs/dev-skills/issue-tracker.md",
      "# Issue tracker: local files\n\nTickets are files under `.scratch/greeter/issues/<NN>-<slug>.md`. A ticket file has a `**Labels:**` line listing its labels, comma-separated. "
      "A source Spec is `.scratch/greeter/SPEC.md` with its own `**Labels:**` line. Blocking: a `**Blocked by:**` line of ticket numbers. No forge; no network.\n")
    tl = "# Triage labels\n\n| Role | Label |\n| --- | --- |\n| `ready-for-agent` | `ready-for-agent` |\n| `bug` | `bug` |\n| `enhancement` | `enhancement` |\n"
    if case["mapping"]:
        tl += "\nThe agent-only role marks an issue for one coding agent only:\n\n| Role | Label | Meaning |\n| --- | --- | --- |\n"
        tl += "".join(f"| `agent-only` | `{lab}` | Only {ag} works this issue |\n" for ag, lab in MAPPING.items())
    w("docs/dev-skills/triage-labels.md", tl)
    w("docs/dev-skills/release.md", "# Release\n\nRelease labels start with `release-`.\n")
    w("docs/dev-skills/boundaries.md", "# Boundaries\n\nNothing needs the user's approval. Milestone label form: `milestone-<n>`.\n")
    w("docs/dev-skills/index.md", "# Docs index\n\n- issue-tracker.md, triage-labels.md, release.md, boundaries.md\n")
    kids = []
    for cid in case["children"]:
        c = dict(CHILDREN[cid]); c.update(case.get("child_overrides", {}).get(cid, {})); kids.append((cid, c))
    spec = ["# Spec: greeter", "", f"**Labels:** {', '.join(case['source_labels'])}", "", "A plain-text greeting formatter, proven in the agents it targets.", "", "## Approved breakdown", ""]
    for cid, c in kids:
        spec.append(f"{cid}. {c['title']} (regular tier)" + (f", blocked by {', '.join(c['blocked_by'])}" if c.get("blocked_by") else ""))
        spec += [f"   - {x}" for x in c["criteria"]]
    w(".scratch/greeter/SPEC.md", "\n".join(spec) + "\n")
    for cid, labels in case.get("preexisting", {}).items():
        c = CHILDREN[cid]
        w(f".scratch/greeter/issues/{cid}-{c['slug']}.md", child_text(cid, labels, case))
    prompt = ("Isolated fixture; the tracker is local files and the user has approved the concrete breakdown in `.scratch/greeter/SPEC.md` (every ticket regular tier). "
              "Run `to-tickets` on that Spec now: publish its tickets with the configured tracker and label mapping, then reply with the outcome the skill requires. "
              "No interview; no network calls. If a ticket cannot be published, say why and ask the one question the skill requires.")
    if case.get("preexisting"):
        prompt += " Tickets 01 and 02 were already filed by an earlier, interrupted run (see `.scratch/greeter/issues/`); resume the publication."
    w("PROMPT.md", prompt + "\n")
    w("REPORT.txt", "")  # the run saves its final reply here before scoring


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CASES:
        sys.exit("usage: make_fixture.py <out-dir> <" + "|".join(CASES) + ">")
    build(sys.argv[1], sys.argv[2])
