"""EXP-002: primitive points over the Heisenberg enveloping algebra U(H). Claims C0 to C6 of the frozen hypothesis.

Run from the repository root:  python <this file>.   Instrument I1 = code/uhlib (exact, Python);
instrument I2 = Singular 4.3.2 Plural in WSL (singular_i2.py, no shared code with I1).
Exit code 1 when C0 (calibration) fails (an instrument defect), 0 otherwise; a failing claim is a recorded result.
Outputs: artifacts/results.json, artifacts/run.log, artifacts/singular/*.sing.
"""
import json
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = HERE.parents[1] / "code"
sys.path.insert(0, str(CODE))
sys.path.insert(0, str(HERE))

import singular_i2 as I2  # noqa: E402
from uhlib import algebra as A  # noqa: E402
from uhlib import kostant, pure, tor  # noqa: E402
from uhlib.fields import QQ, ExtField, PrimeField  # noqa: E402
from uhlib.linalg import Echelon, rank  # noqa: E402
from uhlib.module import coef, dual, presentation, quotient_module, truncate  # noqa: E402

ART = HERE / "artifacts"
SING = ART / "singular"
ART.mkdir(exist_ok=True)
SING.mkdir(exist_ok=True)
LOG = ART / "run.log"
T_START = time.time()
RESULTS = {"experiment": "EXP-002", "hypothesis": "hypothesis.md (frozen, ac4f4880)", "claims": {}}
F_Q = QQ()
F_P = PrimeField(32003)
USE_I2 = "--no-i2" not in sys.argv


def log(msg):
    line = "[%7.1fs] %s" % (time.time() - T_START, msg)
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def save():
    (ART / "results.json").write_text(json.dumps(RESULTS, indent=1, sort_keys=False), encoding="utf-8")


def rows(table):
    return [[i, j, r] for (i, j), r in sorted(table.items())] if table is not None else None


def field_spec(F):
    return {"char": F.char, "deg": F.degree, "modulus": getattr(F, "modulus", None), "name": F.name}


def pres_json(F, shifts, rels):
    return {
        "field": field_spec(F),
        "shifts": list(shifts),
        "rels": [[[k, list(m), F.to_json(c)] for (k, m), c in sorted(r.items())] for r in rels],
    }


def poly_rel(F, poly):
    return {(0, m): coef(F, c) for m, c in poly.items()}


def primitive_table(degrees):
    return {(i, d): b for i, (d, b) in enumerate(zip(degrees, pure.primitive_pure_betti(degrees)))}


def analyze(F, name, shifts, rels, maxdeg, module=None, run_i2=True, i2_unfinished=False, truncated_at=None):
    """Build (or take) the module, its Hilbert function, Betti tables by I1 and I2, and their agreement."""
    t0 = time.time()
    M = module if module is not None else quotient_module(F, shifts, rels, maxdeg=maxdeg, name=name)
    rec = {
        "name": name,
        "field": F.name,
        "presentation": pres_json(F, shifts, rels),
        "hilbert_function": M.hilbert_list(),
        "lowest_degree": M.lo,
        "finite_length": bool(M.finished),
        "degree_bound": maxdeg,
        "total_dimension": M.total_dim(),
    }
    if truncated_at is not None:
        rec["truncated_at_degree"] = truncated_at
    b1 = tor.betti(M) if M.finished else None
    rec["betti_I1"] = rows(b1)
    b2 = None
    if USE_I2 and run_i2 and (M.finished or i2_unfinished):
        safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in name + "_" + F.name)
        try:
            b2, dt, _ = I2.run(rec["presentation"], SING / (safe + ".sing"))
            rec["seconds_I2"] = round(dt, 2)
        except Exception as exc:  # recorded, never hidden
            rec["I2_error"] = repr(exc)[:500]
    rec["betti_I2"] = rows(b2)
    if b2 is not None:
        # independent consistency: the Hilbert function recomputed from the I2 table against I1's dimensions
        extra = 8 if M.finished else 0
        pred = [sum((-1) ** i * r * A.dim_U(t - j) for (i, j), r in b2.items()) for t in range(M.lo, M.hi + 1 + extra)]
        rec["hilbert_consistent_with_I2_table"] = pred == list(M.dims) + [0] * extra
    rec["agree"] = (b1 == b2) if (b1 is not None and b2 is not None) else None
    rec["seconds_I1"] = round(time.time() - t0 - rec.get("seconds_I2", 0), 2)
    return rec, M, b1, b2


# ------------------------------------------------------------------ C0
def claim_c0():
    log("C0 calibration")
    cases = []
    ok_all = True

    def add(rec, expected, note=""):
        nonlocal ok_all
        exp_rows = rows(expected)
        rec["expected"] = exp_rows
        rec["I1_matches_expected"] = rec["betti_I1"] == exp_rows
        rec["I2_matches_expected"] = (rec["betti_I2"] == exp_rows) if rec["betti_I2"] is not None else None
        ok = rec["I1_matches_expected"] and (rec["I2_matches_expected"] in (True, None) if not USE_I2 else rec["I2_matches_expected"] is True)
        rec["calibration_ok"] = bool(ok)
        rec["note"] = note
        ok_all &= bool(ok)
        cases.append(rec)
        log("  %-28s hilbert=%s I1=%s I2=%s ok=%s" % (rec["name"], rec["hilbert_function"], rec["betti_I1"], rec["betti_I2"], ok))

    # the trivial module
    rec, *_ = analyze(F_Q, "k=U/(x,y)", [0], [poly_rel(F_Q, A.X), poly_rel(F_Q, A.Y)], 10)
    add(rec, {(0, 0): 1, (1, 1): 2, (2, 3): 2, (3, 4): 1}, "table (1,2,2,1) on (0,1,3,4)")
    # L(1,0) = U/U(x^2, y^2, xy+yx)
    xy_yx = A.padd(A.poly_mul_int(A.X, A.Y), A.poly_mul_int(A.Y, A.X))
    rels = [poly_rel(F_Q, p) for p in ({(2, 0, 0): 1}, {(0, 2, 0): 1}, xy_yx)]
    rec, *_ = analyze(F_Q, "U/U(x2,y2,xy+yx)", [0], rels, 12)
    add(rec, {(0, 0): 1, (1, 2): 3, (2, 4): 3, (3, 6): 1}, "table (1,3,3,1) on (0,2,4,6)")
    # the Kostant modules L(p,q), p <= 4, as submodules of tensor products of the sp_4 modules
    for p in range(0, 5):
        for q in range(0, p + 1):
            t0 = time.time()
            M = kostant.kostant_module(F_Q, p, q)
            shifts, prels = presentation(M)
            rebuilt = quotient_module(F_Q, shifts, prels, maxdeg=2 * p + 8)
            rec, _, _, _ = analyze(F_Q, "L(%d,%d)" % (p, q), shifts, prels, 2 * p + 8, module=M)
            rec["weyl_dimension"] = kostant.weyl_dimension(p, q)
            rec["dimension_matches_weyl"] = M.total_dim() == kostant.weyl_dimension(p, q)
            rec["module_is_UH_module"] = M.check_relations()
            rec["rebuilt_from_presentation_same_hilbert"] = rebuilt.hilbert_list() == M.hilbert_list()
            rec["presentation_relation_degrees"] = sorted({shifts[k] + A.deg(m) for r in prels for (k, m) in r})
            exp = kostant.expected_table(p, q)
            add(rec, exp, "Table F: beta=(q+1,p+2,p+2,q+1) on (0,p-q+1,p+q+3,2p+4); %.1fs total" % (time.time() - t0))
            if not (rec["dimension_matches_weyl"] and rec["module_is_UH_module"] and rec["rebuilt_from_presentation_same_hilbert"]):
                ok_all = False
    RESULTS["claims"]["C0"] = {"claim": "calibration", "cases": cases, "all_ok": ok_all}
    save()
    log("C0 all_ok=%s" % ok_all)
    return ok_all


# ------------------------------------------------------------------ C1
HAND = {
    2: [{(2, 0, 0): 1}, {(0, 2, 0): 1}],
    3: [{(3, 0, 0): 1}, {(2, 1, 0): 1, (1, 0, 1): -2}, {(1, 2, 0): 1}, {(0, 3, 0): 1}],
    4: [{(4, 0, 0): 1}, {(3, 1, 0): 1, (2, 0, 1): -2}, {(2, 2, 0): 1, (1, 1, 1): -4, (0, 0, 2): 2}, {(2, 0, 1): 1},
        {(2, 2, 0): 1}, {(1, 3, 0): 1}, {(0, 4, 0): 1}, {(0, 2, 1): 1}],
    5: [{(5, 0, 0): 1}, {(4, 1, 0): 1}, {(3, 2, 0): 1}, {(2, 3, 0): 1}, {(1, 4, 0): 1}, {(0, 5, 0): 1},
        {(3, 0, 1): 1}, {(1, 2, 1): 1}, {(0, 3, 1): 1},
        {(2, 1, 1): -4, (1, 0, 2): 2}, {(2, 1, 1): -5, (1, 0, 2): 4}, {(2, 1, 1): 1, (1, 0, 2): -2}, {(0, 1, 2): 6}],
}


def ideal_piece(F, gens, d):
    """Reduced echelon basis of the degree d piece of the left ideal U(gens), over the PBW monomials of degree d."""
    B = list(A.monos(d))
    idx = {m: i for i, m in enumerate(B)}
    E = Echelon(F, len(B))
    for g in gens:
        e = A.deg(next(iter(g)))
        if e > d:
            continue
        for u in A.monos(d - e):
            v = [F.zero] * len(B)
            for m, c in g.items():
                for mm, kk in A.mono_mul(u, m):
                    v[idx[mm]] = F.add(v[idx[mm]], F.mul(coef(F, c), F.from_int(kk)))
            E.insert(v)
    return B, E


def fmt_row(F, B, row):
    terms = []
    for m, c in zip(B, row):
        if not F.is_zero(c):
            mon = "".join(s for s in ("x^%d" % m[0] if m[0] else "", "y^%d" % m[1] if m[1] else "", "z^%d" % m[2] if m[2] else ""))
            terms.append("%s*%s" % (F.to_json(c), mon or "1"))
    return " + ".join(terms) or "0"


def claim_c1():
    log("C1 U/U(x^2,y^2) over QQ and GF(32003)")
    out = {"claim": "U/U(x^2,y^2): Hilbert (1,2,2,2,1), table (1,2,2,1) on (0,2,6,8)", "fields": []}
    gens = [{(2, 0, 0): 1}, {(0, 2, 0): 1}]
    expected = {(0, 0): 1, (1, 2): 2, (2, 6): 2, (3, 8): 1}
    for F in (F_Q, F_P):
        rec, M, b1, b2 = analyze(F, "U/U(x2,y2)", [0], [poly_rel(F, g) for g in gens], 14)
        rec["hilbert_equals_hand_derivation"] = rec["hilbert_function"] == [1, 2, 2, 2, 1]
        rec["table_equals_primitive_pure"] = (b1 == expected and b2 == expected)
        pieces = {}
        for d in range(2, 6):
            B, E = ideal_piece(F, gens, d)
            pieces[str(d)] = {
                "dimension": E.rank(),
                "basis_rows": [fmt_row(F, B, E.rows[p]) for p in sorted(E.rows)],
                "dim_U_d": len(B),
            }
            hand = HAND[d]
            Eh = Echelon(F, len(B))
            idx = {m: i for i, m in enumerate(B)}
            inside = True
            for h in hand:
                v = [F.zero] * len(B)
                for m, c in h.items():
                    v[idx[m]] = coef(F, c)
                inside &= not any(not F.is_zero(t) for t in E.reduce(v))
                Eh.insert(v)
            pieces[str(d)]["hand_elements"] = len(hand)
            pieces[str(d)]["hand_dimension"] = Eh.rank()
            pieces[str(d)]["hand_elements_in_ideal"] = bool(inside)
            pieces[str(d)]["hand_span_equals_ideal_piece"] = bool(inside and Eh.rank() == E.rank())
        rec["ideal_pieces"] = pieces
        out["fields"].append(rec)
        log("  %s hilbert=%s I1=%s I2=%s ideal dims=%s" % (F.name, rec["hilbert_function"], rec["betti_I1"], rec["betti_I2"],
                                                         [pieces[str(d)]["dimension"] for d in range(2, 6)]))
    # the three degree-5 elements: rank in the span of x^2 y z, x z^2 over several fields
    ranks = {}
    trio = [(-4, 2), (-5, 4), (1, -2)]
    for F in (F_Q, PrimeField(2), PrimeField(3), PrimeField(5), PrimeField(7), F_P):
        ranks[F.name] = rank(F, [[coef(F, a), coef(F, b)] for a, b in trio], 2)
    out["degree5_three_elements"] = {"elements": ["-4 x^2yz + 2 x z^2", "-5 x^2yz + 4 x z^2", "x^2yz - 2 x z^2"], "rank_by_field": ranks}
    RESULTS["claims"]["C1"] = out
    save()


# ------------------------------------------------------------------ C2
def claim_c2():
    log("C2 U/U(x^2,y^2) over GF(2^k), GF(3^k), k=1..4")
    out = {"claim": "(x^2,y^2) does not give the table in characteristic 2 and 3", "fields": []}
    gens = [{(2, 0, 0): 1}, {(0, 2, 0): 1}]
    for p in (2, 3):
        for k in (1, 2, 3, 4):
            F = PrimeField(p) if k == 1 else ExtField(p, k)
            rec, M, b1, b2 = analyze(F, "U/U(x2,y2)", [0], [poly_rel(F, g) for g in gens], 14, i2_unfinished=True)
            rec["hilbert_equals_hand_derivation_char0_pattern"] = rec["hilbert_function"] == [1, 2, 2, 2, 1]
            rec["hilbert_function_to_degree_bound"] = M.dims
            rec["note"] = "dims listed through the degree bound %d; finite_length false means not zero by the bound" % 14
            out["fields"].append(rec)
            log("  %s hilbert=%s finite=%s I2=%s" % (F.name, rec["hilbert_function"], rec["finite_length"], rec["betti_I2"]))
    RESULTS["claims"]["C2"] = out
    save()


# ------------------------------------------------------------------ C3
def claim_c3():
    log("C3 U/U(x^e,y^e) over QQ, e=3..6")
    out = {"claim": "pure table (1,2,2,1) on (0,e,3e,4e)", "cases": []}
    for e in (2, 3, 4, 5, 6):
        gens = [{(e, 0, 0): 1}, {(0, e, 0): 1}]
        rec, M, b1, b2 = analyze(F_Q, "U/U(x%d,y%d)" % (e, e), [0], [poly_rel(F_Q, g) for g in gens], 4 * e + 10)
        expected = {(0, 0): 1, (1, e): 2, (2, 3 * e): 2, (3, 4 * e): 1}
        deg = (0, e, 3 * e, 4 * e)
        hf = pure.pure_hilbert_function(deg, (1, 2, 2, 1))
        rec["e"] = e
        rec["pure_table_hilbert_function_predicted"] = hf
        rec["hilbert_equals_pure_prediction"] = rec["hilbert_function"] == hf
        rec["table_equals_primitive_pure"] = (b1 == expected and b2 == expected)
        rec["in_hypothesis_range"] = e >= 3
        out["cases"].append(rec)
        log("  e=%d hilbert=%s I1=%s I2=%s" % (e, rec["hilbert_function"], rec["betti_I1"], rec["betti_I2"]))
    RESULTS["claims"]["C3"] = out
    save()


# ------------------------------------------------------------------ C4
def rand_quadric(rng):
    return [rng.randrange(32003) for _ in A.monos(2)]


def quad_poly(lifts):
    return {m: c for m, c in zip(A.monos(2), lifts) if c}


def claim_c4():
    log("C4 cokernels of random 2x3 matrices of quadrics, 10 seeds")
    out = {"claim": "pure table (2,3,3,2) on (0,2,10,12)", "seeds": [], "cases": []}
    degrees = (0, 2, 10, 12)
    expected = {(0, 0): 2, (1, 2): 3, (2, 10): 3, (3, 12): 2}
    out["pure_hilbert_function_predicted"] = pure.pure_hilbert_function(degrees, (2, 3, 3, 2))
    hits = {"GF(32003)": 0, "QQ": 0}
    for s in range(1, 11):
        seed = 4000 + s
        rng = random.Random(seed)
        draws = [[quad_poly(rand_quadric(rng)) for _ in range(2)] for _ in range(3)]  # 3 relations, 2 components
        out["seeds"].append(seed)
        for F in (F_P, F_Q):
            rels = []
            for r in draws:
                rel = {}
                for comp in range(2):
                    for m, c in r[comp].items():
                        rel[(comp, m)] = coef(F, c)  # QQ: the integer representative in [0, 32003) lifted
                rels.append(rel)
            rec, M, b1, b2 = analyze(F, "coker2x3_seed%d" % seed, [0, 0], rels, 24)
            rec["seed"] = seed
            rec["table_equals_primitive_pure"] = (b1 == expected and b2 == expected)
            hits[F.name] += int(rec["table_equals_primitive_pure"])
            out["cases"].append(rec)
            log("  seed %d %s hilbert=%s finite=%s I1=%s I2=%s pure=%s" % (seed, F.name, rec["hilbert_function"], rec["finite_length"],
                                                                           rec["betti_I1"], rec["betti_I2"], rec["table_equals_primitive_pure"]))
    out["hits_of_10"] = hits
    RESULTS["claims"]["C4"] = out
    save()


# ------------------------------------------------------------------ C5
def claim_c5():
    log("C5 random pairs of quadrics over GF(2^k), GF(3^k), k=1..4, 20 seeds each")
    out = {"claim": "exploration: is (1,2,2,1) on (0,2,6,8) realized in characteristic 2 or 3 by some pair of quadrics",
           "fields": []}
    expected = {(0, 0): 1, (1, 2): 2, (2, 6): 2, (3, 8): 1}
    for p in (2, 3):
        for k in (1, 2, 3, 4):
            F = PrimeField(p) if k == 1 else ExtField(p, k)
            stat = {"field": F.name, "seeds": [], "hilbert_counts": {}, "finite": 0, "infinite_or_unfinished": 0, "table_hits": 0,
                    "hits": [], "betti_counts": {}}
            for s in range(1, 21):
                seed = 5000 + 100 * p + 10 * k + s
                rng = random.Random(seed)
                q = [{(0, m): c for m, c in zip(A.monos(2), (F.random(rng) for _ in A.monos(2))) if not F.is_zero(c)} for _ in range(2)]
                M = quotient_module(F, [0], q, maxdeg=14)
                stat["seeds"].append(seed)
                key = json.dumps(M.hilbert_list()) + ("" if M.finished else " (not zero by degree 14)")
                stat["hilbert_counts"][key] = stat["hilbert_counts"].get(key, 0) + 1
                if M.finished:
                    stat["finite"] += 1
                    b1 = tor.betti(M)
                    bk = json.dumps(rows(b1))
                    stat["betti_counts"][bk] = stat["betti_counts"].get(bk, 0) + 1
                    if b1 == expected:
                        stat["table_hits"] += 1
                        if len(stat["hits"]) < 3:
                            rec, *_ = analyze(F, "pair_seed%d" % seed, [0], q, 14, module=M)
                            rec["seed"] = seed
                            stat["hits"].append(rec)
                else:
                    stat["infinite_or_unfinished"] += 1
            out["fields"].append(stat)
            log("  %s finite=%d unfinished=%d hits=%d hilbert=%s" % (F.name, stat["finite"], stat["infinite_or_unfinished"],
                                                                     stat["table_hits"], stat["hilbert_counts"]))
    RESULTS["claims"]["C5"] = out
    save()


# ------------------------------------------------------------------ C6
def claim_c6():
    log("C6 duality on 20 random finite length modules")
    out = {"claim": "Betti table of the dual module is the reverse of that of M", "cases": [], "construction": (
        "M* = graded dual Hom_k(M,k), M*_(-d) = (M_d)^*; right module by (f.u)(m) = f(um); left module through the "
        "antipode S(x) = -x, S(y) = -y, S(z) = -z: (u.f)(m) = f(S(u)m); matrices of x, y on M* are minus the transposes "
        "of those of M. Reverse means beta_{i,j}(M*) = beta_{3-i,4-j}(M) (resolution of k ends in U(-4)).")}
    F = F_P
    ok_count = 0
    for n in range(20):
        seed = 6000 + n
        rng = random.Random(seed)
        if n < 10:
            kind = "coker 2x3 quadrics"
            shifts = [0, 0]
            rels = []
            for _ in range(3):
                rel = {}
                for comp in range(2):
                    for m, c in quad_poly(rand_quadric(rng)).items():
                        rel[(comp, m)] = coef(F, c)
                rels.append(rel)
            maxdeg = 24
        else:
            kind = "coker 3x5 linear forms (truncated if infinite)"
            shifts = [0, 0, 0]
            rels = []
            for _ in range(5):
                rel = {}
                for comp in range(3):
                    for m in A.monos(1):
                        c = rng.randrange(32003)
                        if c:
                            rel[(comp, m)] = coef(F, c)
                rels.append(rel)
            maxdeg = 14
        M = quotient_module(F, shifts, rels, maxdeg=maxdeg)
        trunc = None
        if not M.finished:
            M = truncate(M, maxdeg)
            trunc = maxdeg
        pshifts, prels = presentation(M)
        recM, _, b1, b2 = analyze(F, "M_seed%d" % seed, pshifts, prels, maxdeg, module=M, truncated_at=trunc)
        D = dual(M)
        dshifts, drels = presentation(D)
        recD, _, d1, d2 = analyze(F, "dual_seed%d" % seed, dshifts, drels, maxdeg, module=D, truncated_at=trunc)
        rev1 = {(3 - i, 4 - j): r for (i, j), r in b1.items()}
        rev2 = {(3 - i, 4 - j): r for (i, j), r in b2.items()} if b2 is not None else None
        hilb = M.hilbert_list()
        case = {
            "seed": seed, "kind": kind, "original_presentation_shifts": shifts, "module": recM, "dual": recD,
            "hilbert_palindromic": hilb == hilb[::-1],
            "dual_equals_reverse_I1": d1 == rev1,
            "dual_equals_reverse_I2": (d2 == rev2) if rev2 is not None else None,
            "dual_is_UH_module": D.check_relations(),
            "reverse_table_I1": rows(rev1),
        }
        case["duality_holds"] = bool(case["dual_equals_reverse_I1"] and case["dual_equals_reverse_I2"] in (True, None))
        ok_count += int(case["duality_holds"])
        out["cases"].append(case)
        log("  seed %d %s M hilbert=%s I1=%s | dual I1=%s | holds=%s" % (seed, kind[:12], hilb, recM["betti_I1"], recD["betti_I1"], case["duality_holds"]))
    out["duality_holds_count"] = ok_count
    RESULTS["claims"]["C6"] = out
    save()


def main():
    LOG.write_text("", encoding="utf-8")
    log("EXP-002 run start; I2 enabled=%s" % USE_I2)
    c0 = claim_c0()
    if not c0:
        log("C0 FAILED: instrument defect; stopping")
        RESULTS["status"] = "C0 failed"
        save()
        return 1
    only = [a for a in sys.argv[1:] if a.startswith("--only=")]
    todo = only[0].split("=")[1].split(",") if only else ["C1", "C2", "C3", "C4", "C5", "C6"]
    funcs = {"C1": claim_c1, "C2": claim_c2, "C3": claim_c3, "C4": claim_c4, "C5": claim_c5, "C6": claim_c6}
    for name in todo:
        funcs[name]()
    RESULTS["status"] = "complete"
    RESULTS["wall_seconds"] = round(time.time() - T_START, 1)
    save()
    log("done in %.1fs; C0 ok; claims recorded: %s" % (time.time() - T_START, ", ".join(sorted(RESULTS["claims"]))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
