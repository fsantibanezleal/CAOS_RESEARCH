# Literature and cross-field representation sweep after EXP-010

Date: 2026-09-27. Online search window: 2026-09-26 to 2026-09-27.
Status: strategic source review under methodology 13. It declares no
experiment and changes no verdict. Every number marked [I] is an exploratory
floating-point value, not a certificate.

## 0. Access boundary

The session's egress proxy rejected arxiv.org, export.arxiv.org, ar5iv,
alphaxiv, zenodo.org, Semantic Scholar, Springer full text, aimath.org and the
Goettingen host of Steuding's dissertation. Labels:

- [V] read in a primary artifact: the cached arXiv sources in `source-cache/`
  (Wang 2609.24167v1, Pearce-Crump 2609.15329v1), a public git repository
  cloned in the session, or anthropic.com;
- [S] taken from an abstract or search snippet of the primary page;
- [I] an inference or a floating-point computation made in this review.

No [S] item may enter a declaration, runner or verdict before it is read in the
primary source (RH-030).

The underlying working notes, the full synthesis report and the two
floating-point exploration scripts are retained in
[`2026-09-27-sweep/`](2026-09-27-sweep/README.md).

## 1. External standing

No located 2026 preprint improves the program's short-interval onset
(`theta>=0.534`, EXP-010) or its attributed global constant
(`0.67250079959...`, EXP-009). Every short-interval onset statement near
`0.5459` returned by search is one of the program's own Zenodo records.

| Item | Status | Consequence |
|---|---|---|
| Wang, arXiv:2609.24167v1 | [V] Proves `C_0+delta_0` with `delta_0=a_0(C_0-2/H_0)/(1-a_0)=6.66624...e-8` by keeping a spectral term `Delta_K` in Lamzouri's inequality (cached `main.tex` l. 34, 76-96). [I] `C_0+delta_0=0.6725007703418...` | EXP-009's `0.6725007995946757...` is about `2.9e-8` above Wang's printed bound. Records must say "the EXP-009 sharp ratio inside Wang's framework", never "Wang's constant". |
| Same source, title | [V] The title is *Proportions of the non-trivial zeros of the Riemann zeta function*. | `references.md` item 28 carried a wrong title; corrected in this round. |
| Same source, l. 912 | [V] Wang states that the refined inequality can improve the short-interval proportions of arXiv:2609.07918. | Priority and gain check for EXP-010 (RH-033). |
| Hua-Yang, arXiv:2608.16034, 2609.27808 (tracked) | [I] Their family constants `0.6725007036`, `0.8362503518` equal `C_0`, `C_1`. | A transplant of the unrefined constant, not a competing improvement. |
| Yang "critical-line program", Zenodo 22065921 | [V, git `ac85152`] Retracted 2026-09-03. A reviewer's "Proposition R": finite unconditional bounds on higher even trace moments of the compressed Weil matrix would force power-law zero-free regions. | Strengthens the existing quarantine of the 79.62% claim, whose repository still rests on sixth-moment constants and is not formally retracted. The announced conditional `0.6788` simple-zero proportion is a watch item only. |
| Lamzouri, arXiv:2609.02882 | [S] Snippets attribute to it a passage on a shorter proof "produced by an internal research version of Claude". | Attribution to be read in section 1 of v2 (RH-030). |
| Formal repositories | [V] AxiomMath/ZetaZerosV2 main `4c73b31`, PR #1 head `02dfc0b`; anthropics/formal-math `fbdc36b`; trmdy `1610b97`. | Unchanged against the pinned snapshots. |
| Goldston-Suriajaya 2511.20059 | [S] Published, Analysis Math. 2026, DOI 10.1007/s10476-026-00186-w. | Citation metadata update. |

New external items outside the previous dossiers, none of which proves a
zero proportion:

| Item | Claim | Use |
|---|---|---|
| Zhu, arXiv:2608.24827 [S] | Certified Weil positivity for test functions supported in `[-0.8,0.8]` through one finite PSD matrix, `8.9e-18<=lambda_min<=2.27e-17`; empirical Landau-Widom decay law | Certificate technology (RH-036) |
| Conrey-Kwan et al., arXiv:2607.00282 [S] | Levinson for PGL(3)xchi, at least 1/9 critical, with a power-saving mean value of `L` times a Dirichlet polynomial for `Q^eps<=T<=Q^(1/3-eps)`; public code | Template for hybrid short-window mean values (RH-027) |
| Rodgers, arXiv:2608.12315 [S] | Weighted Montgomery-Vaughan Hilbert constant strictly larger than `pi` | Relevant only if a Hilbert constant is assumed sharp |
| Connes-Consani-Moscovici arXiv:2511.22755; Connes-van Suijlekom arXiv:2511.23257; Suzuki arXiv:2606.09096 [S] | Zeta spectral triples from primes `p<=lambda^2`; real zeros of the transform of a simple minimal eigenvector; Weil space as a de Branges space | Watch list: finite and certifiable, no proportion channel |
| Shi arXiv:2609.04908; arXiv:2607.02828; arXiv:2605.20224 [S] | Finite matrices from Weil's explicit formula | Representation only; credibility unassessed |

## 2. RH-027 overstated its source

The backlog described RH-027 as a Steuding-range moment `nu<(3theta-1)/4`
for general `Q`. The sources support less:

- [V, program reading 2026-09-12, section 8.2 of the critical-mass dossier]
  Steuding's 1999 Theorem 2.1 treats `F=zeta+zeta'/log T`, Levinson's
  degree-one `Q`, with fixed shifts; the final error analysis specializes to
  derivative orders at most two.
- [S, Springer abstract of Acta Math. Hungar. 96 (2002)] The error
  `O(T^(1/3+eps)M^(4/3))` is stated for mollifier exponent `nu<3/8`.
- [I] `(3theta-1)/4` is the condition `T^(1/3+4nu/3)=o(T^theta)`. It is not a
  stated theorem. It reproduces Steuding's thresholds: `theta=0.552` gives
  `nu=0.164`, `theta=0.591` gives `nu=0.193`.

The supportable range is `nu<min{(3theta-1)/4,3/8}`, proved only for
degree-one `Q` and fixed shifts. A faithful degree-one moment adds nothing
below `0.552`. All of the value lies in an unproved extension to general `Q`
with uniform shifts, which is a new theorem, not an import. The gap over the
localized Young range is `(1-theta)/4`, tending to `1/8` as `theta->1/2+`; the
cap binds only for `theta>5/6`, and the Young range is better for
`theta>7/8`.

Engines named by the review: the Ishikawa-Matsumoto explicit Atkinson-type
formula for the mean square of `zeta` times a Dirichlet polynomial with complex
coefficients (Open Math. 9, 2011) [S], and Tang arXiv:2608.14852 (tracked),
whose admissible `(h,k,delta)` range has not been read [S]. The 2026-09-26
preflight classed Tang as unusable; that decision rested on the abstract and is
reopened only as a reading task.

Guth-Maynard large values (arXiv:2405.20552) and the global Kloosterman
routes (Bettin-Chandee-Radziwill 17/33, Pratt-Robles 6/11, Conrey 4/7) have no
window versions and are not engines for this item [S].

## 3. Kernel choice versus second-order information

Every pair-correlation multiplicity bound reduces to minimizing
`Q(r)=(r-hat(0)+int|alpha| r-hat)/r(0)` over `r>=0` with `r-hat` supported
where `F` is known; then simple `>=2-Q`, distinct `>=(3-Q)/2`. The review
reproduced in floating point the published constants `0.6725`
(Montgomery-Taylor), `0.6727` (Cheer-Goldston) and `0.6792`
(Chirre-Goncalves-de Laat) at support 1 [I].

At short-interval support:

| Support | Montgomery-Taylor simple | Cohn-Elkies simple [I] |
|---|---|---|
| 1.0 | 0.67250 | 0.6793 |
| 0.6 | 0.13455 | 0.1394 |
| 0.55 | -0.0006 | 0.0039 |
| positivity threshold | 0.55019 | about 0.5487 |

The Montgomery-Taylor threshold is the cosine threshold
`0.550193964744154...` already recorded in wiki chapter 3 as Wang's. EXP-010's
`0.534` lies below the whole bandlimited family, so its gain comes from the
EXP-006 parity product and the Levinson density, not from the kernel.

Cohn-Elkies kernels require `F>=0` beyond the support. Under RH this is free.
Unconditionally, zeros off the line contribute complex terms, and the 2026
unconditional constants equal the RH bandlimited constants exactly. Whether
the Lamzouri/Weil-form framework can absorb a sign-constrained tail is the
largest untested global lever (about `+0.0067`, to about `0.679`) and costs
about `0.0015` in onset (RH-032). The Cheer-Goldston versus Montgomery-Taylor
discrepancy must be resolved first: by Krein-Akhiezer factorization the
bandlimited class coincides with the `g*g~` class [I].

Historically, thresholds moved when new information about `F` arrived (GGOS,
`F(alpha)>=3/2-alpha` on `[1,3/2]` under GRH), not when kernels improved. No
unconditional short-window lower bound on `F` beyond `theta` is known.

## 4. Cross-field representations, ranked by proportion channel

1. Finite compression of Weil's Hermitian form. It is the only representation
   that has produced a proportion theorem (Alpoge-Furman, Lamzouri, Wang).
   Two program-relevant extensions: a moment LP over multiplicity
   distributions whose Cauchy-Schwarz instance is the EXP-006 product
   `(Q-S)(N-O)>=2(N-S)^2`, tightened by a three-level input, which is the zeta
   analogue of moving from the Cohn-Elkies bound to the three-point SDP bound
   in sphere packing (RH-034); and a Landau-Widom degrees-of-freedom count for
   the window-support concentration operator, a candidate explanation of the
   clustering of onsets near `theta=1/2` (RH-036, heuristic).
2. Families. A window of length `T^theta` is an orthogonality family for the
   twists `n^(-it)`; the mean-value theorem gives diagonal dominance exactly
   for `nu<theta-1/2` [I]. Families beat this with the asymptotic large sieve
   (Conrey-Iwaniec-Soundararajan 56%; Sono 61.07% critical, 60.44% simple,
   arXiv:2105.07422) [S]. The window analogue is off-diagonal
   Kloosterman/Voronoi information inside the window, the same content as
   RH-027.
3. Function fields. Short-interval statistics become unitary matrix integrals
   with piecewise-polynomial transitions (Keating-Rodgers-Roditty-Gershon-
   Rudnick, arXiv:1504.07804) [S], and nothing singles out half the degree.
   This supports reading `theta=1/2` as an artifact of the approximate
   functional equation, not of the zeros [I].
4. Derivative operators. Conrey (1983) gives critical proportions tending to 1
   for `Xi^(m)`. In windows a longer `Q(d/ds)` costs no polynomial length; the
   degree-201 detectors already use this. The benchmark is the variational
   construction of arXiv:2508.11108 (tracked), positive for arbitrarily short
   mollifiers [S]; its small-`nu` slope has not been compared with `0.7170`
   (RH-028).
5. Below `theta=1/2`. Karatsuba gives odd-order critical zeros for
   `H=T^(27/82+eps)`. The crude conversion `simple>=(c-(Q-1)/6)N` needs an
   odd-order critical proportion above about 0.167 at support 0.55 and 0.19 at
   support 0.5 [I], against Pearce-Crump's best global Selberg constant 7%.
   Not a live route (RH-035).
6. Watch list without a proportion channel: de Bruijn-Newman
   (`0<=Lambda<=0.2`, unchanged since 2020), Jensen hyperbolicity, horocycle
   criteria, Lee-Yang/Polya-Schur stability, multiplicative chaos and the
   spectral triples above. The one-dimensional kernel problems are solved by
   LP/SDP with rational dual certificates; machine-learned test functions are
   not needed there.

## 5. Plan consequences

The review retains the program purpose and the short-interval focus. It
re-scopes RH-027 and RH-028, adds routes RH-030 to RH-037 in
[`backlog.md`](../../../../program/riemann-hypothesis/backlog.md), and records
the focus and manuscript routing in
[`research-governance.json`](../../../../program/riemann-hypothesis/research-governance.json).
No new experiment is declared. The first actions are source reading (RH-030)
and two invariant-first computations (RH-031 and RH-032), each of which
reproduces a known value before any new number is trusted.

## 6. RH-030 primary-source verification (2026-09-27, network restored)

The environment's network access was widened the same day. The pinned
archive was restored (68 documents verified by size and SHA-256), the new
sources were pinned in [`source-manifest-rh030.json`](source-manifest-rh030.json),
and the load-bearing statements were read in full text. This section
supersedes the `[S]` labels above wherever they overlap.

| Item | Primary-text finding [V] | Consequence |
|---|---|---|
| Versions | arXiv 2608.13637v2, 2609.02882v2, 2609.07918v1, 2609.15329v1, 2609.24167v1 and 2508.11108v1 are still the latest versions; the pinned bytes stand. New: 2608.14852v1, 2608.24827v2, 2607.00282v1. | No re-pinning of tracked sources. |
| Wang, arXiv:2609.07918v1 | Theorem 1.1: `c(theta)=2-theta/2-cot(theta/sqrt2)/sqrt2`, `d(theta)=(1+c)/2` for every fixed `0<theta<1`; `theta_0=0.550193964744154...`, `theta_d=0.346658926139761...` (`zeros.tex` l. 173-215). Theorem 2.1: pair formula for fixed `0<lambda<theta<1`, `supp g` in `[-lambda,lambda]`, error `O_g(H+T^lambda L^2)` (l. 277-290). It restates Steuding's mollifier condition as `vartheta<3/8` (l. 136-144). | Confirms every use in EXP-002 to EXP-010. |
| Steuding 1999 dissertation | Theorem 2.1 (printed p. 11): for `theta<3/8`, the mean square of `A F` with `F=zeta+zeta'/L` and `a(n)=mu(n)n^(a-1/2)(1-log n/log M)`, i.e. `P(x)=x`, has error `O(T^(1/3+eps)M^(4/3))`. The cap arises on printed p. 48: `E(T)<<min_{L<=G<=T^(5/6)}{G+G^(-1/2)T^(1/2+eps)M^2}`, balanced at `G=T^(1/3+eps)M^(4/3)`, which needs `G<=T^(5/6)`, i.e. `theta<3/8`. The off-diagonal is bounded with the trivial factor `M^2`. The 2002 journal text is paywalled and was not read. | The RH-027 correction holds and is sharper: the theorem fixes the mollifier (`P(x)=x`) as well as `Q`. Because the `M^2` bound ignores the coefficients, extending the error term to general `P` looks routine [I]; the substantive work is general `Q` with uniform shifts. |
| Tang, arXiv:2608.14852v1 | Theorem 1: distinct odd primes `p,q`, Gaussian window of width `H=T^delta`, `delta` in `(1/2,1)`, no shifts. The twisted moment equals a main term of size `H(pq)^(-1/2)log(T/pq)`, plus a dual moment of `|L(1/2+it,chi)|^2` over characters mod `p` on a range of length about `T/H`, plus `O((T/H)(pqT)^eps[(p/q)^(1/2)+(q/p)^(1/2)])`. Admissibility: `H^2/max{p,q}>T^(1+eps)` (`main.tex` l. 160-206). | The constraint is on `max{p,q}`, not on the product. With mollifier weights `a_h a_k/sqrt(hk)` the summed error is `(T/H)M^(1+eps)`, so Tang's error term alone allows `nu<2theta-1`, twice the localized Young range `theta-1/2` [I]. The open questions are general coprime twists, shifts, and whether the summed dual moments are negligible or contribute a main term. |
| Short mollifiers, arXiv:2508.11108v1 | Theorem 1.1: there is `theta_0>0` such that for `theta<theta_0` some `Q_theta` in `C^1` with `Q(0)=1`, `Q(y)+Q(1-y)=1` and `P(x)=x` gives `kappa>2theta/3`; numerics suggest this for all `theta<=1/2`. | The benchmark proposed for RH-028 was already done in the 2026-09-26 preflight (section 5): their parameters give `0.6824 nu`; EXP-010's `0.7170 nu` sits at the single-piece Euler-Lagrange ceiling `0.7173`. Any further slope gain must come from a second mollifier piece. |
| Lamzouri, arXiv:2609.02882v2 | The "internal research version of Claude" passage is Lamzouri's own abstract and introduction crediting Alpoge-Furman; no attribution problem. Proposition 2.1: `eta` in `L^2`, real, even, `supp eta` in `(-lambda,lambda)`, `K=(eta^2)^`; lower bounds in terms of `sum K(z-s)^2` for any conjugation-invariant finite multiset. Positivity comes from a Hilbert-space (Bessel) argument, and the pair formula it feeds (BGSTB Lemma 5) needs support in `[-1,1]`. | RH-032 premise weakened: a Cohn-Elkies kernel has no compactly supported `eta`, so it lies outside Proposition 2.1 as stated. RH-032 becomes a short admissibility note unless a Gram representation for a sign-constrained tail appears. |
| Archive drift | Two pinned documents no longer reproduce from their URLs: the Anthropic research page (174,655 bytes now against 176,754 pinned) and the Karatsuba 1985 URL (now 27,789 bytes, not the 518,106-byte PDF). | Neither is an input to an open route; recorded, not re-pinned. |

Net effect on the plan: RH-027 gains a cheaper intermediate target (a
Tang-type range `nu<2theta-1`) beside the Steuding-type target; RH-028's
benchmark is closed; RH-032 is downgraded; RH-031 remains the first
computation.
