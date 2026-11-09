#!/usr/bin/env python3
"""Regression guard: duration totals must be attributed to the right subjects."""
import json
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parent
for case in ("green-initial", "ready-final"):
    source = root / "evidence" / case
    normal = subprocess.run(["python3", str(root / "score.py"), str(source), "ready"], capture_output=True, text=True)
    assert normal.returncode == 0, normal.stdout
    actions = json.loads((source / "actions.json").read_text())
    changed = 0
    for action in actions:
        if "<!-- milestone report -->" not in action.get("body", ""):
            continue
        rows = action["body"].splitlines()
        for i, row in enumerate(rows):
            if row.startswith("| coordinator / milestone |"):
                rows[i] = row.replace("| 120 min |", "| 50 min |")
                changed += 1
            elif row.startswith("| build-10 / implement |"):
                rows[i] = row.replace("| 50 min |", "| 120 min |")
                changed += 1
        action["body"] = "\n".join(rows)
    assert changed == 2
    with tempfile.TemporaryDirectory() as scratch:
        Path(scratch, "actions.json").write_text(json.dumps(actions))
        swapped = subprocess.run(["python3", str(root / "score.py"), scratch, "ready"], capture_output=True, text=True)
    assert swapped.returncode == 1, f"{case}: swapped thread durations incorrectly passed"
    assert "FAIL coordinator elapsed is two hours" in swapped.stdout, swapped.stdout
    assert "FAIL build-10 elapsed is 50 minutes" in swapped.stdout, swapped.stdout
    print(f"PASS {case}: normal passes; swapped coordinator/build-10 durations fail")
    for subject, correct_range, contradictory_range in (
        ("coordinator", "10:00–12:00", "10:00–11:00"),
        ("build-10", "10:10–11:00", "10:10–12:00"),
    ):
        contradictory = json.loads((source / "actions.json").read_text())
        changed = 0
        for action in contradictory:
            if "<!-- milestone report -->" not in action.get("body", ""):
                continue
            rows = action["body"].splitlines()
            for i, row in enumerate(rows):
                if row.startswith(f"| {subject} /"):
                    assert correct_range in row
                    rows[i] = row.replace(correct_range, contradictory_range)
                    changed += 1
            action["body"] = "\n".join(rows)
        assert changed == 1
        with tempfile.TemporaryDirectory() as scratch:
            Path(scratch, "actions.json").write_text(json.dumps(contradictory))
            result = subprocess.run(["python3", str(root / "score.py"), scratch, "ready"], capture_output=True, text=True)
        assert result.returncode == 1, f"{case}: contradictory {subject} time range incorrectly passed"
        assert f"FAIL {subject} start/end match session evidence" in result.stdout, result.stdout
        print(f"PASS {case}: contradictory {subject} time range fails")

# accepted case: fixture self-test and scorer regression
import subprocess, tempfile, json, sys
from pathlib import Path
_here = Path(__file__).parent
with tempfile.TemporaryDirectory() as _t:
    _d = Path(_t) / "acc"
    subprocess.run([sys.executable, str(_here / "make-fixture.py"), str(_d), "accepted"], check=True)
    _r = json.loads((_d / "records.json").read_text())
    _ok = (_r["checkins"]["running"] is False and _r["releases"][0]["cut_done"] and _r["user_message_now"]["id"] == "chat://coordinator/u9"
           and _r["user_message_now"]["time"] < _r["milestone"]["now"] and _r["milestone"]["state"] == "open"
           and any("<!-- milestone report -->" in x["body"] for x in _r["existing_tracker_and_scheduler_actions"])
           and all(f["state"] == "closed" for f in _r["features"]))
    print(("PASS" if _ok else "FAIL") + " accepted: rendered records say report posted, check-ins ended, cut done, M1 open, acceptance message after")
    _bad = _ok
    def _score(actions):
        (_d / "actions.json").write_text(json.dumps(actions))
        return subprocess.run([sys.executable, str(_here / "score.py"), str(_d), "accepted"], capture_output=True).returncode
    _good = [{"operation": "comment", "target": "M1", "body": "Accepted in chat://coordinator/u9 at 13:00Z"}, {"operation": "close", "target": "M1", "body": ""}, {"operation": "message-user", "target": "u", "body": "closed"}]
    _c1 = _score(_good) == 0
    _c2 = _score([]) != 0
    _c3 = _score(_good + [{"operation": "start-thread", "target": "R1", "body": "release"}]) != 0
    _c4 = _score([{"operation": "close", "target": "M1", "body": "done"}]) != 0
    print(("PASS" if _c1 else "FAIL") + " accepted: reference run passes")
    print(("PASS" if _c2 and _c3 and _c4 else "FAIL") + " accepted: no close, extra thread start, and close without acceptance note each fail")
    if not (_ok and _c1 and _c2 and _c3 and _c4):
        raise SystemExit(1)
