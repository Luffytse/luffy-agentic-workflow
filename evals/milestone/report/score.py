#!/usr/bin/env python3
"""Score actual proposed coordinator actions against independent fixture facts."""
import argparse,json,re
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument("out",type=Path); p.add_argument("case",choices=["ready","incomplete","final-cut","reentry"]); a=p.parse_args()
actions=json.loads((a.out/"actions.json").read_text()); checks=[]
def check(name,condition):
 checks.append(condition); print(("PASS " if condition else "FAIL ")+name)
reports=[x for x in actions if x["operation"]=="comment" and "<!-- milestone report -->" in x.get("body","")]
if a.case=="reentry":
 check("unchanged review state takes no duplicate action",actions==json.loads((a.out/"before-actions.json").read_text()))
elif a.case=="final-cut":
 check("final Release cut starts before report",any(x["operation"]=="start-thread" and re.search(r"release",x.get("body",""),re.I) and x["target"]=="R1" for x in actions))
 check("await final cut without report or ending checkins",not reports and not any(x["operation"]=="end-checkins" for x in actions))
elif a.case=="incomplete":
 check("open unparked feature prevents report",not reports)
 check("no schedule ending before report eligibility",not any(x["operation"]=="end-checkins" for x in actions))
else:
 check("one report comment on Milestone",len(reports)==1 and reports[0]["target"]=="M1")
 body=reports[0]["body"] if reports else ""
 for name,terms in {
 "acceptance evidence":["F10","test-bye","test-usage","F20","quiet"],
 "park and maintenance reasons":["registry","B30","severe"],
 "every readable user message":["chat://coordinator/u1","tracker://F20/u2","chat://build-20/u3"],
 
 "permission sandbox and Startup":["acceptEdits","sandbox","startup","ready"],
 "per-thread versions and gaps":["coordinator","build-10","build-20","0.41.0","0.40.0","unreadable"],
 "decision evidence":["D2","REVIEW.md","tracker://P7/merge"],
 "skill loading estimate and measurement":["250","80","estimate"],
 "next Milestone suggestions":["next","registry"],
 "history visibility gap":["11:00"],
 }.items(): check(name,all(t.lower() in body.lower() for t in terms))
 def thread_elapsed(subject, duration):
  rows=[line for line in body.splitlines() if re.match(r"^\s*\|?\s*"+re.escape(subject)+r"(?:\s*/|\s*\|)",line,re.I)]
  return any(re.search(duration,line,re.I) for line in rows)
 # Fixture session timestamps are independent evidence, not derived from reported durations.
 for subject, start, end in (("coordinator","10:00","12:00"),("build-10","10:10","11:00")):
  check(subject+" start/end match session evidence",thread_elapsed(subject,re.escape(start)+r"\s*[–—-]\s*"+re.escape(end)+r"\b"))
 two_hours=r"\b(?:2 hours|120[- ]min(?:utes)?|02:00|2h)\b"
 check("coordinator elapsed is two hours",thread_elapsed("coordinator",two_hours))
 check("build-10 elapsed is 50 minutes",thread_elapsed("build-10",r"\b(?:50[- ]min(?:utes)?|0h ?50|00:50)\b"))
 check("Milestone wall time is two hours",any(re.search(r"wall time",line,re.I) and re.search(two_hours,line,re.I) for line in body.splitlines()))
 def row(source):
  lines=body.splitlines()
  return next((line for line in lines if source.lower() in line.lower()), "")
 check("planning message classified planned",bool(re.search(r"(?<!un)planned|feature planning",row("chat://coordinator/u1"),re.I)))
 check("progress correction classified unplanned",bool(re.search("unplanned|step.in",row("tracker://F20/u2"),re.I)))
 check("parked blocker answer classified planned",bool(re.search(r"(?<!un)planned|parked blocker",row("chat://build-20/u3"),re.I)))
 def category(number,word):
  normalized=body.replace(",", "")
  total_lines=[line for line in normalized.splitlines() if re.search("total|known|partial",line,re.I)]
  label={"input":r"(?<!cached )(?<!cached-)\binput", "output":r"\boutput", "cach":r"cached?(?:[-_ ]input)?"}[word]
  return any(re.search(label+r"(?: tokens)?\s*[:=]?\s*"+str(number)+r"\b",line,re.I) for line in total_lines)
 check("known token subtotal preserves categories",category(1700,"input") and category(400,"output") and category(500,"cach") and bool(re.search("partial|incomplete",body,re.I)))
 check("skill loading estimate tied to coordinator",bool(re.search(r"250.*estimat|estimat.*250",row("coordinator"),re.I)) or bool(re.search(r"coordinator[^\n]*250[^\n]*estimat",body,re.I)))
 check("skill loading measured tied to build-10",bool(re.search(r"80.*measur|measur.*80",row("build-10"),re.I)) or bool(re.search(r"build-10[^\n]*80[^\n]*measur",body,re.I)))
 check("report stops for user review",bool(re.search(r"ready for.*review|await.*review|ready for acceptance",body,re.I)))
 stops=[i for i,x in enumerate(actions) if x["operation"]=="end-checkins"]
 report_indices=[i for i,x in enumerate(actions) if x in reports]
 check("schedule stopped before report",bool(stops and report_indices and stops[0]<report_indices[0]))
 check("schedule readback recorded",any(re.search("no future firing|disabled",x.get("body",""),re.I) for x in actions if x["operation"]=="end-checkins"))
 check("no build or close/accept action",not any(x["operation"] in ["start-thread","close","accept"] for x in actions))
 check("Milestone remains open",not any(x["operation"]=="close" and x["target"]=="M1" for x in actions))
raise SystemExit(0 if all(checks) else 1)
