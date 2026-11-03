#!/usr/bin/env python3
"""Score a team-lead dry run: <out-dir>/repo/.scratch/proposed-actions.md against the case's expected actions.

Usage: score.py <out-dir> <deliver|deliver-stall|deliver-pause|deliver-lift|deliver-earlier>
Prints one line per check (PASS, or FAIL with what it saw) and exits 1 when any fails. See evals/team-lead/README.md.
"""
import pathlib
import re
import sys

results = []


def check(name, ok, seen=""):
    results.append(bool(ok))
    print(("PASS " if ok else "FAIL ") + name + ("" if ok or not seen else f": {seen}"))


def parse_blocks(text):
    blocks = []
    for m in re.finditer(r"^### (\d+)\. (.+?)\n(.*?)(?=^### \d+\. |\Z)", text, re.S | re.M):
        op, rest = m.group(2).strip(), m.group(3)
        long = {}
        for key in ("Body", "Brief"):
            bm = re.search(rf"^{key}:\s*\n~~~\n(.*?)\n~~~", rest, re.S | re.M)
            if bm:
                long[key] = bm.group(1)
                rest = rest[: bm.start()] + rest[bm.end():]
        f = {}
        for line in rest.splitlines():
            fm = re.match(r"^([A-Za-z /]+):\s*(.*)$", line)
            if fm:
                f[fm.group(1).strip()] = fm.group(2).strip()
        blocks.append({"op": op, "f": f, "issue": pathlib.Path(f.get("Issue", "")).name,
                       "worker": f.get("Worker", ""), "skill": f.get("Skill", "").strip("`"),
                       "body": long.get("Body", ""), "brief": long.get("Brief", ""), "text": m.group(0)})
    return blocks


def parse_events(text):
    parts = re.split(r"^## Event (\d+)\s*$", text, flags=re.M)
    ev = {0: parse_blocks(parts[0])}
    for i in range(1, len(parts), 2):
        ev[int(parts[i])] = parse_blocks(parts[i + 1])
    return ev


def ops(blocks, op):
    return [b for b in blocks if b["op"].lower().startswith(op.lower())]


def starts(blocks, skill=None, issue=None):
    return [b for b in ops(blocks, "Start a worker")
            if (skill is None or b["skill"] == skill) and (issue is None or b["issue"].startswith(issue))]


def comments(blocks, issue=None, marker=None):
    return [b for b in ops(blocks, "Comment on an issue")
            if (issue is None or b["issue"].startswith(issue)) and (marker is None or marker in b["body"])]


def messages(blocks, worker=None):
    return [b for b in ops(blocks, "Message a worker") if worker is None or b["worker"] == worker]


def stops(blocks, worker=None):
    return [b for b in ops(blocks, "Stop a worker") if worker is None or b["worker"] == worker]


def parks(blocks, issue):
    return [b for b in ops(blocks, "Apply / remove labels") if b["issue"].startswith(issue) and "parked" in b["f"].get("Add", "")]


def user(blocks):
    return ops(blocks, "Message the user")


def quiet(ev, k, why):
    check(f"event {k}: {why}: a quiet check-in writes nothing", ev.get(k) == [],
          ", ".join(b["op"] for b in ev.get(k, [])) or "event missing")


def nothing_started(ev, k):
    check(f"event {k}: nothing started", not starts(ev.get(k, [])), [b["skill"] for b in starts(ev.get(k, []))])


def nudge(ev, k, issue, worker):
    e = ev.get(k, [])
    check(f"event {k}: one nudge record on {issue}", len(comments(e, issue, "<!-- team-lead nudge -->")) == 1)
    check(f"event {k}: one nudge message to {worker}", len(messages(e, worker)) == 1)
    check(f"event {k}: no stop and no fresh worker yet", not stops(e) and not starts(e))


def stop(ev, k, worker):
    e = ev.get(k, [])
    check(f"event {k}: still silent after its nudge: {worker} stopped through the harness", len(stops(e, worker)) == 1)
    check(f"event {k}: no fresh worker before the stop reads back, no second nudge",
          not starts(e) and not comments(e, marker="<!-- team-lead nudge -->"))


def replace(ev, k, issue, skill, branch, old):
    e = ev.get(k, [])
    s = starts(e, skill, issue)
    check(f"event {k}: one fresh {skill} worker on {issue}", len(s) == 1, [b["skill"] + " " + b["issue"] for b in starts(e)])
    if s:
        check(f"event {k}: its brief names the pushed branch {branch} and the tracker", branch in s[0]["brief"]
              and re.search(r"tracker|issue", s[0]["brief"], re.I), s[0]["brief"][:200])
    rec = comments(e, issue, "<!-- team-lead start -->")
    check(f"event {k}: its start record names the worker it takes over from ({old})",
          any("Takes over from" in b["body"] and old in b["body"] for b in rec), [b["body"][:160] for b in rec])


def park(ev, k, issue):
    e = ev.get(k, [])
    check(f"event {k}: {issue} parked with the Park operation (label and parked record)",
          parks(e, issue) and comments(e, issue, "<!-- team-lead parked -->"))
    check(f"event {k}: the user told once", len(user(e)) == 1, len(user(e)))
    check(f"event {k}: no fresh worker on {issue}", not starts(e, issue=issue))


def arranged_before_first_build(ev, k):
    e1, e = ev.get(1, []), ev.get(k, [])
    check("event 1: one Release worker with release, no build worker, and no check-in yet (a planning-only Release worker)",
          len(starts(e1, "release")) == 1 and len(starts(e1)) == 1 and not ops(e1, "Arrange a check-in"),
          [b["op"] for b in e1])
    arr = [i for i, b in enumerate(e) if b["op"].startswith("Arrange a check-in")]
    first = [i for i, b in enumerate(e) if b["op"].startswith("Start a worker")]
    check(f"event {k}: the check-in arranged every hour through the Harness, before the first build worker starts",
          arr and first and arr[0] < first[0] and any(re.search(r"1 ?h|hour|60", e[i]["f"].get("Every", "")) for i in arr),
          [b["op"] for b in e])


def score_deliver(ev):
    arranged_before_first_build(ev, 2)
    e2 = ev.get(2, [])
    s = starts(e2, "implement-spec", "10-")
    check("event 2: one Spec worker with implement-spec on 10, only", len(s) == 1 and len(starts(e2)) == 1,
          [b["skill"] + " " + b["issue"] for b in starts(e2)])
    if s:
        check("event 2: its brief names tier regular and Review depth Deep",
              re.search(r"regular", s[0]["brief"] + s[0]["f"].get("Tier", ""), re.I) and "Deep" in s[0]["brief"])
    check("event 2: a start record on 10", comments(e2, "10-", "<!-- team-lead start -->"))
    quiet(ev, 3, "10 active")
    e4 = ev.get(4, [])
    check("event 4: the repo's merge-time step: 0.4.0 recorded on 10", any("0.4.0" in b["body"] and "version hand-out" in b["body"]
                                                                           for b in comments(e4, "10-")))
    check("event 4: the worker is told", messages(e4, "w-10-0920"))
    nothing_started(ev, 4)
    e5 = ev.get(5, [])
    reread = [i for i, b in enumerate(e5) if b["issue"].startswith("20-") and b["op"].startswith(("Comment", "Edit"))]
    st = [i for i, b in enumerate(e5) if b["op"].startswith("Start a worker") and b["issue"].startswith("20-")]
    check("event 5: 20 re-read after the skill change, before its worker starts", reread and st and reread[0] < st[0],
          [b["op"] + " " + b["issue"] for b in e5])
    if st:
        brief = e5[st[0]]["brief"]
        check("event 5: the implement worker on 20 names no Review depth", e5[st[0]]["skill"] == "implement"
              and not re.search(r"Review depth:? *(Quick|Standard|Deep)", brief), brief[:200])
    e6 = ev.get(6, [])
    check("event 6: pull request #8 ready but not reported: the worker told, no nudge",
          messages(e6, "w-20-1055") and not comments(e6, marker="<!-- team-lead nudge -->"))
    check("event 6: no version number for #8 (no skill file)", not any("version hand-out" in b["body"] for b in comments(e6)))
    e7 = ev.get(7, [])
    check("event 7: a Release worker cuts Release 1", len(starts(e7, "release")) == 1 and len(starts(e7)) == 1)
    quiet(ev, 8, "the Release worker active")
    e9 = ev.get(9, [])
    check("event 9: nothing started; the user told which feature waits (25, on 35)",
          not starts(e9) and any("25" in b["body"] and "35" in b["body"] for b in user(e9)))
    e10 = ev.get(10, [])
    check("event 10: 35 closed: a Release worker plans Release 2", len(starts(e10, "release")) == 1 and len(starts(e10)) == 1)
    e11 = ev.get(11, [])
    s = starts(e11, "implement", "25-")
    check("event 11: an implement worker on 25 at the cheap tier", len(s) == 1 and
          re.search(r"cheap", s[0]["f"].get("Tier", "") + s[0]["brief"], re.I))
    quiet(ev, 12, "25 active")
    nudge(ev, 13, "25-", "w-25-1420")
    stop(ev, 14, "w-25-1420")
    replace(ev, 15, "25-", "implement", "t25", "w-25-1420")
    e16 = ev.get(16, [])
    check("event 16: #11 ready but not reported: the fresh worker told, no nudge, no stop",
          messages(e16, "w-25-1705") and not comments(e16, marker="<!-- team-lead nudge -->") and not stops(e16))
    e17 = ev.get(17, [])
    check("event 17: a Release worker cuts Release 2", len(starts(e17, "release")) == 1 and len(starts(e17)) == 1)
    e18 = ev.get(18, [])
    check("event 18: delivery done: the check-in ended through the harness", ops(e18, "End a check-in"))
    nothing_started(ev, 18)
    allb = [b for k in ev for b in ev[k]]
    check("throughout: the Milestone issue body and every label left alone",
          not any(b["op"].startswith("Edit an issue body") and b["issue"].startswith("00-") for b in allb)
          and not ops(allb, "Apply / remove labels"))
    check("throughout: the check-in arranged once", len(ops(allb, "Arrange a check-in")) == 1)


def score_stall(ev, lift=False):
    arranged_before_first_build(ev, 2)
    check("event 2: the Spec worker on 10", len(starts(ev.get(2, []), "implement-spec", "10-")) == 1)
    quiet(ev, 3, "10 started 40 minutes ago")
    nudge(ev, 4, "10-", "w-10-0920")
    stop(ev, 5, "w-10-0920")
    park(ev, 6, "10-")
    s = starts(ev.get(6, []), "implement", "20-")
    check("event 6: the loop goes on: an implement worker on 20", len(s) == 1)
    e7 = ev.get(7, [])
    replace(ev, 7, "20-", "implement", "t20", "w-20-1205")
    check("event 7: a failed worker needs no nudge or stop", not stops(e7) and not messages(e7))
    quiet(ev, 8, "the fresh worker active")
    nudge(ev, 9, "20-", "w-20-1230")
    stop(ev, 10, "w-20-1230")
    park(ev, 11, "20-")
    quiet(ev, 12, "every feature parked or waiting")
    later = [b for k in ev if 7 <= k <= 12 for b in ev[k]]
    check("events 7 to 12: nothing written for 10 and the user not told of it again",
          not any(b["issue"].startswith("10-") for b in later) and not any("10-farewell" in b["body"] for b in user(later)))
    if not lift:
        return
    e13 = ev.get(13, [])
    check("event 13: 10's park lifted: its last worker (still idle) stopped before any fresh worker",
          stops(e13, "w-10-0920") and not starts(e13))
    park(ev, 14, "10-")
    e15 = ev.get(15, [])
    replace(ev, 15, "20-", "implement", "t20", "w-20-1230")
    check("event 15: 20's last worker already reads stopped: no stop", not stops(e15))
    quiet(ev, 16, "the fresh worker on 20 just started; 10 parked")


def score_pause(ev):
    arranged_before_first_build(ev, 2)
    e2 = ev.get(2, [])
    check("event 2: up to 2 at once: workers on 10 and 20, not 25",
          len(starts(e2, "implement-spec", "10-")) == 1 and len(starts(e2, "implement", "20-")) == 1 and not starts(e2, issue="25-"))
    e3 = ev.get(3, [])
    check("event 3: one pause record on the Milestone issue with the user's words",
          len(comments(e3, "00-", "<!-- team-lead pause -->")) == 1 and any("pause" in b["body"].lower() and "Please pause" in b["body"]
                                                                             for b in comments(e3, "00-")))
    check("event 3: each running worker asked to push and stop at its next natural step",
          messages(e3, "w-10-0920") and messages(e3, "w-20-0920"))
    check("event 3: the user told in one line", len(user(e3)) == 1)
    nothing_started(ev, 3)
    nothing_started(ev, 4)
    check("event 4: no nudge or stop while paused", not stops(ev.get(4, [])) and not comments(ev.get(4, []), marker="nudge"))
    quiet(ev, 5, "paused")
    quiet(ev, 6, "paused, 10 silent since 10:29")
    e7 = ev.get(7, [])
    check("event 7: one resume record with the user's words", len(comments(e7, "00-", "<!-- team-lead resume -->")) == 1
          and any("Resume delivery" in b["body"] for b in comments(e7, "00-")))
    check("event 7: 10's worker told to carry on", messages(e7, "w-10-0920"))
    s = starts(e7, "implement", "25-")
    check("event 7: the free slot takes 25", len(s) == 1 and len(starts(e7)) == 1, [b["issue"] for b in starts(e7)])
    quiet(ev, 8, "10 active from its resume, 25 active")
    e9 = ev.get(9, [])
    nudge(ev, 9, "10-", "w-10-0920")
    check("event 9: 25 not nudged", not messages(e9, "w-25-1230") and not comments(e9, "25-"))
    allb = [b for k in ev for b in ev[k]]
    check("throughout: one pause and one resume record, nothing parked",
          len(comments(allb, marker="<!-- team-lead pause -->")) == 1 and len(comments(allb, marker="<!-- team-lead resume -->")) == 1
          and not ops(allb, "Apply / remove labels"))


def score_earlier(ev):
    allb = [b for k in ev for b in ev[k]]
    check("throughout: no second worker on 10: the old delivery-thread record names its running worker",
          not starts(allb, issue="10-"), [b["skill"] + " " + b["issue"] for b in starts(allb)])
    e1 = ev.get(1, [])
    check("event 1: one resume record (the old milestone pause record counts)",
          len(comments(e1, "00-", "<!-- team-lead resume -->")) == 1)
    check("event 1: the old check-in had ended and a build worker runs: the check-in arranged", ops(e1, "Arrange a check-in"))
    check("event 1: the running worker told to carry on", messages(e1, "w-10-0800"))
    quiet(ev, 2, "w-10-0800 active")
    e3 = ev.get(3, [])
    s = starts(e3, "implement", "20-")
    check("event 3: 10 merged: the next feature, 20, starts with implement", len(s) == 1 and len(starts(e3)) == 1,
          [b["skill"] + " " + b["issue"] for b in starts(e3)])
    check("throughout: the old records left as they are (no edit, no label)",
          not ops(allb, "Edit an issue body") and not ops(allb, "Apply / remove labels"))


def main():
    if len(sys.argv) != 3 or sys.argv[2] not in ("deliver", "deliver-stall", "deliver-pause", "deliver-lift", "deliver-earlier"):
        print(__doc__, file=sys.stderr)
        return 2
    ev = parse_events((pathlib.Path(sys.argv[1]) / "repo/.scratch/proposed-actions.md").read_text())
    {"deliver": score_deliver, "deliver-stall": score_stall, "deliver-pause": score_pause,
     "deliver-lift": lambda e: score_stall(e, lift=True), "deliver-earlier": score_earlier}[sys.argv[2]](ev)
    print(f"{sum(results)}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
