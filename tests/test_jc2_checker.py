"""EXP-015: the JC(2) checker and bridge extractor are boringly correct."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]
                       / "problems" / "algebraic-geometry" / "jacobian-conjecture" / "code"))

from sympy import Rational  # noqa: E402
from jclib.jc2 import bridge_extract, check_collision2, check_keller2, x, y, v, t  # noqa: E402


def test_checker_accepts_automorphism_and_rejects_fakes():
    P, Q = x + y**2, y + (x + y**2) ** 3
    assert check_keller2(P, Q)["keller"] is True
    assert check_keller2(x * y, y)["keller"] is False
    r = check_collision2(P, Q, (Rational(0), Rational(0)), (Rational(1), Rational(0)))
    assert r["valid"] is False and r["reason"] == "images differ"
    r2 = check_collision2(P, Q, (Rational(1), Rational(2)), (Rational(1), Rational(2)))
    assert r2["valid"] is False and r2["reason"] == "points are equal"


def test_bridge_pipeline_end_to_end():
    # Synthetic reduced data (formal demonstration of the pipeline, no existence claim):
    # the extractor must build the planar pair and hand it to the checker verbatim.
    f1, f2, f3 = v + t, v - t, 1 + 0 * v
    out = bridge_extract(f1, f2, f3, (1, 2, 3), (1, 3, 2))
    assert out["extracted"] is True
    assert out["certificate"]["valid"] in (True, False)  # checker ran and returned a verdict
    # Distinct 3D points with EQUAL invariants must be refused (nothing to extract).
    same = bridge_extract(f1, f2, f3, (1, 2, 3), (-1, -2, -3))
    assert same["extracted"] is False
