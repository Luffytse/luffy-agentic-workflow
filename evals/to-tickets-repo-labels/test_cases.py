#!/usr/bin/env python3
"""Self-test: a reference run per case passes, planted wrong runs fail, and the RENDERED fixture (the Spec, the triage-labels
doc and the prompt a session reads) says what each case means. It reads no skill or doc text: rewording must not fail it.
Run: python3 evals/to-tickets-repo-labels/test_cases.py"""
import os, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from cases import CASES, CHILDREN, TABLE
from make_fixture import build
from score import score

fails = []


def ticket(cid, labels):
    c = CHILDREN[cid]
    blocked = f"**Blocked by:** {', '.join(c['blocked_by'])}\n\n" if c.get("blocked_by") else ""
    return f"# {cid}: {c['title']}\n\n**Labels:** {', '.join(labels)}\n\n{blocked}" + "\n".join(f"- [ ] {x}" for x in c["criteria"]) + "\n"


def run(name, mutate=None, source=None):
    with tempfile.TemporaryDirectory() as out:
        build(out, name)
        labels = {k: list(v) for k, v in CASES[name]["expect"].items()}
        if mutate:
            mutate(labels)
        d = os.path.join(out, ".scratch/orders/issues")
        for cid, labs in labels.items():
            open(os.path.join(d, f"{cid}-{CHILDREN[cid]['slug']}.md"), "w").write(ticket(cid, labs))
        if source is not None:
            p = os.path.join(out, ".scratch/orders/SPEC.md")
            open(p, "w").write(open(p).read().replace("**Labels:** " + ", ".join(CASES[name]["source_labels"]), "**Labels:** " + source))
        return score(out, name)


def expect(label, got, must_fail):
    if bool(got) != must_fail:
        fails.append(f"{label}: score gave {got or 'PASS'}")


for n in CASES:
    expect(f"reference {n} passes", run(n), False)

R = "ready-for-agent"
expect("split: UI ticket also gets backend", run("split", lambda l: l.update({"02": [R, "frontend", "backend"]})), True)
expect("split: Spec's kind copied by guess onto the API ticket as frontend", run("split", lambda l: l.update({"01": [R, "frontend"]})), True)
expect("split: changelog ticket labelled", run("split", lambda l: l.update({"03": [R, "backend"]})), True)
expect("split: UI ticket unlabelled", run("split", lambda l: l.update({"02": [R]})), True)
expect("split: unlisted label applied", run("split", lambda l: l.update({"01": [R, "backend", "docs"]})), True)
expect("named: label missing from the UI ticket", run("named", lambda l: l.update({"02": [R, "frontend"]})), True)
expect("named: label missing from the changelog ticket", run("named", lambda l: l.update({"03": [R]})), True)
expect("named: UI ticket loses its own frontend", run("named", lambda l: l.update({"02": [R, "backend"]})), True)
expect("named: Spec label removed", run("named", source=""), True)
expect("no-table: a repo label applied", run("no-table", lambda l: l.update({"01": [R, "backend"]})), True)

# The rendered input must say what the case means.
for n, case in CASES.items():
    with tempfile.TemporaryDirectory() as out:
        build(out, n)
        doc = open(os.path.join(out, "docs/dev-skills/triage-labels.md")).read()
        spec = open(os.path.join(out, ".scratch/orders/SPEC.md")).read()
        prompt = open(os.path.join(out, "PROMPT.md")).read()
        if "<checkout>/plugins/dev-skills/skills/to-tickets/SKILL.md" not in prompt or "<checkout>/plugins/dev-skills/skills/<name>/SKILL.md" not in prompt:
            fails.append(f"{n}: prompt does not say where to load to-tickets and the skills it names from")
        rows = [l for l in doc.splitlines() if l.startswith("| `frontend`") or l.startswith("| `backend`")]
        if len(rows) != (len(TABLE) if case["table"] else 0):
            fails.append(f"{n}: triage-labels doc holds {len(rows)} repo label rows")
        if "## Repo labels" not in doc:
            fails.append(f"{n}: triage-labels doc has no Repo labels section")
        spec_labels = [l for l in spec.splitlines() if l.startswith("**Labels:**")][0]
        for lab in ("frontend", "backend"):
            if (lab in spec_labels) != (lab in case["source_labels"]):
                fails.append(f"{n}: Spec label line {spec_labels!r} does not match source_labels")
        if case["user_named"] != ("named" in prompt and "`backend`" in prompt):
            fails.append(f"{n}: prompt does not say whether the user named the label")
        if "ui/cart.html" not in spec or "api/orders.py" not in spec:
            fails.append(f"{n}: Spec does not name the UI file and the API file its tickets work in")
        if "frontend" in spec.split("## Approved breakdown")[1] or "backend" in spec.split("## Approved breakdown")[1]:
            fails.append(f"{n}: the breakdown names a label, giving the answer away")
        # Ticket 01 is API work only, 02 UI work only, 03 neither.
        if "ui/" in "".join(CHILDREN["01"]["criteria"]) or "api/" in "".join(CHILDREN["02"]["criteria"]) or any(
                x in "".join(CHILDREN["03"]["criteria"]) for x in ("ui/", "api/")):
            fails.append(f"{n}: a ticket's criteria name the wrong layer")

print("\n".join(fails) if fails else "ok")
sys.exit(1 if fails else 0)
