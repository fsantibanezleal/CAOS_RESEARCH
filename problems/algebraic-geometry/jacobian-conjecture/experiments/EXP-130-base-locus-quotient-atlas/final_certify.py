"""Final exact closure certificate for the EXP-130 principal-open base locus."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

from sympy import Poly, QQ, invert, resultant, sympify, symbols


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CERTIFY_PATH = HERE / "certify.py"
E125_PATH = ROOT / "EXP-125-factor-curve-recursion" / "run.py"
CRT_ARTIFACT = HERE / "artifacts" / "crt-worker.json"
PRIOR_CERTIFICATE = HERE / "artifacts" / "certificate.json"
STRUCTURAL_SELECTION = HERE / "artifacts" / "structural-selection.json"
STRUCTURAL_EXACT = HERE / "artifacts" / "structural-exact-worker.json"
ARTIFACT = HERE / "artifacts" / "final-certificate.json"
EXPECTED_CRT = "7189D6C9DBD6CF3E006B937A9DE1547A43155985BEF6716FE544F58A0EE65CB2"
EXPECTED_PRIOR = "645CB57F9AB6BFA7120C5163388930322CE128E6FB324D22DD5B0364F0CEF39D"
EXPECTED_STRUCTURAL_SELECTION = "7EA09CB31314797859CF2EE8A02C984C2066FAD809DAE096F1242F60B24C347E"
EXPECTED_STRUCTURAL_EXACT = "0C6DF9F97BC10F8462C37122B5C47F108A8F8CAE81EBAB80D07CF5304E487961"

cert_spec = importlib.util.spec_from_file_location("cert_exp130_final", CERTIFY_PATH)
cert = importlib.util.module_from_spec(cert_spec)
assert cert_spec.loader is not None
cert_spec.loader.exec_module(cert)

exp_spec = importlib.util.spec_from_file_location("exp125_exp130_final", E125_PATH)
exp125 = importlib.util.module_from_spec(exp_spec)
assert exp_spec.loader is not None
exp_spec.loader.exec_module(exp125)


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


def main() -> None:
    require(sha256(CRT_ARTIFACT) == EXPECTED_CRT, "CRT artifact hash matches")
    require(sha256(PRIOR_CERTIFICATE) == EXPECTED_PRIOR, "prior section-gcd certificate hash matches")
    require(
        sha256(STRUCTURAL_SELECTION) == EXPECTED_STRUCTURAL_SELECTION,
        "structural selection hash matches",
    )
    require(
        sha256(STRUCTURAL_EXACT) == EXPECTED_STRUCTURAL_EXACT,
        "structural exact artifact hash matches",
    )
    crt = json.loads(CRT_ARTIFACT.read_text(encoding="utf-8"))
    prior = json.loads(PRIOR_CERTIFICATE.read_text(encoding="utf-8"))
    structural = json.loads(STRUCTURAL_SELECTION.read_text(encoding="utf-8"))
    exact = json.loads(STRUCTURAL_EXACT.read_text(encoding="utf-8"))
    a, b, c, x, y = symbols("A B C X Y")
    expression = sympify(
        exact["determinant_ratio"], locals={"A": a, "B": b, "C": c}
    )
    valuation, invariant = exp125.exp124.invariant_reduce(
        expression, a, b, c, x, y
    )
    y_degree = int(Poly(invariant, y, domain="QQ[X,B]").degree())
    require(y_degree <= 2, "structural section has Y-degree at most two")
    require(
        exact["rows"] == structural["selected"]["rows"],
        "exact rows match the minimum-SCC structural selection",
    )

    base, directions = exp125.exp124.build_full_system()
    rows = exact["rows"]
    selected_base = base.extract(rows, range(125))
    selected_directions = {
        direction: matrix.extract(rows, range(125))
        for direction, matrix in directions.items()
    }
    anchor_det = sympify(exact["anchor"]["determinant"])
    anchor_point = exact["anchor"]["point"]
    require(
        expression.subs({a: anchor_point[0], b: anchor_point[1], c: anchor_point[2]})
        == 1,
        "structural expression is normalized at its anchor",
    )
    control = (1, 0, 1)
    direct = (
        selected_base
        + control[0] * selected_directions[(0, 1)]
        + control[1] * selected_directions[(0, 5)]
        + control[2] * selected_directions[exp125.exp124.TARGET]
    ).det(method="domain-ge") / anchor_det
    require(
        direct
        == expression.subs({a: control[0], b: control[1], c: control[2]}),
        "structural section passes an independent direct determinant control",
    )

    block_by_degree = {int(item["degree"]): item for item in crt["blocks"]}
    final_blocks = []
    for prior_block in prior["new_block_certificates"]:
        degree = int(prior_block["degree"])
        source = block_by_degree[degree]
        modulus = Poly(
            sympify(source["B_factor"], locals={"B": b}), b, domain=QQ
        ).monic()
        x_class = Poly(
            sympify(source["X_class_mod_B_factor"], locals={"B": b}),
            b,
            domain=QQ,
        )
        common_expression = sympify(
            prior_block["certificate"]["common_gcd_K_Y"],
            locals={"B": b, "Y": y},
        )
        common_coefficients = {
            y_power: Poly(coefficient, b, domain=QQ).rem(modulus)
            for (y_power,), coefficient in Poly(
                common_expression, y, domain="QQ[B]"
            ).terms()
        }
        new_coefficients = cert.crtlib.section_y_coefficients(
            invariant, x_class, modulus, x, b, y
        )
        gcd_record, bezout_common, bezout_new = cert.ky_xgcd(
            common_coefficients, new_coefficients, modulus, b
        )
        require(
            set(gcd_record) == {0}
            and gcd_record[0] == Poly(1, b, domain=QQ),
            f"degree-{degree} structural section breaks the common quadratic",
        )
        bezout_check = cert.ky_add(
            cert.ky_mul(
                bezout_common, common_coefficients, modulus, b
            ),
            cert.ky_mul(bezout_new, new_coefficients, modulus, b),
            modulus,
            b,
        )
        require(
            bezout_check == {0: Poly(1, b, domain=QQ)},
            f"degree-{degree} final K[Y] Bezout identity verifies",
        )
        y_resultant = Poly(
            resultant(
                common_expression,
                cert.ky_expression(new_coefficients, y),
                y,
            ),
            b,
            domain=QQ,
        ).rem(modulus)
        require(
            y_resultant.gcd(modulus).degree() == 0,
            f"degree-{degree} independent final Y-resultant is a unit",
        )
        inverse = cert.crtlib.reduce_b(
            invert(y_resultant.as_expr(), modulus.as_expr()), modulus, b
        )
        norm_matrix = cert.crtlib.multiplication_matrix(
            y_resultant, modulus, b
        ).det(method="domain-ge")
        norm_resultant = resultant(
            modulus.as_expr(), y_resultant.as_expr(), b
        )
        require(
            norm_matrix == norm_resultant and norm_matrix != 0,
            f"degree-{degree} final resultant norm verifies independently",
        )
        final_blocks.append(
            {
                "degree": degree,
                "common_quadratic": str(common_expression),
                "new_section_class": str(
                    cert.ky_expression(new_coefficients, y)
                ),
                "bezout_common": str(
                    cert.ky_expression(bezout_common, y)
                ),
                "bezout_new": str(cert.ky_expression(bezout_new, y)),
                "Y_resultant": str(y_resultant.as_expr()),
                "Y_resultant_inverse": str(inverse.as_expr()),
                "norm": str(norm_matrix),
                "covered": True,
            }
        )

    payload = {
        "experiment": "EXP-130-final-certificate",
        "source_hashes": {
            "crt": EXPECTED_CRT,
            "prior_certificate": EXPECTED_PRIOR,
            "structural_selection": EXPECTED_STRUCTURAL_SELECTION,
            "structural_exact": EXPECTED_STRUCTURAL_EXACT,
        },
        "structural_section": {
            "source": exact["source"],
            "rows": rows,
            "A_valuation": valuation,
            "Y_degree": y_degree,
            "invariant_X_B_Y": str(invariant),
            "cyclic_component_sizes": exact["cyclic_component_sizes"],
            "direct_control": {"point": list(control), "ratio": str(direct)},
        },
        "final_degree_3_6_certificates": final_blocks,
        "degree_12_69_certificates": crt["principal_open_algebra"][
            "block_cover_certificates_in_KY"
        ],
        "principal_open_base_locus": {
            "dimension": 90,
            "block_degrees": [3, 6, 12, 69],
            "reduced": True,
            "uniform_in_C": True,
            "covered": True,
        },
        "coordinate_boundary": crt["coordinate_boundary"],
        "decision": "complete_principal_open_base_locus_closed",
        "scope": (
            "Closes V(R,S) intersect D(X) in the declared four-parameter "
            "restriction. The coordinate component X=B=0 belongs to A=0, "
            "which remains separate. The 24-parameter core, 51-parameter "
            "family, (72,108), degree floor, and JC(2) remain open."
        ),
    }
    persist(payload)
    print(f"[PASS] final certificate SHA256 {sha256(ARTIFACT)}", flush=True)
    print("RESULT: COMPLETE PRINCIPAL-OPEN BASE LOCUS CLOSED", flush=True)


if __name__ == "__main__":
    main()
