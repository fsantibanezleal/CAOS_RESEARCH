"""EXP-134: exact transverse reduction of the accepted EXP-124 graph section."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

from sympy import Poly, QQ, expand, factor_list, sympify, symbols


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP123_RESULTS = (
    EXPERIMENTS
    / "EXP-123-direction-29-symbolic-lift"
    / "artifacts"
    / "results.json"
)
EXP124_RUN = EXPERIMENTS / "EXP-124-rational-graph-alternative-chart" / "run.py"
EXP124_RESULTS = (
    EXPERIMENTS
    / "EXP-124-rational-graph-alternative-chart"
    / "artifacts"
    / "results.json"
)
EXP124_WORKER = (
    EXPERIMENTS
    / "EXP-124-rational-graph-alternative-chart"
    / "artifacts"
    / "symbolic-worker.json"
)
EXP133_RESULTS = (
    EXPERIMENTS
    / "EXP-133-principal-open-28-lift-preflight"
    / "artifacts"
    / "results.json"
)
WORKER = HERE / "symbolic_worker.py"
WORKER_ARTIFACT = HERE / "artifacts" / "symbolic-worker.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
ARTIFACT = HERE / "artifacts" / "results.json"
WORKER_TIMEOUT_SECONDS = 300
TOTAL_GATE_SECONDS = 420


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}", flush=True)


def persist(payload: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def graph_numerator(coefficient, a, b, c, r_ab, s_ab):
    polynomial = Poly(coefficient, c, domain="QQ[A,B]")
    degree = int(polynomial.degree()) if not polynomial.is_zero else 0
    denominator = expand(a**2 * s_ab)
    numerator = expand(
        sum(
            polynomial.nth(power)
            * (-r_ab) ** power
            * denominator ** (degree - power)
            for power in range(degree + 1)
        )
    )
    return degree, numerator


def build_selected_system(exp124, rows):
    base, directions = exp124.build_full_system()
    forced = exp124.exp112.forced_polynomial()
    all_directions = sorted(exp124.exp112.exp071.LOWER)
    _, complete_rows = exp124.exp112.complete_row_labels(forced, all_directions)
    constant_column = exp124.exp112.exp071.NQ.index((0, 0))
    q_columns = [
        index
        for index in range(len(exp124.exp112.exp071.NQ))
        if index != constant_column
    ]
    directions[(2, 8)] = exp124.exp112.coefficient_matrix(
        {(2, 8): exp124.exp112.Fraction(1)},
        complete_rows,
        q_columns,
        include_rhs=False,
    )
    selected_base = base.extract(rows, range(125))
    selected_directions = {
        direction: matrix.extract(rows, range(125))
        for direction, matrix in directions.items()
    }
    return selected_base, selected_directions


def main() -> None:
    started = time.time()
    exp124 = load_module("exp124_for_134_run", EXP124_RUN)
    e123 = json.loads(EXP123_RESULTS.read_text(encoding="utf-8"))
    e124 = json.loads(EXP124_RESULTS.read_text(encoding="utf-8"))
    e124_worker = json.loads(EXP124_WORKER.read_text(encoding="utf-8"))
    e133 = json.loads(EXP133_RESULTS.read_text(encoding="utf-8"))
    rows = list(e124["selected_rows"])
    require(len(rows) == 125 and len(set(rows)) == 125, "loaded accepted EXP-124 row section")
    require(
        e133["degree_ledger"]["EXP-124-graph"] == [0, 0, 0, 0],
        "reproduced EXP-133 modular inertness premise",
    )

    selected_base, selected_directions = build_selected_system(exp124, rows)
    anchor = selected_base + selected_directions[(0, 1)]
    anchor_determinant = anchor.det(method="domain-ge")
    require(anchor_determinant != 0, "accepted rational anchor is invertible")
    inverse = anchor.inv()
    normalized = {
        direction: inverse * matrix
        for direction, matrix in selected_directions.items()
    }
    components = exp124.exp122.cyclic_components(list(normalized.values()))
    largest = max(len(component) for component in components)
    require(largest <= 45, "joint exact SCC remains inside gate 45")

    payload: dict[str, object] = {
        "experiment": "EXP-134",
        "selected_rows": rows,
        "source_sha256": {
            str(EXP123_RESULTS.relative_to(EXPERIMENTS)): digest(EXP123_RESULTS),
            str(EXP124_RESULTS.relative_to(EXPERIMENTS)): digest(EXP124_RESULTS),
            str(EXP124_WORKER.relative_to(EXPERIMENTS)): digest(EXP124_WORKER),
            str(EXP133_RESULTS.relative_to(EXPERIMENTS)): digest(EXP133_RESULTS),
        },
        "anchor_determinant": str(anchor_determinant),
        "joint_component_sizes": [len(component) for component in components],
        "largest_joint_component": largest,
    }
    persist(payload, CHECKPOINT)

    try:
        worker = subprocess.run(
            [sys.executable, str(WORKER)],
            cwd=HERE,
            capture_output=True,
            text=True,
            timeout=WORKER_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        payload["decision"] = "stopped_at_exact_worker_gate"
        payload["worker_stdout"] = error.stdout or ""
        payload["worker_stderr"] = error.stderr or ""
        payload["elapsed_seconds"] = time.time() - started
        persist(payload, ARTIFACT)
        print("[STOP] exact worker reached five-minute gate", flush=True)
        print("RESULT: INCONCLUSIVE AT DECLARED GATE", flush=True)
        return
    print(worker.stdout, end="", flush=True)
    if worker.stderr:
        print(worker.stderr, file=sys.stderr, end="", flush=True)
    require(worker.returncode == 0, "exact symbolic worker completed")

    worker_record = json.loads(WORKER_ARTIFACT.read_text(encoding="utf-8"))
    a, b, c, t, x, y = symbols("A B C T X Y")
    expression = sympify(
        worker_record["determinant_ratio"],
        locals={"A": a, "B": b, "C": c, "T": t},
    )
    old_expression = sympify(
        e124_worker["determinant_ratio"],
        locals={"A": a, "B": b, "C": c},
    )
    require(
        expand(expression.subs(t, 0) - old_expression) == 0,
        "T=0 determinant reproduces the accepted EXP-124 section",
    )

    polynomial_t = Poly(expression, t, domain="QQ[A,B,C]")
    degree_t = int(polynomial_t.degree())
    require(degree_t <= 1, "exact determinant is at most affine in T")
    r = sympify(e123["invariant_reduction"]["R_X_B"], locals={"X": x, "B": b})
    s = sympify(e123["invariant_reduction"]["S_X_B"], locals={"X": x, "B": b})
    r_ab = expand(r.subs(x, a**3))
    s_ab = expand(s.subs(x, a**3))

    transverse_records = []
    all_positive_coefficients_vanish = True
    for power in range(1, degree_t + 1):
        coefficient = expand(polynomial_t.nth(power))
        c_degree, numerator = graph_numerator(coefficient, a, b, c, r_ab, s_ab)
        vanishes = numerator == 0
        all_positive_coefficients_vanish &= vanishes
        transverse_records.append(
            {
                "T_power": power,
                "C_degree": c_degree,
                "coefficient": str(coefficient),
                "cleared_graph_numerator": str(numerator),
                "vanishes_on_graph": vanishes,
            }
        )
    require(
        all_positive_coefficients_vanish,
        "every positive T coefficient vanishes on the EXP-123 graph",
    )

    invariant_n = sympify(
        e124["graph_numerator"], locals={"X": x, "B": b}
    )
    accepted_factors = factor_list(invariant_n, x, b)
    require(len(accepted_factors[1]) == 3, "retained accepted F3 F6 F7 factor ledger")

    controls = []
    for av, bv, cv, tv in ((1, 0, 0, 1), (1, 1, 1, 2), (2, 1, 1, -1), (-1, 1, 2, 3)):
        direct = (
            selected_base
            + av * selected_directions[(0, 1)]
            + bv * selected_directions[(0, 5)]
            + cv * selected_directions[(2, 9)]
            + tv * selected_directions[(2, 8)]
        ).det(method="domain-ge") / anchor_determinant
        predicted = expression.subs({a: av, b: bv, c: cv, t: tv})
        require(direct == predicted, f"direct determinant control ({av},{bv},{cv},{tv})")
        controls.append({"point": [av, bv, cv, tv], "ratio": str(direct)})

    payload.update(
        {
            "symbolic_worker": worker_record,
            "exact_degree_in_T": degree_t,
            "transverse_coefficient_records": transverse_records,
            "graph_restriction_T_inert": all_positive_coefficients_vanish,
            "retained_graph_numerator": str(invariant_n),
            "retained_factorization": [
                {"factor": str(factor), "multiplicity": multiplicity}
                for factor, multiplicity in accepted_factors[1]
            ],
            "direct_exact_controls": controls,
            "decision": "exp124_graph_section_exactly_T_inert",
            "predictions": {
                "p1_joint_scc_at_most_45": largest <= 45,
                "p2_exact_T_degree_at_most_one": degree_t <= 1,
                "p3_positive_T_coefficients_vanish_mod_graph": all_positive_coefficients_vanish,
                "p4_T0_reproduces_EXP124": True,
            },
            "elapsed_seconds": time.time() - started,
            "scope": (
                "Exact characteristic-zero divisibility for the accepted EXP-124 section. "
                "The F3 F6 F7 residual ledger is retained, but its transverse residual "
                "is not covered until the EXP-129 sections are lifted. No claim about the "
                "finite base locus, complete five-coefficient restriction, 24-parameter "
                "core, (72,108), degree floor, or JC(2)."
            ),
        }
    )
    require(payload["elapsed_seconds"] <= TOTAL_GATE_SECONDS, "EXP-134 remains inside total gate")
    persist(payload, ARTIFACT)
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {digest(ARTIFACT)}", flush=True)
    print(
        f"[DONE] {payload['decision']} degree_T={degree_t} "
        f"largest_scc={largest} elapsed={payload['elapsed_seconds']:.2f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
