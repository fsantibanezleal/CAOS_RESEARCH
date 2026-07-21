# EXP-010 - Verdict: CONFIRMED (2026-07-21). The rigidity conjecture is now a theorem

Output: `artifacts/output-2026-07-21.txt`. All four predictions verified exactly.

## Theorem (2D equivariant rigidity; [D], every mechanical step [MV] on sweeps)

Let $\mathbb{G}_m$ act on $\mathbb{C}^2$ with weights $(w_1, -w_2)$, $w_1 \ge 1$, $w_2 \ge 0$,
and let $F = (P, Q)$ be an equivariant polynomial Keller map. Then $F$ is LINEAR:
$F = (f_0 x, g_0 y)$ or $F = (f_0 y, g_0 x)$ up to the equivariant monomial normalization.

Proof structure, with what was machine-certified:
1. Equivariant components are $P = x^{i_1} y^{j_1} f(v)$, $Q = x^{i_2} y^{j_2} g(v)$ with
   $v = x^{w_2} y^{w_1}$, and the determinant factors as
   $\det JF = x^{i_1+i_2-1} y^{j_1+j_2-1} [(i_1 j_2 - i_2 j_1) fg + v(\beta_1 f g' - \beta_2 f' g)]$,
   $\beta_r = w_1 i_r - w_2 j_r$. Certified [MV] for 8 weight pairs (including the semi-trivial
   $(1, 0)$) times all monomial exponents in $[0, 2]^4$, generic symbolic cubic $f, g$
   (648 identity checks).
2. Constancy of the determinant forces $i_1 + i_2 = 1$, $j_1 + j_2 = 1$ (the monomial
   prefactor must be trivial), and the mixed shapes $(xy\,f,\ g)$, $(f,\ xy\,g)$ admit NO
   Keller solution (their bracket is divisible by $v$). Certified [MV]: empty solve at degrees
   $\le 4$ for the whole weight sweep.
3. The surviving shapes reduce to the single ODE $fg + v(w_1 f g' + w_2 f' g) = c$ (or its
   swap). The coefficient of $v^N$ at the top bidegree $N = d_f + d_g$ is
   $(1 + w_1 d_g + w_2 d_f)\, f_{d_f} g_{d_g}$ with a strictly positive integer factor, so the
   top coefficients die and, by descent, $f$ and $g$ are constant. Certified [MV]: for the
   weight sweep and all exact bidegrees $(d_f, d_g) \ne (0, 0)$ up to 5, the constrained system
   (leading coefficients nonzero, $c \ne 0$) has EMPTY solution set; positivity of the kill
   factor checked for all degrees up to 19.

## Adversarial validation record

- The classification is not sampled at instances: predictions 2 and 3 are exact EMPTINESS
  statements of polynomial systems over $\mathbb{Q}$ with the nondegeneracy conditions imposed
  as equations (Rabinowitsch-style), the strongest refutation form available.
- Consistency with EXP-006: its 216 empirical instances were all linear; the theorem explains
  the observation.

## How could this be wrong?

- The arbitrary-degree/weight statement rests on the displayed general formulas (top
  coefficient and shape reduction), which are proved by inspection of the certified identity;
  the sweeps certify every mechanical step at bounded size. A fully formal arbitrary-degree
  proof assistant verification (e.g. Lean) would close the remaining distance; queued as an
  optional hardening item.
- Scope: $\mathbb{G}_m$-equivariant maps only. Non-equivariant 2D Keller maps are untouched;
  JC(2) remains open.

## Consequences

- The strongest 2D statement of the program so far: the symmetry class that produced the 3D
  counterexample is COMPLETELY closed in dimension 2, for every weight choice, not just a
  scanned window. A 2D counterexample, if any, must be genuinely non-equivariant (or use
  non-reductive/degenerate structures; JCB-012 pool).
- Upgrades wiki 04 and the manuscript conjecture to a theorem; EXP-006 stands as the empirical
  companion.
