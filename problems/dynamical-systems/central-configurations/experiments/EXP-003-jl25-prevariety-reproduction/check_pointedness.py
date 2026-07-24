#!/usr/bin/env python3
"""EXP-003 pointedness check on a gfan --usevaluation prevariety output.

With --usevaluation gfan adds a 0th coordinate: rays with first coordinate nonzero
are points of the polyhedral complex; rays with first coordinate zero are unbounded
directions. JL25's pointedness claim (powers-of-3 valuations, n = 5): among the
unbounded directions ALL coordinates are non-positive (min convention), so the
global recession cone is pointed. This script parses the RAYS section and reports.
Exit 0 if pointed (no unbounded direction has a positive coordinate), 1 otherwise.
"""
import sys
from fractions import Fraction

path = sys.argv[1]
rays = []
with open(path, encoding="utf-8", errors="replace") as fh:
    in_rays = False
    for line in fh:
        s = line.strip()
        if s == "RAYS":
            in_rays = True
            continue
        if in_rays:
            if not s:
                break
            row = s.split("#")[0].split()
            if not row:
                break
            rays.append([Fraction(x) for x in row])

unbounded = [r for r in rays if r and r[0] == 0]
bad = [r for r in unbounded if any(c > 0 for c in r[1:])]
print(f"rays: {len(rays)}, unbounded directions: {len(unbounded)}, "
      f"with a positive coordinate: {len(bad)}")
if bad[:3]:
    for r in bad[:3]:
        print("  bad:", [str(c) for c in r])
sys.exit(1 if bad else 0)
