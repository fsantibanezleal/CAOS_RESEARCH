"""Cut-space charges (context/2026-10-06-charges.md).

The charge of a multiset of labels (edges of the Petersen graph P) is its class modulo the cut space
of P. A class is identified by its signature: the inner products with a basis of the cycle space,
which is the orthogonal complement of the cut space, so the signature is a complete class
invariant. The 64 classes fall into six Aut(P)-orbits named by size and coset-leader weight:
0 (1, 0), E (15, 1), D3 (15, 2), D2 (30, 2), T1 (1, 3), T2 (2, 3).
"""

from __future__ import annotations

import itertools
from functools import lru_cache

from .graphs import petersen

M = 15


def _gf2_rank_basis(vectors: list[int]) -> list[int]:
    basis: list[int] = []
    for v in vectors:
        x = v
        for b in basis:
            x = min(x, x ^ b)
        if x:
            basis.append(x)
            basis.sort(reverse=True)
    return basis


@lru_cache(maxsize=1)
def cut_basis() -> tuple[int, ...]:
    p = petersen()
    inc = p.incidence()
    return tuple(_gf2_rank_basis([sum(1 << e for e in inc[v]) for v in range(p.n)]))


@lru_cache(maxsize=1)
def cycle_basis() -> tuple[int, ...]:
    """Basis of the orthogonal complement of the cut space (the cycle space of P)."""
    cuts = cut_basis()
    comp = [x for x in range(1 << M) if all(bin(x & c).count("1") % 2 == 0 for c in cuts)]
    basis = _gf2_rank_basis(comp)
    assert len(basis) == M - len(cuts) == 6
    return tuple(basis)


def signature(vec: int) -> tuple[int, ...]:
    return tuple(bin(vec & c).count("1") % 2 for c in cycle_basis())


def vec(labels) -> int:
    x = 0
    for t in labels:
        x ^= 1 << t
    return x


@lru_cache(maxsize=1)
def orbit_table() -> tuple[dict, dict]:
    """(orbit name of every signature, a representative label triple or pair per orbit)."""
    from . import automorphisms

    p = petersen()
    auts = automorphisms.automorphisms(p)
    idx = {e: i for i, e in enumerate(p.edges)}
    eperm = [[idx[(min(a[u], a[v]), max(a[u], a[v]))] for (u, v) in p.edges] for a in auts]
    sig_weight: dict[tuple, int] = {}
    sig_rep: dict[tuple, tuple] = {}
    for w in range(0, 4):
        for combo in itertools.combinations(range(M), w):
            s = signature(vec(combo))
            if s not in sig_weight:
                sig_weight[s] = w
                sig_rep[s] = combo
    assert len(sig_weight) == 64

    def act(perm, s):
        return signature(vec(perm[t] for t in sig_rep[s]))

    name_of: dict[tuple, str] = {}
    reps: dict[str, tuple] = {}
    seen: set = set()
    for s in sorted(sig_weight, key=lambda s: (sig_weight[s], s)):
        if s in seen:
            continue
        orb = {act(pm, s) for pm in eperm}
        seen |= orb
        key = (len(orb), sig_weight[s])
        name = {(1, 0): "0", (15, 1): "E", (15, 2): "D3", (30, 2): "D2", (1, 3): "T1", (2, 3): "T2"}[key]
        for t in orb:
            name_of[t] = name
        reps[name] = sig_rep[s]
    return name_of, reps


ORBITS = ("0", "E", "D3", "D2", "T1", "T2")
