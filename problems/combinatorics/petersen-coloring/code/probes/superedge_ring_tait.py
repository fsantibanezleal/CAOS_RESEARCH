"""3-edge-colorability of the uniform rings of Petersen superedges for every length (EXP-014, descriptive).

    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/code/probes/superedge_ring_tait.py

The boundary relation of the superedge S = P - u - w for proper 3-edge-colorings (states: the 27
color triples of a connector) is enumerated by brute force; for each junction permutation pi the
ring of t copies is 3-edge-colorable iff the boolean matrix (T Pi)^t has a nonzero diagonal. The
powers are eventually periodic, so the answer for every t follows from finitely many powers.
Writes superedge_ring_tait.json next to this file.
"""

import importlib.util
import itertools
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from pcclib import transfer  # noqa: E402

spec = importlib.util.spec_from_file_location("exp014", HERE.parents[1] / "experiments" / "EXP-014-transfer-semigroups" / "run.py")
exp014 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exp014)

blk = exp014.superedge()
pl = blk.pole
items = sorted({it for v in pl.kept for it in pl.items[v]})
states = list(itertools.product(range(3), repeat=3))
sidx = {s: i for i, s in enumerate(states)}
T = np.zeros((27, 27), dtype=bool)
order = list(pl.kept)
lab = {}


def rec(k):
    if k == len(order):
        a = tuple(lab[("d", j)] for j in blk.left)
        b = tuple(lab[("d", j)] for j in blk.right)
        T[sidx[a], sidx[b]] = True
        return
    its = pl.items[order[k]]
    for perm in itertools.permutations(range(3)):
        new, ok = [], True
        for it, c in zip(its, perm):
            if it in lab:
                if lab[it] != c:
                    ok = False
                    break
            else:
                lab[it] = c
                new.append(it)
        if ok:
            rec(k + 1)
        for it in new:
            del lab[it]


rec(0)
out = {"boundary_pairs": int(T.sum()), "rings": {}}
for pi in transfer.PERMS:
    P = np.zeros((27, 27), dtype=bool)
    for y in states:
        x = [0, 0, 0]
        for j in range(3):
            x[pi[j]] = y[j]
        P[sidx[y], sidx[tuple(x)]] = True
    G = ((T.astype(int) @ P.astype(int)) > 0)
    seen, cur, res = {}, G.copy(), []
    for t in range(1, 200):
        key = cur.tobytes()
        if key in seen:
            start, period = seen[key], t - seen[key]
            break
        seen[key] = t
        res.append(bool(np.any(np.diagonal(cur))))
        cur = (cur.astype(int) @ G.astype(int)) > 0
    out["rings"]["".join(map(str, pi))] = {"colorable_for_t": res, "preperiod": start, "period": period}
    print(pi, "3-edge-colorable for t = 1..", len(res), ":", "".join("1" if r else "0" for r in res), "period", period, "from", start)
(HERE / "superedge_ring_tait.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
