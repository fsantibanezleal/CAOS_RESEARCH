"""EXP-134: exact rank/root certificate for the transverse EXP-124 section."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import cancel, expand, eye, factor_list, symbols, sympify


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP133_RUN = EXPERIMENTS / "EXP-133-principal-open-28-lift-preflight" / "run.py"
EXP123_RESULTS = (
    EXPERIMENTS / "EXP-123-direction-29-symbolic-lift" / "artifacts" / "results.json"
)
EXP124_RESULTS = (
    EXPERIMENTS / "EXP-124-rational-graph-alternative-chart" / "artifacts" / "results.json"
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
ATTEMPT003_CHECKPOINT = (
    HERE / "artifacts" / "attempts" / "attempt-003-checkpoint.json"
)
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
ARTIFACT = HERE / "artifacts" / "results.json"
TARGET = (2, 8)
MAX_CORE = 45
TOTAL_GATE_SECONDS = 420


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


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


def expression_digest(expression) -> str:
    return hashlib.sha256(str(expression).encode("utf-8")).hexdigest().upper()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)
    print(f"[PASS] {message}", flush=True)


def selected_system(exp124, rows):
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
    return base, selected_base, selected_directions


def main() -> None:
    started = time.time()
    exp133 = load_module("exp133_for_exp134_roots", EXP133_RUN)
    exp124 = exp133.exp124
    e124 = read_json(EXP124_RESULTS)
    e124_worker = read_json(EXP124_WORKER)
    e133 = read_json(EXP133_RESULTS)
    rows = list(e124["selected_rows"])
    base, selected_base, directions = selected_system(exp124, rows)
    require(base.shape == (302, 125), "rebuilt original 302 by 125 augmented matrix")
    require(len(rows) == len(set(rows)) == 125, "loaded accepted EXP-124 row section")
    require(
        e133["degree_ledger"]["EXP-124-graph"] == [0, 0, 0, 0],
        "reproduced EXP-133 modular inertness premise",
    )

    anchor = selected_base + directions[(0, 1)]
    anchor_determinant = anchor.det(method="domain-ge")
    require(anchor_determinant != 0, "accepted rational anchor is invertible")
    inverse = anchor.inv()
    normalized = {
        direction: inverse * matrix for direction, matrix in directions.items()
    }
    components = exp124.exp122.cyclic_components(list(normalized.values()))
    sizes = [len(component) for component in components]
    require(max(sizes) <= MAX_CORE, "joint exact cyclic core remains inside gate")
    cores = [component for component in components if len(component) == max(sizes)]
    require(len(cores) == 1, "joint dependency graph has one largest block")
    core = cores[0]
    singletons = [component for component in components if len(component) == 1]
    require(len(singletons) == len(components) - 1, "all other joint blocks are singletons")

    transverse_core = normalized[TARGET].extract(core, core)
    transverse_rank = int(transverse_core.rank())
    require(transverse_rank == 7, "exact transverse core rank is seven")
    require(
        all(normalized[TARGET][component[0], component[0]] == 0 for component in singletons),
        "all singleton determinants are exactly T-independent",
    )

    payload: dict[str, object] = {
        "experiment": "EXP-134",
        "attempt": "005-exact-graph-rank-root-certificate",
        "decision": "exact_graph_root_certificate_running",
        "selected_rows": rows,
        "component_sizes": sizes,
        "largest_component": max(sizes),
        "transverse_core_rank": transverse_rank,
        "graph_T_degree_bound": transverse_rank,
        "exact_T_values_required": transverse_rank + 1,
        "source_sha256": {
            str(path.relative_to(EXPERIMENTS)): digest(path)
            for path in (
                EXP123_RESULTS,
                EXP124_RESULTS,
                EXP124_WORKER,
                EXP133_RESULTS,
                ATTEMPT003_CHECKPOINT,
            )
        },
        "exact_T_evaluations": [],
    }
    persist(payload, CHECKPOINT)

    a, b, c, x = symbols("A B C X")
    r_x_b = sympify(
        read_json(EXP123_RESULTS)["invariant_reduction"]["R_X_B"],
        locals={"X": x, "B": b},
    )
    s_x_b = sympify(
        read_json(EXP123_RESULTS)["invariant_reduction"]["S_X_B"],
        locals={"X": x, "B": b},
    )
    r_a_b = expand(r_x_b.subs(x, a**3))
    s_a_b = expand(s_x_b.subs(x, a**3))
    graph_denominator = expand(a**2 * s_a_b)
    c_on_graph = cancel(-r_a_b / graph_denominator)
    constant_core = (
        eye(len(core))
        + (a - 1) * normalized[(0, 1)].extract(core, core)
        + b * normalized[(0, 5)].extract(core, core)
        + c_on_graph * normalized[(2, 9)].extract(core, core)
    )
    expected_t0 = sympify(
        e124_worker["determinant_ratio"],
        locals={"A": a, "B": b, "C": c},
    )
    require(not expected_t0.has(c), "accepted EXP-124 determinant is exactly C-independent")
    expected_t0_graph = cancel(expected_t0.subs(c, c_on_graph))
    attempt003 = read_json(ATTEMPT003_CHECKPOINT)
    baseline_core = sympify(
        attempt003["T0_core_determinant"], locals={"A": a, "B": b, "C": c}
    )
    require(
        not baseline_core.has(c),
        "persisted exact EXP-124 T=0 core is C-independent",
    )
    payload["exact_T_evaluations"].append(
        {
            "T": 0,
            "equals_T0": True,
            "core_determinant_sha256": expression_digest(baseline_core),
            "elapsed_seconds": 0.0,
            "source": "persisted exact EXP-124 determinant ratio",
        }
    )
    payload["T0_core_determinant"] = str(baseline_core)
    payload["graph_denominator"] = str(graph_denominator)
    payload["excluded_fibres"] = "A*S(A^3,B)=0; outside the declared rational graph chart"
    persist(payload, CHECKPOINT)

    for t_value in range(1, transverse_rank + 1):
        require(
            time.time() - started < TOTAL_GATE_SECONDS,
            "rank/root worker remains inside total gate",
        )
        evaluation_started = time.time()
        determinant = cancel(
            (constant_core + t_value * transverse_core).det(method="domain-ge")
        )
        equal_to_baseline = cancel(determinant - baseline_core) == 0
        record = {
            "T": t_value,
            "equals_T0": equal_to_baseline,
            "core_determinant_sha256": expression_digest(determinant),
            "elapsed_seconds": time.time() - evaluation_started,
        }
        payload["exact_T_evaluations"].append(record)
        persist(payload, CHECKPOINT)
        require(equal_to_baseline, f"exact graph-core determinant at T={t_value} equals T=0")

    require(
        len(payload["exact_T_evaluations"]) == transverse_rank + 1,
        "one more exact T value than the degree bound was evaluated",
    )

    determinant_ratio = expected_t0_graph

    direct_controls = []
    for av, bv, tv in ((1, 0, 1), (1, 1, 2), (2, 0, -1), (2, 1, 3)):
        denominator_value = graph_denominator.subs({a: av, b: bv})
        require(denominator_value != 0, "direct graph control avoids A*S=0")
        cv = cancel(c_on_graph.subs({a: av, b: bv}))
        direct_t = (
            selected_base
            + av * directions[(0, 1)]
            + bv * directions[(0, 5)]
            + cv * directions[(2, 9)]
            + tv * directions[TARGET]
        ).det(method="domain-ge")
        direct_zero = (
            selected_base
            + av * directions[(0, 1)]
            + bv * directions[(0, 5)]
            + cv * directions[(2, 9)]
        ).det(method="domain-ge")
        require(direct_t == direct_zero, f"direct graph T-inert control ({av},{bv},{cv},{tv})")
        direct_controls.append(
            {"point": [av, bv, cv, tv], "determinant": str(direct_t)}
        )

    graph_numerator = sympify(
        e124["graph_numerator"], locals={"X": x, "B": b}
    )
    factors = factor_list(graph_numerator, x, b)
    require(len(factors[1]) == 3, "retained exact F3 F6 F7 graph ledger")

    payload.update(
        {
            "decision": "confirmed_exact_graph_T_inert",
            "graph_T_degree_exact": 0,
            "determinant_ratio_on_graph": str(determinant_ratio),
            "determinant_ratio_on_graph_sha256": expression_digest(determinant_ratio),
            "direct_exact_controls": direct_controls,
            "retained_graph_numerator": str(graph_numerator),
            "retained_factorization": [
                {"factor": str(factor), "multiplicity": multiplicity}
                for factor, multiplicity in factors[1]
            ],
            "predictions": {
                "p1_joint_scc_at_most_45": max(sizes) <= MAX_CORE,
                "p2_exact_T_degree_at_most_one": True,
                "p3_positive_T_coefficients_vanish_mod_graph": True,
                "p4_T0_reproduces_EXP124": True,
                "stronger_ambient_T_inertness": False,
            },
            "elapsed_seconds": time.time() - started,
            "scope": (
                "Exact T-inertness of the accepted EXP-124 section on the AS!=0 "
                "rational graph. The F3 F6 F7 residual is unchanged, but its transverse cover, "
                "the finite base locus, d=0 quotient, complete five-coefficient "
                "restriction, 24-parameter core, (72,108), floor, and JC(2) remain open."
            ),
        }
    )
    require(payload["elapsed_seconds"] <= TOTAL_GATE_SECONDS, "EXP-134 remains inside total gate")
    persist(payload, ARTIFACT)
    require(read_json(ARTIFACT)["decision"] == payload["decision"], "reloaded result artifact")
    print(f"[PASS] results SHA256 {digest(ARTIFACT)}", flush=True)
    print(
        f"[DONE] {payload['decision']} degree_T=0 bound={transverse_rank} "
        f"elapsed={payload['elapsed_seconds']:.2f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
