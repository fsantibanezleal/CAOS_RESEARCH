"""The odd-cycle instance family of Afrasyab (arXiv:2609.17568, Section 5), with per-gadget
parameters.

Wiring (nine arcs per index i, j = (i + 1) mod n), fixed for every member:

    start_i  s -> a_i      rfirst_i  a_i -> b_i     connector_i  b_i -> c_i
    rsecond_i c_i -> d_i   final_i   d_i -> t_i     approach_i   s -> c_i
    direct_i s -> t_i      exit_second_i d_i -> e_i  exit_first_i b_j -> e_i

Terminals are the primaries t_i (demand ``b_i``) then the edge auxiliaries e_i (demand
``delta_i``). Arc order follows Afrasyab's ``instances/C5.json``: for i = 0..n-1 the seven
arcs start, rfirst, connector, rsecond, final, approach, direct; then for i = 0..n-1 the
pair exit_second_i, exit_first_i.

Free per-gadget flows: ``r_i`` = x(start_i) = x(rfirst_i); ``u_i`` = x(exit_first_i)
(first incidence of the edge e_i, at gadget j); ``delta_i - u_i`` = x(exit_second_i);
``approach_i`` = x(approach_i). Conservation then fixes the rest:

    x(connector_i) = r_i - u_{i-1}        x(rsecond_i) = x(connector_i) + approach_i
    x(final_i) = x(rsecond_i) - (delta_i - u_i)        x(direct_i) = b_i - x(final_i)
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping, Optional, Sequence

from .instance import Instance, _rat


def odd_cycle_instance(
    n: int,
    b: Sequence,
    delta: Sequence,
    r: Sequence,
    u: Sequence,
    approach: Sequence,
    costs: Optional[Mapping[str, Sequence]] = None,
    name: str = "",
) -> Optional[Instance]:
    """One member of the odd-cycle family, or None when the parameters are invalid.

    Invalid means: n even or below 3, a sequence not of length n, a demand not positive, or
    any flow negative (u_i or delta_i - u_i, r_i - u_{i-1}, the approach flow, the final arc,
    the direct arc). Feasibility of the fractional flow then holds by construction. The
    realisation conditions of the paper (stable-set correspondence, odd-cycle violation) are
    NOT enforced: a member only has to be a valid instance.

    ``costs`` optionally overrides the per-gadget arc costs with a mapping from
    ``"approach"``, ``"direct"`` or ``"exit_first"`` to a sequence of n values; a missing key
    keeps the default. The default is Afrasyab's ``1 / b_i``, taken from the b of the gadget
    that owns the arc: approach_i and direct_i use b_i, and exit_first_i (the arc into the
    edge terminal e_i, leaving b_j) also uses b_i, the owner index i of e_i. All other arcs
    cost 0. In the uniform case every b_i is the same, so this is the paper's cost vector.
    """
    if not isinstance(n, int) or n < 3 or n % 2 == 0:
        return None
    seqs = {"b": b, "delta": delta, "r": r, "u": u, "approach": approach}
    if any(len(v) != n for v in seqs.values()):
        return None
    b_ = [_rat(v) for v in b]
    d_ = [_rat(v) for v in delta]
    r_ = [_rat(v) for v in r]
    u_ = [_rat(v) for v in u]
    ap = [_rat(v) for v in approach]
    if any(v <= 0 for v in b_) or any(v <= 0 for v in d_):
        return None

    cost = {"approach": [1 / v for v in b_], "direct": [1 / v for v in b_], "exit_first": [1 / v for v in b_]}
    for key, vals in (costs or {}).items():
        if key not in cost or len(vals) != n:
            return None
        cost[key] = [_rat(v) for v in vals]

    zero = Fraction(0)
    g, rs, fin, direct, w = [], [], [], [], []
    for i in range(n):
        gi = r_[i] - u_[i - 1]
        wi = d_[i] - u_[i]
        rsi = gi + ap[i]
        fi = rsi - wi
        di = b_[i] - fi
        for v in (u_[i], wi, r_[i], gi, ap[i], fi, di):
            if v < 0:
                return None
        g.append(gi)
        w.append(wi)
        rs.append(rsi)
        fin.append(fi)
        direct.append(di)

    arcs = []
    for i in range(n):
        arcs += [
            ("s", f"a{i}", r_[i], zero),
            (f"a{i}", f"b{i}", r_[i], zero),
            (f"b{i}", f"c{i}", g[i], zero),
            (f"c{i}", f"d{i}", rs[i], zero),
            (f"d{i}", f"t{i}", fin[i], zero),
            ("s", f"c{i}", ap[i], cost["approach"][i]),
            ("s", f"t{i}", direct[i], cost["direct"][i]),
        ]
    for i in range(n):
        j = (i + 1) % n
        arcs += [
            (f"d{i}", f"e{i}", w[i], zero),
            (f"b{j}", f"e{i}", u_[i], cost["exit_first"][i]),
        ]
    demands = {f"t{i}": b_[i] for i in range(n)} | {f"e{i}": d_[i] for i in range(n)}
    return Instance.build("s", demands, arcs, name=name or f"odd-cycle n={n}")


def afrasyab_uniform(k: int, eps) -> Instance:
    """The uniform member C_{2k+1}: T = k/(2(k+1)), t = T + eps, s0 = 1/2 + eps, b = s0 + t.

    Every gadget has chain flow t (start and rfirst carry t + 1/2), direct flow s0, primary
    demand b, auxiliary demand 1 split 1/2 and 1/2, approach flow 1/2. Raises ValueError for
    k < 1 or eps outside (0, 1/(4(k+1))); a float eps is refused (TypeError), as everywhere in
    ufclib. C5 is ``afrasyab_uniform(2, Fraction(1, 120))``.
    """
    if not isinstance(k, int) or k < 1:
        raise ValueError(f"k must be an integer >= 1, got {k!r}")
    e = _rat(eps)
    if not (0 < e < Fraction(1, 4 * (k + 1))):
        raise ValueError(f"eps must lie in (0, 1/{4 * (k + 1)}), got {e}")
    n = 2 * k + 1
    t = Fraction(k, 2 * (k + 1)) + e
    b = Fraction(1, 2) + e + t
    half = Fraction(1, 2)
    inst = odd_cycle_instance(
        n,
        b=[b] * n,
        delta=[Fraction(1)] * n,
        r=[t + half] * n,
        u=[half] * n,
        approach=[half] * n,
        name=f"afrasyab C{n} eps={e}",
    )
    if inst is None:  # cannot happen inside the eps range
        raise ValueError("uniform parameters produced an invalid member")
    return inst
