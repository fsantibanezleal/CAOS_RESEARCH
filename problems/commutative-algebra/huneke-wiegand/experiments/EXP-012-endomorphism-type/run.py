"""EXP-012: pseudo-Frobenius anatomy of the EXP-011 endomorphism family.

CPU only. Exact integer and bitset arithmetic. No randomness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "artifacts/results.json"


def interval(start: int, stop: int) -> set[int]:
    """Return an inclusive integer interval."""
    return set(range(start, stop + 1)) if start <= stop else set()


def family_sets(
    p: int,
) -> tuple[int, set[int], set[int], set[int], set[int]]:
    if p < 4:
        raise ValueError("EXP-012 is declared only for p>=4")
    s = 6 * p
    a = interval(0, p) | interval(3 * p, 4 * p - 2)
    b = (
        (interval(p + 1, 3 * p - 1) - {2 * p - 1})
        | {4 * p}
        | interval(5 * p - 1, 6 * p - 1)
    )
    c = interval(0, 2 * p) | interval(3 * p, 5 * p - 2)
    q = interval(p + 1, 2 * p - 2) | {2 * p, 4 * p}
    return s, a, b, c, q


def interval_bits(start: int, stop: int, limit: int) -> int:
    start = max(start, 0)
    stop = min(stop, limit)
    if start > stop:
        return 0
    return ((1 << (stop - start + 1)) - 1) << start


def value_bits(values: set[int], offset: int, limit: int) -> int:
    bits = 0
    for value in values:
        shifted = offset + value
        if shifted <= limit:
            bits |= 1 << shifted
    return bits


def lambda_bits(p: int, limit: int) -> int:
    s, a, b, c, q = family_sets(p)
    bits = 1
    bits |= value_bits(a, 4 * s, limit)
    bits |= interval_bits(5 * s, 6 * s - 1, limit)
    bits |= value_bits(b, 6 * s, limit)
    bits |= value_bits(q, 7 * s, limit)
    bits |= value_bits(c, 8 * s, limit)
    bits |= interval_bits(9 * s, limit, limit)
    return bits


def minimal_generators(p: int) -> tuple[int, ...]:
    s, a, b, _, q = family_sets(p)
    return tuple(
        sorted(
            {4 * s + residue for residue in a}
            | interval(5 * s, 6 * s - 1)
            | {6 * s + residue for residue in b}
            | {7 * s + residue for residue in q}
        )
    )


def predicted_pf(p: int) -> tuple[int, ...]:
    s, _, b, c, q = family_sets(p)
    universe = interval(0, s - 1)
    return tuple(
        sorted(
            {6 * s + residue for residue in universe - b}
            | {7 * s + residue for residue in universe - q}
            | {8 * s + residue for residue in universe - c}
        )
    )


def route_a_pf(bits: int, frobenius: int, generators: tuple[int, ...]) -> int:
    """Test every gap against all minimal generators simultaneously."""
    eligible = (1 << (frobenius + 1)) - 1
    for generator in generators:
        eligible &= bits >> generator
    gap_mask = ((1 << (frobenius + 1)) - 1) & ~bits
    return gap_mask & eligible


def route_b_pf(bits: int, multiplicity: int, generators: tuple[int, ...]) -> int:
    """Find maximal Apéry elements under the semigroup order."""
    apery: list[int] = []
    for residue in range(multiplicity):
        value = residue
        while not bits & (1 << value):
            value += multiplicity
        apery.append(value)
    apery_bits = sum(1 << value for value in apery)
    nonmaximal = 0
    for generator in generators:
        nonmaximal |= apery_bits >> generator
    maximal_apery = apery_bits & ~nonmaximal
    return maximal_apery >> multiplicity


def values_from_bits(bits: int, limit: int) -> tuple[int, ...]:
    return tuple(value for value in range(limit + 1) if bits & (1 << value))


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def analyze_parameter(p: int) -> dict[str, object]:
    s, _, _, _, _ = family_sets(p)
    multiplicity = 4 * s
    frobenius = 9 * s - 1
    conductor = frobenius + 1
    generators = minimal_generators(p)
    limit = frobenius + max(generators)
    bits = lambda_bits(p, limit)

    route_a = route_a_pf(bits, frobenius, generators)
    route_b = route_b_pf(bits, multiplicity, generators)
    prediction = predicted_pf(p)
    prediction_bits = sum(1 << value for value in prediction)
    if route_a != route_b:
        delta = route_a ^ route_b
        witness = (delta & -delta).bit_length() - 1
        raise AssertionError(f"p={p}: PF routes disagree at {witness}")
    if route_a != prediction_bits:
        delta = route_a ^ prediction_bits
        witness = (delta & -delta).bit_length() - 1
        raise AssertionError(f"p={p}: PF formula disagrees at {witness}")

    pf_values = values_from_bits(route_a, frobenius)
    reduced_window = interval_bits(conductor - multiplicity, frobenius, frobenius)
    reduced_type = ((~bits) & reduced_window).bit_count()
    genus = ((~bits) & ((1 << conductor) - 1) & ~1).bit_count()
    reflected_pf = {
        frobenius - value for value in pf_values if value != frobenius
    }
    almost_symmetric_direct = reflected_pf <= set(pf_values)
    almost_symmetric_genus = 2 * genus == frobenius + len(pf_values)
    if almost_symmetric_direct != almost_symmetric_genus:
        raise AssertionError(f"p={p}: almost-symmetry criteria disagree")

    expected = {
        "type": 10 * p,
        "reduced_type": 10 * p,
        "maximal_reduced_type": True,
        "almost_symmetric": False,
    }
    observed = {
        "type": len(pf_values),
        "reduced_type": reduced_type,
        "maximal_reduced_type": reduced_type == len(pf_values),
        "almost_symmetric": almost_symmetric_direct,
    }
    if observed != expected:
        raise AssertionError(f"p={p}: invariants {observed}, expected {expected}")
    if min(pf_values) < conductor - multiplicity:
        raise AssertionError(f"p={p}: unexpected lower pseudo-Frobenius number")

    deleted_control = prediction_bits & ~(1 << prediction[0])
    injected_control = prediction_bits | (1 << (5 * s - 1))
    if deleted_control == route_a or injected_control == route_a:
        raise AssertionError(f"p={p}: corrupted PF control was accepted")

    row: dict[str, object] = {
        "p": p,
        "s": s,
        "type": len(pf_values),
        "reduced_type": reduced_type,
        "maximal_reduced_type": True,
        "almost_symmetric": False,
        "first_pf": pf_values[0],
        "last_pf": pf_values[-1],
        "pf_hash": canonical_hash(pf_values),
        "controls": {
            "deleted_pf_rejected": True,
            "injected_lower_gap_rejected": True,
        },
    }
    row["row_hash"] = canonical_hash(row)
    return row


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=4)
    parser.add_argument("--last", type=int, default=300)
    parser.add_argument("--output", type=Path, default=RESULTS)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.first < 4 or args.last < args.first:
        raise ValueError("require 4<=first<=last")
    started = time.perf_counter()
    rows: list[dict[str, object]] = []
    print(f"EXP-012 exact campaign p={args.first},...,{args.last}", flush=True)
    for p in range(args.first, args.last + 1):
        rows.append(analyze_parameter(p))
        if p in {args.first, args.first + 1} or p % 25 == 0 or p == args.last:
            print(f"p={p}: PASS", flush=True)
        if time.perf_counter() - started > 120:
            raise TimeoutError("EXP-012 exceeded its declared two-minute budget")

    aggregate = canonical_hash([row["row_hash"] for row in rows])
    output = {
        "experiment": "EXP-012-endomorphism-type",
        "status": "COMPUTATIONAL_PASS",
        "range": {
            "first": args.first,
            "last": args.last,
            "count": len(rows),
        },
        "predictions": {
            "P1": "PASS_PF_FORMULA",
            "P2": "PASS_TYPE_AND_REDUCED_TYPE_10P",
            "P3": "PASS_MAXIMAL_REDUCED_TYPE",
            "P4": "PASS_NOT_ALMOST_SYMMETRIC",
            "P5": "PENDING_SYMBOLIC_PROOF_AND_AUDIT",
        },
        "campaign_aggregate": aggregate,
        "rows": rows,
    }
    write_json_atomic(args.output, output)
    print(f"EXP-012 computational PASS aggregate={aggregate}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
