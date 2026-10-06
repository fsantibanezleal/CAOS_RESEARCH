"""Which rings of Petersen superedges are snarks (not 3-edge-colorable)? (EXP-014, descriptive)

    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/code/probes/superedge_ring_snarks.py

Rings of t copies of P - u - w with the same junction permutation at every junction, t = 2..8, all
six permutations; 3-edge-colorability decided by PySAT (CaDiCaL) on the direct encoding. Also the
rings of claws (flower-type), as a control: J_k for odd k is a snark. Writes
superedge_ring_snarks.json next to this file.
"""

import importlib.util
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from pcclib import invariants, transfer  # noqa: E402

spec = importlib.util.spec_from_file_location("exp014", HERE.parents[1] / "experiments" / "EXP-014-transfer-semigroups" / "run.py")
exp014 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exp014)


def three_edge_colorable(g) -> bool:
    from pysat.solvers import Solver
    var = lambda e, c: 3 * e + c + 1  # noqa: E731
    cl = []
    for e in range(len(g.edges)):
        cl.append([var(e, c) for c in range(3)])
        cl += [[-var(e, a), -var(e, b)] for a, b in itertools.combinations(range(3), 2)]
    for inc in g.incidence():
        for e, f in itertools.combinations(inc, 2):
            cl += [[-var(e, c), -var(f, c)] for c in range(3)]
    with Solver(name="cadical153", bootstrap_with=cl) as s:
        return s.solve()


rows = []
for name, blk in (("S", exp014.superedge()), ("Y", exp014.claw())):
    for t in range(2, 9):
        for pi in transfer.PERMS:
            word = [(blk, pi)] * t
            if name == "Y":
                word = [(blk, (0, 1, 2))] * (t - 1) + [(blk, pi)]
            try:
                g = transfer.build_ring(word)
            except ValueError:
                rows.append({"block": name, "t": t, "pi": list(pi), "simple": False})
                continue
            rows.append({"block": name, "t": t, "pi": list(pi), "simple": True, "order": g.n, "girth": invariants.girth(g),
                         "three_edge_colorable": three_edge_colorable(g)})
            print(rows[-1], flush=True)
(HERE / "superedge_ring_snarks.json").write_text(json.dumps(rows, indent=1) + "\n", encoding="utf-8", newline="\n")
