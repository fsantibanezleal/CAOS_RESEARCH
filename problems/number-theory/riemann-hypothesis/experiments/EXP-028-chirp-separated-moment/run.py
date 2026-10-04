"""One conditional onset control; the proposed moment range is unproved."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

from flint import arb, ctx, fmpq

HERE = Path(__file__).resolve().parent


def ball(x):
    x = F(x)
    return arb(fmpq(x.numerator, x.denominator))


def run(receipt):
    if receipt.exists():
        raise SystemExit("Preserve previous receipt")
    started = time.process_time()
    source = HERE.parent / "EXP-010-levinson-parity-transfer/artifacts/canonical/result.json"
    raw = source.read_bytes()
    old = json.loads(raw)
    assert old["accepted"] is True
    theta, nu = F(5339, 10000), F(349, 10000)
    entry = next(x for x in old["detector_constants"] if F(x["nu"]) == nu)
    assert entry["constraints"] == {"P(0)": "0", "P(1)": "1", "Q(0)": "1", "Q(y)+Q(1-y)": "1"}
    kappa = F(entry["kappa"]["lower"])
    first = F(17, 20)*(1-2*theta)+F(33, 20)*nu
    second = 1-2*theta+F(15, 8)*nu
    assert first == F(-9, 200000) and second == F(-189, 80000)
    assert first < 0 and second < 0
    assert theta-F(1, 2) < nu < min(F(1, 2), F(17, 33)*(2*theta-1))
    ctx.prec = 256
    t, k, root2 = ball(theta), ball(kappa), arb(2).sqrt()
    c = 2-t/2-(t/root2).cot()/root2
    h = (3+k-((1-k)*(9-k-8*c)).sqrt())/4
    assert h > 0
    assert time.process_time()-started < 30
    result = {"schema": "exp028-conditional-onset-v1", "passed_conditional_controls": True,
              "analytic_moment_theorem_proved": False,
              "hypothesis_sha256": hashlib.sha256((HERE / "hypothesis.md").read_bytes()).hexdigest(),
              "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "detector_receipt_sha256": hashlib.sha256(raw).hexdigest(),
              "theta": str(theta), "nu": str(nu), "existing_onset": "267/500",
              "old_length_range_rejects_this_nu": True,
              "proposed_moment_upper_nu": str(F(17, 33)*(2*theta-1)),
              "E1": str(first), "E2": str(second), "certified_kappa_lower": str(kappa),
              "pair_term": str(c), "conditional_simple_parity_lower": str(h),
              "arithmetic_trust": "Existing EXP-010 detector certificate is a premise; new scalar parity check uses Arb.",
              "cpu_seconds": time.process_time()-started,
              "scope": "Conditional compatibility only. No established new onset or moment range."}
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    run(parser.parse_args().receipt)
