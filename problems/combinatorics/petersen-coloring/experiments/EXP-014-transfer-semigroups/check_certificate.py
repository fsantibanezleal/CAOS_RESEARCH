"""EXP-014 independent checks (hypothesis.md, "Soundness and certificate").

    .venv/Scripts/python.exe .../check_certificate.py --family F1 [--family F2 ...]

1. Recomputes the sector matrices of the small blocks (the claw, the superedge, the forty `Pb`
   blocks) by brute-force enumeration of good maps (no SAT solver) and compares them with
   HEAVY/blocks.npz.
2. Rebuilds the generators of each family from the stored block matrices and compares them with the
   certificate's generators.
3. Verifies the certificate conditions: every product of two generators is in C, C times every
   generator is in C, and every element of C has a nonzero diagonal in some sector.
Writes artifacts/certificate-check.json.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "code"))

import run as exp014  # noqa: E402
from pcclib import graphs, transfer  # noqa: E402

SECTORS = transfer.SECTORS


def enumerate_boundary(block: transfer.Block) -> set[tuple[tuple[int, ...], tuple[int, ...]]]:
    """All (labels on L, labels on R) of maps with every vertex good, by backtracking over vertices."""
    p = graphs.petersen()
    stars = [sorted(s) for s in p.incidence()]
    pl = block.pole
    order = list(pl.kept)
    lab: dict = {}
    out = set()

    def rec(k: int) -> None:
        if k == len(order):
            out.add((tuple(lab[("d", j)] for j in block.left), tuple(lab[("d", j)] for j in block.right)))
            return
        items = pl.items[order[k]]
        for star in stars:
            for perm in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
                new, ok = [], True
                for it, pi in zip(items, perm):
                    t = star[pi]
                    if it in lab:
                        if lab[it] != t:
                            ok = False
                            break
                    else:
                        new.append(it)
                        lab[it] = t
                if ok:
                    rec(k + 1)
                for it in new:
                    del lab[it]

    rec(0)
    return out


def matrices_from_boundary(pairs) -> dict[str, np.ndarray]:
    states = transfer.sector_states()
    out = {}
    for o in SECTORS:
        idx = {t: i for i, t in enumerate(states[o])}
        m = np.zeros((len(idx), len(idx)), dtype=bool)
        for a, b in pairs:
            if a in idx:
                if b not in idx:
                    raise AssertionError("Gauss law violated")
                m[idx[a], idx[b]] = True
        out[o] = m
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", action="append", default=[])
    args = ap.parse_args()
    blocks, mats = exp014.load_blocks()
    report = {"blocks": [], "families": {}}
    for i, blk in enumerate(blocks):
        if not (blk.name in ("Y", "S") or blk.name.startswith("Pb:")):
            continue
        ind = matrices_from_boundary(enumerate_boundary(blk))
        same = all(np.array_equal(ind[o], mats[i][o]) for o in SECTORS)
        report["blocks"].append({"block": blk.name, "independent_enumeration_equal": same})
        print(f"{blk.name}: independent enumeration {'equal' if same else 'DIFFERENT'}", flush=True)
    for fam in args.family:
        z = np.load(exp014.HEAVY / f"certificate-{fam}.npz")
        gens = exp014.generators(blocks, mats, fam)
        stored = [row.tobytes() for row in z["generators"]]
        gens_equal = [transfer.pack(g["mats"]) for g in gens] == stored
        elements = {row.tobytes() for row in z["elements"]}
        gm = [g["mats"] for g in gens]
        two = all(transfer.pack(transfer.product([a, b])) in elements for a in gm for b in gm)
        closed, diag = True, True
        for raw in elements:
            c = transfer.unpack(raw)
            if not transfer.colorable_sectors(c):
                diag = False
            for g in gm:
                if transfer.pack(transfer.product([c, g])) not in elements:
                    closed = False
        report["families"][fam] = {"generators_equal": gens_equal, "elements": len(elements),
                                   "products_of_two_in_C": two, "C_closed_under_generators": closed,
                                   "every_element_nonzero_diagonal": diag}
        print(fam, report["families"][fam], flush=True)
    (HERE / "artifacts" / "certificate-check.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
