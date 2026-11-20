# EXP-148 hypothesis: exact replay of Long's universal Mathieu pair on SU(N), 2 <= N <= 16, through the first column

Declared 2026-11-19, before any code of this experiment ran. Focus JC-F7, backlog JCB-108. CPU only.

A preflight read the source in full and priced the check (private management mirror,
`wip/caos-research/jc-long-preflight-2026-11-19.md`); its transcription probe evaluated the closed formula with the
paper's own reduction and is not this experiment.

## Question

C. D. Long, "The Mathieu Property for Compact Connected Lie Groups", arXiv:2609.16178 v1 (the only version on
2026-11-19; PDF dated 2026-07-30; unrefereed; AI-assistance disclosure on p. 13), states a pair of polynomials on C^2 and
transfers it to every nonabelian compact connected Lie group. For SU(n) in the defining representation (Proposition 5.4,
eq. (5.9), p. 8) the claim is, with z0 = g11, z1 = g21 and I the Haar integral:

- I(P^m) = 0 for every m >= 1;
- I(Q^s P^m) = c_m binom(m-1, s-1) (2)_(4m+s) / (n)_(4m+s), with c_m = 4^m (m!)^2 / (2m+1)! and (x)_k the rising
  factorial; in particular I(Q P^m) > 0 for every m >= 1, which contradicts the Mathieu conjecture for SU(n).

Question: do these identities hold exactly for 2 <= N <= 16, 1 <= m <= 8 and 0 <= s <= 4, when the Haar integrals are
computed by routes that do not use the paper's Hopf-coordinate proof? The range of N covers the columns of the index map
of the cascade paper (v0.10, 10.5281/zenodo.24269044), whose Mathieu row is open for 3 <= N <= 14.

## Source (archived in the data root, `sources/long-2609.16178/`, with SHA256SUMS)

`long-2609.16178v1.pdf`, 14 pages, SHA-256 `1da42c2fddc0a0c559cfdac56514bcfb85c6f3454d4aa443bf8e170f9dbe178f`.

- Eq. (3.1), p. 3: a = |z0|^2 + |z1|^2, tau = |z0|^2 - |z1|^2, u = 2 z0 conj(z1), v = 2 z1 conj(z0); (3.2): a^2 = uv + tau^2.
- Eq. (3.3), p. 4: P = (a + u)(a^2 v - (2a + u) tau^2), Q = u; (3.4): P(rz) = r^8 P(z), Q(rz) = r^2 Q(z).
- Eq. (3.5), p. 4: c_m = int_0^1 (1 - s^2)^m ds = 4^m (m!)^2 / (2m+1)!.
- Theorem 3.1 and Corollary 3.2, pp. 4-5 (the identities on S^3); Theorem 4.1, p. 6 (radial transfer); Proposition 5.4,
  p. 8 (SU(n) and Sp(n)); eq. (5.6): A = a o Phi, with Phi(g) = (g11, g21) in the defining representation.

## Definitions

Mathieu conjecture for a compact connected Lie group K (as used in the cascade paper): if f is a finite-type function
on K (a polynomial in matrix coefficients of finite-dimensional representations) with int f^m = 0 for all m >= 1, then
for every finite-type g, int g f^m = 0 for all large m. P o Phi and Q o Phi are polynomials in g11, g21 and their
conjugates, hence finite type. A monomial z0^a0 z1^a1 conj(z0)^b0 conj(z1)^b1 is balanced when (a0, a1) = (b0, b1).

## Derivation to be checked [D]

1. First column. For N >= 2, SU(N) acts transitively on the unit sphere S^(2N-1) of C^N with stabilizer SU(N-1), so the
   image of Haar measure under g to g e1 is the unique SU(N)-invariant probability measure on the sphere, the uniform
   one. An integrand in g11, g21 and their conjugates is therefore integrated against the uniform measure of S^(2N-1) in
   the first two coordinates.
2. Coefficient identity on S^3 (N = 2, a = 1). With tau = t and u = sqrt(1 - t^2) e^(i phi), the uniform measure is
   dt dphi / (4 pi) on [-1, 1] x [0, 2 pi) (Archimedes), v = conj(u) = (1 - t^2)/u, and
   u P = (1 + u)(1 - (1 + u)^2 t^2). The phi-average of a Laurent polynomial in u is its constant term, so for a
   polynomial H, int H(Q) P^m = (1/2) int_{-1}^{1} [u^m] H(u) (1 + u)^m (1 - (1 + u)^2 t^2)^m dt
   = [u^m] H(u) (1 + u)^(m-1) J_m(1 + u), J_m(y) = int_0^y (1 - s^2)^m ds. Since (1 - s^2)^m vanishes to order m at
   s = 1, J_m(1 + u) = c_m + O(u^(m+1)), hence int H(Q) P^m = c_m [u^m] H(u) (1 + u)^(m-1): zero for H = 1 and
   c_m binom(m-1, s-1) for H = u^s.
3. Transfer. The image mu of Haar measure under Phi is invariant under the SU(2) acting on rows 1 and 2 (left
   multiplication preserves Haar measure). Averaging over that SU(2) and using (3.4), int Q^s P^m dmu =
   c_m binom(m-1, s-1) int a^(4m+s) dmu and int P^m dmu = 0. On the uniform sphere S^(2N-1), |z0|^2 + |z1|^2 has moments
   E[a^k] = (2)_k / (N)_k.

Steps 1 to 3 give the claim for SU(N), every N >= 2 and every m, s. The experiment checks the finite range by machine;
the all-m statement rests on steps 1 to 3, which a reader other than the writer reviews before the cascade paper uses it.

## Method (exact rational arithmetic; `run.py`, Python standard library, `fractions.Fraction`)

Build P from (3.3) by polynomial arithmetic over the Gaussian integers in (z0, z1, w0, w1), w = conj(z), never from the
expanded 16-term form; build Q^s P^m by multiplication. Three integration routes:

- Route A (complex sphere moments): int z^alpha conj(z)^beta over S^(2N-1) is 0 unless alpha = beta, and then
  (N-1)! alpha0! alpha1! / (N-1+alpha0+alpha1)!. All N in 2..16, m in 1..8, s in 0..4.
- Route B (real sphere moments, a different formula and code path): substitute z0 = x0 + i x1, z1 = x2 + i x3, expand in
  the real coordinates and integrate with int x^e over S^(n-1), n = 2N: 0 if some e_k is odd, else
  prod (e_k - 1)!! / (n (n+2) ... (n + |e| - 2)). The imaginary part must vanish exactly. N in 2..16, m in 1..5,
  s in 0..3 (the expansion grows; the range is fixed here, before the run).
- Route C (Weingarten calculus on U(N), no sphere): for the balanced monomials of degree d = 4m+s <= 5, that is
  (m, s) = (1, 0) and (1, 1), the integral of prod g_{i_k 1} conj(g_{j_k 1}) is the sum over sigma, tau in S_d of
  delta(i, sigma j) Wg(sigma tau^-1, N), with Wg(rho, N) = (1/d!^2) sum over partitions lambda of d with at most N parts
  of chi_lambda(1)^2 chi_lambda(rho) / s_lambda(1^N), characters by the Murnaghan-Nakayama rule and s_lambda(1^N) by the
  hook-content formula. N in 2..6. The integrand is balanced, so it is invariant under g to e^(i theta) g and the U(N)
  and SU(N) integrals agree.
- Route H (the reduction of step 2, N = 2 only): the constant-term integral (1/2) int_{-1}^{1} CT_u[...] dt evaluated
  exactly as a polynomial integral in t, m in 1..8, s in 0..4.

Identity checks: (3.2) and (3.4) as polynomial identities; u P - (1 + u)(1 - (1 + u)^2 tau^2) lies in the ideal of
a - 1 and uv + tau^2 - 1 (checked by substitution v = (1 - tau^2)/u, a = 1 as rational functions); the expansion of P has
16 monomials, each balanced, equal to the list of the preflight.

Output `artifacts/results.json`: every (route, N, m, s) with the exact value, the predicted value and equality.

## Controls (each must behave as stated, or the instrument is wrong and no verdict is drawn)

- K1: P with one monomial removed (each of the 16 in turn) has I(P^m) != 0 for some m <= 3 at N = 2, for at least 12 of
  the 16 removals; every removal changes some value in the table.
- K2: the prediction with c_m replaced by 1/(m+1) disagrees at m = 2.
- K3: P with the factor (2a + u) replaced by (a + u) has a nonzero pure moment at some m <= 3.
- K4: Routes A and B agree on 200 random balanced and unbalanced monomials of degree at most 12 at N = 2, 3, 5.
- K5: Route C reproduces int |g11|^2 = 1/N and int |g11|^4 = 2/(N(N+1)) for N = 2..6.
- K6 (known true case): the abelian analogue, P and Q restricted to z1 = 0, gives Q = 0, so no violation arises from the
  torus direction; recorded as a sanity line, not as a test of the Duistermaat-van der Kallen theorem.

## Prediction

Every identity holds on the whole range, on every route (confidence 0.97; steps 1 to 3 were derived by hand before the
run and the preflight's transcription probe agreed with the closed formula).

## What a PASS proves and what a FAIL proves

PASS: the identities hold exactly for the stated finite range of N, m, s by three or four independent routes, so the
formulas of the paper are correctly transcribed and correct on that range, including every N of the open range
3 <= N <= 14 of the cascade paper. It does not prove the statement for all m: that rests on the derivation above (and on
Long's Theorem 3.1), which the machine check supports and does not replace. It verifies nothing about groups other than
SU(N), nor Sections 6 to 8 of the paper. FAIL at any point: eq. (5.9) is wrong as transcribed or as printed; the cell is
reported and the cascade paper cites the claim as not reproduced.

## Premise dependencies

- The statement of the Mathieu conjecture: the cascade paper, Section 2, from its located sources ([V] there).
- The uniqueness of the invariant measure on S^(2N-1) = SU(N)/SU(N-1) (standard; stated in step 1) [D].
- No earlier verdict of this programme is used; EXP-136 checked Long's earlier SU(2) functions (arXiv:2607.19012), a
  different pair.

## Compute budget and kill criterion

Expected under ten minutes in pure Python; killed at 60 minutes. If Route B exceeds the budget at m = 5, its range is
reported as run and the verdict names the cells it did not reach; Routes A and H are the load-bearing ones for the range.

## Invariant-first note

The whole construction is one invariant, the constant term in u after the phase average (step 2); the experiment is the
check of that invariant by direct integration, not a search.
