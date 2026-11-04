#!/usr/bin/env python3
"""A logging stand-in for `gh`, put first on PATH by the Repo labels cases. It serves the made-up tracker's labels and
issues from gh-state.json, applies a label creation or deletion to that file, logs every call as a JSON line to gh.log and
answers anything else with `{}`. Nothing here reaches the network. It lives next to gh-state.json and gh.log."""
import json, os, re, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here) if os.path.basename(here) == "bin" else here
state_path, log_path = os.path.join(root, "gh-state.json"), os.path.join(root, "gh.log")
args = sys.argv[1:]
with open(log_path, "a") as f:
    f.write(json.dumps(args) + "\n")
state = json.load(open(state_path))


def save():
    json.dump(state, open(state_path, "w"), indent=1)


def emit(data):
    jq = None
    for i, a in enumerate(args):
        if a in ("--jq", "-q") and i + 1 < len(args):
            jq = args[i + 1]
    text = json.dumps(data)
    if jq:
        try:
            text = subprocess.run(["jq", "-r", jq], input=text, capture_output=True, text=True).stdout.rstrip("\n")
        except FileNotFoundError:
            pass
    print(text)


def field(name):
    out = []
    for i, a in enumerate(args):
        if a in ("-f", "-F", "--field", "--raw-field") and i + 1 < len(args):
            m = re.match(r"%s=(.*)$" % name, args[i + 1])
            if m:
                out.append(m.group(1))
    return out


joined = " ".join(args)
method = "GET"
for i, a in enumerate(args):
    if a in ("--method", "-X") and i + 1 < len(args):
        method = args[i + 1].upper()
labels_endpoint = re.search(r"repos/[^/\s]+/[^/\s]+/labels(\?|\s|$)", joined + " ")
label_item = re.search(r"repos/[^/\s]+/[^/\s]+/labels/([^\s?]+)", joined)

if args[:2] == ["label", "create"] and len(args) > 2:
    state["labels"].append({"name": args[2], "description": ""}); save()
elif args[:2] == ["label", "delete"] and len(args) > 2:
    state["labels"] = [l for l in state["labels"] if l["name"] != args[2]]; save()
elif label_item and method == "DELETE":
    state["labels"] = [l for l in state["labels"] if l["name"] != label_item.group(1)]; save()
elif label_item and method == "GET":
    hit = [l for l in state["labels"] if l["name"] == label_item.group(1)]
    if not hit:
        print('{"message": "Not Found", "status": "404"}'); sys.exit(1)
    emit(hit[0])
elif labels_endpoint and method == "POST":
    for name in field("name"):
        state["labels"].append({"name": name, "description": (field("description") or [""])[0]})
    save(); print("{}")
elif labels_endpoint:
    emit(state["labels"])
elif args[:2] == ["issue", "list"] or re.search(r"repos/[^/\s]+/[^/\s]+/issues(\?|\s|$)", joined + " "):
    want = []
    for i, a in enumerate(args):
        if a in ("--label", "-l") and i + 1 < len(args):
            want.append(args[i + 1])
    m = re.search(r"labels=([^&\s]+)", joined)
    if m:
        want += m.group(1).split(",")
    emit([dict(i, labels=[{"name": n} for n in i["labels"]], comments=[], state="open")
          for i in state["issues"] if all(w in i["labels"] for w in want)])
else:
    print("{}")
