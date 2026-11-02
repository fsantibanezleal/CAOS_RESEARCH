"""EXP-137 entry point: independent verification of the claimed (72,108) exclusion (P1 to P4).

Run from the repository root:
    .venv/Scripts/python.exe problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-137-helali-72108-independent-verification/run.py

Stages (each checkpointed in artifacts/*.json, flushed progress in artifacts/run-log.txt; delete a checkpoint to redo):
  P1 derive, P2 first block (Singular modStd + fglm), P2b relation to Helali's degree-5 field, P3 certificate identities
  (restricted unpickler only), P3 links (own cascade, Case 2 unit ideal, Case 1 compatibility system), P4 controls.
No script of the external archive is executed or imported; it is read as data only.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.setrecursionlimit(10000)

import derive  # noqa: E402
import p2_firstblock as P2  # noqa: E402
import p3_certs as P3  # noqa: E402
import p3_link as LK  # noqa: E402

ART = HERE / "artifacts"
ART.mkdir(exist_ok=True)
LOG = ART / "run-log.txt"


def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def clean(d):
    if isinstance(d, dict):
        return {k: clean(v) for k, v in d.items() if not str(k).startswith("_")}
    if isinstance(d, (list, tuple)):
        return [clean(x) for x in d]
    return d


def checkpoint(name, fn):
    path = ART / f"checkpoint-{name}.json"
    if path.exists():
        log(f"stage {name}: using checkpoint {path.name}")
        return json.loads(path.read_text())
    t0 = time.time()
    log(f"stage {name}: start")
    res = clean(fn())
    res["_wall_seconds"] = round(time.time() - t0, 1)
    path.write_text(json.dumps(res, indent=1, default=str))
    log(f"stage {name}: done in {res['_wall_seconds']} s")
    return res


def p2b_relation():
    """H(a7) = G(a7^7); relate the degree-5 polynomial G to Helali's field Q[w]/(w^5-w^4+3w^3+3w^2+26)."""
    from flint import fmpq_poly

    lex = P2.parse_lex((ART / "p2_singular.out").read_text())
    import sympy as sp

    H = P2.qpoly_from_expr(lex[1], sp.Symbol("a7"))
    Gc = [H[7 * k] for k in range(6)]
    assert all(H[i] == 0 for i in range(H.degree() + 1) if i % 7)
    G = fmpq_poly(Gc)
    G = G / G[5]
    res = {"H_is_polynomial_in_a7^7": True, "G_degree": G.degree()}
    cont, facs = G.factor()
    res["G_irreducible_over_Q"] = bool(len(facs) == 1 and facs[0][1] == 1 and facs[0][0].degree() == 5)
    cont, facs = H.factor()
    res["H_factorization_over_Q"] = {"content": f"{cont.p}/{cont.q}", "factors": [(f.degree(), m) for f, m in facs]}
    res["H_irreducible_over_Q"] = bool(len(facs) == 1 and facs[0][1] == 1)
    res["G_monic_coefficients_low_to_high"] = [f"{int(c.p)}/{int(c.q)}" for c in (G[i] for i in range(6))]
    Lp = fmpq_poly([26, 0, 3, 3, -1, 1])
    _c, lf = Lp.factor()
    res["helali_L_minpoly"] = "w^5 - w^4 + 3w^3 + 3w^2 + 26"
    res["helali_L_minpoly_irreducible_over_Q"] = bool(len(lf) == 1 and lf[0][0].degree() == 5)
    # Does G have a root in L = Q[w]/(minpoly)?  <=> Q[v]/(G) embeds in L (both degree 5) <=> isomorphic
    gens = "+".join(f"({G[i].p}/{G[i].q})*v^{i}" for i in range(6) if G[i] != 0)
    sing = P2.SCRATCH / "p2b_relation.sing"
    sing.write_text(f"""short=0;
ring R=(0,w),(v),dp;
minpoly=w^5-w^4+3*w^3+3*w^2+26;
poly G={gens};
ideal fa=factorize(G,1);
"NFACT="+string(size(fa));
int i;
for(i=1;i<=size(fa);i++){{ "DEGFACTOR="+string(deg(fa[i])); }}
quit;
""")
    r = subprocess.run(["wsl", "-e", "Singular", "-q", P2.wsl_path(sing)], capture_output=True, text=True, timeout=1800)
    (ART / "p2b_relation_singular.out").write_text(r.stdout + r.stderr)
    degs = [int(x) for x in re.findall(r"DEGFACTOR=(\d+)", r.stdout)]
    res["G_factor_degrees_over_helali_L"] = degs
    res["G_has_root_in_helali_L"] = bool(1 in degs)
    res["relation"] = ("Q[v]/(G) is isomorphic to Helali's L" if 1 in degs and res["G_irreducible_over_Q"] else
                       "G has no root in L: the fields Q[v]/(G) and L are not isomorphic (as fields of degree 5)"
                       if degs else "undetermined")
    res["k_field"] = "K = Q[a7]/(H), degree 35 = 5 * 7 over Q(v) with v = a7^7; L has degree 5"
    res["singular_output_file"] = "artifacts/p2b_relation_singular.out"
    return res


def main():
    LOG.write_text(LOG.read_text() + "--- new invocation ---\n" if LOG.exists() else "")
    log("EXP-137 run start")
    results: dict = {}

    # ---------------- P1
    p1 = checkpoint("p1", derive.main)
    c1, c2 = p1["case1"], p1["case2"]
    cmp1, cmp2 = c1["compare_with_helali_J"], c2["compare_with_helali_J"]
    p1_ok = (
        p1["chain_rule"]["[t,z]_{x,y}"] == -1 and p1["chain_rule"]["x2_minus_t2z4"] == 0
        and p1["chain_rule"]["bracket_xy_equals_minus_bracket_tz"]
        and all(cmp2[f"J{k}_equal"] for k in range(5))
        and all(cmp1[f"J{k}_equal"] for k in (4, 3, 2))
        and all(cmp1[f"J{k}_equal_up_to_negative_band_cross_terms"] for k in range(5))
        and p1["adverse_polygon_control"]["band_system_changed"]
    )
    results["P1"] = {
        "status": "PASS" if p1_ok else "FAIL",
        "claim": "our derivation of the band equations from the polygons agrees with Helali J4..J0",
        "evidence": p1,
        "case1_negative_band_note": (
            "Case 1 has 209 raw coefficient equations in negative bands (-1..-20) and 93 in bands 4..0; J1 and J0 of Case 1 "
            "contain extra cross terms with negative bands (18 and 19 coefficient equations), equal to the bracket restricted "
            "to pairs with a negative band. Helali's J4..J0 are the upper-band-only formulas and are exact for Case 2 and for "
            "J4..J2 of Case 1."),
    }

    # ---------------- P2
    p2 = checkpoint("p2", lambda: P2.run(log=log))
    p2b = checkpoint("p2b", p2b_relation)
    results["P2"] = {"status": p2["status"], "evidence": p2, "relation_to_helali_field": p2b}

    # ---------------- P3 identities
    ours_hash = p2["eliminant_monic_hash"]

    def certs():
        out = {}
        out["case2_unit_identity"] = P3.check_sum_identity("case2", "case2_exact_certificate.pkl",
                                                           "jc2-case2-nullstellensatz-v1", None, ours_hash, log)
        out["case1_h0_branch_s_eq_c"] = P3.check_sum_identity("b1", "h0_branch1_exact_certificate.pkl",
                                                              "jc2-h0-nullstellensatz-v1", "s=c", ours_hash, log)
        out["case1_h0_branch_s_eq_minus_c"] = P3.check_sum_identity("b2", "h0_exact_certificate.pkl",
                                                                    "jc2-h0-nullstellensatz-v1", "s=-c", ours_hash, log)
        out["case1_hard_identity_s_eq_c"] = P3.check_hard_identity(log)
        return out

    certs_res = checkpoint("certs", certs)

    # ---------------- P3 links
    F, A, D = LK.our_field(log=log)
    link2 = checkpoint("link_case2", lambda: LK.case2_link(F, A, D, log=log))

    def c1link():
        r = LK.case1_link(F, A, D, log=log)
        cas = r["_cascade"]
        r["split"] = LK.case1_split_check(F, cas)
        return r

    link1 = checkpoint("link_case1", c1link)

    # Case 1 Singular attempts (recorded, not re-run: they exceed the declared CPU budget)
    c1_attempt = {
        "status": "UNVERIFIED",
        "what_was_attempted": (
            "Our 13 compatibility equations (6 parameters, over K) were passed to Singular nfmodStd and std, and the 9 "
            "equations left after s=c were passed to nfmodStd and std. nfmodStd forks about 25 processes: after about 10 "
            "minutes of wall time (about 4 CPU-hours across processes) none returned and they were killed to respect the "
            "6 CPU-hour budget; the single-core std runs had also not returned after about 10 minutes. No result was obtained; "
            "this is a budget stop, not a finding."),
        "consequence": "Case 1 emptiness is not independently decided by our own Groebner run; the Case 1 link rests on the "
                       "span equality of the 13 compatibility equations and the split check below.",
    }

    # ---------------- assemble P3
    id_ok = all(certs_res[k]["status"] == "PASS" for k in certs_res if not k.startswith("_"))
    c2_ok = link2["status"] == "PASS"
    results["P3"] = {
        "status": "UNVERIFIED",
        "why": "the four identities pass and Case 2 is independently excluded, but the link of the Case 1 certificate "
               "generators (h=0 systems and the hard-identity system E_i) to the P1 equations is only partial",
        "identity_checks_all_pass": id_ok,
        "certificates": certs_res,
        "case2": {
            "status": "PASS" if (c2_ok and certs_res["case2_unit_identity"]["status"] == "PASS") else "FAIL",
            "provenance_of_singular_input": (
                "derived by our own code: lattice points from the polygons (exp137_lib.lattice_points), bracket weights "
                "(p*c - a*q), our own D from J4 in K = Q[a7]/(H) with H from our own Singular modStd, then our layered "
                "linear solve over K (cascade.py layers 3..0). No Helali data other than the comparison are used; the 25 "
                "equations are written to Singular by singular_unit_script"),
            "independent_exclusion_of_case2": bool(link2["singular_unit_ideal"]),
            "our_certificate": "Singular std over (0,u) returns the standard basis {1} for our 25 equations (artifacts/case2_unit_singular.out)",
            "helali_generators_equal_ours": link2["helali_generators_equal_ours_up_to_constant_and_param_permutation"],
            "evidence": link2,
        },
        "case1": {
            "link_compat_13": link1["helali_compat_span_equal_to_ours_per_layer_up_to_param_permutation"],
            "split": link1["split"],
            "hard_and_h0_generator_link": {
                "status": "UNVERIFIED",
                "reason": "the systems E_i (hne0_polred.pkl) and the h=0 systems are produced from the 13 compatibility "
                          "equations by the branch split, the elimination of r, an affine shift in h, a weighted rescaling "
                          "and a descent from degree 35 to degree 5; we verified the first two links (13 equations equal up to "
                          "layer-wise span; s^2 = gamma split exhaustive) but did not reproduce the remaining steps or decide the "
                          "branch systems by our own Groebner run",
            },
            "own_groebner_attempt": c1_attempt,
        },
    }

    # ---------------- P4
    cc = certs_res
    p4 = {
        "case2_corrupt_multiplier_fails": cc["case2_unit_identity"]["p4_corrupt_multiplier_coefficient_identity_fails"],
        "case2_corrupt_generator_fails": cc["case2_unit_identity"]["p4_corrupt_generator_coefficient_identity_fails"],
        "h0_s_eq_c_corrupt_multiplier_fails": cc["case1_h0_branch_s_eq_c"]["p4_corrupt_multiplier_coefficient_identity_fails"],
        "h0_s_eq_c_corrupt_generator_fails": cc["case1_h0_branch_s_eq_c"]["p4_corrupt_generator_coefficient_identity_fails"],
        "h0_s_eq_minus_c_corrupt_multiplier_fails": cc["case1_h0_branch_s_eq_minus_c"]["p4_corrupt_multiplier_coefficient_identity_fails"],
        "h0_s_eq_minus_c_corrupt_generator_fails": cc["case1_h0_branch_s_eq_minus_c"]["p4_corrupt_generator_coefficient_identity_fails"],
        "hard_corrupt_certificate_coefficient_fails": cc["case1_hard_identity_s_eq_c"]["p4_corrupt_certificate_coefficient_identity_fails"],
        "hard_corrupt_generator_coefficient_fails": cc["case1_hard_identity_s_eq_c"]["p4_corrupt_generator_coefficient_identity_fails"],
        "adverse_polygon_changes_band_system": p1["adverse_polygon_control"]["band_system_changed"],
        "adverse_polygon_detail": p1["adverse_polygon_control"],
    }
    results["P4"] = {"status": "PASS" if all(v for k, v in p4.items() if k != "adverse_polygon_detail") else "FAIL",
                     "evidence": p4}

    results["_meta"] = {
        "experiment": "EXP-137", "date": time.strftime("%Y-%m-%d"),
        "external_scripts_executed_or_imported": False, "standard_unpickler_used": False,
        "pickles_read_via": "exp137_lib.restricted_loads (builtins containers/scalars and fractions.Fraction only)",
        "archive_pickles_scanned_for_globals": "all loaded pickles contain no GLOBAL/STACK_GLOBAL/REDUCE opcodes (pickle_global_opcodes in certs)",
        "no_floating_point_in_any_decision": True,
    }
    (ART / "results.json").write_text(json.dumps(results, indent=1, default=str))
    log("results.json written: " + ", ".join(f"{k}={results[k]['status']}" for k in ("P1", "P2", "P3", "P4")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
