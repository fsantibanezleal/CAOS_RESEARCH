# 03 - The seed family (constructor v2): the general counterexample machine

Our main generalization result (EXP-003 failure analysis + EXP-004 verification, all exact).

## Data and construction

Take:
- a **seed** $p(w) = \sum_{i=1}^{d} p_i w^i$ with
  $$p(0) = 0, \qquad \int_0^1 p = 0, \qquad p(1) \ne 0, \qquad p'(1) \ne 2\,p(1);$$
- a **scale** $k \ne 0$; set $m = -k\,p(1)$;
- a **section** $q(v)$ with $q(0) = k$, $q'(0) = \beta = \dfrac{k\,(p(1) - p'(1))}{p'(1) - 2 p(1)}$,
  and ARBITRARY polynomial tail beyond degree 1.

Let $\Phi(w) = \int_0^w p$, $u = 1 + v$, $s = c_1 = q(v) - t$, $w = u s / k$, and define the
reduced data in **potential form**:
$$V' = k^2 p(w) + m\,s, \qquad T' = w\,V' - k^2 \Phi(w),$$
$$b_1 = V'/s = k^2\,\frac{p(w)}{s} + m, \qquad a_1 = T'/s^2 = \frac{u\,b_1}{k} - k^2\,\frac{\Phi(w)}{s^2}$$
(both polynomial in $(v, t)$ because $p$ has valuation 1 and $\Phi$ valuation 2). The map is
$$F_{p,k,q} = \left(\frac{a_1}{x^2},\ \frac{b_1}{x},\ x\,c_1\right)\bigg|_{v = xy,\ t = x^2 z} : \mathbb{C}^3 \to \mathbb{C}^3.$$

## Verified laws

- **Keller, always:** $\det JF_{p,k,q} = -\dfrac{m^2}{k} = -k\,p(1)^2$, a nonzero constant, for
  EVERY admissible datum, including every $q$-tail. (Potential form makes
  $J_2 = m^2 s^2/k$ automatic; the three admissibility conditions are exactly the low-weight
  polynomiality constraints at the origin.)
- **Fiber degree $= d + 1$:** preimages of $(A, B, C)$ correspond to roots of
  $k^2 \Phi(w) - (w\,BC - AC^2) = 0$.
- **Exact reconstruction inverse:** from a root $w$:
  $s = (BC - k^2 p(w))/m$, $u = kw/s$, $x = C/s$, $v = u - 1$, $t = q(v) - s$, $y = v/x$,
  $z = t/x^2$ (verified as an identity modulo the fiber polynomial).
- **The announced map is the minimal instance** $p = 2w - 3w^2$, $k = 2$, $q$ affine; at $d = 2$
  the shape is rigid (EXP-003: unique up to $k$).

## New explicit counterexamples (ours, with rational collision certificates)

| Instance | Seed $p$ | $k$ | $\det$ | Degrees | Fiber deg | Collision (both map to the target) |
|---|---|---|---|---|---|---|
| P3 | $w - 2w^3$ | 3 | $-3$ | $(12, 11, 4)$ | 4 | $(-\tfrac{1}{15}, 18, 5130)$ and $(\tfrac{1}{24}, -18, -10368) \mapsto (-54, -54, 1)$ |
| P4 | $8w - 12w^2 + 4w^3 - 5w^4$ | 14 | $-350$ | $(17, 16, 4)$ | 5 | verified (see EXP-004 artifacts) |
| P5 | $2w - 3w^2$, $q$-tail $v^2$ | 2 | $-2$ | $(8, 7, 5)$ | 3 | verified (see EXP-004 artifacts) |
| P5d5 | $w - 3w^5$ | 5 | $-20$ | $(22, 21, 4)$ | 6 | $(-\tfrac{1}{70}, 75, 399000)$ and $(\tfrac{1}{160}, -150, -3824000) \mapsto (-750, -750, 1)$ (EXP-008) |

## Degree laws and minimality within the family (EXP-008)

For affine sections $q$ the component degrees are exactly $(5d - 3,\, 5d - 4,\, 4)$ (verified
$d = 2..5$); the scale $k$ never changes degrees; $q$-tails strictly increase them; and degree-1
seeds are impossible (the integral condition kills them), so the fiber-degree floor is 3.
Consequently the minimum degree vector over the whole family is $(7, 6, 4)$, attained exactly at
the announced map $F$: **the July 2026 counterexample is THE smallest instance of its own
family.** Whether any $\mathbb{C}^3$ counterexample of total degree 3 to 6 exists (outside the
family) is open; Wang's theorem excludes degree 2 only.

## Characteristic p (EXP-009)

P3 reduces mod $\ell = 13$ and $\ell = 101$ to explicit non-injective Keller maps over
$\mathbb{F}_\ell$ of total degree $12 < \ell$ (the collision certificate survives reduction,
e.g. mod 13: $(6, 5, 8)$ and $(6, 8, 6)$ both map to $(11, 11, 1)$). Unlike the classical
char-$p$ example $x - x^p$ (degree $= p$), these have degree strictly below the characteristic;
expected from standard reduction arguments, now explicitly certified.

The $q$-tail axis (instance P5) changes the component-degree pattern at fixed fiber degree and
determinant: the family is strictly larger than the seed-only family. Collisions are engineered
exactly: prescribe two rational roots $w_1 \ne w_2$, solve the linear system
$w_i\,\tilde V - \tilde T = k^2 \Phi(w_i)$ for the target invariants, reconstruct both preimages.

## What this answers

- **Why is JC false?** Because the Keller condition, in this equivariant class, is a
  TWO-variable potential identity that never sees properness: the family satisfies it for free
  while fibers have any prescribed degree $\ge 3$.
- **Can it be generalized?** Yes, constructively and in more directions than announced (seed
  degree, scale, section tail). Every negative rational occurs as a determinant.
- **What is essential?** Two independent weight-0 invariants + the potential form + valuation
  conditions at the origin. Exactly the first ingredient fails in dimension 2
  ([04-two-dimensional-frontier.md](04-two-dimensional-frontier.md)).

## The landscape: this mechanism is unique among scanned weight systems (EXP-012)

Generalizing the invariant framework to weights $(1, -1, -m)$: the determinant lemma
$\det JF = x^{\sigma+m}\,D$ and the pairing reductions $J_2 = \pm c_1^{r_a+r_b-1} D$ hold for
all scanned $(m, o)$, and the reduced Jacobian vanishes to order $m-1$ along the section. The
survey outcome:

| $m$ | Class | Result |
|---|---|---|
| 1 | $o = (-1, -1, 1)$ | The JC(2) bridge: the reduced pair is itself a 2D Keller map; 93 scanned instances, all injective. A collision here would refute JC(2). |
| 2 | $o = (-2, -1, 1)$ | THE mechanism (the announced map and our family). |
| 3 | $o = (-2, -2, 1)$ | EMPTY (valuation proof: $D(0,0) = 0$ identically). |
| 3 | $o = (-3, -1, 1)$ | Rigid in scans (60 instances, all injective). |
| 4 | $o = (-3, -2, 1)$, potential form | Does NOT exist: Groebner emptiness certificate (seed degree $\le 5$). |

The design hypothesis (families at every even $m$) was refuted by its own experiment; the
finding is stronger: **within the scanned weighted landscape, the announced counterexample's
weight system is the unique one that collides.** Scope and queued widenings in the EXP-012
verdict (JCB-019).
