# Riemann hypothesis: research lines after the proof of 2026-11-20, across fields, and a first attempt at the extension of its mechanism

Date: 2026-11-22. Written by the coordinating session on Felipe's orders of 2026-11-22 (verbatim): "was you even
exploring the paths and concepts that allowed to find a demonstration ?"; "I asked to explore the problem , you
expired what you wanted instead . tou don't explored all the paths , when I explicit required to explore new paths,
nee approaches, to take in consideration the most related fields or event nor commonly related fields or methods .
tags is what is asked in any problems you are working at that repo"; "define a real path, exploring new fields, and
try to solve the most promising one . don't stop". Binding rules applied: methodology 10 (multi-factorial lenses) and
11 (exploration cadence). Marks: [P] read on a primary source; [Z] read in R. Zhang's preliminary note (2026-11-21,
partly AI-written by its author's account, not checked against the Lean code; data root
`caos-research/millennium-review-2026-11-22/rh-anatomy/`); [K] standard; [D] derived here; [Q] an open question.

## 0. Self-questioning (methodology 11, item 2)

The programme's spine since 2026-07 was the proportion of zeros on the line and of simple zeros (Levinson,
mollifiers, pair correlation, short windows). That spine counts zeros on the line; it cannot place all of them there.
The tool review of 2026-10-08 listed only analytic tools and recorded the reformulations as "surveyed, none run". The
fields the proof came from (function-field methods, theta correspondence, automorphic periods, Arakelov geometry,
Galois deformation, Iwasawa theory, additive combinatorics) were never opened. After the release the session again
chose a target inside the old toolbox (T1, simple zeros in short windows). T1 stays a valid line (line B of the plan),
but it is not the answer to an order to explore.

## 1. Anatomy of the proof (lens 2), from [Z] with the formal statements [P]

| Step | Field | What it does | Programme's reading |
|---|---|---|---|
| 1. Zero detection on windows | analytic number theory (Landau, Guinand, Turan, Weil) | a one-sided bound G(x) << x^(1/2 + eps) on intervals [Y, Y^(3/2)] for arbitrarily large Y excludes zeros right of 1/2 | proved on paper and reviewed (`context/2026-11-21-windowed-landau-endgame.md`) |
| 2. Positive combination over the powers of a character | harmonic analysis on finite abelian groups | G_chi = G_1 + (1/(3r + 1)) sum of Re G_psi over the characters inducing the powers of chi; residues at a shared zero add up with positive weights | [Z, (1.1)] |
| 3. Frobenius conditions as character sums | algebraic number theory (Dirichlet, Chebotarev in abelian form) | the places of an abelian CM field E are labelled by Gal(E/Q); a prime power p^j contributes at place g when g - j Frob_p lies in the inertia group; orthogonality turns the count into Dirichlet characters, with a main term M(a, w) from log derivatives at 1 only | [Z, Prop. 3.1] |
| 4. Product formula | arithmetic | a nonzero algebraic integer highly divisible at finite places cannot be small at all archimedean places | [Z, 1.3] |
| 5. Automorphic periods and theta lifts | automorphic forms, representation theory | Bessel periods (Gan-Gross-Prasad) on unitary groups over E+; m successive theta lifts (Weil, Howe, Kudla's seesaw) raise the divisibility; Rallis and Gan-Qiu-Takeda give the norms; Siegel-Weil and mass formulas the dimensions; CM periods (Chowla-Selberg, Anderson) normalize | [Z, 4.1, 4.5] |
| 6. Arakelov slopes | Arakelov geometry, geometry of numbers | lattices of algebraic automorphic forms; Harder-Narasimhan-Stuhler-Grayson filtration; Bost's slope inequality; arithmetic Hilbert-Samuel (Gillet-Soule, S. Zhang); integral p-adic Hodge theory (Fargues; Anschutz-Le Bras) | [Z, 4.2 to 4.4] |
| 7. Denominators | Galois cohomology, deformation theory, Iwasawa theory | Hecke projections can create denominators; their size is bounded by congruences, Galois representations (Clozel-Harris-Labesse, Shin, Chenevier-Harris), Tate-Poitou duality, Taylor-Wiles patching, Kato's Euler system, Ferrero-Washington's vanishing of mu for abelian fields | [Z, 5] |
| 8. Place selection | additive combinatorics | Frobenius acts on the places of E by translation in Gal(E/Q); a short segment of a Frobenius orbit is an arithmetic progression; a Behrend-type set without three-term linear relations meets each segment in at most two places | [Z, 4.6] |
| 9. Parameters | analysis | errors of size x/m and m; m near sqrt(x) gives the exponent 1/2 (the "chain of length sqrt(X)" of the author's note) | [Z, 1.3, 6] |

## 2. The path map (every field, also the unrelated ones)

Each row: the path, its field, its relation to the proof, a first bounded step. Rows 1 to 4 are opened now; the others
are recorded with their step.

| # | Path | Field | Relation | First bounded step |
|---|---|---|---|---|
| 1 | Extension of the mechanism to non-abelian Galois CM fields, toward the hypothesis for Dedekind zeta functions | algebraic number theory, representation theory of finite groups, additive combinatorics | the abelian inputs are listed in Section 3 | Section 3 (attempt begun 2026-11-22) |
| 2 | Corollaries of the formal theorems for abelian fields | class field theory | free consequences | Section 4 (done, classical) |
| 3 | The function-field model of the mechanism | arithmetic geometry over finite fields | Stepanov-Bombieri uses Riemann-Roch on C x C; the proof uses Arakelov slopes on lattices of automorphic forms | write the dictionary: auxiliary function and its vanishing order, against period and its divisibility; degree bound against archimedean norm; Riemann-Roch against Bost's slope inequality; the balance sqrt(q) against m near sqrt(x) |
| 4 | Bost's theta invariants as a replacement for the slope step | Arakelov geometry, statistical mechanics (Bost's thermodynamic formalism, arXiv:1909.04992) | theta invariants give an arithmetic Riemann-Roch (h^0_theta) that slopes approximate | read Bost's notes and Zhang 4.2 to 4.4; ask whether h^0_theta of the period lattices gives the covolume bound directly |
| 5 | Masullo's human draft for Hecke L-functions | automorphic forms (route unknown) | an independent route to the wider statement | obtain the draft; record its method and the reported problems |
| 6 | Connes-Consani: Weil positivity, Riemann-Roch for Spec Z | noncommutative geometry | positivity and Riemann-Roch for the arithmetic curve, now that the target is known to hold | record which of their reductions become theorems and which statements stay open (the semilocal positivity) |
| 7 | Bloch-Kato bounds inside the proof | Iwasawa theory, Euler systems | Section 5 of [Z] bounds Selmer groups of Tate twists | read [Z] 5 with the blueprint; record whether any bound is new (shared with the BSD row of the Millennium review) |
| 8 | Effective and explicit consequences under GRH for Dirichlet L-functions | computational number theory | Bach's bound for the least non-residue, deterministic primality tests, effective class number bounds, explicit prime number theorems in progressions now hold as theorems | list them with their explicit constants; consider a Lean corollary on the model of the Robin-Lagarias check of the MIT page |
| 9 | The formal artifact as an object | formal methods, graph analysis | 1,051,598 declarations; the blueprint's reference graph | compute the import graph of the archive (text only, no build) and map it to the nine steps of Section 1 |
| 10 | Line B of the plan (simple zeros in short windows, T1) | analytic number theory | not implied by the proof | unchanged (RH-067 review pending, RH-062 next) |
| 11 | Random matrices, quantum chaos, de Branges spaces, Hilbert-Polya operators | mathematical physics, operator theory | no relation to the proof found | recorded; reopened only with a concrete statement that stays open under the hypothesis |

## 3. Attempt: the mechanism beyond abelian fields

Target [Q]: for a Galois CM field E with non-abelian group G = Gal(E/Q), every zero of the Dedekind zeta function of a
subfield F of E in the critical strip lies on the line. (A subfield of a CM field is CM or totally real; fields that
are neither, such as Q(2^(1/3)), are outside this route, because the mechanism lives on unitary groups over the totally
real subfield of a CM field.)

### 3.1 Where Gal(E/Q) abelian is used [Z]

| Input | Abelian use | Non-abelian situation |
|---|---|---|
| (a) Frobenius condition (Prop. 3.1) | places labelled by an abelian group; Frobenius acts by translation; orthogonality gives Dirichlet characters | Frobenius is a conjugacy class; see 3.2 |
| (b) Retaining the characters (3.3) | averages over a subgroup H_0 of the label group | right translations by a subgroup commute with the left action of Frobenius; see 3.2 |
| (c) CM periods (4.5) | Chowla-Selberg and Anderson for abelian CM types | periods of non-abelian CM types: Colmez's conjecture, proved for abelian CM fields and in an averaged form (Andreatta-Goren-Howard-Madapusi Pera; Yuan-Zhang, 2018) [K]; [Q] whether the proof needs one CM type or only the Galois average |
| (d) Iwasawa mu (5.3) | Ferrero-Washington: mu = 0 for the cyclotomic Z_p-extension of an abelian field | mu = 0 is Iwasawa's conjecture, open for non-abelian fields [K]; [Q] whether the bound needed for #S(E, j) survives a positive mu (the note says coarser bounds are tolerated at exceptional twists) |
| (e) Euler system (5.2) | Kato's Euler system for two-dimensional modular representations over Q | [Q] which representations occur when E is not abelian (Hilbert modular over a totally real field?), and whether an Euler system or a patching argument replaces Kato's there |
| (f) Galois representations (5) | Clozel-Harris-Labesse, Shin, Chenevier-Harris | available for any CM field [K]: no obstruction |
| (g) Place selection (4.6) | Behrend sets in an abelian group; orbit segments are arithmetic progressions | orbit segments are x, Fx, F^2 x, ...; see 3.3 |

### 3.2 The Frobenius condition in a non-abelian group [D]

Assumption of this computation [Q]: the contribution rule of [Z] 3.1 transfers to G with, for each finite place of
the coefficient field being summed, the Frobenius element of the prime of E below it; this is to be checked on [Z] 4.1
and on the Lean statements. Let the places of E be labelled by G after fixing an embedding, with Frobenius acting on
the left. At an unramified p,
the primes of E above p have Frobenius elements y F y^(-1), y in G. The product formula sums the valuations over all
finite places of the coefficient field, so the contribution of p^j at the place g is averaged over the primes above
p:

    (1/|G|) * sum over y in G of 1{ y F^j y^(-1) = g }  =  1{ F^j in C_g } / |C_g|  =  (1/|G|) * sum over irreducible rho of conj(chi_rho(g)) chi_rho(F^j),

with C_g the conjugacy class of g. For a weight phi on the places, the averaged count is the class average of phi at
F^j:

    sum over g of phi(g) 1{F^j in C_g}/|C_g|  =  phi_bar(F^j),   phi_bar(x) = (1/|C_x|) * sum over g in C_x of phi(g).

For phi the indicator of a subgroup H, phi_bar(x) = |H n C_x|/|C_x| = pi_H(x)/[G : H], with pi_H the permutation
character of G on G/H (pi_H(x) = |C_G(x)| |C_x n H|/|H|). The permutation character is the Artin character of the
Dedekind zeta function of F = E^H. So:

Observation [D]. If the weighted set of places, after the conjugation average, is a nonnegative combination of
indicators of subgroups H_i, the arithmetic side of the identity is a nonnegative combination of -zeta'/zeta of the
fields E^(H_i). Dedekind zeta functions have no pole except at 1, so at a zero every residue in the Mellin transform is
a positive multiple of a multiplicity, which is what the window form of Landau's lemma needs (positive residue at the
real poles; `context/2026-11-21-windowed-landau-endgame.md`). A general weight gives Artin L-functions with complex
coefficients, whose possible poles (Artin's conjecture) and signs break that positivity.

Constraints the observation must meet [Q]: the selected places must lie in one CM type (one place of each pair g, gc),
so c is not in H; and the places with arguments near x must be numerous and sparse along Frobenius orbits (3.3). A
subgroup H contains the whole orbit of each of its elements, which is the opposite of sparse. The abelian proof does
not need the selected set to be a subgroup, because there every function is a class function and the unwanted
characters are separated by averaging and bounded as errors ([Z] 3.3 and Section 6); how those errors are bounded is
the next thing to read, because it decides whether the non-abelian identity can carry Artin L-functions as errors and
keep only Dedekind zeta functions as the main combination.

### 3.3 Place selection in a non-abelian group [D, Q]

In the abelian case a segment of a Frobenius orbit is {g, g + F, g + 2F, ...} and a Behrend set meets each in at most
two points. In G the segment is {g, Fg, F^2 g, ...}: three consecutive points x, y, z satisfy z = y x^(-1) y. A large
set meeting every short segment in at most two points is a set with no "non-abelian three-term progressions" x, Fx,
F^2 x. Roth-type questions in non-abelian groups are studied in additive combinatorics (corners and progressions in
groups; quasirandom groups) [K]; [Q] which construction gives the size the proof needs, with |T2| measured against
|G|/2.

### 3.4 What the attempt established on 2026-11-22, and the next steps

- [D] The Frobenius condition averages to class functions, and subgroup-supported weights give Dedekind zeta
  functions of subfields, with the positivity the zero-detection step needs.
- [Q] Four inputs are open in the non-abelian case: the error separation of [Z] Section 6 with Artin L-functions as
  errors; Colmez-type CM periods for non-abelian CM types (or a proof that the Galois average suffices); a bound for
  #S(E, j) without mu = 0; an Euler system for the representations that occur.
- Next, in order: read [Z] Section 6 (how the surviving characters are bounded) and Section 4.5 (which CM periods
  enter); then the blueprint nodes for the same statements; then the four questions one by one, each as a note with a
  review. The attempt stops with a written obstruction if one input is shown to be equivalent to an open conjecture.

## 4. Corollaries for abelian fields [K, classical; no novelty claimed]

Proposition. Assume the five formal theorems (the hypothesis for every Dirichlet L-function). Let K be a number field
and psi a finite-order Hecke character of K whose class field L is abelian over Q. Then every zero of L(s, psi) with
0 < Re s < 1 has real part 1/2. In particular the hypothesis holds for the Dedekind zeta function of every abelian
number field.

Proof. By the inductive invariance of Artin L-functions, L(s, psi) = L(s, Ind from G_K to G_Q of psi). Since Gal(L/Q)
is abelian, the induced representation is the sum of the characters chi of Gal(L/Q) that restrict to psi on Gal(L/K)
(Frobenius reciprocity). Each chi is, by class field theory over Q, a primitive Dirichlet character chi*, and its
Artin L-function is L(s, chi*). So L(s, psi) is a finite product of Dirichlet L-functions of primitive characters,
and a zero in the critical strip is a zero of one factor, on the line by the formal theorem
`LFunction_eq_zero_re_of_isPrimitive`. For psi trivial, L(s, psi) is the Dedekind zeta function of K.

## 5. Ledger (methodology 10 and 11)

- Lenses active from 2026-11-22: anatomy (Section 1), reformulation and dictionary (rows 3, 4, 6), dimension ladder
  (abelian to non-abelian, Section 3), invariant (the class-function computation, 3.2), external dialogue (Zhang's
  note, the blueprint, Masullo's draft), the spine of line B.
- Exploration entry of this round: the non-abelian Frobenius average (3.2) and the non-abelian place-selection
  question (3.3), both new to the programme.
