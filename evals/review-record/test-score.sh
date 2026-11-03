#!/usr/bin/env bash
# Checks the review-record fixture and its scorer without running an agent: comments.json holds only the comment shapes
# review-record keeps, expected.json covers every Finding id in it, score.py passes the expected answer and fails
# planted wrong ones.
# Usage: bash evals/review-record/test-score.sh
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
fails=0
ok() { echo "ok: $1"; }
no() { echo "FAIL: $1"; fails=$((fails + 1)); }

python3 -I - "$here/comments.json" "$here/expected.json" >"$tmp/fixture.txt" <<'PY' || true
import json, re, sys
comments = json.load(open(sys.argv[1]))
expected = json.load(open(sys.argv[2]))
records = [c for c in comments if c.startswith("<!-- code-review kind=")]
def say(name, cond): print(("ok: " if cond else "FAIL: ") + name)
say("the fixture has Round and Ticket-check records", any("kind=round" in c for c in records) and any("kind=ticket-check" in c for c in records))
say("the fixture has a comment that is not a record", len(records) < len(comments))
say("every record marker gives a level", all("level=" in c.splitlines()[0] for c in records))
say("every record table has the Claim column", all("| Claim |" in c for c in records if "|" in c))
removed = ["kind=attempt", "kind=pre-existing", "merged into", "rebuttal", "partly", "returned:", "flipped:", "Milestone:"]
say("no record uses a removed shape (" + ", ".join(removed) + ")", not any(r in c for c in comments for r in removed))
ids = set(re.findall(r"^\| ((?:R|T)\d[\w.]*-\d+) \|", "\n".join(records), re.M))
say("expected.json's current view covers every Finding id", ids == set(expected["current"]))
say("retrospective and ignored ids split the ids", set(expected["retrospective"]) | set(expected["ignored_ids"]) == ids
    and not set(expected["retrospective"]) & set(expected["ignored_ids"]))
PY
while IFS= read -r l; do case "$l" in ok:*) ok "${l#ok: }" ;; *) no "${l#FAIL: }" ;; esac; done <"$tmp/fixture.txt"

score() { python3 -I "$here/score.py" "$1" >/dev/null 2>&1; }
cp "$here/expected.json" "$tmp/right.json"
if score "$tmp/right.json"; then ok "the scorer passes the expected answer"; else no "the scorer passes the expected answer"; fi
mutate() { # mutate <name> <python expression on d>
  python3 -I -c "import json,sys; d=json.load(open(sys.argv[1])); $2; json.dump(d, open(sys.argv[2],'w'))" "$here/expected.json" "$tmp/$1.json"
  if score "$tmp/$1.json"; then no "the scorer fails a wrong answer: $1"; else ok "the scorer fails a wrong answer: $1"; fi
}
mutate keeps-false-alarm 'i=d["ignored_ids"][0]; d["retrospective"][i]=d["current"][i]; d["ignored_ids"].remove(i)'
mutate stale-status 'k=next(k for k,v in d["current"].items() if v["status"]=="fixed"); d["current"][k]["status"]="open"'
mutate latest-locations-only 'k=next(k for k in d["retrospective"] if len(d["retrospective"][k]["locations"])>len(d["current"][k]["locations"])); d["retrospective"][k]["locations"]=d["current"][k]["locations"]'

if [ "$fails" -gt 0 ]; then echo "$fails check(s) failed"; exit 1; fi
echo "all review-record fixture checks passed"
