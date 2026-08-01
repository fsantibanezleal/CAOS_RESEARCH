"""Exact SLP enumeration cores (polynomial and integer) for the tau program.

Model (polynomial side): inputs {-1, 1, x}; gates +,-,* of fan-in 2; length
= number of gates. Free constant 0 is redundant given -1 (EXP-001 hypothesis
lemma 1). Polynomials are dense coefficient tuples, constant term first,
trailing zeros trimmed; the zero polynomial is ().

Model (integer side, Markstroem arXiv:1306.3091): start from 1; values kept
positive and distinct (normalization WLOG for optimal programs).

State = the SET of values computed so far (reached-set sufficiency: the
future depends only on the set); BFS by length with set-level dedup.
"""

import time

P_MINUS1 = (-1,)
P_ONE = (1,)
P_X = (0, 1)
INPUTS = (P_MINUS1, P_ONE, P_X)


def padd(a, b):
    n = max(len(a), len(b))
    c = [0] * n
    for i, v in enumerate(a):
        c[i] += v
    for i, v in enumerate(b):
        c[i] += v
    while c and c[-1] == 0:
        c.pop()
    return tuple(c)


def psub(a, b):
    n = max(len(a), len(b))
    c = [0] * n
    for i, v in enumerate(a):
        c[i] += v
    for i, v in enumerate(b):
        c[i] -= v
    while c and c[-1] == 0:
        c.pop()
    return tuple(c)


def pmul(a, b):
    if not a or not b:
        return ()
    c = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        if u:
            for j, v in enumerate(b):
                c[i + j] += u * v
    while c and c[-1] == 0:
        c.pop()
    return tuple(c)


def peval(f, v):
    acc = 0
    for c in reversed(f):
        acc = acc * v + c
    return acc


def divisors(n):
    n = abs(n)
    small, large = [], []
    d = 1
    while d * d <= n:
        if n % d == 0:
            small.append(d)
            if d != n // d:
                large.append(n // d)
        d += 1
    return small + large[::-1]


def integer_roots(f):
    """Distinct integer roots of nonzero f, exact (rational root theorem)."""
    if not f:
        raise ValueError("zero polynomial")
    m = 0
    while f[m] == 0:
        m += 1
    roots = set()
    if m > 0:
        roots.add(0)
    g = f[m:]
    if len(g) > 1:
        for d in divisors(g[0]):
            for r in (d, -d):
                if peval(g, r) == 0:
                    roots.add(r)
    return roots


def two_adic_valuations(roots):
    """Set of 2-adic valuations of the nonzero roots ('inf' excluded: 0 is
    reported separately by callers). Instrumentation for the Rojas
    valuation-spectrum view (N_2)."""
    vals = set()
    for r in roots:
        if r == 0:
            continue
        r = abs(r)
        v = 0
        while r % 2 == 0:
            r //= 2
            v += 1
        vals.add(v)
    return vals


def census_polynomials(max_depth, deadline=None, state_cap=5_000_000,
                       progress=None, return_frontier=False):
    """BFS census of the polynomial model.

    Returns (per_depth, first_seen, complete) where per_depth[d] carries
    state/new-poly counts, first_seen maps poly -> first depth (= tau of the
    poly among enumerated depths), complete[d] says depth d was exhausted.
    deadline: absolute time.time() kill; state_cap: memory guard.
    With return_frontier=True, returns a 4th element: the final frontier
    (dict of reached-set states at max_depth), for last-gate scans.
    """
    frontier = {(): None}
    first_seen = {}
    per_depth = {}
    complete = {}
    for depth in range(1, max_depth + 1):
        new_frontier = {}
        new_polys = set()
        aborted = False
        for state in frontier:
            operands = INPUTS + state
            n = len(operands)
            cand = set()
            for i in range(n):
                a = operands[i]
                for j in range(i, n):
                    b = operands[j]
                    cand.add(padd(a, b))
                    cand.add(pmul(a, b))
            for a in operands:
                for b in operands:
                    if a is not b:
                        cand.add(psub(a, b))
            for v in cand:
                if not v or v in operands:
                    continue
                ns = tuple(sorted(state + (v,)))
                new_frontier[ns] = None
                if v not in first_seen:
                    first_seen[v] = depth
                    new_polys.add(v)
            if (deadline and time.time() > deadline) or \
                    len(new_frontier) > state_cap:
                aborted = True
                break
        if aborted:
            complete[depth] = False
            per_depth[depth] = {"complete": False}
            break
        complete[depth] = True
        per_depth[depth] = {
            "complete": True,
            "states": len(new_frontier),
            "new_polynomials": len(new_polys),
        }
        if progress:
            progress(depth, per_depth[depth])
        frontier = new_frontier
    if return_frontier:
        return per_depth, first_seen, complete, frontier
    return per_depth, first_seen, complete


def last_gate_scan(frontier, known_polys, deadline=None, progress=None,
                   progress_every=50_000):
    """Exact z_max at depth d+1 given the EXHAUSTED depth-d frontier.

    Soundness (the last-gate lemma, EXP-003 hypothesis): any f with
    tau(f) = d+1 is the final gate of a length-(d+1) program whose first d
    gates form a normalized reached-set state, i.e. an element of
    `frontier`; so scanning one op over every state's operands enumerates
    every polynomial of tau exactly d+1 (results already in `known_polys`,
    the polys of tau <= d, are skipped). Memory stays O(frontier + distinct
    new polys); no depth-(d+1) states are stored.

    Returns (new_polys_set, complete_flag, states_scanned).
    """
    seen = set(known_polys)
    new_polys = set()
    complete = True
    count = 0
    for state in frontier:
        operands = INPUTS + state
        n = len(operands)
        for i in range(n):
            a = operands[i]
            for j in range(i, n):
                b = operands[j]
                v = padd(a, b)
                if v and v not in seen:
                    seen.add(v)
                    new_polys.add(v)
                v = pmul(a, b)
                if v and v not in seen:
                    seen.add(v)
                    new_polys.add(v)
        for a in operands:
            for b in operands:
                if a is not b:
                    v = psub(a, b)
                    if v and v not in seen:
                        seen.add(v)
                        new_polys.add(v)
        count += 1
        if progress and count % progress_every == 0:
            progress(count, len(new_polys))
        if deadline and time.time() > deadline:
            complete = False
            break
    return new_polys, complete, count


def census_integers(max_depth, deadline=None, state_cap=5_000_000,
                    progress=None):
    """BFS census of Markstroem's integer model. Returns per-depth
    {reached, interval, states, complete} rows (reached counts include 1)."""
    frontier = {(): None}
    reached = {1}
    results = {}
    for depth in range(1, max_depth + 1):
        new_frontier = {}
        aborted = False
        for state in frontier:
            operands = (1,) + state
            n = len(operands)
            cand = set()
            for i in range(n):
                a = operands[i]
                for j in range(i, n):
                    b = operands[j]
                    cand.add(a + b)
                    cand.add(a * b)
            for a in operands:
                for b in operands:
                    d = a - b
                    if d > 0:
                        cand.add(d)
            for v in cand:
                if v <= 0 or v in operands:
                    continue
                ns = tuple(sorted(state + (v,)))
                if ns not in new_frontier:
                    new_frontier[ns] = None
                reached.add(v)
            if (deadline and time.time() > deadline) or \
                    len(new_frontier) > state_cap:
                aborted = True
                break
        if aborted:
            results[depth] = {"complete": False}
            break
        m = 2
        while m + 1 in reached:
            m += 1
        interval = m if 2 in reached else 1
        results[depth] = {
            "complete": True,
            "reached": len(reached),
            "interval": interval,
            "states": len(new_frontier),
        }
        if progress:
            progress(depth, results[depth])
        frontier = new_frontier
    return results


def find_witness_program(target, max_depth):
    """Bounded DFS for one SLP (op list) whose value set contains target."""

    def dfs(state, depth, ops):
        operands = INPUTS + state
        if target in state:
            return ops
        if depth == max_depth:
            return None
        n = len(operands)
        seen_local = set()
        for i in range(n):
            for j in range(n):
                for opname in ("+", "-", "*"):
                    if opname in ("+", "*") and j < i:
                        continue
                    a, b = operands[i], operands[j]
                    if opname == "+":
                        v = padd(a, b)
                    elif opname == "*":
                        v = pmul(a, b)
                    else:
                        if i == j:
                            continue
                        v = psub(a, b)
                    if not v or v in operands or v in seen_local:
                        continue
                    seen_local.add(v)
                    res = dfs(
                        tuple(sorted(state + (v,))),
                        depth + 1,
                        ops + [(list(a), opname, list(b), list(v))],
                    )
                    if res is not None:
                        return res
        return None

    return dfs((), 0, [])
