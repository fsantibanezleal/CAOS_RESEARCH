"""EXP-008: middle gadgets from the 286 order-13 MNH graphs with a universal vertex (HMB-007 step 1).

CPU only, deterministic (no randomness). Reuses EXP-003's instrument (gadgets.py, gate_zhan.py) without editing it.
Steps: gate 1 (Zhan's A_18), gate 2 (the order-12 gadget artifact of EXP-003 reproduced), the input check of the 286
graphs (decoded, order 13, pairwise non-isomorphic, universal vertex, MNH), Q1 (every order-13 gadget by the two
methods; does any have a longest middle path omitting a non-clique set), and Q2 (the triple search, with direct
verification of every candidate) only when Q1 is positive.

Usage (from the repository root): python problems/combinatorics/hoa-mnh/experiments/EXP-008-order13-gadgets/run.py
Exit 0 when Q1 (and Q2 if triggered) is decided; nonzero on a failed gate, a failed input check, a method
disagreement or a missing input.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPS = HERE.parent
EXP003 = EXPS / "EXP-003-gadget-search"
ART = HERE / "artifacts"
INPUT13 = EXPS / "EXP-007-order-13-universal-last" / "artifacts" / "mnh-n13-caseA.txt"
CENSUS_DIRS = [EXPS / "EXP-001-mnh-census" / "artifacts", EXPS / "EXP-002-order-12" / "artifacts"]
PROCESSES = 4

sys.path.insert(0, str(EXP003))
from gadgets import bt_invariants, connected, decode, dp_invariants, is_clique  # noqa: E402


# --- inputs ---------------------------------------------------------------------------------------------
def read_graph6(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"missing input: {path}")
    return [ln.split()[0] for ln in path.read_text(encoding="utf-8").split("\n") if ln.strip()]


def load_order13(path: Path = INPUT13) -> list[str]:
    return read_graph6(path)


def census_file(n: int) -> Path:
    for d in CENSUS_DIRS:
        p = d / f"mnh-n{n}.txt"
        if p.exists():
            return p
    raise FileNotFoundError(f"missing census artifact for order {n}")


# --- exact graph predicates -----------------------------------------------------------------------------
def ham_ends(n: int, adj, s: int) -> int:
    """Bitmask of the vertices v such that the graph has a Hamilton path from s to v (subset DP, exact)."""
    am = [sum(1 << w for w in adj[v]) for v in range(n)]
    full = (1 << n) - 1
    ends = {1 << s: 1 << s}
    for mask in range(1, full + 1):
        if not (mask >> s) & 1 or mask == 1 << s:
            continue
        e = 0
        for w in range(n):
            if w != s and (mask >> w) & 1:
                prev = ends.get(mask ^ (1 << w), 0)
                if prev & am[w]:
                    e |= 1 << w
        if e:
            ends[mask] = e
    return ends.get(full, 0)


def is_mnh(n: int, adj) -> bool:
    """Non-Hamiltonian, and every non-edge closes a Hamilton cycle (a Hamilton path joins its ends)."""
    ends0 = ham_ends(n, adj, 0)
    if any(w in adj[0] for w in range(n) if (ends0 >> w) & 1):
        return False  # Hamiltonian
    for u in range(n):
        e = ham_ends(n, adj, u)
        for v in range(u + 1, n):
            if v not in adj[u] and not (e >> v) & 1:
                return False
    return True


def universal_vertices(n: int, adj) -> list[int]:
    return [v for v in range(n) if len(adj[v]) == n - 1]


def pairwise_non_isomorphic(g6s: list[str]) -> bool:
    """Weisfeiler-Lehman hash as a filter, exact isomorphism test on every collision."""
    import networkx as nx

    buckets: dict[str, list] = {}
    for g6 in g6s:
        g = nx.from_graph6_bytes(g6.encode())
        h = nx.weisfeiler_lehman_graph_hash(g, iterations=4)
        for other in buckets.setdefault(h, []):
            if nx.is_isomorphic(g, other):
                return False
        buckets[h].append(g)
    return True


def input_check(g6s: list[str]) -> dict:
    decoded = [decode(g) for g in g6s]
    return {
        "graphs": len(g6s),
        "distinct_strings": len(set(g6s)),
        "all_order_13": all(n == 13 for n, _ in decoded),
        "pairwise_non_isomorphic": pairwise_non_isomorphic(g6s),
        "all_have_universal_vertex": all(universal_vertices(n, a) for n, a in decoded),
        "all_mnh": all(is_mnh(n, a) for n, a in decoded),
    }


# --- gadgets --------------------------------------------------------------------------------------------
def gadgets_of(g6: str):
    """Every gadget (X, x) of the graph (EXP-003's admissibility and record format); both methods run."""
    n, adjX = decode(g6)
    out, disagreements = [], 0
    for x in range(n):
        rest = [v for v in range(n) if v != x]
        idx = {v: i for i, v in enumerate(rest)}
        m = n - 1
        adj = [set(idx[w] for w in adjX[v] if w != x) for v in rest]
        N = sorted(idx[w] for w in adjX[x])
        if not connected(adj, range(m)) or is_clique(adj, range(m)) or len(N) == m or len(N) < 2:
            continue
        a = dp_invariants(m, adj, N)
        b = bt_invariants(m, adj, N)
        if a != b:
            disagreements += 1
        traceable, homog, starts, d, nonclique = a
        univ = [u for u in N if all(w in adj[u] for w in N if w != u)]
        out.append({"g6": g6, "n": n, "x": x, "m": m, "traceable": traceable, "homog": homog,
                    "univ": univ, "trace_from_univ": all((starts >> u) & 1 for u in univ),
                    "d": d, "nonclique_omit": nonclique})
    return out, disagreements


def all_gadgets(g6s: list[str], processes: int = PROCESSES):
    if processes > 1:
        with Pool(processes) as pool:
            parts = pool.map(gadgets_of, g6s, chunksize=4)
    else:
        parts = [gadgets_of(g) for g in g6s]
    recs, dis = [], 0
    for r, d in parts:
        recs.extend(r)
        dis += d
    return recs, dis


# --- gates ----------------------------------------------------------------------------------------------
def gate1() -> dict:
    p = subprocess.run([sys.executable, str(EXP003 / "gate_zhan.py")], capture_output=True, text=True)
    return {"exit_code": p.returncode, "output": p.stdout.strip().splitlines(), "pass": p.returncode == 0}


def census_g6s(max_order: int) -> list[str]:
    out: list[str] = []
    for n in range(4, max_order + 1):
        out += read_graph6(census_file(n))
    return out


def gate2() -> dict:
    recs, dis = all_gadgets(census_g6s(12))
    ref = json.loads((EXP003 / "artifacts" / "gadgets-to12.json").read_text(encoding="utf-8"))
    return {"recomputed": len(recs), "reference": len(ref), "identical_records": recs == ref,
            "method_disagreements": dis, "pass": recs == ref and len(recs) == 2796 and dis == 0}


# --- triple search (Q2) and direct verification ---------------------------------------------------------
def triple_search(gadgets: list[dict]):
    ok = [g for g in gadgets if g["traceable"] and g["trace_from_univ"]]
    mids = [g for g in ok if g["nonclique_omit"]]
    best = None
    for mid in mids:
        for e1 in ok:
            for e2 in ok:
                trio = (mid, e1, e2)
                if e1["d"] < mid["d"] or e2["d"] < mid["d"]:
                    continue
                if sum(bool(g["univ"]) for g in trio) > 1 or sum(g["homog"] for g in trio) < 2:
                    continue
                order = 3 + sum(g["m"] for g in trio)
                if best is None or order < best[0]:
                    best = (order, trio)
    return best, len(ok), len(mids)


def gadget_graph(g: dict):
    n, adjX = decode(g["g6"])
    x = g["x"]
    rest = [v for v in range(n) if v != x]
    idx = {v: i for i, v in enumerate(rest)}
    adj = [set(idx[w] for w in adjX[v] if w != x) for v in rest]
    N = sorted(idx[w] for w in adjX[x])
    return adj, N


def build_join(trio):
    """K_1 join M, M = three gadgets glued through the adjacent cut {x, y} (each cut vertex adjacent to the
    gadget's N); returns the adjacency list, the vertex z of the join and the vertex sets of the gadgets."""
    adj: list[set[int]] = [{1}, {0}]
    parts = []
    for g in trio:
        gadj, N = gadget_graph(g)
        off = len(adj)
        parts.append(list(range(off, off + len(gadj))))
        adj.extend(set(off + w for w in a) for a in gadj)
        for p in N:
            for c in (0, 1):
                adj[c].add(off + p)
                adj[off + p].add(c)
    z = len(adj)
    adj.append(set(range(z)))
    for v in range(z):
        adj[v].add(z)
    return adj, z, parts


def longest_cycle(adj):
    """Exhaustive longest cycle (DFS from each least vertex); returns (length, vertex list)."""
    n = len(adj)
    best = [0, []]
    for s in range(n):
        path, seen = [s], {s}

        def dfs(v):
            for w in adj[v]:
                if w == s and len(path) >= 3 and len(path) > best[0]:
                    best[0], best[1] = len(path), list(path)
                if w > s and w not in seen:
                    seen.add(w)
                    path.append(w)
                    dfs(w)
                    path.pop()
                    seen.remove(w)

        dfs(s)
    return best[0], best[1]


def hamilton_path_dfs(adj, s, t) -> bool:
    n = len(adj)
    seen = {s}

    def dfs(v):
        if len(seen) == n:
            return v == t
        for w in adj[v]:
            if w not in seen and (w != t or len(seen) == n - 1):
                seen.add(w)
                if dfs(w):
                    return True
                seen.remove(w)
        return False

    return dfs(s)


def verify_candidate(adj, claimed_cycle: int) -> dict:
    """Direct checks of the hypothesis' Validation: the join is MNH (non-Hamiltonian, every non-edge closes a
    Hamilton cycle), its circumference equals the claim, and the residual of a longest cycle is not complete."""
    n = len(adj)
    pairs_ok = all(hamilton_path_dfs(adj, u, v) for u in range(n) for v in range(u + 1, n) if v not in adj[u])
    length, cyc = longest_cycle(adj)
    residual = [v for v in range(n) if v not in set(cyc)]
    res_ok = not is_clique(adj, residual)
    return {"order": n, "nonedge_pairs_have_hamilton_path": pairs_ok, "circumference": length,
            "claimed_cycle": claimed_cycle, "non_hamiltonian": length < n, "residual_not_complete": res_ok,
            "verified": pairs_ok and length < n and length == claimed_cycle and res_ok}


# --- main -----------------------------------------------------------------------------------------------
def main() -> int:
    ART.mkdir(exist_ok=True)
    log: list[str] = []

    def say(msg):
        print(msg, flush=True)
        log.append(msg)

    def flush_log():
        (ART / "run-log.txt").write_text("\n".join(log) + "\n", encoding="utf-8")

    t0 = time.time()
    try:
        g6s = load_order13()
        for n in range(4, 13):
            census_file(n)
    except FileNotFoundError as e:
        print(f"MISSING INPUT: {e}")
        return 3
    g1 = gate1()
    say(f"gate 1 (Zhan A_18): {'PASS' if g1['pass'] else 'FAIL'}; " + " | ".join(g1["output"]))
    g2 = gate2()
    say(f"gate 2 (order-12 reproduction): {'PASS' if g2['pass'] else 'FAIL'}; {json.dumps(g2)}")
    (ART / "gates.json").write_text(json.dumps({"gate1": g1, "gate2": g2}, indent=1) + "\n", encoding="utf-8")
    if not (g1["pass"] and g2["pass"]):
        flush_log()
        return 1
    chk = input_check(g6s)
    say(f"input check: {json.dumps(chk)}")
    if not (chk["graphs"] == 286 and chk["distinct_strings"] == 286 and chk["all_order_13"]
            and chk["pairwise_non_isomorphic"] and chk["all_have_universal_vertex"] and chk["all_mnh"]):
        flush_log()
        return 1
    recs, dis = all_gadgets(g6s)
    (ART / "gadgets-n13.json").write_text(json.dumps(recs, indent=1) + "\n", encoding="utf-8")
    nonclique = [g for g in recs if g["nonclique_omit"]]
    dh = {str(k): sum(g["d"] == k for g in recs) for k in sorted({g["d"] for g in recs})}
    say(f"Q1: {len(recs)} gadgets, method disagreements {dis}, traceable {sum(g['traceable'] for g in recs)}, "
        f"d histogram {json.dumps(dh)}, gadgets with a non-clique omitted set {len(nonclique)}")
    if dis:
        flush_log()
        return 1
    summary = {"gadgets": len(recs), "dp_backtracking_disagreements": dis, "d_histogram": dh,
               "middle_candidates_nonclique": len(nonclique), "q1_positive": bool(nonclique)}
    if nonclique:
        pool_, _ = all_gadgets(census_g6s(12))
        pool_ = pool_ + recs
        best, nok, nmid = triple_search(pool_)
        summary.update({"q2_pool": len(pool_), "q2_traceable_ok": nok, "q2_middles": nmid,
                        "best_order": None if best is None else best[0],
                        "best_triple": None if best is None else list(best[1])})
        if best is not None:
            adj, z, parts = build_join(best[1])
            claimed = best[0] - min(g["d"] for g in best[1])
            summary["claimed_cycle"] = claimed
            summary["verification"] = verify_candidate(adj, claimed)
        say(f"Q2: best order {summary.get('best_order')}; verification {summary.get('verification')}")
    (ART / "triples-n13.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    say(f"done in {time.time() - t0:.0f} s; Q1 {'POSITIVE' if nonclique else 'NEGATIVE'}")
    flush_log()
    return 0


if __name__ == "__main__":
    sys.exit(main())
