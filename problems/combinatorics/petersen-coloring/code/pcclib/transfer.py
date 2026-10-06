"""Transfer relations of 6-poles over the charge sectors, and their semigroups (EXP-014).

A block is a 6-pole with an ordered left connector L and an ordered right connector R (three
dangling ends each). Its transfer relation is the set of pairs (phi(L), phi(R)) of label triples
that a map into E(P) with every vertex good puts on the two connectors. By the Gauss law both
triples have the same charge class, and permuting the ends of a connector keeps the class, so the
relation is block diagonal over the 64 classes; by Aut(P)-equivariance the blocks over one orbit are
conjugate. A block is therefore stored as six boolean sector matrices, one per orbit, with rows and
columns indexed by the ordered label triples of the orbit's representative class
(context/2026-10-06-charges.md, section "Transfer relations").

A ring joins the right connector of block i to the left connector of block i+1 through a junction
permutation pi (end j of R to end pi[j] of L) and closes the cycle. It is Petersen colorable if and
only if some sector of the product T_1 Pi_1 ... T_t Pi_t has a nonzero diagonal entry.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from functools import lru_cache

import numpy as np

from . import charges
from .graphs import Graph
from .poles import Pole, check_pole, pole_formula

SECTORS = charges.ORBITS
PERMS = tuple(itertools.permutations(range(3)))


@lru_cache(maxsize=1)
def sector_states() -> dict[str, tuple[tuple[int, int, int], ...]]:
    """Ordered label triples of each orbit's representative class (sizes 60, 67, 48, 48, 30, 60)."""
    _, reps = charges.orbit_table()
    out = {}
    for o in SECTORS:
        sig = charges.signature(charges.vec(reps[o]))
        out[o] = tuple(t for t in itertools.product(range(15), repeat=3) if charges.signature(charges.vec(t)) == sig)
    return out


@lru_cache(maxsize=None)
def junction_matrix(o: str, pi: tuple[int, int, int]) -> np.ndarray:
    """Pi[y, x] = 1 iff x[pi[j]] = y[j] for every j (the labels carried across the junction)."""
    st = sector_states()[o]
    idx = {t: i for i, t in enumerate(st)}
    m = np.zeros((len(st), len(st)), dtype=bool)
    for i, y in enumerate(st):
        x = [0, 0, 0]
        for j in range(3):
            x[pi[j]] = y[j]
        m[i, idx[tuple(x)]] = True
    return m


@dataclass
class Block:
    name: str
    pole: Pole
    left: tuple[int, int, int]
    right: tuple[int, int, int]

    def reversed(self) -> "Block":
        return Block(self.name + "^r", self.pole, self.right, self.left)


def sector_matrices(block: Block) -> dict[str, np.ndarray]:
    """Exact sector matrices of a block. Every entry is a model checked from the definition."""
    from pysat.solvers import Solver

    f, y = pole_formula(block.pole)
    states = sector_states()
    mats: dict[str, np.ndarray] = {}
    with Solver(name="cadical153", bootstrap_with=f.clauses) as s:
        for o in SECTORS:
            st = states[o]
            idx = {t: i for i, t in enumerate(st)}
            m = np.zeros((len(st), len(st)), dtype=bool)
            for i, a in enumerate(st):
                assume = [y[("d", block.left[k]), a[k]] for k in range(3)]
                sel = f.fresh()
                while s.solve(assumptions=assume + [sel]):
                    model = s.get_model()
                    pos = {lit for lit in model if lit > 0}
                    lab = {key: t for (key, t), var in y.items() if var in pos}
                    b = tuple(lab[("d", block.right[k])] for k in range(3))
                    if not check_pole(block.pole, lab) or b not in idx or tuple(lab[("d", block.left[k])] for k in range(3)) != a:
                        raise AssertionError(f"model failed the check in block {block.name}, sector {o}")
                    m[i, idx[b]] = True
                    s.add_clause([-sel] + [-y[("d", block.right[k]), b[k]] for k in range(3)])
                s.add_clause([-sel])
            mats[o] = m
    return mats


def transpose(mats: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    return {o: m.T.copy() for o, m in mats.items()}


def with_junction(mats: dict[str, np.ndarray], pi: tuple[int, int, int]) -> dict[str, np.ndarray]:
    return {o: bmul(m, junction_matrix(o, pi)) for o, m in mats.items()}


def bmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return (a.astype(np.float32) @ b.astype(np.float32)) > 0.5


def product(elems: list[dict[str, np.ndarray]]) -> dict[str, np.ndarray]:
    out = elems[0]
    for e in elems[1:]:
        out = {o: bmul(out[o], e[o]) for o in SECTORS}
    return out


def colorable_sectors(mats: dict[str, np.ndarray]) -> list[str]:
    """Sectors whose diagonal is nonzero (the charge orbits a closing ring can carry)."""
    return [o for o in SECTORS if bool(np.any(np.diagonal(mats[o])))]


def pack(mats: dict[str, np.ndarray]) -> bytes:
    return np.packbits(np.concatenate([mats[o].ravel() for o in SECTORS])).tobytes()


def unpack(raw: bytes) -> dict[str, np.ndarray]:
    sizes = [len(sector_states()[o]) for o in SECTORS]
    bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8))[: sum(n * n for n in sizes)].astype(bool)
    out, k = {}, 0
    for o, n in zip(SECTORS, sizes):
        out[o] = bits[k:k + n * n].reshape(n, n)
        k += n * n
    return out


def build_ring(word: list[tuple[Block, tuple[int, int, int]]]) -> Graph:
    """The cubic graph of a ring: block i's right end j joined to block i+1's left end pi[j].

    Raises ValueError when the ring is not simple (the sector algebra is exact for multigraphs
    too, but every graph claim of EXP-014 is about simple graphs)."""
    edges, vid, offset = [], [], 0
    for blk, _ in word:
        local = {v: offset + i for i, v in enumerate(blk.pole.kept)}
        vid.append(local)
        for e in blk.pole.internal:
            u, v = blk.pole.parent.edges[e]
            edges.append((local[u], local[v]))
        offset += len(blk.pole.kept)
    t = len(word)
    for i, (blk, pi) in enumerate(word):
        nxt = word[(i + 1) % t][0]
        for j in range(3):
            x = vid[i][blk.pole.dangling[blk.right[j]][0]]
            yv = vid[(i + 1) % t][nxt.pole.dangling[nxt.left[pi[j]]][0]]
            edges.append((x, yv))
    if len({(min(u, v), max(u, v)) for u, v in edges}) != len(edges) or any(u == v for u, v in edges):
        raise ValueError("the ring has a loop or parallel edges")
    return Graph.from_edges(edges)
