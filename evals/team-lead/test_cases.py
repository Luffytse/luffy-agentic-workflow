#!/usr/bin/env python3
"""Self-test of the team-lead dry-run cases: fixture, world, snapshot verdicts and scorer agree.

Run: python3 evals/team-lead/test_cases.py
For each case it builds the fixture, replays a reference run written by hand from the skill text (REFERENCE below),
event by event as a coordinator would (world.py first, then that event's blocks), checks at every check-in that the
snapshot command prints the verdicts the case is built to show, and scores the run: the reference must pass, and a
planted wrong run (a quiet check-in that writes, a takeover before the stop reads back, a pause that starts work) must
fail. It is not a model run: see evals/team-lead/README.md and RESULTS.md for what that leaves owed.
"""
import pathlib
import subprocess
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SNAPSHOT = HERE.parents[1] / "plugins/dev-skills/skills/team-lead/snapshot.py"
D = "2026-11-03T"


def start(issue, skill, tier, brief):
    return f"Start a worker\nIssue: {issue}\nSkill: {skill}\nTier: {tier}\nBrief:\n~~~\n{brief}\n~~~\n"


def comment(issue, body):
    return f"Comment on an issue\nIssue: {issue}\nBody:\n~~~\n{body}\n~~~\n"


def rec(issue, worker, skill, tier, when, extra=""):
    return comment(issue, f"<!-- team-lead start -->\nStarted {worker} with {skill}, tier {tier}, at {when}." + extra)


def msg(worker, body):
    return f"Message a worker\nWorker: {worker}\nBody:\n~~~\n{body}\n~~~\n"


def stop(worker):
    return f"Stop a worker\nWorker: {worker}\n"


def user(body):
    return f"Message the user\nBody:\n~~~\n{body}\n~~~\n"


def label(issue, add):
    return f"Apply / remove labels\nIssue: {issue}\nAdd: {add}\nRemove: none\n"


def nudge(issue, worker, since):
    return [msg(worker, f"Where are you and what blocks you? Answer with a comment on {issue}."),
            comment(issue, f"<!-- team-lead nudge -->\nNudged {worker}: nothing pushed, commented or changed since {since}.")]


def parked(issue, why, writer):
    return [label(issue, "parked"),
            comment(issue, f"<!-- team-lead parked -->\nParked: {why}. {writer} History: the start and nudge records above."),
            user(f"Parked {issue}: {why}.")]


M = "00-milestone.md"
RELEASE_START = [start(M, "release", "premium", "Plan Milestone 1's next Release by the release skill's rule. Milestone issue 00-milestone.md, release doc docs/dev-skills/release.md; no Release cut yet. If nothing qualifies, open no release issue and say so."),
                 rec(M, "w-00-0900", "release", "premium", "09:00Z")]
E1 = RELEASE_START
ARRANGE = [f"Arrange a check-in\nEvery: 1 hour\nInto: coordinator\n", comment(M, "<!-- team-lead check-in -->\nArranged every 1 hour into the coordinator.")]
SPEC10 = ARRANGE + [start("10-farewell.md", "implement-spec", "regular", "Build Spec 10-farewell.md with implement-spec. Milestone issue 00-milestone.md. Model tier: regular. Review level: Deep. Repo: this one."),
          rec("10-farewell.md", "w-10-0920", "implement-spec", "regular", "09:20Z", " Review level Deep.")]
T20 = lambda when, wid: [start("20-quiet.md", "implement", "regular", "Build Ticket 20-quiet.md with implement. Milestone issue 00-milestone.md. Model tier: regular. Repo: this one."),
                         rec("20-quiet.md", wid, "implement", "regular", when)]

STALL = {
    1: E1, 2: SPEC10, 3: [],
    4: nudge("10-farewell.md", "w-10-0920", "09:20Z"),
    5: [stop("w-10-0920")],
    6: parked("10-farewell.md", "the stop of w-10-0920 did not read back (still idle since 09:40Z)",
              "A writer may remain.") + T20("12:05Z", "w-20-1205"),
    7: [start("20-quiet.md", "implement", "regular", "Take over Ticket 20-quiet.md with implement from w-20-1205, which failed: resume from the pushed branch t20 and the tracker (the issue, its comments, its pull request). Milestone issue 00-milestone.md. Model tier: regular."),
        rec("20-quiet.md", "w-20-1230", "implement", "regular", "12:30Z", "\nTakes over from w-20-1205; it read failed at 12:28Z.")],
    8: [],
    9: nudge("20-quiet.md", "w-20-1230", "12:50Z"),
    10: [stop("w-20-1230")],
    11: parked("20-quiet.md", "a second stall (w-20-1230, a replacement, still silent after its nudge)",
               "Its stop read back stopped at 15:03Z: no writer remains."),
    12: [],
}
LIFT = dict(STALL)
LIFT.update({
    13: [stop("w-10-0920")],
    14: parked("10-farewell.md", "after the lift, the stop of w-10-0920 again did not read back (idle since 09:40Z)",
               "A writer may remain."),
    15: [start("20-quiet.md", "implement", "regular", "Resume Ticket 20-quiet.md with implement after the user lifted its park: resume from the pushed branch t20 and the tracker (the issue, the user's comment, the parked record and the start and nudge records). Milestone issue 00-milestone.md. Model tier: regular."),
         rec("20-quiet.md", "w-20-1650", "implement", "regular", "16:50Z", "\nTakes over from w-20-1230; stop read back at 15:03Z.")],
    16: [],
})
DELIVER = {
    1: E1, 2: SPEC10, 3: [],
    4: [comment("10-farewell.md", "<!-- version hand-out -->\nVersion 0.4.0 for #7: merge it next, with the bump as its last commit."),
        msg("w-10-0920", "Version 0.4.0 for #7: merge it next with the bump as its last commit.")],
    5: [comment("20-quiet.md", "Re-read after #7 merged (the greeting skill's new rule): still fits; messages go through `say`."),
        ] + T20("10:55Z", "w-20-1055"),
    6: [msg("w-20-1055", "#8 reads ready: it changes no skill file, so no number: merge it with no bump.")],
    7: [start("40-release-m1-r1.md", "release", "premium", "Cut Milestone 1 · Release 1 (40-release-m1-r1.md) with release and plan the next one. Milestone issue 00-milestone.md. If nothing qualifies, open no release issue."),
        rec("40-release-m1-r1.md", "w-40-1220", "release", "premium", "12:20Z")],
    8: [],
    9: [user("No next Release yet: 25-hello-doc.md waits on 35-readme-tool.md.")],
    10: [start(M, "release", "premium", "Plan Milestone 1's next Release by the release skill's rule; the last release issue cut is 40-release-m1-r1.md. If nothing qualifies, open no release issue."),
         rec(M, "w-00-1400", "release", "premium", "14:00Z")],
    11: [start("25-hello-doc.md", "implement", "cheap", "Build Ticket 25-hello-doc.md with implement. Milestone issue 00-milestone.md. Model tier: cheap."),
         rec("25-hello-doc.md", "w-25-1420", "implement", "cheap", "14:20Z")],
    12: [],
    13: nudge("25-hello-doc.md", "w-25-1420", "14:40Z"),
    14: [stop("w-25-1420")],
    15: [start("25-hello-doc.md", "implement", "cheap", "Take over Ticket 25-hello-doc.md with implement from w-25-1420 (stopped): resume from the pushed branch t25 and the tracker. Milestone issue 00-milestone.md. Model tier: cheap."),
         rec("25-hello-doc.md", "w-25-1705", "implement", "cheap", "17:05Z", "\nTakes over from w-25-1420; stop read back at 17:03Z.")],
    16: [msg("w-25-1705", "#11 reads ready: README only, no number: merge it with no bump.")],
    17: [start("41-release-m1-r2.md", "release", "premium", "Cut Milestone 1 · Release 2 (41-release-m1-r2.md) with release and plan the next one. Milestone issue 00-milestone.md. If nothing qualifies, open no release issue."),
         rec("41-release-m1-r2.md", "w-41-1810", "release", "premium", "18:10Z")],
    18: ["End a check-in\n", comment(M, "<!-- team-lead check-in -->\nEnded; no check-in runs.")],
}
PAUSE = {
    1: E1,
    2: SPEC10 + T20("09:20Z", "w-20-0920"),
    3: [comment(M, '<!-- team-lead pause -->\nPaused at 10:20Z on the user\'s word: "Please pause delivery for now."'),
        msg("w-10-0920", "Pause: push your work and stop at your next natural step; wait for my word."),
        msg("w-20-0920", "Pause: push your work and stop at your next natural step; wait for my word."),
        user("Paused: nothing new starts; the two running workers stop at their next natural step.")],
    4: [], 5: [], 6: [],
    7: [comment(M, '<!-- team-lead resume -->\nResumed at 12:30Z on the user\'s word: "Resume delivery."'),
        msg("w-10-0920", "Resume: carry on from where you stopped."),
        start("25-hello-doc.md", "implement", "cheap", "Build Ticket 25-hello-doc.md with implement. Milestone issue 00-milestone.md. Model tier: cheap."),
        rec("25-hello-doc.md", "w-25-1230", "implement", "cheap", "12:30Z")],
    8: [],
    9: nudge("10-farewell.md", "w-10-0920", "the resume at 12:30Z"),
}
EARLIER = {
    1: [comment(M, '<!-- team-lead resume -->\nResumed at 09:00Z on the user\'s word: "Resume delivery." w-10-0800 (named by the earlier delivery-thread record on 10-farewell.md) reads working.'),
        ARRANGE[0], ARRANGE[1],
        msg("w-10-0800", "Resume: carry on from where you stopped.")],
    2: [],
    3: T20("10:15Z", "w-20-1015"),
}
REFERENCE = {"deliver": DELIVER, "deliver-stall": STALL, "deliver-lift": LIFT, "deliver-pause": PAUSE,
             "deliver-earlier": EARLIER}

# At each check-in: the workers the team lead passes to the snapshot, and the verdict each row must show.
W = lambda wid, issue, branch, started, pr="", resumed="": (f"id={wid};issue={issue};branch={branch};started={D}{started}:00Z"
                                                              + (f";pr={pr}" if pr else "") + (f";resumed={D}{resumed}:00Z" if resumed else ""))
SNAPSHOTS = {
    "deliver": {
        3: [(W("w-10-0920", 10, "t10", "09:20"), "active")],
        6: [(W("w-20-1055", 20, "t20", "10:55", 8), "pull request ready but not reported")],
        12: [(W("w-25-1420", 25, "t25", "14:20"), "active")],
        13: [(W("w-25-1420", 25, "t25", "14:20"), f"silent since {D}14:40:00Z")],
        14: [(W("w-25-1420", 25, "t25", "14:20"), f"still silent after its nudge at {D}16:00:00Z")],
        16: [(W("w-25-1705", 25, "t25", "17:05", 11), "pull request ready but not reported")],
    },
    "deliver-stall": {
        3: [(W("w-10-0920", 10, "t10", "09:20"), "active")],
        4: [(W("w-10-0920", 10, "t10", "09:20"), f"silent since {D}09:20:00Z")],
        5: [(W("w-10-0920", 10, "t10", "09:20"), f"still silent after its nudge at {D}11:00:00Z")],
        8: [(W("w-20-1230", 20, "t20", "12:30"), "active")],
        9: [(W("w-20-1230", 20, "t20", "12:30"), f"silent since {D}12:50:00Z")],
        10: [(W("w-20-1230", 20, "t20", "12:30"), f"still silent after its nudge at {D}14:00:00Z")],
    },
    "deliver-pause": {
        5: [(W("w-10-0920", 10, "t10", "09:20"), "active")],
        6: [(W("w-10-0920", 10, "t10", "09:20"), f"silent since {D}10:29:00Z")],
        8: [(W("w-10-0920", 10, "t10", "09:20"), f"silent since {D}10:29:00Z"),
            (W("w-10-0920", 10, "t10", "09:20", resumed="12:30"), "active"), (W("w-25-1230", 25, "t25", "12:30"), "active")],
        9: [(W("w-10-0920", 10, "t10", "09:20", resumed="12:30"), f"silent since {D}12:30:00Z"),
            (W("w-25-1230", 25, "t25", "12:30"), "active")],
    },
}
SNAPSHOTS["deliver-earlier"] = {2: [(W("w-10-0800", 10, "t10", "08:00"), "active")]}
SNAPSHOTS["deliver-lift"] = dict(SNAPSHOTS["deliver-stall"])
SNAPSHOTS["deliver-lift"][16] = [(W("w-20-1650", 20, "t20", "16:50"), "active")]


def render(run):
    out, n = [], 0
    for k in sorted(run):
        out.append(f"## Event {k}\n")
        for b in run[k]:
            n += 1
            out.append(f"### {n}. {b}")
    return "\n".join(out) + "\n"


def clock(repo, k):
    for line in (repo / ".scratch/clock").read_text().splitlines():
        num, hhmm = line.split()
        if int(num) == k:
            return f"{D}{hhmm}:00Z"
    raise KeyError(k)


def rows(output):
    table = [l for l in output.splitlines() if l.startswith("|")][2:]
    return {c[0]: c[-1] for c in ([x.strip() for x in l.strip("|").split("|")] for l in table)}


class Cases(unittest.TestCase):
    def replay(self, case, run):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        out = pathlib.Path(tmp.name) / "out"
        subprocess.run(["bash", str(HERE / "make-fixture.sh"), str(out), case], check=True, capture_output=True)
        repo = out / "repo"
        actions = repo / ".scratch/proposed-actions.md"
        for k in sorted(run):
            if k > 1:
                subprocess.run(["python3", ".scratch/world.py", str(k)], cwd=repo, check=True, capture_output=True)
            for spec, verdict in SNAPSHOTS.get(case, {}).get(k, []) if run is REFERENCE[case] else []:
                r = subprocess.run(["python3", str(SNAPSHOT), "--now", clock(repo, k), "--worker", spec],
                                   cwd=repo, text=True, capture_output=True)
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
                wid = spec.split(";")[0][3:]
                self.assertEqual(rows(r.stdout)[wid], verdict, f"{case} event {k}: {r.stdout}")
            actions.write_text(render({j: run[j] for j in run if j <= k}))
        return subprocess.run(["python3", str(HERE / "score.py"), str(out), case], text=True, capture_output=True)

    def test_each_reference_run_scores_clean_and_its_snapshots_read_as_built(self):
        for case, run in REFERENCE.items():
            with self.subTest(case=case):
                r = self.replay(case, run)
                self.assertEqual(r.returncode, 0, r.stdout)

    def test_a_quiet_check_in_that_writes_fails(self):
        run = dict(DELIVER)
        run[12] = [comment(M, "<!-- milestone stand-up -->\nCheck-in 15:00Z: 25 active; no decision.")]
        r = self.replay("deliver", run)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("FAIL event 12", r.stdout)

    def test_a_takeover_before_the_stop_reads_back_fails(self):
        run = dict(STALL)
        run[5] = [stop("w-10-0920")] + [start("10-farewell.md", "implement-spec", "regular", "Take over from w-10-0920 on branch t10 and the tracker.")]
        r = self.replay("deliver-stall", run)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("FAIL event 5", r.stdout)

    def test_a_second_worker_beside_an_old_record_fails(self):
        run = dict(EARLIER)
        run[1] = EARLIER[1] + [start("10-farewell.md", "implement-spec", "regular", "Build Spec 10-farewell.md.")]
        r = self.replay("deliver-earlier", run)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("FAIL throughout: no second worker on 10", r.stdout)

    def test_a_check_in_for_a_planning_only_release_worker_fails(self):
        run = dict(DELIVER)
        run[1] = ARRANGE + E1
        run[2] = SPEC10[2:]
        r = self.replay("deliver", run)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("FAIL event 1", r.stdout)

    def test_a_start_while_paused_fails(self):
        run = dict(PAUSE)
        run[4] = [start("25-hello-doc.md", "implement", "cheap", "Build Ticket 25-hello-doc.md.")]
        r = self.replay("deliver-pause", run)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("FAIL event 4", r.stdout)


if __name__ == "__main__":
    unittest.main()
