"""Select a common-quadratic row basis by exact SCC cost before reconstruction."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET_SELECT_PATH = HERE / "targeted_select.py"
TARGET_SELECTION = HERE / "artifacts" / "targeted-selection.json"
FIRST_SELECTION = HERE / "artifacts" / "selection.json"
ARTIFACT = HERE / "artifacts" / "structural-selection.json"
ROOT = HERE.parent
EXPECTED_TARGET = "605B8E29E9694D7249C69E5E1C92680D349E503D37725F105A6F3EDF95AD129C"
TOTAL_GATE_SECONDS = 240

spec = importlib.util.spec_from_file_location("target_exp130_struct", TARGET_SELECT_PATH)
target = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(target)


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


def ordered_basis(matrix, order, prime):
    permuted = [matrix[index] for index in order]
    selected = target.sel.exp125.independent_row_basis_fast(permuted, prime)
    return [order[index] for index in selected]


def main() -> None:
    started = time.time()
    require(sha256(TARGET_SELECTION) == EXPECTED_TARGET, "targeted selection hash matches")
    selection = json.loads(TARGET_SELECTION.read_text(encoding="utf-8"))
    first = json.loads(FIRST_SELECTION.read_text(encoding="utf-8"))
    e123 = json.loads(
        (ROOT / "EXP-123-direction-29-symbolic-lift" / "artifacts" / "results.json").read_text(
            encoding="utf-8"
        )
    )
    e124 = json.loads(
        (ROOT / "EXP-124-rational-graph-alternative-chart" / "artifacts" / "results.json").read_text(
            encoding="utf-8"
        )
    )
    e125 = json.loads(
        (ROOT / "EXP-125-factor-curve-recursion" / "artifacts" / "results.json").read_text(
            encoding="utf-8"
        )
    )
    e127 = json.loads(
        (ROOT / "EXP-127-f7-divisor-norm" / "artifacts" / "results.json").read_text(
            encoding="utf-8"
        )
    )
    e129 = json.loads(
        (ROOT / "EXP-129-f7-crt-minor-atlas" / "artifacts" / "results.json").read_text(
            encoding="utf-8"
        )
    )
    preferred = [
        ("EXP-123-shared", e123["shared_rows"]),
        ("EXP-124-N", e124["selected_rows"]),
    ]
    preferred.extend(
        (f"EXP-125-{name}", rows)
        for name, rows in e125["selected_rows"].items()
    )
    preferred.append(("EXP-127-h7", e127["selected_rows"]))
    preferred.extend(
        (f"EXP-129-atlas-{item['atlas_index']}", item["rows"])
        for item in e129["exact_atlas"]
    )
    preferred.extend(
        [
            ("EXP-130-first-new", first["selected_atlas"][0]["rows"]),
            ("EXP-130-targeted-default", selection["selected_atlas"][0]["rows"]),
        ]
    )

    base, directions = target.sel.exp125.exp124.build_full_system()
    matrices_by_prime = {}
    evaluated_probes = []
    for probe in selection["probes"]:
        prime = int(probe["prime"])
        if prime not in matrices_by_prime:
            matrices_by_prime[prime] = {
                "base": target.sel.exp125.exp124.exp115.matrix_mod(base, prime),
                "A": target.sel.exp125.exp124.exp115.matrix_mod(
                    directions[(0, 1)], prime
                ),
                "B": target.sel.exp125.exp124.exp115.matrix_mod(
                    directions[(0, 5)], prime
                ),
                "C": target.sel.exp125.exp124.exp115.matrix_mod(
                    directions[target.sel.exp125.exp124.TARGET], prime
                ),
            }
        matrix = target.sel.evaluated_matrix(
            matrices_by_prime[prime],
            probe["A"],
            probe["B"],
            probe["C"],
            prime,
        )
        evaluated_probes.append((probe, matrix))

    modular_candidates = []
    seen = set()
    for name, priority_rows in preferred:
        order = list(dict.fromkeys([*priority_rows, *range(302)]))
        rows = ordered_basis(evaluated_probes[0][1], order, evaluated_probes[0][0]["prime"])
        if len(rows) != 125 or tuple(rows) in seen:
            continue
        seen.add(tuple(rows))
        coverage = []
        for probe, matrix in evaluated_probes:
            coverage.append(
                target.sel.exp125.determinant_mod_fast(
                    matrix, rows, probe["prime"]
                )
                != 0
            )
        if all(coverage):
            modular_candidates.append(
                {
                    "source": name,
                    "rows": rows,
                    "replacements_from_source": len(set(rows) - set(priority_rows)),
                }
            )
    require(bool(modular_candidates), "at least one prioritized basis covers all targeted probes")

    exact_candidates = []
    for candidate in modular_candidates:
        if time.time() - started > TOTAL_GATE_SECONDS:
            break
        (
            _,
            _,
            _,
            anchor_det,
            _,
            components,
            anchor_point,
            anchor_attempts,
        ) = target.sel.exp125.exact_profile(base, directions, candidate["rows"])
        exact_candidates.append(
            {
                **candidate,
                "largest_SCC": len(components[0]),
                "cyclic_component_sizes": [len(item) for item in components],
                "anchor": {
                    "point": list(anchor_point),
                    "determinant": str(anchor_det),
                    "attempts": anchor_attempts,
                },
            }
        )
        print(
            f"[INFO] {candidate['source']} replacements="
            f"{candidate['replacements_from_source']} largest_SCC={len(components[0])}",
            flush=True,
        )
    require(bool(exact_candidates), "exact SCC profiles completed within budget")
    selected = min(
        exact_candidates,
        key=lambda item: (
            item["largest_SCC"],
            item["replacements_from_source"],
            item["rows"],
        ),
    )
    require(time.time() - started <= TOTAL_GATE_SECONDS, "structural selection remains within budget")
    payload = {
        "experiment": "EXP-130-structural-selection",
        "targeted_selection_sha256": EXPECTED_TARGET,
        "modular_candidate_count": len(modular_candidates),
        "exact_candidate_count": len(exact_candidates),
        "candidates": exact_candidates,
        "selected": selected,
        "decision": "minimum_exact_SCC_before_reconstruction",
    }
    persist(payload)
    print(f"[PASS] structural selection SHA256 {sha256(ARTIFACT)}", flush=True)
    print(
        f"[INFO] selected={selected['source']} largest_SCC={selected['largest_SCC']}",
        flush=True,
    )


if __name__ == "__main__":
    main()
