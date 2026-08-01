"""EXP-010 P3: deterministic grevlex staircase dimension of the Dziobek ideal.

Computes the reduced grevlex Groebner basis of the stripped system plus the
Rabinowitsch equation in QQ[r_ij, t], then the Krull dimension of the leading
term ideal by the standard independent-set characterization (Kredel and
Weispfenning): dim = the largest cardinality of a variable subset S such that
no leading monomial is supported entirely inside S. With 7 variables the 128
subsets are checked exhaustively, which is exact. Prints JSON on success; the
caller enforces the wall-clock cap.
"""
import json
import sys
from itertools import combinations
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "code"))
from cclib import (cayley_menger_planar4, dziobek4, rvar,  # noqa: E402
                   strip_monomial_factors)

GENS6 = [rvar(i, j) for i in range(1, 5) for j in range(i + 1, 5)]
T = sp.Symbol("t")


def main():
    gens = GENS6 + [T]
    h = dziobek4()
    eqs = [strip_monomial_factors(v, GENS6) for v in h.values()]
    eqs.append(sp.expand(cayley_menger_planar4()))
    eqs.append(T * sp.prod(GENS6) - 1)
    gb = sp.groebner(eqs, *gens, order="grevlex")
    # gb.polys carry the grevlex order; monoms() lists exponent tuples with the
    # leading monomial first, so its positive positions are the LM support.
    lead_supports = []
    for p in gb.polys:
        lead = p.monoms()[0]
        lead_supports.append({gens[i] for i, e in enumerate(lead) if e > 0})
    dim = 0
    witness = []
    for size in range(len(gens), -1, -1):
        found = None
        for S in combinations(gens, size):
            Sset = set(S)
            if all(not sup <= Sset for sup in lead_supports):
                found = S
                break
        if found is not None:
            dim = size
            witness = [str(g) for g in found]
            break
    print(json.dumps({"gb_size": len(gb.exprs), "dim": dim,
                      "independent_set": witness}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
