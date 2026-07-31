"""EXP-129: exact norm-ideal closure of the retained F7 CRT divisor."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import Poly, QQ, expand, fraction, gcd, invert, resultant, sympify, symbols, together


HERE = Path(__file__).resolve().parent
E125_PATH = HERE.parent / "EXP-125-factor-curve-recursion" / "run.py"
E127_ARTIFACT = HERE.parent / "EXP-127-f7-divisor-norm" / "artifacts" / "results.json"
SELECTION = HERE / "artifacts" / "selection.json"
WORKER = HERE / "artifacts" / "exact-worker.json"
ARTIFACT = HERE / "artifacts" / "results.json"
EXPECTED = {
    "EXP-127": "75C8385C175B99FE51B2D3481C8820C5D01D51EFABC4FC75CC5A48ABAFCF9AAE",
    "selection": "B43053AEEE214A77E79AEE00FBE6B66EFB3A5C2F2DF410A650B8EFA43982CEC3",
    "worker": "C2391B0F19840AB617DCDC3FC1AF217EE8B45A93A1E5DBCB579DD4FEB6474527",
}
TOTAL_GATE_SECONDS = 300

spec = importlib.util.spec_from_file_location("exp125_exp129_main", E125_PATH)
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
    ARTIFACT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    started = time.time()
    paths = {"EXP-127": E127_ARTIFACT, "selection": SELECTION, "worker": WORKER}
    for name, path in paths.items():
        require(sha256(path) == EXPECTED[name], f"{name} artifact hash")
    e127 = json.loads(E127_ARTIFACT.read_text(encoding="utf-8"))
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    worker = json.loads(WORKER.read_text(encoding="utf-8"))
    require(len(worker["atlas_records"]) == 2, "two exact atlas bases reconstructed")

    x, b, y, r, s, curves, _, _ = exp125.load_polynomials()
    a, c = symbols("A C")
    f7 = curves["F7"]
    blocks = [
        {
            "degree": int(record["degree"]),
            "factor": Poly(sympify(record["factor"], locals={"B": b}), b, domain=QQ).monic(),
        }
        for record in selection["blocks"]
    ]
    atlas_records = []
    for record in worker["atlas_records"]:
        expression = sympify(record["determinant_ratio"], locals={"A": a, "B": b, "C": c})
        valuation, invariant = exp125.exp124.invariant_reduce(expression, a, b, c, x, y)
        invariant_y = Poly(invariant, y, domain="QQ[X,B]")
        graph_numerator = expand(
            sum(
                invariant_y.nth(power) * (-r) ** power * s ** (invariant_y.degree() - power)
                for power in range(invariant_y.degree() + 1)
            )
        )
        require(graph_numerator != 0, f"atlas {record['atlas_index']} graph section is nonzero")
        field = QQ.frac_field(b)
        quotient, remainder = Poly(graph_numerator, x, domain=field).div(Poly(f7, x, domain=field))
        require(
            Poly(graph_numerator, x, domain=field) == quotient * Poly(f7, x, domain=field) + remainder,
            f"atlas {record['atlas_index']} exact F7 quotient reconstruction",
        )
        require(not remainder.is_zero, f"atlas {record['atlas_index']} is nonzero in the F7 function field")
        require(remainder.degree() <= 1, f"atlas {record['atlas_index']} F7 remainder degree at most one")
        numerator, denominator = fraction(together(remainder.as_expr()))
        require(not denominator.has(x), f"atlas {record['atlas_index']} remainder denominator is X-free")
        primitive_poly = Poly(numerator, x, b, domain=QQ)
        _, integer_poly = primitive_poly.clear_denoms(convert=True)
        _, primitive = integer_poly.primitive()
        if primitive.LC() < 0:
            primitive = -primitive
        section = primitive.as_expr()
        norm = Poly(expand(resultant(f7, section, x)), b, domain=QQ)
        require(not norm.is_zero, f"atlas {record['atlas_index']} norm is nonzero")
        norm = norm.monic()
        block_tests = []
        for block in blocks:
            common = gcd(norm, block["factor"]).monic()
            unit = common.degree() == 0
            inverse = None
            if unit:
                inverse_poly = invert(norm, block["factor"])
                identity = Poly(norm.as_expr() * inverse_poly - 1, b, domain=QQ).rem(block["factor"])
                require(identity.is_zero, f"atlas {record['atlas_index']} degree-{block['degree']} Bezout identity")
                inverse = str(inverse_poly)
            block_tests.append({
                "degree": block["degree"],
                "factor": str(block["factor"].as_expr()),
                "gcd": str(common.as_expr()),
                "gcd_degree": int(common.degree()),
                "is_unit": unit,
                "inverse_mod_factor": inverse,
            })
        atlas_records.append({
            "atlas_index": record["atlas_index"],
            "source_degree": record["source_degree"],
            "rows": record["rows"],
            "anchor": record["anchor"],
            "cyclic_component_sizes": record["cyclic_component_sizes"],
            "determinant_A_valuation": valuation,
            "invariant_Y_degree": int(invariant_y.degree()),
            "invariant_determinant_X_B_Y": str(invariant),
            "graph_numerator": str(graph_numerator),
            "F7_remainder_primitive": str(section),
            "norm_monic": str(norm.as_expr()),
            "norm_degree": int(norm.degree()),
            "block_unit_tests": block_tests,
        })

    coverage = []
    for block in blocks:
        covering = [
            record["atlas_index"]
            for record in atlas_records
            if next(test for test in record["block_unit_tests"] if test["degree"] == block["degree"])["is_unit"]
        ]
        require(bool(covering), f"exact atlas norm ideal is unit on degree-{block['degree']} block")
        coverage.append({"degree": block["degree"], "covering_atlas_indices": covering})
    require(time.time() - started <= TOTAL_GATE_SECONDS, "exact norm-ideal gate remains within budget")

    payload = {
        "experiment": "EXP-129",
        "source_hashes": EXPECTED,
        "same_exact_point_overlaps": selection["same_point_checks"],
        "modular_selection": {
            "probe_counts": selection["probe_counts"],
            "single_basis_found": selection["single_basis_found"],
            "atlas_size": selection["atlas_size"],
        },
        "exact_atlas": atlas_records,
        "blockwise_unit_ideal_coverage": coverage,
        "all_retained_F7_blocks_covered": True,
        "all_known_finite_AS_nonzero_graph_residuals_covered_with_EXP128": True,
        "predictions": {
            "p1_same_exact_points": True,
            "p2_full_rank_modular_probes": True,
            "p3_single_basis": False,
            "p4_exact_reconstruction": True,
            "p5_atlas_norm_ideal_is_unit": True,
        },
        "scope": (
            "Exact closure of the known finite F3/F6/F7 residual union on the AS!=0 EXP-123 graph, "
            "using EXP-128 plus a two-section F7 atlas. V(R,S), A=0, the full four-parameter restriction, "
            "(72,108), the degree floor, and JC(2) remain open."
        ),
    }
    persist(payload)
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {sha256(ARTIFACT)}", flush=True)
    print(f"[INFO] exact block coverage={coverage}", flush=True)
    print("RESULT: COMPLETE", flush=True)


if __name__ == "__main__":
    main()
