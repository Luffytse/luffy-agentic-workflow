#!/usr/bin/env python3
"""Build one case's scratch repo: python3 make_fixture.py <out-dir> <case>. Local-files tracker, no network, no real issue."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cases import CASES, ITEMS


def item(cid, case):
    c = dict(ITEMS[cid]); c.update(case["overrides"].get(cid, {})); return c


def ticket_text(cid, case):
    c = item(cid, case)
    return "\n".join([f"# {cid}: {c['title']}", "", "**Labels:** ready-for-agent", ""] + [f"- [ ] {x}" for x in c["criteria"]] + [""])


def build(out, name):
    case = CASES[name]
    w = lambda rel, text: (os.makedirs(os.path.dirname(os.path.join(out, rel)), exist_ok=True), open(os.path.join(out, rel), "w").write(text))
    w("docs/dev-skills/issue-tracker.md",
      "# Issue tracker: local files\n\nTickets are files under `.scratch/greeter/issues/<NN>-<slug>.md`. A ticket file has a `**Labels:**` line listing its labels, comma-separated. "
      "A source Spec is `.scratch/greeter/SPEC.md`. Blocking: a `**Blocked by:**` line of ticket numbers, omitted when a ticket has no blocker. No forge; no network.\n")
    w("docs/dev-skills/triage-labels.md", "# Triage labels\n\n| Role | Label |\n| --- | --- |\n| `ready-for-agent` | `ready-for-agent` |\n| `bug` | `bug` |\n| `enhancement` | `enhancement` |\n")
    w("docs/dev-skills/release.md", "# Release\n\nRelease labels start with `release-`.\n")
    w("docs/dev-skills/boundaries.md", "# Boundaries\n\nNothing needs the user's approval. Milestone label form: `milestone-<n>`.\n")
    w("docs/dev-skills/index.md", "# Docs index\n\n- issue-tracker.md, triage-labels.md, release.md, boundaries.md, glossary.md\n")
    w("docs/dev-skills/glossary.md",
      "# Glossary\n\n**Greeting**: the text the formatter returns for a name.\n\n**History**: the file of greetings recorded so far.\n\n**Loud log**: the file of shouted greetings.\n")
    spec = ["# Spec: greeter", "", "A plain-text greeting tool. Features are wanted, each its own change.", "", "## Work items", ""]
    for cid in case["items"]:
        c = item(cid, case)
        spec.append(f"{cid}. {c['title']} (regular tier)")
        spec += [f"   - {x}" for x in c["criteria"]]
        spec.append(f"   - Code: `{c['code']}`." + (f" Calls item {c['needs']}'s shout option, so it cannot be built or checked without it." if c.get("needs") else ""))
        spec.append(f"   - Docs: rewrite the glossary entry `{c['entry']}` to say {c['doc']}.")
    w(".scratch/greeter/SPEC.md", "\n".join(spec) + "\n")
    for cid in case.get("preexisting", []):
        w(f".scratch/greeter/issues/{cid}-{ITEMS[cid]['slug']}.md", ticket_text(cid, case))
    prompt = ("Isolated fixture; the tracker is local files. The user has approved turning the work items in `.scratch/greeter/SPEC.md` into tickets (every ticket regular tier) "
              "and leaves how they are grouped and ordered to the skill's rules. Run `to-tickets` on that Spec now: publish its tickets with the configured tracker, then reply with the outcome. "
              "No interview; no network calls.")
    if case.get("preexisting"):
        prompt += " Ticket 01 was already filed by an earlier, interrupted run (see `.scratch/greeter/issues/`); resume the publication."
    w("PROMPT.md", prompt + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CASES:
        sys.exit("usage: make_fixture.py <out-dir> <" + "|".join(CASES) + ">")
    build(sys.argv[1], sys.argv[2])
