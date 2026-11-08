"""JCB-103 preflight probe (not a result): how unbalanced are the coefficients of the branch equations across the
archimedean embeddings of L? For each coefficient c (in the basis 1, y, ..., y^4), compare log10 max_sigma |sigma(c)|
with log10 |N(c)| / 5 (the balanced size). A large gap means scaling by units of L could shorten the inputs."""
import json
import sys

from flint import acb, arb, ctx, fmpq_poly, fmpz

ctx.prec = 3000
P = fmpq_poly([26, 0, 3, 3, -1, 1])
roots = [r for r, m in P.complex_roots()]
print("signature: real roots", sum(1 for r in roots if abs(r.imag) < 1e-30), "of", len(roots))
d = json.load(open(sys.argv[1]))
gaps = []
for e in d["eqs"]:
    for mon, cs in e:
        if not any(cs):
            continue
        vals = [sum(acb(c) * (r ** j) for j, c in enumerate(cs)) for r in roots]
        logs = [float((abs(v)).log() / arb(10).log()) for v in vals]
        lmax = max(logs)
        lnorm = sum(logs) / 5
        gaps.append(lmax - lnorm)
gaps.sort()
print(f"coefficients {len(gaps)}; gap (log10 max embedding - log10 norm / 5): min {gaps[0]:.1f}, "
      f"median {gaps[len(gaps) // 2]:.1f}, max {gaps[-1]:.1f}")
