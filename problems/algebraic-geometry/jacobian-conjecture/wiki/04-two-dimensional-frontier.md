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

## The JC(2) machine and the first full closures (EXP-017/019/020)

The Keller condition is bilinear in the coefficient vectors, so in the affine gauge it is
LINEAR in one side given the other. The machine per degree pair: eliminate the large side
(a Groebner elimination gives the consistency ideal in the small side, whose shape the
leading-form theory predicts in advance), parametrize the consistency variety, complete
linearly, and either invert explicitly or fiber-test.

Results so far: the $(2,3)$ consistency ideal is the single equation
$(4A_0A_2 - A_1^2)^2 = 0$ (the top form of $P$ must be a perfect square, exactly the
leading-form degeneracy); the $(2,4)$ elimination returns the SAME ideal (the locus is
completion-degree independent); and on the parametrized variety $P = x + (\alpha x + \beta y)^2$
the complete $(2,3)$ family is the single branch
$Q = y - \alpha^3 x^2/\beta - 2\alpha^2 xy - \alpha\beta y^2$, with the explicit polynomial
inverse verified by exact composition ($\beta = 0$ forces the affine case). **Every normalized
$(2,3)$ Keller map is invertible, constructively.** Exhaustive certificates also cover
$(2,2)$, $(2,4)$, $(2,5)$, $(3,3)$, $(3,4)$ windows. Classical in content; ours in mechanical
form, and the machine scales.

## The uniform theorem, the descent, and the primitive stratum (EXP-021/022/023)

The column closes uniformly. In shear coordinates $(u_1, u_2) = (\ell, x)$ with
$\ell = \alpha x + \beta y$, the Keller condition for $P = x + \ell^2$ becomes the linear
first-order PDE $2u_1 Q_{u_2} - Q_{u_1} = c$, whose characteristic invariant is exactly $P$.
The complete solution space is $Q = \ell/\beta + H(P)$ with $H$ an arbitrary polynomial, and
one closed formula inverts everything:
$$\ell = \beta\,(v - H(u)), \qquad x = u - \ell^2, \qquad y = (\ell - \alpha x)/\beta.$$
**Uniform theorem [MV at the certified degrees]: every planar Keller map with
$\min(\deg P, \deg Q) \le 2$ is invertible by that formula** (sufficiency generic; completeness
as exact kernel dimensions $\lfloor n/2 \rfloor + 1$ for $n = 3..6$; the inverse verified by
exact composition). EXP-022 extended the closure to ANY section $f$: the whole quasi-triangular
class $P \sim x + f(\ell)$ closes at every degree, and the $(3,3)$ cube case FORCES the
quasi-triangular alignment at the radical level ($A_0^2$ and $A_1^6$ lie in the consistency
ideal once the cube coefficient is inverted).

The classical degree descent is now running code: while the tops are power-proportional,
subtract $c\,P^k$ from $Q$; finish with the closed inverse; replay the elementary steps on the
value side. It explicitly inverted the entire deterministic library (0 to 4 steps per map).
Its failure signature, a PRIMITIVE pair (tops sharing a base form $h$ with $\deg h \ge 2$ and
no power relationship), is exactly the residual open core of JC(2).

First contact with that core (EXP-023): at the smallest primitive bidegrees $(4,6)$, the
completion window is EMPTY on a structured sampled slice. For
$P = x + P_2 + P_3 + a\,h^2$ ($h = xy$ and the rank sweep $x^2 + \gamma y^2$, $a \ne 0$,
25 samples), NO Keller partner of degree $\le 6$ exists at all: the complete linear system is
inconsistent every time, and one descent step extends the exclusion to degree $\le 8$.
Positive controls prove the scan is not vacuous (the harness finds the quasi-triangular
completions of $x + (x+y)^4$; the detector fires on the genuine degree-6 realization above
$x + (x+y)^2$). Literature context, now verified from primary sources (JCB-029 closed):
Magnus proved gcd of the degrees equal 1 implies automorphism (A. Magnus, Volume preserving
transformations in several complex variables, Proc. Amer. Math. Soc. 5 (1954), 256-266), and
Appelgate-Onishi (The Jacobian conjecture in two variables, J. Pure Appl. Algebra 37 (1985),
215-227) with Nagata extended this to gcd equal a prime; the refined coverage is gcd in
{1, 8}, primes, and twice-primes. The plane conjecture is classically EQUIVALENT to the
divisibility statement (deg P divides deg Q or conversely), which is exactly the primitive
stratum framing of our machine. Our gcd-2 emptiness therefore independently replicates
classically covered territory with a different instrument (a validation, not a new theorem);
the genuinely open gcd values start at 9 and 12, i.e. bidegrees like $(18, 27)$ and
$(24, 36)$. That composite-gcd ladder is JCB-028's frontier.
