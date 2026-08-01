"""EXP-134 attempt 003: graph determinant over QQ(A,B)[T]."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import Poly, QQ, Rational, cancel, eye, symbols, sympify
from sympy.polys.matrices import DomainMatrix


HERE = Path(__file__).resolve().parent
GRAPH_WORKER = HERE / "graph_worker.py"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
ARTIFACT = HERE / "artifacts" / "results.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


graph_worker = load_module("exp134_graph_support", GRAPH_WORKER)
exp133 = graph_worker.exp133
exp124 = graph_worker.exp124


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
    e123 = graph_worker.read_json(exp133.EXP123_RESULT)
    e124_worker = graph_worker.read_json(graph_worker.EXP124_WORKER)
    rows, anchor_point, anchor, selected_base, directions = graph_worker.selected_system()
    inverse = anchor.inv()
    normalized = {direction: inverse * matrix for direction, matrix in directions.items()}
    components = exp124.exp122.cyclic_components(list(normalized.values()))
    sizes = [len(component) for component in components]
    require(max(sizes) <= 45, "joint exact cyclic core within gate")
    largest_component = max(components, key=len)
    transverse_core_rank = normalized[(2, 8)].extract(
        largest_component, largest_component
    ).rank()
    require(transverse_core_rank == 7, "exact transverse core rank is seven")

    a, b, c, t, x = symbols("A B C T X")
    r_x_b = sympify(
        e123["invariant_reduction"]["R_X_B"], locals={"X": x, "B": b}
    )
    s_x_b = sympify(
        e123["invariant_reduction"]["S_X_B"], locals={"X": x, "B": b}
    )
    r_a_b = r_x_b.subs(x, a**3)
    denominator = a**2 * s_x_b.subs(x, a**3)
    c_graph = cancel(-r_a_b / denominator)
    coefficient_field = QQ.frac_field(a, b)
    polynomial_ring = coefficient_field.poly_ring(t)

    payload: dict[str, object] = {
        "experiment": "EXP-134",
        "attempt": "003-fraction-field",
        "decision": "exact_worker_running",
        "selected_rows": rows,
        "anchor": anchor_point,
        "component_sizes": sizes,
        "largest_component": max(sizes),
        "coefficient_domain": "QQ(A,B)[T]",
        "graph_substitution": str(c_graph),
        "excluded_fibres": "A*S(A^3,B)=0; outside the EXP-124 AS!=0 graph chart",
        "ambient_structural_degree_bound_T": transverse_core_rank,
        "blocks": [],
    }
    persist(payload, CHECKPOINT)

    ratio = Rational(1)
    all_inert = True
    for index, component in enumerate(components, start=1):
        size = len(component)
        block = (
            eye(size)
            + (a - anchor_point[0])
            * normalized[(0, 1)].extract(component, component)
            + (b - anchor_point[1])
            * normalized[(0, 5)].extract(component, component)
            + (c_graph - anchor_point[2])
            * normalized[(2, 9)].extract(component, component)
            + t * normalized[(2, 8)].extract(component, component)
        )
        block_started = time.time()
        domain_rows = [
            [polynomial_ring.from_sympy(entry) for entry in row]
            for row in block.tolist()
        ]
        determinant = DomainMatrix.from_list(domain_rows, polynomial_ring).det().as_expr()
        degree_t = int(Poly(determinant, t, domain=coefficient_field).degree())
        block_seconds = time.time() - block_started
        all_inert = all_inert and degree_t == 0
        ratio = cancel(ratio * determinant)
        payload["blocks"].append(
            {
                "size": size,
                "vertices": component,
                "elapsed_seconds": block_seconds,
                "degree_T": degree_t,
                "determinant": str(determinant),
            }
        )
        persist(payload, CHECKPOINT)
        print(
            f"[INFO] block {index}/{len(components)} size={size} "
            f"degree_T={degree_t} seconds={block_seconds:.2f}",
            flush=True,
        )
    require(all_inert, "every exact QQ(A,B)[T] block is T-inert")

    expected = sympify(
        e124_worker["determinant_ratio"],
        locals={"A": a, "B": b, "C": c},
    )
    require(cancel(ratio - expected) == 0, "T=0 ratio reproduces EXP-124 exactly")

    anchor_determinant = anchor.det(method="domain-ge")
    controls = []
    for av, bv, tv in ((1, 0, 1), (1, 1, 2), (2, 0, 1), (2, 1, 2)):
        denominator_value = denominator.subs({a: av, b: bv})
        require(denominator_value != 0, "direct control avoids A*S=0")
        cv = cancel(c_graph.subs({a: av, b: bv}))
        observed = graph_worker.direct_ratio(
            anchor_determinant,
            selected_base,
            directions,
            av,
            bv,
            cv,
            tv,
        )
        expected_value = cancel(ratio.subs({a: av, b: bv}))
        require(observed == expected_value, "direct full determinant matches graph ratio")
        controls.append(
            {"A": av, "B": bv, "C": str(cv), "T": tv, "ratio": str(observed)}
        )

    payload.update(
        {
            "decision": "confirmed_exact_graph_T_inert",
            "elapsed_seconds": time.time() - started,
            "ratio_on_graph": str(ratio),
            "direct_controls": controls,
            "predictions": {
                "p1_largest_joint_SCC_at_most_45": max(sizes) <= 45,
                "p2_graph_degree_T_zero": all_inert,
                "p3_positive_T_coefficients_zero_in_graph_quotient": all_inert,
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
    require(
        graph_worker.read_json(ARTIFACT)["decision"] == payload["decision"],
        "reloaded result",
    )
    print(f"[PASS] results SHA256 {digest(ARTIFACT)}", flush=True)


if __name__ == "__main__":
    main()
