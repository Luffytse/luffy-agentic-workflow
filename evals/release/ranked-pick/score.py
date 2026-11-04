#!/usr/bin/env python3
"""Score a release ranked-pick run: <out-dir>/repo/.scratch/proposed-actions.md against the case's expected pick.

Usage: score.py <out-dir> <case>
Prints one line per check (PASS or FAIL with what it saw) and exits 1 when any check fails. See
evals/release/README.md. The checks read the release issue the run opens for "Release 3" (its Order, Left out,
Proposed to the user and Size), the label writes, and, in the cut case, the changelog pull request and the order of
the cut, close and end-of-Release blocks.
"""
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from cases import EXPECT  # noqa: E402

NEXT, NEXT_LABEL = "Release 3", "release-3"
results = []


def check(name, ok, seen=""):
    results.append(bool(ok))
    print(("PASS " if ok else "FAIL ") + name + ("" if ok or seen == "" else f": {seen}"))


def fenced(rest, field):
    m = re.search(rf"^{field}:\s*\n~~~\n(.*?)\n~~~", rest, re.S | re.M)
    return m.group(1) if m else ""


def parse(text):
    blocks = []
    for m in re.finditer(r"^### (\d+)\. (.+?)\n(.*?)(?=^### \d+\. |\Z)", text, re.S | re.M):
        rest = m.group(3)
        files = {f.group(1).strip(): f.group(2) for f in re.finditer(r"^File:\s*(\S+)\s*\n~~~\n(.*?)\n~~~", rest, re.S | re.M)}
        line = lambda k: (re.search(rf"^{k}:\s*(.*)$", rest, re.M) or [None, ""])[1].strip()  # noqa: E731
        issue = line("Issue")
        num = re.match(r"(?:#)?(\d+)", issue.replace("new (", ""))
        blocks.append(dict(k=int(m.group(1)), op=m.group(2).strip().lower(), issue=issue,
                           n=int(num.group(1)) if num and not issue.startswith("new") else None,
                           title=line("Title"), add=line("Add"), remove=line("Remove"), label=line("Label"),
                           skill=line("Skill"), pull=line("Pull"), body=fenced(rest, "Body"), files=files, raw=rest))
    return blocks


def section(body, heading):
    m = re.search(rf"^## {heading}\s*\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1) if m else ""


def refs(text, numbered):
    pat = r"^\s*\d+\.\s+(.*)$" if numbered else r"^\s*-\s+(.*)$"
    out = []
    for line in re.findall(pat, text, re.M):
        m = re.search(r"#(\d+)", line)
        if m:
            out.append((int(m.group(1)), line))
    return out


def labels_split(v):
    return {x.strip() for x in v.split(",") if x.strip() and x.strip().lower() != "none"}


def main(out, case):
    exp = EXPECT[case]
    repo = pathlib.Path(out) / "repo"
    actions = repo / ".scratch/proposed-actions.md"
    blocks = parse(actions.read_text() if actions.exists() else "")
    report = (repo / ".scratch/report.md").read_text() if (repo / ".scratch/report.md").exists() else ""

    created = [b for b in blocks if b["op"].startswith("create an issue") and b["title"].strip() == NEXT]
    check("one release issue opened, titled Release 3", len(created) == 1, f"{len(created)} found")
    body = created[0]["body"] if created else ""
    order = refs(section(body, "Order"), numbered=True)
    got_order = [n for n, _ in order]
    check("Order lists the expected ranked pick, in order", got_order == exp["order"], f"saw {got_order}, want {exp['order']}")
    if exp.get("reasons", True):
        thin = [n for n, line in order if len(re.sub(r"^.*?#\d+", "", line).split()) < 4]
        check("every Order entry has a line of reason", order and not thin, f"thin: {thin}")

    added = {b["n"] for b in blocks if b["op"].startswith("apply") and NEXT_LABEL in labels_split(b["add"])}
    check(f"{NEXT_LABEL} applied to exactly the taken issues", added == exp["labelled"],
          f"saw {sorted(added)}, want {sorted(exp['labelled'])}")
    label_made = any(b["op"].startswith("create a label") and b["label"].strip("` ") == NEXT_LABEL for b in blocks)
    check(f"{NEXT_LABEL} created", label_made)

    left = {n for n, _ in refs(section(body, "Left out"), numbered=False)}
    check("Left out names every ranked candidate not taken", exp["left_out"] <= left, f"saw {sorted(left)}")
    check("nothing taken is listed as left out", not (left & added), f"both: {sorted(left & added)}")
    if exp["not_ranked"]:
        hit = exp["not_ranked"] & (set(got_order) | left | added)
        check("never ranked: not in Order, Left out or labelled", not hit, f"ranked: {sorted(hit)}")
    for n in exp.get("proposed", set()):
        proposed = {m for m, _ in refs(section(body, "Proposed to the user"), numbered=False)}
        check(f"#{n} proposed to the user", n in proposed or re.search(rf"#{n}\b", report), "")

    cleared = {b["n"] for b in blocks if b["op"].startswith("apply") and "next-release" in labels_split(b["remove"])}
    check("next-release removed from exactly the taken marked issues", cleared == exp["cleared"],
          f"saw {sorted(cleared)}, want {sorted(exp['cleared'])}")

    size = re.search(r"\*\*Size:\*\*\s*(\d+)\.\s*Used:\s*(\d+)(.*)$", body, re.M)
    check("Size line gives the size and the items used", size and int(size.group(2)) == exp["used"],
          size.group(0) if size else "no **Size:** line")
    if exp.get("past"):
        past = re.search(r"(\d+)\s+severe", size.group(3)) if size else None
        check("Size line counts the severe issues past the size", past and int(past.group(1)) == exp["past"],
              size.group(0) if size else "")
    if "cut" in exp:
        cut_checks(repo, blocks, exp["cut"], created)
    print(f"{sum(results)}/{len(results)} checks passed")
    return 0 if all(results) else 1


def cut_checks(repo, blocks, cut, created):
    git = lambda *a: subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True).stdout.strip()  # noqa: E731
    start = git("log", "-1", "--format=%h", "--abbrev=7", "--grep", r"(#5)", "--fixed-strings")
    end = git("rev-parse", "--short=7", "HEAD")
    prs = [b for b in blocks if b["op"].startswith(("open a pull request", "update a pull request"))]
    log = next((b["files"][f] for b in reversed(prs) for f in b["files"] if f.endswith("CHANGELOG.md")), "")
    check("a changelog pull request writes CHANGELOG.md", bool(log))
    others = sorted({f for b in prs for f in b["files"] if not f.endswith("CHANGELOG.md")})
    check("the changelog pull request changes no other file (no version file)", not others, f"also: {others}")
    entry = log.split(f"## {cut['name']}", 1)[1].split("\n## ", 1)[0] if f"## {cut['name']}" in log else ""
    check(f"entry headed ## {cut['name']}", bool(entry))
    m = re.search(r"Commits:\s*([0-9a-f]{7,40})\.\.([0-9a-f]{7,40})", entry)
    ok = m and start.startswith(m.group(1)[:7]) and end.startswith(m.group(2)[:7])
    check("Commits line gives the start and end commits", ok, f"saw {m.group(0) if m else None}, want {start}..{end}")
    check("no Versions line (the repo keeps no version)", not re.search(r"^\s*Versions:", entry, re.M))
    for n in cut["shipped"]:
        check(f"#{n} listed as shipped", re.search(rf"^- .*#{n}\b", entry, re.M))
    for n in cut["also_merged"]:
        check(f"#{n} under Also merged", re.search(rf"Also merged.*#{n}\b", entry, re.S))
    check("old entry kept below", "## Release 1" in log)
    k = lambda pred: next((b["k"] for b in blocks if pred(b)), None)  # noqa: E731
    k_pr = k(lambda b: b["op"].startswith("open a pull request"))
    k_merge = k(lambda b: b["op"].startswith("merge a pull request"))
    k_notes = k(lambda b: b["op"].startswith("comment") and b["n"] == 2 and f"## {cut['name']}" in b["body"])
    k_close = k(lambda b: b["op"].startswith("close") and b["n"] == 2)
    k_triage = k(lambda b: b["op"].startswith("run a skill") and "triage" == b["skill"].strip("` "))
    k_retro = k(lambda b: b["op"].startswith("run a skill") and "retro-planning" == b["skill"].strip("` "))
    k_plan = created[0]["k"] if created else None
    recs = [b for b in blocks if b["op"].startswith("comment") and b["n"] == 2
            and "<!-- release end-of-Release pass -->" in b["body"]]
    check("an end-of-Release record for triage and one for retro-planning",
          any("triage" in b["body"].split("-->", 1)[1] for b in recs)
          and any("retro-planning" in b["body"] for b in recs), f"{len(recs)} records")
    seq = [k_pr, k_merge, k_notes, k_close, k_triage, k_retro, k_plan]
    check("cut order: pull request, merge, notes, close, triage, retro-planning, plan",
          None not in seq and seq == sorted(seq), f"block numbers {seq}")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in EXPECT:
        sys.exit(f"usage: score.py <out-dir> <{'|'.join(EXPECT)}>")
    sys.exit(main(sys.argv[1], sys.argv[2]))
