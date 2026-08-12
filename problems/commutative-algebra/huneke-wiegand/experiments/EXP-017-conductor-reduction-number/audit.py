"""Independent reconstruction audit for EXP-017."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
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


@dataclass(frozen=True)
class TailSet:
    low: frozenset[int]
    tail: int


def values(p: int) -> tuple[int, TailSet, TailSet]:
    s = 6 * p
    a = seq(0, p) | seq(3 * p, 4 * p - 2)
    b = ((seq(p + 1, 3 * p - 1) - {2 * p - 1}) | {4 * p} | seq(5 * p - 1, s - 1))
    c = seq(0, 2 * p) | seq(3 * p, 5 * p - 2)
    ring = (
        {0}
        | {4 * s + r for r in a}
        | seq(5 * s, 6 * s - 1)
        | {6 * s + r for r in b}
        | {8 * s + r for r in c}
        | seq(9 * s, 13 * s - 2)
    )
    conductor = (
        {4 * s + r for r in a}
        | {5 * s + r for r in a | b}
        | {6 * s + r for r in b}
        | {8 * s + r for r in c}
        | seq(9 * s, 13 * s - 2)
    )
    return s, TailSet(frozenset(ring), 13 * s), TailSet(frozenset(conductor), 13 * s)


def bit_sum(left: frozenset[int], right: frozenset[int], stop: int) -> set[int]:
    if len(left) > len(right):
        left, right = right, left
    mask = sum(1 << value for value in right)
    total = 0
    for value in left:
        total |= mask << value
    total &= (1 << (stop + 1)) - 1
    result: set[int] = set()
    while total:
        one = total & -total
        result.add(one.bit_length() - 1)
        total ^= one
    return result


def multiply(left: TailSet, right: TailSet) -> TailSet:
    left_minimum = min(left.low) if left.low else left.tail
    right_minimum = min(right.low) if right.low else right.tail
    bound = min(left_minimum + right.tail, right_minimum + left.tail)
    sums = bit_sum(left.low, right.low, bound - 1)
    minimum_sum = left_minimum + right_minimum
    gaps = seq(minimum_sum, bound - 1) - sums
    tail = max(gaps) + 1 if gaps else minimum_sum
    return TailSet(frozenset(value for value in sums if value < tail), tail)


def shift(value: TailSet, amount: int) -> TailSet:
    return TailSet(frozenset(item + amount for item in value.low), value.tail + amount)


def members(value: TailSet, stop: int) -> set[int]:
    return set(value.low) | seq(value.tail, stop)


def difference(top: TailSet, bottom: TailSet) -> set[int]:
    stop = bottom.tail - 1
    a, b = members(top, stop), members(bottom, stop)
    if b - a:
        raise AssertionError(f"audit containment failure at {min(b-a)}")
    return a - b


def reconstruct(p: int) -> dict[str, object]:
    s, ring, t = values(p)
    powers = [t]
    for _ in range(4):
        powers.append(multiply(powers[-1], t))
    quotients = [difference(t, shift(ring, 4 * s))]
    quotients.extend(
        difference(powers[index], shift(powers[index - 1], 4 * s))
        for index in range(1, 5)
    )
    lengths = [len(value) for value in quotients]
    if lengths != [23 * p - 1, 14 * p, 2 * p, 1, 0]:
        raise AssertionError(f"audit p={p}: length profile {lengths}")
    terminal = 17 * s - 1
    if terminal not in quotients[2] or quotients[3] != {terminal}:
        raise AssertionError(f"audit p={p}: terminal persistence failure")
    if powers[4] != shift(powers[3], 4 * s):
        raise AssertionError(f"audit p={p}: reduction equality failure")
    return {
        "p": p,
        "quotient_lengths": lengths,
        "reduction_number": 4,
        "e0": len(difference(ring, shift(ring, 4 * s))),
        "e1": sum(lengths[:-1]),
        "defect_hashes": [digest(sorted(value)) for value in quotients],
    }


def main() -> int:
    source = json.loads(RESULTS.read_text(encoding="utf-8"))
    rows = {row["p"]: row for row in source["rows"]}
    reconstructed = []
    for p in SAMPLES:
        fresh = reconstruct(p)
        recorded = rows[p]
        for key in ("quotient_lengths", "reduction_number", "e0", "e1", "defect_hashes"):
            if fresh[key] != recorded[key]:
                raise AssertionError(f"audit p={p}: mismatch in {key}")
        reconstructed.append(fresh)
    aggregate = digest([row["row_hash"] for row in source["rows"]])
    if aggregate != source["campaign_aggregate"]:
        raise AssertionError("campaign aggregate mismatch")
    controls = {
        "deleted_terminal_rejected": all(reconstruct(p)["quotient_lengths"][2] != 2 * p - 1 for p in SAMPLES),
        "false_early_stability_rejected": all(reconstruct(p)["quotient_lengths"][3] == 1 for p in SAMPLES),
        "perturbed_e1_rejected": all(reconstruct(p)["e1"] != 39 * p + 1 for p in SAMPLES),
    }
    if not all(controls.values()):
        raise AssertionError("an audit corruption survived")
    output = {
        "experiment": "EXP-017-conductor-reduction-number",
        "status": "AUDIT_PASS",
        "samples": list(SAMPLES),
        "campaign_aggregate": aggregate,
        "reconstruction_aggregate": digest(reconstructed),
        "controls": controls,
        "reconstructed": reconstructed,
    }
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"EXP-017 audit PASS aggregate={output['reconstruction_aggregate']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
