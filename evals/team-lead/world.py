#!/usr/bin/env python3
"""The team-lead dry run's world: moves a fixture repo to the state the tracker, git and the harness show at event k.

Copied into a fixture as .scratch/world.py by make-fixture.sh and run there as `python3 .scratch/world.py <k>`, from
the repo root, for events 2 onward in order. It stands in for the workers, the merges, the user's own tracker
actions and the harness. It also applies the coordinator's comment and label writes from .scratch/proposed-actions.md
to the issue files, as the tracker would have, so the next event's reads (and the snapshot command) see them.
See evals/team-lead/README.md.
"""
import pathlib
import re
import subprocess
import sys
import os

R = pathlib.Path(".")
S = R / ".scratch"
DAY = "2026-11-03"


def t(hhmm):
    return f"{DAY}T{hhmm}:00Z"


# --- primitives -----------------------------------------------------------------------------------------------


def issue_path(name):
    return S / "issues" / name


def header(name, key, value):
    p = issue_path(name)
    text = p.read_text()
    text = re.sub(rf"^{key}:.*$", f"{key}: {value}", text, count=1, flags=re.M)
    p.write_text(text)


def labels(name, add=(), remove=()):
    p = issue_path(name)
    m = re.search(r"^Labels:(.*)$", p.read_text(), re.M)
    have = [l.strip() for l in m.group(1).split(",") if l.strip()]
    have = [l for l in have if l not in remove] + [l for l in add if l not in have]
    header(name, "Labels", ", ".join(have))


def comment(name, hhmm, author, text):
    p = issue_path(name)
    body = p.read_text()
    if "\n## Comments" not in body:
        body = body.rstrip("\n") + "\n\n## Comments\n"
    p.write_text(body.rstrip("\n") + f"\n\n### {t(hhmm) if len(hhmm) == 5 else hhmm} {author}\n\n{text}\n")


def new_issue(name, title, kind, labs, body):
    issue_path(name).write_text(f"Title: {title}\nType: {kind}\nLabels: {labs}\nStatus: open\nParent: none\n"
                                f"Blocked by: none\n\n{body}\n\n## Comments\n")


def close(name):
    header(name, "Status", "closed")


def commit(branch, hhmm, subject):
    env = dict(os.environ, GIT_AUTHOR_DATE=t(hhmm), GIT_COMMITTER_DATE=t(hhmm), GIT_AUTHOR_NAME="worker",
               GIT_AUTHOR_EMAIL="worker@example.com", GIT_COMMITTER_NAME="worker",
               GIT_COMMITTER_EMAIL="worker@example.com")
    def g(*a):
        subprocess.run(["git", *a], check=True, env=env, capture_output=True)
    exists = subprocess.run(["git", "rev-parse", "--verify", "-q", branch], capture_output=True).returncode == 0
    # Commit on the branch without touching the working tree: a worktree-free commit of one file.
    parent = branch if exists else "main"
    tree_file = f"work/{branch}.txt"
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=subject + "\n", text=True,
                          capture_output=True, check=True).stdout.strip()
    idx = S / f"index-{branch}"
    ienv = dict(env, GIT_INDEX_FILE=str(idx))
    subprocess.run(["git", "read-tree", parent], env=ienv, check=True)
    subprocess.run(["git", "update-index", "--add", "--cacheinfo", f"100644,{blob},{tree_file}"], env=ienv, check=True)
    tree = subprocess.run(["git", "write-tree"], env=ienv, capture_output=True, text=True, check=True).stdout.strip()
    idx.unlink()
    c = subprocess.run(["git", "commit-tree", tree, "-p", parent, "-m", subject], env=env, capture_output=True,
                       text=True, check=True).stdout.strip()
    g("update-ref", f"refs/heads/{branch}", c)


def pull(n, builds, state, opened, changed, ready="", merged=""):
    lines = [f"Builds: {builds}", f"Branch: t{builds[:2]}", f"State: {state}", f"Opened: {t(opened)}"]
    lines += [f"Ready: {t(ready)}"] if ready else []
    lines += [f"Merged: {t(merged)}"] if merged else []
    lines += [f"Changed: {changed}", "Checks: passing", "", "## Comments", ""]
    (S / "pulls" / f"{n}.md").write_text("\n".join(lines) + "\n")


def worker(wid, issue, branch, state, hhmm):
    p = S / "harness/workers.md"
    lines = [l for l in p.read_text().splitlines() if l.strip() and not l.startswith(wid + " ")]
    lines.append(f"{wid} {issue} branch {branch}: {state} since {t(hhmm)}")
    p.write_text("\n".join(lines) + "\n")


def checkin(text):
    (S / "harness/checkins.md").write_text(text + "\n")


# --- the coordinator's tracker writes, applied as the tracker would ------------------------------------------


def apply_writes():
    actions = (S / "proposed-actions.md").read_text() if (S / "proposed-actions.md").exists() else ""
    done = int((S / "applied").read_text()) if (S / "applied").exists() else 0
    clocks = dict(l.split(" ", 1) for l in (S / "clock").read_text().splitlines() if l.strip())
    event = "1"
    n = 0
    for part in re.split(r"^(## Event \d+)\s*$", actions, flags=re.M):
        m = re.match(r"## Event (\d+)", part)
        if m:
            event = m.group(1)
            continue
        for b in re.finditer(r"^### (\d+)\. (.+?)\n(.*?)(?=^### \d+\. |\Z)", part, re.S | re.M):
            n += 1
            if n <= done:
                continue
            op, rest = b.group(2).strip(), b.group(3)
            im = re.search(r"^Issue:\s*(\S+)", rest, re.M)
            name = pathlib.Path(im.group(1)).name if im else ""
            if not name or not issue_path(name).exists():
                continue
            if op.startswith("Comment on an issue"):
                bm = re.search(r"^Body:\s*\n~~~\n(.*?)\n~~~", rest, re.S | re.M)
                if bm:
                    comment(name, clocks.get(event, "00:00"), "coordinator", bm.group(1))
            elif op.startswith("Apply / remove labels"):
                add = re.search(r"^Add:\s*(.*)$", rest, re.M)
                rem = re.search(r"^Remove:\s*(.*)$", rest, re.M)
                split = lambda m_: [x.strip() for x in m_.group(1).split(",") if x.strip() and x.strip() != "none"] if m_ else []
                labels(name, split(add), split(rem))
    (S / "applied").write_text(str(n))


# --- the worlds ---------------------------------------------------------------------------------------------

M = "00-milestone.md"


def release_one(features):
    new_issue("40-release-m1-r1.md", "Release Milestone 1 · Release 1", "release", "release-m1-r1",
              "**Milestone:** 00-milestone.md\n\nGoal: " + ", ".join(features) + ".\n\nMaintenance fixes: none.")
    for f in features:
        labels(f, ["release-m1-r1"])
    worker("w-00-0900", M, "none", "ended", "09:19")


def common(k, features):
    if k == 2:
        release_one(features)
    if k == 3:
        checkin("Every 1 hour into the coordinator, on the hour.")


def deliver(k):
    common(k, ["10-farewell.md", "11-bye-code.md", "12-bye-usage.md", "20-quiet.md"])
    if k == 3:
        commit("t10", "09:50", "farewell: the bye command")
        worker("w-10-0920", "10-farewell.md", "t10", "working", "09:20")
    elif k == 4:
        pull(7, "10-farewell.md", "open", "10:30", "skills/greeting/SKILL.md, src/greet.sh, test.sh", ready="10:35")
    elif k == 5:
        (R / "VERSION").write_text("0.4.0\n")
        skill = R / "skills/greeting/SKILL.md"
        skill.write_text(skill.read_text() + "- A farewell is `Goodbye, <name>!`; every message, farewells included, is printed by one `say` function.\n")
        pull(7, "10-farewell.md", "merged", "10:30", "skills/greeting/SKILL.md, src/greet.sh, test.sh", ready="10:35",
             merged="10:52")
        for f in ("10-farewell.md", "11-bye-code.md", "12-bye-usage.md"):
            close(f)
        worker("w-10-0920", "10-farewell.md", "t10", "ended", "10:53")
    elif k == 6:
        commit("t20", "11:40", "quiet: the --quiet flag")
        pull(8, "20-quiet.md", "open", "11:50", "src/greet.sh, test.sh", ready="11:55")
        worker("w-20-1055", "20-quiet.md", "t20", "idle", "11:56")
    elif k == 7:
        pull(8, "20-quiet.md", "merged", "11:50", "src/greet.sh, test.sh", ready="11:55", merged="12:15")
        close("20-quiet.md")
        worker("w-20-1055", "20-quiet.md", "t20", "ended", "12:16")
    elif k == 8:
        commit("t40", "12:40", "changelog: Milestone 1 · Release 1")
        comment("40-release-m1-r1.md", "12:41", "w-40-1220", "Whole-Release check running.")
        worker("w-40-1220", "40-release-m1-r1.md", "t40", "working", "12:20")
    elif k == 9:
        close("40-release-m1-r1.md")
        worker("w-40-1220", "40-release-m1-r1.md", "t40", "ended", "13:28")
    elif k == 10:
        close("35-readme-tool.md")
        comment("35-readme-tool.md", "13:50", "user", "Picked the checker; closing.")
    elif k == 11:
        new_issue("41-release-m1-r2.md", "Release Milestone 1 · Release 2", "release", "release-m1-r2",
                  "**Milestone:** 00-milestone.md\n\nGoal: document the commands.\n\nMaintenance fixes: none.")
        labels("25-hello-doc.md", ["release-m1-r2"])
        worker("w-00-1400", M, "none", "ended", "14:18")
    elif k == 12:
        commit("t25", "14:40", "readme: hello and bye")
        worker("w-25-1420", "25-hello-doc.md", "t25", "working", "14:20")
    elif k == 13:
        worker("w-25-1420", "25-hello-doc.md", "t25", "idle", "14:41")
    elif k == 14:
        pass
    elif k == 15:
        worker("w-25-1420", "25-hello-doc.md", "t25", "stopped", "17:03")
    elif k == 16:
        commit("t25", "17:40", "readme: examples")
        pull(11, "25-hello-doc.md", "open", "17:45", "README.md", ready="17:50")
        worker("w-25-1705", "25-hello-doc.md", "t25", "idle", "17:51")
    elif k == 17:
        pull(11, "25-hello-doc.md", "merged", "17:45", "README.md", ready="17:50", merged="18:08")
        close("25-hello-doc.md")
        worker("w-25-1705", "25-hello-doc.md", "t25", "ended", "18:09")
    elif k == 18:
        close("41-release-m1-r2.md")
        worker("w-41-1810", "41-release-m1-r2.md", "t41", "ended", "18:38")


def stall(k):
    common(k, ["10-farewell.md", "11-bye-code.md", "12-bye-usage.md", "20-quiet.md"])
    if k == 3:
        worker("w-10-0920", "10-farewell.md", "t10", "working", "09:20")
    elif k == 4:
        worker("w-10-0920", "10-farewell.md", "t10", "idle", "09:40")
    elif k == 5:
        pass
    elif k == 6:
        pass  # the stop was asked for; the harness still reads the worker idle since 09:40
    elif k == 7:
        commit("t20", "12:20", "quiet: the --quiet flag")
        worker("w-20-1205", "20-quiet.md", "t20", "failed", "12:28")
    elif k == 8:
        commit("t20", "12:50", "quiet: keep the exit code")
        worker("w-20-1230", "20-quiet.md", "t20", "working", "12:30")
    elif k == 9:
        worker("w-20-1230", "20-quiet.md", "t20", "idle", "12:51")
    elif k == 10:
        pass
    elif k == 11:
        worker("w-20-1230", "20-quiet.md", "t20", "stopped", "15:03")
    elif k == 12:
        pass


def lift(k):
    if k <= 12:
        return stall(k)
    if k == 13:
        labels("10-farewell.md", remove=["parked"])
        comment("10-farewell.md", "16:28", "user", "Removed the parked label: the farewell wording is settled, carry on.")
    elif k == 14:
        pass  # the stop was asked for again; the harness still reads w-10-0920 idle since 09:40
    elif k == 15:
        labels("20-quiet.md", remove=["parked"])
        comment("20-quiet.md", "16:48", "user", "Removed the parked label: keep the exit code in its own function.")
    elif k == 16:
        worker("w-20-1650", "20-quiet.md", "t20", "working", "16:50")


def pause(k):
    common(k, ["10-farewell.md", "11-bye-code.md", "12-bye-usage.md", "20-quiet.md", "25-hello-doc.md"])
    if k == 3:
        commit("t10", "10:10", "farewell: the bye command")
        commit("t20", "10:12", "quiet: the --quiet flag")
        worker("w-10-0920", "10-farewell.md", "t10", "working", "09:20")
        worker("w-20-0920", "20-quiet.md", "t20", "working", "09:20")
    elif k == 4:
        pull(8, "20-quiet.md", "merged", "10:30", "src/greet.sh, test.sh", ready="10:32", merged="10:38")
        close("20-quiet.md")
        worker("w-20-0920", "20-quiet.md", "t20", "ended", "10:39")
        commit("t10", "10:28", "farewell: usage text")
        comment("10-farewell.md", "10:29", "w-10-0920", "Pushed `farewell: usage text`; stopping here until told to carry on.")
        worker("w-10-0920", "10-farewell.md", "t10", "idle", "10:29")
    elif k == 5:
        pass
    elif k == 6:
        pass
    elif k == 7:
        pass
    elif k == 8:
        # 10's worker carries on but pushes nothing yet: only the resume makes it active.
        worker("w-10-0920", "10-farewell.md", "t10", "working", "12:31")
        worker("w-25-1230", "25-hello-doc.md", "t25", "working", "12:30")
    elif k == 9:
        commit("t25", "13:40", "readme: hello and bye")
        worker("w-10-0920", "10-farewell.md", "t10", "idle", "12:46")  # still nothing pushed since 10:28


def earlier(k):
    # Delivery resumes on a Milestone whose records are the earlier milestone loop's: 10's Spec worker, started before
    # the pause and named only by an old delivery-thread record, still runs.
    if k == 2:
        commit("t10", "09:30", "farewell: usage text")
        checkin("Every 1 hour into the coordinator, on the hour.")
    elif k == 3:
        pull(7, "10-farewell.md", "merged", "09:40", "src/greet.sh, test.sh", ready="09:45", merged="10:10")
        for f in ("10-farewell.md", "11-bye-code.md", "12-bye-usage.md"):
            close(f)
        worker("w-10-0800", "10-farewell.md", "t10", "ended", "10:11")


WORLDS = {"deliver": deliver, "stall": stall, "lift": lift, "pause": pause, "earlier": earlier}
LAST = {"deliver": 18, "stall": 12, "lift": 16, "pause": 9, "earlier": 3}


def main():
    k = int(sys.argv[1])
    variant = (S / "variant").read_text().strip()
    cur = int((S / "stage").read_text())
    if k == 1 and cur == 1:
        print("world at event 1 (the fixture starts here; nothing to run)")
        return 0
    if k != cur + 1 or k > LAST[variant]:
        print(f"at stage {cur}; next is {cur + 1} (last {LAST[variant]})", file=sys.stderr)
        return 2
    apply_writes()
    WORLDS[variant](k)
    (S / "stage").write_text(str(k))
    print(f"world at event {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
