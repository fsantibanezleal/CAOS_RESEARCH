"""Planarity certificates and their independent checker (EXP-007, claim R3).

Two layers, kept apart on purpose:

* the CHECKERS (`trace_faces`, `check_planar_certificate`, `check_kuratowski_certificate`) are plain Python.
  They never import or call a planarity solver and trust nothing from one but the certificate it hands over:
  a rotation system for a planar answer, a Kuratowski subgraph for a non-planar answer;
* the SOLVER wrapper (`decide_planarity`) calls `networkx.check_planarity(G, counterexample=True)`, turns its
  answer into a certificate and hands it to the checker.

The graph is the simple undirected graph of the instance arcs (parallel arcs merged, which does not change
planarity; loops dropped). Vertex and edge names are strings.
"""

from __future__ import annotations

from typing import Iterable, Mapping, Sequence

Edge = tuple[str, str]


def _norm_edges(edges: Iterable[Edge]) -> set[frozenset[str]]:
    out: set[frozenset[str]] = set()
    for u, v in edges:
        if u != v:
            out.add(frozenset((str(u), str(v))))
    return out


def _adjacency(vertices: Iterable[str], edges: set[frozenset[str]]) -> dict[str, set[str]]:
    adj: dict[str, set[str]] = {str(v): set() for v in vertices}
    for e in edges:
        a, b = tuple(e)
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    return adj


def _components(adj: Mapping[str, set[str]]) -> list[list[str]]:
    seen: set[str] = set()
    comps: list[list[str]] = []
    for start in sorted(adj):
        if start in seen:
            continue
        stack, comp = [start], []
        seen.add(start)
        while stack:
            v = stack.pop()
            comp.append(v)
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        comps.append(sorted(comp))
    return comps


# ---------------------------------------------------------------------------------------------------
# Rotation systems: face tracing and the Euler check
# ---------------------------------------------------------------------------------------------------


def trace_faces(rotation: Mapping[str, Sequence[str]]) -> list[list[tuple[str, str]]]:
    """Faces of a rotation system. Convention of the repository certificate: from dart (u, v) the next
    dart is (v, w) with w the predecessor of u in the clockwise rotation at v. Every dart is used once."""
    position = {v: {w: i for i, w in enumerate(ws)} for v, ws in rotation.items()}
    unused = {(u, v) for v, ws in rotation.items() for u in ws}
    faces: list[list[tuple[str, str]]] = []
    for start in sorted(unused):
        if start not in unused:
            continue
        face = []
        dart = start
        while dart in unused:
            unused.discard(dart)
            face.append(dart)
            u, v = dart
            ws = rotation[v]
            dart = (v, ws[(position[v][u] - 1) % len(ws)])
        faces.append(face)
    return faces


def check_planar_certificate(
    vertices: Iterable[str], edges: Iterable[Edge], rotation: Mapping[str, Sequence[str]]
) -> dict:
    """Accept a rotation system only if it is a combinatorial embedding of exactly this graph with
    V - E + F = 2 on every connected component (genus 0). Returns a dict with ``ok``, ``reason``,
    totals ``V``, ``E``, ``F``, ``components`` and a ``per_component`` list."""
    eset = _norm_edges(edges)
    adj = _adjacency([str(v) for v in vertices], eset)
    result: dict = {"ok": False, "reason": "", "V": len(adj), "E": len(eset), "F": None,
                    "components": len(_components(adj)), "per_component": []}
    if set(rotation) != set(adj):
        result["reason"] = "rotation system and graph have different vertex sets"
        return result
    for v, ws in rotation.items():
        if len(set(ws)) != len(ws):
            result["reason"] = f"repeated neighbour in the rotation at {v}"
            return result
        if set(ws) != adj[v]:
            result["reason"] = f"rotation at {v} is not the neighbour set of the graph"
            return result
    faces = trace_faces(rotation)
    comp_of: dict[str, int] = {}
    comps = _components(adj)
    for i, comp in enumerate(comps):
        for v in comp:
            comp_of[v] = i
    face_count = [0] * len(comps)
    for face in faces:
        face_count[comp_of[face[0][0]]] += 1
    total_f = 0
    all_ok = True
    for i, comp in enumerate(comps):
        n_v = len(comp)
        n_e = sum(len(adj[v]) for v in comp) // 2
        n_f = face_count[i] if n_e > 0 else 1  # an isolated vertex has the one outer face
        euler = n_v - n_e + n_f
        all_ok &= euler == 2
        total_f += n_f
        result["per_component"].append({"V": n_v, "E": n_e, "F": n_f, "euler": euler})
    result["F"] = total_f
    result["ok"] = all_ok
    result["reason"] = "genus 0 on every component" if all_ok else "V - E + F != 2 on a component (genus > 0)"
    return result


# ---------------------------------------------------------------------------------------------------
# Kuratowski subgraphs
# ---------------------------------------------------------------------------------------------------


def check_kuratowski_certificate(
    vertices: Iterable[str], edges: Iterable[Edge], sub_edges: Iterable[Edge]
) -> dict:
    """Accept a subgraph only if (1) every vertex and edge of it is in the graph, and (2) suppressing its
    degree-2 vertices gives a simple graph isomorphic to K5 or K3,3. Returns ``ok``, ``type``
    ('K5' or 'K3,3'), ``suppressed_vertices`` and the reduced ``core_edges``."""
    gv = {str(v) for v in vertices}
    ge = _norm_edges(edges)
    se = _norm_edges(sub_edges)
    res: dict = {"ok": False, "reason": "", "type": None, "suppressed_vertices": 0, "core_edges": []}
    if not se:
        res["reason"] = "empty subgraph"
        return res
    for e in se:
        if e not in ge:
            res["reason"] = f"edge {sorted(e)} is not an edge of the graph"
            return res
        if not e <= gv:
            res["reason"] = f"edge {sorted(e)} has a vertex outside the graph"
            return res
    adj = _adjacency([], se)
    suppressed = 0
    while True:
        v = next((u for u in sorted(adj) if len(adj[u]) == 2), None)
        if v is None:
            break
        a, b = sorted(adj[v])
        if b in adj[a]:
            res["reason"] = "suppressing a degree-2 vertex would create a parallel edge"
            return res
        adj[a].discard(v)
        adj[b].discard(v)
        adj[a].add(b)
        adj[b].add(a)
        del adj[v]
        suppressed += 1
    res["suppressed_vertices"] = suppressed
    degrees = sorted(len(ns) for ns in adj.values())
    n = len(adj)
    res["core_edges"] = sorted(sorted(e) for e in {frozenset((u, w)) for u, ns in adj.items() for w in ns})
    if n == 5 and degrees == [4] * 5:
        res["ok"], res["type"], res["reason"] = True, "K5", "subdivision of K5"
        return res
    if n == 6 and degrees == [3] * 6:
        colour: dict[str, int] = {}
        start = next(iter(sorted(adj)))
        colour[start] = 0
        stack = [start]
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if w not in colour:
                    colour[w] = 1 - colour[u]
                    stack.append(w)
                elif colour[w] == colour[u]:
                    res["reason"] = "reduced core is not bipartite"
                    return res
        if len(colour) == 6 and sorted(colour.values()) == [0, 0, 0, 1, 1, 1]:
            res["ok"], res["type"], res["reason"] = True, "K3,3", "subdivision of K3,3"
            return res
        res["reason"] = "reduced core is cubic on 6 vertices but not K3,3"
        return res
    res["reason"] = f"reduced core has {n} vertices with degrees {degrees}: not K5 and not K3,3"
    return res


# ---------------------------------------------------------------------------------------------------
# The solver, wrapped
# ---------------------------------------------------------------------------------------------------


def decide_planarity(vertices: Sequence[str], edges: Iterable[Edge]) -> dict:
    """Run networkx.check_planarity with a counterexample and check the certificate it returns."""
    import networkx as nx

    eset = _norm_edges(edges)
    g = nx.Graph()
    g.add_nodes_from(str(v) for v in vertices)
    g.add_edges_from(tuple(sorted(e)) for e in eset)
    planar, cert = nx.check_planarity(g, counterexample=True)
    vs = list(g.nodes())
    es = [tuple(e) for e in g.edges()]
    if planar:
        rotation = {v: list(cert.neighbors_cw_order(v)) for v in g.nodes()}
        check = check_planar_certificate(vs, es, rotation)
        return {"planar": True, "certificate_ok": bool(check["ok"]), "certificate": "rotation system",
                "V": check["V"], "E": check["E"], "F": check["F"], "components": check["components"],
                "check": check, "rotation": rotation}
    sub = [tuple(e) for e in cert.edges()]
    check = check_kuratowski_certificate(vs, es, sub)
    return {"planar": False, "certificate_ok": bool(check["ok"]), "certificate": "Kuratowski subgraph",
            "kuratowski_type": check["type"], "kuratowski_edges": sorted(sorted(e) for e in sub),
            "suppressed_vertices": check["suppressed_vertices"], "check": check}
