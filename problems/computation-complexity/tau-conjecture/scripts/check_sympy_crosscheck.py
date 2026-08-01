"""Adversarial cross-check (TCB-005 audit piece): tclib exact root counting
vs sympy, on every polynomial of tau <= 3 (all 220) plus the EXP-002
depth-5 records. Independent code path: sympy factorizes; tclib uses the
divisor argument. Any mismatch exits nonzero.

Run from repo root:
    .venv python problems/computation-complexity/tau-conjecture/scripts/check_sympy_crosscheck.py
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "code"))

import sympy  # noqa: E402

from tclib.enum import census_polynomials, integer_roots  # noqa: E402

X = sympy.symbols("x")


def sympy_integer_roots(coeffs):
    poly = sum(c * X**i for i, c in enumerate(coeffs))
    return {int(r) for r, _ in sympy.roots(sympy.Poly(poly, X)).items()
            if r.is_integer}


def main():
    checked = 0
    _, first_seen, _ = census_polynomials(3)
    sample = list(first_seen)
    rec_file = (HERE.parent / "experiments" / "EXP-002-census-depth5"
                / "artifacts" / "census5.json")
    if rec_file.exists():
        data = json.loads(rec_file.read_text(encoding="utf-8"))
        for recs in data["records"].values():
            sample.extend(tuple(r["poly"]) for r in recs)
    for f in sample:
        ours = integer_roots(f)
        theirs = sympy_integer_roots(f)
        if ours != theirs:
            print(f"MISMATCH {f}: tclib={sorted(ours)} sympy={sorted(theirs)}")
            return 1
        checked += 1
    print(f"OK: {checked} polynomials cross-checked (tclib == sympy)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
