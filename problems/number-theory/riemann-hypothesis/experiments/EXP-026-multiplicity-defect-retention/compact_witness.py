"""Certify the single compact isolation configuration declared before this run."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import time

from flint import arb, ctx, fmpq

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "EXP-025-vector-pressure-distinct-lift"


def a(x):
    return arb(fmpq(x.numerator, x.denominator))


def ball(lo, hi):
    return arb(a((lo+hi)/2), a((hi-lo)/2))


def certify():
    started = time.process_time()
    ctx.prec = 256
    spec = importlib.util.spec_from_file_location("source025", SOURCE / "run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    raw = (SOURCE / "artifacts/input/Solution.lean").read_bytes()
    coeffs, _, pressures = module.source_packet(raw)
    cs = [a(x) for x in coeffs]
    freqs = [arb(2).sqrt()]+[2*j*arb.pi() for j in range(1, 13)]
    norm = sum((c*(w/2).sinc() for c, w in zip(cs, freqs)), arb(0))
    assert norm > 0

    def kernel(x):
        assert time.process_time()-started < 20, "CPU budget exhausted"
        return sum((c*(((w+2*arb.pi()*x)/2).sinc()+((w-2*arb.pi()*x)/2).sinc())/2
                    for c, w in zip(cs, freqs)), arb(0))/norm

    def sign(x):
        y = kernel(a(x))
        assert y > 0 or y < 0, f"Unresolved sign at {x}"
        return (1 if y > 0 else -1), str(y)

    roots = []
    grid = [F(1, 2)+F(j, 16) for j in range(121)]
    signs = [sign(x) for x in grid]
    for i in range(120):
        if signs[i][0] == signs[i+1][0]:
            continue
        lo, hi, slo = grid[i], grid[i+1], signs[i][0]
        while hi-lo > F(1, 2**40):
            mid = (lo+hi)/2
            smid, _ = sign(mid)
            if smid == slo:
                lo = mid
            else:
                hi = mid
        roots.append({"lo": str(lo), "hi": str(hi),
                      "K_lo": sign(lo)[1], "K_hi": sign(hi)[1]})
        if len(roots) == 6:
            break
    assert len(roots) == 6, "Insufficient certified sign-changing roots"
    intervals = [ball(F(r["lo"]), F(r["hi"])) for r in roots]
    points = [arb(0)]+intervals
    # At the exact IVT roots the doubled row vanishes identically. All other
    # entries are enclosed for every independent choice inside the brackets.
    upper = [[arb(0) for _ in range(7)] for _ in range(7)]
    energy = arb(0)
    for i in range(1, 7):
        for j in range(i+1, 7):
            value = kernel(points[j]-points[i])
            upper[i][j] = upper[j][i] = value.abs_upper()
            energy += 2*value**2
    unit_rows = [1+sum(row, arb(0)) for row in upper]
    # Simple rows match unit rows; the isolated doubled row has diagonal two.
    weighted_rows = [arb(2)]+unit_rows[1:]
    c = a(F(17043, 5000))
    assert all(row < c for row in unit_rows), "Unit Gram clipping uncertified"
    assert all(row < c for row in weighted_rows), "Weighted Gram clipping uncertified"
    assert energy > 0, "Positive simple-block energy uncertified"
    gaps = [points[i+1]-points[i] for i in range(6)]
    charge = sum((a(b)*gap for b, gap in zip(pressures, gaps)), arb(0))
    delta = a(F(39369, 5000000))
    assert charge < delta, "Pressure exceeds declared local budget"
    return {"source_sha256": hashlib.sha256(raw).hexdigest(), "precision_bits": 256,
            "grid": {"start": "1/2", "end": "8", "step": "1/16", "cells": 120},
            "root_intervals": roots, "root_width_target": "1/1099511627776",
            "multiplicities": [2, 1, 1, 1, 1, 1, 1],
            "unit_gram_row_upper_bounds": [str(x) for x in unit_rows],
            "weighted_gram_row_upper_bounds": [str(x) for x in weighted_rows],
            "clipping_threshold": "17043/5000", "simple_block_energy": str(energy),
            "gap_enclosures": [str(x) for x in gaps], "pressure_charge": str(charge),
            "pressure_budget": "39369/5000000", "exact_root_remainder": "0",
            "scope": "Actual kernel point Grams; no assertion these are zeta-zero gaps.",
            "arithmetic_trust": "FLINT/Arb; exact IVT roots are defined by disjoint sign brackets.",
            "cpu_seconds": time.process_time()-started}


def run(receipt):
    if receipt.exists():
        raise SystemExit("Preserve the previous receipt")
    result = {"schema": "exp026-compact-isolation-v1", "passed": False,
              "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "declaration_sha256": hashlib.sha256((HERE / "compact-witness-declaration.md").read_bytes()).hexdigest()}
    try:
        result["certificate"] = certify()
        result["passed"] = True
    except (AssertionError, ValueError) as error:
        result["failure"] = str(error)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    raise SystemExit(run(parser.parse_args().receipt))
