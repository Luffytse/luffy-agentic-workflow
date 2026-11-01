#!/usr/bin/env python3
"""Score an observed record interpretation; ordering of sets is immaterial."""
import json
import sys
from pathlib import Path

def normalize(value):
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items()}
    if isinstance(value, list):
        return sorted(value)
    return value

expected = json.loads(Path(__file__).with_name("expected.json").read_text())
for name in sys.argv[1:]:
    observed = json.loads(Path(name).read_text())
    assert normalize(observed) == normalize(expected), f"record interpretation differs: {name}"
    print(f"PASS: {name}")
if len(sys.argv) == 1:
    raise SystemExit("usage: score.py <observed.json> [...]")
