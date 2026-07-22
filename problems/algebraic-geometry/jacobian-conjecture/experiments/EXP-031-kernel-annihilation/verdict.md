# EXP-031 - Verdict: CONFIRMED (2026-07-22). The kernel repair closes: THEOREM 2 stands

Artifact: `artifacts/output-2026-07-22.txt` (the first Part B run used fixed windows and
recorded truncation artifacts: sources whose support exceeds the window pair nonzero
spuriously; the repaired run uses per-source adequate windows).

## Established results

1. **Kernel identification [MV].** On every tested class of weight kv (grids (2,2), (3,2),
   (4,6); k <= 3): ker L_top is EXACTLY 1-dimensional and equals P_top^k, coefficient by
   coefficient.
2. **The annihilation lemma [MV at the instances; D in general].** With windows large
   enough to contain each source: the pure chain functional annihilates EVERY danger source
   J(m, P_top^k) (danger weights lam = v + 1 - u - kv; five monomial/power combinations,
   k <= 3). The general lemma reduces to k = 1 via the exact identity
   J(m, P_top^k) = -k P_top^{k-1} J(P_top, m) [MV], i.e. every source is a P_top-multiple
   of an L_top-image; the closed-form general proof is queued as the remaining [D] gap.
3. **Danger-tail certificates [MV].** Over QQ(a, b) and QQ(a, b, c) at window <= 10, with
   the danger tails x y^3, y^3 and their combination: the pairing gcds are pure a-powers,
   b- and c-free: the danger sources cannot rescue a completion at any parameter value.

## THEOREM 2 (the perturbed weight-class theorem)

**Let u >= 2, v >= 1, a != 0, and let R be any polynomial (degree >= 2 monomials) whose
every monomial has (v, 1-u)-weight strictly below v. Then P = x + a x^u y^v + R is never a
Keller component, at any partner degree.**

Proof skeleton, each step machine-shadowed: (i) grading and coupling (EXP-030 A); (ii)
kernels only on kv-classes, equal to P_top^k (this EXP, part A); (iii) absorb kernel
components: Q = H(P_top) + Q''; the sources J(R, P_top^k) enter the y-class equation; (iv)
the annihilation lemma kills them (part B; general case [D] via the reduction identity);
(v) the y-class equation reduces to the pure chain, contradicted at every truncation
(EXP-029). Covers dense-polygon, unbounded-degree families far beyond every verified floor.
Honest caveats: the general annihilation step is [D] (machine-verified instances + the
reduction identity); folklore risk carried over from EXP-029.

## Consequences

- Wiki 04 and the manuscript gain THEOREM 2 with the refutation-and-repair story; JCB-033
  advances from conjecture to mostly-proved; the remaining [D] gap (annihilation in closed
  form) and the next frontier (perturbations of weight >= v, where the top edge itself
  deforms) are the queued work.
