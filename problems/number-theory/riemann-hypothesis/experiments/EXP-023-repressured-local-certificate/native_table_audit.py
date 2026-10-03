"""Independent whole-cell 0F1 enclosures for bound EXP-023 kernel tables."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import struct
import time

from flint import arb, ctx, fmpq

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
PACKET = PROBLEM/"experiments/EXP-018-nine-point-distinct-transfer/artifacts/input/nine-point-final.json"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def rational(value):
    numerator, denominator = value.as_integer_ratio()
    return arb(fmpq(numerator, denominator))


def sinc_derivatives(z):
    u = -z*z/4
    f3 = u.hypgeom_0f1(arb(fmpq(3, 2)))
    f5 = u.hypgeom_0f1(arb(fmpq(5, 2)))
    f7 = u.hypgeom_0f1(arb(fmpq(7, 2)))
    return f3, -z*f5/3, -f5/3+z*z*f7/15


class BudgetExpired(Exception):
    pass


def run(directory, cells, seconds):
    started = time.monotonic()
    ctx.prec = 256
    packet_raw = PACKET.read_bytes()
    binding = json.loads((directory/"run-binding.json").read_bytes())
    if sha(packet_raw) != binding["packet_sha256"] or binding["cells"] != 52240 or binding["grid"] != 4000:
        raise ValueError("input binding changed")
    packet = json.loads(packet_raw)
    coefficients = [arb(fmpq(n, packet["window_coefficient_denominator"]))
                    for n in packet["window_coefficient_numerators"]]
    omegas = [arb(2).sqrt()]+[2*j*arb.pi() for j in range(1, 7)]
    k0 = sum((c*sinc_derivatives(w/2)[0] for c, w in zip(coefficients, omegas)), arb(0))
    if not k0 > 0:
        raise ValueError("normalization unresolved")
    for z in [arb(1), arb(2), arb(fmpq(1, 8))]:
        value, first, second = sinc_derivatives(z)
        direct = (z.sin()/z, (z*z.cos()-z.sin())/(z*z),
                  ((2-z*z)*z.sin()-2*z*z.cos())/(z*z*z))
        if not all((left-right).contains(0) for left, right in zip([value, first, second], direct)):
            raise ValueError("normalization control disagreement")
    zero = sinc_derivatives(arb(0))
    if not all((left-right).contains(0) for left, right in zip(zero, [arb(1), arb(0), -arb(1)/3])):
        raise ValueError("zero control disagreement")
    tables = []
    for name in ["w.bin", "w-second.bin"]:
        raw = (directory/"tables"/name).read_bytes()
        if sha(raw) != binding["tables"][name] or len(raw) != 8*binding["cells"]:
            raise ValueError("table binding changed")
        tables.append(struct.unpack(f">{binding['cells']}d", raw))
    counts = {"subcell_enclosures": 0, "accepted_subcells": 0, "maximum_bisection_depth": 0}
    pi = arb.pi()

    def compare(index, lo, hi, depth):
        if time.monotonic()-started >= seconds:
            raise BudgetExpired
        counts["subcell_enclosures"] += 1
        counts["maximum_bisection_depth"] = max(counts["maximum_bisection_depth"], depth)
        center, radius = (lo+hi)/2, (hi-lo)/2
        x = arb(fmpq(center.numerator, center.denominator), fmpq(radius.numerator, radius.denominator))
        k = first = second = arb(0)
        for coefficient, omega in zip(coefficients, omegas):
            vm, dm, d2m = sinc_derivatives(omega/2-pi*x)
            vp, dp, d2p = sinc_derivatives(omega/2+pi*x)
            k += coefficient*(vm+vp)/2
            first += coefficient*pi*(dp-dm)/2
            second += coefficient*pi*pi*(d2m+d2p)/2
        magnitude_lower = arb((k/k0).abs_lower())
        w_lower = magnitude_lower*magnitude_lower
        w_second = 2*(first*first+k*second)/(k0*k0)
        if w_lower >= rational(tables[0][index]) and w_second >= rational(tables[1][index]):
            counts["accepted_subcells"] += 1
            return True
        if depth == 8:
            return False
        middle = (lo+hi)/2
        return compare(index, lo, middle, depth+1) and compare(index, middle, hi, depth+1)

    completed, unresolved, expired = 0, None, False
    for index in range(cells):
        try:
            passed = compare(index, Fraction(index, 4000), Fraction(index+1, 4000), 0)
        except BudgetExpired:
            expired = True
            break
        if not passed:
            unresolved = index
            break
        completed += 1
        if completed % 512 == 0:
            print(f"native-table completed={completed}/{cells} elapsed={time.monotonic()-started:.3f}s", flush=True)
    elapsed = time.monotonic()-started
    return {"schema": "exp023-native-table-audit-v1", "all_cells_passed": completed == binding["cells"],
            "requested_range_passed": completed == cells, "requested_cells": cells,
            "completed_closed_cells": completed, "table_cells": binding["cells"],
            "unresolved_cell": unresolved, "budget_expired": expired, "budget_seconds": seconds,
            "elapsed_seconds": elapsed, "projected_full_seconds": elapsed*binding["cells"]/completed if completed else None,
            "precision_bits": 256, "counts": counts, "tables_sha256": binding["tables"],
            "packet_sha256": sha(packet_raw), "source_sha256": sha(Path(__file__).read_bytes()),
            "declaration_sha256": sha((HERE/"native-table-audit-declaration.md").read_bytes()),
            "scope": "native hypergeometric whole-cell table input audit; shared FLINT/Arb trust base; not complete multidimensional cover"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cells", type=int, default=512)
    parser.add_argument("--seconds", type=float, default=30)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.cells <= 52240 or not 0 < args.seconds <= 600:
        parser.error("declared cell/budget bounds exceeded")
    if args.receipt.exists():
        parser.error("preserve existing audit receipt")
    result = run(args.output_dir, args.cells, args.seconds)
    args.receipt.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
