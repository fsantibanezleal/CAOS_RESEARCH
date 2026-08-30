"""Symbolic and cross-artifact certificate for EXP-036.

This route proves that the cubic mapping-cone summand is absent at every
declared family target and checks the finite rank claims against the canonical
and independent artifacts.  It deliberately preserves two failed numerical
interpolations so that finite data are not promoted to an infinite theorem.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import sympy


HERE = Path(__file__).resolve().parent
ARTIFACTS = HERE / "artifacts"
OUTPUT = ARTIFACTS / "symbolic-certificate.json"
CANONICAL_FILES = (
    ARTIFACTS / "results-p6.json",
    ARTIFACTS / "target-t2-p7-p8.json",
    ARTIFACTS / "target-t2-p9.json",
)
AUDIT_FILES = (
    ARTIFACTS / "audit-p6.json",
    ARTIFACTS / "audit-t2-p7-p8.json",
)
AUDIT_STOP_FILE = ARTIFACTS / "audit-t2-p9-resource-stop.json"
LOCALIZATION_FILE = ARTIFACTS / "localization-p4.json"


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def main() -> int:
    p, t = sympy.symbols("p t", integer=True)
    exterior_size = 2 * p - t - 2
    minimum_high_sum = sympy.expand(
        exterior_size * 6 * p + exterior_size * (exterior_size - 1) / 2
    )
    tau = 4 * p**2 + 6 * p - t * (t - 1) / 2
    shifted_offset = tau - 3 * p
    gap = sympy.expand(minimum_high_sum - shifted_offset)
    expected_gap = 10 * p**2 - 8 * p * t - 20 * p + t**2 + 2 * t + 3
    if sympy.simplify(gap - expected_gap) != 0:
        raise AssertionError("cubic gap identity failed")
    endpoint_gap = sympy.factor(gap.subs(t, p - 2))
    if sympy.simplify(endpoint_gap - 3 * (p - 1) ** 2) != 0:
        raise AssertionError("cubic endpoint factorization failed")
    forward_difference = sympy.expand(gap.subs(t, t + 1) - gap)
    if sympy.simplify(forward_difference - (2 * t - 8 * p + 3)) != 0:
        raise AssertionError("cubic monotonicity identity failed")

    canonical_artifacts = [load(path) for path in CANONICAL_FILES]
    rows = {
        (row["p"], row["t"]): row
        for artifact in canonical_artifacts
        for row in artifact["rows"]
    }
    expected_cells = {
        (4, 2),
        (5, 2),
        (5, 3),
        (6, 2),
        (6, 3),
        (6, 4),
        (7, 2),
        (8, 2),
        (9, 2),
    }
    if set(rows) != expected_cells:
        raise AssertionError({"unexpected_cells": sorted(rows)})

    finite_cubic_checks = {}
    for cell, row in sorted(rows.items()):
        p_value, t_value = cell
        size_value = 2 * p_value - t_value - 2
        literal_minimum = sum(range(6 * p_value, 6 * p_value + size_value))
        literal_shifted = row["total_offset"] - 3 * p_value
        literal_gap = literal_minimum - literal_shifted
        symbolic_gap = int(gap.subs({p: p_value, t: t_value}))
        finite_cubic_checks[f"{p_value}:{t_value}"] = {
            "source_exterior_size": size_value,
            "minimum_high_sum": literal_minimum,
            "shifted_target_offset": literal_shifted,
            "positive_gap": literal_gap,
            "checks": {
                "literal_matches_symbolic": literal_gap == symbolic_gap,
                "source_diagonal_absent": literal_gap > 0,
            },
        }
        if not all(finite_cubic_checks[f"{p_value}:{t_value}"]["checks"].values()):
            raise AssertionError({"cubic_finite_failure": cell})

    odd_fields_agree = all(
        row["field_rows"]["3"] == row["field_rows"]["1000003"]
        for row in rows.values()
    )
    if not odd_fields_agree:
        raise AssertionError("odd canonical fields disagree")

    audits = [load(path) for path in AUDIT_FILES]
    for audit in audits:
        if audit["status"] not in {"PASS_INDEPENDENT", "PASS_INDEPENDENT_P6"}:
            raise AssertionError("independent audit is not passing")
        if not all(
            all(comparison.values()) for comparison in audit["comparisons"].values()
        ):
            raise AssertionError("independent audit comparison failed")
        if not all(
            row["field_rows"]["3"] == row["field_rows"]["5"]
            for row in audit["rows"]
        ):
            raise AssertionError("independent odd-field control failed")
    audited_cells = sorted(
        (row["p"], row["t"])
        for audit in audits
        for row in audit["rows"]
    )
    expected_audited_cells = sorted(expected_cells - {(9, 2)})
    if audited_cells != expected_audited_cells:
        raise AssertionError({"unexpected_audited_cells": audited_cells})
    audit_stop = load(AUDIT_STOP_FILE)
    if (
        audit_stop["status"] != "INCONCLUSIVE_RESOURCE_BUDGET"
        or audit_stop["mathematical_evidence"] is not False
    ):
        raise AssertionError("p9 audit stop is not correctly scoped")

    localization = load(LOCALIZATION_FILE)["rows"][0]["unit_residual"]
    localization_checks = {
        "unit_pivots_74": localization["unit_pivots"] == 74,
        "residual_shape_5_by_45": (
            localization["residual_rows"], localization["residual_columns"]
        )
        == (5, 45),
        "two_nonzero_entries": localization["residual_nonzeros"] == 2,
        "entry_gcd_two": localization["residual_entry_gcd"] == 2,
        "one_factor_two": localization["residual_smith_profile"][
            "torsion_invariant_factors"
        ]
        == {"2": 1},
        "seven_low_variables_in_this_reduction": len(
            localization["transform_certificate"]["low_variable_support"]
        )
        == 7,
    }
    if not all(localization_checks.values()):
        raise AssertionError({"localization_failure": localization_checks})

    t2_rows = [rows[(p_value, 2)] for p_value in range(5, 10)]
    t2_kernel_independent = all(
        row["field_rows"]["2"]["kernel_cokernel_dimension"]
        == row["field_rows"]["3"]["kernel_cokernel_dimension"]
        for row in t2_rows
    )
    t2_a_gaps = [
        row["field_rows"]["2"]["surviving_a_dimension"]
        - row["field_rows"]["3"]["surviving_a_dimension"]
        for row in t2_rows
    ]
    if not t2_kernel_independent or t2_a_gaps != [4, 9, 18, 31, 49]:
        raise AssertionError(
            {
                "t2_kernel_independent": t2_kernel_independent,
                "t2_a_gaps": t2_a_gaps,
            }
        )

    square_prediction_at_p7 = (7 - 3) ** 2
    quadratic_prediction_at_p9 = 2 * 9**2 - 17 * 9 + 39
    interpolation_controls = {
        "square_formula": {
            "fit_cells": {"4": 1, "5": 4, "6": 9},
            "prediction_p7": square_prediction_at_p7,
            "actual_p7": rows[(7, 2)]["field_rows"]["2"]["surviving_a_dimension"]
            - rows[(7, 2)]["field_rows"]["3"]["surviving_a_dimension"],
            "refuted": square_prediction_at_p7 != t2_a_gaps[2],
        },
        "quadratic_formula_2p2_minus_17p_plus_39": {
            "fit_cells": {str(p_value): t2_a_gaps[p_value - 5] for p_value in range(5, 9)},
            "prediction_p9": quadratic_prediction_at_p9,
            "actual_p9": t2_a_gaps[-1],
            "refuted": quadratic_prediction_at_p9 != t2_a_gaps[-1],
        },
    }
    if not all(control["refuted"] for control in interpolation_controls.values()):
        raise AssertionError("interpolation negative controls did not fail")

    result = {
        "experiment": "EXP-036",
        "status": "PASS_SYMBOLIC_AND_CROSS_ARTIFACT",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_file_sha256": {
            path.name: file_hash(path)
            for path in (
                *CANONICAL_FILES,
                *AUDIT_FILES,
                AUDIT_STOP_FILE,
                LOCALIZATION_FILE,
            )
        },
        "cubic_cone_absence": {
            "domain": "integers p>=4 and 2<=t<=p-2",
            "source_exterior_size": str(exterior_size),
            "minimum_high_sum": str(minimum_high_sum),
            "shifted_target_offset": str(shifted_offset),
            "gap": str(gap),
            "forward_difference_in_t": str(forward_difference),
            "endpoint_minimum": str(endpoint_gap),
            "proof": (
                "The gap decreases with t on the declared interval, so its minimum is "
                "3*(p-1)^2 at t=p-2, which is positive for p>=4."
            ),
            "conclusion": "the shifted D_p(-3) diagonal is zero, hence C_p equals A_p at every declared target",
            "finite_checks": finite_cubic_checks,
        },
        "finite_rank_checks": {
            "cells": [list(cell) for cell in sorted(rows)],
            "canonical_odd_fields_agree": odd_fields_agree,
            "independent_cells_through_p8_pass": [
                list(cell) for cell in audited_cells
            ],
            "independent_p9_status": audit_stop["status"],
            "t2_p5_through_p9_kernel_characteristic_independent": t2_kernel_independent,
            "t2_p5_through_p9_a_and_c_gaps": t2_a_gaps,
        },
        "p4_integral_localization": {
            "checks": localization_checks,
            "transform_certificate_hash": localization["transform_certificate_hash"],
            "low_variable_support": localization["transform_certificate"][
                "low_variable_support"
            ],
            "recognition_scope": (
                "this deterministic reduction uses seven low variables; the proposed "
                "six-variable RP2 recognition is not established"
            ),
        },
        "interpolation_negative_controls": interpolation_controls,
        "scope": (
            "All-parameter cubic absence is proved. Characteristic dependence is exact "
            "only for the nine computed cells; no infinite torsion formula is claimed."
        ),
    }
    result["artifact_sha256"] = digest(result)
    write_json_atomic(OUTPUT, result)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
