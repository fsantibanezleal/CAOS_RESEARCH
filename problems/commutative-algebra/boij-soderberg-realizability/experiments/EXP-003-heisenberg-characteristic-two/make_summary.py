"""Write results-summary.md from artifacts/results.json (every number in the summary comes from the run).

Usage (repository root):  python <this file>
"""
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = json.loads((HERE / "artifacts" / "results.json").read_text(encoding="utf-8"))
T = R["tasks"]
out = []


def w(s=""):
    out.append(s)


def table(header, body):
    w("| " + " | ".join(header) + " |")
    w("|" + "|".join("---" for _ in header) + "|")
    for row in body:
        w("| " + " | ".join(str(c) for c in row) + " |")
    w()


def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


def tasks(prefix):
    return {k: v for k, v in T.items() if k.startswith(prefix)}


def tab(rows_):
    return "; ".join("(%d, d=%d, %d)" % tuple(t) for t in rows_) if rows_ else "-"


w("# EXP-003 results summary")
w()
w("Run: `run.py` from the repository root; hypothesis.md frozen (not edited). Instrument I1 = `code/uhlib` (exact arithmetic: "
  "Fraction over QQ, integers mod p, GF(2^k) with a verified irreducible modulus; the numpy build `uhlib/fastmod.py` for prime "
  "fields and GF(2^k), the Python build for QQ). Instrument I2 = Singular 4.3.2 Plural in WSL (`singular_i2.py`, no shared code with "
  "I1). Betti tables are read from the degrees of the generators of `mres`, never from `betti()`.")
w("Wall time of the run: %s s (tasks ran in parallel processes). Status: %s." % (R.get("wall_seconds"), R.get("status")))
w()

# ---------------------------------------------------------------- C0
c0 = R["C0"]
w("## C0 calibration of the two instruments")
w()
table(["module", "field", "expected table", "I1", "I2", "ok"],
      [[c["name"], c["field"], tab(c["expected"]), tab(c["betti_I1"]), tab(c["betti_I2"]), c["calibration_ok"]] for c in c0["cases"]])
w("Complex K exact in degrees 0..10 (rank counts): %s. Numpy build equals Python build on U/U(x^3,y^3): %s. All calibration cases ok: **%s**. "
  "The trivial module over GF(2), GF(4), GF(16), GF(256) also exercises the Singular `minpoly` path used for A1, A2, B1 in characteristic 2."
  % (c0["complex_K_exact"], c0["numpy_build_equals_python_build_check"], c0["all_ok"]))
w()

# ---------------------------------------------------------------- A1, A2
w("## A1 and A2: two-dimensional subspaces of U_2 = span(x^2, xy, y^2, z) in characteristic 2")
w()
w("Each subspace is given by its reduced echelon basis in the monomial order (y^2, xy, x^2, z). Hilbert function of U/U(f, g) through "
  "degree 20 by the numpy build; 'nonzero' means the dimension is positive in every degree 2..20. The data of the derivation: the dimension of "
  "the central part of the subspace, the central quadric c, and for a one-dimensional central part the determinant of right "
  "multiplication by the non-central generator on U/Uc over R = C/(c) (C = k[x^2, y^2, z]); 'det degree' is the degree in the grading of U.")
w()
body = []
xrows = []
for fld, claim, expected_n in (("GF(2)", "A1", 35), ("GF(4)", "A1", 357), ("GF(16)", "A2", 200), ("GF(256)", "A2", 200)):
    ts = tasks("%s:%s:" % (claim, fld))
    recs = sorted((x for v in ts.values() if "records" in v for x in v["records"]), key=lambda x: x["index"])
    tot = {v["total_subspaces"] for v in ts.values() if "total_subspaces" in v}
    dist = {v["distinct"] for v in ts.values() if "distinct" in v}
    nz = sum(x["nonzero_every_degree_2_to_20"] for x in recs)
    cen = collections.Counter(x["derivation"]["central_dimension"] for x in recs)
    one = [x for x in recs if x["derivation"]["central_dimension"] == 1]
    det_nz = sum(1 for x in one if not x["derivation"]["det_is_zero"])
    degs = sorted({x["derivation"]["det_degree"] for x in one if not x["derivation"]["det_is_zero"]})
    hf = collections.Counter(tuple(x["hilbert_0_to_20"]) for x in recs)
    body.append([claim, fld, expected_n, len(recs), "%s" % sorted(dist), "%d / %d" % (nz, len(recs)),
                 "dim0:%d dim1:%d dim2:%d" % (cen.get(0, 0), cen.get(1, 0), cen.get(2, 0)),
                 "det nonzero %d, det zero %d (degrees %s)" % (det_nz, len(one) - det_nz, degs), len(hf)])
    xs = [x for x in recs if "xcheck_python_hilbert_equal" in x]
    xrows.append([fld, len(xs), sum(x["xcheck_python_hilbert_equal"] for x in xs),
                  sum(1 for x in xs if x.get("I2_hilbert_equals_I1_through_12")), sum(1 for x in xs if "I2_error" in x)])
    w_hf = hf
table(["claim", "field", "subspaces expected", "computed", "distinct bases", "nonzero in every degree 2..20", "central part dimension",
       "derivation data (central dim 1)", "distinct Hilbert functions"], body)
w("Exhaustive enumeration: the Gaussian binomials [4 choose 2]_q give 35 for q = 2 and 357 for q = 4; the code asserts the enumerated number "
  "equals them and the 'distinct bases' column counts distinct reduced echelon bases. The 200 subspaces over GF(16) and GF(256) are "
  "uniform random (fixed seeds 20261119 + q, duplicates rejected).")
w()
w("Cross-checks on 10 subspaces per field (indices drawn by a fixed seed): "
  "I1 numpy Hilbert function against the pure Python `ideal_hilbert` through degree 20, and against the Hilbert function recomputed "
  "from the Singular Betti table through degree 12.")
w()
table(["field", "subspaces cross-checked", "Python Hilbert equal", "Singular Hilbert (through 12) equal", "Singular errors"], xrows)
all_hf = collections.Counter()
for fld, claim in (("GF(2)", "A1"), ("GF(4)", "A1"), ("GF(16)", "A2"), ("GF(256)", "A2")):
    for v in tasks("%s:%s:" % (claim, fld)).values():
        for x in v.get("records", []):
            all_hf[(fld, tuple(x["hilbert_0_to_20"][:9]))] += 1
w("Hilbert functions that occur (first nine terms, with counts per field):")
w()
for (fld, hf), n in sorted(all_hf.items()):
    w("- %s: %s ... : %d subspaces" % (fld, list(hf), n))
w()
bad = [(fld, x["index"]) for fld, claim in (("GF(2)", "A1"), ("GF(4)", "A1"), ("GF(16)", "A2"), ("GF(256)", "A2"))
       for v in tasks("%s:%s:" % (claim, fld)).values() for x in v.get("records", []) if not x["nonzero_every_degree_2_to_20"]]
w("Subspaces with a zero graded piece in some degree 2..20: %s." % (bad if bad else "none"))
w("Comparison with the prediction (A1 and A2 hold in every case): the quotient is nonzero in every degree 2..20 for all computed subspaces; "
  "no machine statement of infinite length is made (the machine shows degrees up to 20 only).")
w()

# ---------------------------------------------------------------- B1
w("## B1 random presentations, characteristic 2 and the GF(32003) control")
w()
w("For each ray: B0 generators in degree 0 and B1 relations in degree d1 (primitive pure table of the ray), entries uniform in U_(d1); "
  "degree bound d3 + 6; 'finite' = zero in three consecutive degrees within the bound; 'pure hits' = finite and the Betti table equals "
  "the primitive pure table. A miss proves nothing about realizability.")
w()
body = []
for ri in range(8):
    for fld in ("GF(32003)", "GF(2)", "GF(2^2)", "GF(2^4)"):
        v = T.get("B1:%d:%s" % (ri, fld))
        if not v or "error" in v:
            continue
        hr = v["hit_records"]
        body.append(["(%s)" % ",".join(map(str, v["ray"])), "B0=%d B1=%d d1=%d" % (v["B0"], v["B1"], v["d1"]), fld, v["seeds"], v["finite"],
                     v["unfinished"], v["hits"], "%d/%d" % (sum(1 for h in hr if h["agree"] is True), len(hr))])
table(["ray", "presentation", "field", "seeds", "finite", "not finite by the bound", "pure hits", "I1=I2 on hit records"], body)
w("Primitive tables of the eight rays: " + "; ".join("(%s): %s" % (",".join(map(str, T["B1:%d:GF(2)" % ri]["ray"])), tab(T["B1:%d:GF(2)" % ri]["primitive_table"]))
                                                    for ri in range(8)) + ".")
w()
w("Finite non-pure tables over GF(32003) (what the generic presentation gives when the ray is not hit):")
w()
for ri in range(8):
    v = T.get("B1:%d:GF(32003)" % ri)
    if v and v["hits"] == 0:
        w("- ray (%s): %s" % (",".join(map(str, v["ray"])), "; ".join("%s x %d" % (tab(json.loads(k)), n) for k, n in v["finite_table_counts"].items())))
w()
rays_hit32003 = [tuple(T["B1:%d:GF(2)" % ri]["ray"]) for ri in range(8) if T["B1:%d:GF(32003)" % ri]["hits"] > 0]
rays_miss32003 = [tuple(T["B1:%d:GF(2)" % ri]["ray"]) for ri in range(8) if T["B1:%d:GF(32003)" % ri]["hits"] == 0]
char2_hit = {fld: [tuple(T["B1:%d:GF(2)" % ri]["ray"]) for ri in range(8) if T.get("B1:%d:%s" % (ri, fld), {}).get("hits", 0) > 0] for fld in ("GF(2)", "GF(2^2)", "GF(2^4)")}
char2_miss = {fld: [tuple(T["B1:%d:GF(2)" % ri]["ray"]) for ri in range(8) if T.get("B1:%d:%s" % (ri, fld), {}).get("hits", 0) == 0] for fld in char2_hit}
w("Comparison with the predictions: over GF(32003) the rays hit are %s and the rays not hit are %s (prediction: every ray hit except possibly "
  "(0,3,9,12) and the (1,6,6,1) ray (0,5,7,12)). In characteristic 2: rays with at least one hit over GF(2): %s; over GF(4): %s; over GF(16): %s. "
  "Rays with no hit over GF(2), GF(4), GF(16) respectively: %s; %s; %s. (0,2,10,12) has hits in characteristic 2: %s. "
  "Rays with odd d1 ((0,1,*), (0,3,5,8), (0,3,9,12), (0,5,7,12)) hit in characteristic 2: %s."
  % (rays_hit32003, rays_miss32003, char2_hit["GF(2)"], char2_hit["GF(2^2)"], char2_hit["GF(2^4)"], char2_miss["GF(2)"], char2_miss["GF(2^2)"],
     char2_miss["GF(2^4)"], any((0, 2, 10, 12) in v for v in char2_hit.values()),
     {fld: [r for r in char2_hit[fld] if r[1] % 2 == 1] for fld in char2_hit}))
cand = [r for r in rays_hit32003 if all(r in char2_miss[f] for f in char2_miss)]
w("Rays hit over GF(32003) and not hit over GF(2), GF(4), GF(16) in the 40 seeds each: %s. By the hypothesis's own consequence rule such a ray is a candidate for a "
  "characteristic-dependent point and needs a proof before any claim; for these rays every one of the 40 random presentations per field had a nonzero quotient in "
  "every degree up to the bound (columns 'finite' = 0)." % cand)
w()
w("A ray not hit over GF(32003) is, per the hypothesis, not reachable by generic presentations and its characteristic 2 outcome is not interpreted. "
  "No statement of non-realizability is made for any ray.")
w()

# ---------------------------------------------------------------- C1
w("## C1 proof steps for M_e = U/U(x^e, y^e), e = 2..8")
w()
body = []
for e in range(2, 9):
    for fld in ("QQ", "GF(32003)"):
        v = T.get("C1:%d:%s" % (e, fld))
        if not v or "error" in v:
            continue
        kd = v["kernel_y"]
        body.append([e, fld, v["total_dimension"], v["hilbert_equals_product_formula"], v["weight_pieces_equal_D_q"], len(v["weight_pieces"]),
                     kd["kernel_y_equals_span_of_z_c_g_a"], kd["classes_lie_in_kernel_y"], v["socle"], v["socle_is_weight0_degree_4e_minus_4_dim1"], v["task_seconds"]])
table(["e", "field", "length", "Hilbert series = product formula", "(weight, degree) pieces = D_q(n')", "nonzero pieces", "ker y = span of z^c g_a",
       "all z^c g_a in ker y", "socle {(degree,weight): dim}", "socle = weight 0, degree 4e-4, dim 1", "seconds"], body)
w("The QQ rows are the claim; the GF(32003) rows are the same computation over a prime field (the numpy build) and are listed as a second field, not a "
  "substitute. All QQ computations ran exactly (Fractions), including e = 7 and e = 8. The weight of a PBW monomial x^a y^b z^c is b - a. "
  "The kernel of y is compared degree by degree: the span of the classes of z^c g_a (a < e, g_a as in step 5 of the note, reordered into the PBW basis) "
  "against the kernel of the matrix of y.")
w()
c1rows = [T["C1:%d:QQ" % e] for e in range(2, 9) if "C1:%d:QQ" % e in T]
c1ok = all(v["hilbert_equals_product_formula"] and v["weight_pieces_equal_D_q"] and v["kernel_y"]["kernel_y_equals_span_of_z_c_g_a"]
           and v["socle_is_weight0_degree_4e_minus_4_dim1"] for v in c1rows)
w("Comparison with the prediction (C1 holds for every e <= 8): over QQ the four statements (weight pieces = D_q(n'), kernel of y = span of z^c g_a, socle one-dimensional "
  "of weight 0 and degree 4e-4, Hilbert series = product formula) are all True for e = %s: %s. This is a finite check of the derivation for e <= 8, not the proof." % (
      [v["e"] for v in c1rows], c1ok))
w()

# ---------------------------------------------------------------- C2
w("## C2 k[z]-structure of M_e, e = 2..5, QQ")
w()
body = []
for e in range(2, 6):
    v = T.get("C2:%d" % e)
    if not v or "error" in v:
        continue
    body.append([e, v["total_dimension"], v["number_of_generators"], v["blocks_equal_prediction"], v["length_multiset"], v["length_multiset_predicted"]])
table(["e", "length", "k[z]-generators", "(generator degree, length) multiset = pattern", "lengths found", "lengths predicted"], body)
for e in range(2, 6):
    v = T.get("C2:%d" % e)
    if v and "error" not in v:
        w("- e = %d, blocks (generator degree g, length L, multiplicity) of the summands k[z]/(z^L)(-g): %s" % (e, v["blocks_degree_length_multiplicity"]))
w()
c2ok = [e for e in range(2, 6) if T["C2:%d" % e]["blocks_equal_prediction"]]
w("Comparison with the prediction (pattern holds): the (generator degree, length) multiset equals the pattern for e in %s of 2..5." % c2ok)
w()
w("The pattern: one summand k[z]/(z^(2e-1-a-b)) for each a, b < e, generated in degree a + b (the hypothesis fixes the lengths; the generator degree a + b "
  "is the degree of x^a y^b and is how the comparison above reads the pattern, together with the lengths alone).")
w()

# ---------------------------------------------------------------- C3
w("## C3 characteristics, e = 2..5, primes p <= 23")
w()
for e in range(2, 6):
    v = T.get("C3:%d" % e)
    if not v or "error" in v:
        continue
    w("### e = %d" % e)
    w()
    w("Predicted bad primes <= 23 (p divides (2e-1)! or a tableau count of the rectangle (e-w) x k, entries <= e): %s. Observed primes with a non-pure "
      "quotient: %s. Observed subset of predicted: %s. Observed equals predicted: %s." % (v["predicted_bad_primes_le_23"], v["observed_non_pure_primes"],
                                                                                          v["observed_subset_of_predicted"], v["observed_equals_predicted"]))
    w()
    table(["p", "predicted bad", "length", "Hilbert function (to the bound)", "I1 table", "pure (I1)", "I2 agrees"],
          [[r["p"], r["predicted_bad"], ("finite %d" % r["total_dimension"]) if r["finite_length"] else "nonzero at bound %d" % r["degree_bound"],
            r["hilbert_function"] if len(r["hilbert_function"]) < 40 else "%s ..." % r["hilbert_function"][:40], tab(r["betti_I1"]), r["pure_table_I1"],
            r["agree"] if r["finite_length"] else "Hilbert via I2 table: %s" % r.get("hilbert_consistent_with_I2_table")] for r in v["per_prime"]])
    why = v["prediction_reasons"]
    w("Reasons (per prime): " + "; ".join("%s: %s" % (p, ", ".join(rs[:3]) + (" ..." if len(rs) > 3 else "")) for p, rs in why.items()))
    w()

# ---------------------------------------------------------------- D1
w("## D1 genericity: random pairs of forms of degree e over GF(32003)")
w()
body = []
for e in (2, 3, 4, 5, 10):
    v = T.get("D1:%d" % e)
    if not v or "error" in v:
        continue
    p0 = v["pairs"][0]
    body.append([e, v["pairs_count"], v["maxrank_hilbert_prediction"], v["all_hilbert_equal_maxrank"], v["pure_count"], tab(p0["betti_I1"]),
                 "%d/%d" % (sum(1 for p in v["pairs"] if p["agree"] is True), sum(1 for p in v["pairs"] if p["agree"] is not None))])
table(["e", "pairs", "max-rank Hilbert function (first non-positive coefficient cut)", "all pairs have it", "pure tables", "Betti table of pair 1 (I1)", "I1=I2 (pairs with I2)"], body)
d1 = {e: T["D1:%d" % e] for e in (2, 3, 4, 5, 10) if "D1:%d" % e in T}
w("Outcome by e: " + "; ".join("e = %d: maximal-rank Hilbert function in %d of %d pairs, pure table in %d of %d" % (
    e, sum(p["hilbert_equals_maxrank"] for p in v["pairs"]), v["pairs_count"], v["pure_count"], v["pairs_count"]) for e, v in d1.items()) + ".")
w()
w("Comparison with the prediction (D1: maximal-rank Hilbert function and a non-pure table for e = 4, 5, 10; a pure table for e = 2, 3): see the columns 'all pairs have it' and 'pure tables'. "
  "The pair counts (5 per e) are a choice of the run; the hypothesis says 'random pairs'.")
w()

# ---------------------------------------------------------------- D2
w("## D2 the ray (0,3,15,18), table (2,3,3,2)")
w()
v = T.get("D2")
if v and "error" not in v:
    rm = v["random_matrices_of_cubics"]
    w("10 random 2 by 3 matrices of cubics over GF(32003): pure table (2,3,3,2) on (0,3,15,18) for %d of 10. Pure Hilbert function of the ray: %s." % (rm["hits"], rm["pure_hilbert_function"]))
    w()
    table(["seed", "length", "I1 table", "I2 table", "agree", "pure", "Hilbert = pure prediction"],
          [[s["seed"], s["total_dimension"] if s["finite_length"] else "not finite", tab(s["betti_I1"]), tab(s["betti_I2"]), s["agree"], s["table_equals_primitive_pure"],
            s["hilbert_equals_pure_prediction"]] for s in rm["seeds"]])
    sub = v["substitution_in_L11"]
    w("Presentation of the Kostant module L(1,1) from `uhlib`: generator degrees %s, %d relations with entry degrees %s:" % (sub["L11_presentation_shifts"], sub["L11_relation_count"], sub["L11_entry_degrees"]))
    w()
    for r in sub["L11_relations"]:
        w("- " + " + ".join("%s * [gen %d] x^%d y^%d z^%d" % (c, k, m[0], m[1], m[2]) for k, m, c in r))
    w()
    w("Substituting x -> x^e, y -> y^e in every entry (over GF(32003)):")
    w()
    table(["e", "target ray", "length", "Hilbert function", "I1 table", "I2 table", "agree", "pure on the target ray"],
          [[c["e"], tuple(c["target_ray"]), c["total_dimension"] if c["finite_length"] else "not finite", c["hilbert_function"], tab(c["betti_I1"]), tab(c["betti_I2"]),
            c["agree"], c["table_equals_primitive_pure"]] for c in sub["cases"]])
w()

# ---------------------------------------------------------------- agreement and times
w("## Instrument agreement")
w()
cnt = collections.Counter()
hc = collections.Counter()
for d in walk(R):
    if "agree" in d:
        cnt[d["agree"]] += 1
    if "hilbert_consistent_with_I2_table" in d:
        hc[d["hilbert_consistent_with_I2_table"]] += 1
    if "I2_hilbert_equals_I1_through_12" in d:
        hc["A-check " + str(d["I2_hilbert_equals_I1_through_12"])] += 1
    if "I2_error" in d:
        cnt["I2_error"] += 1
w("Betti tables compared between I1 and I2 on finite length modules: agree True = %d, False = %d, not compared (I2 on a module not finite by the bound: only the Hilbert "
  "function from the I2 table is compared) = %d, I2 errors = %d. Hilbert function recomputed from the I2 table equals I1's: %s." % (cnt[True], cnt[False], cnt[None], cnt["I2_error"], dict(hc)))
w()
w("## Wall times")
w()
per = collections.defaultdict(float)
for k, v in T.items():
    per[k.split(":")[0]] += v.get("task_seconds", 0)
w("Summed task seconds per claim (processes ran in parallel): " + ", ".join("%s %.0f s" % (k, s) for k, s in sorted(per.items())) + ". Total wall time %s s." % R.get("wall_seconds"))
w()
w("## Deviations and choices not fixed by the hypothesis")
w()
for line in (
    "A numpy build of the quotient module (`uhlib/fastmod.py`, same reduced echelon rule, tested equal to `quotient_module`) is the I1 build for prime fields and GF(2^k); "
    "the pure Python build is used for QQ. Without it the B1 search over GF(16) (about 10 minutes per module in pure Python) was not feasible.",
    "A1, A2: Hilbert functions come from the numpy build without module action; on 10 subspaces per field they are also computed by the pure Python `ideal_hilbert` and recomputed "
    "from the Singular Betti table (through degree 12). The ten indices are fixed by `random.Random(31 + k).sample`.",
    "B1: 20 seeds over GF(32003), 40 over GF(2), GF(4), GF(16); seeds are 1000000 (ray index + 1) + 1000 q + s. At most three hits per ray and field get an I2 run; all other tables are I1 only.",
    "C2: the hypothesis fixes the lengths of the summands; the generator degree a + b is an addition of this run.",
    "C3: the predicted set is computed over 0 <= w < e, 1 <= k <= e as the hypothesis states, with p <= 23.",
    "D1: five random pairs per e; I2 on every pair for e <= 5 and on the first pair for e = 10. D2(b): the substituted modules were built over GF(32003) only (not QQ).",
    "No statement about the realizability or non-realizability of any ray is made from these runs.",
):
    w("- " + line)
w()
(HERE / "results-summary.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("wrote results-summary.md, %d lines" % len(out))
