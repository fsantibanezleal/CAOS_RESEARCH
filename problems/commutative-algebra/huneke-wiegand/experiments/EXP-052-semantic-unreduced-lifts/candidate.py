"""Frozen EXP-052 semantic candidate learned from p=8,9,10 only."""

from __future__ import annotations

import json


def sign(exponent: int) -> int:
    return -1 if exponent & 1 else 1


def endpoint(value: int, tag: str, first: int, last: int) -> list[object]:
    left = value - first
    right = last - value
    return [tag, "L", left] if left <= right else [tag, "R", right]


def affine(value: int, p: int) -> list[int]:
    slope = min(range(25), key=lambda candidate: (abs(value - candidate * p), candidate))
    return [slope, value - slope * p]


def token(
    *, p: int, kind: str, missing_l0: set[int], missing_l1: set[int], product: int
) -> dict[str, object]:
    return {
        "kind": kind,
        "product": affine(product, p),
        "l0_missing": [endpoint(value, "L0", 1, p) for value in sorted(missing_l0)],
        "l1_missing": [
            endpoint(value, "L1", 3 * p, 4 * p - 2) for value in sorted(missing_l1)
        ],
        "high_selected": [["H0", "L", 0], ["H2", "L", 0]],
    }


def add_a(
    records: list[list[object]], *, p: int, coefficient: int, a: int, b: int, u: bool
) -> None:
    missing_l1 = {3 * p, 3 * p + (1 if u else 2)}
    product = a + b - int(u)
    records.append(
        [
            coefficient,
            token(
                p=p,
                kind="A",
                missing_l0={a, b},
                missing_l1=missing_l1,
                product=product,
            ),
        ]
    )


def completion_a(p: int) -> list[list[object]]:
    """Candidate for the two-column 58->59 divided boundary."""
    records: list[list[object]] = []
    for r in range(3):
        add_a(
            records,
            p=p,
            coefficient=sign(r + 1),
            a=p - 3,
            b=p - r,
            u=False,
        )
        for a in range(r + 1, p - 3):
            add_a(
                records,
                p=p,
                coefficient=sign(p + a + r - 1),
                a=a,
                b=p - r,
                u=False,
            )
    for a in range(4, p - 3):
        add_a(
            records,
            p=p,
            coefficient=2 * sign(p + a),
            a=a,
            b=p - 3,
            u=False,
        )

    for coefficient, a, b in (
        (-2, p - 2, p),
        (2, p - 2, p - 1),
        (2, p - 3, p),
        (-2, p - 3, p - 1),
    ):
        add_a(records, p=p, coefficient=coefficient, a=a, b=b, u=True)
    for a in range(4, p - 3):
        add_a(
            records,
            p=p,
            coefficient=2 * sign(p + a),
            a=a,
            b=p - 2,
            u=True,
        )
    for a in range(5, p - 3):
        add_a(
            records,
            p=p,
            coefficient=2 * sign(p + a + 1),
            a=a,
            b=p - 3,
            u=True,
        )
    if len(records) != 6 * p - 30:
        raise AssertionError({"p": p, "completion_a_size": len(records)})
    return records


def add_b(
    records: list[list[object]], *, p: int, coefficient: int, a: int,
    second_low_l1: int, w: int, product: int
) -> None:
    records.append(
        [
            coefficient,
            token(
                p=p,
                kind="B",
                missing_l0={a},
                missing_l1={3 * p, second_low_l1, w},
                product=product,
            ),
        ]
    )


def completion_b(p: int) -> list[list[object]]:
    """Candidate for the two-column 58->62 divided boundary."""
    records: list[list[object]] = []
    for w in range(3 * p + 2, 4 * p - 1):
        add_b(
            records,
            p=p,
            coefficient=2 * sign(w - (3 * p + 2)),
            a=p - 2,
            second_low_l1=3 * p + 1,
            w=w,
            product=w + p - 3,
        )
    for w in range(3 * p + 3, 4 * p - 1):
        add_b(
            records,
            p=p,
            coefficient=-sign(w - (3 * p + 3)),
            a=p - 3,
            second_low_l1=3 * p + 2,
            w=w,
            product=w + p - 3,
        )
        add_b(
            records,
            p=p,
            coefficient=2 * sign(w - (3 * p + 3)),
            a=p - 3,
            second_low_l1=3 * p + 1,
            w=w,
            product=w + p - 4,
        )
    for a in range(1, p - 3):
        first_w = 4 * p - a - 1
        for w in range(first_w, 4 * p - 1):
            add_b(
                records,
                p=p,
                coefficient=-sign(w - first_w),
                a=a,
                second_low_l1=3 * p + 2,
                w=w,
                product=w + a,
            )
    if len(records) != p * (p - 1) // 2 - 5:
        raise AssertionError({"p": p, "completion_b_size": len(records)})
    return records


def canonical(records: list[list[object]]) -> list[list[object]]:
    return sorted(
        records,
        key=lambda value: json.dumps(value, sort_keys=True, separators=(",", ":")),
    )


def candidate(p: int, source: int, target: int) -> list[list[object]]:
    if (source, target) == (58, 59):
        return canonical(completion_a(p))
    if (source, target) == (58, 62):
        return canonical(completion_b(p))
    raise ValueError((source, target))
