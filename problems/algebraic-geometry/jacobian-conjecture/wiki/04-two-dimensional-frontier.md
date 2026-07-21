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

## What we conjecture (not yet proved)

**Conjecture (2D equivariant rigidity).** Every $\mathbb{G}_m$-equivariant Keller map of
$\mathbb{C}^2$ is invertible. Status after EXP-006 (branch-symbolic enumeration with a
valuation-aware ansatz, which fixed EXP-005's vacuous scan): the scan is now real, and the
outcome is SHARPER than the conjecture within its window. Over $a \in \{1,2,3\}$,
$b_1 \in [-3, 3]$, $\deg f, \deg g \le 3$: 382 solution branches produced 216 polynomial Keller
instances, 648 in-image fibers were computed exactly, every fiber has one preimage, and every
surviving instance is LINEAR (diagonal or swap form): nothing nonlinear even exists as an
equivariant Keller map in the window. The conjecture stands unrefuted with real supporting
coverage; beyond the window it remains a conjecture (general weight pairs and higher degrees
are the queued widening).

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
