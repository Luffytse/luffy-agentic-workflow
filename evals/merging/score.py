#!/usr/bin/env python3
"""Score a merging run: <out-dir>/repo/.scratch/proposed-actions.md and .scratch/report.md against the case's expectation.

Usage: score.py <out-dir> <case>
Prints one line per check (PASS, or FAIL with what it saw) and exits 1 when any check fails. See
evals/merging/README.md. It reads what the run would have done (the dry-run blocks, in order) and what it told the
user, never the skill's text.
"""
import json
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from cases import EXPECT, NEXT_VERSION  # noqa: E402
from make_fixture import tree_hash  # noqa: E402

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
        line = lambda k: (re.search(rf"^{k}:[ \t]*(.*)$", rest, re.M) or [None, ""])[1].strip()  # noqa: E731
        files = {f.group(1).strip(): f.group(2) for f in re.finditer(r"^File:\s*(\S+)\s*\n~~~\n(.*?)\n~~~", rest, re.S | re.M)}
        blocks.append(dict(op=m.group(2).strip().lower(), issue=line("Issue"), pull=line("Pull"), method=line("Method").lower(),
                           title=line("Title"), branch=line("Branch"), outcome=line("Outcome").lower(), reason=line("Reason"),
                           body=fenced(rest, "Body"), message=fenced(rest, "Message"), question=fenced(rest, "Question"),
                           files=files, raw=rest))
    return blocks


def first(blocks, op, pred=lambda b: True):
    for i, b in enumerate(blocks):
        if b["op"] == op and pred(b):
            return i
    return None


def score(out, case):
    out = pathlib.Path(out)
    repo = out / "repo"
    fx = json.loads((out / "fixture.json").read_text())
    exp = EXPECT[case]
    actions = repo / ".scratch/proposed-actions.md"
    blocks = parse(actions.read_text()) if actions.exists() else []
    report = (repo / ".scratch/report.md").read_text() if (repo / ".scratch/report.md").exists() else ""
    low = report.lower()

    rev = lambda ref: subprocess.run(["git", "-C", str(repo), "rev-parse", ref], capture_output=True, text=True).stdout.strip()  # noqa: E731
    check("dry run: main and ticket-10 unchanged in git", rev("main") == fx["main"] and rev("ticket-10") == fx["branch"])
    check("dry run: no file outside the two dry-run files changed", tree_hash(repo) == fx["tree"])
    check("the run wrote a report", report.strip() != "")

    merges = [i for i, b in enumerate(blocks) if b["op"] == "merge a pr"]
    closes = [i for i, b in enumerate(blocks) if b["op"] == "close"]
    if exp["merge"]:
        check("merged once", len(merges) == 1, f"{len(merges)} merge blocks")
        if merges:
            m = blocks[merges[0]]
            check("merge: pull request 1, squash", m["pull"].lstrip("#") == "1" and m["method"] == "squash", f"{m['pull']} {m['method']}")
            check("merge: titled with the pull request's typed title", m["title"].strip("`'\" ") == fx["title"], m["title"])
            check("merge: the commit message is the pull request's body", fx["marker"] in m["message"] and "Closes #10" in m["message"])
            after = [i for i in closes if i > merges[0] and re.search(r"(^|\D)10(\D|$)", blocks[i]["issue"])]
            check("issue #10 closed after the merge, as completed, naming the pull request",
                  bool(after) and blocks[after[0]]["outcome"].startswith("completed") and re.search(r"(#1\b|pull request 1|PR 1|pulls/1)", blocks[after[0]]["reason"], re.I),
                  "; ".join(f"{blocks[i]['issue']} {blocks[i]['outcome']} {blocks[i]['reason']}" for i in closes) or "no close")
            check("nothing closed before the merge", not [i for i in closes if i < merges[0]])
        edits = [i for i, b in enumerate(blocks) if b["op"] == "edit a pull request body"]
        rules = [i for i in edits if re.search(r"^\W*Agent-merged rules:", blocks[i]["body"], re.M)]
        if exp["rules_line"]:
            ok = bool(rules) and merges and rules[0] < merges[0] and re.search(r"^\W*Agent-merged rules:.*REVIEW\.md", blocks[rules[0]]["body"], re.M)
            check("an `Agent-merged rules:` line naming REVIEW.md is added to the body before the merge", ok)
            check("the squash message carries the edited body's `Agent-merged rules:` line", bool(merges) and "Agent-merged rules:" in blocks[merges[0]]["message"])
            check("the report names REVIEW.md", "review.md" in low)
        else:
            check("no `Agent-merged rules:` line (no rules file, no design answer)", not rules and not (merges and "Agent-merged rules:" in blocks[merges[0]]["message"]))
        if exp.get("closes_edit"):
            has = lambda b: re.search(r"^\W*Closes #10\b", b["body"], re.M)  # noqa: E731
            ce = [i for i in edits if has(blocks[i])]
            check("the body gets a `Closes #10` line, by a body edit before the merge", bool(ce) and bool(merges) and ce[0] < merges[0])
            check("the squash message carries the edited body's `Closes #10` line", bool(merges) and bool(re.search(r"^\W*Closes #10\b", blocks[merges[0]]["message"], re.M)))
        version_commits = [i for i, b in enumerate(blocks) if b["op"] == "commit to a branch" and "VERSION" in b["files"]]
        asks = [i for i, b in enumerate(blocks) if b["op"] == "ask the coordinator" and "version" in (b["question"] + b["raw"]).lower()]
        if exp["bump"]:
            check("asked the coordinator for the version number", bool(asks))
            check("one bump commit", len(version_commits) == 1, f"{len(version_commits)}")
            if version_commits and merges:
                vc = blocks[version_commits[0]]
                check("bump commit: on ticket-10, by the Implementer", vc["branch"] == "ticket-10" and "implementer" in vc["raw"].lower(), f"{vc['branch']}")
                check(f"bump commit: changes only VERSION, to {NEXT_VERSION}", list(vc["files"]) == ["VERSION"] and vc["files"]["VERSION"].strip() == NEXT_VERSION, f"{list(vc['files'])}")
                check("order: number asked, then the bump commit, then the merge", bool(asks) and asks[0] < version_commits[0] < merges[0])
                later = [i for i, b in enumerate(blocks) if b["op"] == "commit to a branch" and version_commits[0] < i < merges[0]]
                check("the bump is the last commit of the pull request's own work", not later)
        else:
            check("no bump: no version asked for, no commit changing VERSION", not asks and not version_commits)
    else:
        check("not merged", not merges, f"{len(merges)} merge blocks")
        check("nothing closed", not closes)
        for phrase in exp.get("names", []):
            check(f"the message to the user names the boundary \"{phrase}\"", re.search(phrase.replace("delete", r"delet\w*", 1), low) is not None)
        if exp.get("not_merged"):
            check("the message to the user says the pull request is not merged",
                  re.search(r"(not|n't|never|isn't|hasn't)\b[^.\n]{0,60}\bmerged|still (open|unmerged)|unmerged|state: open", low) is not None)
    return all(results)


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in EXPECT:
        sys.exit(f"usage: score.py <out-dir> <{'|'.join(EXPECT)}>")
    sys.exit(0 if score(sys.argv[1], sys.argv[2]) else 1)
