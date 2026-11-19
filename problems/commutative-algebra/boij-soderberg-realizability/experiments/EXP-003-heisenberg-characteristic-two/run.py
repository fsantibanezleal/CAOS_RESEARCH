"""EXP-003: U(H) in characteristic 2, proof steps of U/U(x^e, y^e), genericity. Claims A1, A2, B1, C1, C2, C3, D1, D2
of the frozen hypothesis (hypothesis.md), plus C0 (calibration of the two instruments).

Run from the repository root:  python <this file>.   Instrument I1 = code/uhlib (exact, Python/numpy);
instrument I2 = Singular 4.3.2 Plural in WSL (singular_i2.py, no shared code with I1).
Tasks run in parallel processes (one per claim part); each returns a plain dict that the main process stores in
artifacts/results.json.  Exit code 1 when C0 fails (an instrument defect) or a task raised, 0 otherwise; a claim that
does not hold is a recorded result, not a failure.
Options: --no-i2 (skip Singular), --only=A1,B1,... (run some claims; results.json keeps the other claims already
stored), --workers=N.
Outputs: artifacts/results.json, artifacts/run.log, artifacts/singular/*.sing.
"""
import json
import os
import random
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = HERE.parents[1] / "code"
sys.path.insert(0, str(CODE))
sys.path.insert(0, str(HERE))

import singular_i2 as I2  # noqa: E402
from uhlib import algebra as A  # noqa: E402
from uhlib import kostant, pure, structure as S, tor  # noqa: E402
from uhlib.fastmod import quotient_module_np  # noqa: E402
from uhlib.fields import QQ, CachedExtField, ExtField, PrimeField  # noqa: E402
from uhlib.linalg import Echelon  # noqa: E402
from uhlib.module import coef, presentation, quotient_module  # noqa: E402

ART = HERE / "artifacts"
SING = ART / "singular"
LOG = ART / "run.log"
T_START = float(os.environ.get("EXP003_T0", time.time()))
USE_I2 = "--no-i2" not in sys.argv

RAYS = [(0, 1, 5, 6), (0, 1, 7, 8), (0, 1, 9, 10), (0, 1, 11, 12), (0, 3, 5, 8), (0, 5, 7, 12), (0, 3, 9, 12), (0, 2, 10, 12)]
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]


def log(msg):
    line = "[%7.1fs] %s" % (time.time() - T_START, msg)
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


# ------------------------------------------------------------------ fields and helpers
def make_f(spec):
    """spec = ('QQ',) or ('GF', p, k)."""
    if spec[0] == "QQ":
        return QQ()
    _, p, k = spec
    if k == 1:
        return PrimeField(p)
    return CachedExtField(p, k) if p == 2 else ExtField(p, k)


def field_spec(F):
    return {"char": F.char, "deg": F.degree, "modulus": getattr(F, "modulus", None), "name": F.name}


def rows(table):
    return [[i, j, r] for (i, j), r in sorted(table.items())] if table is not None else None


def pres_json(F, shifts, rels):
    return {
        "field": field_spec(F),
        "shifts": list(shifts),
        "rels": [[[k, list(m), F.to_json(c)] for (k, m), c in sorted(r.items())] for r in rels],
    }


def primitive_table(degrees):
    return {(i, d): b for i, (d, b) in enumerate(zip(degrees, pure.primitive_pure_betti(degrees)))}


def build(F, shifts, rels, maxdeg, with_action=True):
    """Module through the numpy build for prime fields and GF(2^k), through the Python build otherwise (QQ)."""
    if isinstance(F, QQ):
        return quotient_module(F, shifts, rels, maxdeg=maxdeg)
    return quotient_module_np(F, shifts, rels, maxdeg=maxdeg, with_action=with_action)


def i2_table(pres, name, field_name, M, finished_only=True):
    """(table, seconds, error) from Singular; the Hilbert function recomputed from the table is compared with I1's."""
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in name + "_" + field_name)
    try:
        b2, dt, _ = I2.run(pres, SING / (safe + ".sing"))
    except Exception as exc:  # recorded, never hidden
        return None, 0, repr(exc)[:500]
    return b2, dt, None


def analyze(F, name, shifts, rels, maxdeg, module=None, run_i2=True, i2_unfinished=False):
    """Build (or take) the module, its Hilbert function, the Betti tables by I1 and I2 and their agreement."""
    t0 = time.time()
    M = module if module is not None else build(F, shifts, rels, maxdeg)
    rec = {
        "name": name, "field": F.name, "presentation": pres_json(F, shifts, rels),
        "hilbert_function": M.hilbert_list(), "lowest_degree": M.lo, "finite_length": bool(M.finished),
        "degree_bound": maxdeg, "total_dimension": M.total_dim(),
    }
    b1 = tor.betti(M) if M.finished else None
    rec["betti_I1"] = rows(b1)
    b2 = None
    if USE_I2 and run_i2 and (M.finished or i2_unfinished):
        b2, dt, err = i2_table(rec["presentation"], name, F.name, M)
        rec["seconds_I2"] = round(dt, 2)
        if err:
            rec["I2_error"] = err
    rec["betti_I2"] = rows(b2)
    if b2 is not None:
        extra = 8 if M.finished else 0
        pred = [sum((-1) ** i * r * A.dim_U(t - j) for (i, j), r in b2.items()) for t in range(M.lo, M.hi + 1 + extra)]
        rec["hilbert_consistent_with_I2_table"] = pred == list(M.dims) + [0] * extra
    rec["agree"] = (b1 == b2) if (b1 is not None and b2 is not None) else None
    rec["seconds_I1"] = round(time.time() - t0 - rec.get("seconds_I2", 0), 2)
    return rec, M, b1, b2


def mono_poly(F, p):
    return {(0, m): coef(F, c) for m, c in p.items()}


def poly_json(F, p):
    return [[list(m), F.to_json(c)] for m, c in sorted(p.items())]


# ------------------------------------------------------------------ C0: calibration
def task_c0():
    cases, ok_all = [], True

    def add(rec, expected, note=""):
        nonlocal ok_all
        exp_rows = rows(expected)
        rec["expected"] = exp_rows
        rec["I1_matches_expected"] = rec["betti_I1"] == exp_rows
        rec["I2_matches_expected"] = (rec["betti_I2"] == exp_rows) if rec["betti_I2"] is not None else None
        ok = rec["I1_matches_expected"] and (rec["I2_matches_expected"] is True if USE_I2 else True)
        rec["calibration_ok"] = bool(ok)
        rec["note"] = note
        ok_all &= bool(ok)
        cases.append(rec)

    K = tor.trivial_module_resolution()
    complex_ok = tor.check_complex(K) and tor.check_exact(K, 10)
    for spec in (("QQ",), ("GF", 2, 1), ("GF", 2, 2), ("GF", 2, 4), ("GF", 2, 8), ("GF", 32003, 1)):
        F = make_f(spec)
        rec, *_ = analyze(F, "k=U/(x,y)", [0], [mono_poly(F, A.X), mono_poly(F, A.Y)], 10)
        add(rec, {(0, 0): 1, (1, 1): 2, (2, 3): 2, (3, 4): 1}, "trivial module, table (1,2,2,1) on (0,1,3,4)")
    F = QQ()
    rec, *_ = analyze(F, "U/U(x2,y2)", [0], [mono_poly(F, {(2, 0, 0): 1}), mono_poly(F, {(0, 2, 0): 1})], 14)
    add(rec, {(0, 0): 1, (1, 2): 2, (2, 6): 2, (3, 8): 1}, "EXP-002 C1: Hilbert (1,2,2,2,1), table (1,2,2,1) on (0,2,6,8)")
    for p, q in ((1, 1), (2, 0), (2, 1), (3, 1)):
        M = kostant.kostant_module(F, p, q)
        shifts, prels = presentation(M)
        rec, *_ = analyze(F, "L(%d,%d)" % (p, q), shifts, prels, 2 * p + 8, module=M)
        rec["weyl_dimension"] = kostant.weyl_dimension(p, q)
        rec["dimension_matches_weyl"] = M.total_dim() == kostant.weyl_dimension(p, q)
        add(rec, kostant.expected_table(p, q), "Table F: (q+1,p+2,p+2,q+1) on (0,p-q+1,p+q+3,2p+4)")
        ok_all &= rec["dimension_matches_weyl"]
    # the numpy build against the Python build on U/U(x^e, y^e), e = 3, GF(32003)
    Fp = PrimeField(32003)
    g = [mono_poly(Fp, {(3, 0, 0): 1}), mono_poly(Fp, {(0, 3, 0): 1})]
    same = quotient_module(Fp, [0], g, maxdeg=20).dims == quotient_module_np(Fp, [0], g, maxdeg=20).dims
    return {"claim": "calibration of both instruments", "cases": cases, "complex_K_exact": bool(complex_ok),
            "numpy_build_equals_python_build_check": bool(same), "all_ok": bool(ok_all and complex_ok and same)}


# ------------------------------------------------------------------ A1, A2: subspaces of U_2 in characteristic 2
QUADRICS = list(A.monos(2))  # (0,2,0) y^2, (1,1,0) xy, (2,0,0) x^2, (0,0,1) z


def subspace_list(spec):
    """All 2-dimensional subspaces of U_2 over GF(2), GF(4) (rref bases) or 200 random ones over GF(16), GF(256)."""
    F = make_f(spec)
    q = spec[1] ** spec[2]
    if q <= 4:
        subs = list(S.rref_subspaces(F, 4, 2))
        assert len(subs) == S.gaussian_binomial(q, 4, 2)
        return F, subs
    rng = random.Random(20261119 + q)
    seen, subs = set(), []
    while len(subs) < 200:
        E = Echelon(F, 4)
        while E.rank() < 2:
            E.insert([F.random(rng) for _ in range(4)])
        rws = [E.rows[p] for p in sorted(E.rows)]
        key = tuple(tuple(r) for r in rws)
        if key not in seen:
            seen.add(key)
            subs.append(rws)
    return F, subs


def sub_gens(F, rws):
    return [{m: c for m, c in zip(QUADRICS, r) if not F.is_zero(c)} for r in rws]


def task_A(spec, lo, hi, xcheck_ids):
    F, subs = subspace_list(tuple(spec))
    out = []
    for idx in range(lo, min(hi, len(subs))):
        gens = sub_gens(F, subs[idx])
        t0 = time.time()
        M = quotient_module_np(F, [0], [mono_poly(F, g) for g in gens], maxdeg=20, with_action=False)
        dims = M.dims
        rec = {"index": idx, "basis": [poly_json(F, g) for g in gens], "hilbert_0_to_20": dims,
               "nonzero_every_degree_2_to_20": len(dims) == 21 and all(dims[d] > 0 for d in range(2, 21))}
        rec["derivation"] = S.derivation_data(F, gens)
        if idx in xcheck_ids:
            ph = S.ideal_hilbert(F, gens, 20)
            rec["xcheck_python_hilbert_equal"] = ph == (dims + [0] * (21 - len(dims)))
            if USE_I2:
                pres = pres_json(F, [0], [mono_poly(F, g) for g in gens])
                b2, dt, err = i2_table(pres, "A_%s_%d" % ("_".join(map(str, spec[1:])), idx), F.name, None)
                rec["betti_I2"] = rows(b2)
                rec["seconds_I2"] = round(dt, 2)
                if err:
                    rec["I2_error"] = err
                if b2 is not None:
                    pred = [sum((-1) ** i * r * A.dim_U(t - j) for (i, j), r in b2.items()) for t in range(13)]
                    rec["hilbert_0_to_12_from_I2_table"] = pred
                    rec["I2_hilbert_equals_I1_through_12"] = pred == dims[:13]
        rec["seconds"] = round(time.time() - t0, 2)
        out.append(rec)
    return {"field": F.name, "records": out, "total_subspaces": len(subs),
            "distinct": len({tuple(tuple(r) for r in s) for s in subs})}


# ------------------------------------------------------------------ B1: random presentations in characteristic 2 and the control
def task_B(ray_index, spec, nseeds):
    F = make_f(tuple(spec))
    degs = RAYS[ray_index]
    betas = pure.primitive_pure_betti(degs)
    b0, b1, d1 = betas[0], betas[1], degs[1]
    expected = primitive_table(degs)
    maxdeg = degs[3] + 6
    pure_hf = pure.pure_hilbert_function(degs, betas)
    stat = {"ray": list(degs), "primitive_table": rows(expected), "B0": b0, "B1": b1, "d1": d1, "field": F.name, "seeds": nseeds,
            "degree_bound": maxdeg, "pure_hilbert_function": pure_hf, "finite": 0, "unfinished": 0, "hits": 0,
            "hilbert_counts": {}, "finite_table_counts": {}, "hit_records": [], "hit_seeds": []}
    t0 = time.time()
    for s in range(nseeds):
        seed = 1000000 * (ray_index + 1) + 1000 * (spec[1] if spec[2] == 1 else spec[1] ** spec[2]) + s
        rng = random.Random(seed)
        rels = []
        for _ in range(b1):
            rel = {}
            for k in range(b0):
                for m in A.monos(d1):
                    c = F.random(rng)
                    if not F.is_zero(c):
                        rel[(k, m)] = c
            rels.append(rel)
        M = quotient_module_np(F, [0] * b0, rels, maxdeg=maxdeg)
        hl = M.hilbert_list()
        key = json.dumps(hl) + ("" if M.finished else " (nonzero at the degree bound)")
        stat["hilbert_counts"][key] = stat["hilbert_counts"].get(key, 0) + 1
        if not M.finished:
            stat["unfinished"] += 1
            continue
        stat["finite"] += 1
        bt = tor.betti(M)
        tk = json.dumps(rows(bt))
        stat["finite_table_counts"][tk] = stat["finite_table_counts"].get(tk, 0) + 1
        if bt == expected:
            stat["hits"] += 1
            stat["hit_seeds"].append(seed)
            if len(stat["hit_records"]) < 3:
                rec, *_ = analyze(F, "B1_ray%d_seed%d" % (ray_index, seed), [0] * b0, rels, maxdeg, module=M)
                rec["seed"] = seed
                rec["table_equals_primitive_pure"] = rec["betti_I1"] == rows(expected) and rec["betti_I2"] in (None, rows(expected))
                rec["hilbert_equals_pure_prediction"] = rec["hilbert_function"] == pure_hf
                stat["hit_records"].append(rec)
    stat["seconds"] = round(time.time() - t0, 1)
    return stat


# ------------------------------------------------------------------ C1, C2: the proof steps for U/U(x^e, y^e)
def me_module(F, e):
    gens = [mono_poly(F, {(e, 0, 0): 1}), mono_poly(F, {(0, e, 0): 1})]
    return build(F, [0], gens, 4 * e + 6)


def task_C1(e, spec):
    F = make_f(tuple(spec))
    t0 = time.time()
    M = me_module(F, e)
    rec = {"e": e, "field": F.name, "finite_length": bool(M.finished), "hilbert_function": M.hilbert_list(),
           "total_dimension": M.total_dim()}
    prod = [0] * (4 * e)
    for a in range(e):
        for b in range(e):
            for c in range(e):
                prod[a + b + 2 * c] += 1
    while prod and prod[-1] == 0:
        prod.pop()
    rec["product_formula"] = prod
    rec["hilbert_equals_product_formula"] = rec["hilbert_function"] == prod
    wp = S.weight_pieces(M)
    pred = S.predicted_weight_pieces(e)
    rec["weight_pieces"] = {"%d,%d" % k: v for k, v in sorted(wp.items(), key=lambda t: (t[0][1], t[0][0]))}
    rec["weight_pieces_equal_D_q"] = wp == pred
    rec["weight_pieces_differences"] = {"%d,%d" % k: [wp.get(k, 0), pred.get(k, 0)] for k in sorted(set(wp) | set(pred)) if wp.get(k, 0) != pred.get(k, 0)}
    rec["kernel_y"] = S.kernel_y_report(M, e)
    soc = S.socle_by_weight(M)
    rec["socle"] = {"%d,%d" % k: v for k, v in sorted(soc.items())}
    rec["socle_total_dimension"] = sum(soc.values())
    rec["socle_is_weight0_degree_4e_minus_4_dim1"] = soc == {(4 * e - 4, 0): 1}
    rec["seconds"] = round(time.time() - t0, 1)
    return rec


def task_C2(e):
    F = QQ()
    M = me_module(F, e)
    blocks = S.z_blocks(M)
    pred = S.predicted_z_blocks(e)
    lengths = {}
    for (g, L), c in blocks.items():
        lengths[L] = lengths.get(L, 0) + c
    return {"e": e, "field": "QQ", "blocks_degree_length_multiplicity": [[g, L, c] for (g, L), c in sorted(blocks.items())],
            "predicted_blocks": [[g, L, c] for (g, L), c in sorted(pred.items())],
            "blocks_equal_prediction": blocks == pred,
            "length_multiset": {str(L): c for L, c in sorted(lengths.items())},
            "length_multiset_predicted": {str(L): c for L, c in sorted({L: sum(c for (g, l), c in pred.items() if l == L) for (g, L) in pred}.items())},
            "number_of_generators": sum(blocks.values()), "total_dimension": M.total_dim()}


# ------------------------------------------------------------------ C3: characteristics
def task_C3(e):
    bad, reasons, counts = S.predicted_bad_primes(e, 23, detail=True)
    expected = {(0, 0): 1, (1, e): 2, (2, 3 * e): 2, (3, 4 * e): 1}
    degs = (0, e, 3 * e, 4 * e)
    pure_hf = pure.pure_hilbert_function(degs, (1, 2, 2, 1))
    per_prime, observed_bad = [], []
    for p in PRIMES:
        F = PrimeField(p)
        gens = [mono_poly(F, {(e, 0, 0): 1}), mono_poly(F, {(0, e, 0): 1})]
        rec, M, b1, b2 = analyze(F, "C3_e%d" % e, [0], gens, 4 * e + 8, i2_unfinished=True)
        rec["p"] = p
        rec["pure_table_I1"] = b1 == expected
        rec["pure_table_I2"] = (b2 == expected) if (b2 is not None and M.finished) else None
        rec["hilbert_equals_pure_prediction"] = rec["hilbert_function"] == pure_hf
        rec["predicted_bad"] = p in bad
        rec["observed_pure"] = bool(rec["pure_table_I1"])
        if not rec["observed_pure"]:
            observed_bad.append(p)
        per_prime.append(rec)
    return {"e": e, "predicted_bad_primes_le_23": bad, "prediction_reasons": {str(p): r for p, r in reasons.items()},
            "tableau_counts": {"%d,%d" % k: v for k, v in sorted(counts.items())},
            "observed_non_pure_primes": observed_bad, "observed_subset_of_predicted": set(observed_bad) <= set(bad),
            "observed_equals_predicted": set(observed_bad) == set(bad), "per_prime": per_prime}


# ------------------------------------------------------------------ D1, D2: genericity
def maxrank_series(e, n):
    s = [A.dim_U(t) - 2 * A.dim_U(t - e) for t in range(n)]
    cut = next((i for i, c in enumerate(s) if c <= 0), n)
    return s[:cut]


def task_D1(e, npairs):
    F = PrimeField(32003)
    degs = (0, e, 3 * e, 4 * e)
    pure_table = primitive_table(degs)
    pred = maxrank_series(e, 6 * e)
    out = {"e": e, "maxrank_hilbert_prediction": pred, "pairs": []}
    for s in range(npairs):
        seed = 700000 + 100 * e + s
        rng = random.Random(seed)
        rels = []
        for _ in range(2):
            rels.append({(0, m): c for m in A.monos(e) for c in [F.random(rng)] if not F.is_zero(c)})
        rec, M, b1, b2 = analyze(F, "D1_e%d_seed%d" % (e, seed), [0], rels, len(pred) + 8, run_i2=(e <= 5 or s == 0))
        rec["seed"] = seed
        rec["hilbert_equals_maxrank"] = rec["hilbert_function"] == pred
        rec["table_equals_primitive_pure"] = b1 == pure_table
        out["pairs"].append({k: v for k, v in rec.items() if k != "presentation"} | {"presentation_terms": sum(len(r) for r in rec["presentation"]["rels"])})
    out["all_hilbert_equal_maxrank"] = all(p["hilbert_equals_maxrank"] for p in out["pairs"])
    out["pure_count"] = sum(p["table_equals_primitive_pure"] for p in out["pairs"])
    out["pairs_count"] = npairs
    return out


def substitute_power(F, rels, e):
    """Replace x by x^e and y by y^e in every entry of linear relations (entries in span(x, y))."""
    out = []
    for r in rels:
        new = {}
        for (k, m), c in r.items():
            assert m in ((1, 0, 0), (0, 1, 0)), "entry is not linear in x, y: %s" % (m,)
            new[(k, (e, 0, 0) if m == (1, 0, 0) else (0, e, 0))] = c
        out.append(new)
    return out


def task_D2():
    F = PrimeField(32003)
    out = {}
    # (a) random 2 x 3 matrices of cubics on (0,3,15,18)
    degs = (0, 3, 15, 18)
    expected = primitive_table(degs)
    pure_hf = pure.pure_hilbert_function(degs, (2, 3, 3, 2))
    rand = {"ray": list(degs), "pure_hilbert_function": pure_hf, "seeds": []}
    for s in range(1, 11):
        seed = 800000 + s
        rng = random.Random(seed)
        rels = [{(k, m): c for k in range(2) for m in A.monos(3) for c in [F.random(rng)] if not F.is_zero(c)} for _ in range(3)]
        rec, M, b1, b2 = analyze(F, "D2_cubics_seed%d" % seed, [0, 0], rels, 24, run_i2=(s <= 4))
        rec["seed"] = seed
        rec["table_equals_primitive_pure"] = b1 == expected
        rec["hilbert_equals_pure_prediction"] = rec["hilbert_function"] == pure_hf
        rand["seeds"].append({k: v for k, v in rec.items() if k != "presentation"})
    rand["hits"] = sum(r["table_equals_primitive_pure"] for r in rand["seeds"])
    out["random_matrices_of_cubics"] = rand
    # (b) substitution in a presentation of L(1,1)
    L = kostant.kostant_module(QQ(), 1, 1)
    shifts, prels = presentation(L)
    lin_degrees = sorted({A.deg(m) for r in prels for (_, m) in r})
    sub = {"L11_presentation_shifts": shifts, "L11_relation_count": len(prels), "L11_entry_degrees": lin_degrees,
           "L11_relations": [[[k, list(m), str(c)] for (k, m), c in sorted(r.items())] for r in prels], "cases": []}
    for e, target in ((2, (0, 2, 10, 12)), (3, (0, 3, 15, 18))):
        srels = [{key: coef(F, c) for key, c in r.items()} for r in substitute_power(F, prels, e)]
        exp = primitive_table(target)
        rec, M, b1, b2 = analyze(F, "D2_L11_sub_e%d" % e, shifts, srels, target[3] + 6)
        rec["e"] = e
        rec["target_ray"] = list(target)
        rec["table_equals_primitive_pure"] = b1 == exp
        rec["hilbert_equals_pure_prediction"] = rec["hilbert_function"] == pure.pure_hilbert_function(target, pure.primitive_pure_betti(target))
        sub["cases"].append(rec)
    out["substitution_in_L11"] = sub
    return out


# ------------------------------------------------------------------ orchestration
def run_task(name, fn, args):
    t0 = time.time()
    try:
        res = globals()[fn](*args)
        res["task_seconds"] = round(time.time() - t0, 1)
        return name, res
    except Exception as exc:
        return name, {"error": repr(exc), "trace": traceback.format_exc()[-2000:], "task_seconds": round(time.time() - t0, 1)}


def task_list(only):
    tasks = []
    def want(c):
        return not only or c in only

    if want("A1"):
        for spec, n in ((("GF", 2, 1), 35), (("GF", 2, 2), 357)):
            ids = sorted(random.Random(31 + spec[2]).sample(range(n), 10))
            for lo in range(0, n, 60):
                tasks.append(("A1:%s:%d" % ("GF(%d)" % (spec[1] ** spec[2]), lo), "task_A", (spec, lo, lo + 60, ids)))
    if want("A2"):
        for spec in (("GF", 2, 4), ("GF", 2, 8)):
            ids = sorted(random.Random(31 + spec[2]).sample(range(200), 10))
            for lo in range(0, 200, 25):
                tasks.append(("A2:%s:%d" % ("GF(%d)" % (spec[1] ** spec[2]), lo), "task_A", (spec, lo, lo + 25, ids)))
    if want("B1"):
        for ri in range(len(RAYS)):
            for spec, n in ((("GF", 32003, 1), 20), (("GF", 2, 1), 40), (("GF", 2, 2), 40), (("GF", 2, 4), 40)):
                tasks.append(("B1:%d:%s" % (ri, make_f(spec).name), "task_B", (ri, spec, n)))
    if want("C1"):
        for e in range(2, 9):
            tasks.append(("C1:%d:QQ" % e, "task_C1", (e, ("QQ",))))
            tasks.append(("C1:%d:GF(32003)" % e, "task_C1", (e, ("GF", 32003, 1))))
    if want("C2"):
        for e in range(2, 6):
            tasks.append(("C2:%d" % e, "task_C2", (e,)))
    if want("C3"):
        for e in range(2, 6):
            tasks.append(("C3:%d" % e, "task_C3", (e,)))
    if want("D1"):
        for e, n in ((2, 5), (3, 5), (4, 5), (5, 5), (10, 5)):
            tasks.append(("D1:%d" % e, "task_D1", (e, n)))
    if want("D2"):
        tasks.append(("D2", "task_D2", ()))
    return tasks


def save(results):
    ART.mkdir(exist_ok=True)
    (ART / "results.json").write_text(json.dumps(results, indent=1), encoding="utf-8")


def main():
    only = [a.split("=")[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")]
    only = only[0] if only else []
    workers = int(next((a.split("=")[1] for a in sys.argv[1:] if a.startswith("--workers=")), 24))
    os.environ["EXP003_T0"] = str(T_START)
    ART.mkdir(exist_ok=True)
    SING.mkdir(exist_ok=True)
    prior = {}
    if only and (ART / "results.json").exists():
        prior = json.loads((ART / "results.json").read_text(encoding="utf-8"))
    else:
        LOG.write_text("", encoding="utf-8")
    results = {"experiment": "EXP-003", "hypothesis": "hypothesis.md (frozen)", "tasks": prior.get("tasks", {})}
    log("EXP-003 run start; I2 enabled=%s; only=%s" % (USE_I2, only or "all"))
    c0 = task_c0()
    results["C0"] = c0
    log("C0 all_ok=%s (%d cases, complex_K_exact=%s)" % (c0["all_ok"], len(c0["cases"]), c0["complex_K_exact"]))
    save(results)
    if not c0["all_ok"]:
        results["status"] = "C0 failed"
        save(results)
        log("C0 FAILED: instrument defect; stopping")
        return 1
    tasks = task_list(only)
    errors = 0
    heavy_first = sorted(tasks, key=lambda t: (not t[0].startswith(("B1:3", "B1:0", "D1:10", "D2", "C3")), t[0]))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futs = [pool.submit(run_task, n, f, a) for n, f, a in heavy_first]
        for fut in as_completed(futs):
            name, res = fut.result()
            results["tasks"][name] = res
            if "error" in res:
                errors += 1
                log("TASK %s ERROR %s" % (name, res["error"]))
            else:
                log("task %s done in %.1fs" % (name, res["task_seconds"]))
            save(results)
    results["status"] = "complete" if not errors else "complete with %d task errors" % errors
    results["wall_seconds"] = round(time.time() - T_START, 1)
    save(results)
    log("done in %.1fs; C0 ok; %d tasks, %d errors" % (time.time() - T_START, len(tasks), errors))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
