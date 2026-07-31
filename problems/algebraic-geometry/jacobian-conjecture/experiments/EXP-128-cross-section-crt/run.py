"""EXP-128: cross-section unit tests on the finite graph ledger."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import Matrix, Poly, QQ, expand, gcd, invert, resultant, sympify, symbols


HERE = Path(__file__).resolve().parent
E125_DIR = HERE.parent / "EXP-125-factor-curve-recursion"
E126_DIR = HERE.parent / "EXP-126-f6-divisor-norm"
E127_DIR = HERE.parent / "EXP-127-f7-divisor-norm"
E125_PATH = E125_DIR / "run.py"
E125_ARTIFACT = E125_DIR / "artifacts" / "results.json"
E126_ARTIFACT = E126_DIR / "artifacts" / "results.json"
E127_ARTIFACT = E127_DIR / "artifacts" / "results.json"
ARTIFACT = HERE / "artifacts" / "results.json"
EXPECTED_HASHES = {
    "EXP-125": "2470AB06210C5E8CDE09FB3F1FFA227520D6C810FBF70A8E0713BBCDC240D803",
    "EXP-126": "CF9A4F6284A79344C9361CABE97D34C8FD54654FEF907DA44BD68DD399AA20B1",
    "EXP-127": "75C8385C175B99FE51B2D3481C8820C5D01D51EFABC4FC75CC5A48ABAFCF9AAE",
}
TOTAL_GATE_SECONDS = 180

spec = importlib.util.spec_from_file_location("exp125_crt", E125_PATH)
exp125 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp125)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def persist(payload: dict[str, object]) -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def monic(expression, variable):
    return Poly(expression, variable, domain=QQ).monic()


def product(polynomials):
    result = 1
    for polynomial in polynomials:
        result = expand(result * polynomial.as_expr())
    return result


def retained_factors(records, flag, b):
    return [
        monic(sympify(record["factor"], locals={"B": b}), b)
        for record in records
        if record[flag]
    ]


def same_polynomial(left, right):
    return left.monic() == right.monic()


def quotient_remainder(section, curve, x, b):
    field = QQ.frac_field(b)
    section_poly = Poly(section, x, domain=field)
    curve_poly = Poly(curve, x, domain=field)
    quotient, remainder = section_poly.div(curve_poly)
    require(
        section_poly == quotient * curve_poly + remainder,
        "exact quotient reconstruction",
    )
    return remainder


def quotient_norm(curve, remainder, x, b):
    curve_x = Poly(curve, x, domain=QQ.frac_field(b))
    degree = int(curve_x.degree())
    norm = Poly(expand(resultant(curve, remainder.as_expr(), x)), b, domain=QQ)
    require(not norm.is_zero, "cross-section norm is nonzero")
    multiplication_check = None
    if degree == 1:
        require(remainder.degree() == 0, "linear-curve remainder is constant")
    elif degree == 2:
        require(remainder.degree() <= 1, "quadratic-curve remainder is linear")
        leading = expand(curve_x.LC())
        a1 = expand(curve_x.nth(1))
        a0 = expand(curve_x.nth(0))
        u = expand(remainder.nth(1))
        v = expand(remainder.nth(0))
        matrix = Matrix([[v, -u * a0 / leading], [u, v - u * a1 / leading]])
        multiplication_norm = expand(matrix.det())
        require(
            expand(norm.as_expr() - leading * multiplication_norm) == 0,
            "resultant and quotient-multiplication norms agree",
        )
        multiplication_check = {
            "matrix": [[str(value) for value in row] for row in matrix.tolist()],
            "determinant": str(multiplication_norm),
            "resultant_scale": str(leading),
        }
    else:
        raise AssertionError("unexpected curve degree")
    return norm.monic(), multiplication_check


def unit_test(name, curve, section, ledger, x, b):
    remainder = quotient_remainder(section, curve, x, b)
    if remainder.is_zero:
        print(f"[INFO] {name} vanishes identically on its curve", flush=True)
        return {
            "name": name,
            "curve_degree_X": int(
                Poly(curve, x, domain=QQ.frac_field(b)).degree()
            ),
            "remainder": "0",
            "norm_monic": "0",
            "norm_degree": None,
            "ledger": str(ledger.as_expr()),
            "ledger_degree": int(ledger.degree()),
            "gcd_with_ledger": str(ledger.as_expr()),
            "gcd_degree": int(ledger.degree()),
            "covered_ledger_degree": 0,
            "surviving_ledger_degree": int(ledger.degree()),
            "is_unit_on_ledger": False,
            "multiplication_check": None,
            "norm_inverse_mod_ledger": None,
        }
    norm, multiplication = quotient_norm(curve, remainder, x, b)
    common = gcd(norm, ledger).monic()
    unit = common.degree() == 0
    record = {
        "name": name,
        "curve_degree_X": int(Poly(curve, x, domain=QQ.frac_field(b)).degree()),
        "remainder": str(remainder.as_expr()),
        "norm_monic": str(norm.as_expr()),
        "norm_degree": int(norm.degree()),
        "ledger": str(ledger.as_expr()),
        "ledger_degree": int(ledger.degree()),
        "gcd_with_ledger": str(common.as_expr()),
        "gcd_degree": int(common.degree()),
        "covered_ledger_degree": int(ledger.degree() - common.degree()),
        "surviving_ledger_degree": int(common.degree()),
        "is_unit_on_ledger": unit,
        "multiplication_check": multiplication,
    }
    if unit:
        inverse = invert(norm, ledger)
        identity = Poly(norm.as_expr() * inverse - 1, b, domain=QQ).rem(ledger)
        require(identity.is_zero, f"{name} Bezout inverse verifies modulo ledger")
        record["norm_inverse_mod_ledger"] = str(inverse)
    return record


def crt_records(unique_factors, combined, b):
    records = []
    idempotents = []
    for index, factor in enumerate(unique_factors):
        complement = combined.exquo(factor)
        inverse = invert(complement, factor)
        idempotent = Poly(
            complement.as_expr() * inverse, b, domain=QQ
        ).rem(combined)
        require(
            idempotent.rem(factor) == Poly(1, b, domain=QQ),
            f"CRT block {index + 1} is one on its factor",
        )
        for other_index, other in enumerate(unique_factors):
            if other_index == index:
                continue
            require(
                idempotent.rem(other).is_zero,
                f"CRT block {index + 1} is zero on block {other_index + 1}",
            )
        idempotents.append(idempotent)
        records.append(
            {
                "factor": str(factor.as_expr()),
                "degree": int(factor.degree()),
                "complement": str(complement.as_expr()),
                "inverse_mod_factor": str(inverse),
                "idempotent_mod_combined": str(idempotent.as_expr()),
            }
        )
    total = Poly(sum(item.as_expr() for item in idempotents), b, domain=QQ).rem(
        combined
    )
    require(total == Poly(1, b, domain=QQ), "CRT idempotents sum to one")
    for left in range(len(idempotents)):
        for right in range(left + 1, len(idempotents)):
            require(
                Poly(
                    idempotents[left].as_expr() * idempotents[right].as_expr(),
                    b,
                    domain=QQ,
                ).rem(combined).is_zero,
                f"CRT blocks {left + 1} and {right + 1} are orthogonal",
            )
    return records


def main() -> None:
    started = time.time()
    paths = {
        "EXP-125": E125_ARTIFACT,
        "EXP-126": E126_ARTIFACT,
        "EXP-127": E127_ARTIFACT,
    }
    for name, path in paths.items():
        require(sha256(path) == EXPECTED_HASHES[name], f"{name} result hash")
    e125 = json.loads(E125_ARTIFACT.read_text(encoding="utf-8"))
    e126 = json.loads(E126_ARTIFACT.read_text(encoding="utf-8"))
    e127 = json.loads(E127_ARTIFACT.read_text(encoding="utf-8"))
    x, b, _, _, _, curves, _, _ = exp125.load_polynomials()

    ledgers = {
        "F3": retained_factors(
            e125["F3_quotient_factor_roles"], "retained_on_A_S_nonzero", b
        ),
        "F6": retained_factors(
            e126["norm_factor_roles"], "retained_on_A_S_nonzero", b
        ),
        "F7": retained_factors(
            e127["norm_factor_roles"],
            "retained_conservatively_on_A_S_nonzero",
            b,
        ),
    }
    require([item.degree() for item in ledgers["F3"]] == [9, 15], "F3 ledger")
    require([item.degree() for item in ledgers["F6"]] == [18, 30], "F6 ledger")
    require([item.degree() for item in ledgers["F7"]] == [3, 9, 18], "F7 ledger")

    labelled = [
        (f"{curve}_{int(factor.degree())}", factor)
        for curve, factors in ledgers.items()
        for factor in factors
    ]
    overlaps = []
    for left_index, (left_name, left) in enumerate(labelled):
        for right_name, right in labelled[left_index + 1 :]:
            common = gcd(left, right).monic()
            if common.degree() > 0:
                overlaps.append(
                    {
                        "left": left_name,
                        "right": right_name,
                        "gcd": str(common.as_expr()),
                        "degree": int(common.degree()),
                        "identical": same_polynomial(left, right),
                    }
                )
    print(
        f"[INFO] retained projection overlaps: {len(overlaps)}",
        flush=True,
    )

    unique_factors = []
    block_sources = []
    for name, factor in labelled:
        match = next(
            (index for index, existing in enumerate(unique_factors) if same_polynomial(factor, existing)),
            None,
        )
        if match is None:
            unique_factors.append(factor)
            block_sources.append([name])
        else:
            block_sources[match].append(name)
    combined = monic(product(unique_factors), b)
    require(
        all(
            gcd(unique_factors[i], unique_factors[j]).degree() == 0
            for i in range(len(unique_factors))
            for j in range(i + 1, len(unique_factors))
        ),
        "unique ledger factors are pairwise coprime",
    )
    require(
        gcd(combined, combined.diff()).degree() == 0,
        "combined projected ledger is squarefree",
    )

    h36 = sympify(e125["graph_numerator"], locals={"X": x, "B": b})
    h7 = sympify(e127["quotient_remainder_primitive"], locals={"X": x, "B": b})
    ledger_polys = {
        name: monic(product(factors), b) for name, factors in ledgers.items()
    }
    tests = [
        unit_test("h7_on_F3", curves["F3"], h7, ledger_polys["F3"], x, b),
        unit_test("h7_on_F6", curves["F6"], h7, ledger_polys["F6"], x, b),
        unit_test("h36_on_F7", curves["F7"], h36, ledger_polys["F7"], x, b),
    ]
    complete_graph_cover = all(record["is_unit_on_ledger"] for record in tests)
    crt = crt_records(unique_factors, combined, b)
    require(time.time() - started <= TOTAL_GATE_SECONDS, "EXP-128 remains within gate")

    prediction_1 = len(unique_factors) == 7 and combined.degree() == 102
    payload = {
        "experiment": "EXP-128",
        "source_hashes": EXPECTED_HASHES,
        "retained_ledgers": {
            name: [str(factor.as_expr()) for factor in factors]
            for name, factors in ledgers.items()
        },
        "pairwise_projection_overlaps": overlaps,
        "declared_factor_count": len(labelled),
        "unique_projected_factor_count": len(unique_factors),
        "unique_block_sources": block_sources,
        "combined_projected_ledger_monic": str(combined.as_expr()),
        "combined_projected_ledger_degree": int(combined.degree()),
        "combined_projected_ledger_squarefree": True,
        "crt_blocks": crt,
        "cross_section_unit_tests": tests,
        "complete_rational_graph_cover_on_A_S_nonzero": complete_graph_cover,
        "cross_section_coverage_summary": {
            "h7_covers_F3_degree": tests[0]["covered_ledger_degree"],
            "h7_leaves_F3_degree": tests[0]["surviving_ledger_degree"],
            "h7_covers_F6_degree": tests[1]["covered_ledger_degree"],
            "h7_leaves_F6_degree": tests[1]["surviving_ledger_degree"],
            "h36_covers_F7_degree": tests[2]["covered_ledger_degree"],
            "h36_leaves_F7_degree": tests[2]["surviving_ledger_degree"],
        },
        "predictions": {
            "p1_seven_pairwise_coprime_degree_102": prediction_1,
            "p2_h7_unit_on_F3_ledger": tests[0]["is_unit_on_ledger"],
            "p3_h7_unit_on_F6_ledger": tests[1]["is_unit_on_ledger"],
            "p4_h36_unit_on_F7_ledger": tests[2]["is_unit_on_ledger"],
            "p5_exact_bezout_and_crt_identities": True,
        },
        "scope": (
            "Cross-coverage of the retained F3/F6/F7 divisors on the "
            "AS!=0 rational graph only. V(R,S), A=0, the full four-parameter "
            "restriction, (72,108), the degree floor, and JC(2) remain open."
        ),
    }
    persist(payload)
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {sha256(ARTIFACT)}", flush=True)
    print(
        f"[INFO] unique_projection_degree={combined.degree()}, "
        f"cross_units={[record['is_unit_on_ledger'] for record in tests]}, "
        f"complete_graph_cover={complete_graph_cover}",
        flush=True,
    )
    print("RESULT: COMPLETE", flush=True)


if __name__ == "__main__":
    main()
