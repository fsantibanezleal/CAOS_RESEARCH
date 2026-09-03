"""Independent formula and rank audit for EXP-048."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXP047 = HERE.parent / "EXP-047-relative-kernel-smith"
RESULTS = HERE / "artifacts" / "results.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
EXPECTED_RUN_SHA256 = "ec245859931cf1b3992630c8faab207a158ae5b72a3283783ec938cd3b76e70a"
EXPECTED_RESULTS_SHA256 = "ba44eae4c9193bc941411b059dc7a7d7a4c69dff3d818e05d3395338e125a400"
EXPECTED_EXP047_SHA256 = "f78d251ae1746a88d1190756572aa251b9daf70ceb103cef9765c6d73b26f46c"


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


def endpoint(value: int, tag: str, first: int, last: int) -> list[object]:
    left = value - first
    right = last - value
    return [tag, "L", left] if left <= right else [tag, "R", right]


def affine(value: int, p: int) -> list[int]:
    slope = min(range(25), key=lambda candidate: (abs(value - candidate * p), candidate))
    return [slope, value - slope * p]


def row_token(
    *, p: int, kind: str, product: int, l0_missing: list[int], l1_offsets: list[int]
) -> dict[str, object]:
    return {
        "kind": kind,
        "product": affine(product, p),
        "l0_missing": [endpoint(value, "L0", 1, p) for value in sorted(l0_missing)],
        "l1_missing": [
            endpoint(3 * p + offset, "L1", 3 * p, 4 * p - 2)
            for offset in sorted(l1_offsets)
        ],
        "high_selected": [["H0", "L", 0], ["H2", "L", 0]],
    }


def sorted_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return sorted(rows, key=lambda row: json.dumps(row, sort_keys=True, separators=(",", ":")))


def alpha(p: int, j: int) -> list[dict[str, object]]:
    """Observed completion chain for the R0 atom, j=1,2."""

    center = p - 1 - j
    return sorted_rows(
        [
            row_token(
                p=p,
                kind="A",
                product=p + w - 3,
                l0_missing=[center, w],
                l1_offsets=[0, j],
            )
            for w in range(4, p + 1)
            if w != center
        ]
    )


def beta(p: int, j: int) -> list[dict[str, object]]:
    """Observed completion chains for the R2 atom, j=1,2."""

    if j == 1:
        rows = [
            row_token(
                p=p,
                kind="B",
                product=4 * p + v + branch - 4,
                l0_missing=[p - 2],
                l1_offsets=[0, branch, v],
            )
            for branch in (1, 2)
            for v in range(3, p - 1)
        ]
    elif j == 2:
        rows = [
            row_token(
                p=p,
                kind="B",
                product=4 * p + v - 3,
                l0_missing=[p - 3],
                l1_offsets=[0, 2, v],
            )
            for v in range(3, p - 1)
        ]
    else:
        raise ValueError(j)
    return sorted_rows(rows)


def main() -> int:
    if sha256(HERE / "run.py") != EXPECTED_RUN_SHA256:
        raise AssertionError("run.py hash mismatch")
    if sha256(RESULTS) != EXPECTED_RESULTS_SHA256:
        raise AssertionError("results hash mismatch")
    exp047_path = EXP047 / "artifacts" / "results.json"
    if sha256(exp047_path) != EXPECTED_EXP047_SHA256:
        raise AssertionError("EXP-047 results hash mismatch")

    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    exp047 = json.loads(exp047_path.read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, value: bool) -> None:
        checks.append({"name": name, "pass": bool(value)})

    stored_hash = results.pop("artifact_hash")
    check("results internal hash", digest(results) == stored_hash)
    results["artifact_hash"] = stored_hash
    check("results complete", results["status"] == "COMPLETE")
    check("declared parameter set", [row["p"] for row in results["rows"]] == [8, 9, 10, 11])
    check("P1 finite pass", results["p1_status"] == "PASS_FINITE")
    check("P2 refuted", results["p2_status"] == "REFUTED")
    check("P3 refuted", results["p3_status"] == "REFUTED")

    exp047_records = {
        (row["p"], record["source_mask"], record["target_mask"]): record
        for row in exp047["rows"]
        for record in row["inclusions"]
    }
    for row in results["rows"]:
        p = int(row["p"])
        records = {
            (record["source_mask"], record["target_mask"]): record
            for record in row["inclusions"]
        }
        for key, expected_rank in (((58, 59), 2), ((58, 62), 2), ((56, 58), p - 7)):
            record = records[key]
            exact = exp047_records[p, *key]["relative"]
            independent_rank = int(exact["rank_q"]) - int(exact["ranks"]["2"])
            check(f"p={p} {key[0]}->{key[1]} rank", record["bockstein_rank"] == expected_rank)
            check(
                f"p={p} {key[0]}->{key[1]} rank agrees EXP-047",
                record["bockstein_rank"] == independent_rank,
            )
            check(f"p={p} {key[0]}->{key[1]} reverse audit", record["reverse_agrees"])
            check(
                f"p={p} {key[0]}->{key[1]} representative hashes",
                record["representative_template_hashes"]
                == [digest(rep) for rep in record["representatives"]],
            )

        alpha_actual = records[58, 59]["representatives"]
        beta_actual = records[58, 62]["representatives"]
        check(f"p={p} alpha-1 formula", alpha_actual[0] == alpha(p, 1))
        check(f"p={p} alpha-2 formula", alpha_actual[1] == alpha(p, 2))
        check(f"p={p} beta-1 formula", beta_actual[0] == beta(p, 1))
        check(f"p={p} beta-2 formula", beta_actual[1] == beta(p, 2))
        check(f"p={p} alpha support law", records[58, 59]["support_sizes"] == [p - 4, p - 4])
        check(
            f"p={p} beta support law",
            records[58, 62]["support_sizes"] == [2 * p - 8, p - 4],
        )

    passed = sum(item["pass"] for item in checks)
    certificate = {
        "experiment": "EXP-048",
        "audit": "independent rank recomposition and explicit completion-chain formulas",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checks_passed": passed,
        "checks_total": len(checks),
        "run_sha256": EXPECTED_RUN_SHA256,
        "results_sha256": EXPECTED_RESULTS_SHA256,
        "exp047_results_sha256": EXPECTED_EXP047_SHA256,
        "formula_scope": "post-result exact finite classification, not an all-parameter proof",
        "checks": checks,
    }
    certificate["artifact_hash"] = digest(certificate)
    write_json_atomic(OUTPUT, certificate)
    print(json.dumps({key: certificate[key] for key in ("status", "checks_passed", "checks_total", "artifact_hash")}, indent=2))
    return 0 if certificate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
