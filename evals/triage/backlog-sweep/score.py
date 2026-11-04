#!/usr/bin/env python3
"""Score a triage backlog-sweep run: <out-dir>/repo/.scratch/proposed-actions.md against the case's expected outcome.

Usage: score.py <out-dir>
Prints one line per check (PASS or FAIL with what it saw) and exits 1 when any check fails. See
evals/triage/README.md. The checks read the run's Close, Apply / remove labels and Comment on an issue blocks: which
issues close and how, which gain `next-release` or `ready-for-human`, the `## Triage batch` summary on the release
issue, and the triage disclaimer on every comment.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from sweep_case import DISCLAIMER, EXPECT  # noqa: E402

results = []


def check(name, ok, seen=""):
    results.append(bool(ok))
    print(("PASS " if ok else "FAIL ") + name + ("" if ok or seen == "" else f": {seen}"))


def fenced(rest, field):
    m = re.search(rf"^{field}:\s*\n~~~\n(.*?)\n~~~", rest, re.S | re.M)
    return m.group(1) if m else ""


def number(issue):
    if issue.lower().startswith("new"):
        return None
    m = re.search(r"(?:^|/|#)0*(\d+)(?:-|\b)", issue)
    return int(m.group(1)) if m else None


def parse(text):
    blocks = []
    for m in re.finditer(r"^### (\d+)\. (.+?)\n(.*?)(?=^### \d+\. |\Z)", text, re.S | re.M):
        rest = m.group(3)
        line = lambda k: (re.search(rf"^{k}:\s*(.*)$", rest, re.M) or [None, ""])[1].strip()  # noqa: E731
        blocks.append(dict(k=int(m.group(1)), op=m.group(2).strip().lower(), n=number(line("Issue")),
                           add=line("Add"), remove=line("Remove"), label=line("Label"), outcome=line("Outcome").lower(),
                           reason=line("Reason"), body=fenced(rest, "Body")))
    return blocks


def labels_split(v):
    return {x.strip().strip("`") for x in v.split(",") if x.strip() and x.strip().lower() != "none"}


def main(out):
    e = EXPECT
    repo = pathlib.Path(out) / "repo"
    actions = repo / ".scratch/proposed-actions.md"
    blocks = parse(actions.read_text() if actions.exists() else "")
    closes = {b["n"]: b for b in blocks if b["op"].startswith("close")}
    comments = [b for b in blocks if b["op"].startswith("comment")]
    said = lambda n: " ".join([closes[n]["reason"]] if n in closes else []  # noqa: E731
                              + [b["body"] for b in comments if b["n"] == n])
    added = lambda label: {b["n"] for b in blocks if b["op"].startswith("apply") and label in labels_split(b["add"])}  # noqa: E731
    removed = lambda label: {b["n"] for b in blocks if b["op"].startswith("apply") and label in labels_split(b["remove"])}  # noqa: E731

    d, k = e["duplicate"], e["kept"]
    check(f"duplicate #{d} closed as a duplicate or not planned",
          d in closes and closes[d]["outcome"] in ("duplicate", "not planned"), closes.get(d, {}).get("outcome", "not closed"))
    check(f"duplicate #{d}'s close links the kept issue #{k}", re.search(rf"#{k}\b", said(d)), said(d)[:120])

    o = e["obsolete"]
    check(f"obsolete #{o} closed", o in closes)
    check(f"obsolete #{o}'s close gives the reason", len(said(o).split()) >= 6, said(o)[:120])

    x = e["expired"]
    check(f"#{x}, left out of 3 Releases in a row, closed as not planned",
          x in closes and closes[x]["outcome"] == "not planned", closes.get(x, {}).get("outcome", "not closed"))
    check(f"#{x}'s close says reopen to bring it back", re.search(r"reopen to bring it back", said(x), re.I),
          said(x)[:120])

    wrongly = sorted(e["stay_open"] & set(closes))
    check("no other issue closed (left out twice, not in a row, planned feature, enhancements, marked)",
          not wrongly, f"closed: {wrongly}")

    marked = added("next-release")
    check("next-release set on exactly the severe issue and the feature-blocker", marked == e["next_release"],
          f"saw {sorted(marked)}, want {sorted(e['next_release'])}")
    for n in e["ready_for_agent_added"]:
        check(f"#{n} triaged to ready-for-agent", n in added("ready-for-agent"))
    human = added("ready-for-human")
    check("each agent-found enhancement sent to ready-for-human", e["to_human"] <= human, f"saw {sorted(human)}")
    check("no agent-found enhancement put at ready-for-agent", not (e["to_human"] & added("ready-for-agent")),
          f"added to: {sorted(e['to_human'] & added('ready-for-agent'))}")
    check("ready-for-agent removed from the agent-found enhancement that had it",
          e["off_ready_for_agent"] <= removed("ready-for-agent"), f"removed from: {sorted(removed('ready-for-agent'))}")

    rel_labels = sorted({lab for b in blocks if b["op"].startswith(("apply", "create a label"))
                         for lab in labels_split(b["add"]) | labels_split(b["label"]) if lab.startswith("release-")})
    check("no release label applied or created (Release planning owns them)", not rel_labels, f"saw {rel_labels}")

    r = e["release_issue"]
    summary = [b for b in comments if b["n"] == r and re.search(r"^## Triage batch\s*$", b["body"], re.M)]
    check(f"one ## Triage batch summary on release issue #{r}", len(summary) == 1, f"{len(summary)} found")
    text = summary[0]["body"] if summary else ""
    missing = sorted(n for n in e["summary_names"] if not re.search(rf"#{n}\b", text))
    check("the summary lists every issue the batch decided", not missing, f"missing: {missing}")

    bare = sorted({b["n"] for b in comments if not b["body"].lstrip().startswith(DISCLAIMER)})
    check("every comment starts with the triage disclaimer", comments and not bare, f"without it: {bare}")
    print(f"{sum(results)}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: score.py <out-dir>")
    sys.exit(main(sys.argv[1]))
