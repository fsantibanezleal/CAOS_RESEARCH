# Novel approaches to (72,108) and JC(2) - deep exploration (2026-07-24)

Written on the Opus tier at Felipe's request to rethink the ATTACK, not to sweep.
Grounded on two established facts of this program:
- The annihilation lemma (EXP-036): J(m, P^k) = -k L(P^{k-1} m), L the FULL
  logarithmic-derivative operator; every ladder source is an L-image.
- The dual identity (EXP-068/074): the cokernel covector Lambda0 is a true
  left-kernel vector (Lambda0 M0 = 0); it annihilates every bracket image, so
  ladder solvability is automatic at every order and obstructions are purely
  top-order.

Everything below is labeled [HYPOTHESIS], [REFRAME], or [DIRECTION]. None is a
claim; each names its cheapest first experiment.

---

## 0. [REFRAME] The campaign is TWO-SIDED: exclusion and counterexample are one computation

The certificate we hunt is a covector that closes the reduced (72,108) Keller
system. Read the tower honestly:

- A covector appears at some finite degree  =>  the reduced system is certified
  INCONSISTENT  =>  (72,108) EXCLUDED  =>  floor rises  =>  evidence FOR JC(2).
- NO covector exists at ANY degree  =>  the reduced Keller system is (as far as
  this certificate sees) CONSISTENT  =>  a potential Keller pair on the reduced
  polygon  =>  the first step of a COUNTEREXAMPLE, i.e. evidence AGAINST JC(2).

So every "degree d closed, no covector" result (EXP-067 d=1, EXP-072 d=2) and
every "open, all supports feasible" result (EXP-071/073/075) is not merely one
more exclusion attempt: it is a Bayesian increment on WHICH WAY (72,108) goes.
The current reading (no covector at 1-2; open through triples at 3) is weak but
non-zero evidence toward CONSISTENCY. This is why the tower must be pushed to a
decision, not abandoned. It also means the same machinery, run to the end,
either raises the floor or hands us a counterexample skeleton to lift.

Caveat: the covector is SUFFICIENT for exclusion, not proven necessary; absence
is evidence, not proof, of consistency. Direction 3 below removes this caveat.

---

## 1. [DIRECTION, highest value] The truncation tower has a COMPUTABLE FINITE CEILING

The open-ended "degree by degree" sweep hides that the covector, IF it exists,
exists at BOUNDED degree. In EXP-064's framing the finite covector exists iff
the operators A_i are jointly nilpotent on the Krylov closure V_inf of Lambda0;
joint nilpotency on a finite-dimensional space (here dim V_inf = 122, ambient
kernel dim 165) has nilpotency index <= dim. Hence:

  THERE IS AN EXPLICIT N (<= ~122, sharpenable) such that a finite covector
  exists  <=>  it exists at eps-degree <= N.

Consequence: checking the support tiers up to the degree implied by N DECIDES
(72,108) either way. If we exhaust to N with everything feasible, we have PROVEN
no covector exists -> (by section 0) consistency -> the counterexample hunt
begins with certainty, not a hunch. This converts the sweep from an unbounded
process into a FINITE decision procedure.

First experiment [EXP-078, cheap]: compute the true ceiling N from the module
structure (the Krylov dimension already in hand from EXP-064; refine the bound
using the sigma-independent direct system so it is not pinned-sigma-specific).
Deliverable: a number N and the statement "checking through eps-degree N decides
(72,108)". Even N ~ 20-100 turns the campaign finite.

Refinement: an EFFECTIVE NULLSTELLENSATZ bound (Kollar: deg <= (max deg)^n) on
the reduced ideal gives an independent, possibly smaller ceiling and, if 1 is in
the ideal, a direct inconsistency certificate bypassing covectors entirely.
Worth a parallel computation.

---

## 2. [HYPOTHESIS] The annihilation lemma is a FLAT CONNECTION; termination is a REGULARITY question

J(m, P^k) = -k L(P^{k-1} m) says the Jacobian-bracket-against-P-powers is an
L-total-derivative: the P^k are horizontal for the operator L up to its image.
Package L as a connection nabla on the module of tails. Then:
- all-orders solvability (kernel = constants, EXP-057/058) is H^0(nabla);
- the obstruction to a FINITE covector is a class in H^1(nabla);
- the corrector ladder Lambda_alpha = (words in A_i) Lambda_0 is the parallel
  transport, and it TERMINATES iff nabla is regular-singular at the class where
  the obstruction localizes (the constant's class in the staircase transport).

If nabla is regular singular: finite-dim cohomology, the ladder terminates, a
covector exists -> EXCLUSION, at bounded degree (this would also PROVE the
ceiling of section 1 structurally). If nabla is IRREGULAR: the ladder need not
terminate, and the empirical "obstruction moves with degree" is the STOKES
PHENOMENON of an irregular connection -> consistency -> counterexample side.

So the singularity TYPE of nabla decides JC(2) at (72,108) in one structural
stroke. This is the deepest lead: it would replace the sweep with a theorem.

First experiment [EXP-079]: write L in the window basis as an explicit matrix
of the graded pieces; compute its singularity type at the constant's class
(order of pole / formal type). Regular vs irregular is a finite exact
computation on the connection matrix.

---

## 3. [HYPOTHESIS] sl2 / weight-module structure turns "which degree closes" into a decomposition

The (v, 1-u) grading is a torus weight h. The T_i shift weight by fixed amounts;
the annihilation covector is a weight-lowest vector. If a raising e and lowering
f close with h into sl2 (or a larger W-algebra given the staircase), the
corrector ladder is a weight module and:
- it terminates  <=>  the module is finite-dimensional (bounded weight);
- the obstruction  =  a PRIMITIVE (highest-weight) vector not killed by e.

This makes "the obstruction moves with degree" a statement about the sl2 (or
Virasoro/W) decomposition of the ladder module, a clean representation-theoretic
invariant. It also predicts the LOCATIONS of obstructions (primitive vectors)
rather than finding them by sweep -> could replace the quadruple+ sweeps.

First experiment [EXP-080, cheap]: test whether the graded operators close into
sl2: compute [e, f] on the window basis and check it equals h (the weight
operator) up to scalars. A yes reorganizes the entire truncation story.

---

## 4. [DIRECTION] The 3D->2D obstruction transfer, made POSITIVE

We proved the Alpoge mechanism does not transplant to 2D (rigidity + uniqueness).
Turn the negative into the covector: the 3D collision uses a nilpotent absorbed
by the third variable; in 2D that nilpotent has nowhere to go, and its DUAL is
plausibly exactly Lambda0 (the covector that kills all bracket images). If the
2D obstruction covector IS the shadow of the 3D collision, we get a conceptual
origin for Lambda0 and a transfer principle for OTHER cases (each 3D
counterexample family projecting to a 2D exclusion covector).

First experiment [EXP-081]: compute the 3D collision covector (from the
validated dim-3 counterexample), project along the mechanism's variable, and
compare to Lambda0 on the (72,108) reduced system.

---

## 5. [DIRECTION, long shot for an ALL-DEGREES theorem] Berkovich / tropical at infinity

The 1884 obstacle is ramification at infinity; the Newton-polygon machinery is
already its tropicalization. A Berkovich-analytic reformulation of the Keller
condition at the place at infinity (the reduction graph of the boundary) is a
COMPACT object, so an exclusion proved there would be UNIFORM in degree - the
kind of statement that could close JC(2) rather than one case. Speculative;
opens as a literature dossier (Baker-Payne-Rabinoff tropicalization of curves;
the semistable reduction of the boundary of a Keller pair).

---

## Execution order (main session, interleaved with the delegated sweep/C13)

1. EXP-078 (the ceiling) FIRST: cheap, and it reframes the entire campaign as a
   finite decision - the single highest information-per-cost item.
2. EXP-080 (sl2 closure test): cheap; a yes reorganizes everything.
3. EXP-079 (connection singularity type): the deep lead; medium cost.
4. EXP-081 (3D->2D covector): connects to the published cascade.
5. Section 5 as a parallel dossier.

Each becomes a declared hypothesis.md before any run. Results that close a block
trigger the Paper B chapter + Zenodo per methodology/09.
