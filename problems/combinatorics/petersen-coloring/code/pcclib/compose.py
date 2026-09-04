"""Counterexample-guided search over cubic graphs built from copies of the Petersen 4-pole F.

A composition has `k` disjoint copies of F (8 vertices, 10 internal edges, 4 semi-edges at four
distinct owner vertices) and `m` free vertices with three semi-edges each. A perfect matching of
the semi-edges defines a cubic multigraph; the join formula excludes loops and double edges.
The search alternates a join-formula solve, a structural check (connected, bridgeless), and a
Petersen-colorability decision on the candidate; every learned clause is sound and logged with
its witness so the final exhaustion claim can be audited.
"""

from __future__ import annotations

import itertools
import json
import time
from pathlib import Path

from .cnf import CNF
from .graphs import Graph, petersen, petersen_minus_adjacent_pair
from . import checkers, encoders, invariants, solver

F_GRAPH, F_OWNERS = petersen_minus_adjacent_pair()
F_ADJ = F_GRAPH.adjacency()


def f_semiedge_automorphisms() -> list[tuple[int, ...]]:
    """Permutations of the four owner positions induced by automorphisms of F (as a graph)."""
    n = F_GRAPH.n
    adj = [set(a) for a in F_ADJ]
    owners = list(F_OWNERS)
    perms = []
    for perm in itertools.permutations(range(n)):
        if all(perm[o] in owners for o in owners) and all(
            perm[w] in adj[perm[v]] for v in range(n) for w in adj[v]
        ):
            perms.append(tuple(owners.index(perm[o]) for o in owners))
    return sorted(set(perms))


class Composition:
    def __init__(self, k: int, m: int):
        self.k, self.m = k, m
        # semi-edge ids: F copy i, position p -> 4*i + p ; free vertex u, slot s -> 4k + 3u + s
        self.n_semi = 4 * k + 3 * m
        self.pairs: list[tuple[int, int]] = []
        for a, b in itertools.combinations(range(self.n_semi), 2):
            if self.admissible(a, b):
                self.pairs.append((a, b))
        self.pair_index = {p: i for i, p in enumerate(self.pairs)}

    def unit(self, s: int) -> tuple[str, int, int]:
        if s < 4 * self.k:
            return ("F", s // 4, s % 4)
        r = s - 4 * self.k
        return ("V", r // 3, r % 3)

    def admissible(self, a: int, b: int) -> bool:
        ua, ub = self.unit(a), self.unit(b)
        if ua[0] == "V" and ub[0] == "V" and ua[1] == ub[1]:
            return False  # loop
        if ua[0] == "F" and ub[0] == "F" and ua[1] == ub[1]:
            oa, ob = F_OWNERS[ua[2]], F_OWNERS[ub[2]]
            if ob in F_ADJ[oa]:
                return False  # double edge inside a copy of F
        return True

    def join_formula(self) -> tuple[CNF, dict[tuple[int, int], int]]:
        f = CNF()
        j = {p: f.var(f"j_{p[0]}_{p[1]}") for p in self.pairs}
        for s in range(self.n_semi):
            lits = [j[p] for p in self.pairs if s in p]
            f.exactly_one(lits)
        # no double edge between two free vertices
        for u, v in itertools.combinations(range(self.m), 2):
            su = [4 * self.k + 3 * u + t for t in range(3)]
            sv = [4 * self.k + 3 * v + t for t in range(3)]
            cross = [j[(min(a, b), max(a, b))] for a in su for b in sv]
            for x, y in itertools.combinations(cross, 2):
                f.add(-x, -y)
        # symmetry: free vertices are interchangeable; fix the first semi-edge of free vertex u
        # to join a semi-edge with index at least that of free vertex u-1's first partner is
        # not encoded (kept simple and sound: no symmetry breaking on free vertices).
        return f, j

    def vertex_of_semiedge(self, s: int) -> int:
        kind, i, p = self.unit(s)
        if kind == "F":
            return 8 * i + F_OWNERS[p]
        return 8 * self.k + i

    def build(self, matching: list[tuple[int, int]]) -> tuple[Graph, dict[int, int]]:
        """Graph on 8k + m vertices; returns it and the map semi-edge -> edge index."""
        edges = []
        for i in range(self.k):
            for u, v in F_GRAPH.edges:
                edges.append((8 * i + u, 8 * i + v))
        join_edges = []
        for a, b in matching:
            join_edges.append((self.vertex_of_semiedge(a), self.vertex_of_semiedge(b)))
        all_edges = edges + join_edges
        es = sorted({(min(u, v), max(u, v)) for u, v in all_edges})
        if len(es) != len(all_edges):
            raise ValueError("double edge")
        g = Graph.from_edges(es)
        index = {e: i for i, e in enumerate(g.edges)}
        semi_to_edge = {}
        for a, b in matching:
            u, v = self.vertex_of_semiedge(a), self.vertex_of_semiedge(b)
            semi_to_edge[a] = semi_to_edge[b] = index[(min(u, v), max(u, v))]
        return g, semi_to_edge

    def semiedges_of_vertices(self, vertices: set[int]) -> list[int]:
        return [s for s in range(self.n_semi) if self.vertex_of_semiedge(s) in vertices]


def label_variants(comp: Composition, labels: list[int]) -> list[list[int]]:
    """The labeling plus single-unit variants that are still valid gadget colorings."""
    out = [labels]
    for i in range(comp.k):
        base = labels[4 * i: 4 * i + 4]
        for perm in F_AUTS:
            if perm == (0, 1, 2, 3):
                continue
            lab = list(labels)
            for p in range(4):
                lab[4 * i + p] = base[perm[p]]
            out.append(lab)
    for u in range(comp.m):
        base = labels[4 * comp.k + 3 * u: 4 * comp.k + 3 * u + 3]
        for perm in itertools.permutations(range(3)):
            if perm == (0, 1, 2):
                continue
            lab = list(labels)
            for t in range(3):
                lab[4 * comp.k + 3 * u + t] = base[perm[t]]
            out.append(lab)
    return out


F_AUTS = f_semiedge_automorphisms()


def verify_witness_labels(comp: Composition, labels: list[int]) -> bool:
    """Independent check: the labels restricted to each gadget extend to a valid star map."""
    p = petersen()
    stars = {frozenset(s) for s in p.incidence()}
    # free vertices: three labels must form a star of P
    for u in range(comp.m):
        trip = labels[4 * comp.k + 3 * u: 4 * comp.k + 3 * u + 3]
        if len(set(trip)) != 3 or frozenset(trip) not in stars:
            return False
    # copies of F: the four boundary labels must extend to a P-coloring of F (decided by SAT
    # elsewhere); here we check membership in the precomputed P-coloring set of F
    for i in range(comp.k):
        if tuple(labels[4 * i: 4 * i + 4]) not in PCOL_F:
            return False
    return True


def pcol_f(work: Path) -> set[tuple[int, int, int, int]]:
    """P-coloring set of F: boundary label tuples of all Petersen colorings of F closed by
    the semi-edges' owners. Computed once by enumerating colorings of F with its four semi-edges
    attached to four pendant vertices... equivalently by solving the star constraints directly.
    """
    p = petersen()
    stars = [frozenset(s) for s in p.incidence()]
    pedges = p.edges
    adjP = [[j for j in range(15) if j != i and set(pedges[i]) & set(pedges[j])] for i in range(15)]
    inc = F_GRAPH.incidence()
    # brute force over edge maps is 15^10; instead use SAT once per boundary tuple is too slow;
    # do a backtracking search over the 10 internal edges with owner-star constraints.
    m = len(F_GRAPH.edges)
    result: set[tuple[int, int, int, int]] = set()
    order = list(range(m))
    assign = [-1] * m

    def consistent(e: int, lab: int) -> bool:
        for v in F_GRAPH.edges[e]:
            for e2 in inc[v]:
                if e2 != e and assign[e2] >= 0:
                    if assign[e2] == lab or lab not in adjP[assign[e2]]:
                        return False
        return True

    def rec(idx: int) -> None:
        if idx == m:
            # each internal vertex (degree 3) already forms a star (pairwise adjacent, distinct);
            # each owner (degree 2) has two adjacent distinct labels; the missing third edge of
            # that star is determined: the unique third edge at the common Petersen vertex.
            bl = []
            for o in F_OWNERS:
                a, b = [assign[e] for e in inc[o]]
                common = set(pedges[a]) & set(pedges[b])
                w = next(iter(common))
                third = next(t for t in range(15) if w in pedges[t] and t not in (a, b))
                bl.append(third)
            result.add(tuple(bl))
            return
        e = order[idx]
        for lab in range(15):
            if consistent(e, lab):
                assign[e] = lab
                rec(idx + 1)
                assign[e] = -1

    rec(0)
    _ = stars
    return result


PCOL_F: set[tuple[int, int, int, int]] = set()


def init_pcol(work: Path) -> None:
    global PCOL_F
    if not PCOL_F:
        PCOL_F = pcol_f(work)


def search(comp: Composition, work: Path, budget_s: float, max_iter: int, log) -> dict:
    """Run the CEGAR loop for one class. Returns a summary dict; appends to work/<class>.jsonl."""
    init_pcol(work)
    work.mkdir(parents=True, exist_ok=True)
    tag = f"k{comp.k}m{comp.m}"
    ledger = work / f"{tag}.jsonl"
    base, j = comp.join_formula()
    learned: list[tuple[int, ...]] = []
    witnesses = 0
    if ledger.exists():
        for line in ledger.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            learned.append(tuple(rec["clause"]))
    t0 = time.time()
    it = 0
    found = []
    status = "running"
    while True:
        if time.time() - t0 > budget_s or it >= max_iter:
            status = "budget"
            break
        f = CNF()
        f.nvars = base.nvars
        f.names = base.names
        f.clauses = list(base.clauses) + learned
        cnf_path = work / f"{tag}_join.cnf"
        f.write(cnf_path)
        rec = solver.solve(cnf_path, work / f"{tag}_join.drat", int(budget_s), want_proof=False)
        if rec["status"] == "UNSAT":
            # final certificate: re-solve with proof
            rec2 = solver.solve(cnf_path, work / f"{tag}_join.drat", int(budget_s), want_proof=True)
            status = "exhausted" if rec2.get("drat_trim_verified") else "exhausted-unverified"
            break
        if rec["status"] != "SAT":
            status = "solver-" + rec["status"]
            break
        model = set(rec["model"])
        matching = [p for p in comp.pairs if j[p] in model]
        it += 1
        g, semi_to_edge = comp.build(matching)
        comps = invariants.components(g)
        if len(comps) > 1:
            side = set(comps[0])
            inside = comp.semiedges_of_vertices(side)
            clause = tuple(j[(min(a, b), max(a, b))] for a in inside for b in range(comp.n_semi)
                           if b not in inside and (min(a, b), max(a, b)) in j)
            learned.append(clause)
            ledger.open("a", encoding="utf-8").write(json.dumps({"it": it, "kind": "disconnected", "side": sorted(side), "clause": list(clause)}) + "\n")
            continue
        cut = invariants.cyclic_edge_cut_below(g, 2)  # a bridge that separates cycles; in a
        # cubic graph every bridge separates two cyclic sides, so this finds bridges
        if cut is not None:
            e = cut[0]
            u, v = g.edges[e]
            side = set(invariants.components(g, {e})[0])
            inside = comp.semiedges_of_vertices(side)
            bridge_pair = next(p for p in matching if semi_to_edge[p[0]] == e)
            clause = tuple(j[(min(a, b), max(a, b))] for a in inside for b in range(comp.n_semi)
                           if b not in inside and (min(a, b), max(a, b)) in j
                           and (min(a, b), max(a, b)) != bridge_pair)
            learned.append(clause)
            ledger.open("a", encoding="utf-8").write(json.dumps({"it": it, "kind": "bridge", "bridge": [u, v], "clause": list(clause)}) + "\n")
            continue
        # Petersen colorability of the candidate
        pf = encoders.petersen_coloring(g)
        pc = work / f"{tag}_cand.cnf"
        pf.write(pc)
        prec = solver.solve(pc, work / f"{tag}_cand.drat", int(budget_s), want_proof=False)
        if prec["status"] == "UNSAT":
            # counterexample candidate: certify with proof and the normal-5 route
            prec2 = solver.solve(pc, work / f"{tag}_cand_{len(found)}.drat", int(budget_s), want_proof=True)
            nf = encoders.normal_coloring(g, 5)
            nc = work / f"{tag}_cand_{len(found)}_normal5.cnf"
            nf.write(nc)
            nrec = solver.solve(nc, work / f"{tag}_cand_{len(found)}_normal5.drat", int(budget_s), want_proof=True)
            found.append({"it": it, "n": g.n, "edges": [list(e) for e in g.edges], "digest": g.digest(),
                          "petersen_verified": prec2.get("drat_trim_verified"), "normal5_status": nrec["status"],
                          "normal5_verified": nrec.get("drat_trim_verified"), "matching": matching})
            log(f"  COUNTEREXAMPLE candidate at iteration {it}: n={g.n} digest={g.digest()[:16]} petersen_verified={prec2.get('drat_trim_verified')} normal5={nrec['status']}")
            (work / f"{tag}_found_{len(found)-1}.edgelist").write_text("\n".join(f"{u} {v}" for u, v in g.edges) + "\n", encoding="utf-8")
            clause = tuple(-j[p] for p in matching)
            learned.append(clause)
            ledger.open("a", encoding="utf-8").write(json.dumps({"it": it, "kind": "counterexample", "digest": g.digest(), "clause": list(clause)}) + "\n")
            continue
        if prec["status"] != "SAT":
            status = "candidate-" + prec["status"]
            break
        pmodel = set(prec["model"])
        images = checkers.edge_color_map(pmodel, pf.names, len(g.edges), 15, prefix="y")
        assert checkers.petersen_defect(g, images) == 0
        labels = [images[semi_to_edge[s]] for s in range(comp.n_semi)]
        added = 0
        for lab in label_variants(comp, labels):
            assert verify_witness_labels(comp, lab)
            clause = tuple(j[p] for p in comp.pairs if lab[p[0]] != lab[p[1]])
            if not clause:
                # every admissible pair carries equal labels: this coloring colors EVERY
                # composition of the class, so the class is exhausted by a single witness
                ledger.open("a", encoding="utf-8").write(json.dumps({"it": it, "kind": "universal-coloring", "labels": lab}) + "\n")
                status = "exhausted-universal"
                break
            learned.append(clause)
            added += 1
        if status == "exhausted-universal":
            break
        witnesses += 1
        ledger.open("a", encoding="utf-8").write(json.dumps({"it": it, "kind": "coloring", "labels": labels, "variants": added, "clause": [j[p] for p in comp.pairs if labels[p[0]] != labels[p[1]]]}) + "\n")
        if it % 25 == 0:
            log(f"  {tag}: iteration {it}, learned {len(learned)} clauses, {len(found)} found, {round(time.time()-t0)} s")
    return {"class": tag, "k": comp.k, "m": comp.m, "n": 8 * comp.k + comp.m, "status": status, "iterations": it,
            "learned": len(learned), "witnesses": witnesses, "found": found, "seconds": round(time.time() - t0, 1)}
