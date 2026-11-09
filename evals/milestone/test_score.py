#!/usr/bin/env python3
"""Self-test of score.py's planning cases: a hand-written reference run of each case passes, and each planted wrong
run fails the check it plants. Builds the fixtures with make-fixture.sh in a temporary directory.

Usage: python3 evals/milestone/test_score.py   (exits 1 when any expectation fails)
See evals/milestone/README.md.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCORE = os.path.join(HERE, "score.py")
BUILD = os.path.join(HERE, "make-fixture.sh")

ROWS = """| # | Feature | Kind | Accepted when |
| --- | --- | --- | --- |
| 1 | `10-farewell.md` Add a farewell command | Spec | `greet.sh bye Ada` prints `Goodbye, Ada!`; no name greets the world; tests cover both |
| 2 | `20-quiet.md` Add a --quiet flag | lone Ticket | `--quiet` prints nothing and keeps the exit code |"""
COLOUR_ROW = ("| 3 | `50-colour-terminal.md` Colour the name on a terminal (added 2026-11-02 by the user) | lone Ticket "
              "| green only on a terminal; `--no-color` turns it off; a test covers both |")


def block(n, op, issue, fields="", body=None):
    text = f"### {n}. {op}\nIssue: {issue}\n{fields}"
    if body is not None:
        text += f"Body:\n~~~\n{body}\n~~~\n"
    return text + "\n"


def milestone_body(repo, extra_row=True, excluded=None):
    """The fixture's Milestone issue body (headers and comments cut), with the colour row and an Excluded list."""
    text = open(os.path.join(repo, ".scratch/issues/00-milestone.md")).read()
    body = text.split("\n\n", 1)[1].split("\n## Comments")[0].rstrip()
    if extra_row:
        body = body.replace(ROWS.splitlines()[-1], ROWS.splitlines()[-1] + "\n" + COLOUR_ROW)
    if excluded is not None:
        body = re.sub(r"## Excluded\n\n.*", "## Excluded\n\n" + excluded, body, flags=re.S)
    return body


def plan_small_run(repo):
    body = """## Goal

Scripts can run the greeter silently.

## Features, in build order

One at a time, in this order. Each feature is its own issue carrying `milestone-1`.

| # | Feature | Kind | Accepted when |
| --- | --- | --- | --- |
| 1 | `20-quiet.md` Add a --quiet flag | lone Ticket | `--quiet` prints nothing and keeps the exit code |

## Acceptance

- Every feature above is merged and its issue closed.

## Excluded

- None."""
    actions = (block(1, "Create a label", "new", "Label: milestone-1\n")
               + block(2, "Create an issue", "new (00-milestone.md)",
                       "Title: Milestone 1: quiet in scripts\nLabels: milestone-1\nParent: none\n", body)
               + block(3, "Apply / remove labels", ".scratch/issues/20-quiet.md", "Add: milestone-1\nRemove: none\n")
               + block(4, "Make an issue a sub-issue of a parent", ".scratch/issues/20-quiet.md",
                       "Parent: .scratch/issues/00-milestone.md\n"))
    return actions, ("- What outcome do you want by the Milestone's end?\n- Here is the whole draft (one at a time, "
                     "Acceptance with only its first line, Excluded: None.). Is this right?\n")


def plan_setaside_run(repo, ask=True, excluded="- Translations (`31-translations.md`), set aside for a later Milestone.",
                      label31=False):
    actions, qs = plan_small_run(repo)
    actions = actions.replace("- None.", excluded)
    if label31:
        actions += block(5, "Apply / remove labels", ".scratch/issues/31-translations.md", "Add: milestone-1\nRemove: none\n")
    if ask:
        qs = ("- Some work is set aside for a later Milestone: 31 Translations (next Milestone), French and Spanish "
              "greetings. Does any of it join this one?\n") + qs
    return actions, qs


def add_run(repo, case, ticket12=True, ask_agreement=None, labels_first=False, keep_colour=False):
    excluded = None
    if case == "add-feature-excluded":
        # A note under the list naming colour as taken out is fine; colour left in the list is not.
        excluded = ("- Colour output (`30-colour.md`).\n- Translations." if keep_colour else
                    "- Translations.\n\n_2026-11-02: colour output (`30-colour.md`) taken out of Excluded, by the user._")
    t12_old = open(os.path.join(repo, ".scratch/issues/12-bye-usage.md")).read().split("\n\n", 1)[1].rstrip()
    t12_new = (t12_old.replace("`usage: greet.sh hello|bye <name>`", "`usage: greet.sh [--no-color] hello|bye <name>`")
               + "\n\n"
               "_Updated for `50-colour-terminal.md` (added to Milestone 1 on 2026-11-02): the usage line lists "
               "`--no-color` too._")
    acts = [block(1, "Create an issue", "new (50-colour-terminal.md)",
                  "Title: Colour the name on a terminal\nLabels: enhancement\nParent: none\n",
                  "Colour the name in `hello` green only on a terminal; `--no-color` turns it off.")]
    if labels_first:
        acts.append(block(2, "Apply / remove labels", ".scratch/issues/50-colour-terminal.md", "Add: milestone-1\nRemove: none\n"))
    n = len(acts) + 1
    acts.append(block(n, "Edit an issue body", ".scratch/issues/00-milestone.md", "",
                      milestone_body(repo, excluded=excluded)))
    n += 1
    if not labels_first:
        acts.append(block(n, "Apply / remove labels", ".scratch/issues/50-colour-terminal.md",
                          "Add: milestone-1\nRemove: none\n"))
        n += 1
    if ticket12:
        acts.append(block(n, "Edit an issue body", ".scratch/issues/12-bye-usage.md", "", t12_new))
    qs = "- Shall I plan issue 30 first, and what should it do?\n- Where does it go in the order?\n"
    if ask_agreement is None:
        ask_agreement = case == "add-feature-excluded"
    if ask_agreement:
        qs += "- Milestone 1 excludes colour output: may I take it out of Excluded so the feature can join?\n"
    return "".join(acts), qs


def run(out, case, actions, questions):
    with open(os.path.join(out, "repo/.scratch/proposed-actions.md"), "w") as f:
        f.write(actions)
    with open(os.path.join(out, "repo/.scratch/questions.md"), "w") as f:
        f.write(questions)
    p = subprocess.run([sys.executable, SCORE, out, case], capture_output=True, text=True)
    return p.returncode, p.stdout


failures = []


def expect(name, case, make, passes, fails_on=None):
    tmp = tempfile.mkdtemp()
    out = os.path.join(tmp, case)
    subprocess.run(["bash", BUILD, out, case], check=True, capture_output=True)
    actions, qs = make(os.path.join(out, "repo"))
    code, text = run(out, case, actions, qs)
    ok = (code == 0) if passes else (code == 1 and (fails_on is None or any(
        l.startswith("FAIL " + fails_on) for l in text.splitlines())))
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        failures.append(name)
        print(text)


expect("plan-small reference passes", "plan-small", plan_small_run, True)
expect("plan-small with a Boundaries section fails", "plan-small",
       lambda r: (plan_small_run(r)[0].replace("- None.", "- None.\n\n## Boundaries\n\n- **Budget:** none."),
                  plan_small_run(r)[1]), False, "shape: no Boundaries section")
expect("plan-small asking for a budget fails", "plan-small",
       lambda r: (plan_small_run(r)[0], plan_small_run(r)[1] + "- Is there a budget for this Milestone?\n"),
       False, "no question on what a one-Release Milestone defaults")
expect("plan-setaside reference passes", "plan-setaside", plan_setaside_run, True)
expect("plan-setaside without the set-aside question fails", "plan-setaside",
       lambda r: plan_setaside_run(r, ask=False), False, "asked which set-aside work joins")
expect("plan-setaside with Excluded saying None fails", "plan-setaside",
       lambda r: plan_setaside_run(r, excluded="- None."), False, "Excluded names the translations")
expect("plan-setaside labelling the set-aside issue fails", "plan-setaside",
       lambda r: plan_setaside_run(r, label31=True), False, "no label on 31-translations")
expect("plan-setaside with only the draft question naming 31 fails", "plan-setaside",
       lambda r: (plan_setaside_run(r, ask=False)[0], plan_setaside_run(r, ask=False)[1]
                  + "- Here is the draft; Excluded names 31 Translations. Is this right?\n"),
       False, "asked which set-aside work joins")
for c in ("add-feature", "add-feature-excluded"):
    expect(f"{c} reference passes", c, lambda r, c=c: add_run(r, c), True)
    expect(f"{c} leaving touched Ticket 12 as it was fails", c, lambda r, c=c: add_run(r, c, ticket12=False),
           False, "touched Ticket 12")
    expect(f"{c} labelling before listing fails", c, lambda r, c=c: add_run(r, c, labels_first=True),
           False, "nothing carries the Milestone label")
expect("add-feature-excluded keeping colour in Excluded fails", "add-feature-excluded",
       lambda r: add_run(r, "add-feature-excluded", keep_colour=True), False, "Excluded drops colour")
expect("add-feature asking an agreement question fails", "add-feature",
       lambda r: add_run(r, "add-feature", ask_agreement=True), False, "no question on the Milestone's goal")
expect("add-feature-excluded asking no agreement question fails", "add-feature-excluded",
       lambda r: add_run(r, "add-feature-excluded", ask_agreement=False), False, "exactly one question")

print(f"{len(failures)} failed")
sys.exit(1 if failures else 0)
