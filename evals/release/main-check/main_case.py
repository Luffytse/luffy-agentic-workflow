"""The main-check case of the release eval: its fixture data and the outcome it expects.

make_fixture.py builds the repo from this data; score.py and test_cases.py read EXPECT. Keep this file, the scorer
and the README away from the session under test: EXPECT is the answer.

Issue numbers are the issue file prefixes (#30 is .scratch/issues/30-*.md). Release 2 (#2) is cut and closed with
both end-of-Release records, so the run goes straight to planning Release 3. After Release 2's end, four pull
requests merged into main that close no issue: #7 fixes the usage typo (#30), #8 adds the shout flag (#21, a
planned feature), #9 fixes names with spaces for `hello` only (#31's `bye` half is still true), #10 drops
`--version` (#32's subject).
"""

GOAL = "Round out the greeter's options."

def greet(fixed_usage=False, shout=False, whole_hello=False, version=True):
    """main's src/greet.sh after the pull requests named by the flags (all False/True defaults: before any)."""
    usage = ("[-s] " if shout else "") + ("hello" if fixed_usage else "helo") + "|bye <name>"
    hello = ('  hello) echo "Hello, ${2:-world}!" ;;' if whole_hello
             else "  hello) name=$(echo ${2:-world} | cut -d' ' -f1); echo \"Hello, ${name}!\" ;;")
    cases = [hello, "  bye) name=$(echo ${2:-world} | cut -d' ' -f1); echo \"Goodbye, ${name}!\" ;;"]
    if version:
        cases.append("  --version) echo 0.0.0 ;;")
    cases.append(f'  *) echo "usage: greet.sh {usage}" >&2; exit 2 ;;')
    body = "case \"${1:-}\" in\n" + "\n".join(cases) + "\nesac\n"
    if not shout:
        return "#!/usr/bin/env bash\n# usage: greet.sh " + usage + "\n" + body
    return ("#!/usr/bin/env bash\n# usage: greet.sh " + usage + "\nshout=0\n"
            'if [ "${1:-}" = "-s" ]; then shout=1; shift; fi\n'
            "out=$(\n" + body + ") || exit 2\n"
            'if [ "$shout" = 1 ]; then echo "$out" | tr \'[:lower:]\' \'[:upper:]\'; else echo "$out"; fi\n')


# The four merged pull requests, oldest first, each with the flags main's src/greet.sh has once it merges.
PULLS = [
    dict(n=7, title="fix: usage line says hello", date="2026-10-20",
         body="The usage line said `helo`. Reported in #30; this pull request does not close it.",
         state=dict(fixed_usage=True)),
    dict(n=8, title="feat: -s shouts the greeting", date="2026-10-21",
         body="`-s` before the command prints the greeting in capitals.",
         state=dict(fixed_usage=True, shout=True)),
    dict(n=9, title="fix: hello keeps the whole name", date="2026-10-22",
         body="`hello` no longer cuts the name at the first space. `bye` is unchanged.",
         state=dict(fixed_usage=True, shout=True, whole_hello=True)),
    dict(n=10, title="chore: drop --version", date="2026-10-23",
         body="The repo keeps no version (its release doc's policy is none), so the `--version` option goes.",
         state=dict(fixed_usage=True, shout=True, whole_hello=True, version=False)),
]

TEST_SH = '#!/usr/bin/env bash\nset -e\n[ "$(bash src/greet.sh hello Ada)" = "Hello, Ada!" ]\necho OK\n'


def bug(n, slug, title, created, body):
    return dict(n=n, slug=slug, title=title, type="ticket", labels=["ready-for-agent", "bug"], created=created, body=body)


ISSUES = [
    dict(n=20, slug="quiet", title="Quiet flag", type="ticket", labels=["ready-for-agent", "enhancement", "milestone-1"],
         created="2026-10-03", body="`-q` before the command prints the greeting with no trailing newline: "
                                    "`greet.sh -q hello Ada` prints `Hello, Ada!` and nothing after it."),
    dict(n=21, slug="shout", title="Shout flag", type="ticket", labels=["ready-for-agent", "enhancement", "milestone-1"],
         created="2026-10-03", body="`-s` before the command prints the greeting in capitals: "
                                    "`greet.sh -s hello Ada` prints `HELLO, ADA!`."),
    bug(30, "usage-typo", "Typo in usage text", "2026-09-01",
        "Run `greet.sh` with no command: the usage line says `greet.sh helo|bye <name>`. It should say `hello`."),
    bug(31, "name-spaces", "Names with spaces are cut at the first space", "2026-09-05",
        "Both commands drop everything after the first space of the name:\n\n"
        "- `greet.sh hello \"Ada Lovelace\"` prints `Hello, Ada!`\n"
        "- `greet.sh bye \"Ada Lovelace\"` prints `Goodbye, Ada!`\n\n"
        "Each should print the whole name."),
    bug(32, "version-zero", "--version always prints 0.0.0", "2026-09-10",
        "`greet.sh --version` prints `0.0.0` whatever the release. It should print the real version."),
    bug(33, "test-bye", "test.sh does not test bye", "2026-09-15",
        "`test.sh` checks `hello` only, so a broken `bye` passes the check. Add a `bye` check."),
    bug(34, "sometimes-fails", "greet sometimes fails", "2026-09-20",
        "It failed on the build box last week. Not sure why. Someone said it might be the locale?"),
    dict(n=45, slug="colour", title="Colour output", type="ticket", labels=["ready-for-agent", "enhancement"],
         created="2026-10-05", body="`-c` prints the greeting in green, and `greet.sh --version` lists `colour` "
                                    "among the features it was built with."),
]

MILESTONE_FEATURES = [20, 21]
LATER = 45  # the Milestone issue leaves it to the next Milestone

# Verdict classes the scorer accepts for each issue in the check's scope. Already fixed and obsolete take the same
# action (close, or for a planned feature, the user), so either is accepted for the three closed-or-asked issues.
GONE = {"already fixed", "obsolete"}
EXPECT = dict(
    verdicts={20: {"still valid"}, 21: GONE, 30: GONE, 31: {"changed scope"}, 32: GONE, 33: {"still valid"},
              34: {"cannot tell"}},
    # where the evidence lives on main: the pull request number, or the file
    evidence={21: ["#8", "greet.sh"], 30: ["#7", "greet.sh"], 31: ["#9", "greet.sh"], 32: ["#10", "greet.sh"]},
    closed={30, 32},
    edited={31},
    asked={21},  # a planned feature that main already does: goes to the user, not closed, not ranked
    unchecked={34},
    untouched={45},
    order=[20, 31, 33],
    labelled={20, 31, 33},
    used=3,
)
