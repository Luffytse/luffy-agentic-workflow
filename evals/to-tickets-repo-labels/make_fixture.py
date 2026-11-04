#!/usr/bin/env python3
"""Build one case's scratch repo: python3 make_fixture.py <out-dir> <case>. Local-files tracker, no network, no real issue."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cases import CASES, CHILDREN, READY, TABLE


def write(out, rel, text):
    os.makedirs(os.path.dirname(os.path.join(out, rel)), exist_ok=True)
    open(os.path.join(out, rel), "w").write(text)


def triage_labels(table):
    text = ("# Triage labels\n\n| Role | Label |\n| --- | --- |\n| `ready-for-agent` | `ready-for-agent` |\n| `bug` | `bug` |\n"
            "| `enhancement` | `enhancement` |\n\n## Repo labels\n\nLabels this repo records for its own kinds of work, each with one line "
            "saying when it applies. They are not triage roles. An empty table means the repo has none.\n\n"
            "| Label in our tracker | When it applies |\n| -------------------- | --------------- |\n")
    if table:
        text += "".join(f"| `{lab}` | {when} |\n" for lab, when in TABLE.items())
    return text


def spec_text(case):
    spec = ["# Spec: order totals", "", f"**Labels:** {', '.join(case['source_labels'])}", "",
            "Orders show their total, from the API to the cart page, with a changelog line.", "", "## Approved breakdown", ""]
    for cid, c in CHILDREN.items():
        spec.append(f"{cid}. {c['title']} (regular tier)" + (f", blocked by {', '.join(c['blocked_by'])}" if c.get("blocked_by") else ""))
        spec += [f"   - {x}" for x in c["criteria"]]
    return "\n".join(spec) + "\n"


def prompt_text(case):
    text = ("Isolated fixture; the tracker is local files and the user has approved the concrete breakdown in `.scratch/orders/SPEC.md` (every ticket regular tier). "
            "Load `to-tickets` from `<checkout>/plugins/dev-skills/skills/to-tickets/SKILL.md` and any skill it names from `<checkout>/plugins/dev-skills/skills/<name>/SKILL.md`. Run it on that Spec now: publish its tickets with the configured tracker and label docs, then reply with the outcome the skill requires. "
            "No interview; no network calls.")
    if case["user_named"]:
        text += " The user named " + ", ".join(f"`{x}`" for x in case["source_labels"]) + " for this Spec when planning it, and the Spec carries it."
    return text + "\n"


def build(out, name):
    case = CASES[name]
    write(out, "docs/dev-skills/issue-tracker.md",
          "# Issue tracker: local files\n\nTickets are files under `.scratch/orders/issues/<NN>-<slug>.md`. A ticket file has a `**Labels:**` line listing its labels, comma-separated. "
          "A source Spec is `.scratch/orders/SPEC.md` with its own `**Labels:**` line. Blocking: a `**Blocked by:**` line of ticket numbers. No forge; no network.\n")
    write(out, "docs/dev-skills/triage-labels.md", triage_labels(case["table"]))
    write(out, "docs/dev-skills/release.md", "# Release\n\nRelease labels start with `release-`.\n")
    write(out, "docs/dev-skills/boundaries.md", "# Boundaries\n\nNothing needs the user's approval. Milestone label form: `milestone-<n>`.\n")
    write(out, "docs/dev-skills/index.md", "# Docs index\n\n- issue-tracker.md, triage-labels.md (with the Repo labels table), release.md, boundaries.md\n")
    write(out, ".scratch/orders/SPEC.md", spec_text(case))
    write(out, "PROMPT.md", prompt_text(case))
    os.makedirs(os.path.join(out, ".scratch/orders/issues"), exist_ok=True)


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CASES:
        sys.exit("usage: make_fixture.py <out-dir> <" + "|".join(CASES) + ">")
    build(sys.argv[1], sys.argv[2])
