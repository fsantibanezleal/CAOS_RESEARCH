"""EXP-134 attempt 002: exact determinant after rational-graph reduction."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import Matrix, Poly, QQ, Rational, cancel, expand, eye, symbols, sympify


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP133_RUN = EXPERIMENTS / "EXP-133-principal-open-28-lift-preflight" / "run.py"
EXP124_CHECKPOINT = (
    EXPERIMENTS / "EXP-124-rational-graph-alternative-chart/artifacts/checkpoint.json"
)
EXP124_WORKER = (
    EXPERIMENTS / "EXP-124-rational-graph-alternative-chart/artifacts/symbolic-worker.json"
)
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
ARTIFACT = HERE / "artifacts" / "results.json"
TARGET = (2, 8)
MAX_CORE = 45


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


exp133 = load_module("exp133_for_exp134_graph", EXP133_RUN)
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


def selected_system():
    checkpoint = read_json(EXP124_CHECKPOINT)
    rows = list(checkpoint["selected_rows"])
    anchor_point = list(checkpoint["anchor"]["point"])
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
    return rows, anchor_point, anchor, selected_base, selected_directions


def direct_ratio(
    anchor_determinant,
    selected_base,
    directions,
    a_value,
    b_value,
    c_value,
    t_value,
):
    matrix = (
        selected_base
        + a_value * directions[(0, 1)]
        + b_value * directions[(0, 5)]
        + c_value * directions[(2, 9)]
        + t_value * directions[TARGET]
    )
    return cancel(matrix.det(method="domain-ge") / anchor_determinant)


def main() -> None:
    started = time.time()
    e123 = read_json(exp133.EXP123_RESULT)
    e124_worker = read_json(EXP124_WORKER)
    rows, anchor_point, anchor, selected_base, directions = selected_system()
    require(len(rows) == len(set(rows)) == 125, "loaded accepted EXP-124 section")

    inverse = anchor.inv()
    normalized = {direction: inverse * matrix for direction, matrix in directions.items()}
    components = exp124.exp122.cyclic_components(list(normalized.values()))
    sizes = [len(component) for component in components]
    require(max(sizes) <= MAX_CORE, "joint exact cyclic core within gate")

    a, b, t, x = symbols("A B T X")
    r_x_b = sympify(
        e123["invariant_reduction"]["R_X_B"], locals={"X": x, "B": b}
    )
    s_x_b = sympify(
        e123["invariant_reduction"]["S_X_B"], locals={"X": x, "B": b}
    )
    r_a_b = expand(r_x_b.subs(x, a**3))
    s_a_b = expand(s_x_b.subs(x, a**3))
    denominator = expand(a**2 * s_a_b)

    payload: dict[str, object] = {
        "experiment": "EXP-134",
        "attempt": "002-graph-first",
        "decision": "exact_worker_running",
        "selected_rows": rows,
        "anchor": anchor_point,
        "component_sizes": sizes,
        "largest_component": max(sizes),
        "graph_denominator": str(denominator),
        "excluded_fibres": "A*S(A^3,B)=0; these are outside the EXP-124 AS!=0 graph chart",
        "source_sha256": {
            str(path.relative_to(EXPERIMENTS)): digest(path)
            for path in (exp133.EXP123_RESULT, EXP124_CHECKPOINT, EXP124_WORKER)
        },
        "blocks": [],
    }
    persist(payload, CHECKPOINT)

    ratio_t0 = Rational(1)
    all_t_inert = True
    for index, component in enumerate(components, start=1):
        size = len(component)
        constant_part = (
            eye(size)
            + (a - anchor_point[0])
            * normalized[(0, 1)].extract(component, component)
            + (b - anchor_point[1])
            * normalized[(0, 5)].extract(component, component)
            - anchor_point[2] * normalized[(2, 9)].extract(component, component)
            + t * normalized[TARGET].extract(component, component)
        )
        cleared = (
            denominator * constant_part
            - r_a_b * normalized[(2, 9)].extract(component, component)
        )
        block_started = time.time()
        determinant = expand(cleared.det(method="domain-ge"))
        block_seconds = time.time() - block_started
        polynomial_t = Poly(determinant, t, domain=QQ.frac_field(a, b))
        t_inert = polynomial_t.degree() == 0
        all_t_inert = all_t_inert and t_inert
        ratio_t0 = cancel(ratio_t0 * determinant.subs(t, 0) / denominator**size)
        payload["blocks"].append(
            {
                "size": size,
                "vertices": component,
                "elapsed_seconds": block_seconds,
                "degree_T": polynomial_t.degree(),
                "T_inert": t_inert,
                "cleared_determinant": str(determinant),
            }
        )
        persist(payload, CHECKPOINT)
        print(
            f"[INFO] block {index}/{len(components)} size={size} "
            f"degree_T={polynomial_t.degree()} seconds={block_seconds:.2f}",
            flush=True,
        )
    require(all_t_inert, "every exact graph-first cyclic block is T-inert")

    c = symbols("C")
    expected_t0 = sympify(
        e124_worker["determinant_ratio"],
        locals={"A": a, "B": b, "C": c},
    )
    require(
        cancel(ratio_t0 - expected_t0) == 0,
        "graph-first T=0 ratio reproduces EXP-124 exactly",
    )

    anchor_determinant = anchor.det(method="domain-ge")
    direct_controls = []
    for a_value, b_value, t_value in ((1, 0, 1), (1, 1, 2), (2, 0, 1), (2, 1, 2)):
        r_value = r_a_b.subs({a: a_value, b: b_value})
        denominator_value = denominator.subs({a: a_value, b: b_value})
        require(denominator_value != 0, "direct graph control avoids A*S=0")
        c_value = cancel(-r_value / denominator_value)
        observed = direct_ratio(
            anchor_determinant,
            selected_base,
            directions,
            a_value,
            b_value,
            c_value,
            t_value,
        )
        expected = cancel(ratio_t0.subs({a: a_value, b: b_value}))
        require(observed == expected, "direct full determinant matches T-inert graph ratio")
        direct_controls.append(
            {
                "A": a_value,
                "B": b_value,
                "C": str(c_value),
                "T": t_value,
                "ratio": str(observed),
            }
        )

    payload.update(
        {
            "decision": "confirmed_exact_graph_T_inert",
            "elapsed_seconds": time.time() - started,
            "ratio_on_graph": str(ratio_t0),
            "direct_controls": direct_controls,
            "predictions": {
                "p1_largest_joint_SCC_at_most_45": max(sizes) <= MAX_CORE,
                "p2_graph_degree_T_zero": all_t_inert,
                "p3_positive_T_coefficients_zero_in_graph_quotient": all_t_inert,
                "p4_T0_reproduces_EXP124": True,
            },
            "scope": (
                "Exact T-inertness of the EXP-124 minor on the AS!=0 rational graph. "
                "Residual curves, finite base locus, transverse d=0, complete five-"
                "coefficient restriction, (72,108), floor, and JC(2) remain open."
            ),
        }
    )
    persist(payload, ARTIFACT)
    require(read_json(ARTIFACT)["decision"] == payload["decision"], "reloaded result artifact")
    print(f"[PASS] results SHA256 {digest(ARTIFACT)}", flush=True)


if __name__ == "__main__":
    main()
