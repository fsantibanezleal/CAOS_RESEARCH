"""Exact distinct-strip arithmetic, admitted only after the complete local audit."""

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

from partitioned_audit import audit, require

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def transfer(directory):
    cover = audit(directory)
    packet_path = PROBLEM / "experiments/EXP-018-nine-point-distinct-transfer/artifacts/input/nine-point-final.json"
    packet = json.loads(packet_path.read_bytes())
    weights = dict(zip(map(tuple, packet["pair_order"]),
                       [Q(n, packet["pair_weight_denominator"]) for n in packet["pair_weight_numerators"]]))
    require(set(weights) == {(i, j) for i in range(9) for j in range(i+1, 9)}, "pair coverage")
    require(all(w >= 0 for w in weights.values()), "negative weight")
    capacities = [sum(weights[i, i+d] for i in range(9-d)) for d in range(1, 9)]
    require(all(x == 2 for x in capacities), "span capacity")
    window_path = PROBLEM / "experiments/EXP-019-nine-point-local-replay/artifacts/window-audit.json"
    window = json.loads(window_path.read_bytes())
    require(window["passed"] is True and window["packet_sha256"] == sha(packet_path), "window binding")
    require(window["code_sha256"] == sha(PROBLEM / "code/window_input_audit.py"), "window audit source")
    H = Q(window["H_cert"])
    require(H == Q(3362285207, 5000000000), "window coefficient")
    p, delta = Q(cover["binding"]["pressure"]), Q(cover["binding"]["target"])
    m, r, tau, c = 562, 8, Q(1203, 500), Q(1703, 500)
    D = delta*(m-r)
    a, beta = D/m, r*p*(m-r)/m
    residuals = {"first_threshold": c-1-tau, "second_threshold": c-2-tau/2,
                 "clipping": tau*tau-D, "first_trace": 6*c-7-c*c-a,
                 "second_trace": 4*c-2-c*c-2*a, "denominator": 2-a}
    require(all(x >= 0 for x in residuals.values()) and 2-a > 0, "invalid transfer")
    q = (1+H-beta)/(2-a)
    require(q == Q(2340938143167, 2795532013000), "independent fraction mismatch")
    delta20, p20, m20 = Q(3051, 500000), Q(1, 2500), 958
    q20 = (1+H-r*p20*(m20-r)/m20)/(2-delta20*(m20-r)/m20)
    require(q-q20 > Q(1, 10000), "predeclared value gate")
    return {"schema": "exp023-exact-transfer-audit-v1", "passed": True,
            "scope": "complete local certificate and exact transfer under explicitly attributed analytic inputs",
            "counted_objects": "distinct zero points in the whole critical strip",
            "denominator": "all nontrivial zeros counted with multiplicity up to height T",
            "liminf_fraction": str(q), "pressure": str(p), "delta": str(delta),
            "m": m, "r": r, "tau": str(tau), "c": str(c), "D": str(D),
            "a": str(a), "beta": str(beta), "capacities": list(map(str, capacities)),
            "residuals": {k: str(v) for k, v in residuals.items()},
            "conditional_exp020_fraction": str(q20), "gain_over_conditional_exp020": str(q-q20),
            "window_audit_sha256": sha(window_path), "packet_sha256": sha(packet_path),
            "cover_auditor_sha256": cover["auditor_sha256"],
            "reports_sha256": cover["reports_sha256"], "totals": cover["totals"],
            "transfer_auditor_sha256": sha(Path(__file__)),
            "analytic_dependencies": ["BGSTB integrated complex-zero pair-correlation theorem and preserved correction",
                                      "Knausgard mixed Gram and threshold assembly, rederived in EXP019 review"],
            "excluded_claims": ["RH", "simple critical-line proportion", "effective height",
                                "short-window onset improvement", "external peer review", "worldwide priority"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = transfer(args.output_dir)
    args.receipt.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(result["liminf_fraction"])
