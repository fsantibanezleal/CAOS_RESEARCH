"""EXP-129 selection gate: exact point overlap and modular row-basis atlas."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import Poly, QQ, expand, invert, primerange, sympify, symbols


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
E125_DIR = ROOT / "EXP-125-factor-curve-recursion"
E125_PATH = E125_DIR / "run.py"
E125_ARTIFACT = E125_DIR / "artifacts" / "results.json"
E127_ARTIFACT = ROOT / "EXP-127-f7-divisor-norm" / "artifacts" / "results.json"
E128_ARTIFACT = ROOT / "EXP-128-cross-section-crt" / "artifacts" / "results.json"
ARTIFACT = HERE / "artifacts" / "selection.json"
EXPECTED = {
    "EXP-125": "2470AB06210C5E8CDE09FB3F1FFA227520D6C810FBF70A8E0713BBCDC240D803",
    "EXP-127": "75C8385C175B99FE51B2D3481C8820C5D01D51EFABC4FC75CC5A48ABAFCF9AAE",
    "EXP-128": "AAC40AA02B7E8E2F593E2F634EC518C7DF960EC4F50C61367AFFE0149E84EDD0",
}
PROBES_PER_BLOCK = 2
TOTAL_GATE_SECONDS = 180

spec = importlib.util.spec_from_file_location("exp125_exp129", E125_PATH)
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


def reduce_mod(expression, modulus, variable):
    return Poly(expand(expression), variable, domain=QQ).rem(modulus).as_expr()


def eval_mod(expression, variables, values, prime):
    polynomial = Poly(expression, *variables, domain=QQ)
    value = 0
    for powers, coefficient in polynomial.terms():
        coefficient_mod = exp125.exp124.mod_entry(coefficient, prime)
        term = coefficient_mod
        for scalar, power in zip(values, powers):
            term = term * pow(int(scalar), int(power), prime) % prime
        value = (value + term) % prime
    return value


def main() -> None:
    started = time.time()
    paths = {
        "EXP-125": E125_ARTIFACT,
        "EXP-127": E127_ARTIFACT,
        "EXP-128": E128_ARTIFACT,
    }
    for name, path in paths.items():
        require(sha256(path) == EXPECTED[name], f"{name} result hash")
    e125 = json.loads(E125_ARTIFACT.read_text(encoding="utf-8"))
    e127 = json.loads(E127_ARTIFACT.read_text(encoding="utf-8"))
    e128 = json.loads(E128_ARTIFACT.read_text(encoding="utf-8"))
    x, b, _, r, s, curves, _, _ = exp125.load_polynomials()
    a, c = symbols("A C")
    h7 = sympify(e127["quotient_remainder_primitive"], locals={"X": x, "B": b})
    h7_x = Poly(h7, x, domain=QQ.frac_field(b))
    require(h7_x.degree() == 1, "h7 is linear in X")
    u = expand(h7_x.nth(1))
    v = expand(h7_x.nth(0))

    ledger_records = [
        record
        for record in e127["norm_factor_roles"]
        if record["retained_conservatively_on_A_S_nonzero"]
    ]
    require([record["degree"] for record in ledger_records] == [3, 9, 18], "F7 ledger degrees")
    blocks = []
    for record in ledger_records:
        modulus = Poly(sympify(record["factor"], locals={"B": b}), b, domain=QQ).monic()
        u_inverse = invert(Poly(u, b, domain=QQ), modulus)
        x_class = reduce_mod(-v * u_inverse.as_expr(), modulus, b)
        require(reduce_mod(h7.subs(x, x_class), modulus, b) == 0, f"degree-{record['degree']} h7 point class")
        require(reduce_mod(curves["F7"].subs(x, x_class), modulus, b) == 0, f"degree-{record['degree']} F7 point class")
        if record["degree"] == 9:
            require(reduce_mod(curves["F3"].subs(x, x_class), modulus, b) == 0, "degree-9 F3/F7 same X-class")
        if record["degree"] == 18:
            require(reduce_mod(curves["F6"].subs(x, x_class), modulus, b) == 0, "degree-18 F6/F7 same X-class")
        blocks.append({"degree": int(record["degree"]), "factor": modulus, "X_class": x_class})

    base, directions = exp125.exp124.build_full_system()
    matrices_by_prime = {}
    probes = []
    probe_counts = {block["degree"]: 0 for block in blocks}
    for prime in primerange(127, 2500):
        if all(count >= PROBES_PER_BLOCK for count in probe_counts.values()):
            break
        try:
            block_roots = {
                block["degree"]: [
                    bv
                    for bv in range(prime)
                    if eval_mod(block["factor"].as_expr(), (b,), (bv,), prime) == 0
                ]
                for block in blocks
                if probe_counts[block["degree"]] < PROBES_PER_BLOCK
            }
        except ValueError:
            continue
        if not any(block_roots.values()):
            continue
        matrices = {
            "base": exp125.exp124.exp115.matrix_mod(base, prime),
            "A": exp125.exp124.exp115.matrix_mod(directions[(0, 1)], prime),
            "B": exp125.exp124.exp115.matrix_mod(directions[(0, 5)], prime),
            "C": exp125.exp124.exp115.matrix_mod(directions[exp125.exp124.TARGET], prime),
        }
        matrices_by_prime[prime] = matrices
        for block in blocks:
            degree = block["degree"]
            if probe_counts[degree] >= PROBES_PER_BLOCK:
                continue
            for bv in block_roots.get(degree, []):
                xv = eval_mod(block["X_class"], (b,), (bv,), prime)
                roots_a = [av for av in range(1, prime) if pow(av, 3, prime) == xv]
                for av in roots_a:
                    sv = eval_mod(s, (x, b), (xv, bv), prime)
                    if sv == 0:
                        continue
                    rv = eval_mod(r, (x, b), (xv, bv), prime)
                    yv = -rv * pow(sv, -1, prime) % prime
                    cv = yv * pow(av * av, -1, prime) % prime
                    evaluated = exp125.exp124.combine_mod(
                        matrices["base"], matrices["A"], matrices["B"], matrices["C"], av, bv, cv, prime
                    )
                    rows = exp125.independent_row_basis_fast(evaluated, prime)
                    require(len(rows) == 125, f"degree-{degree} probe has full row rank at p={prime}")
                    probes.append({
                        "degree": degree,
                        "prime": prime,
                        "A": av,
                        "B": bv,
                        "C": cv,
                        "X": xv,
                        "Y": yv,
                        "row_basis": rows,
                    })
                    probe_counts[degree] += 1
                    break
                if probe_counts[degree] >= PROBES_PER_BLOCK:
                    break

    require(all(count >= PROBES_PER_BLOCK for count in probe_counts.values()), "two modular probes found on every CRT block")
    existing = {tuple(e125["selected_rows"][name]) for name in ("F3", "F6", "F7")}
    candidates = []
    for probe in probes:
        rows = probe["row_basis"]
        key = tuple(rows)
        if key in existing or any(item["rows"] == rows for item in candidates):
            continue
        coverage = []
        for target in probes:
            matrices = matrices_by_prime[target["prime"]]
            evaluated = exp125.exp124.combine_mod(
                matrices["base"], matrices["A"], matrices["B"], matrices["C"],
                target["A"], target["B"], target["C"], target["prime"],
            )
            nonzero = exp125.determinant_mod_fast(evaluated, rows, target["prime"]) != 0
            coverage.append({"degree": target["degree"], "prime": target["prime"], "nonzero": nonzero})
        candidates.append({"rows": rows, "source_degree": probe["degree"], "coverage": coverage})
    complete = next((item for item in candidates if all(test["nonzero"] for test in item["coverage"])), None)
    uncovered = set(range(len(probes)))
    atlas = []
    while uncovered:
        best = max(
            candidates,
            key=lambda item: sum(
                1 for index in uncovered if item["coverage"][index]["nonzero"]
            ),
        )
        newly_covered = {
            index for index in uncovered if best["coverage"][index]["nonzero"]
        }
        require(bool(newly_covered), "candidate atlas advances modular probe coverage")
        atlas.append(best)
        uncovered -= newly_covered
    require(not uncovered, "finite row-basis atlas covers every modular CRT probe")
    require(time.time() - started <= TOTAL_GATE_SECONDS, "selection gate remains within budget")

    payload = {
        "experiment": "EXP-129-selection",
        "source_hashes": EXPECTED,
        "same_point_checks": {
            "degree_9_F3_F7_same_X_class": True,
            "degree_18_F6_F7_same_X_class": True,
        },
        "blocks": [
            {"degree": block["degree"], "factor": str(block["factor"].as_expr()), "X_class": str(block["X_class"])}
            for block in blocks
        ],
        "probe_counts": {str(key): value for key, value in probe_counts.items()},
        "probes": probes,
        "candidate_count": len(candidates),
        "single_basis_found": complete is not None,
        "atlas_size": len(atlas),
        "selected_atlas": atlas,
        "selection_predictions": {"p1_same_exact_points": True, "p2_full_rank": True, "p3_single_modular_basis": complete is not None},
        "scope": "Modular selection gate only; characteristic-zero closure requires exact determinant reconstruction and norm gcds.",
    }
    persist(payload)
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {sha256(ARTIFACT)}", flush=True)
    print(f"[INFO] primes={sorted(matrices_by_prime)}, candidates={len(candidates)}, atlas_size={len(atlas)}, single_basis={complete is not None}", flush=True)
    print("RESULT: SELECTION COMPLETE", flush=True)


if __name__ == "__main__":
    main()
