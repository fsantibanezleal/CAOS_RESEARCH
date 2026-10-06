from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = (
    ROOT
    / "problems"
    / "commutative-algebra"
    / "huneke-wiegand"
    / "experiments"
    / "EXP-064-exact-carrier-two-primary"
)


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, EXPERIMENT / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RUN = load("hw_exp064", "run.py")
AUDIT = load("hw_exp064_audit", "audit.py")


def payload() -> dict[str, object]:
    return json.loads((EXPERIMENT / "artifacts" / "results.json").read_text(encoding="utf-8"))


def test_diagonal_exponent_control_separates_two_from_four() -> None:
    assert AUDIT.diagonal_first_bockstein(2) == 1
    assert AUDIT.diagonal_first_bockstein(4) == 0


def test_carrier_types_and_minimal_coverage_are_frozen() -> None:
    result = payload()
    unsigned = dict(result)
    artifact_hash = unsigned.pop("artifact_hash")
    assert RUN.digest(unsigned) == artifact_hash
    expected = {
        8: {56: 0, 58: 1, 59: 3, 62: 3},
        9: {56: 0, 58: 2, 59: 4, 62: 4},
        10: {56: 0, 58: 3, 59: 5, 62: 5},
        11: {56: 1, 58: 5, 59: 7, 62: 7},
    }
    for row in result["rows"]:
        p = row["p"]
        for certificate in row["certificates"]:
            mask = certificate["mask"]
            beta = expected[p][mask]
            assert certificate["complete_two_primary_type"] == f"(Z/2)^{beta}"
            product = int(certificate["prime_product_hex"], 16)
            norm = certificate["maximum_squared_column_norm"]
            rank = certificate["target_rational_rank"]
            assert AUDIT.covered(product, norm, rank)
            assert not AUDIT.covered(
                product // int(certificate["prime_tests"][-1]["prime"]), norm, rank
            )


def test_endpoint_vanishing_and_complete_generators() -> None:
    for row in payload()["rows"]:
        p = row["p"]
        consequences = {item["mask"]: item for item in row["triangle_consequences"]}
        assert consequences[58]["integrally_zero_triangles"] == [
            [0, 1, p - 3],
            [0, 2, p - 4],
        ]
        assert consequences[59]["integrally_zero_triangles"] == []
        assert consequences[62]["integrally_zero_triangles"] == []
        assert consequences[58]["generator_count"] == RUN.EXPECTED_BETA[p][58]
