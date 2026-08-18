"""Independent clique reconstruction for the EXP-026 grevlex staircase."""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_INPUT = HERE / "artifacts" / "results.json"
DEFAULT_OUTPUT = HERE / "artifacts" / "audit.json"
DEFAULT_CHECKPOINT = HERE / "artifacts" / "audit-checkpoint.json"
DEFAULT_SAMPLES = (4, 5, 6, 17, 73, 151, 300)

Monomial = tuple[int, ...]


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def interval(start: int, stop: int) -> tuple[int, ...]:
    return tuple(range(start, stop + 1)) if start <= stop else ()


def independent_offsets(p: int) -> tuple[int, ...]:
    blocks = (
        (0,),
        interval(1, p),
        interval(3 * p, 4 * p - 2),
        interval(6 * p, 8 * p - 2),
        interval(8 * p, 10 * p - 2),
        (10 * p,),
        interval(11 * p - 1, 12 * p - 1),
        interval(13 * p + 1, 14 * p - 2),
        interval(14 * p, 15 * p - 1),
        (16 * p,),
        interval(17 * p - 1, 18 * p - 1),
    )
    flattened = tuple(sorted({value for block in blocks for value in block}))
    if len(flattened) != 10 * p:
        raise AssertionError(f"p={p}: independent generator count mismatch")
    return flattened


def remove_one(value: Monomial, index: int) -> Monomial:
    return value[:index] + value[index + 1 :]


def distinct_divisors(value: Monomial) -> set[Monomial]:
    return {remove_one(value, index) for index in range(len(value))}


def relation_hash(leads: set[Monomial], standards: dict[int, Monomial]) -> str:
    relations = [[list(lead), list(standards[sum(lead)])] for lead in sorted(leads)]
    return canonical_hash(relations)


def direct_pairs(offsets: tuple[int, ...], q: int) -> tuple[dict[int, Monomial], int]:
    standards: dict[int, Monomial] = {}
    zero_count = 0
    for left_index, left in enumerate(offsets):
        split = bisect.bisect_left(offsets, q - left, lo=left_index)
        zero_count += len(offsets) - max(left_index, split)
        for right in offsets[left_index:split]:
            standards.setdefault(left + right, (left, right))
    return standards, zero_count


def adjacency(pair_set: set[Monomial]) -> dict[int, set[int]]:
    answer: dict[int, set[int]] = {}
    for left, right in pair_set:
        answer.setdefault(left, set()).add(right)
        answer.setdefault(right, set()).add(left)
    return answer


def triple_candidates(pair_set: set[Monomial], adjacent: dict[int, set[int]]) -> set[Monomial]:
    candidates: set[Monomial] = set()
    for left, middle in pair_set:
        for right in adjacent.get(left, set()) & adjacent.get(middle, set()):
            if right >= middle:
                candidates.add((left, middle, right))
    return candidates


def higher_candidates(
    standards: set[Monomial], adjacent: dict[int, set[int]]
) -> set[Monomial]:
    candidates: set[Monomial] = set()
    degree = len(next(iter(standards))) if standards else 0
    for value in standards:
        possible = None
        for entry in set(value):
            neighbors = adjacent.get(entry, set())
            possible = set(neighbors) if possible is None else possible & neighbors
        for final in possible or ():
            if final < value[-1]:
                continue
            candidate = value + (final,)
            if all(divisor in standards for divisor in distinct_divisors(candidate)):
                candidates.add(candidate)
    if candidates and len(next(iter(candidates))) != degree + 1:
        raise AssertionError("candidate degree corruption")
    return candidates


def choose_standards(candidates: set[Monomial], q: int) -> dict[int, Monomial]:
    standards: dict[int, Monomial] = {}
    for value in sorted(candidates):
        total = sum(value)
        if total < q:
            standards.setdefault(total, value)
    return standards


def reconstruct(p: int) -> dict[str, object]:
    q = 24 * p
    offsets = independent_offsets(p)
    pairs, zero_pairs = direct_pairs(offsets, q)
    pair_set = set(pairs.values())
    adjacent = adjacency(pair_set)

    candidates3 = triple_candidates(pair_set, adjacent)
    standards3 = choose_standards(candidates3, q)
    cubics = candidates3 - set(standards3.values())

    candidates4 = higher_candidates(set(standards3.values()), adjacent)
    standards4 = choose_standards(candidates4, q)
    quartics = candidates4 - set(standards4.values())

    candidates5 = higher_candidates(set(standards4.values()), adjacent)
    standards5 = choose_standards(candidates5, q)
    quintics = candidates5 - set(standards5.values())

    candidates6 = higher_candidates(set(standards5.values()), adjacent)
    standards6 = choose_standards(candidates6, q)
    sextics = candidates6 - set(standards6.values())

    expected_dimensions = [22 * p, q - 1, q, q, q]
    dimensions = [len(pairs), len(standards3), len(standards4), len(standards5), len(standards6)]
    if dimensions != expected_dimensions:
        raise AssertionError(f"p={p}: independent dimensions {dimensions} != {expected_dimensions}")
    if len(cubics) != 5 * p - 1 or len(quartics) != p - 2 or quintics or sextics:
        raise AssertionError(
            f"p={p}: boundary profile {(len(cubics), len(quartics), len(quintics), len(sextics))}"
        )
    if any(0 in lead for lead in cubics | quartics):
        raise AssertionError(f"p={p}: independent boundary contains X_0")

    total_pairs = len(offsets) * (len(offsets) + 1) // 2
    row = {
        "p": p,
        "pair_factorizations_enumerated": total_pairs,
        "standard_counts_2_to_6": dimensions,
        "quadratic_profile": {
            "total": total_pairs - len(pairs),
            "binomial": total_pairs - zero_pairs - len(pairs),
            "monomial_zero": zero_pairs,
        },
        "boundary_counts_3_to_6": [len(cubics), len(quartics), len(quintics), len(sextics)],
        "cubic_relation_hash": relation_hash(cubics, standards3),
        "quartic_relation_hash": relation_hash(quartics, standards4),
        "x0_divides_minimal_lead": False,
    }
    row["audit_row_hash"] = canonical_hash(row)
    return row


def parse_samples(raw: str) -> tuple[int, ...]:
    return tuple(int(item) for item in raw.split(",") if item.strip())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    parser.add_argument("--samples", default=",".join(map(str, DEFAULT_SAMPLES)))
    parser.add_argument("--budget-seconds", type=float, default=120.0)
    args = parser.parse_args()

    campaign = json.loads(args.input.read_text(encoding="utf-8"))
    if campaign.get("status") != "PASS":
        raise SystemExit("audit requires a PASS campaign")
    rows_by_p = {row["p"]: row for row in campaign["rows"]}
    samples = parse_samples(args.samples)
    started = time.perf_counter()
    rows = []
    status = "PASS"
    for p in samples:
        if time.perf_counter() - started > args.budget_seconds:
            status = "INCONCLUSIVE_BUDGET"
            break
        if p not in rows_by_p:
            raise AssertionError(f"p={p}: missing campaign row")
        audited = reconstruct(p)
        campaign_row = rows_by_p[p]
        for key in (
            "quadratic_profile",
            "cubic_relation_hash",
            "quartic_relation_hash",
            "x0_divides_minimal_lead",
        ):
            if audited[key] != campaign_row[key]:
                raise AssertionError(
                    f"p={p}: audit mismatch for {key}: {audited[key]} != {campaign_row[key]}"
                )
        rows.append(audited)
        write_json_atomic(
            args.checkpoint,
            {
                "experiment": "EXP-026-audit",
                "status": "RUNNING",
                "last_completed": p,
                "audit_row_hashes": [row["audit_row_hash"] for row in rows],
            },
        )
    if len(rows) != len(samples) and status == "PASS":
        status = "INCONCLUSIVE"

    all_row_rehash = canonical_hash([row["row_hash"] for row in campaign["rows"]])
    if all_row_rehash != campaign["campaign_aggregate"]:
        raise AssertionError("all-row campaign aggregate mismatch")
    result = {
        "experiment": "EXP-026-grevlex-staircase-audit",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "samples": list(samples),
        "completed_samples": len(rows),
        "campaign_all_row_rehash": all_row_rehash,
        "audit_aggregate": canonical_hash([row["audit_row_hash"] for row in rows]),
        "elapsed_seconds": time.perf_counter() - started,
        "rows": rows,
    }
    write_json_atomic(args.output, result)
    write_json_atomic(
        args.checkpoint,
        {
            "experiment": "EXP-026-audit",
            "status": status,
            "last_completed": rows[-1]["p"] if rows else None,
            "audit_row_hashes": [row["audit_row_hash"] for row in rows],
        },
    )
    print(
        f"EXP-026 audit {status}: samples={len(rows)} aggregate={result['audit_aggregate']} "
        f"elapsed={result['elapsed_seconds']:.3f}s"
    )
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())

