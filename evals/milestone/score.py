#!/usr/bin/env python3
"""Score a milestone dry run of the planning phase, or check one Milestone issue body against the shape.

The delivery cases moved to evals/team-lead/score.py with the team-lead skill.

Usage:
  score.py <out-dir> <plan|add-feature>   score <out-dir>/repo/.scratch/proposed-actions.md for that case
  score.py --shape <body-file>            check a Milestone issue body (for example a real one) against the shape

Prints one line per check (PASS or FAIL with what it saw) and exits 1 when any check fails.
See evals/milestone/README.md.
"""
import re
import sys

LABEL = "milestone-1"
HEADINGS = ["## Goal", "## Features, in build order", "## Acceptance", "## Excluded", "## Boundaries"]
COLUMNS = ["#", "Feature", "Kind", "Accepted when"]

results = []


def check(name, ok, seen=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + ("" if ok or not seen else f": {seen}"))


def parse_actions(text):
    """Split proposed-actions.md into blocks: (number, operation, issue, fields, body)."""
    blocks = []
    for m in re.finditer(r"^### (\d+)\. (.+?)\n(.*?)(?=^### \d+\. |\Z)", text, re.S | re.M):
        num, op, rest = int(m.group(1)), m.group(2).strip(), m.group(3)
        body, brief = "", ""
        bm = re.search(r"^Body:\s*\n~~~\n(.*?)\n~~~", rest, re.S | re.M)
        if bm:
            body = bm.group(1)
            rest = rest[: bm.start()] + rest[bm.end():]
        bm = re.search(r"^Brief:\s*\n~~~\n(.*?)\n~~~", rest, re.S | re.M)
        if bm:
            brief = bm.group(1)
            rest = rest[: bm.start()] + rest[bm.end():]
        fields = {}
        for line in rest.splitlines():
            fm = re.match(r"^([A-Za-z ]+):\s*(.*)$", line)
            if fm:
                fields[fm.group(1).strip()] = fm.group(2).strip()
        if not brief:
            brief = fields.get("Brief", "")
        blocks.append({"n": num, "op": op, "issue": fields.get("Issue", "") or fields.get("Thread", ""), "f": fields,
                       "body": body, "brief": brief, "text": m.group(0)})
    return blocks



def section(body, heading):
    i = body.find(heading + "\n")
    if i < 0:
        return ""
    rest = body[i + len(heading) + 1:]
    j = rest.find("\n## ")
    return rest if j < 0 else rest[:j]


def feature_rows(body):
    """Rows of the first table in the Features section: list of cell lists (header first)."""
    rows = []
    for line in section(body, "## Features, in build order").splitlines():
        if line.startswith("|") and not re.match(r"^\|\s*-", line):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows


def shape(body, prefix=""):
    """Check one Milestone issue body against the shape; return the feature rows."""
    pos = [body.find(h + "\n") for h in HEADINGS]
    missing = [h for h, p in zip(HEADINGS, pos) if p < 0]
    check(prefix + "headings present", not missing, "missing " + ", ".join(missing))
    present = [p for p in pos if p >= 0]
    check(prefix + "headings in order", present == sorted(present), "out of order")
    feats = section(body, "## Features, in build order")
    first = next((l for l in feats.splitlines() if l.strip()), "")
    check(prefix + "order rule stated before the table",
          bool(re.search(r"one at a time|at once|in this order", first, re.I)), repr(first[:80]))
    rows = feature_rows(body)
    header = rows[0] if rows else []
    check(prefix + "feature table columns start " + " | ".join(COLUMNS), header[:4] == COLUMNS, " | ".join(header))
    data = rows[1:]
    check(prefix + "at least one feature row", bool(data))
    if header[:4] == COLUMNS:
        empty = [r[0] for r in data if len(r) < 4 or not r[3]]
        check(prefix + "every feature row has its acceptance criteria", not empty, "empty in rows " + ", ".join(empty))
    check(prefix + "Boundaries has a Budget line",
          bool(re.search(r"^- \*\*Budget:?\*\*", section(body, "## Boundaries"), re.M)))
    check(prefix + "Boundaries has a line beyond Budget",
          len([l for l in section(body, "## Boundaries").splitlines() if l.startswith("- ")]) >= 2)
    return data


def labels_added(blocks, issue_part):
    return [b for b in blocks if b["op"] == "Apply / remove labels" and issue_part in b["issue"]
            and LABEL in b["f"].get("Add", "")]


def score_plan(blocks):
    creates = [b for b in blocks if b["op"] == "Create an issue" and LABEL in b["f"].get("Labels", "")
               and b["f"].get("Title", "").startswith("Milestone 1:")]
    check("one Milestone issue created, titled 'Milestone 1: ...', labelled " + LABEL, len(creates) == 1,
          f"{len(creates)} found")
    if not creates:
        return
    m = creates[0]
    rows = shape(m["body"], "shape: ")
    names = [r[1] if len(r) > 1 else "" for r in rows]
    check("features listed farewell then quiet",
          len(names) == 2 and "10" in names[0] and "20" in names[1], " / ".join(names))
    check("order rule says up to 2 at once",
          bool(re.search(r"2 at once|two at once", section(m["body"], "## Features, in build order"), re.I)))
    check("Excluded names colour and translations",
          bool(re.search(r"colou?r", section(m["body"], "## Excluded"), re.I))
          and "ranslation" in section(m["body"], "## Excluded"))
    check("Boundaries names the registry approval", "registry" in section(m["body"], "## Boundaries"))
    check("Acceptance has the user's review check", "--quiet bye Ada" in section(m["body"], "## Acceptance"))
    made = [b for b in blocks if b["op"] == "Create a label" and b["f"].get("Label") == LABEL]
    check("label created before the Milestone issue", bool(made) and made[0]["n"] < m["n"])
    for part in ["10-farewell", "11-bye-code", "12-bye-usage", "20-quiet"]:
        hit = labels_added(blocks, part)
        check(f"{part} labelled {LABEL} after the Milestone issue is created",
              bool(hit) and hit[0]["n"] > m["n"])
    check("30-colour never labelled", not labels_added(blocks, "30-colour"))
    subs = {b["issue"] for b in blocks if b["op"] == "Make an issue a sub-issue of a parent"}
    check("10 and 20 linked as sub-issues", any("10-farewell" in s for s in subs) and any("20-quiet" in s for s in subs),
          ", ".join(sorted(subs)))
    check("Tickets 11 and 12 keep their Spec parent", not any("11-" in s or "12-" in s for s in subs))
    started = [b for b in blocks if b["op"] == "Start a thread"]
    released = [b for b in blocks if "release-" in b["f"].get("Add", "") + b["f"].get("Labels", "")
                + b["f"].get("Label", "")]
    check("no thread started and no release label (delivery has not started)", not started and not released,
          f"{len(started)} threads, {len(released)} release-label actions")


def score_add(blocks, original):
    edits = [b for b in blocks if b["op"] == "Edit an issue body" and "00-milestone" in b["issue"]]
    check("Milestone issue body edited once", len(edits) == 1, f"{len(edits)} found")
    if not edits:
        return
    e = edits[0]
    plan30 = [b for b in blocks if b["n"] < e["n"] and (
        ("30-colour" in b["issue"] and b["op"] in ("Edit an issue body", "Apply / remove labels")
         and "milestone" not in b["f"].get("Add", ""))
        or (b["op"] == "Create an issue" and re.search(r"colou?r", b["f"].get("Title", ""), re.I)))]
    check("issue 30 planned (its Ticket written) before the Milestone issue changes", bool(plan30))
    rows = shape(e["body"], "shape: ")
    names = [r[1] if len(r) > 1 else "" for r in rows]
    check("rows: farewell, quiet, then colour",
          len(rows) == 3 and "10" in names[0] and "20" in names[1] and ("30" in names[2] or "olo" in names[2]),
          " / ".join(names))
    check("added row marked 'added <date> by the user'",
          len(rows) == 3 and re.search(r"added 2026-11-02 by the user", " ".join(rows[2]), re.I) is not None)
    changed = [h for h in ["## Goal", "## Acceptance", "## Excluded", "## Boundaries"]
               if section(original, h).strip() != section(e["body"], h).strip()]
    check("goal, acceptance, exclusions and boundaries unchanged", not changed, "changed " + ", ".join(changed))
    target = [b for b in blocks if b["op"] == "Apply / remove labels" and LABEL in b["f"].get("Add", "")
              and "colo" in b["issue"]]
    check("the colour feature labelled after the Milestone issue lists it", bool(target) and target[0]["n"] > e["n"])
    early = [b for b in blocks if b["n"] < e["n"] and LABEL in b["f"].get("Add", "") + b["f"].get("Labels", "")]
    check("nothing carries the Milestone label before it is listed", not early,
          ", ".join(str(b["n"]) for b in early))
    rel = [b for b in blocks if "release-0.4.0" in b["f"].get("Add", "")]
    check("not added to the open Release 0.4.0", not rel)


def starts(blocks, skill=None):
    """Thread starts, optionally with this exact skill (the Skill line, without backticks or a leading slash)."""
    out = []
    for b in blocks:
        if b["op"] != "Start a thread":
            continue
        name = b["f"].get("Skill", "").strip("`/ ").lower()
        if skill is None or name == skill:
            out.append(b)
    return out



def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--shape":
        shape(open(sys.argv[2]).read())
    elif len(sys.argv) == 3 and sys.argv[2] in ("plan", "add-feature"):
        out, case = sys.argv[1], sys.argv[2]
        try:
            text = open(f"{out}/repo/.scratch/proposed-actions.md").read()
        except FileNotFoundError:
            text = ""
        blocks = parse_actions(text)
        check("proposed-actions.md holds actions", bool(blocks))
        if case == "plan":
            score_plan(blocks)
        else:
            original = open(f"{out}/repo/.scratch/issues/00-milestone.md").read()
            score_add(blocks, original)
    else:
        print(__doc__)
        sys.exit(2)
    print(f"{sum(results)}/{len(results)} checks pass")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
