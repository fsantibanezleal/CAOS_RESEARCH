"""EXP-134: exact graph-quotient lift of the EXP-124 section."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import Poly, QQ, Rational, expand, eye, symbols, sympify


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP133_RUN = EXPERIMENTS / "EXP-133-principal-open-28-lift-preflight" / "run.py"
EXP124_CHECKPOINT = (
    EXPERIMENTS
    / "EXP-124-rational-graph-alternative-chart"
    / "artifacts"
    / "checkpoint.json"
)
EXP124_WORKER = (
    EXPERIMENTS
    / "EXP-124-rational-graph-alternative-chart"
    / "artifacts"
    / "symbolic-worker.json"
)
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
ARTIFACT = HERE / "artifacts" / "results.json"
MAX_CORE = 35
TARGET = (2, 8)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


exp133 = load_module("exp133_for_exp134", EXP133_RUN)
exp124 = exp133.exp124


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def persist(payload: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)
    print(f"[PASS] {message}", flush=True)


def main() -> None:
    started = time.time()
    e124_checkpoint = read_json(EXP124_CHECKPOINT)
    e124_worker = read_json(EXP124_WORKER)
    e123 = read_json(exp133.EXP123_RESULT)
    rows = list(e124_checkpoint["selected_rows"])
    anchor_point = list(e124_checkpoint["anchor"]["point"])

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
    directions[TARGET] = exp124.exp112.coefficient_matrix(
        {TARGET: exp124.exp112.Fraction(1)},
        complete_rows,
        q_columns,
        include_rhs=False,
    )
    require(base.shape == (302, 125), "rebuilt original 302 by 125 matrix")
    require(len(rows) == len(set(rows)) == 125, "loaded accepted EXP-124 section")

    selected_base = base.extract(rows, range(125))
    selected_directions = {
        direction: directions[direction].extract(rows, range(125))
        for direction in ((0, 1), (0, 5), (2, 9), TARGET)
    }
    anchor = (
        selected_base
        + anchor_point[0] * selected_directions[(0, 1)]
        + anchor_point[1] * selected_directions[(0, 5)]
        + anchor_point[2] * selected_directions[(2, 9)]
    )
    inverse = anchor.inv()
    normalized = {
        direction: inverse * matrix
        for direction, matrix in selected_directions.items()
    }
    components = exp124.exp122.cyclic_components(list(normalized.values()))
    component_sizes = [len(component) for component in components]
    require(max(component_sizes) <= MAX_CORE, "joint exact cyclic core at most 35")

    payload: dict[str, object] = {
        "experiment": "EXP-134",
        "decision": "exact_worker_running",
        "source_sha256": {
            str(path.relative_to(EXPERIMENTS)): digest(path)
            for path in (
                exp133.EXP123_RESULT,
                EXP124_CHECKPOINT,
                EXP124_WORKER,
            )
        },
        "selected_rows": rows,
        "anchor": anchor_point,
        "component_sizes": component_sizes,
        "largest_component": max(component_sizes),
        "blocks": [],
    }
    persist(payload, CHECKPOINT)

    a, b, c, t = symbols("A B C T")
    expression = Rational(1)
    for index, component in enumerate(components, start=1):
        block = (
            eye(len(component))
            + (a - anchor_point[0])
            * normalized[(0, 1)].extract(component, component)
            + (b - anchor_point[1])
            * normalized[(0, 5)].extract(component, component)
            + (c - anchor_point[2])
            * normalized[(2, 9)].extract(component, component)
            + t * normalized[TARGET].extract(component, component)
        )
        determinant = expand(block.det(method="domain-ge"))
        expression = expand(expression * determinant)
        payload["blocks"].append(
            {
                "size": len(component),
                "vertices": component,
                "determinant": str(determinant),
            }
        )
        persist(payload, CHECKPOINT)
        print(
            f"[INFO] exact block {index}/{len(components)} size={len(component)}",
            flush=True,
        )

    t_polynomial = Poly(expression, t)
    t0 = expand(t_polynomial.nth(0))
    expected_t0 = sympify(
        e124_worker["determinant_ratio"],
        locals={"A": a, "B": b, "C": c},
    )
    require(expand(t0 - expected_t0) == 0, "reproduced EXP-124 ratio at T=0")

    x = symbols("X")
    r_expression = sympify(
        e123["invariant_reduction"]["R_X_B"],
        locals={"X": x, "B": b},
    )
    s_expression = sympify(
        e123["invariant_reduction"]["S_X_B"],
        locals={"X": x, "B": b},
    )
    graph = expand(
        r_expression.subs(x, a**3) + a**2 * c * s_expression.subs(x, a**3)
    )
    graph_poly = Poly(graph, a, b, c, domain=QQ)
    coefficient_records = []
    ambient_nonzero = False
    all_divisible = True
    for degree in range(1, t_polynomial.degree() + 1):
        coefficient = expand(t_polynomial.nth(degree))
        ambient_nonzero = ambient_nonzero or coefficient != 0
        quotient, remainder = Poly(coefficient, a, b, c, domain=QQ).div(graph_poly)
        divisible = remainder.is_zero
        all_divisible = all_divisible and divisible
        coefficient_records.append(
            {
                "degree_T": degree,
                "coefficient": str(coefficient),
                "coefficient_total_degree": (
                    Poly(coefficient, a, b, c).total_degree() if coefficient != 0 else -1
                ),
                "coefficient_terms": (
                    len(Poly(coefficient, a, b, c).terms()) if coefficient != 0 else 0
                ),
                "divisible_by_graph": divisible,
                "quotient": str(quotient.as_expr()) if divisible else None,
                "remainder": str(remainder.as_expr()),
            }
        )
    require(all_divisible, "every positive-T coefficient is divisible by graph equation")

    payload.update(
        {
            "decision": "confirmed_graph_quotient_T_inert",
            "elapsed_seconds": time.time() - started,
            "determinant_ratio": str(expression),
            "degree_T_ambient": t_polynomial.degree(),
            "ambient_positive_T_coefficient_nonzero": ambient_nonzero,
            "graph_equation": str(graph),
            "coefficient_records": coefficient_records,
            "predictions": {
                "p1_joint_core_at_most_35": max(component_sizes) <= MAX_CORE,
                "p2_T0_reproduced": True,
                "p3_all_positive_T_coefficients_in_graph_ideal": all_divisible,
                "p4_ambient_T_dependence_nonzero": ambient_nonzero,
            },
            "scope": (
                "Exact T-inertness of one EXP-124 minor on the rational graph only. "
                "No residual-curve, base-locus, five-coefficient, (72,108), floor, "
                "or JC(2) closure."
            ),
        }
    )
    persist(payload, ARTIFACT)
    require(read_json(ARTIFACT)["decision"] == payload["decision"], "reloaded result artifact")
    print(f"[PASS] results SHA256 {digest(ARTIFACT)}", flush=True)


if __name__ == "__main__":
    main()
