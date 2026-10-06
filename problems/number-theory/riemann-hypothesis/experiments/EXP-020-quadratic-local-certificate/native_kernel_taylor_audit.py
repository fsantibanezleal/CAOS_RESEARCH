"""Native midpoint 0F1 with whole-cell kernel-first Taylor enclosures."""

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import struct
import time

from flint import arb, ctx, fmpq

HERE = Path(__file__).resolve().parent
PACKET = HERE.parents[1]/"experiments/EXP-018-nine-point-distinct-transfer/artifacts/input/nine-point-final.json"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def exact(value):
    if isinstance(value, Fraction):
        return arb(fmpq(value.numerator, value.denominator))
    numerator, denominator = value.as_integer_ratio()
    return arb(fmpq(numerator, denominator))


def sinc_jet(z):
    u = -z*z/4
    f3 = u.hypgeom_0f1(arb(fmpq(3, 2)))
    f5 = u.hypgeom_0f1(arb(fmpq(5, 2)))
    f7 = u.hypgeom_0f1(arb(fmpq(7, 2)))
    f9 = u.hypgeom_0f1(arb(fmpq(9, 2)))
    return f3, -z*f5/3, -f5/3+z*z*f7/15, z*f7/5-z*z*z*f9/105


class BudgetExpired(Exception):
    pass


def run(directory, cells, seconds):
    started = time.monotonic()
    ctx.prec = 256
    packet_raw = PACKET.read_bytes()
    binding = json.loads((directory/"run-binding.json").read_bytes())
    if sha(packet_raw) != binding["packet_sha256"] or binding["cells"] != 61029 or binding["grid"] != 4000:
        raise ValueError("input binding changed")
    packet = json.loads(packet_raw)
    coefficients = [arb(fmpq(n, packet["window_coefficient_denominator"]))
                    for n in packet["window_coefficient_numerators"]]
    pi = arb.pi()
    omegas = [arb(2).sqrt()]+[2*j*pi for j in range(1, 7)]
    k0 = sum((c*sinc_jet(w/2)[0] for c, w in zip(coefficients, omegas)), arb(0))
    if not k0 > 0:
        raise ValueError("normalization unresolved")
    coefficient_bound = sum((arb(c.abs_upper()) for c in coefficients), arb(0))
    amplitude = coefficient_bound/k0
    k2_bound = arb((pi*pi*coefficient_bound).abs_upper())
    w4_bound = arb(((2*pi)**4*amplitude**2).abs_upper())
    for z in [arb(1), arb(2), arb(fmpq(1, 8))]:
        direct = (z.sin()/z, (z*z.cos()-z.sin())/(z*z),
                  ((2-z*z)*z.sin()-2*z*z.cos())/(z*z*z),
                  ((6*z-z**3)*z.cos()+(3*z*z-6)*z.sin())/z**4)
        if not all((left-right).contains(0) for left, right in zip(sinc_jet(z), direct)):
            raise ValueError("native jet identity control disagreement")
    if not all((left-right).contains(0) for left, right in zip(sinc_jet(arb(0)), [arb(1), arb(0), -arb(1)/3, arb(0)])):
        raise ValueError("native zero jet control disagreement")
    tables = []
    for name in ["w.bin", "w-second.bin"]:
        raw = (directory/"tables"/name).read_bytes()
        if sha(raw) != binding["tables"][name] or len(raw) != 8*binding["cells"]:
            raise ValueError("table binding changed")
        values = struct.unpack(f">{binding['cells']}d", raw)
        if not all(math.isfinite(value) for value in values):
            raise ValueError("nonfinite table")
        tables.append(values)
    counts = {"subcell_enclosures": 0, "accepted_subcells": 0, "maximum_bisection_depth": 0}

    def lower_bounds(lo, hi):
        midpoint = exact((lo+hi)/2)
        radius = exact((hi-lo)/2)
        k = arb(0)
        first = arb(0)
        second = arb(0)
        third = arb(0)
        for coefficient, omega in zip(coefficients, omegas):
            vm, dm, d2m, d3m = sinc_jet(omega/2-pi*midpoint)
            vp, dp, d2p, d3p = sinc_jet(omega/2+pi*midpoint)
            k += coefficient*(vm+vp)/2
            first += coefficient*pi*(dp-dm)/2
            second += coefficient*pi*pi*(d2m+d2p)/2
            third += coefficient*pi**3*(d3p-d3m)/2
        normalization = k0*k0
        w2 = 2*(first*first+k*second)/normalization
        w3 = 2*(3*first*second+k*third)/normalization
        kernel_error = arb(first.abs_upper())*radius+k2_bound*radius*radius/2
        # The Arb constructor rounds this exact upper error outward. It is
        # not converted to binary64 or truncated before building the ball.
        kernel_cell = k+arb(0, kernel_error.abs_upper())
        magnitude_lower = arb((kernel_cell/k0).abs_lower())
        w_lower = magnitude_lower*magnitude_lower
        second_lower = w2-arb(w3.abs_upper())*radius-w4_bound*radius*radius/2
        return w_lower, second_lower

    control_lo, control_hi = Fraction(0), Fraction(1, 4000)
    control_bounds = lower_bounds(control_lo, control_hi)
    # Deliberately raise each stored test value above its enclosure's upper
    # endpoint. These are in-memory controls; actual tables remain untouched.
    rejection_controls = [not (value >= arb(value.upper())+1) for value in control_bounds]
    if not all(rejection_controls):
        raise ValueError("increased lower-bound control accepted")

    def compare(index, lo, hi, depth):
        if time.monotonic()-started >= seconds:
            raise BudgetExpired
        counts["subcell_enclosures"] += 1
        counts["maximum_bisection_depth"] = max(counts["maximum_bisection_depth"], depth)
        lower = lower_bounds(lo, hi)
        if all(value >= exact(table[index]) for value, table in zip(lower, tables)):
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
            print(f"native-kernel-taylor completed={completed}/{cells} elapsed={time.monotonic()-started:.3f}s", flush=True)
    elapsed = time.monotonic()-started
    return {"schema": "exp020-native-kernel-taylor-audit-v1", "all_cells_passed": completed == binding["cells"],
            "requested_range_passed": completed == cells, "requested_cells": cells,
            "completed_closed_cells": completed, "table_cells": binding["cells"],
            "unresolved_cell": unresolved, "budget_expired": expired, "budget_seconds": seconds,
            "elapsed_seconds": elapsed, "projected_full_seconds": elapsed*binding["cells"]/completed if completed else None,
            "precision_bits": 256, "counts": counts, "increased_bound_controls_rejected": rejection_controls,
            "global_k2_bound": str(k2_bound), "global_w4_bound": str(w4_bound),
            "tables_sha256": binding["tables"], "packet_sha256": sha(packet_raw),
            "source_sha256": sha(Path(__file__).read_bytes()),
            "declaration_sha256": sha((HERE/"native-kernel-taylor-declaration.md").read_bytes()),
            "scope": "native hypergeometric midpoint evaluations with whole-cell kernel/Fourier Taylor bounds; shared FLINT/Arb trust base; not full multidimensional cover"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--cells", type=int, default=512)
    parser.add_argument("--seconds", type=float, default=30)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.cells <= 61029 or not 0 < args.seconds <= 600:
        parser.error("declared cell/budget bounds exceeded")
    if args.receipt.exists():
        parser.error("preserve existing audit receipt")
    result = run(args.output_dir, args.cells, args.seconds)
    args.receipt.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
