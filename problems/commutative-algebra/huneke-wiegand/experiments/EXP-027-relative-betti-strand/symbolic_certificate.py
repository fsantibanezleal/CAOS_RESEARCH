"""Z3 certificate for the EXP-027 interval and quadratic-path lemmas."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from z3 import And, Exists, If, Int, Not, Or, Solver, Xor, unsat


HERE = Path(__file__).resolve().parent
DEFAULT_OUTPUT = HERE / "artifacts" / "symbolic-certificate.json"


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def interval(value, start, stop):
    return And(start <= value, value <= stop)


def generator(value, p):
    return Or(
        value == 0,
        interval(value, 1, p),
        interval(value, 3 * p, 4 * p - 2),
        interval(value, 6 * p, 8 * p - 2),
        interval(value, 8 * p, 10 * p - 2),
        value == 10 * p,
        interval(value, 11 * p - 1, 12 * p - 1),
        interval(value, 13 * p + 1, 14 * p - 2),
        interval(value, 14 * p, 15 * p - 1),
        value == 16 * p,
        interval(value, 17 * p - 1, 18 * p - 1),
    )


def support(value, p):
    return Or(
        interval(value, 9 * p, 11 * p - 2),
        interval(value, 11 * p, 13 * p - 2),
        value == 13 * p,
        interval(value, 14 * p - 1, 15 * p - 1),
        interval(value, 16 * p + 1, 17 * p - 2),
        interval(value, 17 * p, 18 * p - 1),
        value == 19 * p,
        interval(value, 20 * p - 1, 21 * p - 1),
    )


def center(value, p):
    return And(generator(value, p), generator(value - p, p), generator(value + p, p))


def expected_center(value, p):
    return Or(
        interval(value, 7 * p, 8 * p - 2),
        interval(value, 8 * p, 9 * p - 2),
        value == 9 * p,
        value == 10 * p,
    )


def check_unsat(name: str, expression) -> dict[str, object]:
    solver = Solver()
    solver.add(expression)
    result = solver.check()
    row = {"name": name, "result": str(result), "passed": result == unsat}
    if result != unsat:
        row["model"] = str(solver.model())
    return row


def middle_indicator(value, p):
    return If(interval(value, 3 * p, 4 * p - 2), 1, 0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    p, a, b, u = Int("p"), Int("a"), Int("b"), Int("u")
    x, y, z, w = Int("x"), Int("y"), Int("z"), Int("w")
    high = And(generator(a, p), a >= 6 * p)
    center_path = Exists(
        [u],
        And(
            generator(u, p),
            generator(a - u, p),
            generator(a - u - p, p),
            generator(a - u + p, p),
        ),
    )
    path_available = Or(
        And(generator(a + p, p), generator(a + 2 * p, p)),
        a == 7 * p - 1,
        center_path,
    )
    queries = [
        check_unsat(
            "support_equals_shifted_high",
            And(p >= 4, Xor(support(b, p), And(generator(b - 3 * p, p), b - 3 * p >= 6 * p))),
        ),
        check_unsat(
            "center_set_formula",
            And(p >= 4, Xor(center(a, p), expected_center(a, p))),
        ),
        check_unsat(
            "every_high_offset_has_quadratic_path",
            And(p >= 4, high, Not(path_available)),
        ),
        check_unsat(
            "low_total_below_seven_p",
            And(p >= 4, generator(a, p), a < 6 * p, 3 * p + a > 7 * p - 2),
        ),
        check_unsat(
            "low_fiber_moves_preserve_middle_parity",
            And(
                p >= 4,
                generator(x, p),
                generator(y, p),
                generator(z, p),
                generator(w, p),
                x + y == z + w,
                x + y <= 7 * p - 2,
                (
                    middle_indicator(x, p)
                    + middle_indicator(y, p)
                    - middle_indicator(z, p)
                    - middle_indicator(w, p)
                )
                % 2
                != 0,
            ),
        ),
        check_unsat(
            "transient_morse_range_disjoint_from_support",
            And(p >= 4, interval(b, 6 * p, 7 * p - 3), support(b, p)),
        ),
    ]
    payload = {
        "experiment": "EXP-027-relative-betti-strand",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if all(row["passed"] for row in queries) else "FAIL",
        "queries": queries,
    }
    payload["aggregate"] = hashlib.sha256(
        json.dumps(queries, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    write_json_atomic(args.output, payload)
    print(f"EXP-027 symbolic {payload['status']}: {len(queries)} queries {payload['aggregate']}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
