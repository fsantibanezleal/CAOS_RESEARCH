"""EXP-026 exact campaign for the canonical grevlex staircase."""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import time
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
DEFAULT_CHECKPOINT = HERE / "artifacts" / "checkpoint.json"

PREMISES = {
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-023-one-cubic-defining-ideal/proof.md":
        "4f24c8bacf3ea4a7691142b6fbb2a79b40a1c200ec5051df3c79c3dc45bed084",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-024-extremal-betti-data/proof.md":
        "b7b654609cfca99e979b26741f7d2b6bbbfc0029d882c38e3c2932bfc9146088",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-025-curvilinear-primary-structure/proof.md":
        "70c7838ce843252aba335d80ade105d1d1942c490530ea7770483be0dff9a61f",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-025-curvilinear-primary-structure/run.py":
        "42411e5f8a166bd4a4663b49dfa3c19808b283735d2d633517c632e876f0377d",
}

Monomial = tuple[int, ...]
Relation = tuple[Monomial, Monomial]


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def interval(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def degree_one_offsets(p: int) -> set[int]:
    return (
        {0}
        | interval(1, p)
        | interval(3 * p, 4 * p - 2)
        | interval(6 * p, 8 * p - 2)
        | interval(8 * p, 10 * p - 2)
        | {10 * p}
        | interval(11 * p - 1, 12 * p - 1)
        | interval(13 * p + 1, 14 * p - 2)
        | interval(14 * p, 15 * p - 1)
        | {16 * p}
        | interval(17 * p - 1, 18 * p - 1)
    )


def expected_bases(p: int) -> list[set[int]]:
    q = 24 * p
    e1 = degree_one_offsets(p)
    e2 = interval(0, 2 * p) | interval(3 * p, 5 * p - 2) | interval(6 * p, q - 1)
    e3 = interval(0, q - 1) - {6 * p - 1}
    full = interval(0, q - 1)
    return [{0}, e1, e2, e3, full, full, full]


def bitset(values: set[int]) -> int:
    answer = 0
    for value in values:
        answer |= 1 << value
    return answer


def truncated_sum(left: int, generators: tuple[int, ...], q: int) -> int:
    answer = 0
    for generator in generators:
        answer |= left << generator
    return answer & ((1 << q) - 1)


def verify_premises() -> dict[str, str]:
    observed = {relative: file_hash(ROOT / relative) for relative in PREMISES}
    if observed != PREMISES:
        mismatch = {
            relative: {"expected": PREMISES[relative], "observed": observed[relative]}
            for relative in PREMISES
            if observed[relative] != PREMISES[relative]
        }
        raise RuntimeError(f"frozen premise mismatch: {mismatch}")
    return observed


def monomial(*offsets: int) -> Monomial:
    return tuple(sorted(offsets))


def divisors(value: Monomial) -> set[Monomial]:
    return {value[:index] + value[index + 1 :] for index in range(len(value))}


class Staircase:
    """Compact exact oracle for grevlex-smallest nondecreasing factorizations."""

    def __init__(self, p: int) -> None:
        self.p = p
        self.q = 24 * p
        self.offsets = tuple(sorted(degree_one_offsets(p)))
        self.offset_set = frozenset(self.offsets)

    @lru_cache(maxsize=None)
    def _canonical(self, degree: int, total: int, start: int) -> Monomial | None:
        if degree == 0:
            return () if total == 0 else None
        if total < 0 or start >= len(self.offsets):
            return None
        smallest = self.offsets[start]
        largest = self.offsets[-1]
        if degree * smallest > total or degree * largest < total:
            return None
        stop = bisect.bisect_right(self.offsets, total // degree)
        for index in range(start, stop):
            value = self.offsets[index]
            if value + (degree - 1) * largest < total:
                continue
            tail = self._canonical(degree - 1, total - value, index)
            if tail is not None:
                return (value,) + tail
        return None

    def canonical(self, degree: int, total: int) -> Monomial | None:
        if total >= self.q:
            return None
        return self._canonical(degree, total, 0)

    def is_standard(self, value: Monomial) -> bool:
        return self.canonical(len(value), sum(value)) == value

    def reverse_canonical_pair(self, total: int) -> Monomial | None:
        answer = None
        for left in self.offsets:
            right = total - left
            if right < left:
                break
            if right in self.offset_set:
                answer = (left, right)
        return answer


def cubic_relations(p: int) -> list[Relation]:
    relations: list[Relation] = []
    for i in range(1, p + 1):
        if i == 1:
            tail1 = monomial(0, 3 * p, 10 * p)
        elif i < p:
            tail1 = monomial(0, 0, 13 * p + i - 1)
        else:
            tail1 = monomial(0, 1, 14 * p - 2)
        relations.append((monomial(i, p, 12 * p - 1), tail1))

        tail2 = (
            monomial(0, i - 1, 16 * p)
            if i < p
            else monomial(0, 0, 17 * p - 1)
        )
        relations.append((monomial(i, p, 15 * p - 1), tail2))

        tail3 = (
            monomial(0, 3 * p + i - 1, 16 * p)
            if i < p
            else monomial(0, 3 * p, 17 * p - 1)
        )
        relations.append((monomial(i, p, 18 * p - 1), tail3))

        tail5 = (
            monomial(0, 7 * p + i - 2, 15 * p - 1)
            if i <= 2
            else monomial(0, 6 * p + i - 3, 16 * p)
        )
        relations.append((monomial(i, 4 * p - 2, 18 * p - 1), tail5))

    for i in range(1, p - 1):
        relations.append(
            (
                monomial(i, 4 * p - 2, 16 * p),
                monomial(0, 3 * p, 17 * p + i - 2),
            )
        )
    relations.append((monomial(p, p, p), monomial(0, 0, 3 * p)))
    return sorted(relations)


def quartic_relations(p: int) -> list[Relation]:
    return [
        (
            monomial(i, p, p, 4 * p - 2),
            monomial(0, 0, 0, 6 * p + i - 2),
        )
        for i in range(2, p)
    ]


def relation_hash(relations: list[Relation]) -> str:
    return canonical_hash([[list(lead), list(tail)] for lead, tail in sorted(relations)])


def validate_relation(staircase: Staircase, relation: Relation) -> None:
    lead, tail = relation
    if not set(lead + tail) <= staircase.offset_set:
        raise AssertionError(f"p={staircase.p}: relation uses a missing variable: {relation}")
    if len(lead) != len(tail) or sum(lead) != sum(tail):
        raise AssertionError(f"p={staircase.p}: relation is not bihomogeneous: {relation}")
    if not lead > tail:
        raise AssertionError(f"p={staircase.p}: wrong grevlex orientation: {relation}")
    if staircase.canonical(len(tail), sum(tail)) != tail:
        raise AssertionError(f"p={staircase.p}: noncanonical reduced tail: {relation}")
    if staircase.is_standard(lead):
        raise AssertionError(f"p={staircase.p}: proposed lead is standard: {lead}")
    if not all(staircase.is_standard(item) for item in divisors(lead)):
        raise AssertionError(f"p={staircase.p}: lead is not a minimal boundary: {lead}")


def zero_pair_count(offsets: tuple[int, ...], q: int) -> int:
    answer = 0
    for index, left in enumerate(offsets):
        first = max(index, bisect.bisect_left(offsets, q - left, lo=index))
        answer += len(offsets) - first
    return answer


def analyze_parameter(p: int) -> dict[str, object]:
    if p < 4:
        raise ValueError("EXP-026 is declared only for p>=4")
    staircase = Staircase(p)
    q = staircase.q
    offsets = staircase.offsets
    expected = expected_bases(p)

    current = bitset(set(offsets))
    dimensions = [1, len(offsets)]
    for degree in range(2, 7):
        current = truncated_sum(current, offsets, q)
        dimensions.append(current.bit_count())
        observed = {value for value in range(q) if (current >> value) & 1}
        if observed != expected[degree]:
            raise AssertionError(f"p={p}: degree-{degree} offset basis mismatch")
    expected_dimensions = [1, 10 * p, 22 * p, q - 1, q, q, q]
    if dimensions != expected_dimensions:
        raise AssertionError(f"p={p}: Hilbert dimensions {dimensions} != {expected_dimensions}")

    total_pairs = len(offsets) * (len(offsets) + 1) // 2
    zero_quadrics = zero_pair_count(offsets, q)
    standard_quadrics = len(expected[2])
    binomial_quadrics = total_pairs - zero_quadrics - standard_quadrics
    expected_zero = (23 * p * p + 15 * p - 2) // 2
    expected_binomial = (77 * p * p - 49 * p + 2) // 2
    if zero_quadrics != expected_zero or binomial_quadrics != expected_binomial:
        raise AssertionError(f"p={p}: quadratic type split mismatch")

    cubics = cubic_relations(p)
    quartics = quartic_relations(p)
    if len({lead for lead, _tail in cubics}) != 5 * p - 1:
        raise AssertionError(f"p={p}: cubic family collision")
    if len({lead for lead, _tail in quartics}) != p - 2:
        raise AssertionError(f"p={p}: quartic family collision")
    for relation in cubics + quartics:
        validate_relation(staircase, relation)
    if any(0 in lead for lead, _tail in cubics + quartics):
        raise AssertionError(f"p={p}: X_0 divides a nonquadratic leading monomial")

    quadratic_count = total_pairs - standard_quadrics
    profile = {"2": quadratic_count, "3": len(cubics), "4": len(quartics), "5": 0, "6": 0}
    expected_profile = {
        "2": 50 * p * p - 17 * p,
        "3": 5 * p - 1,
        "4": p - 2,
        "5": 0,
        "6": 0,
    }
    if profile != expected_profile:
        raise AssertionError(f"p={p}: degree profile {profile} != {expected_profile}")

    declared_pair = staircase.canonical(2, 4 * p)
    reverse_pair = staircase.reverse_canonical_pair(4 * p)
    controls = {
        "reversed_order_rejected": declared_pair != reverse_pair,
        "deleted_cubic_member_rejected": len(cubics) - 1 != 5 * p - 1,
        "shifted_quartic_endpoint_rejected": p - 1 != p - 2,
        "corrupted_tail_rejected": sum(monomial(0, 1, 3 * p)) != 3 * p,
        "wrong_total_offset_rejected": sum(monomial(p, p, p)) != sum(monomial(0, 1, 3 * p)),
        "x0_leading_generator_rejected": not any(0 in lead for lead, _tail in cubics + quartics),
        "degree_five_false_standard_rejected": not staircase.is_standard(monomial(p, p, p, p, p)),
        "eventual_hilbert_only_rejected": dimensions[:4] != [q, q, q, q],
    }
    if not all(controls.values()):
        raise AssertionError(f"p={p}: adversarial mutation survived: {controls}")

    row: dict[str, object] = {
        "p": p,
        "q": q,
        "variable_count": len(offsets),
        "term_order": "grevlex; X_a>X_b iff a>b; X_0 last",
        "hilbert_dimensions_0_to_6": dimensions,
        "quadratic_profile": {
            "total": quadratic_count,
            "binomial": binomial_quadrics,
            "monomial_zero": zero_quadrics,
        },
        "reduced_basis_degree_profile": profile,
        "reduced_basis_total": 50 * p * p - 11 * p - 3,
        "cubic_relation_hash": relation_hash(cubics),
        "quartic_relation_hash": relation_hash(quartics),
        "x0_divides_minimal_lead": False,
        "controls": controls,
    }
    row["row_hash"] = canonical_hash(row)
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=4)
    parser.add_argument("--last", type=int, default=300)
    parser.add_argument("--budget-seconds", type=float, default=120.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    args = parser.parse_args()
    if args.first < 4 or args.last < args.first:
        raise SystemExit("require 4 <= first <= last")

    started = time.perf_counter()
    premise_hashes = verify_premises()
    rows: list[dict[str, object]] = []
    status = "PASS"
    for p in range(args.first, args.last + 1):
        if time.perf_counter() - started > args.budget_seconds:
            status = "INCONCLUSIVE_BUDGET"
            break
        row = analyze_parameter(p)
        rows.append(row)
        write_json_atomic(
            args.checkpoint,
            {
                "experiment": "EXP-026",
                "status": "RUNNING",
                "first": args.first,
                "requested_last": args.last,
                "last_completed": p,
                "row_hashes": [item["row_hash"] for item in rows],
            },
        )
    if len(rows) != args.last - args.first + 1 and status == "PASS":
        status = "INCONCLUSIVE"
    result = {
        "experiment": "EXP-026-grevlex-staircase",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "range": {"first": args.first, "requested_last": args.last},
        "completed_rows": len(rows),
        "premise_hashes": premise_hashes,
        "campaign_aggregate": canonical_hash([row["row_hash"] for row in rows]),
        "elapsed_seconds": time.perf_counter() - started,
        "rows": rows,
    }
    write_json_atomic(args.output, result)
    write_json_atomic(
        args.checkpoint,
        {
            "experiment": "EXP-026",
            "status": status,
            "first": args.first,
            "requested_last": args.last,
            "last_completed": rows[-1]["p"] if rows else None,
            "row_hashes": [item["row_hash"] for item in rows],
        },
    )
    print(
        f"EXP-026 {status}: rows={len(rows)} aggregate={result['campaign_aggregate']} "
        f"elapsed={result['elapsed_seconds']:.3f}s"
    )
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())

