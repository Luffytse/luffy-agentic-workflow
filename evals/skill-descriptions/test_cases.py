#!/usr/bin/env python3
"""Self-test of the skill-descriptions eval: no model session. Checks the listing builder on a planted skills
folder and on the real one, that the cases cover every skill, and that the scorer and comparator give the
expected verdicts on planted answers.

Run: python3 evals/skill-descriptions/test_cases.py
"""
import collections
import json
import pathlib
import re
import subprocess
import sys
import tempfile

here = pathlib.Path(__file__).resolve().parent
repo = here.parent.parent
sys.path.insert(0, str(here))
import build_listing  # noqa: E402
import cases as case_data  # noqa: E402
import compare  # noqa: E402
import make_batches  # noqa: E402
import score  # noqa: E402

SKILLS = repo / "plugins" / "dev-skills" / "skills"
CASES = case_data.load()
failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)


# --- listing builder on a planted folder
with tempfile.TemporaryDirectory() as tmp:
    root = pathlib.Path(tmp)
    for name, fm in {
        "alpha": 'name: alpha\ndescription: "Do \\"alpha\\" things. Use when asked."\nargument-hint: "x: y"',
        "beta": "name: beta\ndescription: Plain one. Use when plain.\nuser-invocable: false\nmetadata:\n  credits:\n    skill: z",
    }.items():
        (root / name).mkdir()
        (root / name / "SKILL.md").write_text(f"---\n{fm}\n---\n\nbody: ignored\n", encoding="utf-8")
    skills = build_listing.load_skills(root)
    check([s[0] for s in skills] == ["alpha", "beta"], "planted: names")
    check(skills[0][1] == 'Do "alpha" things. Use when asked.', f"planted: quoted description {skills[0][1]!r}")
    check(skills[1][1] == "Plain one. Use when plain." and skills[1][2] is True, "planted: plain description, hidden flag")
    check(build_listing.listing(skills) == '- dev-skills:alpha: Do "alpha" things. Use when asked.\n- dev-skills:beta: Plain one. Use when plain.\n',
          "planted: listing text")
    rows, total = build_listing.word_counts(skills)
    check(rows == [("alpha", 6), ("beta", 5)] and total == 11, f"planted: word counts {rows} {total}")

# --- the real skills folder
real = build_listing.load_skills(SKILLS)
real_names = {s[0] for s in real}
check(len(real) == 35, f"real: expected 35 skills, found {len(real)}")
text = build_listing.listing(real)
check(len(text.splitlines()) == len(real), "real: one line per skill")
check(all(re.match(r"^- dev-skills:[a-z-]+: \S", ln) for ln in text.splitlines()), "real: line shape")
check({s[0] for s in real if s[2]} >= {"merging", "review-record", "docs-index", "issue-absorption", "model-tiers", "worker-control"},
      "real: hidden skills are in the listing")
check(build_listing.word_counts(real)[1] == sum(len(s[1].split()) for s in real), "real: total words")

# --- cases
ids = [c["id"] for c in CASES]
check(len(ids) == len(set(ids)), "cases: duplicate ids")
for c in CASES:
    check(c["kind"] in ("trigger", "near-miss", "none"), f"{c['id']}: bad kind")
    check(c["expected"] in real_names or c["expected"] == "none", f"{c['id']}: expected {c['expected']!r} is not a skill")
    check(c["kind"] != "none" or c["expected"] == "none", f"{c['id']}: kind none needs expected none")
    check(c["expected"] != "none" or c["kind"] == "none", f"{c['id']}: expected none needs kind none")
    check(c["prompt"].strip() and "\n\n" not in c["prompt"], f"{c['id']}: prompt empty or multi-paragraph")
trig = collections.Counter(c["expected"] for c in CASES if c["kind"] == "trigger")
for name in sorted(real_names):
    check(trig[name] >= 3, f"cases: {name} has {trig[name]} trigger prompts, needs 3")
check(sum(1 for c in CASES if c["kind"] == "none") >= 3, "cases: need a few none prompts")
near = {c["expected"] for c in CASES if c["kind"] == "near-miss"}
for pair in ("grilling", "grill-with-docs", "retro", "retro-planning", "implement", "implement-spec", "to-spec", "wayfinder",
             "agentic-review", "review-rounds"):
    check(pair in near, f"cases: no near-miss expecting {pair}")
check(case_data.ALLOW_NAME_IN_PROMPT <= set(ids), "cases: ALLOW_NAME_IN_PROMPT names an unknown case")
for c in CASES:  # a prompt must not reveal the expected skill's name
    if c["expected"] == "none" or c["id"] in case_data.ALLOW_NAME_IN_PROMPT:
        continue
    pat = r"\b" + re.escape(c["expected"]).replace(r"\-", "[- ]") + r"\b"
    check(not re.search(pat, c["prompt"], re.I), f"{c['id']}: prompt names the skill {c['expected']!r}")

# --- batches hold the prompts, with opaque labels, and never an expected answer or a case id
with tempfile.TemporaryDirectory() as tmp:
    rc = make_batches.main([str(SKILLS), tmp])
    out = pathlib.Path(tmp)
    index = json.loads((out / "batches.json").read_text())
    mapped = [cid for m in index.values() for cid in m.values()]
    check(rc == 0 and sorted(mapped) == sorted(ids), "batches: every case in exactly one batch")
    labels = [lab for m in index.values() for lab in m]
    check(len(labels) == len(set(labels)) and all(re.fullmatch(r"S\d+", lab) for lab in labels), "batches: labels are unique S<n>")
    check(all(len(m) <= 7 for m in index.values()), "batches: size")
    prompts = {c["id"]: c["prompt"] for c in CASES}
    for name, mapping in index.items():
        text = (out / f"{name}.md").read_text()
        check(text.count("- dev-skills:") == 35, f"{name}: listing")
        head, _, rest = text.partition("## Situations")
        situations, _, tail = rest.partition("## Answer")
        headers = re.findall(r"(?m)^### (.*)$", situations)
        check(headers == list(mapping), f"{name}: situation headers are the opaque labels, in order {headers}")
        check(all(prompts[cid] in situations for cid in mapping.values()), f"{name}: prompts present")
        for cid in ids:  # no case id (it holds the skill name and kind) anywhere after the listing
            check(cid not in situations and cid not in tail, f"{name}: case id {cid} leaked")
        for skill in sorted(real_names):  # headers never carry a skill name; prompts only the ALLOW list's ordinary words
            check(not any(skill in h for h in headers), f"{name}: header names {skill}")
        check("expected" not in situations.lower(), f"{name}: expected answers leaked")
        check(not re.search(r"\bt\d\b|nm-", situations + tail), f"{name}: id fragments leaked")
    check(make_batches.make_batches(CASES, 7, 621) == make_batches.make_batches(CASES, 7, 621), "batches: not deterministic")
    check((out / "answers").is_dir(), "batches: answers folder")

# --- scorer and comparator on planted answers
perfect = {c["id"]: "dev-skills:" + c["expected"] if c["expected"] != "none" else "none" for c in CASES}
s = score.score(CASES, {k: score.norm(v) for k, v in perfect.items()})
check(s["correct"] == s["total"] == len(CASES) and not s["misses"], "score: perfect run")

by_id = {c["id"]: c for c in CASES}


def wrong(base, changes):
    a = dict(base)
    a.update(changes)
    return {k: score.norm(v) for k, v in a.items()}


base_ans = wrong(perfect, {"nm-retro-1": "retro-planning", "grilling-t2": "none"})
base = score.score(CASES, base_ans)
check(base["correct"] == len(CASES) - 2, "score: baseline count")
check(base["confusion"][("retro", "retro-planning")] == 1 and base["confusion"][("grilling", "none")] == 1, "score: confusion pairs")
check(base["per_skill"]["grilling"] == [4, 3] and base["per_skill"]["retro"] == [4, 3], f"score: per skill {base['per_skill']['grilling']}")
check(("retro", "retro-planning") in base["near_miss_confusion"] and ("grilling", "none") not in base["near_miss_confusion"],
      "score: near-miss pairs are the near-miss cases only")
check("retro -> retro-planning: 1" in score.report(base), "score: report")
gone = score.score(CASES, {})
check(gone["correct"] == 0 and gone["confusion"][("retro", "(no answer)")] == 4, "score: missing answers are misses")

# same as baseline passes; better passes
for label, changes in {"same": {}, "better": {"nm-retro-1": "retro"}}.items():
    new = score.score(CASES, wrong(base_ans, changes))
    check(compare.compare(base, new)[0], f"compare: {label} should pass")
# worse overall and per skill
new = score.score(CASES, wrong(base_ans, {"pr-t1": "none"}))
ok, fails, _ = compare.compare(base, new)
check(not ok and any(f.startswith("overall") for f in fails) and any(f.startswith("pr:") for f in fails), f"compare: worse should fail {fails}")
# equal overall but one skill worse (another better): fails per skill
new = score.score(CASES, wrong(base_ans, {"nm-retro-1": "retro", "pr-t1": "none"}))
ok, fails, _ = compare.compare(base, new)
check(not ok and len(fails) == 1 and fails[0].startswith("pr:"), f"compare: per-skill fail {fails}")
# new near-miss confusion pair with the same totals elsewhere
new = score.score(CASES, wrong(base_ans, {"nm-retro-1": "retro", "nm-grill-with-docs-1": "grilling", "grill-with-docs-t1": "grill-with-docs"}))
ok, fails, _ = compare.compare(base, new)
check(not ok and any("new near-miss confusion: grill-with-docs -> grilling" in f for f in fails), f"compare: new pair {fails}")
# a new pair from a trigger case is a warning only
new = score.score(CASES, wrong(base_ans, {"nm-retro-1": "retro", "grilling-t1": "grill-with-docs", "grilling-t2": "grilling"}))
ok, fails, warns = compare.compare(base, new)
check(ok and any("grilling -> grill-with-docs" in w for w in warns), f"compare: trigger-case pair is a warning {fails} {warns}")

# --- the CLIs run on a run folder, answers keyed by the opaque labels
def write_run(tmp, answers_by_id):
    run = pathlib.Path(tmp)
    make_batches.main([str(SKILLS), str(run)])
    idx = json.loads((run / "batches.json").read_text())
    for name, mapping in idx.items():
        (run / "answers" / f"{name}.json").write_text(json.dumps({lab: answers_by_id[cid] for lab, cid in mapping.items()}))
    return run


with tempfile.TemporaryDirectory() as t1, tempfile.TemporaryDirectory() as t2:
    a = write_run(t1, perfect)
    b = write_run(t2, wrong(perfect, {"pr-t1": "none"}))
    check(score.score(CASES, score.load_answers(a))["correct"] == len(CASES), "cli: labels translate back to case ids")
    r = subprocess.run([sys.executable, str(here / "compare.py"), str(a), str(b)], capture_output=True, text=True)
    check(r.returncode == 1 and "FAIL" in r.stdout, "cli: compare should exit 1 on a worse run")
    r = subprocess.run([sys.executable, str(here / "compare.py"), str(a), str(a)], capture_output=True, text=True)
    check(r.returncode == 0 and r.stdout.strip().endswith("PASS"), "cli: compare should exit 0 on the same run")
    r = subprocess.run([sys.executable, str(here / "score.py"), str(b)], capture_output=True, text=True)
    check(r.returncode == 0 and "pr-t1 [trigger]: pr -> none" in r.stdout, "cli: score output")
    # a JSON null answer is a miss, never "none"
    idx = json.loads((b / "batches.json").read_text())
    nm_label = next(lab for m in idx.values() for lab, cid in m.items() if cid == "none-1")
    fname = next(n for n, m in idx.items() if nm_label in m)
    data = json.loads((b / "answers" / f"{fname}.json").read_text())
    data[nm_label] = None
    (b / "answers" / f"{fname}.json").write_text(json.dumps(data))
    got = score.load_answers(b)["none-1"]
    check(got == score.INVALID, f"score: null answer read as {got!r}")
    res = score.score(CASES, score.load_answers(b))
    check(("none", score.INVALID) in res["confusion"], "score: null answer on a none case must be a miss")
    # an unknown label is an error
    (b / "answers" / "extra.json").write_text('{"S999": "none"}')
    try:
        score.load_answers(b)
        check(False, "score: unknown label should raise")
    except ValueError:
        pass
check(score.norm(None) == score.INVALID and score.norm(3) == score.INVALID and score.norm(["pr"]) == score.INVALID, "score: non-strings are invalid")

if failures:
    print("\n".join(f"FAIL {f}" for f in failures))
    sys.exit(1)
print(f"ok: {len(CASES)} cases over {len(real)} skills")
