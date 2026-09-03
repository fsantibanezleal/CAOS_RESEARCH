"""Independent lattice nonmembership and parity-certificate audit for EXP-049."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from flint import fmpz_mat


HERE = Path(__file__).resolve().parent
EXP047 = HERE.parent / "EXP-047-relative-kernel-smith"
RESULTS = HERE / "artifacts" / "results.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
EXPECTED_RUN_SHA256 = "83a6f0b248516aea77bd0af15c716eccb01ec1ad84260a75e21bb632986dc130"
EXPECTED_RESULTS_SHA256 = "567f554abaa1456133a4c0cd475d1848dad92a36dd8b9412381fe2fab9fc39b7"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def reverse_hnf_membership(
    columns: list[list[list[int]]], row_count: int, support: list[int]
) -> bool:
    transposed = fmpz_mat(len(columns), row_count)
    for new_row, entries in enumerate(reversed(columns)):
        for column, value in entries:
            transposed[new_row, int(column)] = int(value)
    hnf = transposed.hnf()
    residual = [2 if column in set(support) else 0 for column in range(row_count)]
    for row in range(hnf.nrows()):
        pivot = next((column for column in range(hnf.ncols()) if hnf[row, column]), None)
        if pivot is None:
            break
        quotient, remainder = divmod(residual[pivot], int(hnf[row, pivot]))
        if remainder:
            return False
        if quotient:
            for column in range(hnf.ncols()):
                residual[column] -= quotient * int(hnf[row, column])
    return not any(residual)


def parity(support: set[int], entries: list[list[int]]) -> int:
    return sum(int(row) in support for row, value in entries if int(value) & 1) & 1


def endpoint(value: int, tag: str, first: int, last: int) -> list[object]:
    left = value - first
    right = last - value
    return [tag, "L", left] if left <= right else [tag, "R", right]


def affine(value: int, p: int) -> list[int]:
    slope = min(range(25), key=lambda candidate: (abs(value - candidate * p), candidate))
    return [slope, value - slope * p]


def beta_row(p: int, u: int, offsets: list[int], product: int) -> dict[str, object]:
    return {
        "kind": "B",
        "product": affine(product, p),
        "l0_missing": [endpoint(u, "L0", 1, p)],
        "l1_missing": [
            endpoint(3 * p + offset, "L1", 3 * p, 4 * p - 2)
            for offset in sorted(offsets)
        ],
        "high_selected": [["H0", "L", 0], ["H2", "L", 0]],
    }


def sorted_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return sorted(rows, key=lambda row: json.dumps(row, sort_keys=True, separators=(",", ":")))


def beta_duals(p: int) -> list[list[dict[str, object]]]:
    v1 = [0, 1, p - 2]
    v2 = [0, 2, p - 2]
    first = [
        beta_row(p, p - 1, v1, 5 * p - 4),
        beta_row(p, p - 2, v1, 5 * p - 5),
    ]
    second = [
        beta_row(p, p - 1, v1, 5 * p - 4),
        beta_row(p, p - 2, v2, 5 * p - 4),
        beta_row(p, p - 2, v1, 5 * p - 5),
        beta_row(p, p - 3, v2, 5 * p - 5),
    ]
    return [sorted_rows(first), sorted_rows(second)]


def main() -> int:
    if sha256(HERE / "run.py") != EXPECTED_RUN_SHA256:
        raise AssertionError("run.py hash mismatch")
    if sha256(RESULTS) != EXPECTED_RESULTS_SHA256:
        raise AssertionError("results hash mismatch")
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, value: bool) -> None:
        checks.append({"name": name, "pass": bool(value)})

    stored_hash = results.pop("artifact_hash")
    check("results internal hash", digest(results) == stored_hash)
    results["artifact_hash"] = stored_hash
    check("results complete", results["status"] == "COMPLETE")
    check("declared parameter set", [row["p"] for row in results["rows"]] == [8, 9, 10, 11])
    check("P1 refuted", results["p1_status"] == "REFUTED")
    check("P2 refuted", results["p2_status"] == "REFUTED")
    check("P3 finite pass", results["p3_status"] == "PASS_FINITE")

    for row in results["rows"]:
        p = int(row["p"])
        for inclusion in row["inclusions"]:
            source = int(inclusion["source_mask"])
            target = int(inclusion["target_mask"])
            relative_path = EXP047 / "artifacts" / f"relative-p{p}-m{source}-m{target}.json"
            check(
                f"p={p} {source}->{target} relative hash",
                sha256(relative_path) == inclusion["relative_sha256"],
            )
            relative = json.loads(relative_path.read_text(encoding="utf-8"))
            columns = relative["matrix_columns"]
            for chain in inclusion["chains"]:
                chain_index = int(chain["chain_index"])
                check(
                    f"p={p} {source}->{target} chain {chain_index} hash",
                    digest(chain["chain_rows"]) == chain["chain_hash"],
                )
                check(
                    f"p={p} {source}->{target} chain {chain_index} reverse-HNF nonmembership",
                    not reverse_hnf_membership(
                        columns, int(inclusion["added_rows"]), chain["chain_rows"]
                    ),
                )
            chain_supports = [set(chain["chain_rows"]) for chain in inclusion["chains"]]
            for route in ("dual_low", "dual_high"):
                dual = inclusion[route]
                supports = [set(map(int, support)) for support in dual["supports"]]
                check(
                    f"p={p} {source}->{target} {route} annihilation",
                    all(
                        all(parity(support, entries) == 0 for entries in columns)
                        for support in supports
                    ),
                )
                pairings = [
                    [len(support & chain) & 1 for chain in chain_supports]
                    for support in supports
                ]
                check(
                    f"p={p} {source}->{target} {route} pairings",
                    pairings == [[1, 0], [0, 1]],
                )
                check(
                    f"p={p} {source}->{target} {route} bounded support",
                    max(map(len, supports)) <= 4,
                )
            if (source, target) == (58, 62):
                actual = [sorted_rows(rows) for rows in inclusion["dual_low"]["semantic_supports"]]
                check(f"p={p} beta dual formulas", actual == beta_duals(p))

    passed = sum(item["pass"] for item in checks)
    certificate = {
        "experiment": "EXP-049",
        "audit": "reverse-column HNF nonmembership and direct parity certificates",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checks_passed": passed,
        "checks_total": len(checks),
        "run_sha256": EXPECTED_RUN_SHA256,
        "results_sha256": EXPECTED_RESULTS_SHA256,
        "beta_dual_scope": "exact on p=8,...,11; conjectural as an all-parameter formula",
        "checks": checks,
    }
    certificate["artifact_hash"] = digest(certificate)
    write_json_atomic(OUTPUT, certificate)
    print(
        json.dumps(
            {
                key: certificate[key]
                for key in ("status", "checks_passed", "checks_total", "artifact_hash")
            },
            indent=2,
        )
    )
    return 0 if certificate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
