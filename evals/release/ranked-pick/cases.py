"""The ranked-pick cases of the release eval: each case's fixture data and the pick it expects.

make_fixture.py builds a case's repo from this data; score.py and test_cases.py read EXPECT. Keep this file, the
scorer and the README away from the session under test: EXPECT is the answer.

Issue numbers are the issue file prefixes (#10 is .scratch/issues/10-*.md). Every case shares the Milestone (#1),
the closed release issue of the last Release (#2, "Release 2", unless the case cuts it) and the fixture repo. The
Milestone's goal is GOAL unless the case names its own.
"""
import copy

GOAL = "Round out the greeter's commands."

# Base features of Milestone 1: the Spec farewell with two Tickets, and the lone Ticket quiet.
FAREWELL = [
    dict(n=10, slug="farewell", title="Farewell command", type="spec", labels=["ready-for-agent", "enhancement", "milestone-1"],
         created="2026-10-02", body="Add `greet.sh bye <name>`. Tickets: #11, #12."),
    dict(n=11, slug="bye-code", title="bye: the command", type="ticket", labels=["ready-for-agent", "enhancement", "milestone-1"],
         created="2026-10-02", parent=10, body="Part of #10\n\nPrint `Goodbye, <name>!`."),
    dict(n=12, slug="bye-usage", title="bye: usage text", type="ticket", labels=["ready-for-agent", "enhancement", "milestone-1"],
         created="2026-10-02", parent=10, body="Part of #10\n\nAdd `bye` to the usage line."),
]
QUIET = dict(n=20, slug="quiet", title="Quiet flag", type="ticket", labels=["ready-for-agent", "enhancement", "milestone-1"],
             created="2026-10-03", body="`-q` prints the greeting with no trailing newline.")


def bug(n, slug, title, created, body, labels=None):
    return dict(n=n, slug=slug, title=title, type="ticket", labels=labels or ["ready-for-agent", "bug"],
                created=created, body=body)


TYPO = bug(30, "usage-typo", "Typo in usage text", "2026-09-01", "The usage line says `greet.sh helo`. Should say `hello`.")

CASES = {
    # Group 1 before group 2 before group 3; a severe issue before an issue only marked next-release, though it is
    # newer; the mark is cleared from the marked issue once it is taken.
    "severe-first": dict(
        size=5,
        milestone=[10, 20],
        issues=FAREWELL + [QUIET, TYPO,
            bug(31, "name-log", "greet.sh writes every name to a world-readable log", "2026-10-20",
                "Every run appends the name given to `/tmp/greet.log`, mode 0666, readable by every user on the machine. "
                "Names include the email addresses some scripts pass. A security hole."),
            bug(35, "slow-test", "test.sh takes 10 s", "2026-10-02",
                "Retro planning for Release 2 marked this to join the next Release: `test.sh` sleeps 10 s for nothing.",
                labels=["ready-for-agent", "bug", "next-release"]),
        ],
    ),
    # A feature's open blocker (a ready-for-agent bug outside the Milestone) goes just before that feature.
    "blocker-first": dict(
        size=5,
        milestone=[10, 20],
        issues=FAREWELL + [dict(QUIET, blocked_by=[40]), TYPO,
            bug(40, "flag-parse", "Flags after the name are dropped", "2026-10-25",
                "`greet.sh hello Ada -x` ignores `-x`: the parser stops at the name. The quiet flag (#20) needs it."),
        ],
    ),
    # Ready-for-agent bugs fill the places the Milestone's features leave, oldest first; a bug still at needs-triage
    # is not a candidate.
    "bugs-fill": dict(
        size=5,
        milestone=[20, 21],
        issues=[QUIET,
            dict(n=21, slug="shout", title="Shout flag", type="ticket", labels=["ready-for-agent", "enhancement", "milestone-1"],
                 created="2026-10-04", body="`-s` prints the greeting in capitals."),
            TYPO,
            bug(31, "empty-name", "Empty name prints `Hello, !`", "2026-09-15", "`greet.sh hello ''` prints `Hello, !`."),
            bug(32, "exit-code", "Unknown command exits 0 from a pipe", "2026-10-01", "`greet.sh nope | cat` exits 0."),
            bug(33, "trailing-space", "Trailing space after the greeting", "2026-10-10", "Every greeting ends in a space."),
            bug(34, "unicode", "Names with accents come out mangled", "2026-08-01", "Reported, not yet triaged.",
                labels=["needs-triage", "bug"]),
        ],
    ),
    # An enhancement the Milestone issue does not list is never ranked, though it is ready-for-agent; an agent-found
    # one at ready-for-human neither.
    "unplanned-feature": dict(
        size=5,
        milestone=[10, 20],
        issues=FAREWELL + [QUIET, TYPO,
            dict(n=50, slug="colour", title="Colour output", type="ticket", labels=["ready-for-agent", "enhancement"],
                 created="2026-09-10", body="Print the greeting in green when stdout is a terminal."),
            dict(n=51, slug="lint", title="Run shellcheck in test.sh", type="ticket", labels=["ready-for-human", "enhancement"],
                 created="2026-09-12", body="Found by an agent's audit of the repo: shellcheck would catch quoting bugs."),
        ],
    ),
    # The Release size is reached: what does not fit is left out, with the reason.
    "size-reached": dict(
        size=3,
        milestone=[20, 21, 22, 23],
        issues=[QUIET,
            dict(n=21, slug="shout", title="Shout flag", type="ticket", labels=["ready-for-agent", "enhancement", "milestone-1"],
                 created="2026-10-04", body="`-s` prints the greeting in capitals."),
            dict(n=22, slug="name-file", title="Read names from a file", type="ticket", labels=["ready-for-agent", "enhancement", "milestone-1"],
                 created="2026-10-05", body="`-f <file>` greets each name in the file."),
            dict(n=23, slug="count", title="Repeat flag", type="ticket", labels=["ready-for-agent", "enhancement", "milestone-1"],
                 created="2026-10-06", body="`-n <k>` repeats the greeting k times."),
            TYPO,
        ],
    ),
    # Every severe issue joins, even past the size; a marked issue that is not severe does not, nor do the features.
    "severe-past-size": dict(
        size=2,
        milestone=[10, 20],
        issues=FAREWELL + [QUIET,
            bug(31, "profile", "`--save` overwrites ~/.profile", "2026-10-20",
                "`greet.sh hello Ada --save` writes the greeting over `~/.profile` and the user's settings are lost."),
            bug(36, "ci-red", "test.sh fails on main, so no pull request can pass", "2026-10-05",
                "Since #9 merged, `bash test.sh` fails on main; every pull request's check is red and nothing can merge."),
            bug(37, "token-log", "test.sh prints the registry token in CI logs", "2026-10-25",
                "`test.sh` echoes `$REGISTRY_TOKEN`; the token is in every public CI log. A security hole."),
            bug(35, "slow-test", "test.sh takes 10 s", "2026-10-01",
                "Retro planning for Release 2 marked this to join the next Release: `test.sh` sleeps 10 s for nothing.",
                labels=["ready-for-agent", "bug", "next-release"]),
        ],
    ),
    # The agent re-orders the Milestone's features: the one the others depend on first, then the one that moves the
    # goal ("usable from scripts") furthest, though the Milestone issue lists it second; one reason line each.
    "reorder": dict(
        size=5,
        goal="Make the greeter usable from scripts.",
        milestone=[24, 25, 26],
        issues=[
            dict(n=24, slug="colour", title="Colour output", type="ticket", labels=["ready-for-agent", "enhancement", "milestone-1"],
                 created="2026-10-02", blocked_by=[26], body="Print greetings in a colour the config file names."),
            dict(n=25, slug="json", title="JSON output for scripts", type="ticket", labels=["ready-for-agent", "enhancement", "milestone-1"],
                 created="2026-10-03", blocked_by=[26],
                 body="`--json` prints `{\"greeting\": ...}` so scripts can parse the output; the output format comes from the config file."),
            dict(n=26, slug="config", title="Config file loader", type="ticket", labels=["ready-for-agent", "enhancement", "milestone-1"],
                 created="2026-10-04", body="Read `~/.greetrc` (output format, colour). #24 and #25 need it."),
        ],
    ),
    # A repo that keeps no version cuts a whole Release: shipped test, changelog entry with no Versions line and no
    # version file, the end-of-Release pass in order, then the plan.
    "no-version": dict(
        size=5,
        milestone=[10, 20, 21],
        cut=True,
        issues=[
            dict(n=10, slug="farewell", title="Farewell command", type="ticket", labels=["ready-for-agent", "enhancement", "milestone-1", "release-2"],
                 created="2026-10-02", status="closed", body="Add `greet.sh bye <name>`."),
            dict(QUIET, labels=QUIET["labels"] + ["release-2"], status="closed"),
            dict(n=21, slug="shout", title="Shout flag", type="ticket", labels=["ready-for-agent", "enhancement", "milestone-1"],
                 created="2026-10-04", body="`-s` prints the greeting in capitals."),
        ],
        pulls=[
            dict(n=7, title="feat: farewell command", body="Closes #10", file="src/greet.sh", line="# bye\n"),
            dict(n=8, title="feat: quiet flag", body="Fixes #20", file="src/greet.sh", line="# quiet\n"),
            dict(n=9, title="docs: README usage", body="No issue.", file="README.md", line="Usage: greet.sh hello <name>\n"),
        ],
    ),
}
# A release issue written before the Order list (a `## Scope` list and a Cap line, no `## Order`) whose label its
# issues carry is the current Release: it is cut as in no-version, never replanned.
CASES["old-shape-cut"] = dict(copy.deepcopy(CASES["no-version"]), old_shape=True)

EXPECT = {
    "severe-first": dict(order=[31, 35, 10, 20, 30], labelled={31, 35, 10, 11, 12, 20, 30}, left_out=set(),
                         not_ranked=set(), cleared={35}, used=5),
    "blocker-first": dict(order=[10, 40, 20, 30], labelled={10, 11, 12, 40, 20, 30}, left_out=set(),
                          not_ranked=set(), cleared=set(), used=4),
    "bugs-fill": dict(order=[20, 21, 30, 31, 32], labelled={20, 21, 30, 31, 32}, left_out={33},
                      not_ranked={34}, cleared=set(), used=5),
    "unplanned-feature": dict(order=[10, 20, 30], labelled={10, 11, 12, 20, 30}, left_out=set(),
                              not_ranked={50, 51}, proposed={50}, cleared=set(), used=3),
    "size-reached": dict(order=[20, 21, 22], labelled={20, 21, 22}, left_out={23, 30},
                         not_ranked=set(), cleared=set(), used=3),
    "severe-past-size": dict(order=[36, 31, 37], labelled={36, 31, 37}, left_out={35, 10, 20},
                             not_ranked=set(), cleared=set(), kept_mark={35}, used=2, past=1),
    "reorder": dict(order=[26, 25, 24], labelled={26, 25, 24}, left_out=set(), not_ranked=set(),
                    cleared=set(), used=3, reasons=True),
    "no-version": dict(order=[21], labelled={21}, left_out=set(), not_ranked=set(), cleared=set(), used=1,
                       cut=dict(name="Release 2", shipped=[10, 20], also_merged=[9])),
}
EXPECT["old-shape-cut"] = EXPECT["no-version"]
