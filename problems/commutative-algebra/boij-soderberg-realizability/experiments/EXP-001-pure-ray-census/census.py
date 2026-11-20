"""EXP-001 stage 0: the exact census of the 220 pure rays (0,d1,d2,d3), d3 <= 12, over k[x,y,z].

CPU only, standard library, exact rational/integer arithmetic. Written independently of Macaulay2: the only
call into Macaulay2 is the optional `--check-m2` comparison (gate G1), which reads the package's own numbers
and compares them with the ones computed here.

Usage (from the repository root, repo .venv):
    python census.py                 # print the stage 0 counts
    python census.py --check-m2      # gate G1: compare with pureBetti and pureAll of Macaulay2 (WSL)

Notation. d = (0,d1,d2,d3); beta = primitive Herzog-Kuhl point; B = m * beta is the point at multiple m.
A "route" realizes a multiple of the primitive point; the set of realized multiples on a ray is closed under
addition (direct sums). Obstructions O1 to O6 (hypothesis.md): O1 second syzygy, O2 codimension (with the
Buchsbaum-Rim equality case), O3 regularity, O4 even Gorenstein, O5 three generators, O6 duals of O1 to O5.
They are statements about modules over the commutative ring S, never applied over U(H).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from fractions import Fraction
from functools import lru_cache
from math import comb, gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
MMAX = 12  # multiples m = 1..12 are classified by the obstructions
ANY, INF, CHAR0 = "any field", "infinite field", "characteristic 0"


def fmt(d) -> str:
    return "(" + ",".join(str(x) for x in d) + ")"


def wsl_path(path: str) -> str:
    """Windows path to the path of the same file inside WSL (D:/x to /mnt/d/x)."""
    p = str(path).replace("\\", "/")
    m = re.match(r"^([A-Za-z]):/(.*)$", p)
    if not m:
        return p
    return f"/mnt/{m.group(1).lower()}/{m.group(2)}"


# ------------------------------------------------------------------------------------------ rays and points

def rays(dmax: int = 12) -> list[tuple[int, int, int, int]]:
    """The 220 degree sequences (0,d1,d2,d3), 0 < d1 < d2 < d3 <= dmax, sorted by (d1,d2,d3)."""
    return sorted(((0, a, b, c) for a in range(1, dmax) for b in range(a + 1, dmax)
                   for c in range(b + 1, dmax + 1)), key=lambda d: (d[1], d[2], d[3]))


def _lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


@lru_cache(maxsize=None)
def primitive_point(d: tuple[int, ...]) -> tuple[int, ...]:
    """Least integral point proportional to (prod_{j != i} |d_i - d_j|^-1)."""
    n = len(d)
    fr = []
    for i in range(n):
        den = 1
        for j in range(n):
            if j != i:
                den *= abs(d[i] - d[j])
        fr.append(Fraction(1, den))
    lcm = 1
    for f in fr:
        lcm = _lcm(lcm, f.denominator)
    ints = [int(f * lcm) for f in fr]
    g = 0
    for x in ints:
        g = gcd(g, x)
    return tuple(x // g for x in ints)


def dual(d: tuple[int, ...]) -> tuple[int, ...]:
    """Ext^3(-, S): d to (0, d3-d2, d3-d1, d3) (the Betti numbers are reversed)."""
    return (0,) + tuple(d[-1] - d[-1 - k] for k in range(1, len(d) - 1)) + (d[-1],)


def dual_beta(beta) -> tuple[int, ...]:
    return tuple(reversed(tuple(beta)))


def scaled_from(d) -> tuple[int, ...] | None:
    g = 0
    for x in d:
        g = gcd(g, x)
    return tuple(x // g for x in d) if g > 1 else None


# ------------------------------------------------------------------------------------------ parity, Hilbert

def parity(d, beta=None) -> int:
    """p(-1) = sum (-1)^(i + d_i) beta_i, p(t) = sum (-1)^i beta_i t^{d_i}."""
    beta = beta or primitive_point(tuple(d))
    return sum((-1) ** (i + d[i]) * beta[i] for i in range(len(d)))


def _poly_div(num: list[int], den: list[int]) -> list[int] | None:
    """Exact division of integer polynomials (low degree first), den with leading coefficient +-1."""
    assert den[-1] in (1, -1)
    rem = list(num)
    q = [0] * max(1, len(num) - len(den) + 1)
    for k in range(len(num) - len(den), -1, -1):
        c = rem[k + len(den) - 1] * den[-1]  # den[-1] is its own inverse
        q[k] = c
        for j, dj in enumerate(den):
            rem[k + j] -= c * dj
    if any(rem):
        return None
    while len(q) > 1 and q[-1] == 0:
        q.pop()
    return q


def _numerator(d, beta) -> list[int]:
    p = [0] * (d[-1] + 1)
    for i in range(len(d)):
        p[d[i]] += (-1) ** i * beta[i]
    return p


def hilbert_S(d, beta=None) -> list[int]:
    """Hilbert function of the pure module over S: coefficients of p(t)/(1-t)^3."""
    beta = beta or primitive_point(tuple(d))
    q = _poly_div(_numerator(d, beta), [1, -3, 3, -1])
    assert q is not None, f"{d}: p(t) is not divisible by (1-t)^3"
    return q


def hilbert_UH(d, beta=None) -> list[int] | None:
    """Hilbert function over U(H): coefficients of p(t)/((1-t)^2 (1-t^2)); None when parity fails."""
    beta = beta or primitive_point(tuple(d))
    return _poly_div(_numerator(d, beta), [1, -2, 0, 2, -1])


# ------------------------------------------------------------------------------------------ constructions

def schur_dim(n: int, lam) -> int:
    """dim S_lam(k^n) by the hook-content formula; lam non-increasing, trailing zeros ignored."""
    lam = [x for x in lam if x > 0]
    assert all(lam[i] >= lam[i + 1] for i in range(len(lam) - 1)), lam
    if len(lam) > n:
        return 0
    conj = [sum(1 for x in lam if x > j) for j in range(lam[0] if lam else 0)]
    num, den = 1, 1
    for i, row in enumerate(lam):
        for j in range(row):
            num *= n + j - i
            den *= (row - j - 1) + (conj[j] - i - 1) + 1
    assert num % den == 0
    return num // den


def es_beta0(d) -> int:
    """Eisenbud-Schreyer (any field): beta_0 = prod_i binom(d_i - d_0 - 1, d_i - d_{i-1} - 1)."""
    out = 1
    for i in range(1, len(d)):
        out *= comb(d[i] - d[0] - 1, d[i] - d[i - 1] - 1)
    return out


def efw_two_invariant_beta0(d) -> int:
    """Eisenbud-Floystad-Weyman, second construction (characteristic 0): a Schur functor dimension."""
    n = len(d) - 1
    e = [d[i] - d[i - 1] for i in range(1, n + 1)]
    t: list[int] = []
    for i in range(1, n + 1):
        t += [n - i] * (e[n - i] - 1)
    t.append(0)
    return schur_dim(len(t), tuple(t))


def efw_weyman_beta0(d) -> int:
    """Eisenbud-Floystad-Weyman, first construction (characteristic 0)."""
    dd = [d[i] - d[0] for i in range(1, len(d))]
    e0 = [dd[i] - dd[i - 1] - 1 for i in range(1, len(dd))]
    e = [dd[0] - 1] + e0
    lam = [sum(e[i:]) for i in range(1, len(dd) + 1)]
    return schur_dim(len(dd), tuple(lam))


def pure_all(d) -> tuple[int, int, int]:
    return (es_beta0(d), efw_two_invariant_beta0(d), efw_weyman_beta0(d))


def _multiple(b0: int, beta0: int):
    f = Fraction(b0, beta0)
    return f.numerator if f.denominator == 1 else f


def es_multiple(d):
    return _multiple(es_beta0(d), primitive_point(tuple(d))[0])


def efw_multiples(d) -> tuple:
    b0 = primitive_point(tuple(d))[0]
    return (_multiple(efw_two_invariant_beta0(d), b0), _multiple(efw_weyman_beta0(d), b0))


def soderberg(d) -> dict | None:
    """Soderberg Proposition 4.1 on the rays (0,a,a+1,d3): s generators, socle type t, multiple s/beta_0."""
    if len(d) != 4 or d[2] != d[1] + 1:
        return None
    a, d3 = d[1], d[3]
    s, t = comb(d3 - a, 2), comb(a + 1, 2)
    beta = primitive_point(tuple(d))
    mult = _multiple(s, beta[0])
    integral = isinstance(mult, int)
    consistent = integral and t == mult * beta[3]
    return {"s": s, "t": t, "multiple": mult if integral else None, "consistent": consistent}


def _is_multiple(table, beta) -> int | None:
    """m with table == m * beta, or None."""
    m = Fraction(table[0], beta[0])
    if m.denominator != 1 or m < 1:
        return None
    return int(m) if all(table[i] == m * beta[i] for i in range(len(beta))) else None


def classical_routes(d, beta) -> list[dict]:
    """Classical constructions whose Betti table is a multiple of the primitive point (dossier 3.2 (d))."""
    out: list[dict] = []
    d1, d2, d3 = d[1], d[2], d[3]

    def add(route, table, field, evidence):
        m = _is_multiple(table, beta)
        if m is not None:
            out.append({"route": route, "multiple": m, "field": field, "evidence": evidence,
                        "table": list(table)})

    if d2 == 2 * d1 and d3 == 3 * d1:
        add("Koszul", (1, 3, 3, 1), "any field", f"Koszul complex on three forms of degree {d1}")
    if d2 == d1 + 1 and d3 == d1 + 2:
        a = d1
        add("S/m^a", (1, comb(a + 2, 2), a * (a + 2), comb(a + 1, 2)), "any field",
            f"S/m^{a} (Eagon-Northcott), a = {a}")
    if d1 == 1 and d2 == 2:
        a = d3 - 2
        add("dual of S/m^a", (comb(a + 1, 2), a * (a + 2), comb(a + 2, 2), 1), "any field",
            f"Ext^3(S/m^{a}, S), a = {a}")
    if d3 == d1 + d2 and beta[0] == 1 and beta[3] == 1 and beta[1] == beta[2] and beta[1] % 2 == 1 \
            and beta[1] != 3:
        n = beta[1]
        add("generic Pfaffians", (1, n, n, 1), "infinite field",
            f"Pfaffians of a generic {n}x{n} skew matrix of forms of degree {d2 - d1} (Buchsbaum-Eisenbud)")
    if d1 > 0 and d2 % d1 == 0 and d2 // d1 >= 2 and d3 == d2 + d1:
        a = d2 // d1 - 1
        add("Buchsbaum-Rim", (a, a + 2, a + 2, a), "infinite field",
            f"Buchsbaum-Rim complex of a generic {a}x{a + 2} matrix of forms of degree {d1}")
    return out


def direct_routes(d) -> list[dict]:
    """Every route that realizes some multiple of the primitive point on this ray, with its field scope."""
    beta = primitive_point(tuple(d))
    routes: list[dict] = []
    es0, tw0, we0 = pure_all(d)
    for name, b0, field, ref in (
        ("Eisenbud-Schreyer", es0, "any field", "pureCharFree formula, Theorem 5.1"),
        ("EFW two-invariant", tw0, "characteristic 0", "pureTwoInvariant formula"),
        ("EFW Weyman", we0, "characteristic 0", "pureWeyman formula"),
    ):
        mult = _multiple(b0, beta[0])
        routes.append({"route": name, "multiple": mult if isinstance(mult, int) else None, "field": field,
                       "evidence": f"{ref}: beta_0 = {b0} = {mult} x {beta[0]}"})
    routes += classical_routes(d, beta)
    return routes


# ------------------------------------------------------------------------------------------ obstructions

def _is_buchsbaum_rim(d, B) -> bool:
    a = B[0]
    return (d[1] > 0 and d[2] == (a + 1) * d[1] and d[3] == (a + 2) * d[1]
            and tuple(B) == (a, a + 2, a + 2, a))


def _direct(d, B) -> list[str]:
    """O1 to O5 for the point B on the ray d (commutative ring S, any field)."""
    d1, d2, d3 = d[1], d[2], d[3]
    b0, b1, b2, b3 = B
    ids = []
    if b1 >= b0 + 1 and d2 > (b0 + 1) * d1:
        ids.append("O1")
    if b1 < b0 + 2 or (b1 == b0 + 2 and not _is_buchsbaum_rim(d, B)):
        ids.append("O2")
    if b1 >= b0 + 2 and d3 > (b0 + 2) * d1:
        ids.append("O3")
    if b0 == 1 and b3 == 1 and b1 == b2 and b1 % 2 == 0:
        ids.append("O4")
    if b0 == 1 and b1 == 3 and not (d2 == 2 * d1 and d3 == 3 * d1):
        ids.append("O5")
    return ids


def obstructions(d, m: int) -> list[str]:
    """Obstruction ids excluding the point m*beta_d; O6 carries the ids of the dual ray (O6:O1+O5)."""
    d = tuple(d)
    B = tuple(m * x for x in primitive_point(d))
    ids = _direct(d, B)
    dd = dual(d)
    dual_ids = _direct(dd, tuple(m * x for x in primitive_point(dd)))
    if dual_ids:
        ids.append("O6:" + "+".join(dual_ids))
    return ids


# ------------------------------------------------------------------------------------------ closures

def field_covers(a: str, b: str) -> bool:
    """True when a module realized over every field of scope a is realized over every field of scope b."""
    return a == b or a == ANY or (a == INF and b == CHAR0)


def field_meet(a: str, b: str) -> str | None:
    """Scope in which two realizations can be added (direct sum); None when no field is common."""
    return b if field_covers(a, b) else (a if field_covers(b, a) else None)


def compute_tables(extra_realized=(), dmax: int = 12) -> dict:
    """Stage 0 table (with closures under direct sums, scaling and duality) of every ray.

    extra_realized: hits found later, each {d, m, route, field, evidence}; they enter the same closures, so
    nothing is ever realized without a named source.
    """
    ray_list = rays(dmax)
    in_window = set(ray_list)
    realized: dict[tuple, dict[int, list[dict]]] = {d: {} for d in ray_list}
    excluded: dict[tuple, dict[int, list[str]]] = {d: {} for d in ray_list}

    def add_real(d, m, route, field, evidence):
        entries = realized[d].setdefault(m, [])
        if not any(e["route"] == route and e["evidence"] == evidence for e in entries):
            entries.append({"route": route, "field": field, "evidence": evidence})
            return True
        return False

    recs: dict[tuple, dict] = {}
    for d in ray_list:
        beta = primitive_point(d)
        hf_uh = hilbert_UH(d, beta)
        sod = soderberg(d)
        classical = classical_routes(d, beta)
        recs[d] = {
            "d": list(d), "beta": list(beta), "parity": parity(d, beta), "hf_S": hilbert_S(d, beta),
            "hf_UH": hf_uh, "es_multiple": es_multiple(d), "efw_multiples": list(efw_multiples(d)),
            "soderberg_multiple": sod["multiple"] if sod else None,
            "classical": [{k: v for k, v in c.items() if k != "table"} for c in classical],
        }
        for r in direct_routes(d):
            if r["multiple"] is not None:
                add_real(d, r["multiple"], r["route"], r["field"], f"{fmt(d)}: {r['evidence']}")
        for m in range(1, MMAX + 1):
            ids = obstructions(d, m)
            if ids:
                excluded[d][m] = ids
    for h in extra_realized:
        add_real(tuple(h["d"]), int(h["m"]), h["route"], h["field"], h["evidence"])

    def derive(d, m, field, route, evidence) -> bool:
        """Add a derived entry unless an existing entry at (d, m) already covers its field scope."""
        entries = realized[d].setdefault(m, [])
        if any(field_covers(e["field"], field) for e in entries):
            return False
        entries.append({"route": route, "field": field, "evidence": evidence})
        return True

    changed = True
    while changed:
        changed = False
        for d in ray_list:  # direct sums of two realizations over a common field
            for m in range(2, MMAX + 1):
                for a in range(1, m // 2 + 1):
                    b = m - a
                    for ea in list(realized[d].get(a, [])):
                        for eb in list(realized[d].get(b, [])):
                            f = field_meet(ea["field"], eb["field"])
                            if f is not None and derive(
                                    d, m, f, "direct sum",
                                    f"{fmt(d)}: m={a} ({ea['route']}) plus m={b} ({eb['route']})"):
                                changed = True
        for d in ray_list:  # scaling: a realization at d' = d/g gives one at d (same multiple)
            src = scaled_from(d)
            if src is not None and src in in_window:
                for m, entries in list(realized[src].items()):
                    for e in list(entries):
                        if derive(d, m, e["field"], "scaling",
                                  f"{fmt(d)}: scaling lemma from {fmt(src)} m={m} ({e['route']})"):
                            changed = True
        for d in ray_list:  # duality: a realization at d gives one at the dual ray (same multiple)
            dd = dual(d)
            for m, entries in list(realized[d].items()):
                for e in list(entries):
                    if derive(dd, m, e["field"], "duality",
                              f"{fmt(dd)}: Ext^3 duality from {fmt(d)} m={m} ({e['route']})"):
                        changed = True
        for d in ray_list:  # an exclusion at e*d gives one at d (e*d in the window)
            for e in range(2, dmax // d[3] + 1):
                big = tuple(e * x for x in d)
                if big in in_window:
                    for m, ids in list(excluded[big].items()):
                        if m not in excluded[d]:
                            excluded[d][m] = [f"SCALE:{ids[0].split(':')[0]}@{fmt(big)}"]
                            changed = True
        for d in ray_list:  # an exclusion at d gives one at the dual ray
            dd = dual(d)
            for m, ids in list(excluded[d].items()):
                if m not in excluded[dd]:
                    excluded[dd][m] = [f"DUAL:{ids[0].split(':')[0]}@{fmt(d)}"]
                    changed = True

    for d in ray_list:
        rec = recs[d]
        ex = {m: excluded[d][m] for m in sorted(excluded[d])}
        re_ = {m: realized[d][m] for m in sorted(realized[d])}
        low = next((m for m in range(1, MMAX + 1) if m not in ex), MMAX + 1)
        up = min(re_) if re_ else None
        rec.update({
            "excluded": ex, "realized": re_, "low": low, "up": up,
            "status_primitive": "realized" if 1 in re_ else ("excluded" if 1 in ex else "open"),
            "dual": list(dual(d)), "scaled_from": list(scaled_from(d)) if scaled_from(d) else None,
            "conflicts": sorted(set(re_) & set(ex)),
        })
    return recs


def g4_violation(table: dict, d, m: int) -> list[str]:
    """Obstruction ids excluding (d, m): a hit on such a point stops the run (gate G4)."""
    rec = table.get(tuple(d))
    return list(rec["excluded"].get(int(m), [])) if rec else []


def counts(table: dict) -> dict:
    recs = list(table.values())
    sub9 = [r for r in recs if r["d"][3] <= 9]
    return {
        "rays": len(recs),
        "cyclic_B0_1": sum(1 for r in recs if r["beta"][0] == 1),
        "parity_passing": sum(1 for r in recs if r["parity"] == 0),
        "primitive_realized": sum(1 for r in recs if r["status_primitive"] == "realized"),
        "primitive_excluded": sum(1 for r in recs if r["status_primitive"] == "excluded"),
        "primitive_open": sum(1 for r in recs if r["status_primitive"] == "open"),
        "primitive_realized_char0": sum(
            1 for r in recs if r["status_primitive"] == "realized"
            and any(e["field"] in (ANY, INF, CHAR0) for e in r["realized"][1])),
        "primitive_realized_any_or_infinite_field": sum(
            1 for r in recs if r["status_primitive"] == "realized"
            and any(e["field"] in (ANY, INF) for e in r["realized"][1])),
        "primitive_realized_char0_or_one_prime_only": sum(
            1 for r in recs if r["status_primitive"] == "realized"
            and not any(e["field"] in (ANY, INF) for e in r["realized"][1])),
        "c_determined": sum(1 for r in recs if r["up"] is not None and r["low"] == r["up"]),
        "rays_d3_le_9": len(sub9),
        "d3_le_9_primitive_open": sum(1 for r in sub9 if r["status_primitive"] == "open"),
        "d3_le_9_primitive_open_parity_failing": sum(
            1 for r in sub9 if r["status_primitive"] == "open" and r["parity"] != 0),
        "conflicts": sum(1 for r in recs if r["conflicts"]),
    }


# ------------------------------------------------------------------------------------------ gates

def gate_g6(known: dict | None = None) -> dict:
    """G6: (0,4,9,10) and (0,1,6,10) at m = 1 and m = 2 (Table B).

    The census part (beta, parity, obstructions, m = 2 not excluded) is decided here; "realized at m = 2" is
    decided by stage 1a (randomModule), passed in `known` as {"(0,4,9,10)": True, ...}.
    """
    want = {"(0,4,9,10)": ((1, 3, 8, 6), -16, {"O1", "O5"}), "(0,1,6,10)": ((6, 8, 3, 1), 16, {"O2", "O3"})}
    details, ok = {}, True
    for name, (beta, pm1, need) in want.items():
        d = tuple(int(x) for x in name.strip("()").split(","))
        got = {x.split(":")[0] for x in obstructions(d, 1)}
        m2_open = not obstructions(d, 2)
        good = primitive_point(d) == beta and parity(d) == pm1 and need <= got and m2_open
        details[name] = {"beta": list(primitive_point(d)), "p_minus_1": parity(d), "m1_obstructions": sorted(got),
                         "m2_not_excluded": m2_open, "census_ok": good}
        if known is not None:
            details[name]["m2_realized_stage_1a"] = bool(known.get(name))
            good = good and bool(known.get(name))
        ok = ok and good
    return {"passed": ok, "complete": known is not None, "details": details}


def gate_g7(m2_value: int | None = None) -> dict:
    d = (0, 4, 9, 13)
    return {"ray": fmt(d), "beta": list(primitive_point(d)), "pureCharFree_python": es_beta0(d),
            "multiple": es_multiple(d), "dossier_printed_example": 380, "pureCharFree_macaulay2": m2_value,
            "passed": es_beta0(d) == 15400 and (m2_value is None or m2_value == es_beta0(d))}


# ------------------------------------------------------------------------------------------ dossier Appendix A (G2)

def parse_appendix(path) -> list[dict]:
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| \((0,\d+,\d+,\d+)\) \| \(([\d,]+)\) \|", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append({"d": tuple(int(x) for x in m.group(1).split(",")),
                     "beta": tuple(int(x) for x in m.group(2).split(",")),
                     "status": cells[2], "reason": cells[3], "es_multiple": int(cells[4]),
                     "parity_pass": cells[5] == "yes", "hf_nonneg": cells[6]})
    return rows


def compare_appendix(rows: list[dict], table: dict) -> dict:
    status_map = {"realized": "realized", "obstructed": "excluded", "UNDECIDED": "open"}
    out = {"rows": len(rows), "beta_mismatch": [], "es_mismatch": [], "parity_mismatch": [], "hf_mismatch": [],
           "status_differences": [], "status_agree": 0}
    for row in rows:
        rec = table.get(row["d"])
        name = fmt(row["d"])
        if rec is None:
            out["beta_mismatch"].append(name)
            continue
        if tuple(rec["beta"]) != row["beta"]:
            out["beta_mismatch"].append(name)
        if rec["es_multiple"] != row["es_multiple"]:
            out["es_mismatch"].append(name)
        if (rec["parity"] == 0) != row["parity_pass"]:
            out["parity_mismatch"].append(name)
        if row["parity_pass"] and (rec["hf_UH"] is not None and all(c >= 0 for c in rec["hf_UH"])) != \
                (row["hf_nonneg"] == "yes"):
            out["hf_mismatch"].append(name)
        theirs, mine = status_map.get(row["status"], row["status"]), rec["status_primitive"]
        if theirs == mine:
            out["status_agree"] += 1
            continue
        if mine == "realized":
            e = rec["realized"][1][0]
            reason = f"realized here by {e['route']} ({e['field']}): {e['evidence']}"
        elif mine == "excluded":
            reason = "excluded here by " + ",".join(rec["excluded"][1])
        else:
            reason = f"dossier says {row['status']} ({row['reason']}); no stage 0 route or obstruction here"
        out["status_differences"].append({"d": name, "dossier": row["status"], "census": mine, "reason": reason})
    return out


# ------------------------------------------------------------------------------------------ G1 against Macaulay2

def check_m2(timeout: int = 600) -> dict:
    """Gate G1: run Macaulay2 (WSL) on all 220 rays and compare pureBetti and pureAll with the census."""
    script = wsl_path(str(HERE / "m2" / "check_numbers.m2"))
    proc = subprocess.run(["wsl", "-e", "M2", "--script", script], capture_output=True, text=True, timeout=timeout)
    got = {}
    for line in proc.stdout.splitlines():
        if line.startswith("RAY|"):
            _, d, beta, al = line.split("|")
            got[tuple(int(x) for x in d.split(","))] = (tuple(int(x) for x in beta.split(",")),
                                                        tuple(int(x) for x in al.split(",")))
    bad = []
    for d in rays():
        mine = (primitive_point(d), pure_all(d))
        if got.get(d) != mine:
            bad.append({"d": fmt(d), "python": [list(mine[0]), list(mine[1])],
                        "macaulay2": [list(got[d][0]), list(got[d][1])] if d in got else None})
    n_cyc = sum(1 for d in rays() if primitive_point(d)[0] == 1)
    n_par = sum(1 for d in rays() if parity(d) == 0)
    m2_g7 = None
    m = re.search(r"^G7\|(\d+)$", proc.stdout, re.M)
    if m:
        m2_g7 = int(m.group(1))
    return {"rays_compared": len(got), "mismatches": bad, "rays": len(rays()), "cyclic": n_cyc,
            "parity_passing": n_par, "m2_pureCharFree_0_4_9_13": m2_g7,
            "passed": not bad and len(got) == 220 and len(rays()) == 220 and n_cyc == 44 and n_par == 29,
            "m2_stderr_tail": proc.stderr[-500:]}


def main(argv: list[str]) -> int:
    table = compute_tables()
    c = counts(table)
    print(json.dumps(c, indent=1))
    if "--check-m2" in argv:
        g1 = check_m2()
        print(json.dumps({k: v for k, v in g1.items() if k != "mismatches"}, indent=1))
        if g1["mismatches"]:
            print("MISMATCHES", json.dumps(g1["mismatches"][:5]))
        return 0 if g1["passed"] else 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
