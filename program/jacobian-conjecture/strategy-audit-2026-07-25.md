# Jacobian program strategy audit: 2026-07-25

Scope: review every active proposal around the planar $(72,108)$ problem, determine what each
route can prove, correct stale inferences, and rank the next work by information per cost.

## Amendment after EXP-094

The exact source-identity audit resolved the C10/C11/C19/C20 question negatively:
GGV2 Remark 2.32 excludes none of them. C10/C11 have \(A'_0=(1,0)\), not
\((2,1)\); C19/C20 have \(B_1=A_0=(6,15)\), not \((6,18+6k)\).
The earlier strong-candidate classification conflated distinct source objects.
The cheap lookup for these four rows is closed. For the immediate \((72,108)\)
target, the Newton-resolution applicability bridge now ranks ahead of further
frontier enumeration.

## Executive decision

Redirect the immediate campaign. EXP-075's dormant hit was recovered and reproduced during this
audit: the exact four-parameter support at reordered index 2662 is infeasible over both primes.
It proves that no global degree-three polynomial covector exists. Cancel EXP-093, stop EXP-075
after this decisive hit, and do not run EXP-079, EXP-081, or EXP-092 as presently formulated.

The next block is source-first and structural:

1. complete the low-cost [125,150] source frontier;
2. test whether recent Newton-resolution restrictions survive the GGHV reduction;
3. instantiate the already-identified Lee-Li and approximate-root constraints;
4. formulate universal inconsistency as an exact module or finite-chart problem;
5. do not engineer the cancelled cubic solve; reserve matrix-free work for a newly justified
   higher-degree or module computation.

This is a redirection of experiments, not of the target. The target remains simultaneous
all-parameter closure of the reduced GGHV $(72,108)$ branches.

## Corrections to the evidence model

### The finite-covector search is not two-sided

A polynomial left covector with nonzero target pairing is a sufficient inconsistency
certificate. The converse has not been proved. Therefore:

- finding a covector can exclude the certified system;
- not finding one does not establish consistency;
- feasible restricted supports do not move probability toward a counterexample in any
  calibrated or theorem-backed sense;
- there is no validated finite ceiling after EXP-078 withdrew the Krylov argument.

The “counterexample skeleton” and Bayesian language in the 2026-07-24 exploration note is
withdrawn. It may be reconsidered only after a necessity theorem for the certificate class.

### Support sweeps are one-sided

EXP-067 and EXP-072 found infeasible restricted systems, so they can exclude the corresponding
certificate degrees under their exact restriction logic and gates. EXP-073 and the feasible
EXP-075 prefixes are null results only. EXP-075 later found an infeasible coordinate slice, which
is conclusive in the opposite direction because every global covector would restrict to that
slice. Feasible restricted supports cannot prove that the full space has a solution.

### The reduced bracket changes theorem applicability

The GGHV normal form used by the program satisfies
$$
[P,Q]=x^2,
$$
not the Keller equation $[f,g]=1$. Results about Keller maps, Hamiltonian slices, line fibres,
locally nilpotent derivations, and Newton polygons of counterexamples do not automatically apply
to $(P,Q)$. Each route needs an exact transport statement through the GGHV transformations.

### Samples and axes are not simultaneous symbolic coverage

The forced edge is fixed but 51 lower coefficients remain free. Pointwise samples and individual
axis charts are useful controls. They do not prove inconsistency over the full parameter space.
The correct all-parameter object is an ideal, module, or constructible-cover statement over
$\mathbb{Q}[\varepsilon_1,\ldots,\varepsilon_{51}]$.

## EXP-075 recovery and EXP-093 cancellation

The committed artifact `output-run2-2026-07-24.txt` contained an unpropagated result:
support
$$
\{(0,3),(1,0),(3,4),(4,7)\}
$$
was infeasible at blocker-first index 2662 over both configured primes. A targeted rerun on
2026-07-25 reproduced the same result in 12 seconds with the regression gate green.

This is the conclusive direction of support restriction. Any global degree-three polynomial
covector would restrict to a solution on every four-parameter coordinate slice. This slice is
infeasible, so no such global covector exists. This does not imply consistency, a
counterexample, or absence of certificates at higher degree.

EXP-093 proposed solving the full degree-three system. Its target is now proved empty, so the
experiment is cancelled.

## Cancelled EXP-093 scale audit

Let $r=51$ be the number of perturbation parameters and $g=165$ the gauge dimension. A general
certificate through degree $d$ contains one gauge vector for every parameter monomial of degrees
$1,\ldots,d$.

| Truncation | Parameter blocks | Gauge unknowns |
|---|---:|---:|
| degree 1 | $\binom{51}{1}=51$ | $8,415$ |
| through degree 2 | $51+\binom{52}{2}=1,377$ | $227,205$ |
| through degree 3 | $1,377+\binom{53}{3}=24,803$ | $4,092,495$ |

At order four there are $\binom{54}{4}=316,251$ parameter monomials. With 125 output rows, the
homogeneous order-four block alone represents $39,531,375$ scalar conditions before structural
compression. The full system also contains the lower-order equations.

Consequences recorded before the decisive EXP-075 recovery:

- the previous “227k+” estimate is the through-degree-two count;
- a generic sparse matrix materialization may be impractical;
- materializing the system would have been irresponsible without an implicit-operator pilot;
- after the EXP-075 reproduction, no pilot or full solve is warranted.

## Route adjudication

| Route | Decision | What it can prove | Next gate |
|---|---|---|---|
| EXP-084/085/094 frontier source reconciliation | PARTIAL, FOUR CANDIDATES RESOLVED NEGATIVELY | exact classification progress independent of the certificate tower | derive the 16 unprinted \(A'_0\) values only as a separate frontier task |
| Makar-Limanov/Trakhtenberg Newton resolution | PURSUE NOW | potentially eliminates or sharply restricts the forced shape if the conditions transport | prove the $[f,g]=1$ to $[P,Q]=x^2$ applicability bridge |
| Lee-Li inner-polynomial and inner-vertex restrictions | PURSUE NOW | cheap support restrictions or an incompatibility | instantiate every hypothesis on the GGHV transformation |
| GGHV approximate roots and intersection numbers | PURSUE NOW | independent arithmetic constraints and audit of the current polygon assembly | source-complete derivation on the $(8,28),(3,2)$ case |
| Certificate module and finite chart cover | PURSUE, SMALL ANALOG FIRST | a rigorous all-parameter inconsistency proof using one or several localized certificates | define the module, pairing ideal, specialization law, and toy control |
| EXP-093 cubic solve | CANCEL | target ruled out by EXP-075 | preserve the size audit; no implementation |
| Jelonek 2026 component theorem | HOLD AS FRAME | organizes bounded-degree Keller maps into automorphism or generic-counterexample components | identify a component-level object before claiming relevance to the reduced pair |
| EXP-075 quadruple sweep | DONE | reproduced infeasible support excludes global degree-three polynomial covectors | stop at first decisive hit; preserve verdict and artifacts |
| EXP-079 flat connection | RETIRE AS STATED | nothing rigorous until a connection and implication are defined | replace by the certificate-module formulation |
| EXP-081 3D collision projection | RETIRE AS STATED | no typed comparison presently exists | construct an explicit map between the relevant dual spaces |
| EXP-092 LND/line fibres | HOLD | can decide a genuine Keller coordinate if a slice/LND hypothesis is proved | bridge $D_P(Q)=x^2$ to a unit slice or return to an original Keller pair |
| EXP-080 natural `sl2` route | DONE, SCOPED NULL | refutes only the declared canonical grading premise | revisit only with an explicit grading-compatible gauge |

## New structural route: certificate modules and chart covers

Write the reduced linear system as
$$
M(\varepsilon)q=b
$$
over $R=\mathbb{Q}[\varepsilon_1,\ldots,\varepsilon_{51}]$. A global polynomial covector
$c(\varepsilon)$ with
$$
c^T M=0,\qquad c^T b\in\mathbb{Q}^{\times}
$$
is sufficient but may be unnecessarily restrictive.

The more general target is:

1. compute the left-syzygy module of $M$ or a presentation adapted to the grading;
2. form the ideal of pairings $I=\{c^Tb:c^TM=0\}$;
3. test whether localized pairing ideals cover parameter space;
4. certify a finite principal-open cover $D(s_i)$ with
   $1\in\sqrt{(s_1,\ldots,s_k)}$ and a valid localized certificate on each chart;
5. treat specialization carefully, because kernels and syzygies can jump on closed strata.

This subsumes the useful part of the determinant/minor route and the axis-chart experiments.
It also explains why one finite polynomial covector need not be necessary for uniform
inconsistency.

## Source-frontier route

EXP-083/084/085 and the EXP-094 correction give:

- C13 is excluded in the cited GGV text;
- C10/C11 do not match the discarded Heitmann families because their
  \(A'_0=(1,0)\), not \((2,1)\);
- C19/C20 do not match the GGV \(B_0,B_1\) cases because
  \(B_1=A_0=(6,15)\), not \((6,18+6k)\);
- 16 configurations need their unprinted $A'_0$ forcing derived;
- C01/C04 remain open unless an exact source or derivation says otherwise.

The 16-value derivation remains useful for the [125,150] frontier, but it is not
a prerequisite for attacking the separate \((72,108)\) target. No large frontier
computation is justified without those values.

## Modern source leads

### Newton resolution

Makar-Limanov and Trakhtenberg give an algorithm based on integrality and polynomiality
conditions on the Newton resolution of a hypothetical planar counterexample. Their computed
degree list at total degree at most 100 is
$$
\{42,48,50,56,60,63,64,66,70,72,75,80,84,88,90,96,98,99,100\}.
$$
They also give explicit degree-72 leading shapes. The forced reduced polynomial
$P_T=y^8(xy-1)^8+x$ has total degree 24 and leading edge a high power of a primitive form,
which makes the comparison unusually sharp. No contradiction is claimed: their assumptions
concern a reduced component of an actual Keller counterexample, whereas $P_T$ belongs to a
pair with bracket $x^2$.

The first experiment is therefore an applicability audit of the GGHV changes of variables,
including denominators, Newton polygon transformation, and what happens to leading-form
power data.

### Inner vertices and approximate roots

Lee-Li's inner-polynomial restrictions and the GGHV approximate-root/intersection-number
formulas are already in the bibliography but have not been instantiated on the current
51-parameter family. They rank ahead of another certificate sweep because they may remove
coefficients or branches before linear algebra and provide an independent audit of the forced
polygons.

### Parameter-space components

Jelonek's 2026 result states that, at bounded degree, the automorphism locus inside the
Jacobian-one parameter space is Zariski closed and each irreducible component is either an
automorphism component or has generic counterexamples. This is useful medium-term framing for
an original Keller parameter space. It does not directly apply to the reduced
$[P,Q]=x^2$ family.

## Recommended experiment sequence

1. Source audit round: finish EXP-084/085 and the missing table/family identifications.
2. Declare a Newton-resolution applicability experiment with a pass/fail transformation table.
3. Declare a combined Lee-Li/approximate-root applicability experiment.
4. Declare a small certificate-module/chart-cover analog, with known consistent and inconsistent
   controls.
5. Re-rank. The live choices are a chart-cover/module computation, a source-derived restriction,
   or a newly justified higher-degree structural probe. The cubic solve is not a choice.

## Claims that remain unchanged

- JC(2) is open.
- The program has not excluded $(72,108)$.
- The forced-edge families have exact sampled and axis-symbolic certificates within their stated
  scopes.
- EXP-067 and EXP-072 are valid within their declared full/restricted systems and arithmetic
  gates.
- EXP-075 now excludes degree-three polynomial covectors in the declared class.
- EXP-078 and EXP-080 remain valuable scoped nulls.
- Papers and wiki material must not acquire a floor-raise statement until simultaneous symbolic
  coverage and branch assembly are independently verified.

## Exploration moment

The new viewpoint this round is that “one global polynomial covector” is only one sufficient
certificate shape. A finite constructible cover by localized certificates may prove uniform
inconsistency even when no single global polynomial covector terminates. This replaces the
undefined flat-connection analogy with a precise commutative-algebra target and connects the
existing determinant, axis, and ladder experiments in one framework.
