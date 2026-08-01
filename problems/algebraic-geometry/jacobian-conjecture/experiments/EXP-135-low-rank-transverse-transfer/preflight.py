"""EXP-135 exact rational-control preflight for the rank-seven transfer."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

from sympy import Poly, cancel, eye, symbols, sympify


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP134_RUN = EXPERIMENTS / "EXP-134-exact-transverse-graph-section" / "run.py"
EXP123_RESULTS = (
    EXPERIMENTS / "EXP-123-direction-29-symbolic-lift" / "artifacts" / "results.json"
)
EXP124_RESULTS = (
    EXPERIMENTS / "EXP-124-rational-graph-alternative-chart" / "artifacts" / "results.json"
)
EXP133_RESULTS = (
    EXPERIMENTS / "EXP-133-principal-open-28-lift-preflight" / "artifacts" / "results.json"
)
EXP134_TERMINAL = (
    EXPERIMENTS
    / "EXP-134-exact-transverse-graph-section"
    / "artifacts"
    / "attempts"
    / "attempt-005-checkpoint.json"
)
ARTIFACT = HERE / "artifacts" / "preflight.json"
TARGET = (2, 8)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


exp134 = load_module("exp134_for_exp135", EXP134_RUN)
exp133 = load_module("exp133_for_exp135", exp134.EXP133_RUN)
exp124 = exp133.exp124


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)
    print(f"[PASS] {message}", flush=True)


def nilpotency_index(matrix) -> int | None:
    power = matrix
    for index in range(1, matrix.rows + 1):
        if power.is_zero_matrix:
            return index
        power = power * matrix
    return None


def main() -> None:
    e123 = read_json(EXP123_RESULTS)
    e124 = read_json(EXP124_RESULTS)
    rows = list(e124["selected_rows"])
    _, selected_base, directions = exp134.selected_system(exp124, rows)
    anchor = selected_base + directions[(0, 1)]
    inverse = anchor.inv()
    normalized = {direction: inverse * matrix for direction, matrix in directions.items()}
    components = exp124.exp122.cyclic_components(list(normalized.values()))
    core = max(components, key=len)
    require(len(core) == 33, "reproduced unique size-33 joint core")

    transverse = normalized[TARGET].extract(core, core)
    _, pivot_columns = transverse.rref()
    require(len(pivot_columns) == 7, "transverse core has exact rank seven")
    u = transverse[:, list(pivot_columns)]
    _, pivot_rows = u.T.rref()
    pivot_rows = list(pivot_rows)
    require(len(pivot_rows) == 7, "rank factor has seven independent rows")
    u_pivot = u.extract(pivot_rows, range(7))
    v_transpose = u_pivot.inv() * transverse.extract(pivot_rows, range(33))
    require(u * v_transpose == transverse, "verified exact K_T=U V^T factorization")

    a, b, x, t = symbols("A B X T")
    r_x_b = sympify(
        e123["invariant_reduction"]["R_X_B"], locals={"X": x, "B": b}
    )
    s_x_b = sympify(
        e123["invariant_reduction"]["S_X_B"], locals={"X": x, "B": b}
    )
    controls = []
    for av, bv in ((1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)):
        r_value = r_x_b.subs({x: av**3, b: bv})
        s_value = s_x_b.subs({x: av**3, b: bv})
        denominator = av**2 * s_value
        if denominator == 0:
            continue
        cv = cancel(-r_value / denominator)
        h0 = (
            eye(33)
            + (av - 1) * normalized[(0, 1)].extract(core, core)
            + bv * normalized[(0, 5)].extract(core, core)
            + cv * normalized[(2, 9)].extract(core, core)
        )
        if h0.det(method="domain-ge") == 0:
            continue
        transfer = v_transpose * h0.inv() * u
        polynomial = Poly((eye(7) + t * transfer).det(method="domain-ge"), t)
        inert = polynomial.as_expr() == 1
        require(inert, f"exact transfer determinant is one at A={av}, B={bv}")
        controls.append(
            {
                "A": av,
                "B": bv,
                "C": str(cv),
                "transfer_rank": int(transfer.rank()),
                "nilpotency_index": nilpotency_index(transfer),
                "det_I_plus_T_transfer": str(polynomial.as_expr()),
                "transfer_matrix": [[str(entry) for entry in row] for row in transfer.tolist()],
            }
        )
        if len(controls) == 4:
            break
    require(len(controls) == 4, "completed four exact rational graph controls")

    payload = {
        "experiment": "EXP-135",
        "decision": "confirmed_exact_rational_control_preflight",
        "core_size": len(core),
        "transverse_rank": len(pivot_columns),
        "pivot_columns": list(pivot_columns),
        "pivot_rows": pivot_rows,
        "controls": controls,
        "source_sha256": {
            str(path.relative_to(EXPERIMENTS)): digest(path)
            for path in (
                EXP123_RESULTS,
                EXP124_RESULTS,
                EXP133_RESULTS,
                EXP134_TERMINAL,
            )
        },
        "scope": (
            "Exact low-rank factorization and four rational graph controls only. "
            "No global graph identity, residual cover, five-coefficient closure, "
            "(72,108), floor, or JC(2) result."
        ),
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    require(read_json(ARTIFACT)["decision"] == payload["decision"], "reloaded preflight")
    print(f"[PASS] preflight SHA256 {digest(ARTIFACT)}", flush=True)


if __name__ == "__main__":
    main()
