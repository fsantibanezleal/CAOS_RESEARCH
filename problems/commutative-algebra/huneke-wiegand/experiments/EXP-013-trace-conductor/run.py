"""EXP-013: exact trace and conductor ideals for the EXP-009 family.

CPU only. Exact finite set arithmetic. No randomness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "artifacts" / "results.json"


def interval(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def family_sets(p: int) -> tuple[int, set[int], set[int], set[int], set[int], set[int]]:
    if p < 4:
        raise ValueError("EXP-013 is declared only for p>=4")
    s = 6 * p
    a = interval(0, p) | interval(3 * p, 4 * p - 2)
    b = (
        (interval(p + 1, 3 * p - 1) - {2 * p - 1})
        | {4 * p}
        | interval(5 * p - 1, 6 * p - 1)
    )
    c = interval(0, 2 * p) | interval(3 * p, 5 * p - 2)
    q = interval(p + 1, 2 * p - 2) | {2 * p, 4 * p}
    h = {s - 1 - residue for residue in q}
    return s, a, b, c, q, h


def gamma_contains(value: int, p: int) -> bool:
    if value == 0:
        return True
    if value < 0:
        return False
    s, a, b, c, _, _ = family_sets(p)
    level, residue = divmod(value, s)
    if level == 4:
        return residue in a
    if level == 5:
        return True
    if level == 6:
        return residue in b
    if level == 8:
        return residue in c
    if 9 <= level <= 11:
        return True
    if level == 12:
        return residue <= s - 2
    return level >= 13


def lambda_contains(value: int, p: int) -> bool:
    if gamma_contains(value, p):
        return True
    s, _, _, _, q, _ = family_sets(p)
    level, residue = divmod(value, s)
    return (level == 7 and residue in q) or value == 13 * s - 1


def predicted_trace_contains(value: int, p: int) -> bool:
    s, a, b, c, _, _ = family_sets(p)
    level, residue = divmod(value, s)
    return (
        (level == 4 and residue in a)
        or (level == 5 and residue in a | b)
        or (level == 6 and residue in b)
        or (level == 8 and residue in c)
        or (level >= 9 and gamma_contains(value, p))
    )


def values(predicate: object, p: int, limit: int) -> set[int]:
    return {value for value in range(limit + 1) if predicate(value, p)}  # type: ignore[operator]


def minkowski(left: set[int], right: set[int], limit: int) -> set[int]:
    return {x + y for x in left for y in right if x + y <= limit}


def route_a(p: int, limit: int) -> tuple[set[int], set[int], set[int]]:
    """Construct the two colons and traces from their module definitions."""
    s, _, _, _, _, _ = family_sets(p)
    gamma = values(gamma_contains, p, limit + s)
    _, _, _, _, q, _ = family_sets(p)
    new_e_values = {7 * s + residue for residue in q} | {13 * s - 1}

    # Since 1 belongs to J, R:J is a subset of Gamma; only the second generator is new.
    r_colon_j = {n for n in gamma if n <= limit and gamma_contains(n + s, p)}
    # W=R:J is a Gamma-ideal, so J*W=W union (s+W).
    trace_j = r_colon_j | {n + s for n in r_colon_j if n + s <= limit}

    # It suffices to check Lambda below the conductor of Gamma minus n.
    r_colon_e = {
        n
        for n in gamma
        if n <= limit
        and all(gamma_contains(n + e, p) for e in new_e_values)
    }
    # Verify the conductor is stable under the generators outside Gamma.
    if any(
        n + e <= limit and n + e not in r_colon_e
        for n in r_colon_e
        for e in new_e_values
    ):
        raise AssertionError(f"p={p}: R:E is not stable under E")
    trace_e = set(r_colon_e)
    return trace_j, r_colon_e, trace_e


def route_b(p: int, limit: int) -> tuple[set[int], set[int], set[int]]:
    """Evaluate independent valuewise colon and sum predicates."""
    s, _, _, _, _, _ = family_sets(p)
    gamma_window = [n for n in range(limit + 1) if gamma_contains(n, p)]
    _, _, _, _, q, _ = family_sets(p)
    lambda_new = [7 * s + residue for residue in q] + [13 * s - 1]
    w = [n for n in gamma_window if gamma_contains(n + s, p)]

    trace_j = {
        value
        for value in range(limit + 1)
        if value in w or (value >= s and value - s in w)
    }
    conductor = {
        n
        for n in gamma_window
        if not any(not gamma_contains(n + e, p) for e in lambda_new)
    }
    trace_e = {
        value
        for value in range(limit + 1)
        if value in conductor
    }
    return trace_j, conductor, trace_e


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def set_hash(data: set[int]) -> str:
    return canonical_hash(sorted(data))


def analyze_parameter(p: int) -> dict[str, object]:
    s, _, _, _, q, h = family_sets(p)
    limit = 15 * s
    predicted = values(predicted_trace_contains, p, limit)
    a_trace_j, a_conductor, a_trace_e = route_a(p, limit)
    b_trace_j, b_conductor, b_trace_e = route_b(p, limit)

    six_sets = (a_trace_j, a_conductor, a_trace_e, b_trace_j, b_conductor, b_trace_e)
    if any(candidate != predicted for candidate in six_sets):
        candidate = next(candidate for candidate in six_sets if candidate != predicted)
        witness = min(candidate ^ predicted)
        raise AssertionError(f"p={p}: trace/conductor formula mismatch at {witness}")

    gamma_below_tail = values(gamma_contains, p, 9 * s - 1)
    trace_below_tail = {value for value in predicted if value < 9 * s}
    colength = len(gamma_below_tail - trace_below_tail)
    if colength != p + 1:
        raise AssertionError(f"p={p}: colength {colength}, expected {p + 1}")
    if h != ({2 * p - 1, 4 * p - 1} | interval(4 * p + 1, 5 * p - 2)):
        raise AssertionError(f"p={p}: reflected obstruction formula failed")
    if len(q) != p or len(h) != p:
        raise AssertionError(f"p={p}: block cardinality failed")

    deleted = predicted - {4 * s}
    injected = predicted | {5 * s + min(h)}
    altered_lambda = lambda value: lambda_contains(value, p) and value != 7 * s + min(q)
    altered_conductor = {
        n
        for n in range(limit + 1)
        if gamma_contains(n, p)
        and all(
            gamma_contains(n + e, p)
            for e in range(13 * s)
            if altered_lambda(e) and n + e < 13 * s
        )
    }
    if deleted == a_trace_j or injected == a_conductor or altered_conductor == a_conductor:
        raise AssertionError(f"p={p}: an adversarial mutation was not rejected")

    first = min(predicted)
    finite_missing = sorted(gamma_below_tail - trace_below_tail)
    row: dict[str, object] = {
        "p": p,
        "s": s,
        "q_count": len(q),
        "reflected_obstruction_count": len(h),
        "colength": colength,
        "first_trace_value": first,
        "full_intermediate_start": 9 * s,
        "tail_start": 13 * s,
        "first_missing_r_value": finite_missing[0],
        "last_missing_r_value": finite_missing[-1],
        "trace_hash_through_15s": set_hash(predicted),
        "controls": {
            "deleted_trace_value_rejected": True,
            "injected_obstruction_rejected": True,
            "altered_overring_rejected": True,
        },
    }
    row["row_hash"] = canonical_hash(row)
    return row


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=4)
    parser.add_argument("--last", type=int, default=300)
    parser.add_argument("--output", type=Path, default=RESULTS)
    args = parser.parse_args()
    started = time.perf_counter()
    rows: list[dict[str, object]] = []
    print(f"EXP-013 exact campaign p={args.first},...,{args.last}", flush=True)
    for p in range(args.first, args.last + 1):
        rows.append(analyze_parameter(p))
        if p in {args.first, args.first + 1, args.last} or p % 25 == 0:
            print(f"p={p}: PASS", flush=True)
        if time.perf_counter() - started > 120:
            raise TimeoutError("EXP-013 exceeded its declared two-minute budget")
    aggregate = canonical_hash([row["row_hash"] for row in rows])
    output = {
        "experiment": "EXP-013-trace-conductor",
        "status": "COMPUTATIONAL_PASS",
        "range": {"first": args.first, "last": args.last, "count": len(rows)},
        "predictions": {
            "exact_common_ideal": "PASS",
            "colength_p_plus_1": "PASS",
            "independent_routes": "PASS",
            "adversarial_controls": "PASS",
            "all_parameter_theorem": "PENDING_SYMBOLIC_PROOF",
        },
        "campaign_aggregate": aggregate,
        "rows": rows,
    }
    write_json_atomic(args.output, output)
    print(f"EXP-013 computational PASS aggregate={aggregate}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
