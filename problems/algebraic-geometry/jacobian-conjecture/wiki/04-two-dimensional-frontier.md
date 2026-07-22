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

Novelty status (FULL adversarial pass, 2026-07-22, context dossier): NOT FOUND in the
literature, and the statement has genuine content: the C*-equivariant analog FAILS on
Q-acyclic pseudo-planes (Dubouloz-Palka, Adv. Math. 339 (2018)), and the known equivariant
positive result covers only small FINITE groups (Miyanishi, Transform. Groups 28 (2023)).
The positive-weight case is folklore-trivial; the mixed-weight case is ours as far as the
pass could determine. Folklore risk stays recorded; the manuscript phrasing awaits Felipe's
validation.

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
$x + (x+y)^2$). Literature context, RECALIBRATED against the full audited pass (2026-07-22 dossier,
correcting the earlier reading): for a counterexample pair, B = gcd of the degrees
satisfies the FULL interval coverage B <= 8 (Magnus, Math. Scand. 3 (1955) for gcd 1;
Nakai-Baba for <= 2; Appelgate-Onishi, J. Pure Appl. Algebra 37 (1985), with Nagata for
<= 8 or prime), B != p (Abhyankar 2008), B >= 16 (Heitmann, J. Pure Appl. Algebra 64
(1990)), and B != 2p with B = 16 or B > 20 (Guccione-Guccione-Valqui, J. Algebra 471
(2017); Zoladek's claimed B > 33 has a documented gap and is never cited here). The plane
conjecture is classically EQUIVALENT to the divisibility statement, which is exactly the
primitive-stratum framing of our machine. Consequently our certificates at gcd 2, 9, 12
and 18 are ALL replications inside the verified floor (kept as independent machine
validations); the live frontier is the GGV B = 16 normal form and, below max degree 125,
the single surviving pair (72, 108). First contact is made (EXP-026): the $(18, \le 27)$ completion window on the
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

Derived statement, since subsumed: $P = x + a h^2$ is never a Keller component at any
partner degree; this is now a corollary of the weight-class theorem below. The similarity
theorem's exact hypotheses are verified (van den Essen's book, Thm 10.2.1 via Lee-Li:
N^0 polygons including the origin, BOTH degrees > 1, origin-centered, ratio deg P : deg Q).
The audited degree floor: Moh 1983 discards max degree <= 100 (complete published detail
only for the largest case, 64), and GGHV (arXiv:2204.14178, Thm 2.1) prove any
counterexample has max degree >= 125 OR degrees exactly (72, 108), the lone pair left open
for compute reasons.

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

## Theorem 4: the vertex dichotomy (EXP-033)

The two boundary directions of the edge fan fall by one-line class arguments: for
$P = x\,\varphi(y)$ the constant's class equation is $\varphi(y) h'(y) = 1$, which no
polynomial satisfies once $\deg \varphi \ge 1$ (kernels are $(x\varphi)^s$; certificate
$-c_1^6$ for $x(1 + c_1 y)$); for $P = x\,\varphi(x)$, $J(P, Q) = (x\varphi)'(x)\,Q_y$
forces a non-polynomial $Q_y$.

**Theorem 4 (vertex dichotomy).** If the monomial $x$ is a VERTEX of the Newton polygon of
a Keller component $P$ (linear part $x$), then $P = x + f(y)$: every edge at the vertex is
an excluded $x$-divisible shape (Theorem 3 and the axis cases) except segments to pure-$y$
vertices $(0, d)$, which contain no interior lattice points. Machine-verified on all three
sides: vertex-$x$ samples with mixed monomials are all inconsistent; triangular samples are
consistent (they are components); and the escape route is real: $x + (x+y)^2$ and
$x + (x+2y)^3$, where $x$ is swallowed inside the polygon, are components.

The recorded strategy (JCB-036): non-triangular components must swallow $x$; a linear gauge
rotation puts the dominating direction on a coordinate and the vertex analysis re-applies:
an induction whose closure on the triangular family would be JC(2). The open steps
(rotation normal form, behavior of the excluded shapes under rotation, ties) are the
program's standing target, stated as strategy, not as a claim.

## The corner is diagonal; the core is the staircase (EXP-035/036)

Two results closed this stage. First, the mixed corner, long suspected to be the hard
object, is clean: for $B = x^i y^j$ ($i, j \ge 1$),
$$J(B^p,\; x^a y^b) = p\,(ib - ja)\; x^{ip+a-1} y^{jp+b-1},$$
a DIAGONAL operator whose eigenvalue is the determinant of the exponent pair against the
corner direction and whose kernel is exactly the powers of $B$. A pure corner can never
carry the Keller constant (the output exponents never both vanish). The constant must
therefore be manufactured along the STAIRCASE of Newton vertices running from the swallowed
linear vertex $(1,0)$ up to the top corner, and that transport, the classical Moh staircase,
is the program's residual open core (JCB-038). Thirty monomial-corner samples were scanned:
every completion window empty.

Second, the annihilation lemma is closed in general, and with it the last derived gap in
Theorems 2, 3 and 4, which are now UNCONDITIONAL. The route required a refutation first: the
declared argument used $L_{top}$ and failed both machine tests. The operator that the
certificate covector annihilates is the FULL $L = J(P, \cdot)$, and the sources satisfy
$$J(m, P^k) = -k\,L\!\left(P^{k-1} m\right),$$
so every source is an image with an explicit preimage, and a left-null covector kills the
whole image at once. The finite-window subtlety is exactly a truncation bookkeeping: the
pairing vanishes precisely when the preimage fits the window, which retrodicts the artifact
values recorded in EXP-031 number for number.

## The staircase transport and the fifth exclusion (EXP-037/042/044)

The open core got its instrument and its first theorem. Under the x-edge grading
$(v, 1-u)$, the completion window is BLOCK-TRIANGULAR: every matrix entry sits at a
P-class offset, the minimal class is the diagonal, and classwise elimination (solve the
banded diagonal, inject kernel parameters, emit cokernel obstructions) reproduces every
monolithic verdict, with the obstruction always localizing at the CONSTANT'S class
(EXP-037; the declared vertex-hand-off guess was refuted by that cleaner fact).

**Theorem 5 (window form, sound at every parameter; EXP-042).** For the minimal swallowed
family $P = x + a\,x^u y^v + b\,x^d$ across the tested grid, cleared certificate covectors
(polynomial entries, identity $c^T M = 0$ verified) pair to MONOMIALS such as
$-13860\,a^7$: the window is empty for every parameter value with $a \ne 0$.

**Toward all degrees (EXP-044).** The normalized constant-class equation is IDENTICALLY
$-2a$ at every window tested (N up to 13); the cleared pairings follow the law
$-c_N a^N$ with positive ratios (the odd primes $2N-3$ pattern); and the certificates form
a coherent TOWER: each window's covector restricts to the previous one on all rows with a
single common ratio. Window growth adds unknowns only upstream of the constant's row.
THE TOWER LEMMA IS NOW PROVED (EXP-046) for primitive tops and the d >= u+v regimes:
old columns vanish on new rows; the new block is the top-form action with kernel spanned
by top-form powers; each resonance reduces in-window modulo ker L (the key identity
kappa = lambda(P - low)^k); and the extension was realized across an active resonance
with the pairing preserved. THEOREM 5 IS THEREFORE UNCONDITIONAL on that scope: the
first all-degree exclusion of an above-weight staircase perturbation. The proper-power
case (e.g. u = v = 2) has its odd resonances measured zero (the (xy)^5 pairing at window
9); the derivation of that kill is the lemma's one remaining case.

Two instrument facts complete the stage: the matched-pair law (EXP-038: the pair adds
efficiency, roughly halving window unknowns, but no obstruction depth) and the
$x^m$-anchored edge operator (EXP-043),
$$J\!\left(x^m \varphi(z),\, x^{\alpha} y^{\beta}\right) = x^{m+\alpha-1} y^{\beta-1}
\left[\beta m\,\varphi + (\beta k - \alpha l)\, z\varphi'\right], \qquad z = x^k y^l,$$
of which Theorem 3's operator is the case $m = 1$.

## The frontier engaged (EXP-043/045)

The GGV B = 16 normal form is now inside the program's reach. Its leading form
$R_0 = x(xy^4 - \lambda_0)^3$ is $(4,-1)$-homogeneous with collinear x-anchored support;
for standard pairs ($m \ge 2$) the $R_0^m$ edge CANNOT produce the Keller constant (the
$x^{m-1}$-divisibility one-liner makes the pure form trivially excluded, and the operator
formula shows no monomial reaches the constant): the B = 16 case is formally a staircase
transport problem. Theorem 4 excludes the pure $m = 1$ shape outright. Mid-scale
certificates now exist at degree 32 ($P = x + R_0(1)^2$: windows 12, 16, 20 all empty),
and the imported similarity filter (partner supported in the scaled polygon; verified to
keep every true partner on library pairs) cuts window unknowns by a factor of ~19: the
$(48, 64)$ full-window system drops from 2142 to 111 unknowns, and the classwise blocks
are at most 13. The validation sweep RAN (EXP-047): three degree-48 F1-flavor samples have empty
filtered windows at N = 64 in 2.4-3.6 seconds each, excluding all partners of degree
<= 64 per sample; the open territory (max degree > 150, and (72, 108)) is next at
comparable cost.

## The witness, and where everything is written

The explicit dimension-48 gradient witness (HC(48) false with an exact $\mathbb{Q}(i)$
collision; the failing Hessian-nilpotent quartic $P_\star$) is EXP-041 and lives, with the
full consequence cascade, in the cascade companion manuscript. The planar results of this
page are the planar-program manuscript (manuscript-planar/); the 3D aftermath is the
foundational manuscript. The routes map (near-term: the tower lemma; the B = 16 sweep) is
program/jacobian-conjecture/routes-2026-07-22.md.

## The half-plane tower: proper-power tops close on the staircase stratum (EXP-051)

The last structural gap of the tower program closed on its natural stratum: for any
P = x + R whose total-degree top corner is the y-most support point (all swallowed
staircases), the y-heavy half-plane subsystem H = {i <= j} carries the whole
obstruction: T-power resonances reduce by the universal identity, non-T-power kernel
elements have x-heavy sources with EMPTY H-support, and columns leaving H vanish from
the subsystem entirely. ONE H-certificate at one window therefore excludes P at ALL
partner degrees, proper-power tops included. Machine record: symbolic H-certificates at
every tested window at (2,2,2); and the frontier payoff: the degree-32 B = 16-flavor
sample and the degree-72 corner-(16,56) sample are now excluded at all partner degrees
(pairings -256 and -32). Together, Theorems 5-6 and the half-plane lemma cover the
entire swallowed-staircase stratum with y-most top corners from single window solves.

## The (72, 108) attack: the reduced system and the corrector ladder (EXP-050..055)

The lone open degree pair below 125 reduces (GGHV Prop 4.3, transcription verified
against the LaTeX sources) to pairs with [P, Q] = x^2 on SMALL polygons: N(P) with
corners (0,0), (1,0), (8,14), (8,16), (0,8) (61 lattice points) and N(Q) with corners
(0,0), (2,1), (12,21), (12,24), (0,12) (125 lattice points). The machine's state:
sampled shapes at the original degrees and on the reduced polygons are all
partner-free (seconds per certificate; EXP-050/052); on the forced-top-edge stratum
(y^8 (xy - t)^8 symbolic) every cleared certificate pairs to the CONSTANT 576, with a
five-row support (EXP-053); rigid universality of that covector was REFUTED (51
entering lower combinations, EXP-054), pointing to the perturbative construction; its
base is sound and FIRST-ORDER UNIVERSALITY IS PROVED (26/26 correctors with the 576
pairing pinned, localized supports; EXP-055), with the corrector ladder continuing at
order 2 (EXP-056, in flight). Termination at any finite order yields the explicit
universal covector and closes the reduced stratum; the remaining assembly is the
reduction's other forcing branches, after which the verified JC(2) floor rises from
108 to 125.
