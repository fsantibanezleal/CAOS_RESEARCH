"""EXP-138: the de Bondt homogenization gives a Keller map on C^15 with an exact collision."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-138-mathieu-su15/artifacts/results.json"


def test_recorded_map_collides_and_is_homogeneous() -> None:
    data = json.loads(RESULTS.read_text(encoding="utf-8"))["P2"]
    x = list(sp.symbols("x1:16"))
    G = [sp.sympify(g) for g in data["components"]]
    assert len(G) == 15
    for i, g in enumerate(G):
        h = sp.expand(g - x[i])
        assert h == 0 or (sp.Poly(h, *x).is_homogeneous and sp.Poly(h, *x).total_degree() == 7)
    p, q = ([sp.Integer(int(c)) for c in pt] for pt in data["points"])
    assert p != q
    assert [g.subs(dict(zip(x, p))) for g in G] == [g.subs(dict(zip(x, q))) for g in G]


def test_alpoge_volume_normalized_map() -> None:
    x1, x2, x3 = sp.symbols("x1:4")
    v = 1 + 2 * x1 * x2
    F = sp.Matrix([x1 - 3 * x1**2 * x2 - x1**3 * x3, 3 * v**2 * x1 * x3 + (9 * v**2 - 6 * v - 2) * x2,
                   v**3 * x3 + (6 * v**2 + 2 * v) * x2**2])
    assert sp.expand(F.jacobian([x1, x2, x3]).det()) == 1
    assert F.subs({x1: 0, x2: 1, x3: -8}) == F.subs({x1: -1, x2: 1, x3: 4})
