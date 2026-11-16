"""EXP-146 mutants (review F12): the gates must fail on a broken bound engine or a broken image formula.

Each mutant is stated exactly, run on the production gate setup (the same cases, seeds and sizes as run.py), and its
result is written to artifacts/mutants.json. Run from the repository root:
  .venv/Scripts/python.exe problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-146-case1-chain-certificate/mutants.py

  M1  res_bound output lowered: every entry of the returned table B_h(w) is replaced by B_h(w) - 1 (all weights, w = 0
      included); checked by G2 random (2,000 pairs, as in run.py).
  M1b the same lowering applied only to the second step of the composition family (600 cases, as in run.py).
  M2  degree-drop factor removed: res_image returns Res(phi f, phi g) without the factor (-1)^(n (m - m')) lc(phi g)^(m - m');
      checked by G3 (500 cases, as in run.py) and by its first 60 cases.
The unmutated gates are run first on the same inputs as the baseline (0 violations, 0 mismatches expected).
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import chaincert as cc  # noqa: E402
import gates  # noqa: E402

ART = HERE / "artifacts"


def lowered(orig, delta=1, only_xi=None):
    """res_bound with every table entry lowered by delta (only for the elimination variable index only_xi, if given)."""
    def res_bound_lowered(*a, **k):
        B = orig(*a, **k)
        if B is None or (only_xi is not None and a[6] != only_xi):
            return B
        return cc.Bd(B.vs, {key: v - delta for key, v in B.tab.items()})
    return res_bound_lowered


def factor_removed(F, G, xi, xname, m, p):
    return F.resultant(G, xname)


def main():
    prime1 = cc.Prime(gates.P1, gates.R1)
    out = {"experiment": "EXP-146", "mutants": {}, "baseline": {}}
    orig_bound, orig_image = cc.res_bound, cc.res_image
    t = time.time()
    out["baseline"]["G2_random_2000"] = gates.g2_random(2000)
    out["baseline"]["G2_composition_600"] = gates.g2_composition(600)
    out["baseline"]["G3_500"] = gates.g3_degree_drop(500, prime1)
    out["baseline"]["G3_60"] = gates.g3_degree_drop(60, prime1)
    try:
        cc.res_bound = lowered(orig_bound)
        g2 = gates.g2_random(2000)
        out["mutants"]["M1_res_bound_minus_1_G2_random"] = {
            "mutation": "every entry of the table returned by res_bound lowered by 1",
            "weights_checked": g2["weights_checked"], "violations": g2["violations"],
            "pairs_kept": g2["cases"], "gate_fails": not g2["pass"]}
        cc.res_bound = lowered(orig_bound, only_xi=1)
        comp = gates.g2_composition(600)
        out["mutants"]["M1b_res_bound_minus_1_second_step_composition"] = {
            "mutation": "every entry of the table returned by res_bound lowered by 1 in the second composed step "
                        "(elimination of a), the first step (elimination of x) unchanged",
            "weights_checked": comp["composition_weights"], "violations": comp["composition_violations"],
            "cases": comp["composition_cases"], "gate_fails": not comp["pass"]}
    finally:
        cc.res_bound = orig_bound
    try:
        cc.res_image = factor_removed
        for n in (60, 500):
            g3 = gates.g3_degree_drop(n, prime1)
            out["mutants"][f"M2_degree_drop_factor_removed_G3_{n}"] = {
                "mutation": "res_image without the factor (-1)^(n (m - m')) lc(phi g)^(m - m')",
                "cases": g3["cases"], "mismatches": g3["mismatches"], "gate_fails": not g3["pass"]}
    finally:
        cc.res_image = orig_image
    out["seconds"] = round(time.time() - t, 1)
    out["all_mutants_caught"] = all(v["gate_fails"] for v in out["mutants"].values())
    out["baseline_clean"] = (out["baseline"]["G2_random_2000"]["pass"] and out["baseline"]["G2_composition_600"]["pass"]
                             and out["baseline"]["G3_500"]["pass"])
    ART.mkdir(exist_ok=True)
    (ART / "mutants.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out["mutants"], indent=1))
    print("all mutants caught:", out["all_mutants_caught"], "baseline clean:", out["baseline_clean"])
    return 0 if out["all_mutants_caught"] and out["baseline_clean"] else 1


if __name__ == "__main__":
    sys.exit(main())
