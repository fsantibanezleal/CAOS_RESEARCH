"""EXP-030 symbolic coefficient, support, and total certificate."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import sympy


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "artifacts" / "symbolic-certificate.json"


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def add(left: list[int], right: list[int], factor: int = 1) -> list[int]:
    size = max(len(left), len(right))
    answer = left + [0] * (size - len(left))
    for index, value in enumerate(right):
        answer[index] += factor * value
    while answer and answer[-1] == 0:
        answer.pop()
    return answer


def convolve(left: list[int], right: list[int]) -> list[int]:
    answer = [0] * (len(left) + len(right) - 1)
    left_nonzero = [(index, value) for index, value in enumerate(left) if value]
    right_nonzero = [(index, value) for index, value in enumerate(right) if value]
    for i, alpha in left_nonzero:
        for j, beta in right_nonzero:
            answer[i + j] += alpha * beta
    return answer


def indicator(stop: int, intervals: list[tuple[int, int]]) -> list[int]:
    answer = [0] * (stop + 1)
    for start, end in intervals:
        for value in range(start, end + 1):
            answer[value] += 1
    return answer


def elementary_profiles(values: list[int], maximum_size: int = 3) -> list[list[int]]:
    maximum_sum = sum(sorted(values, reverse=True)[:maximum_size])
    profiles = [[0] * (maximum_sum + 1) for _ in range(maximum_size + 1)]
    profiles[0][0] = 1
    current_maximum = 0
    for value in values:
        for size in range(maximum_size, 0, -1):
            for total in range(current_maximum, -1, -1):
                coefficient = profiles[size - 1][total]
                if coefficient:
                    profiles[size][total + value] += coefficient
        current_maximum += value
        current_maximum = min(current_maximum, maximum_sum)
    return profiles


def profile_row(p: int) -> dict[str, object]:
    low = list(range(0, p + 1)) + list(range(3 * p, 4 * p - 1))
    high = (
        list(range(6 * p, 8 * p - 1))
        + list(range(8 * p, 10 * p - 1))
        + [10 * p]
        + list(range(11 * p - 1, 12 * p))
        + list(range(13 * p + 1, 14 * p - 1))
        + list(range(14 * p, 15 * p))
        + [16 * p]
        + list(range(17 * p - 1, 18 * p))
    )
    elementary = elementary_profiles(low)
    e1, e2, e3 = elementary[1], elementary[2], elementary[3]
    h1 = indicator(4 * p - 2, [(0, p), (3 * p, 4 * p - 2)])
    h2 = indicator(5 * p - 2, [(0, 2 * p), (3 * p, 5 * p - 2)])
    h3 = indicator(6 * p - 2, [(0, 3 * p), (3 * p, 6 * p - 2)])

    q = add(add(convolve(e1, h1), h2, -1), e2, -1)
    s = add(add(add(h3, convolve(e1, h2), -1), convolve(e2, h1), 1), e3, -1)
    high_profile = [0] * (max(high) + 1)
    for value in high:
        high_profile[value] = 1
    extended = add(s, convolve(high_profile, q), 1)
    shifted = [0] * (3 * p) + extended

    if any(value < 0 for value in q) or any(value < 0 for value in s):
        raise AssertionError(f"p={p}: negative Betti coefficient")
    support = {offset for offset, value in enumerate(shifted) if value}
    expected_support = (
        set(range(3 * p + 4, 29 * p - 4))
        - set(range(6 * p - 3, 6 * p + 2))
        - set(range(9 * p - 3, 9 * p + 1))
    )
    expected_total = 8 * p * (7 * p * p - 12 * p + 2) // 3
    checks = {
        "low_count": len(low) == 2 * p,
        "high_count": len(high) == 8 * p,
        "quadratic_total": sum(q) == p * (2 * p - 3),
        "linear_syzygy_total": sum(s) == 8 * p * (p - 1) * (p - 2) // 3,
        "degree_six_total": sum(shifted) == expected_total,
        "support": support == expected_support,
        "support_count": len(support) == 26 * p - 17,
    }
    if not all(checks.values()):
        raise AssertionError(f"p={p}: symbolic profile check failed: {checks}")

    row: dict[str, object] = {
        "p": p,
        "quadratic_total": sum(q),
        "linear_syzygy_total": sum(s),
        "degree_six_total": sum(shifted),
        "support_count": len(support),
        "support_min": min(support),
        "support_max": max(support),
        "hole_intervals": [[6 * p - 3, 6 * p + 1], [9 * p - 3, 9 * p]],
        "profile_hash": canonical_hash([(i, value) for i, value in enumerate(shifted) if value]),
        "checks": checks,
    }
    row["row_hash"] = canonical_hash(row)
    return row


def main() -> int:
    p = sympy.symbols("p", integer=True, positive=True)
    c = 2 * p - 2
    quadratic = sympy.expand(c * (c + 1) / 2 - 1)
    linear_syzygy = sympy.expand(c * (c - 2) * (c + 2) / 3)
    degree_six = sympy.factor(8 * p * quadratic + linear_syzygy)
    identities = {
        "quadratic": sympy.simplify(quadratic - p * (2 * p - 3)) == 0,
        "linear_syzygy": sympy.simplify(
            linear_syzygy - 8 * p * (p - 1) * (p - 2) / 3
        ) == 0,
        "degree_six": sympy.simplify(
            degree_six - 8 * p * (7 * p * p - 12 * p + 2) / 3
        ) == 0,
        "support_count": sympy.simplify((29 * p - 5) - (3 * p + 4) + 1 - 5 - 4)
        == 26 * p - 17,
    }
    divisibility = {
        str(residue): (8 * residue * (7 * residue * residue - 12 * residue + 2)) % 3 == 0
        for residue in range(3)
    }
    if not all(identities.values()) or not all(divisibility.values()):
        raise AssertionError("closed symbolic identity failed")

    parameters = list(range(4, 26)) + [50, 100, 300]
    rows = [profile_row(value) for value in parameters]
    payload: dict[str, object] = {
        "experiment": "EXP-030-colon-idealization-degree-six",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "route": "independent coefficient arrays plus SymPy scalar identities",
        "sympy_version": sympy.__version__,
        "parameters": parameters,
        "identities": identities,
        "divisibility_mod_3": divisibility,
        "rows": rows,
    }
    payload["symbolic_aggregate"] = canonical_hash(
        {
            "rows": [row["row_hash"] for row in rows],
            "identities": identities,
            "divisibility": divisibility,
        }
    )
    write_json_atomic(OUTPUT, payload)
    print(f"PASS aggregate={payload['symbolic_aggregate']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
