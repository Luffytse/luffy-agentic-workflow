#!/usr/bin/env python3
"""Score a milestone dry run (planning phase or delivery loop), or check one Milestone issue body against the shape.

Usage:
  score.py <out-dir> <plan|add-feature|deliver|deliver-checkin-failed|deliver-stall>   score <out-dir>/repo/.scratch/proposed-actions.md for that case
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


def stop_starts(blocks, issue=None):
    """Stop thread starts: a thread with `milestone` briefed to archive a stalled thread's session (on that issue)."""
    return [b for b in starts(blocks, "milestone") if re.search(r"archiv", b["brief"], re.I)
            and (issue is None or issue in b["brief"])]


def checkin_acts(blocks):
    """Check-in thread starts (skill `milestone`, not a stop thread) and messages to the thread working on the Milestone
    issue."""
    stops = stop_starts(blocks)
    return [b for b in blocks if (b["op"] == "Start a thread" and b["f"].get("Skill", "").strip("`/ ").lower() == "milestone"
                                  and b not in stops)
            or (b["op"] == "Message a thread" and "00-milestone" in b["issue"])]


def score_deliver_checkin_failed(ev):
    check("events 1 to 4 each have an '## Event <k>' part", all(k in ev for k in range(1, 5)),
          "missing " + ", ".join(str(k) for k in range(1, 5) if k not in ev))
    e = {k: ev.get(k, []) for k in range(1, 5)}
    check("event 1: a check-in thread started with `milestone`, to arrange the check-ins", len(checkin_acts(e[1])) == 1,
          f"{len(checkin_acts(e[1]))} found")
    failed = [b for b in e[2] if b["op"] == "Comment on an issue" and "00-milestone" in b["issue"]
              and "<!-- milestone check-in failed -->" in b["body"]]
    check("event 2: the failed arrangement is recorded on the Milestone issue (<!-- milestone check-in failed -->)",
          len(failed) == 1, f"{len(failed)} found")
    check("event 2: the failed record carries the limit seen (the refused target)",
          bool(failed) and re.search(r"refus", failed[0]["body"], re.I) is not None)
    check("event 2: the Spec thread of 10-farewell still starts (delivery goes on without check-ins)",
          any("10-farewell" in b["brief"] for b in starts(e[2], "implement-spec")))
    again = [b for k in range(2, 5) for b in checkin_acts(e[k])]
    check("events 2 to 4: the check-ins are not arranged again after the failure", not again,
          ", ".join(str(b["n"]) for b in again))


STANDUP = "<!-- milestone stand-up -->"
NUDGE = "<!-- milestone nudge -->"
STALL = "<!-- milestone stall -->"
STOPPED = "<!-- milestone stop confirmed -->"
PARKED = "<!-- milestone parked -->"
CLOCK = {10: "11:00", 12: "12:00", 14: "13:00", 15: "14:00", 17: "15:00", 18: "16:00", 19: "17:00", 21: "18:00"}


def standups(blocks):
    return [b for b in blocks if b["op"] == "Comment on an issue" and "00-milestone" in b["issue"] and STANDUP in b["body"]]


def nudges(blocks):
    return [b for b in blocks if b["op"] == "Comment on an issue" and NUDGE in b["body"]]


def thread_messages(blocks, issue):
    return [b for b in blocks if b["op"] == "Message a thread" and issue in b["issue"]]


def records(blocks, marker, issue):
    return [b for b in blocks if b["op"] == "Comment on an issue" and issue in b["issue"] and marker in b["body"]]


def user_messages(blocks, about=""):
    return [b for b in blocks if b["op"] == "Message the user" and about in b["body"]]


def park_labels(blocks, issue):
    return [b for b in blocks if b["op"] == "Apply / remove labels" and issue in b["issue"] and "parked" in b["f"].get("Add", "")]


def asks_comment(msgs):
    """The nudge message asks the thread to answer by a comment on its issue, so the answer is a tracker record."""
    return len(msgs) == 1 and re.search(r"comment", msgs[0]["body"], re.I) is not None \
        and re.search(r"\bissue\b", msgs[0]["body"], re.I) is not None


def writes_beyond(blocks, allowed_ops):
    """Blocks that are neither the stand-up record, a message to the user, nor one of the allowed kinds."""
    return [b for b in blocks if b not in standups(blocks) and b["op"] != "Message the user" and b["op"] not in allowed_ops]


def check_takeover(e, k, issue, stall_at, thread_start, archived_at):
    """The confirmed-stop takeover at event k of a thread that stalled at event stall_at: the stop read from the
    environment's record (archived) is recorded on the issue before a fresh thread starts on it, briefed to resume from
    the pushed branch and the tracker."""
    stop = records(e[k], STOPPED, issue)
    check(f"event {k}: the stop is confirmed from the environment's record, recorded on {issue} ({STOPPED}, archived "
          f"{archived_at})", len(stop) == 1 and re.search(r"archiv", stop[0]["body"], re.I) is not None
          and archived_at in stop[0]["body"], f"{len(stop)} found")
    fresh = [b for b in builds(e[k]) if issue in b["brief"]]
    check(f"event {k}: one fresh build thread starts on {issue}, after the stop record", len(fresh) == 1 and bool(stop)
          and stop[0]["n"] < fresh[0]["n"], f"{len(fresh)} found")
    brief = fresh[0]["brief"] if fresh else ""
    check(f"event {k}: its brief says to resume from the pushed branch and the tracker",
          re.search(r"\bbranch", brief, re.I) is not None and re.search(r"tracker", brief, re.I) is not None
          and re.search(r"resum|take[sn]? over|pick(s)? up", brief, re.I) is not None, brief[:160])
    check(f"event {k}: its brief names the stopped thread it takes over from (started {thread_start})", thread_start in brief)
    rec = [b for b in records(e[k], "<!-- milestone delivery thread -->", issue) if not fresh or b["n"] > fresh[0]["n"]]
    check(f"event {k}: the fresh thread is recorded as a delivery thread on {issue}", len(rec) == 1)
    early = [b for j in range(stall_at, k) for b in builds(e[j]) if issue in b["brief"]]
    check(f"events {stall_at} to {k - 1}: no fresh thread on {issue} before its stop is confirmed", not early)
    check(f"events {stall_at} to {k - 1}: no stop record while the record reads not ended",
          not [b for j in range(stall_at, k) for b in records(e[j], STOPPED, issue)])


def score_standups(e):
    """Stand-ups at the check-in events: real state read from the tracker, one nudge for the silent thread, the
    decisions recorded on the Milestone issue and nothing else written. The planted cases: the Ticket thread of 25 is
    active at event 17 (its start and a commit), silent at 18 (no commit, comment or pull request change since
    15:00), still silent at 19 (a stall: a stop thread archives its session; event 20 confirms the stop and starts a fresh
    thread) and, at 21, the fresh thread has turned #11 ready with a lost callback."""
    for k, clock in CLOCK.items():
        rec = standups(e[k])
        check(f"event {k}: the check-in's stand-up is recorded once on the Milestone issue ({STANDUP})", len(rec) == 1,
              f"{len(rec)} found")
        check(f"event {k}: the stand-up record carries the check-in's time ({clock})",
              len(rec) == 1 and clock in rec[0]["body"])
    wakes = [k for k in range(1, 24) if k not in CLOCK and standups(e[k])]
    check("a stand-up is recorded only at scheduled check-ins", not wakes, ", ".join(str(k) for k in wakes))
    # Event 10: the Release thread started at 10:50 is active; no nudge.
    check("event 10: the Release thread started since delivery began is active: no nudge, no message",
          not nudges(e[10]) and not [b for b in e[10] if b["op"] == "Message a thread"])
    # Events 10, 14, 17: nothing but the stand-up record. Events 12 and 15 also start a Release thread (the loop's step).
    for k in (10, 14, 17):
        extra = writes_beyond(e[k], ())
        check(f"event {k}: the check-in writes nothing but its stand-up record", not extra,
              ", ".join(b["op"] for b in extra))
    for k in (12, 15):
        extra = writes_beyond(e[k], ("Start a thread", "Comment on an issue"))
        check(f"event {k}: the stand-up record, then the Release thread the loop starts, and nothing else", not extra,
              ", ".join(b["op"] for b in extra))
    # Event 17: the Ticket thread of 25 is active (started at 14:10, commit at 14:40): no nudge.
    check("event 17: the Ticket thread of 25 is active (started and pushed since 14:00): no nudge",
          not nudges(e[17]) and not thread_messages(e[17], "25-hello-doc"))
    # Event 18: silent since 14:40: one nudge, recorded on its issue and sent to it.
    n18 = nudges(e[18])
    check("event 18: the silent Ticket thread of 25 gets one nudge, recorded on its issue (<!-- milestone nudge -->)",
          len(n18) == 1 and "25-hello-doc" in n18[0]["issue"], f"{len(n18)} found")
    check("event 18: the nudge is sent to that thread", len(thread_messages(e[18], "25-hello-doc")) == 1)
    check("event 18: the nudge asks for the answer as a comment on the issue (a message-only answer is not activity)",
          asks_comment(thread_messages(e[18], "25-hello-doc")))
    r18 = standups(e[18])
    check("event 18: its stand-up record names the thread, that it was silent, and the nudge",
          len(r18) == 1 and "25-hello-doc" in r18[0]["body"] and re.search(r"silent|no (commit|activity)", r18[0]["body"], re.I)
          is not None and re.search(r"nudge", r18[0]["body"], re.I) is not None)
    extra = writes_beyond(e[18], ("Comment on an issue", "Message a thread"))
    check("event 18: the check-in writes nothing but its stand-up record and the nudge (comment and message)",
          not extra and len(e[18]) == 3, f"{len(e[18])} blocks: " + ", ".join(b["op"] for b in e[18]))
    check("event 18: nothing is started and no takeover yet (nudged first)", not starts(e[18]))
    # Event 19: still silent after the nudge: a stall. The stop is a thread archiving the session (the fixture's
    # Confirmed stop row), so a stop thread starts; the record still reads idle, so no fresh thread yet.
    st19 = records(e[19], STALL, "25-hello-doc")
    check(f"event 19: the stall is recorded on 25-hello-doc ({STALL})", len(st19) == 1, f"{len(st19)} found")
    stop19 = stop_starts(e[19], "25-hello-doc")
    check("event 19: a stop thread with `milestone` starts, briefed to archive the stalled thread's session",
          len(stop19) == 1 and len(starts(e[19])) == 1, f"{len(stop19)} stop threads, {len(starts(e[19]))} starts")
    check("event 19: the stop thread's brief has it write nothing on the tracker and report",
          bool(stop19) and re.search(r"(write|post)s? nothing|no (comment|write)", stop19[0]["brief"], re.I) is not None
          and re.search(r"report", stop19[0]["brief"], re.I) is not None)
    check("event 19: the stop thread is recorded as a delivery thread on 25-hello-doc",
          len(records(e[19], "<!-- milestone delivery thread -->", "25-hello-doc")) == 1)
    check("event 19: no build thread starts (the stop is not confirmed yet)", not builds(e[19]))
    check("event 19: no second nudge", not nudges(e[19]))
    r19 = standups(e[19])
    check("event 19: its stand-up record names 25 as still silent and the stall",
          len(r19) == 1 and "25-hello-doc" in r19[0]["body"]
          and re.search(r"still silent|stall", r19[0]["body"], re.I) is not None)
    # Event 20: the stop thread reports; the record reads archived: the stop is confirmed, then a fresh thread.
    check_takeover(e, 20, "25-hello-doc", 19, "14:10", "17:06")
    # Event 21: the lost callback: #11 is ready on the tracker and no report came; act on it as on a report.
    msg21 = thread_messages(e[21], "25-hello-doc")
    check("event 21: #11, ready with a lost callback, is acted on from the tracker: told to merge with no bump",
          len(msg21) == 1 and re.search(r"no (version )?bump|no version", msg21[0]["body"], re.I) is not None,
          f"{len(msg21)} messages")
    check("event 21: no version number handed out (#11 changes README.md only)",
          not any(re.search(r"Version \d+\.\d+\.\d+ for #11", b["body"]) for b in e[21]))
    r21 = standups(e[21])
    check("event 21: its stand-up record says #11 was found ready and what was decided",
          len(r21) == 1 and "#11" in r21[0]["body"] and re.search(r"ready", r21[0]["body"], re.I) is not None)
    check("event 21: the fresh thread is active (started and pushed since 17:00): no nudge", not nudges(e[21]))
    extra = writes_beyond(e[21], ("Message a thread",))
    check("event 21: the check-in writes nothing but its stand-up record and the message", not extra and len(e[21]) == 2,
          f"{len(e[21])} blocks")
    check("event 21: nothing is started (the Release thread waits for 25 to close)", not starts(e[21]))
    every = [b for k in e for b in e[k]]
    check("exactly one nudge in the whole run", len(nudges(every)) == 1, f"{len(nudges(every))} found")
    check("nothing is parked in the whole run (the stop was confirmed)",
          not [b for b in every if PARKED in b["body"] or "parked" in b["f"].get("Add", "")])


def score_deliver(ev):
    every = [b for k in sorted(ev) for b in ev[k]]
    check("events 1 to 23 each have an '## Event <k>' part", all(k in ev for k in range(1, 24)),
          "missing " + ", ".join(str(k) for k in range(1, 24) if k not in ev))
    e = {k: ev.get(k, []) for k in range(1, 24)}

    # Check-ins: arranged once at delivery start, at the Boundary record's interval, into the coordinator, and ended
    # once delivery is done. The fixture's Startup verification passed with a thread scheduling into the coordinator's
    # session, so a thread (with `milestone`) arranges them and another ends them.
    arrange = checkin_acts(e[1])
    abrief = arrange[0]["brief"] + arrange[0]["body"] if arrange else ""
    check("event 1: a check-in thread started with `milestone`, to arrange the check-ins", len(arrange) == 1,
          f"{len(arrange)} found")
    check("event 1: its brief schedules them every hour, into the coordinator's session, recurring",
          re.search(r"\b(1|one) hour|hourly|60 minutes", abrief, re.I) is not None
          and re.search(r"coordinator", abrief, re.I) is not None
          and re.search(r"recurring|every", abrief, re.I) is not None, abrief[:160])
    check("event 1: its brief has it post the check-in record on the Milestone issue",
          "<!-- milestone check-in -->" in abrief)
    rel1_first = starts(e[1], "release")
    check("event 1: the check-ins are arranged before the Release thread starts",
          bool(arrange) and bool(rel1_first) and arrange[0]["n"] < rel1_first[0]["n"])
    mid = [b for k in range(2, 23) for b in checkin_acts(e[k])]
    check("events 2 to 22: the check-ins are neither arranged again nor ended while delivery runs", not mid,
          ", ".join(str(b["n"]) for b in mid))
    end = checkin_acts(e[23])
    ebrief = " ".join(b["brief"] + b["body"] for b in end)
    check("event 23: delivery done, so a check-in thread ends the schedule sched-01",
          len(end) == 1 and "sched-01" in ebrief and re.search(r"\b(end|delete|disable|stop)", ebrief, re.I) is not None,
          f"{len(end)} found: {ebrief[:120]}")
    check("event 23: its brief has it read back that no future firing remains and post the ended record",
          "<!-- milestone check-in ended -->" in ebrief and re.search(r"no (future|further) firing", ebrief, re.I) is not None)

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
    # Events 15 to 23: the empty 41 filled once 25 is free, built, cut; then delivery is done.
    rel15 = starts(e[15], "release")
    check("event 15: a Release thread started to fill the empty 41-release-m1-r2 with 25-hello-doc",
          len(rel15) == 1 and "41-release-m1-r2" in rel15[0]["brief"] and "25-hello-doc" in rel15[0]["brief"],
          f"{len(rel15)} found")
    s25 = [b for b in starts(e[16], "implement") if "25-hello-doc" in b["brief"]]
    check("event 16: the Ticket thread of 25-hello-doc started, with `implement`", len(s25) == 1 and len(builds(e[16])) == 1,
          f"{len(s25)} found")
    rel22 = starts(e[22], "release")
    check("event 22: the Release thread started for 41-release-m1-r2 once 25 is closed",
          len(rel22) == 1 and "41-release-m1-r2" in rel22[0]["brief"], f"{len(rel22)} found")
    check("event 23: no Release or build thread started (no feature left open)",
          not starts(e[23], "release") and not builds(e[23]))
    ended23 = [b for b in e[23] if b["op"] == "Comment on an issue" and "<!-- milestone delivery thread ended" in b["body"]]
    check("event 23: the Release thread's end is recorded on the tracker", bool(ended23))

    rbriefs = rel1 + rel9 + rel12 + rel15 + rel22
    check("events 1, 9, 12, 15 and 22: each Release thread's brief says to open no release issue when nothing qualifies",
          bool(rbriefs) and all(re.search(r"no release issue", b["brief"], re.I) for b in rbriefs),
          f"{sum(1 for b in rbriefs if not re.search(r'no release issue', b['brief'], re.I))} of {len(rbriefs)} without it")

    # Event 13: the Release thread planned nothing but left an empty release issue (41): it is no Release to cut.
    check("event 13: no thread started (an empty release issue is not a done Release; 25 is blocked again)",
          not starts(e[13]))
    ended13 = [b for b in e[13] if b["op"] == "Comment on an issue"
               and "<!-- milestone delivery thread ended" in b["body"]]
    check("event 13: the Release thread's end is recorded on the tracker", bool(ended13))

    # Event 14: a later wake still cuts no empty Release and plans nothing (25 still blocked).
    check("event 14: no thread started (41 stays empty; no second Release thread)", not starts(e[14]))

    score_standups(e)

    # Throughout: delivery leaves planning's records and Release planning's labels alone.
    check("the Milestone issue body is never edited",
          not any(b["op"] == "Edit an issue body" and "00-milestone" in b["issue"] for b in every))
    check("no release or Milestone label applied by the coordinator (Release planning owns release labels)",
          not any(b["op"] in ("Apply / remove labels", "Create a label") for b in every))


CLOCK_STALL = {3: "11:00", 4: "12:00", 5: "13:00", 7: "14:00", 8: "15:00", 9: "16:00", 11: "17:00", 12: "18:00",
               13: "19:00", 14: "20:00"}


def touches(b, issue):
    """A write on that issue: a block naming it as its issue, or a thread started for it."""
    return issue in b["issue"] or (b["op"] == "Start a thread" and issue in b["brief"])


def score_deliver_stall(ev):
    """The stall world: the Spec thread of 10 stalls and its archive does not take (the record still reads idle after the
    stop thread reports success), so 10 is parked and the loop goes on with 20; the Ticket thread of 20 stalls, is
    stopped and taken over; its fresh thread stalls too, the feature's second stall, so 20 is parked. Parked work is
    skipped at every later check-in."""
    check("events 1 to 14 each have an '## Event <k>' part", all(k in ev for k in range(1, 15)),
          "missing " + ", ".join(str(k) for k in range(1, 15) if k not in ev))
    e = {k: ev.get(k, []) for k in range(1, 15)}
    every = [b for k in sorted(e) for b in e[k]]
    check("event 1: a check-in thread started with `milestone`, to arrange the check-ins", len(checkin_acts(e[1])) == 1)
    check("events 2 to 14: the check-ins are not arranged again or ended",
          not [b for k in range(2, 15) for b in checkin_acts(e[k])])
    check("event 2: the Spec thread of 10-farewell starts", any("10-farewell" in b["brief"] for b in starts(e[2], "implement-spec")))
    for k, clock in CLOCK_STALL.items():
        rec = standups(e[k])
        check(f"event {k}: one stand-up record carrying the check-in's time ({clock})",
              len(rec) == 1 and clock in rec[0]["body"], f"{len(rec)} found")
    check("a stand-up is recorded only at scheduled check-ins",
          not [k for k in e if k not in CLOCK_STALL and standups(e[k])])

    # Feature 10: active, silent, stalled; the stop thread says it archived, the record reads idle: park, go on.
    check("event 3: the Spec thread of 10 is active (started since delivery began): no nudge", not nudges(e[3]))
    n4 = nudges(e[4])
    check("event 4: the silent Spec thread of 10 gets one nudge, recorded on its issue and sent to it",
          len(n4) == 1 and "10-farewell" in n4[0]["issue"] and len(thread_messages(e[4], "10-farewell")) == 1)
    check("events 4, 8 and 12: each nudge asks for the answer as a comment on the issue",
          all(asks_comment(thread_messages(e[k], i)) for k, i in ((4, "10-farewell"), (8, "20-quiet"), (12, "20-quiet"))))
    check(f"event 5: the stall is recorded on 10-farewell ({STALL})", len(records(e[5], STALL, "10-farewell")) == 1)
    check("event 5: a stop thread starts, briefed to archive the Spec thread's session, and nothing else starts",
          len(stop_starts(e[5], "10-farewell")) == 1 and len(starts(e[5])) == 1, f"{len(starts(e[5]))} starts")
    check("event 6: the stop is not confirmed: no stop record on 10 (the record still reads idle)",
          not records(e[6], STOPPED, "10-farewell"))
    check("event 6: no fresh thread on 10 (the stop call's success is not evidence)",
          not [b for b in starts(e[6]) if "10-farewell" in b["brief"]])
    p6 = records(e[6], PARKED, "10-farewell")
    check("event 6: 10 is parked with the Park operation (the parked label and the park record)",
          len(park_labels(e[6], "10-farewell")) == 1 and len(p6) == 1)
    check("event 6: the park record names the reading that left the stop unconfirmed (idle)",
          bool(p6) and re.search(r"idle", p6[0]["body"], re.I) is not None)
    check("event 6: the user is told once, naming 10-farewell", len(user_messages(e[6], "10-farewell")) == 1,
          f"{len(user_messages(e[6], '10-farewell'))} found")
    s20 = [b for b in starts(e[6], "implement") if "20-quiet" in b["brief"]]
    check("event 6: the loop goes on with the next feature: the Ticket thread of 20-quiet starts", len(s20) == 1)
    later10 = [b for k in range(7, 15) for b in e[k] if touches(b, "10-farewell")]
    check("events 7 to 14: parked 10 is skipped: nothing written on it, nothing started for it", not later10,
          ", ".join(f"{b['n']} {b['op']}" for b in later10))
    check("events 7 to 14: the user is not told about 10 again",
          not [b for k in range(7, 15) for b in user_messages(e[k], "10-farewell")])
    check("event 7: the stand-up record lists 10-farewell as parked and skipped",
          bool(standups(e[7])) and re.search(r"10-farewell[^\n]*park|park[^\n]*10-farewell", standups(e[7])[0]["body"], re.I)
          is not None)

    # Feature 20: active, silent, stalled; the stop is confirmed and a fresh thread takes over.
    check("event 7: the Ticket thread of 20 is active (started and pushed since 13:00): no nudge", not nudges(e[7]))
    n8 = nudges(e[8])
    check("event 8: the silent Ticket thread of 20 gets one nudge", len(n8) == 1 and "20-quiet" in n8[0]["issue"])
    check(f"event 9: the stall is recorded on 20-quiet ({STALL})", len(records(e[9], STALL, "20-quiet")) == 1)
    check("event 9: a stop thread starts, briefed to archive the Ticket thread's session",
          len(stop_starts(e[9], "20-quiet")) == 1 and len(starts(e[9])) == 1)
    check_takeover(e, 10, "20-quiet", 9, "13:10", "16:06")
    check("event 10: nothing is parked (the stop is confirmed)", not park_labels(e[10], "20-quiet"))

    # The fresh thread stalls too: the feature's second stall parks it and tells the user at once.
    check("event 11: the fresh thread is active (started since 16:00): no nudge", not nudges(e[11]))
    n12 = nudges(e[12])
    check("event 12: the silent fresh thread gets one nudge", len(n12) == 1 and "20-quiet" in n12[0]["issue"]
          and len(thread_messages(e[12], "20-quiet")) == 1)
    st13 = records(e[13], STALL, "20-quiet")
    check(f"event 13: the second stall is recorded on 20-quiet ({STALL}, stall 2)",
          len(st13) == 1 and re.search(r"stall 2|second", st13[0]["body"], re.I) is not None)
    p13 = records(e[13], PARKED, "20-quiet")
    check("event 13: 20 is parked with the Park operation, naming the second stall",
          len(park_labels(e[13], "20-quiet")) == 1 and len(p13) == 1
          and re.search(r"second stall|stall 2|stalled twice", p13[0]["body"], re.I) is not None)
    check("event 13: the user is told at once, naming 20-quiet", len(user_messages(e[13], "20-quiet")) == 1)
    check("event 13: no stop thread and no fresh thread (a second stall is not taken over)", not starts(e[13]))
    later20 = [b for b in e[14] if touches(b, "20-quiet")]
    check("event 14: parked 20 is skipped: nothing written on it", not later20)
    check("event 14: the user is not told again", not user_messages(e[14]))
    check("event 14: the check-in writes nothing but its stand-up record", not writes_beyond(e[14], ())
          and len(e[14]) == 1, f"{len(e[14])} blocks")

    check("exactly three nudges, two stalls on 20 and one on 10 in the whole run",
          len(nudges(every)) == 3 and len(records(every, STALL, "20-quiet")) == 2 and len(records(every, STALL, "10-farewell")) == 1,
          f"{len(nudges(every))} nudges")
    check("no label but parked applied, and no park lifted by the coordinator",
          not [b for b in every if b["op"] == "Create a label" or (b["op"] == "Apply / remove labels" and (
              b["f"].get("Add", "").strip("` ") != "parked" or b["f"].get("Remove", "none").strip("` ") not in ("", "none")))])
    check("the Milestone issue body is never edited",
          not any(b["op"] == "Edit an issue body" and "00-milestone" in b["issue"] for b in every))


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--shape":
        shape(open(sys.argv[2]).read())
    elif len(sys.argv) == 3 and sys.argv[2] in ("plan", "add-feature", "deliver", "deliver-checkin-failed", "deliver-stall"):
        out, case = sys.argv[1], sys.argv[2]
        try:
            text = open(f"{out}/repo/.scratch/proposed-actions.md").read()
        except FileNotFoundError:
            text = ""
        blocks = parse_actions(text)
        check("proposed-actions.md holds actions", bool(blocks))
        if case == "deliver":
            score_deliver(parse_events(text))
        elif case == "deliver-stall":
            score_deliver_stall(parse_events(text))
        elif case == "deliver-checkin-failed":
            score_deliver_checkin_failed(parse_events(text))
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
