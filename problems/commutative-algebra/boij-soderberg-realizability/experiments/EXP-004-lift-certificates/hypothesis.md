# EXP-004 preflight: rank certificates for the lift of the prime-field realizations to characteristic 0

Date: 2026-11-19. Status: frozen before any computation of this experiment. CPU only. Exact arithmetic (integer
matrices; ranks over the rationals and over GF(32003)).

## Question

EXP-001 found, on 130 pairs (ray, multiple), a module over GF(32003) with a pure Betti table and recomputed 64 of them
over QQ by resolving the lifted module in Macaulay2; 57 rechecks were not run, 7 stopped at the 30 minute limit and 2
did not give the pure table. A resolution over QQ is expensive and its failure says little. Is there a cheaper exact
certificate, and what does it give on the 66 hits without a completed positive recheck?

Certificate (rank test): build the lifted module from the saved generator matrix with symmetric integer
representatives, and compare, degree by degree, the rank over QQ and the rank over GF(32003) of the integer matrix that
defines its graded piece. If the ranks agree in every degree, the lemma below gives the pure table over QQ.

## Lemma (to be reviewed with the experiment)

Let p be a prime, S_R = R[a,b,c], and let A be a homogeneous matrix with integer coefficients.

(a) Cokernel form. Let M_k = coker(A over k : S_k(-d1)^b to S_k^a). In degree d the piece (M_k)_d is the cokernel of an
integer matrix A_d reduced to k, so dim (M_Q)_d = rows(A_d) - rank_Q(A_d) <= rows(A_d) - rank_p(A_d) = dim (M_Fp)_d.
Suppose M_Fp has finite length and a pure Betti table beta, and rank_Q(A_d) = rank_p(A_d) for every d up to the top
degree of M_Fp. Then M_Q has finite length and the same Betti table.

(b) Image form. Let T_R = S_R/(a^(r+1), b^(r+1), c^(r+1)), free over R, and N_k the image of A over k between free
T_k-modules. dim (N_k)_d is the rank over k of an integer matrix A_d, so dim (N_Q)_d >= dim (N_Fp)_d. Suppose N_Fp has
a pure Betti table beta as an S-module and rank_Q(A_d) = rank_p(A_d) for every d. Then N_Q has the same Betti table.

Proof. Work over the local ring Z_(p). In (a) let M = coker(A over Z_(p)); each M_d is the cokernel of the integer
matrix A_d, and equal ranks over Q and over F_p mean that M_d has no p-torsion, so it is free of finite rank over
Z_(p). In (b) let N be the image of A over Z_(p), torsion free in each degree; equal ranks mean that the cokernel of
A_d has no p-torsion, so N_d tensor F_p injects into the target and equals the image of A_d over F_p. In both cases we
have a graded S_(p)-module X, free of finite rank over Z_(p) in each degree, with X tensor F_p = the module over F_p
and X tensor Q = the module over Q. Take a minimal graded free resolution of X tensor F_p. Lift its generators to X
(Nakayama over Z_(p), degree by degree); the kernel K of the resulting surjection F_0 to X is again free over Z_(p) in
each degree, and K tensor F_p is the kernel over F_p because Tor_1 over Z_(p) of X_d with F_p vanishes. Repeating gives
a graded free resolution of X over S_(p) whose reduction is the minimal resolution over F_p. Tensoring with Q (flat)
gives a free resolution of the module over Q with the same graded ranks, so beta_ij(Q) <= beta_ij(F_p) for all i, j.
The Hilbert functions are equal, so for each j the alternating sums over i agree; the table over F_p is pure, so for
each j at most one i has beta_ij(F_p) nonzero, and the inequality forces equality. In (a) M_Q vanishes in every degree
where M_Fp does (it is generated in degree 0 and its pieces are no larger), so it has finite length; in (b) N_Q is a
submodule of a module of finite length.

The converse is not claimed: unequal ranks say that this lift is not flat at p, not that the ray fails over QQ.

## Method

- Input: the 130 verified hits of EXP-001 (`hits-manifest.json`; files under the data root, SHA-256 checked), each
  with its ray, multiple, generator ("module": the cokernel of a generic matrix of forms of degree d1, form (a) with
  the saved generator matrix; "socle": a generic level module, the image of a generic matrix of forms inside the
  truncated ring, form (b) with the saved generator matrix and the same exponents as the package's construction).
- For each hit and each degree: the integer matrix A_d built from the symmetric representatives; its rank over
  GF(32003) and its rank over QQ.
- Instruments: python-flint (integer matrices; `fmpz_mat.rank`, `nmod_mat.rank`) as the first; PARI/GP (`matrank` on
  the same integer matrix, and on its reduction) as the second, on every matrix of at most 2,000 rows and on a sample
  of 20 larger ones.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1: the ranks over GF(32003) reproduce, in every degree, the Hilbert function of the pure table of the hit (this
  checks the parsing of the saved matrices and the two constructions against EXP-001's own verdict on each hit).
- G2 (known answers): on the 64 hits whose resolution over QQ gave the pure table in EXP-001, the rank test passes in
  every degree (a module with that table has that Hilbert function, so a failure is a defect of this instrument or
  of the lift it uses).
- G3: the two instruments agree on every matrix both compute.
- G4: unit tests of the monomial bookkeeping on modules with known Hilbert functions (the Koszul complex's cokernel
  S/(a,b,c)^k, a complete intersection, the truncated ring T).

## Predictions

- P1: G1 to G4 hold (0.85).
- P2: at least 55 of the 66 hits without a completed positive recheck pass the rank test (0.75), and at least 40 of
  the 46 rays that EXP-001 leaves realized over GF(32003) only become realized in characteristic 0 (0.7).
- P3: on the two hits whose resolution over QQ was not pure ((0,3,8,10) and (0,3,11,12), multiple 1), the rank test
  fails too, with a larger rank over QQ in some degree (0.5). If it passes on either, the lemma and the EXP-001
  recheck contradict each other and one of them is wrong: the run stops there until the contradiction is explained
  (the resolution over QQ is then recomputed in a second system).

## What a PASS proves and what a FAIL proves

A pass on a hit proves, with the lemma, that the lifted module has the pure table over QQ, hence that the point is
realized over every field of characteristic 0. A fail proves nothing about the ray. The lemma is a derivation [D]
until a reader other than the writer has checked it; the table of EXP-001 is updated only with hits that pass and only
after that review.

## Premise dependencies

- The saved hits and their verified tables over GF(32003): EXP-001 (two systems).
- Flatness and lifting of minimal resolutions over a discrete valuation ring: the argument above.
- python-flint and PARI/GP ranks: exact; cross-checked (G3).

## Budget and kill criterion

Under two hours of wall time on at most 8 processes; a matrix whose rank over QQ exceeds 20 minutes is recorded as not
decided. If G2 fails on any hit, stop.
