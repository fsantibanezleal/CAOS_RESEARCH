"""EXP-002: polynomial census to depth 5 + 2-adic valuation instrumentation.

Deterministic, headless, exact. See hypothesis.md (committed before run).
Usage: python run.py [--smoke]
"""

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))

from tclib.enum import (  # noqa: E402
    census_polynomials,
    find_witness_program,
    integer_roots,
    peval,
    two_adic_valuations,
)

T0 = time.time()
ART = HERE / "artifacts"


def log(msg):
    print(f"[{time.time() - T0:8.1f}s] {msg}", flush=True)


def checkpoint(payload):
    ART.mkdir(exist_ok=True)
    tmp = ART / "census5.json.tmp"
    tmp.write_text(json.dumps(payload, indent=1, sort_keys=True),
                   encoding="utf-8")
    tmp.replace(ART / "census5.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    max_depth = 3 if args.smoke else 5
    deadline = T0 + (120 if args.smoke else 2400)  # 40 min kill

    log(f"EXP-002: census to depth {max_depth} (smoke={args.smoke})")

    def prog(depth, row):
        log(f"  depth {depth}: states={row['states']} "
            f"new_polys={row['new_polynomials']}")
        checkpoint({"partial_depth": depth})

    per_depth, first_seen, complete = census_polynomials(
        max_depth, deadline=deadline, progress=prog)

    # Smoke gate: depths 1-3 must reproduce EXP-001.
    exp001 = {1: 9, 2: 98, 3: 1462}
    for d, s in exp001.items():
        if d <= max_depth and complete.get(d) and per_depth[d]["states"] != s:
            log(f"SMOKE GATE FAIL at depth {d}: {per_depth[d]['states']} != {s}")
            checkpoint({"gate": "FAIL", "per_depth": per_depth})
            return 1

    zmax_cum, best = {}, 0
    records = {}
    for d in sorted(set(first_seen.values())):
        if not complete.get(d):
            continue
        polys_d = [p for p, fd in first_seen.items() if fd == d]
        zd = max(len(integer_roots(p)) for p in polys_d)
        best = max(best, zd)
        zmax_cum[d] = best
        recs = sorted(p for p in polys_d
                      if len(integer_roots(p)) == best)[:40]
        records[d] = []
        for p in recs:
            roots = sorted(integer_roots(p))
            records[d].append({
                "poly": list(p),
                "roots": roots,
                "twoadic_valuations_nonzero_roots":
                    sorted(two_adic_valuations(set(roots))),
                "has_root_zero": 0 in roots,
            })
        log(f"  depth {d}: zmax_cum={best} records={len(records[d])}")

    witnesses = {}
    if not args.smoke and complete.get(5):
        for rec in records.get(5, [])[:3]:
            target = tuple(rec["poly"])
            prog_ops = find_witness_program(target, 5)
            witnesses[str(rec["poly"])] = prog_ops
            if prog_ops:
                assert tuple(prog_ops[-1][3]) == target
                for r in rec["roots"]:
                    assert peval(target, r) == 0

    payload = {
        "per_depth": per_depth,
        "complete": complete,
        "zmax_cumulative": zmax_cum,
        "records": records,
        "witness_programs_depth5": witnesses,
        "model": "inputs {-1,1,x}; gates +,-,*; length = op count",
        "smoke": args.smoke,
    }
    checkpoint(payload)
    log("done; artifacts/census5.json written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
