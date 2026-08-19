"""EXP-011: exact endomorphism overrings for the EXP-009 family.

CPU only. Exact integer and bitset arithmetic. No randomness.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "artifacts"
RESULTS = ARTIFACTS / "results.json"


def interval(start: int, stop: int) -> tuple[int, ...]:
    """Return the inclusive integer interval, or the empty tuple."""
    return tuple(range(start, stop + 1)) if start <= stop else ()


def family_sets(p: int) -> tuple[int, set[int], set[int], set[int], set[int]]:
    if p < 4:
        raise ValueError("EXP-011 is declared only for p>=4")
    s = 6 * p
    a = set(interval(0, p)) | set(interval(3 * p, 4 * p - 2))
    b = (
        (set(interval(p + 1, 3 * p - 1)) - {2 * p - 1})
        | {4 * p}
        | set(interval(5 * p - 1, 6 * p - 1))
    )
    c = set(interval(0, 2 * p)) | set(interval(3 * p, 5 * p - 2))
    q = set(interval(p + 1, 2 * p - 2)) | {2 * p, 4 * p}
    return s, a, b, c, q


def interval_bits(start: int, stop: int, limit: int) -> int:
    start = max(start, 0)
    stop = min(stop, limit)
    if start > stop:
        return 0
    return ((1 << (stop - start + 1)) - 1) << start


def value_bits(values: set[int] | tuple[int, ...], offset: int, limit: int) -> int:
    bits = 0
    for value in values:
        shifted = offset + value
        if 0 <= shifted <= limit:
            bits |= 1 << shifted
    return bits


def gamma_generators(p: int) -> tuple[int, ...]:
    s, a, b, _, _ = family_sets(p)
    return tuple(
        sorted(
            {4 * s + residue for residue in a}
            | set(interval(5 * s, 6 * s - 1))
            | {6 * s + residue for residue in b}
        )
    )


def explicit_gamma_bits(p: int, limit: int) -> int:
    s, a, b, c, _ = family_sets(p)
    bits = 1
    bits |= value_bits(a, 4 * s, limit)
    bits |= interval_bits(5 * s, 6 * s - 1, limit)
    bits |= value_bits(b, 6 * s, limit)
    bits |= value_bits(c, 8 * s, limit)
    bits |= interval_bits(9 * s, 13 * s - 2, limit)
    bits |= interval_bits(13 * s, limit, limit)
    return bits


def generated_bits(generators: tuple[int, ...], limit: int) -> int:
    """Generate the semigroup through limit by exact bounded sum layers."""
    mask = (1 << (limit + 1)) - 1
    exact = 1
    reachable = 1
    max_terms = limit // min(generators)
    for _ in range(max_terms):
        following = 0
        for generator in generators:
            following |= exact << generator
        following &= mask
        if following == 0:
            break
        reachable |= following
        exact = following
    return reachable


def bits_hash(bits: int, limit: int) -> str:
    length = (limit + 8) // 8
    payload = (bits & ((1 << (limit + 1)) - 1)).to_bytes(length, "little")
    return hashlib.sha256(payload).hexdigest()


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def invariants(bits: int, limit: int) -> dict[str, int | bool]:
    tail_width = 32
    tail = interval_bits(limit - tail_width + 1, limit, limit)
    if bits & tail != tail:
        raise AssertionError("membership window does not end in a proved tail")
    window_mask = (1 << (limit + 1)) - 1
    gaps = (~bits) & window_mask
    frobenius = gaps.bit_length() - 1
    conductor = frobenius + 1
    genus_mask = ((1 << conductor) - 1) & ~1
    genus = ((~bits) & genus_mask).bit_count()
    symmetry_failure = next(
        (
            value
            for value in range(frobenius + 1)
            if bool(bits & (1 << value))
            == bool(bits & (1 << (frobenius - value)))
        ),
        None,
    )
    multiplicity = next(value for value in range(1, conductor) if bits & (1 << value))
    return {
        "multiplicity": multiplicity,
        "frobenius": frobenius,
        "conductor": conductor,
        "genus": genus,
        "symmetric": symmetry_failure is None,
        "first_symmetry_failure": -1 if symmetry_failure is None else symmetry_failure,
    }


def analyze_parameter(p: int) -> dict[str, object]:
    s, _, _, _, q = family_sets(p)
    limit = 19 * s
    gamma_limit = limit + s
    mask = (1 << (limit + 1)) - 1
    gamma_mask = (1 << (gamma_limit + 1)) - 1

    gamma_formula_full = explicit_gamma_bits(p, gamma_limit)
    gamma_gens = gamma_generators(p)
    gamma_generated_full = generated_bits(gamma_gens, gamma_limit)
    if gamma_formula_full != gamma_generated_full:
        raise AssertionError(f"p={p}: generated Gamma disagrees with formula")

    value_set = (
        gamma_generated_full | (gamma_generated_full << s)
    ) & gamma_mask
    lambda_semantic = value_set & (value_set >> s) & mask

    old_frobenius = 13 * s - 1
    gamma_formula = gamma_formula_full & mask
    lambda_formula = gamma_formula | value_bits(q, 7 * s, limit) | (1 << old_frobenius)
    if lambda_semantic != lambda_formula:
        delta = lambda_semantic ^ lambda_formula
        witness = (delta & -delta).bit_length() - 1
        raise AssertionError(f"p={p}: Lambda formula mismatch at {witness}")

    lambda_gens = tuple(sorted(set(gamma_gens) | {7 * s + residue for residue in q}))
    lambda_generated = generated_bits(lambda_gens, limit)
    if lambda_generated != lambda_semantic:
        delta = lambda_generated ^ lambda_semantic
        witness = (delta & -delta).bit_length() - 1
        raise AssertionError(f"p={p}: generated Lambda mismatch at {witness}")

    data = invariants(lambda_semantic, limit)
    expected = {
        "multiplicity": 24 * p,
        "frobenius": 54 * p - 1,
        "conductor": 54 * p,
        "genus": 38 * p - 1,
        "symmetric": False,
    }
    for key, value in expected.items():
        if data[key] != value:
            raise AssertionError(f"p={p}: {key}={data[key]}, expected {value}")

    extras_bits = lambda_semantic & ~gamma_formula & mask
    extras = tuple(value for value in range(limit + 1) if extras_bits & (1 << value))
    predicted_extras = tuple(sorted({7 * s + residue for residue in q} | {old_frobenius}))
    if extras != predicted_extras:
        raise AssertionError(f"p={p}: incorrect Lambda minus Gamma")
    if len(extras) != p + 1:
        raise AssertionError(f"p={p}: extra count is {len(extras)}, expected {p + 1}")
    if len(lambda_gens) != 12 * p:
        raise AssertionError(f"p={p}: embedding dimension is not 12p")

    missing_q_control = lambda_formula & ~(1 << (7 * s + p + 1))
    if missing_q_control == lambda_semantic:
        raise AssertionError(f"p={p}: missing-Q corruption was not rejected")
    shifted_terminal_control = lambda_formula & ~(1 << old_frobenius)
    shifted_terminal_control |= 1 << (old_frobenius + 1)
    if shifted_terminal_control == lambda_semantic:
        raise AssertionError(f"p={p}: terminal corruption was not rejected")

    row: dict[str, object] = {
        "p": p,
        "s": s,
        "q_count": len(q),
        "extra_count": len(extras),
        "embedding_dimension": len(lambda_gens),
        "invariants": data,
        "gamma_hash": bits_hash(gamma_formula, 13 * s - 1),
        "lambda_hash": bits_hash(lambda_semantic, 13 * s - 1),
        "first_extra": extras[0],
        "last_extra": extras[-1],
        "controls": {"missing_q_rejected": True, "terminal_shift_rejected": True},
    }
    row["row_hash"] = canonical_hash(row)
    return row


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    started = time.perf_counter()
    rows: list[dict[str, object]] = []
    print("EXP-011 exact campaign p=4,...,300", flush=True)
    for p in range(4, 301):
        rows.append(analyze_parameter(p))
        if p in {4, 5} or p % 25 == 0 or p == 300:
            print(f"p={p}: PASS", flush=True)
        if time.perf_counter() - started > 120:
            raise TimeoutError("EXP-011 exceeded its declared two-minute budget")

    aggregate = canonical_hash([row["row_hash"] for row in rows])
    output = {
        "experiment": "EXP-011-endomorphism-family",
        "status": "COMPUTATIONAL_PASS",
        "range": {"first": 4, "last": 300, "count": len(rows)},
        "predictions": {
            "P1": "PASS",
            "P2": "PASS",
            "P3": "PASS",
            "P4": "PASS",
            "P5": "PENDING_SYMBOLIC_PROOF",
            "P6": "PASS_ROUTE_A_ROUTE_B_CONTROLS",
        },
        "campaign_aggregate": aggregate,
        "rows": rows,
    }
    write_json_atomic(RESULTS, output)
    print(f"EXP-011 computational PASS aggregate={aggregate}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
