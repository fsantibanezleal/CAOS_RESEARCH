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

### 3.4 Reading of [Z] Section 6, and a reduction by a compositum [D, under the assumption of 3.2]

[Z] Section 6: the coefficient of G_chi(x) after the averages is proportional to t m b v2/n, and Lemma 6.1 needs the
selected sets nearly full: t >= n x^(-delta/8) and n x^(-delta) <= v2 <= n, with n = |H| the size of the odd part of
the label group. The characters that survive the averaging over H_0 and are not used in G_chi contribute at most
4 r x^(1/2 + delta) "for the choices in [Alp26]" (Proposition 6.3); the note does not say how this bound is obtained.
[Q] It is the step to read in the blueprint first (backlog RH-068): if those extra terms are bounded through the
hypothesis for the extra characters themselves, the argument is an induction; if through zero-free regions at large
arguments, it is not.

Why the non-abelian part must stay fixed [K]: in quasirandom groups such as SL_2(F_q), dense sets contain many
progressions x, xg, xg^2 (T. Tao, "Mixing for progressions in nonabelian groups", Forum Math. Sigma, 2013), so a
place set of density x^(-delta) meeting every orbit segment in at most two points cannot be expected when the
non-abelian part of the label group grows. The proof's own label group grows (the cyclotomic layers vary with x), so
the growing part must be abelian.

The compositum. Let E_0 be a Galois CM field with non-abelian group G_0, and A_x the abelian CM fields the proof
uses, chosen linearly disjoint from E_0. Then E = E_0 A_x is a Galois CM field (a compositum of CM fields is CM) with
Gal(E/Q) = G_0 x Gal(A_x/Q). Label the places by pairs (g_0, a); Frobenius acts by (F_0, F_A). Take the selected
places T2 = {1} x B, with B a Behrend-type set in the abelian coordinate inside one CM type of A_x. Then:

1. CM type: each pair {(g_0, a), (g_0 c_0, a c_A)} is separated by the abelian coordinate, so {1} x B lies in a CM type
   of E whatever c_0 is.
2. Sparsity: the orbit of (1, a) meets {1} x Gal(A_x/Q) only at the steps j that are multiples of the order of F_0,
   where the abelian coordinates form an arithmetic progression; a Behrend set meets it in at most two points.
   Density: |T2| = |B| out of |G_0| |A_x|/2 places, the density of B times the constant 2/|G_0|, absorbed by
   x^(-delta).
3. Arithmetic side: averaging over the primes above p conjugates only the G_0 coordinate; by 3.2 the weight 1_{1} on
   G_0 averages to the regular character divided by |G_0|, the condition "p splits completely in E_0". With the abelian
   coordinate expanded in Dirichlet characters chi of A_x, the identity carries the Hecke L-functions
   L(s, chi o N_{E_0/Q}) of E_0, which for chi trivial is the Dedekind zeta function of E_0. These have no pole except
   s = 1 for chi trivial, so a positive combination modelled on [Z] (1.1) has positive residues at every zero, as the
   zero-detection step needs.
4. Target, if the rest transfers: every zero of zeta_{E_0} in the critical strip on the line; hence, by
   Aramata-Brauer (zeta_{E_0}/zeta_F entire for F inside E_0), the same for every subfield F of E_0: every field whose
   Galois closure is CM, and every totally real Galois field (take E_0 = F(i)).

What this reduction leaves [Q]: the transfer assumption of 3.2; the bound for the extra characters (RH-068); and the
arithmetic inputs for E = E_0 A_x, which is not abelian: periods of its CM types (RH-069), the Iwasawa mu-invariant of
its cyclotomic towers (RH-070), Euler systems and Galois representations for the lifts (RH-070). The combinatorial and
character-theoretic layers stop being the obstruction (RH-071 reduced to the abelian Behrend construction).

### 3.5 The three open inputs, read on the blueprint [B] (chrisflav/riemann-blueprint, nodes named; copies under the data root, `caos-research/riemann-hypothesis/line-f/blueprint/`)

RH-068, the characters that are not used. [B, thm-chain-averaging and its proof; thm-core-inequality.proof;
thm-auxiliary-fields; lem-good-auxiliary-primes] The auxiliary field is a Galois CM field E, abelian over Q, with
Gal(E/Q) = {+-1}^2 x A, |A| = n, containing sqrt(-q) and sqrt(-d) for primes q = 3 mod 8, d = 7 mod 16, of degree about
x^(2 + 8 eps), cut out of a cyclotomic field by conditions on psi, (./q), (./d). The other characters xi of Gal(E/Q)
trivial on A_0 enter as the sum of |g_xi(x)|; they are bounded by 4 o x^(1/2 + eps) because q and d are chosen
"good": for most primes q and d, every character involving (./q) or (./d) has L(s, chi) nonzero for
Re s > 1 - 1/400, |L'/L(1, chi)| <= C log Y, and |g_chi(y)| <= y^(1/2 + tau) on the window, by a mean-square estimate
over q (a large sieve for real characters) and Chebyshev's inequality, with the supply of primes from the prime number
theorem in progressions (Deuring-Heilbronn, Turan). "The square-root bound for g_chi is the strength of the Riemann
Hypothesis for chi, but only on [Y, X], and it is obtained for most q and d by averaging, not for each." So the extra
characters are handled by unconditional averaging, not by induction. [D, plausible] In the compositum of 3.4 the
analogous terms are Hecke L-functions of E_0 twisted by xi o N_{E_0/Q}; their Dirichlet coefficients are supported on
norms and the same mean square over q applies to the sequence sum over N(a) = n of Lambda_{E_0}(a) (a large sieve over
the quadratic characters (n/q)), with the zero-free region and the bound at 1 for Hecke L-functions of a fixed E_0.
This input transfers, subject to writing it out.

RH-069, the periods. [B, thm-chain-averaging] The main term is
M(a, w) = a (log a - 1 - gamma + L'/L(1, chi_K) - (1/|Phi|) sum over rho in Phi of log w(rho)), with K = Q(sqrt(-d)),
and the proof of the member bound uses Chowla-Selberg [B, thm-member-gap-bound.proof]. So the CM periods enter through
one imaginary quadratic field, matched against L'/L(1, chi_K). [D] In the compositum, the arithmetic main term of the
condition "p splits completely in E_0" carries the constant term of -zeta_{E_0}'/zeta_{E_0} at 1 (the Euler-Kronecker
constant of E_0, a sum of log derivatives at 1 of the Artin L-functions of G_0), and the period side must reproduce
it. That is a Chowla-Selberg formula for the non-abelian part: Colmez's conjecture, which relates Faltings heights of
CM abelian varieties to log derivatives of Artin L-functions. [Q] Whether the averaged form, which is proved
(Andreatta-Goren-Howard-Madapusi Pera; Yuan-Zhang, 2018), suffices depends on whether the construction can average its
main term over the CM types of E_0; this is now the sharpest form of the question.
[B, thm-member-gap-bound.proof and thm-chowla-selberg] How the period enters: in the upper bound for the slope,
log Omega = gamma + log(pi/v) - L'/L(1, chi_K) is "the mean logarithm of the periods that the Chowla-Selberg formula
gives", and the Chowla-Selberg node states it as the mean over the h ideal classes of K of
log(4 pi Im(tau_c) |eta(tau_c)|^4). So the proof uses the average of the log-periods over the Galois orbit of CM
points (the class group), not the period of one CM point. [D] This favours the averaged form of Colmez's formula for
the compositum: what is needed is an average of log-periods over a Galois orbit of CM points, matched against the
constant of the arithmetic main term. [Q] Which average the arithmetic side of the compositum produces (over the
CM types of E_0 K, or over a smaller orbit), and whether it equals the one the averaged formula (Andreatta-Goren-
Howard-Madapusi Pera; Yuan-Zhang) evaluates, which carries L'/L of the quadratic character of the CM extension.
[B] The blueprint reads the whole step as "the arithmetic form of Stepanov's method": the factor m in the
divisibility bound plays the multiplicity of the auxiliary function and the slope inequality plays the degree bound.

RH-070, the Tate-Shafarevich bound. [B, def-sha-bound] For the psi-fields E and twists 0 < e < t = floor(x^401), the
groups Sha^1(G_{E,S}, Q_l/Z_l(-e)) must be finite and sum over l in Sigma of log l times the sum over e of their
lengths at most exp(x^eps/2), for every finite set Sigma. [D, tentative] The allowance exp(x^eps/2) is superpolynomial
in x, while the degree of E is about x^(2 + 8 eps) and t is x^401: a growth of lengths that is polynomial in the
degree and in e, such as a positive Iwasawa mu-invariant gives along the 2-power cyclotomic tower (length about
mu 2^n), fits inside it. So Ferrero-Washington may be needed for finiteness or for the form of the bound proved in the
Lean code, not for its size. [Q] Read the blueprint's chap-sha to see where the vanishing of mu is used; for E_0 A_x
the finiteness for e >= 1 is the point to check (Soule's results on H^2 with positive Tate twists; the
Quillen-Lichtenbaum comparison, now a theorem by Voevodsky and Rost) [K].

### 3.6 What the attempt established on 2026-11-22, and the next steps

- [D] The Frobenius condition averages to class functions; subgroup-supported weights give Dedekind zeta functions
  of subfields, with the positivity the zero-detection step needs (3.2).
- [D] With E = E_0 A_x (E_0 fixed, Galois CM, non-abelian; A_x the proof's abelian fields) and T2 = {1} x B, the
  place selection reduces to the abelian Behrend construction and the arithmetic side becomes the Hecke L-functions
  L(s, chi o N_{E_0/Q}) of E_0, among them its Dedekind zeta function (3.4). A growing non-abelian part is excluded
  by Tao's mixing theorem.
- [B, D] The characters that are not used are bounded in the proof by unconditional averaging over auxiliary primes,
  which plausibly transfers to the compositum (RH-068, 3.5).
- [Q] The input that remains sharp: the main term must be reproduced by periods; for E_0 this is a Chowla-Selberg
  formula for the non-abelian part (Colmez's conjecture); open unless the construction can use the averaged form,
  which is proved (RH-069). The Tate-Shafarevich bound has superpolynomial slack and may not need mu = 0 (RH-070,
  tentative). The Euler-system input for the representations of the compositum is not yet read (RH-070).
- Next, in order: the blueprint's proof of thm-member-gap-bound (how Chowla-Selberg enters and whether its
  constant can be averaged over CM types); chap-sha (where mu = 0 is used); then a written note on the compositum
  reduction with a review. The attempt stops with a written obstruction if the period input is shown to need
  Colmez's conjecture for a single CM type.

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
- Second entry of the same day: the compositum reduction (3.4) and the three inputs read on the blueprint (3.5).
