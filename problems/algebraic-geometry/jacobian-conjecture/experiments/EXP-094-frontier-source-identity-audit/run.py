"""EXP-094: exact source-identity audit for four frontier configurations.

CPU only. Exact tuple and integer arithmetic. No external dependencies.
"""

from __future__ import annotations

import json
from pathlib import Path


Point = tuple[int, int]


CASES = (
    {"id": "C10", "family": "F9", "a0": (7, 21), "a0_prime": (1, 0)},
    {"id": "C11", "family": "F11", "a0": (7, 21), "a0_prime": (1, 0)},
    {"id": "C19", "family": "F7", "a0": (6, 15), "a0_prime": (1, 0)},
    {"id": "C20", "family": "F8", "a0": (6, 15), "a0_prime": (1, 0)},
)


def matches_heitmann_721(a0: Point, a0_prime: Point) -> bool:
    """Return the exact GGV2 predicate for the discarded A0=(7,21) families."""

    return a0 == (7, 21) and a0_prime == (2, 1)


def matches_ggv_615(b0: Point | None, b1: Point) -> bool:
    """Return the exact GGV2 predicate for the B0=(6,15) family."""

    if b0 != (6, 15) or b1[0] != 6 or b1[1] < 18:
        return False
    offset = b1[1] - 18
    return offset % 6 == 0 and b1[1] % 30 != 0


def matches_known_828_840(b0: Point, b1: Point) -> bool:
    """Return the source predicate that excluded C13 in EXP-082."""

    return b0 == (8, 28) and b1 == (8, 40)


def classify_case(case: dict[str, str | Point]) -> dict[str, object]:
    a0 = case["a0"]
    a0_prime = case["a0_prime"]
    assert isinstance(a0, tuple)
    assert isinstance(a0_prime, tuple)

    # GGHV17 identifies the first complete-chain corner with
    # B1 = m^{-1} en_{1,0}(P) = A0.
    b1 = a0
    heitmann_match = matches_heitmann_721(a0, a0_prime)

    # B0 is not needed to reject the GGV (6,15) predicate: B1 already fails.
    ggv_615_match = matches_ggv_615(None, b1)
    return {
        "id": case["id"],
        "family": case["family"],
        "a0": list(a0),
        "a0_prime": list(a0_prime),
        "b1_equals_a0": list(b1),
        "matches_heitmann_721_predicate": heitmann_match,
        "matches_ggv_615_predicate": ggv_615_match,
        "excluded_by_cited_remark": heitmann_match or ggv_615_match,
    }


def main() -> None:
    controls = {
        "heitmann_positive": matches_heitmann_721((7, 21), (2, 1)),
        "ggv_615_positive": matches_ggv_615((6, 15), (6, 18)),
        "ggv_615_divisibility_negative": matches_ggv_615((6, 15), (6, 30)),
        "c13_positive": matches_known_828_840((8, 28), (8, 40)),
    }
    expected_controls = {
        "heitmann_positive": True,
        "ggv_615_positive": True,
        "ggv_615_divisibility_negative": False,
        "c13_positive": True,
    }
    assert controls == expected_controls, (controls, expected_controls)

    rows = [classify_case(case) for case in CASES]
    assert all(not row["excluded_by_cited_remark"] for row in rows), rows

    result = {
        "experiment": "EXP-094",
        "arithmetic": "exact integer and tuple predicates",
        "controls": controls,
        "rows": rows,
        "decision": (
            "GGV2 Remark 2.32 does not exclude C10, C11, C19, or C20. "
            "The previous candidate classification conflated distinct source identities."
        ),
        "non_claims": [
            "The four configurations are not proved realizable.",
            "The four configurations are not proved to survive other restrictions.",
            "No planar counterexample is constructed.",
            "The (72,108) case is not decided.",
        ],
    }

    output = json.dumps(result, indent=2, sort_keys=True)
    print(output, flush=True)

    artifact = Path(__file__).with_name("artifacts") / "results.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(output + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
