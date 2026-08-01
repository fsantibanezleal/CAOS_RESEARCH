"""Characteristic-zero K[Y] certification for the EXP-130 selected basis."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import Poly, QQ, expand, invert, resultant, sympify, symbols


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
E125_PATH = ROOT / "EXP-125-factor-curve-recursion" / "run.py"
CRT_PATH = HERE / "crt_worker.py"
E124_ARTIFACT = ROOT / "EXP-124-rational-graph-alternative-chart" / "artifacts" / "results.json"
E125_ARTIFACT = ROOT / "EXP-125-factor-curve-recursion" / "artifacts" / "results.json"
E127_ARTIFACT = ROOT / "EXP-127-f7-divisor-norm" / "artifacts" / "results.json"
E129_ARTIFACT = ROOT / "EXP-129-f7-crt-minor-atlas" / "artifacts" / "results.json"
CRT_ARTIFACT = HERE / "artifacts" / "crt-worker.json"
SELECTION = HERE / "artifacts" / "selection.json"
EXACT_ARTIFACT = HERE / "artifacts" / "exact-worker.json"
ARTIFACT = HERE / "artifacts" / "certificate.json"
EXPECTED_CRT = "7189D6C9DBD6CF3E006B937A9DE1547A43155985BEF6716FE544F58A0EE65CB2"
EXPECTED_SELECTION = "77FFCD863B06141C8E95108D130869227D4D7532B4470B58ABB5A9CED959C418"
EXPECTED_EXACT = "CF305B272DFB26A223F0BDFDD93E879B04488B5FC2981418582ACC5DAAD9AA17"

spec = importlib.util.spec_from_file_location("exp125_exp130_cert", E125_PATH)
exp125 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp125)

crt_spec = importlib.util.spec_from_file_location("crt_exp130_cert", CRT_PATH)
crtlib = importlib.util.module_from_spec(crt_spec)
assert crt_spec.loader is not None
crt_spec.loader.exec_module(crtlib)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def persist(payload: dict[str, object]) -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def ky_trim(polynomial, modulus):
    return {
        degree: coefficient.rem(modulus)
        for degree, coefficient in polynomial.items()
        if not coefficient.rem(modulus).is_zero
    }


def ky_add(left, right, modulus, b):
    result = dict(left)
    for degree, coefficient in right.items():
        result[degree] = result.get(degree, Poly(0, b, domain=QQ)) + coefficient
    return ky_trim(result, modulus)


def ky_sub(left, right, modulus, b):
    return ky_add(
        left,
        {degree: -coefficient for degree, coefficient in right.items()},
        modulus,
        b,
    )


def ky_mul(left, right, modulus, b):
    result = {}
    for left_degree, left_coefficient in left.items():
        for right_degree, right_coefficient in right.items():
            degree = left_degree + right_degree
            result[degree] = result.get(degree, Poly(0, b, domain=QQ)) + (
                left_coefficient * right_coefficient
            ).rem(modulus)
    return ky_trim(result, modulus)


def ky_scale(polynomial, scalar, modulus):
    return ky_trim(
        {
            degree: (coefficient * scalar).rem(modulus)
            for degree, coefficient in polynomial.items()
        },
        modulus,
    )


def ky_divmod(numerator, denominator, modulus, b):
    if not denominator:
        raise ZeroDivisionError("zero polynomial in K[Y]")
    quotient = {}
    remainder = dict(numerator)
    denominator_degree = max(denominator)
    denominator_lead_inverse = Poly(
        invert(
            denominator[denominator_degree].as_expr(), modulus.as_expr()
        ),
        b,
        domain=QQ,
    ).rem(modulus)
    while remainder and max(remainder) >= denominator_degree:
        remainder_degree = max(remainder)
        shift = remainder_degree - denominator_degree
        coefficient = (
            remainder[remainder_degree] * denominator_lead_inverse
        ).rem(modulus)
        term = {shift: coefficient}
        quotient = ky_add(quotient, term, modulus, b)
        remainder = ky_sub(
            remainder, ky_mul(term, denominator, modulus, b), modulus, b
        )
    return quotient, remainder


def ky_xgcd(left, right, modulus, b):
    old_r, current_r = dict(left), dict(right)
    old_s, current_s = {0: Poly(1, b, domain=QQ)}, {}
    old_t, current_t = {}, {0: Poly(1, b, domain=QQ)}
    while current_r:
        quotient, remainder = ky_divmod(old_r, current_r, modulus, b)
        old_r, current_r = current_r, remainder
        old_s, current_s = current_s, ky_sub(
            old_s, ky_mul(quotient, current_s, modulus, b), modulus, b
        )
        old_t, current_t = current_t, ky_sub(
            old_t, ky_mul(quotient, current_t, modulus, b), modulus, b
        )
    if not old_r:
        return {}, {}, {}
    leading = old_r[max(old_r)]
    inverse = Poly(
        invert(leading.as_expr(), modulus.as_expr()), b, domain=QQ
    ).rem(modulus)
    return (
        ky_scale(old_r, inverse, modulus),
        ky_scale(old_s, inverse, modulus),
        ky_scale(old_t, inverse, modulus),
    )


def ky_expression(polynomial, y):
    return expand(
        sum(coefficient.as_expr() * y**degree for degree, coefficient in polynomial.items())
    )


def section_record(name, expression, x_class, modulus, x, b, y):
    coefficients = crtlib.section_y_coefficients(
        expression, x_class, modulus, x, b, y
    )
    return {
        "name": name,
        "coefficients": ky_trim(coefficients, modulus),
    }


def main() -> None:
    started = time.time()
    require(sha256(CRT_ARTIFACT) == EXPECTED_CRT, "CRT artifact hash matches")
    require(sha256(SELECTION) == EXPECTED_SELECTION, "selection artifact hash matches")
    require(sha256(EXACT_ARTIFACT) == EXPECTED_EXACT, "exact worker artifact hash matches")
    crt = json.loads(CRT_ARTIFACT.read_text(encoding="utf-8"))
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    exact = json.loads(EXACT_ARTIFACT.read_text(encoding="utf-8"))
    e124 = json.loads(E124_ARTIFACT.read_text(encoding="utf-8"))
    e125 = json.loads(E125_ARTIFACT.read_text(encoding="utf-8"))
    e127 = json.loads(E127_ARTIFACT.read_text(encoding="utf-8"))
    e129 = json.loads(E129_ARTIFACT.read_text(encoding="utf-8"))
    a, b, c, x, y = symbols("A B C X Y")
    locals_map = {"A": a, "B": b, "C": c, "X": x, "Y": y}
    exact_record = exact["atlas_records"][0]
    expression = sympify(exact_record["determinant_ratio"], locals=locals_map)
    valuation, invariant = exp125.exp124.invariant_reduce(
        expression, a, b, c, x, y
    )
    invariant_y_degree = int(Poly(invariant, y, domain="QQ[X,B]").degree())
    require(invariant_y_degree == 2, "new exact section is quadratic in Y")

    base, directions = exp125.exp124.build_full_system()
    rows = selection["selected_atlas"][0]["rows"]
    selected_base = base.extract(rows, range(125))
    selected_directions = {
        direction: matrix.extract(rows, range(125))
        for direction, matrix in directions.items()
    }
    anchor_det = sympify(exact_record["anchor"]["determinant"])
    anchor_point = exact_record["anchor"]["point"]
    require(
        expression.subs({a: anchor_point[0], b: anchor_point[1], c: anchor_point[2]})
        == 1,
        "reconstructed expression is normalized at its exact anchor",
    )
    control_point = (1, 0, 1)
    direct = (
        selected_base
        + control_point[0] * selected_directions[(0, 1)]
        + control_point[1] * selected_directions[(0, 5)]
        + control_point[2] * selected_directions[exp125.exp124.TARGET]
    ).det(method="domain-ge") / anchor_det
    predicted = expression.subs(
        {a: control_point[0], b: control_point[1], c: control_point[2]}
    )
    require(direct == predicted, "independent direct determinant control agrees")

    candidates = [
        (
            "EXP-124-N",
            sympify(e124["invariant_determinant_X_B_Y"], locals=locals_map),
        ),
        (
            "EXP-125-h36",
            sympify(e125["invariant_determinant_X_B_Y"], locals=locals_map),
        ),
        (
            "EXP-127-h7",
            sympify(e127["invariant_determinant_X_B_Y"], locals=locals_map),
        ),
    ]
    candidates.extend(
        (
            f"EXP-129-atlas-{record['atlas_index']}",
            sympify(record["invariant_determinant_X_B_Y"], locals=locals_map),
        )
        for record in e129["exact_atlas"]
    )
    candidates.append(("EXP-130-new", invariant))

    block_certificates = []
    for block in crt["blocks"]:
        degree = int(block["degree"])
        if degree not in (3, 6):
            continue
        modulus = Poly(
            sympify(block["B_factor"], locals={"B": b}), b, domain=QQ
        ).monic()
        x_class = Poly(
            sympify(block["X_class_mod_B_factor"], locals={"B": b}),
            b,
            domain=QQ,
        )
        records = [
            section_record(name, item, x_class, modulus, x, b, y)
            for name, item in candidates
        ]
        new_record = next(item for item in records if item["name"] == "EXP-130-new")
        require(bool(new_record["coefficients"]), f"new exact section is nonzero on degree-{degree} block")
        certificate = None
        for old_record in records:
            if old_record["name"] == "EXP-130-new":
                continue
            gcd_record, bezout_new, bezout_old = ky_xgcd(
                new_record["coefficients"],
                old_record["coefficients"],
                modulus,
                b,
            )
            if not (
                set(gcd_record) == {0}
                and gcd_record[0] == Poly(1, b, domain=QQ)
            ):
                continue
            bezout_check = ky_add(
                ky_mul(
                    bezout_new,
                    new_record["coefficients"],
                    modulus,
                    b,
                ),
                ky_mul(
                    bezout_old,
                    old_record["coefficients"],
                    modulus,
                    b,
                ),
                modulus,
                b,
            )
            require(
                bezout_check == {0: Poly(1, b, domain=QQ)},
                f"degree-{degree} K[Y] Bezout identity verifies",
            )
            y_resultant = Poly(
                resultant(
                    ky_expression(new_record["coefficients"], y),
                    ky_expression(old_record["coefficients"], y),
                    y,
                ),
                b,
                domain=QQ,
            ).rem(modulus)
            require(
                y_resultant.gcd(modulus).degree() == 0,
                f"degree-{degree} independent Y-resultant is a unit",
            )
            inverse = crtlib.reduce_b(
                invert(y_resultant.as_expr(), modulus.as_expr()), modulus, b
            )
            norm_matrix = crtlib.multiplication_matrix(
                y_resultant, modulus, b
            ).det(method="domain-ge")
            norm_resultant = resultant(
                modulus.as_expr(), y_resultant.as_expr(), b
            )
            require(
                norm_matrix == norm_resultant and norm_matrix != 0,
                f"degree-{degree} selected Y-resultant norm verifies independently",
            )
            certificate = {
                "type": "quadratic-affine-pair",
                "sections": ["EXP-130-new", old_record["name"]],
                "K_Y_bezout_new": str(ky_expression(bezout_new, y)),
                "K_Y_bezout_old": str(ky_expression(bezout_old, y)),
                "Y_resultant": str(y_resultant.as_expr()),
                "Y_resultant_inverse": str(inverse.as_expr()),
                "norm": str(norm_matrix),
            }
            break
        common_gcd = records[0]["coefficients"]
        for record in records[1:]:
            common_gcd, _, _ = ky_xgcd(
                common_gcd, record["coefficients"], modulus, b
            )
        covered = certificate is not None
        if covered:
            require(
                set(common_gcd) == {0}
                and common_gcd[0] == Poly(1, b, domain=QQ),
                f"degree-{degree} complete known-section gcd is one",
            )
        else:
            require(
                bool(common_gcd) and max(common_gcd) > 0,
                f"degree-{degree} uncovered section gcd has positive Y-degree",
            )
            certificate = {
                "type": "uncovered-common-factor",
                "common_gcd_K_Y": str(ky_expression(common_gcd, y)),
                "common_gcd_Y_degree": max(common_gcd),
            }
        block_certificates.append(
            {"degree": degree, "covered": covered, "certificate": certificate}
        )

    all_new_blocks_covered = all(item["covered"] for item in block_certificates)
    payload = {
        "experiment": "EXP-130-certificate",
        "source_hashes": {
            "crt": EXPECTED_CRT,
            "selection": EXPECTED_SELECTION,
            "exact_worker": EXPECTED_EXACT,
        },
        "new_section": {
            "rows": rows,
            "anchor": exact_record["anchor"],
            "cyclic_component_sizes": exact_record["cyclic_component_sizes"],
            "A_valuation": valuation,
            "invariant_X_B_Y": str(expand(invariant)),
            "Y_degree": invariant_y_degree,
            "direct_control": {
                "point": list(control_point),
                "ratio": str(direct),
            },
        },
        "new_block_certificates": block_certificates,
        "previous_block_certificates": crt["principal_open_algebra"][
            "block_cover_certificates_in_KY"
        ],
        "complete_principal_open_base_locus_covered": all_new_blocks_covered,
        "coordinate_boundary": crt["coordinate_boundary"],
        "decision": (
            "complete_principal_open_base_locus_closed"
            if all_new_blocks_covered
            else "target_common_KY_factors_with_new_rows"
        ),
        "elapsed_seconds": time.time() - started,
        "scope": (
            "Exact closure of V(R,S) intersect D(X) uniformly in C. The X=B=0 "
            "coordinate component remains part of the separate A=0 boundary. "
            "No full-core, (72,108), degree-floor, or JC(2) conclusion follows."
        ),
    }
    persist(payload)
    print(f"[PASS] certificate SHA256 {sha256(ARTIFACT)}", flush=True)
    if all_new_blocks_covered:
        print("RESULT: COMPLETE PRINCIPAL-OPEN BASE LOCUS CLOSED", flush=True)
    else:
        pending = [
            str(item["degree"])
            for item in block_certificates
            if not item["covered"]
        ]
        print("RESULT: TARGET COMMON K[Y] FACTORS ON DEGREES " + ",".join(pending), flush=True)


if __name__ == "__main__":
    main()
