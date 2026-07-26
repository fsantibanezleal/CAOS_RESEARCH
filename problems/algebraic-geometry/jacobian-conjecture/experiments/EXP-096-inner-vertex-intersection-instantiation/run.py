"""EXP-096: exact inner-vertex and approximate-root instantiation."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


Point = tuple[int, int]


def in_inner_vertex_region(
    point: Point, *, a: int, b: int, m: int, n: int
) -> bool:
    x, y = point
    center = Fraction(a, a + b)
    slope = Fraction(n, 1) - center
    slope /= Fraction(m, 1) - center
    lower = slope * (x - center) + center
    upper = Fraction(n, m) * x
    return 0 <= y < Fraction(a - 1, a) * n and lower <= y <= upper


def enumerate_positive_inner_vertices(
    *, a: int, b: int, m: int, n: int
) -> list[Point]:
    candidates: list[Point] = []
    for x in range(1, m + 1):
        for y in range(1, n + 1):
            if in_inner_vertex_region((x, y), a=a, b=b, m=m, n=n):
                candidates.append((x, y))
    return candidates


def major_intersection(
    *, class_count: int, component_factor: int, corner_height: int, k: int, l: int
) -> Fraction:
    roots_per_class = component_factor * corner_height
    return class_count * roots_per_class * Fraction(k, l)


def main() -> None:
    lee_parameters = {"a": 2, "b": 3, "m": 16, "n": 56}
    candidates = enumerate_positive_inner_vertices(**lee_parameters)
    expected_candidates = [
        (1, 3),
        (2, 7),
        (3, 10),
        (4, 14),
        (5, 17),
        (6, 21),
        (7, 24),
    ]
    assert candidates == expected_candidates, candidates

    region_controls = {
        "diagonal_positive": in_inner_vertex_region(
            (2, 7), **lee_parameters
        ),
        "above_diagonal_negative": in_inner_vertex_region(
            (1, 4), **lee_parameters
        ),
        "below_narrow_strip_negative": in_inner_vertex_region(
            (8, 27), **lee_parameters
        ),
        "height_boundary_negative": in_inner_vertex_region(
            (8, 28), **lee_parameters
        ),
    }
    assert region_controls == {
        "diagonal_positive": True,
        "above_diagonal_negative": False,
        "below_narrow_strip_negative": False,
        "height_boundary_negative": False,
    }

    open_intersection = major_intersection(
        class_count=4,
        component_factor=3,
        corner_height=7,
        k=1,
        l=4,
    )
    assert open_intersection == 21

    major_roots = 4 * 3 * 7
    minor_roots = 3 * 8
    total_roots = major_roots + minor_roots
    assert (major_roots, minor_roots, total_roots) == (84, 24, 108)

    # Published Example 3.22, family F1 at j=0:
    # four classes, m=3, final-corner height b=3, k/l=1/4.
    f1_control = major_intersection(
        class_count=4,
        component_factor=3,
        corner_height=3,
        k=1,
        l=4,
    )
    assert f1_control == 9

    diagonal_candidates = [
        point
        for point in candidates
        if Fraction(point[1], point[0]) == Fraction(56, 16)
    ]
    off_diagonal_candidates = [
        point for point in candidates if point not in diagonal_candidates
    ]

    result = {
        "experiment": "EXP-096",
        "arithmetic": "exact integer and Fraction arithmetic",
        "lee_li": {
            "parameters": lee_parameters,
            "region_slope": "139/39",
            "nonzero_inner_vertex_candidates": [
                list(point) for point in candidates
            ],
            "candidate_count": len(candidates),
            "diagonal_candidates": [
                list(point) for point in diagonal_candidates
            ],
            "off_diagonal_candidates": [
                list(point) for point in off_diagonal_candidates
            ],
            "stronger_diagonal_corollary_applies": False,
            "ratio_b_over_a": "3/2",
            "diagonal_corollary_threshold": "19",
            "controls": region_controls,
        },
        "approximate_roots": {
            "major_class_count": 4,
            "roots_per_major_class": 21,
            "major_root_count": major_roots,
            "minor_root_count": minor_roots,
            "total_root_count": total_roots,
            "lambda_q_per_class": "1/4",
            "intersection_number_I_P_Q": int(open_intersection),
            "f1_smallest_member_control": int(f1_control),
        },
        "decision": (
            "Every nonzero Lee-Li inner vertex for the original degree-72 "
            "component lies in a seven-point set, and the open GGHV chain has "
            "exact resultant intersection number I(P,Q)=21."
        ),
        "uses": [
            "Reject any reconstructed original pair whose inner vertex is outside the seven-point set.",
            "Reject any reconstructed original pair whose resultant has x-degree other than 21.",
            "Use the 84 major plus 24 minor root partition as a consistency gate.",
        ],
        "non_claims": [
            "The seven inner-vertex candidates are not proved realizable.",
            "The open chain is not excluded.",
            "No planar counterexample is constructed.",
            "The planar degree floor is not raised.",
        ],
    }

    output = json.dumps(result, indent=2, sort_keys=True)
    print(output, flush=True)

    artifact = Path(__file__).with_name("artifacts") / "results.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(output + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
