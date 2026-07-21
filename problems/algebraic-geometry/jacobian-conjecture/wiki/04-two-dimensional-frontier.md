# 04 - The two-dimensional frontier (JC(2), open)

JC(2) remains open. This page records exactly what our results say about it, and what they do
not: honesty gates apply (null results and conjectures are labeled as such).

## The exact obstruction to the mechanism (EXP-005)

For a nontrivial $\mathbb{G}_m$-action with weights $(1, -a)$ on $\mathbb{C}^2$, every
equivariant polynomial map has the form $P = x^{b_1} f(v)$, $Q = x^{b_2} g(v)$ with
$v = x^a y$ the ONLY independent weight-0 invariant, and (proved symbolically, generic $f, g$):
$$\det JF = x^{\,b_1 + b_2 + a - 1}\,\bigl(b_1\, f g' - b_2\, f' g\bigr).$$
Keller therefore forces $b_1 + b_2 = 1 - a$ and the single univariate ODE
$$b_1\, f g' - b_2\, f' g = \text{const} \ne 0.$$
By contrast, the 3D counterexample machine needs TWO independent invariants: with only one, the
reduced pair $(V', T')$ depends on one variable, $dV' \wedge dT' = 0$, so $J_2 \equiv 0$ and
$\det JF \equiv 0$ (a one-line proposition, recorded in EXP-005 as such). **The mechanism that
killed JC(3) is structurally unavailable in dimension 2.** Also checked: no coordinate slice of
the announced $F$ is a 2D Keller map.

## The rigidity theorem (EXP-010; formerly our conjecture)

**Theorem (2D equivariant rigidity).** For any $\mathbb{G}_m$-action with weights
$(w_1, -w_2)$, $w_1 \ge 1$, $w_2 \ge 0$, every equivariant polynomial Keller map of
$\mathbb{C}^2$ is LINEAR: $(f_0 x, g_0 y)$ or $(f_0 y, g_0 x)$.

Proof shape (every mechanical step machine-certified on sweeps, EXP-010): equivariant
components are a monomial times $f(v)$, $v = x^{w_2} y^{w_1}$; the determinant factors as a
monomial times the bracket $(i_1 j_2 - i_2 j_1) fg + v(\beta_1 f g' - \beta_2 f' g)$; constancy
forces the shapes $(x f, y g)$ or the swap (mixed shapes are never Keller); and the resulting
ODE $fg + v(w_1 f g' + w_2 f' g) = c$ has only constant solutions because its top coefficient
carries the strictly positive factor $1 + w_1 d_g + w_2 d_f$. EXP-006's 216 empirical instances
(all linear) are the experimental companion of this statement.

Consequence: a 2D counterexample, if one exists, must be genuinely NON-equivariant; the
symmetry class that produced the entire 3D counterexample family is completely closed in
dimension 2.

## The real picture of the 3D map (EXP-011)

Over $\mathbb{R}$, the announced $F$ restricts to a surjective, orientation-reversing
($\det = -2$), non-proper, non-injective real Keller map. The census: 1 or 3 real preimages,
separated by the discriminant wall ($D > 0$: three sheets; $D < 0$: one), with escapes exactly
on the wall. This also records that the constant-Jacobian REAL statement in dimension 3 falls
with the same example (Pinchuk 1994 covered the non-constant case in the plane).

## The honest map of the remaining routes to a 2D counterexample

If JC(2) is false, the counterexample must use one of:
1. **No symmetry at all** (generic maps): untouched by our obstruction; the classical evidence
   (Moh: degree $\le 100$) constrains low degrees only.
2. **Non-reductive symmetry** ($\mathbb{G}_a$-actions, unipotent flows): invariant rings in 2D
   are again univariate, so a naive transplant faces the same one-invariant collapse; whether a
   twisted variant escapes is genuinely open (JCB-012).
3. **Weighted structures over non-toric gradings** (e.g. valuations at infinity rather than
   monomial weights): connects to the classical Newton-polygon / Abhyankar program; queued with
   the JC(2) primary-literature pass (JCB-010).

Conversely, a PROOF of JC(2) along this program's lines would need a properness argument: show a
2D Keller map cannot have asymptotic values (the known equivalence: proper Keller implies
invertible). Our 3D family shows exactly HOW asymptotic values are produced (the reconstruction
inverse has denominators vanishing as $w$ approaches roots of $BC = k^2 p(w)$); the 2D question
is whether the one-invariant geometry leaves room for that escape. This is the sharpest
transferable question our results produce, and it is where the program pushes next (EXP-006/007).
