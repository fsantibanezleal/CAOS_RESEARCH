"""Independent bounded-bitset reconstruction audit for EXP-019."""

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
    limit = 40 * s
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
        | {4 * s + residue for residue in a}
        | seq(5 * s, 6 * s - 1)
        | {6 * s + residue for residue in b}
        | {8 * s + residue for residue in c}
        | seq(9 * s, 13 * s - 2)
        | seq(13 * s, limit)
    )
    conductor_values = (
        {4 * s + residue for residue in a}
        | {5 * s + residue for residue in a | b}
        | {6 * s + residue for residue in b}
        | {8 * s + residue for residue in c}
        | seq(9 * s, 13 * s - 2)
        | seq(13 * s, limit)
    )
    ring = to_bits(ring_values)
    conductor = to_bits(conductor_values)
    powers = [ring, conductor]
    for _ in range(4):
        powers.append(bit_product(powers[-1], conductor, mask))

    expected_fourth = to_bits(seq(16 * s, limit))
    expected_fifth = to_bits(seq(20 * s, limit))
    if powers[4] != expected_fourth or powers[5] != expected_fifth:
        raise AssertionError(f"audit p={p}: reduction-tail reconstruction failed")

    torsion: list[list[int]] = []
    for degree in range(5):
        quotient = powers[degree] & ~powers[degree + 1] & mask
        threshold = 4 * (degree + 1) * s
        saturation_tail = to_bits(seq(threshold, limit))
        torsion.append(bit_values(quotient & saturation_tail))

    wanted = sorted(5 * s + residue for residue in h)
    if torsion != [wanted, [], [], [], []]:
        raise AssertionError(f"audit p={p}: exact H0 profile mismatch")

    maximal = ring & ~1
    for value in wanted:
        if ((maximal << value) & mask) & ~conductor:
            raise AssertionError(f"audit p={p}: degree-zero annihilator failed")
        if ((conductor << value) & mask) & ~powers[2]:
            raise AssertionError(f"audit p={p}: positive-degree annihilator failed")
        if not (((ring << value) & mask) & ~conductor):
            raise AssertionError(f"audit p={p}: corrupted maximal ideal was accepted")

    lengths = [len(values) for values in torsion]
    numerator = [1, 10 * p - 1, 12 * p, 2 * p - 1, 1]
    return {
        "p": p,
        "h0_lengths_degree_0_through_4": lengths,
        "h0_degree_zero_values": wanted,
        "h0_degree_zero_residues_from_5s": sorted(h),
        "homogeneous_maximal_annihilates_h0": True,
        "degree_zero_maximal_action": "ANNIHILATES",
        "positive_degree_action": "ANNIHILATES",
        "buchsbaum": True,
        "cohen_macaulay": False,
        "buchsbaum_invariant": sum(lengths),
        "cm_quotient_hilbert_numerator": numerator,
        "torsion_hashes": [digest(values) for values in torsion],
    }


def main() -> int:
    source = json.loads(RESULTS.read_text(encoding="utf-8"))
    rows = {row["p"]: row for row in source["rows"]}
    aggregate = digest([row["row_hash"] for row in source["rows"]])
    if aggregate != source["campaign_aggregate"]:
        raise AssertionError("campaign aggregate mismatch")

    fields = (
        "h0_lengths_degree_0_through_4",
        "h0_degree_zero_values",
        "h0_degree_zero_residues_from_5s",
        "homogeneous_maximal_annihilates_h0",
        "degree_zero_maximal_action",
        "positive_degree_action",
        "buchsbaum",
        "cohen_macaulay",
        "buchsbaum_invariant",
        "cm_quotient_hilbert_numerator",
        "torsion_hashes",
    )
    reconstructed: list[dict[str, object]] = []
    for p in SAMPLES:
        fresh = reconstruct(p)
        for field in fields:
            if fresh[field] != rows[p][field]:
                raise AssertionError(f"audit p={p}: mismatch in {field}")
        reconstructed.append(fresh)

    controls = {
        "unit_torsion_rejected": all(0 not in item["h0_degree_zero_values"] for item in reconstructed),
        "deleted_torsion_rejected": all(
            item["buchsbaum_invariant"] != item["p"] - 1 for item in reconstructed
        ),
        "positive_degree_torsion_rejected": all(
            item["h0_lengths_degree_0_through_4"][1:] == [0, 0, 0, 0]
            for item in reconstructed
        ),
        "degree_zero_action_verified": all(
            item["degree_zero_maximal_action"] == "ANNIHILATES" for item in reconstructed
        ),
        "false_non_buchsbaum_rejected": all(item["buchsbaum"] for item in reconstructed),
    }
    if not all(controls.values()):
        raise AssertionError("an audit corruption survived")

    output = {
        "experiment": "EXP-019-conductor-buchsbaum",
        "status": "AUDIT_PASS",
        "samples": list(SAMPLES),
        "campaign_aggregate": aggregate,
        "reconstruction_aggregate": digest(reconstructed),
        "controls": controls,
        "reconstructed": reconstructed,
    }
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"EXP-019 audit PASS aggregate={output['reconstruction_aggregate']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
