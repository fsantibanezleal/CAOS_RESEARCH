# Direct read: Dias-Pan, generic finiteness for cross central configurations of the 6-body and 6-vortex problems (CCB-036)

Read 2026-08-01, IN FULL (24 pages), from the author PDF.

- Source: arXiv:1811.08681v1 (math.DS, 21 Nov 2018), "Generic finiteness for a
  class of symmetric planar central configurations of the six-body problem and
  the six-vortex problem", Thiago Dias (UFRPE, then NTHU) and Bo-Yu Pan (NTHU).
- Archive: `E:\_Datos\caos-research\central-configurations\papers\arxiv-1811.08681.pdf`,
  SHA-256 408209a3e33c6ea2d7f64ca5b87e9b8bcef8701f6bb6f89fbdb1aef38fc95084.
- Publication status: UNCHECKED beyond arXiv v1; do not cite a journal version.
- Companion code: SageMath + Singular notebooks, their ref [8]:
  github.com/thiagodiasoliveira/CC6BP (not yet fetched; candidate for diffing).

## 1. What is proved (their statements, our tags)

- Object: CROSS central configurations of the planar 6-body problem (CC6BP):
  symmetric planar CCs with exactly four bodies x1..x4 on the symmetry line and
  x5, x6 mirror-paired on the perpendicular line. Symmetry forces m5 = m6
  (their Prop 3.1, one-line Laura-Andoyer argument). [V, read]
- Theorem 1.1 / 7.11 AS PRINTED: "There is a proper OPEN set B of R^5 such that
  if (m1,...,m5) in R^5 \ B the number of cross central configurations of the
  Newtonian six-body problem is finite." DISCREPANCY, recorded verbatim: the
  PROOF of 7.11 constructs B = Btilde intersect R^5 and states "B is a proper
  CLOSED subset of R^5" (Btilde a proper closed subset of C^5 from Thm 7.10).
  The mathematics delivered is finiteness off a proper closed subset; the word
  "open" in the two theorem statements is a typo for the complement phrasing.
  We must never quote the "open" phrasing as if it were the content. [V, read]
- Theorem 8.2: same statement shape for the six-VORTEX problem (vorticities
  gamma_i, s replaced by v_ikj = r_ik^-2 - r_jk^-2). [V, read]
- Both proofs are computer-assisted (SageMath + Singular); the paper self-labels
  Sections 4 and 7 as containing computer-aided proofs. [V]

## 2. The formulation (equations we may want in cclib)

- Laura-Andoyer equations (their (3.3)): L_ij = sum_{k != i,j} m_k s_ikj
  Delta_ijk = 0, with s_ikj = r_ik^-3 - r_jk^-3 and Delta_ijk the 3-point
  orientation determinant. Equivalent to planar noncollinear CCs with center of
  mass at the origin (they cite Hagihara Ch. III). This is the fourth
  formulation in our CCB-027 catalog, HERE seen doing real work: the L_ij are
  LINEAR IN THE MASSES, which is what makes their Jacobian block-triangular.
- Symmetry + shape reduction: conditions i-iv fix indexing, scale
  (x52 - x42 = 1) and orientation; the six-body cross geometry collapses the
  Laura-Andoyer system to FOUR nontrivial equations (3.4), and the Delta_ijk
  are eliminated via explicit signed-area relations (3.5), yielding system
  (3.6) in distances, s-variables and masses.
- The algebraic model (Prop 4.1): quasi-affine Omega = Ztilde \ D in C^32
  (16 S-variables, 11 R-variables, 5 masses; 28 equations: 12 Z_ij + 4 W_i
  clearing the S-definitions, 8 shape equations F1..F8 mixing collinearity
  r12 + r23 - r13 = 0 with Pythagoras relations like
  4 r15^2 - r56^2 - 4(r14 - 1)^2 = 0, and 4 Laura-Andoyer L1..L4).
  Mass space dim 5, so generic finiteness = dim(Omega) <= 5.

## 3. The proof architecture (the part that matters to OUR lane)

Chain: dim(E) = 4 for the shape variety E = Z(F1..F8) \ D (computed in
Singular, with I(H) primary so E irreducible); the Jacobian of the full system
is BLOCK-TRIANGULAR at fiber points (S-block diagonal nonsingular, R-block
identity), so inequality (7.1): dim_P(fiber of pi_1) <= 5 - rank(dL/dm at P),
where dL/dm is an explicit 4 x 5 matrix with entries s_ikj r_ij (masses appear
linearly). Then a case split over dim of pi_1(component):

- rank >= 2 everywhere on physical fibers (Prop 7.2, sign analysis of the
  s-entries from the shape inequalities) gives fiber dim <= 3.
- Lemma 7.3 (the workhorse): if dim pi_1(Omega_i) <= k and Omega_i is NOT
  inside the rank-<k determinantal variety Delta_k, then dim Omega_i <= k +
  (5 - k) = 5, by the dimension-of-fibers theorem on a dominant restriction.
- Components inside Delta_2 are DISCARDED as containing no physical CC6BP
  point (Prop 7.2). Presentational gap, noted: Theorem 7.9 asserts
  dim(Omega) <= 5 outright, while the argument as written controls only
  components containing CC6BP points (the discarded ones never matter for
  counting CC6BPs in 7.11, so the RESULT stands; the gloss is theirs, not
  ours to repair silently).
- dim pi_1 = 4 case (Prop 7.8) needs a WITNESS: an explicit CC6BP y with
  rank(dL/dm)(P_y) = 4, built in Prop 5.2 (equal m1..m4, collinear quadruple
  plus square): elimination in Singular gives the R12-eliminant
  (R12 - 1)^4 h(R12) with deg h = 52 (leading terms 49 R12^52 - 2548 R12^51 +
  66738 R12^50 + ...), Sturm isolates the unique root in (0,1) to
  (0.4402418528, 0.4402418529), the Extension Theorem lifts it, and the m5
  value (truncated 4.76482836) is unique because F3, F4 are LINEAR in M5.
  The rank-4 check evaluates a 4x4 minor determinant at the witness with an
  explicit mean-value-theorem error budget (their bound: error <= 10 against
  a value near 11.2514 sqrt(2) - 233.1798). Coarse but valid. [V, read]

## 4. THE INSTRUMENT WE WANT: Lemma 7.5's partial Groebner basis

Their Delta_3 case needs dim Z(J) <= 2 for J = <D_1..D_40, F_1..F_8> in the 11
distance variables, where D_l are the order-3 minors of dL/dm pushed to
distance-only form (substitute s_ikj = R_ij^-3 - R_jk^-3, clear denominators;
D_1 = (R25^3 - R12^3)(R35^3 - R23^3)(R15^3 - R13^3) - (R35^3 - R13^3)
(R15^3 - R12^3)(R25^3 - R23^3) is their printed example). A full GB of J was
out of reach ("arduous"). Their move:

  For each l = 1..40 compute the grevlex GB of the SMALL ideal
  J_l = <F_1..F_8, D_l> (eight shape equations plus ONE minor), collect the
  leading monomials of ALL these GBs into one monomial set K (24 monomials,
  printed on p. 18), and check dim Z(K) = 2 in Singular. Since each J_l is
  contained in J, every collected monomial is in LT(J), so K subset LT(J) and
  their Lemma 6.4 gives dim Z(J) = dim Z(LT(J)) <= dim Z(K) = 2. Runs "on a
  notebook with 16GB of memory in a few minutes".

Why this matters to us: it is a DECOMPOSABLE, budget-friendly, fully rigorous
UPPER-BOUND instrument for dimensions. Any monomials provably in LT(I) bound
dim from above; you harvest them from whatever subideals are tractable. This
is precisely the contingency our EXP-010 P3 rung lacks when a full staircase
GB caps (EXP-009 taught us caps are the default at n >= 4 for full solves),
and it scales by CHOICE OF SUBIDEALS rather than by total system size. Also
composable with our sections instrument: sections give the probabilistic
two-sided estimate, subideal leading terms give a deterministic upper bound,
and the deterministic lower direction can come from an explicit witness point
plus tangent/Jacobian rank (their Lemma 7.7 pattern, which we already run as
exact rank checks elsewhere).

## 5. What this closes and what it opens for the n = 6 strata map

- CLOSED (by them): generic finiteness for the CROSS symmetric class of planar
  6-body CCs (four on the symmetry axis, mirror pair off-axis, m5 = m6), and
  the same for six vortices. This is one closed stratum in the n = 6 symmetric
  landscape; it does NOT touch the general planar n = 6 problem (masses off
  the symmetric stratum, or other symmetry types).
- Their explicit witness (collinear quadruple + square, m1..m4 equal,
  m5 = m6 about 4.7648) is a concrete CC6BP we can re-derive exactly with our
  own instruments (the eliminant is degree 52 in one variable: well inside
  EXP-006-scale msolve work) as a calibration anchor if we open the symmetric
  lane (CCB-036 next stage).
- Open strata adjacent to this paper: other n = 6 symmetry types (two on the
  axis + two mirror pairs; three mirror pairs, i.e. full reflection symmetry
  with nobody on the axis; kite subcases). Montaldi (their [20]) guarantees
  EXISTENCE per symmetry type; finiteness per type in the Dias-Pan style
  (quotient system + fiber dimension + partial GB) looks n = 5-scale per
  stratum, exactly as CCB-036 conjectured. Their vortex section shows the
  method transfers across potentials (our CCB-019 lens).
- Their ref [9] (Dias, Proc. AMS 145 (2017) 3069-3084, "New equations for
  central configurations and generic finiteness") generalizes Moeckel's
  generic Dziobek finiteness to semi-integer exponents; relevant to CCB-019
  and to EXP-011's framing. Moeckel's Dziobek paper is their [19]: Trans.
  Amer. Math. Soc. 353(11) (2001), 4673-4686. Both UNFETCHED as PDFs; the
  citations are now verified via this paper's bibliography.

## 6. Honesty ledger for this read

- Everything in Sections 1-8 was read from the PDF directly; the SageMath /
  Singular notebooks were NOT run or fetched (their repo is recorded above).
  Claims of the form "dim(H) = 4 computed in Singular" are therefore [Vs]
  (verified as stated in the paper, computation not reproduced).
- The Theorem 1.1 / 7.11 "open"-vs-closed typo is recorded above; our wiki and
  any manuscript text must state the closed-complement form and may note the
  typo explicitly when citing.
- No journal version was checked; cite as arXiv:1811.08681 (2018) until a
  published version is verified.
