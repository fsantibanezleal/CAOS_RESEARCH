"""EXP-095: exact Newton-resolution applicability and candidate crosswalk.

CPU only. Exact integer and Fraction arithmetic. No external dependencies.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import TypeAlias


Scalar: TypeAlias = int | Fraction
Point: TypeAlias = tuple[Scalar, Scalar]


def scale(point: Point, factor: int) -> Point:
    return (factor * point[0], factor * point[1])


def serial_point(point: Point) -> list[int | str]:
    values: list[int | str] = []
    for coordinate in point:
        if isinstance(coordinate, Fraction) and coordinate.denominator != 1:
            values.append(f"{coordinate.numerator}/{coordinate.denominator}")
        else:
            values.append(int(coordinate))
    return values


def source_hypotheses_hold(*, ring: str, bracket: str) -> bool:
    return ring == "C[x,y]" and bracket == "1"


def candidate_signature(
    *,
    degree: int,
    a0: Point,
    a0_prime: Point,
    a1: Point,
    component_factor: int,
) -> dict[str, object]:
    return {
        "degree": degree,
        "v0": scale(a0, component_factor),
        "v1_prime": scale(a0_prime, component_factor),
        "v1": scale(a1, component_factor),
    }


def signature_matches(left: dict[str, object], right: dict[str, object]) -> bool:
    return left == right


def serial_signature(signature: dict[str, object]) -> dict[str, object]:
    return {
        "degree": signature["degree"],
        "v0": serial_point(signature["v0"]),  # type: ignore[arg-type]
        "v1_prime": serial_point(signature["v1_prime"]),  # type: ignore[arg-type]
        "v1": serial_point(signature["v1"]),  # type: ignore[arg-type]
    }


def main() -> None:
    original_applicable = source_hypotheses_hold(ring="C[x,y]", bracket="1")
    final_reduced_applicable = source_hypotheses_hold(
        ring="C[x,x^-1,y]", bracket="x^2"
    )
    assert original_applicable
    assert not final_reduced_applicable

    gghv_open = candidate_signature(
        degree=72,
        a0=(8, 28),
        a0_prime=(1, 0),
        a1=(Fraction(11, 4), 7),
        component_factor=2,
    )
    mlt_d72_first = {
        "degree": 72,
        "v0": (16, 56),
        "v1_prime": (2, 0),
        "v1": (Fraction(11, 2), 14),
    }
    mlt_d72_second = {
        "degree": 72,
        "v0": (16, 56),
        "v1_prime": (2, 0),
        "v1": (5, 12),
    }

    first_match = signature_matches(gghv_open, mlt_d72_first)
    second_match = signature_matches(gghv_open, mlt_d72_second)
    assert first_match
    assert not second_match

    endpoint_negative = candidate_signature(
        degree=72,
        a0=(8, 28),
        a0_prime=(2, 0),
        a1=(Fraction(11, 4), 7),
        component_factor=2,
    )
    final_corner_negative = candidate_signature(
        degree=72,
        a0=(8, 28),
        a0_prime=(1, 0),
        a1=(Fraction(5, 2), 6),
        component_factor=2,
    )
    assert not signature_matches(endpoint_negative, mlt_d72_first)
    assert not signature_matches(final_corner_negative, mlt_d72_first)
    assert signature_matches(final_corner_negative, mlt_d72_second)

    result = {
        "experiment": "EXP-095",
        "arithmetic": "exact integer and Fraction identities",
        "applicability": {
            "original_polynomial_keller_pair": original_applicable,
            "final_gghv_laurent_pair": final_reduced_applicable,
            "direct_failure_reasons": [
                "ambient ring is C[x,x^-1,y], not C[x,y]",
                "bracket is x^2, not 1",
            ],
        },
        "gghv_open_signature": serial_signature(gghv_open),
        "mlt_d72_first_signature": serial_signature(mlt_d72_first),
        "mlt_d72_second_signature": serial_signature(mlt_d72_second),
        "matches": {
            "first_d72_branch": first_match,
            "second_d72_branch": second_match,
        },
        "controls": {
            "polynomial_bracket_one_positive": original_applicable,
            "laurent_bracket_x2_negative": final_reduced_applicable,
            "altered_endpoint_matches_first": signature_matches(
                endpoint_negative, mlt_d72_first
            ),
            "altered_final_corner_matches_first": signature_matches(
                final_corner_negative, mlt_d72_first
            ),
            "altered_final_corner_matches_second": signature_matches(
                final_corner_negative, mlt_d72_second
            ),
        },
        "decision": (
            "The Newton-resolution hypotheses apply to the original degree-72 "
            "Keller component, not directly to the final Laurent pair. Its exact "
            "corner signature is the first retained MLT D=72 branch, so the "
            "published list reproduces rather than excludes the GGHV open case."
        ),
        "non_claims": [
            "The retained branch is not proved realizable.",
            "No planar counterexample is constructed.",
            "The (72,108) case is not excluded.",
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
