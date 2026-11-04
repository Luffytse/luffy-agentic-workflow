#!/usr/bin/env python3
"""Score a release main-check run: <out-dir>/repo/.scratch/proposed-actions.md against the case's expected outcome.

Usage: score.py <out-dir>
Prints one line per check (PASS or FAIL with what it saw) and exits 1 when any check fails. See
evals/release/README.md. The checks read the "Release 3" issue the run opens (its Order and its
"## Checked against main" section), the close, edit and label blocks, their order, and .scratch/report.md.
"""
import importlib.util
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from main_case import EXPECT, ISSUES, PULLS  # noqa: E402

_spec = importlib.util.spec_from_file_location("release_ranked_pick_score", HERE.parent / "ranked-pick/score.py")
rp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rp)

NEXT, NEXT_LABEL = "Release 3", "release-3"
VERDICTS = ["still valid", "already fixed", "changed scope", "obsolete", "cannot tell"]
results = []


def check(name, ok, seen=""):
    results.append(bool(ok))
    print(("PASS " if ok else "FAIL ") + name + ("" if ok or seen == "" else f": {seen}"))


def issue_no(b):
    """The issue a block names: "30-usage-typo.md", "#30", "30" or a path ending in the file; None for a new issue
    or a pull request."""
    if b["issue"].startswith("new") or "PR" in b["issue"]:
        return None
    m = re.match(r"\s*#?(\d+)", b["issue"].rsplit("/", 1)[-1])
    return int(m.group(1)) if m else None


def rows(section):
    """{issue: (verdict, rest of the line after the verdict)} from the section's list lines."""
    out = {}
    for line in re.findall(r"^\s*(?:[-*]|\d+\.)\s+(.*)$", section, re.M):
        m = re.search(r"#(\d+)", line)
        if not m:
            continue
        tail = line[m.end():].lower()
        hits = sorted((tail.find(v), v) for v in VERDICTS if v in tail)
        verdict = hits[0][1] if hits else None
        rest = tail[hits[0][0] + len(verdict):] if hits else tail
        out[int(m.group(1))] = (verdict, rest)
    return out


def names_evidence(text, marks, shas):
    t = text.lower()
    return any(re.search(re.escape(m.lower()) + (r"\b" if m.startswith("#") else ""), t) for m in marks) or \
        any(s and s[:7] in t for s in shas)


def main(out):
    repo = pathlib.Path(out) / "repo"
    actions = repo / ".scratch/proposed-actions.md"
    blocks = rp.parse(actions.read_text() if actions.exists() else "")
    for b in blocks:
        b["n"] = issue_no(b)
    report = (repo / ".scratch/report.md").read_text() if (repo / ".scratch/report.md").exists() else ""
    git = lambda *a: subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True).stdout.strip()  # noqa: E731
    shas = {p["n"]: git("log", "-1", "--format=%h", "--abbrev=7", "--fixed-strings", "--grep", f"(#{p['n']})") for p in PULLS}
    sha_for = lambda marks: [shas[int(m[1:])] for m in marks if m.startswith("#")]  # noqa: E731

    created = [b for b in blocks if b["op"].startswith("create an issue") and b["title"].strip() == NEXT]
    check("one release issue opened, titled Release 3", len(created) == 1, f"{len(created)} found")
    body = created[0]["body"] if created else ""
    k_plan = created[0]["k"] if created else None
    own = re.search(r"\((\d+)", created[0]["issue"]) if created else None
    own = int(own.group(1)) if own else None  # the release issue's own later edits are not the check's
    later = [b for b in blocks if own and b["op"].startswith("edit an issue") and b["n"] == own]
    if later:
        body = later[-1]["body"]  # the release issue as its last whole-body edit leaves it

    section = rp.section(body, "Checked against main")
    check("the release issue has a ## Checked against main section", re.search(r"^## Checked against main\s*$", body, re.M))
    heads = re.findall(r"^## (.+?)\s*$", body, re.M)
    check("the section comes right after ## Left out",
          "Left out" in heads and "Checked against main" in heads
          and heads.index("Checked against main") == heads.index("Left out") + 1, f"headings {heads}")
    got = rows(section)
    for n, want in EXPECT["verdicts"].items():
        v = got.get(n, (None, ""))[0]
        check(f"#{n} verdict is {' or '.join(sorted(want))}", v in want, f"saw {v!r}")
    for n, marks in EXPECT["evidence"].items():
        rest = got.get(n, (None, ""))[1]
        check(f"#{n} row gives its evidence on main", names_evidence(rest, marks, sha_for(marks)), f"saw {rest.strip()!r}")
    for n in EXPECT["unchecked"]:
        rest = got.get(n, (None, ""))[1]
        check(f"#{n} row says what is missing", len(re.findall(r"[a-z]+", rest)) >= 3, f"saw {rest.strip()!r}")
    for n in EXPECT["untouched"]:
        check(f"#{n} (left to the next Milestone) has no row: it is out of the check", n not in got)
    extra = set(got) - set(EXPECT["verdicts"]) - EXPECT["untouched"]
    check("no row for an issue outside the check's scope", not extra, f"extra rows {sorted(extra)}")

    closes = {b["n"]: b for b in blocks if b["op"].startswith("close") and b["n"] != own}
    check("closed exactly the already-fixed and obsolete issues that are not planned features",
          set(closes) == EXPECT["closed"], f"saw {sorted(closes)}, want {sorted(EXPECT['closed'])}")
    for n in EXPECT["closed"]:
        b = closes.get(n)
        reason = (b["raw"] if b else "") + "".join(c["body"] for c in blocks if c["op"].startswith("comment") and c["n"] == n)
        check(f"#{n} closed as not planned", b and re.search(r"^Outcome:\s*not planned", b["raw"], re.M | re.I),
              b["raw"].strip() if b else "no close")
        marks = EXPECT["evidence"][n]
        check(f"#{n} close names where on main", names_evidence(reason, marks, sha_for(marks)), reason.strip()[:120])
    for n in EXPECT["asked"]:
        check(f"#{n} (a planned feature main already does) is not closed", n not in closes)
        check(f"#{n} goes to the user (named in the report)", re.search(rf"#{n}\b", report), "report does not name it")
        asked = [c for c in blocks if c["op"].startswith("comment") and c["n"] == n
                 and c["body"].lstrip().startswith("Checked against main:")]
        check(f"#{n} carries the question as a comment starting `Checked against main:`", asked,
              "no such comment block")

    edits = {b["n"]: b for b in blocks if b["op"].startswith("edit an issue") and b["n"] != own}
    check("edited exactly the changed-scope issue", set(edits) == EXPECT["edited"],
          f"saw {sorted(edits)}, want {sorted(EXPECT['edited'])}")
    for n in EXPECT["edited"]:
        new = edits[n]["body"] if n in edits else ""
        old = next(i["body"] for i in ISSUES if i["n"] == n)
        check(f"#{n} new body keeps the part still true on main (bye)", "bye" in new and "Goodbye, Ada!" in new, new[:120])
        check(f"#{n} new body is written whole (keeps the rest of the old body)", "Each should print the whole name" in new
              or len(new) >= len(old) // 2, new[:120])
        check(f"#{n} new body carries a note naming main's change", names_evidence(new, ["#9"], sha_for(["#9"]))
              or re.search(r"\bmain\b", new, re.I), new[-160:])

    for n in EXPECT["untouched"]:
        hit = [b["k"] for b in blocks if b["n"] == n]
        check(f"#{n} (left to the next Milestone) is untouched: no write names it", not hit, f"blocks {hit}")

    writes = [b["k"] for b in blocks if b["n"] in (set(closes) | set(edits))
              and b["op"].startswith(("close", "edit an issue"))]
    check("the check's closes and edits come before the release issue is opened",
          k_plan is not None and writes and max(writes) < k_plan, f"writes {writes}, release issue {k_plan}")

    order = [n for n, _ in rp.refs(rp.section(body, "Order"), numbered=True)]
    check("Order ranks only issues that survived the check", order == EXPECT["order"],
          f"saw {order}, want {EXPECT['order']}")
    added = {b["n"] for b in blocks if b["op"].startswith("apply") and NEXT_LABEL in rp.labels_split(b["add"])}
    check(f"{NEXT_LABEL} applied to exactly the taken issues", added == EXPECT["labelled"],
          f"saw {sorted(added)}, want {sorted(EXPECT['labelled'])}")
    for n in EXPECT["unchecked"] | EXPECT["asked"]:  # a Left out line saying it waits or is unchecked is allowed
        check(f"#{n} not ranked (not in Order, not labelled)", n not in set(order) | added)
    size = re.search(r"\*\*Size:\*\*\s*(\d+)\.\s*Used:\s*(\d+)", body)
    check("Size line gives the items used", size and int(size.group(2)) == EXPECT["used"],
          size.group(0) if size else "no **Size:** line")
    print(f"{sum(results)}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: score.py <out-dir>")
    sys.exit(main(sys.argv[1]))
