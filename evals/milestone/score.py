#!/usr/bin/env python3
"""Score a milestone dry run (planning phase or delivery loop), or check one Milestone issue body against the shape.

Usage:
  score.py <out-dir> <plan|add-feature|deliver>   score <out-dir>/repo/.scratch/proposed-actions.md for that case
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


def parse_events(text):
    """Split proposed-actions.md at its '## Event <k>' lines: {k: blocks}. Blocks before the first event are under 0."""
    events, parts = {}, re.split(r"^## Event (\d+)\s*$", text, flags=re.M)
    events[0] = parse_actions(parts[0])
    for i in range(1, len(parts), 2):
        events[int(parts[i])] = parse_actions(parts[i + 1])
    return events


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


def builds(blocks):
    return starts(blocks, "implement") + starts(blocks, "implement-spec")


def versions(blocks):
    return set(re.findall(r"\b\d+\.\d+\.\d+\b", "\n".join(b["text"] for b in blocks)))


def score_deliver(ev):
    every = [b for k in sorted(ev) for b in ev[k]]
    check("events 1 to 12 each have an '## Event <k>' part", all(k in ev for k in range(1, 13)),
          "missing " + ", ".join(str(k) for k in range(1, 13) if k not in ev))
    e = {k: ev.get(k, []) for k in range(1, 13)}

    # Event 1: Release grouping, handed to release planning; no build thread before the Release is planned.
    rel1 = starts(e[1], "release")
    check("event 1: a Release thread started with `release`", len(rel1) == 1, f"{len(rel1)} found")
    brief = rel1[0]["brief"] if rel1 else ""
    i10, i20 = brief.find("10-farewell"), brief.find("20-quiet")
    check("event 1: its brief groups farewell (with 11 and 12) then quiet into one Release",
          0 <= i10 < i20 and "11-bye-code" in brief and "12-bye-usage" in brief, brief[:160])
    check("event 1: the Release is named Milestone 1 · Release 1 (release-m1-r1)",
          "release-m1-r1" in brief or re.search(r"Milestone 1 · Release 1", brief) is not None)
    check("event 1: no build thread before the Release is planned", not builds(e[1]))

    # Event 2: the next thread, within the thread limit and the Milestone's one-at-a-time rule.
    b2 = builds(e[2])
    check("event 2: exactly one build thread started (one at a time)", len(b2) == 1, f"{len(b2)} found")
    spec = starts(e[2], "implement-spec")
    first = spec[0] if spec else {"brief": ""}
    check("event 2: it is the Spec thread of 10-farewell, with `implement-spec`",
          len(spec) == 1 and "10-farewell" in first["brief"], first["brief"][:120])
    check("event 2: its brief carries the model tier (regular) and the issue's Review depth (Deep)",
          re.search(r"\bregular\b", first["brief"], re.I) is not None
          and re.search(r"\bDeep\b", first["brief"]) is not None)
    check("events 1 to 6: 20-quiet not started while farewell is open",
          not any("20-quiet" in b["brief"] for k in range(1, 7) for b in builds(e[k])))

    # Event 3: the version hand-out, recorded on the tracker.
    v3 = versions(e[3]) - {"0.3.0"}
    check("event 3: version 0.4.0 handed out, and no other", v3 == {"0.4.0"}, ", ".join(sorted(v3)) or "none")
    rec = [b for b in e[3] if b["op"] == "Comment on an issue" and "0.4.0" in b["body"]]
    check("event 3: the hand-out is recorded on the tracker (a comment naming 0.4.0)", bool(rec))
    told = [b for b in e[3] if b["op"] == "Message a thread" and "0.4.0" in b["body"]]
    check("event 3: the Spec thread is told its number", bool(told))
    check("event 3: no build thread started while the number is out", not builds(e[3]))

    # Event 4: #10 (no issue of its own) asks while #7's 0.4.0 is out: it waits, recorded.
    wait10 = [b for b in e[4] if b["op"] == "Comment on an issue" and re.search(r"Waiting", b["body"])
              and "#10" in b["body"]]
    check("event 4: #10 waits while 0.4.0 is out for #7, recorded as Waiting", bool(wait10))
    check("event 4: #10 gets no number yet",
          not any(re.search(r"Version \d+\.\d+\.\d+ for #10", b["body"]) for b in e[4]))

    # Event 5: #7 closed unmerged voids its number, so the waiter #10 is served first and #9 waits behind it.
    give10 = [b for b in e[5] if b["op"] == "Comment on an issue"
              and re.search(r"Version 0\.4\.0 for #10", b["body"])]
    check("event 5: #7's number is void, so the waiting #10 gets 0.4.0, recorded", bool(give10))
    wait9 = [b for b in e[5] if b["op"] == "Comment on an issue" and re.search(r"Waiting", b["body"])
             and "#9" in b["body"]]
    check("event 5: #9 waits behind #10, recorded as Waiting", bool(wait9))
    check("event 5: #9 gets no number yet",
          not any(re.search(r"Version \d+\.\d+\.\d+ for #9", b["body"]) for b in e[5]))

    # Event 6: #10 merged (a skill merge): the waiting #9 gets 0.5.0; 20 is re-read; nothing starts.
    give9 = [b for b in e[6] if b["op"] == "Comment on an issue" and re.search(r"Version 0\.5\.0 for #9", b["body"])]
    check("event 6: main reads 0.4.0, so the waiting #9 gets 0.5.0, recorded", bool(give9))
    rr6 = [b for b in e[6] if "20-quiet" in b["issue"] and b["op"] in ("Edit an issue body", "Comment on an issue", "Close")
           and "<!-- milestone delivery thread" not in b["body"]]
    check("event 6: 20-quiet re-read after #10 changed the skill", bool(rr6))
    check("event 6: no build thread started (10 still holds the slot)", not builds(e[6]))

    # Event 7: the Ticket re-read after the farewell skill merge, before the next thread starts.
    s20 = [b for b in builds(e[7]) if "20-quiet" in b["brief"]]
    check("event 7: the Ticket thread of 20-quiet started, with `implement`",
          len(s20) == 1 and bool(starts(e[7], "implement")), f"{len(s20)} found")
    check("event 7: its brief carries no Review depth (20 names none, so agentic-review chooses)",
          bool(s20) and not re.search(r"review depth", s20[0]["brief"], re.I))
    reread = [b for b in e[7] if "20-quiet" in b["issue"]
              and b["op"] in ("Edit an issue body", "Comment on an issue", "Close")
              and "<!-- milestone delivery thread" not in b["body"]]
    check("event 7: 20-quiet re-read against the changed skill before its thread starts",
          bool(reread) and (not s20 or reread[0]["n"] < s20[0]["n"]))
    check("event 7: the re-read brings in the farewell (quiet silences bye too)",
          any(re.search(r"\bbye\b|farewell", b["body"], re.I) for b in reread))
    check("event 7: no Release thread yet (20-quiet is still open)", not starts(e[7], "release"))

    # Event 8: no number for a pull request that changes no skill.
    v8 = versions(e[8]) - {"0.3.0", "0.4.0", "0.5.0"}
    check("event 8: no version handed out for a pull request that changes no skill",
          not v8 and not any(re.search(r"Version \d+\.\d+\.\d+ for #8", b["body"]) for b in e[8]),
          ", ".join(sorted(v8)))
    told8 = [b for b in e[8] if b["op"] == "Message a thread" and "20-quiet" in b["issue"]]
    check("event 8: the Ticket thread is told to merge with no bump", bool(told8))

    # Event 9: the Release boundary.
    rel9 = starts(e[9], "release")
    check("event 9: the Release thread started once every issue of the Release is closed",
          len(rel9) == 1 and "40-release-m1-r1" in rel9[0]["brief"], f"{len(rel9)} found")
    check("event 9: no build thread started (25-hello-doc is not in the Release)", not builds(e[9]))

    # Event 10: a second wake while the Release thread runs starts nothing.
    check("event 10: no thread started while the Release thread is running", not starts(e[10]))

    # Event 11: the Release thread planned nothing (25 still blocked): its end is recorded, nothing starts.
    check("event 11: no thread started (the one feature left is still blocked)", not starts(e[11]))
    ended = [b for b in e[11] if b["op"] == "Comment on an issue" and "<!-- milestone delivery thread ended" in b["body"]]
    check("event 11: the Release thread's end is recorded on the tracker", bool(ended))

    # Event 12: the blocker closed, so the loop plans the next Release itself.
    rel12 = starts(e[12], "release")
    check("event 12: a Release thread started to plan the next Release with 25-hello-doc",
          len(rel12) == 1 and "25-hello-doc" in rel12[0]["brief"], f"{len(rel12)} found")
    check("event 12: no build thread before that Release is planned", not builds(e[12]))

    # Throughout: delivery leaves planning's records and Release planning's labels alone.
    check("the Milestone issue body is never edited",
          not any(b["op"] == "Edit an issue body" and "00-milestone" in b["issue"] for b in every))
    check("no release or Milestone label applied by the coordinator (Release planning owns release labels)",
          not any(b["op"] in ("Apply / remove labels", "Create a label") for b in every))


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--shape":
        shape(open(sys.argv[2]).read())
    elif len(sys.argv) == 3 and sys.argv[2] in ("plan", "add-feature", "deliver"):
        out, case = sys.argv[1], sys.argv[2]
        try:
            text = open(f"{out}/repo/.scratch/proposed-actions.md").read()
        except FileNotFoundError:
            text = ""
        blocks = parse_actions(text)
        check("proposed-actions.md holds actions", bool(blocks))
        if case == "deliver":
            score_deliver(parse_events(text))
        elif case == "plan":
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
