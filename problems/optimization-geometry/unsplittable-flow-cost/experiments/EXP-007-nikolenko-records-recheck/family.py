"""Exact builders for EXP-007: instances from the JSON, family members from their symbolic description.

No float enters: expressions are parsed with ``ast`` into ``Fraction`` arithmetic and anything that is not an
integer literal, a name, + - * / or an integer power is refused. Instances are built with ufclib's own
constructor (which refuses floats); the JSON ``paths`` lists are never read.
"""

from __future__ import annotations

import ast
import operator
import re
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Mapping

PROBLEM_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROBLEM_ROOT / "code"))

from ufclib import Instance  # noqa: E402

_BIN = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


def eval_expr(expr: str, env: Mapping[str, F]) -> F:
    """Evaluate a rational expression (``^`` is a power) exactly; floats, calls and attributes are refused."""

    def ev(node: ast.AST) -> F:
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(node.value, int):
                raise ValueError(f"only integer literals are allowed, got {node.value!r}")
            return F(node.value)
        if isinstance(node, ast.Name):
            if node.id not in env:
                raise ValueError(f"unbound name {node.id!r}")
            return F(env[node.id])
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            val = ev(node.operand)
            return -val if isinstance(node.op, ast.USub) else val
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Pow):
                base, exp = ev(node.left), ev(node.right)
                if exp.denominator != 1:
                    raise ValueError("only integer exponents are allowed")
                return base ** int(exp)
            if type(node.op) in _BIN:
                return _BIN[type(node.op)](ev(node.left), ev(node.right))
        raise ValueError(f"unsupported expression element: {ast.dump(node)}")

    # the transcription writes "2t-t^2": make the implicit product of a literal and a name explicit
    text = re.sub(r"(?<![A-Za-z_0-9])(\d+)(?=[A-Za-z_(])", lambda m: m.group(1) + "*", expr).replace("^", "**")
    return ev(ast.parse(text, mode="eval"))


def sqrt41_bounds() -> tuple[F, F]:
    """Rational bounds lo < sqrt 41 < hi with hi - lo = 10^-9, verified by squaring."""
    lo, hi = F(6403124237, 10**9), F(6403124238, 10**9)
    if not (lo * lo < 41 < hi * hi):
        raise AssertionError("sqrt 41 bounds fail the squaring check")
    return lo, hi


def instance_from_entry(entry: Mapping) -> Instance:
    """The ufclib Instance of a concrete JSON entry (arcs, demands, source), values as exact strings."""
    arcs = [(a["tail"], a["head"], a["x"], a["cost"]) for a in entry["arcs"]]
    return Instance.build(source=entry["source_vertex"], demands=dict(entry["demands"]), arcs=arcs,
                          name=entry["id"])


# ---------------------------------------------------------------------------------------------------
# Four-interval family: evaluate the entry's own symbolic x and cost expressions
# ---------------------------------------------------------------------------------------------------


def four_interval_member(entry: Mapping, t: F, eps: F) -> Instance:
    """Member F(t, eps) of UF-4INT-FAMILY from its symbolic arcs, demands and (d, f) lists."""
    base = {"t": F(t), "eps": F(eps)}
    d = [eval_expr(s, base) for s in entry["x_symbols"]["d"]]
    f = [eval_expr(s, base) for s in entry["x_symbols"]["f"]]
    env = dict(base)
    for i in range(len(d)):
        env[f"d{i}"], env[f"f{i}"] = d[i], f[i]
    arcs = [(a["tail"], a["head"], eval_expr(a["x"], env), eval_expr(a["cost"], env)) for a in entry["arcs"]]
    demands = {name: eval_expr(expr, base) for name, expr in entry["demands"].items()}
    return Instance.build(source=entry["source_vertex"], demands=demands, arcs=arcs,
                          name=f"4INT t={t} eps={eps}")


def four_interval_closed_form(t: F, eps: F) -> F:
    """Paper I Lemma 4.6: C(t) - eps with C(t) = (1-t)^2 (1 + 4t - t^2), as transcribed in UF-4INT-FAMILY."""
    return (1 - t) ** 2 * (1 + 4 * t - t * t) - eps


# ---------------------------------------------------------------------------------------------------
# Generic interval builder (used for the ternary core)
# ---------------------------------------------------------------------------------------------------


def interval_instance(intervals, d, f, name: str = "") -> Instance:
    """Spine v0..v_{rmax+1}; terminal i has an early exit (v_l, t_i) carrying d_i (1 - f_i) at unit cost 1/d_i
    and a late exit (v_{r+1}, t_i) carrying d_i f_i at cost 0; spine arc j carries every terminal whose early
    path (j < l) or late path (j <= r) uses it. Conventions of Papers I to III as recorded in the
    transcription report."""
    p = max(r for _, r in intervals) + 1
    arcs = []
    for j in range(p):
        load = F(0)
        for (lo, hi), di, fi in zip(intervals, d, f):
            if j < lo:
                load += di * (1 - fi)
            if j <= hi:
                load += di * fi
        arcs.append((f"v{j}", f"v{j + 1}", load, F(0)))
    for i, ((lo, hi), di, fi) in enumerate(zip(intervals, d, f)):
        arcs.append((f"v{lo}", f"t{i}", di * (1 - fi), 1 / di))
        arcs.append((f"v{hi + 1}", f"t{i}", di * fi, F(0)))
    return Instance.build(source="v0", demands={f"t{i}": di for i, di in enumerate(d)}, arcs=arcs, name=name)


TERNARY_INTERVALS = ((0, 1), (0, 2), (1, 2))


def ternary_member(eta: F) -> Instance:
    """Ternary core at eta: d = (1, (3-eta)/4, 1), f = ((1+eta)/4, (1+eta)/2, (1+eta)/4), cost 1/d_i."""
    eta = F(eta)
    d = [F(1), (3 - eta) / 4, F(1)]
    f = [(1 + eta) / 4, (1 + eta) / 2, (1 + eta) / 4]
    return interval_instance(TERNARY_INTERVALS, d, f, name=f"ternary eta={eta}")


def ternary_closed_form(eta: F) -> F:
    return (3 - F(eta)) ** 2 / 8


# ---------------------------------------------------------------------------------------------------
# Builder validation: reproduce a concrete entry exactly (up to the entry's own common scales)
# ---------------------------------------------------------------------------------------------------


def reproduces_entry(inst: Instance, entry: Mapping) -> dict:
    """Does ``inst`` equal the concrete JSON entry arc by arc, up to one scale for flows and demands and one
    scale for costs? Returns {'ok', 'flow_scale', 'cost_scale', 'reason'} (scales exact)."""
    arcs = entry["arcs"]
    if len(arcs) != len(inst.arcs):
        return {"ok": False, "reason": f"arc counts differ: {len(inst.arcs)} vs {len(arcs)}"}
    e_arcs = [(a["tail"], a["head"], F(a["x"]), F(a["cost"])) for a in arcs]
    e_dem = {k: F(v) for k, v in entry["demands"].items()}
    if set(e_dem) != set(inst.demands) or inst.source != entry["source_vertex"]:
        return {"ok": False, "reason": "terminals or source differ"}
    flow_scale = next(e_dem[k] / inst.demands[k] for k in e_dem)
    cost_scale = None
    for a, (tail, head, x, cost) in zip(inst.arcs, e_arcs):
        if (a.tail, a.head) != (tail, head):
            return {"ok": False, "reason": f"arc {a.index}: endpoints differ"}
        if a.x * flow_scale != x:
            return {"ok": False, "reason": f"arc {a.index}: flow differs"}
        if cost == 0 or a.cost == 0:
            if cost != 0 or a.cost != 0:
                return {"ok": False, "reason": f"arc {a.index}: zero cost differs"}
            continue
        if cost_scale is None:
            cost_scale = cost / a.cost
        if a.cost * cost_scale != cost:
            return {"ok": False, "reason": f"arc {a.index}: cost differs"}
    for k in e_dem:
        if inst.demands[k] * flow_scale != e_dem[k]:
            return {"ok": False, "reason": f"demand {k} differs"}
    return {"ok": True, "flow_scale": str(flow_scale), "cost_scale": str(cost_scale), "reason": ""}
