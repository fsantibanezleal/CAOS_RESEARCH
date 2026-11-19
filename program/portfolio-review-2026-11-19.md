# CAOS Research portfolio review, 2026-11-19

Follows [the review of 2026-10-30](portfolio-review-2026-10-30.md). Method: one literature researcher per active problem and
one for the proposed rows (eleven in all), searching for items dated after each problem's last external pass and for new
versions of every known reference; every item marked plan-changing was re-read on its primary page by an independent
skeptic; a synthesis ranked the problems by the probability that the next bounded action yields a decisive, attributable
advance within weeks. The full report, with every URL and search, is kept in the private management mirror
(`wip/caos-research/external-refresh-2026-11-19.md`). Marks as in the previous review: [V] read on the primary page, [V2]
secondary, [U] not confirmed. No negative search below is a novelty proof.

## 1. What changed outside

| Problem | New since the last pass | Impact |
|---|---|---|
| `jacobian-conjecture` | C. D. Long, "The Mathieu property for compact connected Lie groups", arXiv:2609.16178 v1 (dated 2026-07-30 in its PDF; unrefereed) [V]: for every nonabelian compact connected group G there are polynomials A, P, Q with all pure moments of P zero and I_G(Q^s P^m) = c_m binom(m-1, s-1) I_G(A^(4m+s)) > 0, c_m = 4^m (m!)^2/(2m+1)!; s = 1 gives a Mathieu counterexample on every such group. Also new or re-versioned: Gao arXiv:2608.00222 v2 (2026-11-04), Adamus-Hajto (v2 2026-11-16), Borisov-Gabber-Vasiu arXiv:2609.05746, Wang-Yan arXiv:2610.36495 [V/V2]; none touches JC(2), the degree floor or (72,108) | Plan-changing for the cascade: the open range SU(N), 3 <= N <= 14, and every other nonabelian group are claimed false (proof not checked). The planar side is unchanged: no refereed Helali, no GGHV update, no new reduction of the [125,150] configurations |
| `unsplittable-flow-cost` | S. Nikolenko, three Zenodo preprints (2026-07-30 to 2026-08-13; records 21701162, 21716713, 21922203) and the repository snikolenko/unsplittable-flows [V]: a planar lower bound (299 - 41 sqrt 41)/32 = 1.1397 (2026-07-30), in which 9/8 is the exact supremum of the symmetric three-terminal template; a general lower bound 1.2824948, refined by A. De la Fuente to 1.28260069 (merged 2026-08-04); a planar record 1.17353531974518; exact-mean decompositions with E(3) = 9/8, E(4) = 1.1397 [V] | Plan-changing: "alpha* >= 9/8, alpha*_planar in [9/8, 2]" (EXP-005) is superseded as a bound, and the 9/8 value was published by Nikolenko a month before the Muffatti commit credited in EXP-005. The Rybin instance value 16/15 and EXP-006 stand |
| `proposed-rows` | Qin and Sun arXiv:2610.12218 [V]: H(d) = Omega(d^2 ln^2 d), Lean-certified per the authors; the explicit bound is positive only from about d = 1659 | `hilbert-16`: the asymptotic lower bound is taken; only exact small-degree certificates remain. `boij-soderberg-realizability`: no follow-up to arXiv:2605.25259v2 [V]; the published witnesses have d3 = 21 (Question 6.1) |
| `navier-stokes` | Fan Zheng arXiv:2610.02509 (unforced Euler blowup claim) and arXiv:2610.06544 (unforced IPM gradient blowup) [V] | Minor: citations for the dormant audit paper |
| `riemann-hypothesis` | Knausgard arXiv:2610.08965, Cobeli-Zaharescu, Pearce-Crump v2 [V]: global proportions; no short-interval onset below 0.5339 | Minor; the research stays paused |
| `central-configurations` | Liu-Liu arXiv:2610.32751, a Tomar Zenodo companion, a newer Nagy working paper [V]; no rebuild or critique of the five-body claims | Minor; on hold |
| `petersen-coloring`, `tau-conjecture`, `hoa-mnh`, `bougard-joret`, `huneke-wiegand` | Nothing new in the searches listed; every key reference is at its recorded version | None |

The openai/math repository has no commit after 2026-10-30 [V].

## 2. Ranking for the next bounded action (probability of a decisive, attributable advance within weeks)

| Rank | Problem | Next bounded action | Estimate |
|---|---|---|---|
| 1 | `boij-soderberg-realizability` (open now) | Stage 0 and 1 of the dossier's plan: the realizability table of the primitive points for d3 <= 12 over S, with formula bounds, published obstructions and a random-module search in Macaulay2; the two d3 = 10 counterexamples to Question 6.1 checked by machine | 55 to 65 percent |
| 2 | `petersen-coloring` | PCC-F5: H_3 membership of G68 at target order 52 (the formula of EXP-007 addendum 7 exists) | 50 to 60 percent, conditional |
| 3 | `tau-conjecture` | TC-F5 witness anatomy | about 50 percent |
| 4 | `bougard-joret` | BJ-F4 (BJB-015) | 35 to 45 percent |
| 5 | `huneke-wiegand` | HWB-101 | 30 to 40 percent |
| 6 | `hoa-mnh` | order 13 case B | 25 to 35 percent |
| 7 | `unsplittable-flow-cost` | an independent exact re-verification of Nikolenko's records (verification, 60 to 70 percent); a new record 10 to 15 percent | see decisions |
| 8 | `jacobian-conjecture` | JC-F5 ([125,150] systems) | 10 to 15 percent; the exact replay of Long's construction is a short verification |
| 9 to 12 | `central-configurations`, `riemann-hypothesis`, `navier-stokes`, other rows | | 10 percent or less |

## 3. Decisions

1. **Open `boij-soderberg-realizability`** as the deep focus of this round (rank 1; the order of the 2026-10-30 review, "open
   after hoa-mnh", is met). Toolchain: Macaulay2 1.22 in WSL, Singular 4.3.2 for cross-checks. First bounded experiment:
   Stage 0 and Stage 1 of the 2026-09-02 dossier, hypothesis frozen before any computation.
2. **`jacobian-conjecture`:** JC-F4 is closed (success gate met; planar v0.38, 10.5281/zenodo.24358296). Long's Mathieu
   result enters the cascade board as claimed [V]; the cascade paper is revised (v0.11) after an exact replay of his
   construction on SU(3) where feasible (a new experiment, verification only). JC-F5 stays proposed with its preflight
   (count the [125,150] configurations and derive one system) before any certificate campaign.
3. **`unsplittable-flow-cost`:** the records state Nikolenko's bounds and correct the credit of 9/8 (Nikolenko 2026-07-30,
   symmetric template; the Muffatti family checked by EXP-005 is its limit point). The programme's lower-bound focus is
   closed as superseded; the preprint (10.5281/zenodo.21554259) is revised as required by its now-stale statements, with an
   independent exact re-verification of the current records as its new content (a new experiment).
4. **`petersen-coloring`:** PCC-F6 closes (EXP-015); PCC-F5 is the next focus after the Boij-Soderberg opening.
5. `tau-conjecture`, `bougard-joret`, `huneke-wiegand`, `hoa-mnh`: their proposed focuses stand; no external change.
6. `hilbert-16`: re-scoped to exact small-degree certificates only; not opened.

## 4. Non-claims

The estimates are judgments, not measurements. Every claim of another author recorded here is theirs; claims whose proofs
CAOS has not checked are marked as claimed.
