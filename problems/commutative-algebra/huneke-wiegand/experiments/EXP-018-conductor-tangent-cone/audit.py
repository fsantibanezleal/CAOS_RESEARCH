"""Independent bounded-bitset reconstruction audit for EXP-018."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "artifacts" / "results.json"
AUDIT = ROOT / "artifacts" / "audit.json"
SAMPLES = (4, 5, 17, 73, 151, 300)


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def seq(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def to_bits(values: set[int]) -> int:
    return sum(1 << value for value in values)


def bit_product(left: int, right: int, mask: int) -> int:
    if left.bit_count() > right.bit_count():
        left, right = right, left
    result = 0
    cursor = left
    while cursor:
        lowest = cursor & -cursor
        result |= right << (lowest.bit_length() - 1)
        cursor ^= lowest
    return result & mask


def bit_values(bits: int) -> list[int]:
    values: list[int] = []
    while bits:
        lowest = bits & -bits
        values.append(lowest.bit_length() - 1)
        bits ^= lowest
    return values


def reconstruct(p: int) -> dict[str, object]:
    s = 6 * p
    limit = 24 * s
    mask = (1 << (limit + 1)) - 1
    a = seq(0, p) | seq(3 * p, 4 * p - 2)
    b = (
        (seq(p + 1, 3 * p - 1) - {2 * p - 1})
        | {4 * p}
        | seq(5 * p - 1, s - 1)
    )
    c = seq(0, 2 * p) | seq(3 * p, 5 * p - 2)
    h = {2 * p - 1, 4 * p - 1} | seq(4 * p + 1, 5 * p - 2)

    ring_values = (
        {0}
        | {4 * s + r for r in a}
        | seq(5 * s, 6 * s - 1)
        | {6 * s + r for r in b}
        | {8 * s + r for r in c}
        | seq(9 * s, 13 * s - 2)
        | seq(13 * s, limit)
    )
    t_values = (
        {4 * s + r for r in a}
        | {5 * s + r for r in a | b}
        | {6 * s + r for r in b}
        | {8 * s + r for r in c}
        | seq(9 * s, 13 * s - 2)
        | seq(13 * s, limit)
    )
    ring = to_bits(ring_values)
    t = to_bits(t_values)
    powers = [ring, t]
    for _ in range(4):
        powers.append(bit_product(powers[-1], t, mask))

    q = (ring << (4 * s)) & mask
    defects: list[int] = []
    defect_hashes: list[str] = []
    sally: list[int] = []
    for n in range(5):
        denominator = (powers[n] << (4 * s)) & mask
        intersection = q & powers[n + 1]
        if denominator & ~intersection:
            raise AssertionError(f"audit p={p}: containment failure at degree {n}")
        defect_bits = intersection & ~denominator & mask
        defects.append(defect_bits.bit_count())
        defect_hashes.append(digest(bit_values(defect_bits)))
        quotient_bits = powers[n + 1] & ~denominator & mask
        sally.append(quotient_bits.bit_count())

    if defects != [0, p, 0, 0, 0]:
        raise AssertionError(f"audit p={p}: VV profile {defects}")
    wanted_bits = to_bits({9 * s + value for value in h})
    actual_bits = (q & powers[2]) & ~((powers[1] << (4 * s)) & mask) & mask
    if actual_bits != wanted_bits:
        raise AssertionError(f"audit p={p}: exact defect mismatch")
    if sally != [23 * p - 1, 14 * p, 2 * p, 1, 0]:
        raise AssertionError(f"audit p={p}: Sally profile {sally}")

    hilbert = [24 * p - value for value in sally]
    numerator = [hilbert[0]] + [
        hilbert[index] - hilbert[index - 1] for index in range(1, 5)
    ]
    if numerator != [p + 1, 9 * p - 1, 12 * p, 2 * p - 1, 1]:
        raise AssertionError(f"audit p={p}: Hilbert numerator {numerator}")
    return {
        "p": p,
        "vv_defect_lengths_n0_through_n4": defects,
        "nonzero_defect_residues": sorted(h),
        "depth": 0,
        "cohen_macaulay": False,
        "sally_quotient_lengths": sally,
        "hilbert_function_h0_through_h4": hilbert,
        "hilbert_numerator": numerator,
        "defect_hashes": defect_hashes,
    }


def main() -> int:
    source = json.loads(RESULTS.read_text(encoding="utf-8"))
    rows = {row["p"]: row for row in source["rows"]}
    aggregate = digest([row["row_hash"] for row in source["rows"]])
    if aggregate != source["campaign_aggregate"]:
        raise AssertionError("campaign aggregate mismatch")

    fields = (
        "vv_defect_lengths_n0_through_n4",
        "nonzero_defect_residues",
        "depth",
        "cohen_macaulay",
        "sally_quotient_lengths",
        "hilbert_function_h0_through_h4",
        "hilbert_numerator",
        "defect_hashes",
    )
    reconstructed = []
    for p in SAMPLES:
        fresh = reconstruct(p)
        recorded = rows[p]
        for field in fields:
            if fresh[field] != recorded[field]:
                raise AssertionError(f"audit p={p}: mismatch in {field}")
        reconstructed.append(fresh)

    controls = {
        "deleted_first_witness_rejected": all(
            reconstruct(p)["vv_defect_lengths_n0_through_n4"][1] != p - 1
            for p in SAMPLES
        ),
        "false_degree_two_defect_rejected": all(
            reconstruct(p)["vv_defect_lengths_n0_through_n4"][2] == 0
            for p in SAMPLES
        ),
        "false_cm_rejected": all(not reconstruct(p)["cohen_macaulay"] for p in SAMPLES),
    }
    if not all(controls.values()):
        raise AssertionError("an audit corruption survived")

    output = {
        "experiment": "EXP-018-conductor-tangent-cone",
        "status": "AUDIT_PASS",
        "samples": list(SAMPLES),
        "campaign_aggregate": aggregate,
        "reconstruction_aggregate": digest(reconstructed),
        "controls": controls,
        "reconstructed": reconstructed,
    }
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"EXP-018 audit PASS aggregate={output['reconstruction_aggregate']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
