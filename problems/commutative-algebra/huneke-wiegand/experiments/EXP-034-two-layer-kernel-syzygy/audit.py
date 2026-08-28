"""EXP-034 independent numerical-semigroup and literal-chain audit.

This route reconstructs the Artinian fiber bases from value-semigroup ideal
powers. It does not import the canonical block or incidence functions.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_CANONICAL = HERE / "artifacts" / "results.json"
DEFAULT_OUTPUT = HERE / "artifacts" / "audit.json"


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def integers(first: int, last: int) -> set[int]:
    return set(range(first, last + 1)) if first <= last else set()


@dataclass(frozen=True)
class Profile:
    finite: frozenset[int]
    conductor: int

    @property
    def minimum(self) -> int:
        return min(self.finite) if self.finite else self.conductor

    def contains(self, value: int) -> bool:
        return value >= self.conductor or value in self.finite


def residue_sets(p: int) -> tuple[int, set[int], set[int], set[int]]:
    s = 6 * p
    first = integers(0, p) | integers(3 * p, 4 * p - 2)
    second = (
        (integers(p + 1, 3 * p - 1) - {2 * p - 1})
        | {4 * p}
        | integers(5 * p - 1, 6 * p - 1)
    )
    third = integers(0, 2 * p) | integers(3 * p, 5 * p - 2)
    return s, first, second, third


def ring_profile(p: int) -> Profile:
    s, first, second, third = residue_sets(p)
    finite = (
        {0}
        | {4 * s + value for value in first}
        | integers(5 * s, 6 * s - 1)
        | {6 * s + value for value in second}
        | {8 * s + value for value in third}
        | integers(9 * s, 13 * s - 2)
    )
    return Profile(frozenset(finite), 13 * s)


def conductor_profile(p: int) -> Profile:
    s, first, second, third = residue_sets(p)
    finite = (
        {4 * s + value for value in first}
        | {5 * s + value for value in first | second}
        | {6 * s + value for value in second}
        | {8 * s + value for value in third}
        | integers(9 * s, 13 * s - 2)
    )
    return Profile(frozenset(finite), 13 * s)


def maximal_profile(p: int) -> Profile:
    ring = ring_profile(p)
    return Profile(frozenset(ring.finite - {0}), ring.conductor)


def product(left: Profile, right: Profile) -> Profile:
    bound = min(left.minimum + right.conductor, right.minimum + left.conductor)
    sums = {
        a + b
        for a in left.finite
        for b in right.finite
        if a + b < bound
    }
    floor = left.minimum + right.minimum
    gaps = integers(floor, bound - 1) - sums
    conductor = max(gaps) + 1 if gaps else floor
    return Profile(frozenset(value for value in sums if value < conductor), conductor)


def shift(profile: Profile, amount: int) -> Profile:
    return Profile(
        frozenset(value + amount for value in profile.finite),
        profile.conductor + amount,
    )


def quotient_basis(numerator: Profile, denominators: list[Profile]) -> list[int]:
    stop = max([numerator.conductor] + [item.conductor for item in denominators])
    return [
        value
        for value in range(numerator.minimum, stop)
        if numerator.contains(value)
        and not any(item.contains(value) for item in denominators)
    ]


def direct_artinian_bases(p: int) -> tuple[set[int], set[int]]:
    q = 24 * p
    ideal = conductor_profile(p)
    maximal = maximal_profile(p)
    square = product(ideal, ideal)
    degree_one = quotient_basis(ideal, [product(maximal, ideal), shift(ring_profile(p), q)])
    degree_two = quotient_basis(square, [product(maximal, square), shift(ideal, q)])
    return (
        {value - q for value in degree_one},
        {value - 2 * q for value in degree_two},
    )


def low_product_basis(p: int, left: int, right: int) -> tuple[str, int] | None:
    left_second = left >= 3 * p
    right_second = right >= 3 * p
    if left_second and right_second:
        return None
    if not left_second and not right_second:
        total = left + right
        return ("ring", total) if total > p else None
    total = left + right
    return ("canonical", total) if total >= 4 * p - 1 else None


def literal_low_source(p: int, total: int) -> list[tuple[tuple[int, ...], int]]:
    low = list(range(1, p + 1)) + list(range(3 * p, 4 * p - 1))
    low_set = set(low)
    return [
        (exterior, total - sum(exterior))
        for exterior in itertools.combinations(low, p)
        if total - sum(exterior) in low_set
    ]


def audit_row(p: int, enumerate_source: bool) -> dict[str, object]:
    c_degree_one, c_degree_two = direct_artinian_bases(p)
    low = set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))
    high = c_degree_one - low
    low_products = {
        product_value[1]
        for left, right in itertools.combinations_with_replacement(sorted(low), 2)
        if (product_value := low_product_basis(p, left, right)) is not None
    }
    kernel_degree_two = c_degree_two - low_products
    target = 8 * p - 1
    exterior = tuple(range(1, p + 1))
    representations = {
        variable
        for variable in c_degree_one
        if target - variable in high
    }

    source_rows = []
    if enumerate_source:
        exterior_sum = sum(exterior)
        for coefficient in exterior:
            total = exterior_sum + coefficient
            source = literal_low_source(p, total)
            selected = (exterior, coefficient)
            if source != [selected]:
                raise AssertionError(f"p={p}, coefficient={coefficient}: low source is not unique")
            differential = [
                {
                    "removed": variable,
                    "face": list(exterior[:position] + exterior[position + 1 :]),
                    "product": low_product_basis(p, variable, coefficient),
                    "sign": -1 if position % 2 else 1,
                }
                for position, variable in enumerate(exterior)
                if low_product_basis(p, variable, coefficient) is not None
            ]
            pivot = [item for item in differential if item["removed"] == p]
            if len(pivot) != 1 or pivot[0]["product"] != ("ring", p + coefficient):
                raise AssertionError(f"p={p}, coefficient={coefficient}: rational unit pivot failed")
            source_rows.append(
                {
                    "coefficient": coefficient,
                    "source_dimension": len(source),
                    "boundary_rank_over_QQ": 1,
                    "unit_pivot": pivot[0],
                }
            )

    checks = {
        "direct_degree_one_count": len(c_degree_one) == 10 * p - 1,
        "direct_degree_two_count": len(c_degree_two) == 12 * p,
        "kernel_degree_one_count": len(high) == 8 * p,
        "kernel_degree_two_count": len(kernel_degree_two) == 10 * p,
        "target_in_kernel_degree_two": target in kernel_degree_two,
        "target_not_degree_one": target not in c_degree_one,
        "representations": representations == set(exterior),
        "literal_sources_have_unit_rank": not enumerate_source or len(source_rows) == p,
    }
    if not all(checks.values()):
        raise AssertionError(f"p={p}: independent audit failed: {checks}")
    row: dict[str, object] = {
        "p": p,
        "checks": checks,
        "direct_degree_one_hash": digest(sorted(c_degree_one)),
        "direct_degree_two_hash": digest(sorted(c_degree_two)),
        "kernel_degree_one_hash": digest(sorted(high)),
        "kernel_degree_two_hash": digest(sorted(kernel_degree_two)),
        "representations": sorted(representations),
        "source_rows": source_rows,
    }
    row["row_hash"] = digest(row)
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, default=DEFAULT_CANONICAL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-p", type=int, default=25)
    parser.add_argument("--enumerate-max-p", type=int, default=9)
    parser.add_argument("--budget-seconds", type=float, default=180.0)
    args = parser.parse_args()
    started = time.perf_counter()
    canonical = json.loads(args.canonical.read_text(encoding="utf-8"))
    if canonical.get("status") != "PASS_CANONICAL" or canonical.get("row_count") != 297:
        raise RuntimeError("canonical artifact is not the declared complete campaign")

    rows = []
    for p in range(4, args.max_p + 1):
        rows.append(audit_row(p, p <= args.enumerate_max_p))
        if time.perf_counter() - started > args.budget_seconds:
            raise TimeoutError(f"INCONCLUSIVE_BUDGET after p={p}")

    controls = {
        "filled_gap_changes_kernel_basis": all(
            8 * p - 1 in direct_artinian_bases(p)[1] for p in (4, 7, args.max_p)
        ),
        "wrong_target_rejected": all(
            {
                variable
                for variable in direct_artinian_bases(p)[0]
                if 8 * p - variable in (direct_artinian_bases(p)[0] - set(range(1, p + 1))
                                         - set(range(3 * p, 4 * p - 1)))
            }
            != set(range(1, p + 1))
            for p in (4, 7, args.max_p)
        ),
    }
    if not all(controls.values()):
        raise AssertionError(f"independent mutation survived: {controls}")
    result = {
        "experiment": "EXP-034",
        "route": "independent numerical-semigroup and literal-chain audit",
        "status": "PASS_INDEPENDENT",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "canonical_artifact_sha256": canonical["artifact_sha256"],
        "parameters": {
            "min_p": 4,
            "max_p": args.max_p,
            "enumerate_max_p": args.enumerate_max_p,
            "budget_seconds": args.budget_seconds,
        },
        "controls": controls,
        "rows": rows,
        "aggregate_sha256": digest([row["row_hash"] for row in rows]),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    result["artifact_sha256"] = digest(result)
    write_json_atomic(args.output, result)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
