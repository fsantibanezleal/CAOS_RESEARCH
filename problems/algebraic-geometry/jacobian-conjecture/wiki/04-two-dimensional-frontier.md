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

Novelty status (bounded literature pass, 2026-07-21, recorded in EXP-026): two targeted
searches found adjacent work (Newton-polygon shape constraints on minimal counterexamples;
quasi-homogeneous sufficient conditions for the REAL Jacobian conjecture) but no statement of
this theorem. It may be folklore among specialists via Newton-polygon arguments; the full
weight-generality and the machine-certified proof are, to our knowledge, ours. A full-text
literature pass stays queued (JCB-031) before the manuscript presents rigidity as
unqualifiedly new.

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
$(24, 36)$. First contact is made (EXP-026): the $(18, \le 27)$ completion window on the
pure slice $P = x + a\,(x^4 y^5)^2$ is EMPTY for every $a \ne 0$ (certificate pairing
$-144\,a^2$), with the same emptiness across three structurally different degree-9 bases and
a gcd-12 reach probe at $(24, \le 36)$. Honest framing: these bidegrees sit inside Moh's
degree-100 verified range, so the new content is the explicit, per-pair machine certificate
(Moh's verification is not constructive per pair); the beyond-Moh rungs are the standing
target (JCB-030).

## The polygon strategy: from windows to all degrees (EXP-028)

The window certificates kept producing exactly ONE obstruction pairing, from 25 to 700
completion unknowns. EXP-028 identified why: the certificate vector's support lies exactly on
the ray parallel to $P$'s Newton-edge direction, so each certificate is a weighted EDGE
RESIDUE, the machine shadow of the classical polygon calculus. Abhyankar's similarity theorem
(early 1970s; the Newton polygons of a Jacobian pair with both degrees $> 1$ are similar
triangles with ratio $\deg f : \deg g$) gives a lattice sieve: for $P = x + a h^2$
($h = x^p y^q$, $p \ne q$) the admissible partner degrees are exactly the multiples of
$\deg P$, machine-enumerated. The decisive test: the $(18, \le 36)$ window CONTAINS the
first admissible rung $n = 36$ and is empty anyway, certified for every $a \ne 0$ (pairing
gcd $-576\,a^3$): the divisible rungs die by edge descent into previously emptied windows.

Derived statement [D, conditional]: $P = x + a h^2$ is NEVER a Keller component at ANY
partner degree. It hardens to a theorem once the similarity theorem's exact hypotheses are
read from the primary text (JCB-031); the windows through degree 36 are its unconditional
machine-verified shadow. The successor instrument (JCB-032) is the edge-residue functional in
closed form; with it, rungs beyond the current verified floor (Moh 1983 to degree 100;
raised to 108 by arXiv:2204.14178), e.g. gcd 45 at bidegrees $(90, 135)$, become reachable,
where a certified exclusion would be a statement nobody has verified in any form.

## The weight-class theorem (EXP-029): monomial slices fall at all degrees

**Theorem (unconditional).** For $u \ge 2$, $v \ge 1$, $a \ne 0$, the polynomial
$P = x + a\,x^u y^v$ is never a Keller component: no polynomial $Q$ of any degree satisfies
$J(P, Q) = \text{const} \ne 0$.

Proof sketch (elementary; every step machine-verified on grids). Under the weights
$(v,\, 1-u)$, $P$ is weighted-homogeneous, so $J(P, \cdot)$ shifts weight by a constant and
the Keller equation decouples by weight class. The constant $1$ is reachable only from the
class of $y$, spanned by the single ray $g_s = x^{ks} y^{ms+1}$
($k = (u-1)/d$, $m = v/d$, $d = \gcd(u-1, v)$), on which the operator is banded:
$L(g_s) = (ms+1)\,e_s + a B_s\,e_{s+d}$ with $B_s$ a positive integer. The first row forces
the chain nonzero, the last row demands it vanish: contradiction at every truncation, and
every polynomial $Q$ truncates.

This is the closed form of every pure-slice window certificate the program produced (all
seven measured pairings are reproduced by the chain product), it certifies beyond the
verified floor at negligible cost (degree $135 > 108$: checked to partner degrees
$\sim 1000$), and it retires the pure-slice window program. Honesty: the proof is
elementary once seen (folklore risk recorded); we have not found it stated; it was found by
the machine's certificate anatomy. Scope: the theorem needs the perturbation to be ONE
monomial; non-monomial slices have genuine multi-edge polygons and are the next target
(JCB-033: the multi-edge calculus, aiming at upper-triangularity of the edge filtration).

## Theorem 2: lower-weight perturbations never rescue (EXP-030/031)

**Theorem 2 (machine-shadowed; one [D] step).** Let $u \ge 2$, $v \ge 1$, $a \ne 0$, and
let $R$ be any polynomial (monomials of degree $\ge 2$) whose every monomial has
$(v, 1-u)$-weight strictly below $v$. Then $P = x + a\,x^u y^v + R$ is never a Keller
component, at any partner degree.

The proof went through a public refutation: the naive step (injectivity of
$L_{top} = J(x + a x^u y^v, \cdot)$ on every weight class) is FALSE: on the classes of
weight $kv$ the kernel is exactly $\langle P_{top}^k \rangle$. The repair: absorb the
kernel components of $Q$ as $H(P_{top})$; the perturbation then injects the sources
$J(R, P_{top}^k)$ into the constant's equation; the ANNIHILATION LEMMA (machine-verified at
adequate windows; in general it reduces to $k = 1$ via the exact identity
$J(m, P_{top}^k) = -k P_{top}^{k-1} J(P_{top}, m)$, the closed-form step still labeled [D])
kills every such source; the constant's equation reduces to the pure chain of the
weight-class theorem, contradicted at every truncation. Danger-weight tails, the exact
monomials that feed the sources, are certified harmless over $\mathbb{Q}(a, b, c)$: the
pairing gcds stay pure $a$-powers. The quasi-triangular components (which DO exist) violate
the hypothesis (x-power or linear-base tops): the theorem is silent exactly where it must
be. The next frontier is perturbations of weight $\ge v$, where the top edge itself
deforms.

## Theorem 3: every x-anchored edge falls (EXP-032)

**Theorem 3.** Let $z = x^k y^m$ ($k, m \ge 1$) and $E = x\,\varphi(z)$ with
$\deg \varphi = g \ge 1$. Then $E$ is never the leading form of a Keller component, and
$P = E + R$ (any lower-weight tail $R$) is never a Keller component, at any degree.

The mechanism collapsed to one univariate line: on the $y$-class ray the operator is
MULTIPLICATION, $J(E, g_s) = [(ms+1)\varphi + k z \varphi'] z^s$ (machine-verified with
symbolic coefficients), so the class equation is
$m z \varphi f' + (\varphi + k z \varphi') f = 1$ for a polynomial $f$; its top
coefficient at degree $D + g$ is $(mD + kg + 1)\varphi_g c_D$, all factors nonzero:
induction kills $f$. Full windows confirm the whole edge family empty, including
perfect-square and perfect-cube $\varphi$ (factorization does not rescue); the
$\mathbb{Q}(a,b)$ certificate for the binomial edge is $60 a^3$, $b$-free; kernels are the
powers $E^j$; lower tails never rescue; the quasi-triangular control stays consistent.

Consequence, and the program's sharpest frame yet: NO Keller component of $\C^2$ has a
Newton top edge anchored at the linear vertex $x$ with interior direction. Components must
have $y$-anchored (quasi-triangular type) tops, and the two-variable Jacobian conjecture is
exactly the statement that nothing else lives there. Classifying the $y$-anchored
completions is the queued endgame frame (JCB-035); the single remaining derived gap in the
with-tails statements is the annihilation lemma in closed form (JCB-033), shared by
Theorems 2 and 3.
