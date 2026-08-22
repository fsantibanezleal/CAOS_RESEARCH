"""EXP-009: symmetry audit. See hypothesis.md."""
import json, sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))
from tclib.enum import census_polynomials

t0 = time.time()
per_depth, first_seen, complete = census_polynomials(5)
assert all(complete.values())
print(f"catalog: {len(first_seen)} polys ({time.time()-t0:.1f}s)", flush=True)

def reflect(p):  # f(x) -> f(-x)
    return tuple(c if i % 2 == 0 else -c for i, c in enumerate(p))

def neg(p):
    return tuple(-c for c in p)

res = {}
for name, op in (("reflection", reflect), ("negation", neg)):
    eq = uneq = missing = 0
    examples = []
    viol = 0
    for p, d in first_seen.items():
        q = op(p)
        dq = first_seen.get(q)
        if dq is None:
            missing += 1          # partner has tau = 6 (catalog cap): unequal
            if len(examples) < 8:
                examples.append((list(p), d, "partner tau>5"))
            continue
        if dq == d:
            eq += 1
        else:
            uneq += 1
            if abs(dq - d) > 1:
                viol += 1
            if len(examples) < 8:
                examples.append((list(p), d, dq))
    total = len(first_seen)
    res[name] = {"equal": eq, "unequal": uneq, "partner_beyond_catalog": missing,
                 "abs_diff_gt1_violations": viol,
                 "equal_fraction_within_catalog": round(eq / (eq + uneq), 4),
                 "examples_unequal": examples}
    print(name, res[name]["equal_fraction_within_catalog"], "eq", eq, "uneq", uneq,
          "missing", missing, "viol>1", viol, flush=True)

# committed counterexamples
cx = {"2x": (first_seen.get((0, 2)), first_seen.get((0, -2))),
      "x^2": (first_seen.get((0, 0, 1)), first_seen.get((0, 0, -1)))}
print("counterexamples (tau, tau_partner):", cx, flush=True)
res["committed_counterexamples"] = {k: list(v) for k, v in cx.items()}
(HERE / "artifacts").mkdir(exist_ok=True)
(HERE / "artifacts" / "symmetry.json").write_text(json.dumps(res, indent=1), "utf-8")
print("done", flush=True)
