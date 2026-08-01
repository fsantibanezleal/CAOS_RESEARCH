"""EXP-003: exact z_max(6) via the last-gate scan over the depth-5 frontier.

Deterministic, headless, exact. See hypothesis.md (committed before run).
Usage: python run.py [--smoke]   (smoke: scan depth-4 frontier, expect
z_max(5) = 4 and 11,377 new polys, reproducing EXP-002)
"""

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))

from tclib.enum import (  # noqa: E402
    INPUTS,
    census_polynomials,
    find_witness_program,
    integer_roots,
    last_gate_scan,
    peval,
    two_adic_valuations,
)

T0 = time.time()
ART = HERE / "artifacts"

EXPECTED_STATES = {1: 9, 2: 98, 3: 1462, 4: 29506, 5: 778087}
EXPECTED_NEW5 = 11377


def log(msg):
    print(f"[{time.time() - T0:8.1f}s] {msg}", flush=True)


def checkpoint(payload):
    ART.mkdir(exist_ok=True)
    tmp = ART / "scan6.json.tmp"
    tmp.write_text(json.dumps(payload, indent=1, sort_keys=True),
                   encoding="utf-8")
    tmp.replace(ART / "scan6.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    base_depth = 4 if args.smoke else 5
    deadline = T0 + (300 if args.smoke else 3000)  # 50 min kill

    log(f"EXP-003: rebuild frontier to depth {base_depth}")
    per_depth, first_seen, complete, frontier = census_polynomials(
        base_depth, deadline=deadline, return_frontier=True,
        progress=lambda d, r: log(f"  depth {d}: states={r['states']}"))

    for d in range(1, base_depth + 1):
        if not complete.get(d) or \
                per_depth[d]["states"] != EXPECTED_STATES[d]:
            log(f"REGRESSION GATE FAIL at depth {d}")
            checkpoint({"gate": "FAIL", "per_depth": per_depth})
            return 1
    log(f"frontier gate PASS ({len(frontier)} states)")

    log("last-gate scan...")
    new_polys, scan_complete, scanned = last_gate_scan(
        frontier, set(first_seen) | set(INPUTS), deadline=deadline,
        progress=lambda c, n: log(f"  scanned {c} states, {n} new polys"))
    log(f"scan: complete={scan_complete} states={scanned} "
        f"new_polys={len(new_polys)}")

    zmax_prev = 4 if not args.smoke else 3
    zmax, records = zmax_prev, []
    zcounts = {}
    for p in new_polys:
        z = len(integer_roots(p))
        zcounts[z] = zcounts.get(z, 0) + 1
        if z > zmax:
            zmax, records = z, [p]
        elif z == zmax and len(records) < 40:
            if z > zmax_prev:
                records.append(p)
    log(f"z_max(depth {base_depth + 1}) = {zmax} "
        f"(records beyond previous max: {len(records)})")

    rec_payload = []
    for p in sorted(records):
        roots = sorted(integer_roots(p))
        rec_payload.append({
            "poly": list(p),
            "roots": roots,
            "twoadic_valuations_nonzero_roots":
                sorted(two_adic_valuations(set(roots))),
        })

    witnesses = {}
    if not args.smoke and scan_complete:
        for rec in rec_payload[:3]:
            target = tuple(rec["poly"])
            prog_ops = find_witness_program(target, base_depth + 1)
            witnesses[str(rec["poly"])] = prog_ops
            if prog_ops:
                assert tuple(prog_ops[-1][3]) == target
                for r in rec["roots"]:
                    assert peval(target, r) == 0

    payload = {
        "base_depth": base_depth,
        "scan_complete": scan_complete,
        "states_scanned": scanned,
        "new_polynomials": len(new_polys),
        "z_histogram_new": {str(k): v for k, v in sorted(zcounts.items())},
        "zmax": zmax,
        "records_beyond_previous": rec_payload,
        "witness_programs": witnesses,
        "smoke": args.smoke,
    }
    checkpoint(payload)
    log("done; artifacts/scan6.json written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
