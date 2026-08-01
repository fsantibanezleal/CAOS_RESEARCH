"""EXP-130 row selection at the exact common quadratic fibres."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import Poly, QQ, primerange, sympify, symbols


HERE = Path(__file__).resolve().parent
SELECT_PATH = HERE / "select.py"
CRT_ARTIFACT = HERE / "artifacts" / "crt-worker.json"
CERTIFICATE = HERE / "artifacts" / "certificate.json"
FIRST_SELECTION = HERE / "artifacts" / "selection.json"
ARTIFACT = HERE / "artifacts" / "targeted-selection.json"
EXPECTED_CRT = "7189D6C9DBD6CF3E006B937A9DE1547A43155985BEF6716FE544F58A0EE65CB2"
EXPECTED_CERTIFICATE = "645CB57F9AB6BFA7120C5163388930322CE128E6FB324D22DD5B0364F0CEF39D"
EXPECTED_FIRST_SELECTION = "77FFCD863B06141C8E95108D130869227D4D7532B4470B58ABB5A9CED959C418"
PRIMES_PER_BLOCK = 2
TOTAL_GATE_SECONDS = 180

spec = importlib.util.spec_from_file_location("select_exp130_target", SELECT_PATH)
sel = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(sel)


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


def main() -> None:
    started = time.time()
    require(sha256(CRT_ARTIFACT) == EXPECTED_CRT, "CRT artifact hash matches")
    require(sha256(CERTIFICATE) == EXPECTED_CERTIFICATE, "quadratic certificate hash matches")
    require(sha256(FIRST_SELECTION) == EXPECTED_FIRST_SELECTION, "first selection hash matches")
    crt = json.loads(CRT_ARTIFACT.read_text(encoding="utf-8"))
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    first_selection = json.loads(FIRST_SELECTION.read_text(encoding="utf-8"))
    x, b, y = symbols("X B Y")
    block_by_degree = {int(item["degree"]): item for item in crt["blocks"]}
    blocks = []
    for item in certificate["new_block_certificates"]:
        degree = int(item["degree"])
        source = block_by_degree[degree]
        blocks.append(
            {
                "degree": degree,
                "factor": Poly(
                    sympify(source["B_factor"], locals={"B": b}), b, domain=QQ
                ).monic(),
                "X_class": sympify(
                    source["X_class_mod_B_factor"], locals={"B": b}
                ),
                "common_quadratic": sympify(
                    item["certificate"]["common_gcd_K_Y"],
                    locals={"B": b, "Y": y},
                ),
            }
        )
    require([item["degree"] for item in blocks] == [3, 6], "targeted blocks are degrees 3 and 6")

    base, directions = sel.exp125.exp124.build_full_system()
    matrices_by_prime = {}
    probes = []
    rank_defects = []
    accepted_primes = {3: set(), 6: set()}
    for prime in primerange(127, 10000):
        if all(len(values) >= PRIMES_PER_BLOCK for values in accepted_primes.values()):
            break
        matrices = None
        for block in blocks:
            degree = block["degree"]
            if len(accepted_primes[degree]) >= PRIMES_PER_BLOCK:
                continue
            accepted_points = []
            roots_b = [
                value
                for value in range(prime)
                if sel.eval_mod(block["factor"].as_expr(), (b,), (value,), prime)
                == 0
            ]
            for b_value in roots_b:
                x_value = sel.eval_mod(block["X_class"], (b,), (b_value,), prime)
                roots_a = [
                    value
                    for value in range(1, prime)
                    if pow(value, 3, prime) == x_value
                ]
                if not roots_a:
                    continue
                roots_y = [
                    value
                    for value in range(prime)
                    if sel.eval_mod(
                        block["common_quadratic"],
                        (b, y),
                        (b_value, value),
                        prime,
                    )
                    == 0
                ]
                for y_value in roots_y:
                    accepted_points.append(
                        (roots_a[0], b_value, x_value, y_value)
                    )
            if not accepted_points:
                continue
            if matrices is None:
                matrices = {
                    "base": sel.exp125.exp124.exp115.matrix_mod(base, prime),
                    "A": sel.exp125.exp124.exp115.matrix_mod(
                        directions[(0, 1)], prime
                    ),
                    "B": sel.exp125.exp124.exp115.matrix_mod(
                        directions[(0, 5)], prime
                    ),
                    "C": sel.exp125.exp124.exp115.matrix_mod(
                        directions[sel.exp125.exp124.TARGET], prime
                    ),
                }
                matrices_by_prime[prime] = matrices
            full_rank_on_prime = False
            for a_value, b_value, x_value, y_value in accepted_points[:2]:
                c_value = y_value * pow(a_value * a_value, -1, prime) % prime
                evaluated = sel.evaluated_matrix(
                    matrices, a_value, b_value, c_value, prime
                )
                rows = sel.exp125.independent_row_basis_fast(evaluated, prime)
                record = {
                    "degree": degree,
                    "prime": prime,
                    "A": a_value,
                    "B": b_value,
                    "C": c_value,
                    "X": x_value,
                    "Y": y_value,
                    "rank": len(rows),
                    "row_basis": rows,
                }
                if len(rows) == 125:
                    probes.append(record)
                    full_rank_on_prime = True
                    print(
                        f"[PASS] degree-{degree} common-quadratic root has "
                        f"full rank at p={prime}",
                        flush=True,
                    )
                else:
                    rank_defects.append(record)
                    print(
                        f"[INFO] degree-{degree} rank={len(rows)} at p={prime}",
                        flush=True,
                    )
            if full_rank_on_prime:
                accepted_primes[degree].add(prime)

    require(
        all(len(values) >= PRIMES_PER_BLOCK for values in accepted_primes.values()),
        "two full-rank common-quadratic primes found for each block",
    )
    existing = {
        *(tuple(item["row_basis"]) for item in first_selection["probes"]),
        *(tuple(item["rows"]) for item in first_selection["selected_atlas"]),
    }
    candidates = []
    for probe in probes:
        rows = probe["row_basis"]
        if tuple(rows) in existing or any(item["rows"] == rows for item in candidates):
            continue
        coverage = []
        for target in probes:
            evaluated = sel.evaluated_matrix(
                matrices_by_prime[target["prime"]],
                target["A"],
                target["B"],
                target["C"],
                target["prime"],
            )
            coverage.append(
                {
                    "degree": target["degree"],
                    "prime": target["prime"],
                    "nonzero": sel.exp125.determinant_mod_fast(
                        evaluated, rows, target["prime"]
                    )
                    != 0,
                }
            )
        candidates.append(
            {
                "rows": rows,
                "source_degree": probe["degree"],
                "coverage": coverage,
            }
        )
    require(bool(candidates), "new targeted row bases were found")
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
            index
            for index in uncovered
            if best["coverage"][index]["nonzero"]
        }
        require(bool(newly_covered), "targeted atlas advances probe coverage")
        atlas.append(best)
        uncovered -= newly_covered
    require(time.time() - started <= TOTAL_GATE_SECONDS, "targeted selection remains within budget")
    payload = {
        "experiment": "EXP-130-targeted-selection",
        "source_hashes": {
            "crt": EXPECTED_CRT,
            "certificate": EXPECTED_CERTIFICATE,
            "first_selection": EXPECTED_FIRST_SELECTION,
        },
        "blocks": [
            {
                "degree": item["degree"],
                "factor": str(item["factor"].as_expr()),
                "X_class": str(item["X_class"]),
                "common_quadratic": str(item["common_quadratic"]),
            }
            for item in blocks
        ],
        "accepted_primes": {
            str(degree): sorted(values)
            for degree, values in accepted_primes.items()
        },
        "probes": probes,
        "rank_defects": rank_defects,
        "candidate_count": len(candidates),
        "atlas_size": len(atlas),
        "selected_atlas": atlas,
        "single_basis_found": any(
            all(test["nonzero"] for test in item["coverage"])
            for item in candidates
        ),
        "scope": (
            "Modular selection only at the exact common quadratic fibres. "
            "Characteristic-zero reconstruction remains required."
        ),
    }
    persist(payload)
    print(f"[PASS] targeted selection SHA256 {sha256(ARTIFACT)}", flush=True)
    print(
        f"[INFO] candidates={len(candidates)} atlas_size={len(atlas)} "
        f"rank_defects={len(rank_defects)}",
        flush=True,
    )


if __name__ == "__main__":
    main()

