"""Exact dyadic exponent controls, including the narrower window and far tail."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent


def audit():
    started = time.process_time()
    theta, nu, eta = F(5339, 10000), F(349, 10000), F(1, 100000)
    gaussian_theta = theta-eta
    rho = 1-2*gaussian_theta
    bound1 = F(17, 20)*rho+F(33, 20)*nu
    bound2 = rho+F(15, 8)*nu
    assert (bound1, bound2) == (F(-7, 250000), F(-937, 400000))
    assert bound1 < 0 and bound2 < 0
    assert nu < F(17, 33)*(2*gaussian_theta-1)
    assert nu < 2*gaussian_theta-1
    # Separate source monomials; no final-exponent formula is substituted here.
    count = 0
    worst = [None, None]
    for gi in range(9):
        g = nu*F(gi, 8)
        for pi in range(13):
            p = (nu-g)*F(pi, 12)
            for qi in range(13):
                q = (nu-g)*F(qi, 12)
                cutoff = rho+p+q
                # All pieces of the N slope, plus far-tail stress points.
                dual_scales = {F(0), max(F(0), cutoff), p+q, F(1, 2), F(1), F(2)}
                if cutoff > 0:
                    dual_scales.add(cutoff/2)
                for r in sorted(dual_scales):
                    sigma = F(1, 4) if r <= cutoff else F(17, 4)
                    normalization = -g+sigma*rho
                    norms = (sigma-F(1, 2))*(p+q)+(F(1, 2)-sigma)*r
                    parameter = max(F(0), r-p-q)/2
                    terms = [F(7, 20)*(r+p+q)+max(p, q)/4,
                             F(3, 8)*(r+p+q)+(r+max(p, q))/8]
                    for k, theorem in enumerate(terms):
                        total = normalization+norms+parameter+theorem
                        target = (bound1, bound2)[k]
                        assert total <= target, (g, p, q, r, k, total, target)
                        if worst[k] is None or total > worst[k][0]:
                            worst[k] = (total, g, p, q, r)
                    count += 1
    # Universal slope signs supply the dyadic N summation, beyond the grid.
    low_slopes = [F(1, 2)-F(1, 4)+F(7, 20),
                  F(1, 2)-F(1, 4)+F(3, 8)+F(1, 8)]
    high_slopes = [x-4+F(1, 2) for x in low_slopes]
    assert low_slopes == [F(3, 5), F(3, 4)]
    assert all(x > 0 for x in low_slopes)
    assert all(x < 0 for x in high_slopes)
    # Each engineered wrong choice changes an actual necessary inequality.
    wrong_eta = F(1, 10000)
    assert F(17, 20)*(1-2*(theta-wrong_eta))+F(33, 20)*nu > 0
    endpoint = F(17, 33)*(2*gaussian_theta-1)
    assert not F(17, 20)*rho+F(33, 20)*endpoint < 0
    separation = (1-gaussian_theta)/2
    assert bound1+separation > 0
    assert any(x+F(1, 2) > 0 for x in low_slopes)  # no tail contour change
    assert max(F(0), F(2)-2*nu)/2 > 0  # parameter grows; its reversal is wrong
    assert time.process_time()-started < 30
    return {"arithmetic": "stdlib Fraction only", "theta": str(theta),
            "nu": str(nu), "eta": str(eta), "gaussian_theta": str(gaussian_theta),
            "charged_exponents": [str(bound1), str(bound2)],
            "exact_dyadic_boxes": count,
            "worst_grid_exponents_and_scales": [[str(v) for v in item] for item in worst],
            "low_N_slopes": [str(x) for x in low_slopes],
            "high_N_slopes_including_parameter_growth": [str(x) for x in high_slopes],
            "negative_controls": {"oversized_window_loss_rejected": True,
                                  "zero_margin_rejected": True,
                                  "doubled_separation_rejected": True,
                                  "uncontrolled_tail_rejected": True,
                                  "reversed_parameter_factor_rejected": True},
            "analytic_moment_theorem_proved": False,
            "scope": "Exponent accounting only; universal analysis is in mellin-proof.md.",
            "cpu_seconds": time.process_time()-started}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    destination = parser.parse_args().receipt
    if destination.exists():
        raise SystemExit("Preserve previous receipt")
    result = {"schema": "exp028-adversarial-exponents-v1", "passed": False,
              "auditor_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "declaration_sha256": hashlib.sha256((HERE / "adversarial-declaration.md").read_bytes()).hexdigest()}
    try:
        result["audit"] = audit()
        result["passed"] = True
    except AssertionError as error:
        result["failure"] = str(error) or "An exponent obligation failed"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
    raise SystemExit(0 if result["passed"] else 1)
