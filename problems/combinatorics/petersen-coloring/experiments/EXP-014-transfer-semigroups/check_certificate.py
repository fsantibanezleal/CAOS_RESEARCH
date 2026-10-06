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


def matrices_vertex_encoding(block: transfer.Block) -> dict[str, np.ndarray]:
    """Second encoding, second solver: one variable per (vertex, image vertex of P, bijection of its
    three items onto the image's star), exactly one per vertex, each choice implying the item labels;
    MiniSat 2.2 instead of CaDiCaL."""
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool
    from pysat.solvers import Solver

    p = graphs.petersen()
    stars = [sorted(s) for s in p.incidence()]
    pl = block.pole
    pool = IDPool()
    clauses = []
    lab = lambda it, t: pool.id(("l", it, t))  # noqa: E731
    items = sorted({it for v in pl.kept for it in pl.items[v]})
    for it in items:
        clauses += CardEnc.equals([lab(it, t) for t in range(15)], 1, vpool=pool, encoding=EncType.pairwise).clauses
    for v in pl.kept:
        opts = []
        for x, star in enumerate(stars):
            for perm in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
                o = pool.id(("o", v, x, perm))
                opts.append(o)
                for it, pi in zip(pl.items[v], perm):
                    clauses.append([-o, lab(it, star[pi])])
        clauses.append(opts)
    states = transfer.sector_states()
    out = {}
    with Solver(name="minisat22", bootstrap_with=clauses) as s:
        for o in SECTORS:
            st = states[o]
            idx = {t: i for i, t in enumerate(st)}
            m = np.zeros((len(st), len(st)), dtype=bool)
            for i, a in enumerate(st):
                assume = [lab(("d", block.left[k]), a[k]) for k in range(3)]
                sel = pool.id(("sel", o, i))
                while s.solve(assumptions=assume + [sel]):
                    model = set(l for l in s.get_model() if l > 0)
                    b = tuple(next(t for t in range(15) if lab(("d", block.right[k]), t) in model) for k in range(3))
                    m[i, idx[b]] = True
                    s.add_clause([-sel] + [-lab(("d", block.right[k]), b[k]) for k in range(3)])
                s.add_clause([-sel])
            out[o] = m
    return out


def _vertex_job(i: int):
    blocks, mats = exp014.load_blocks()
    ind = matrices_vertex_encoding(blocks[i])
    return blocks[i].name, all(np.array_equal(ind[o], mats[i][o]) for o in SECTORS)


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


def imul(a: dict, b: dict) -> dict:
    """Boolean product by integer matrix multiplication (a different path from the runner's float32)."""
    return {o: (a[o].astype(np.int32) @ b[o].astype(np.int32)) > 0 for o in SECTORS}


def diagonal_nonzero(c: dict) -> bool:
    return any(bool(c[o][i, i]) for o in SECTORS for i in range(c[o].shape[0]))


def as_words(raw: bytes) -> np.ndarray:
    pad = np.zeros(269 * 8, dtype=np.uint8)
    b = np.frombuffer(raw, dtype=np.uint8)
    pad[:b.size] = b
    return pad.view(np.uint64)


def check_antichain(fam: str, blocks, mats) -> dict:
    """Conditions with containment: products of two generators and C times generators each contain an
    element of C; every element of C has a nonzero diagonal."""
    z = np.load(exp014.HEAVY / f"certificate-{fam}-antichain.npz")
    gens = exp014.generators(blocks, mats, fam)
    gens_equal = [transfer.pack(g["mats"]) for g in gens] == [row.tobytes() for row in z["generators"]]
    raws = [row.tobytes() for row in z["elements"]]
    cw = np.array([as_words(r) for r in raws])
    gm = [g["mats"] for g in gens]

    def contains_some(m: dict) -> bool:
        x = as_words(transfer.pack(m))
        return bool(np.any(np.all((cw & ~x) == 0, axis=1)))

    two = all(contains_some(imul(a, b)) for a in gm for b in gm)
    closed = all(contains_some(imul(transfer.unpack(r), g)) for r in raws for g in gm)
    diag = all(diagonal_nonzero(transfer.unpack(r)) for r in raws)
    return {"mode": "antichain", "generators_equal": gens_equal, "elements": len(raws), "products_of_two_contain_C": two,
            "C_times_generators_contain_C": closed, "every_element_nonzero_diagonal": diag}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", action="append", default=[])
    ap.add_argument("--blocks", action="store_true", help="recheck every block with the second encoding")
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--antichain", action="append", default=[])
    args = ap.parse_args()
    blocks, mats = exp014.load_blocks()
    out_path = HERE / "artifacts" / "certificate-check.json"
    report = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
    report.setdefault("blocks", {})
    report.setdefault("families", {})
    if args.blocks:
        for i, blk in enumerate(blocks):
            if blk.name in ("Y", "S"):
                ind = matrices_from_boundary(enumerate_boundary(blk))
                same = all(np.array_equal(ind[o], mats[i][o]) for o in SECTORS)
                report["blocks"][blk.name] = {"brute_force_enumeration_equal": same}
                print(f"{blk.name}: brute-force enumeration {'equal' if same else 'DIFFERENT'}", flush=True)
        from multiprocessing import Pool
        with Pool(args.workers) as pool:
            for name, same in pool.imap_unordered(_vertex_job, range(len(blocks))):
                report["blocks"].setdefault(name, {})["vertex_encoding_minisat_equal"] = same
                print(f"{name}: vertex encoding {'equal' if same else 'DIFFERENT'}", flush=True)
    for fam in args.family:
        z = np.load(exp014.HEAVY / f"certificate-{fam}.npz")
        gens = exp014.generators(blocks, mats, fam)
        stored = [row.tobytes() for row in z["generators"]]
        gens_equal = [transfer.pack(g["mats"]) for g in gens] == stored
        elements = {row.tobytes() for row in z["elements"]}
        gm = [g["mats"] for g in gens]
        two = all(transfer.pack(imul(a, b)) in elements for a in gm for b in gm)
        closed, diag = True, True
        for raw in elements:
            c = transfer.unpack(raw)
            if not diagonal_nonzero(c):
                diag = False
            for g in gm:
                if transfer.pack(imul(c, g)) not in elements:
                    closed = False
        report["families"][fam] = {"generators_equal": gens_equal, "elements": len(elements),
                                   "products_of_two_in_C": two, "C_closed_under_generators": closed,
                                   "every_element_nonzero_diagonal": diag}
        print(fam, report["families"][fam], flush=True)
    for fam in args.antichain:
        report["families"][fam + "-antichain"] = check_antichain(fam, blocks, mats)
        print(fam, "antichain", report["families"][fam + "-antichain"], flush=True)
    (HERE / "artifacts" / "certificate-check.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
