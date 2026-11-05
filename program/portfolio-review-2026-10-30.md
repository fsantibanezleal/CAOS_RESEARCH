# Portfolio review, 2026-10-30: external status of every problem and the priorities that follow

This is a program-level strategy record under methodology 13. It does not change any experiment
verdict. For each of the 20 portfolio rows it records the external status found online on
2026-10-30, the developments after each problem's last literature pass, the public work that
overlaps a CAOS result, and the plan change that follows. Facts carry the marks of methodology 05
([V] read on a primary source, [V2] secondary only, [U] searched and not located); assessments are
labelled as such and kept apart from the facts.

## Method

- Four bounded literature passes on 2026-10-30 (algebra; combinatorics and optimization; number
  theory and complexity; dynamics, PDE and physics), each covering status, new versions,
  follow-ups, overlaps with CAOS claims, open sub-questions, competition, and the OpenAI Math
  release (`openai/math` at upstream commit `4eaee87`, 2026-10-29). Their full reports, with every
  URL, are kept in the private management mirror.
- The claims that change a plan were re-read on the primary page by the coordinating session:
  arXiv:2610.13100 and arXiv:2610.16107 (five-body central configurations), arXiv:2610.08144
  (Navier-Stokes Lean audit), arXiv:2609.24167 (withdrawal), Zenodo record 21479814 (the planar
  (72,108) claim), arXiv:2610.24889 (cascade dimensions) and arXiv:1211.4554v1, Proposition 10 and
  Theorem 13 (gluing and the Huneke-Wiegand property).
- Internal state is read from the records on `develop` at `8d2267b7`.

No negative search below is a novelty proof.

## 1. Priorities (assessment)

Ranked by: a decisive, attributable next result that a small exact-computation program can still
obtain; the novelty window; the assets already built; and the cost of the next bounded action.

| Rank | Problem | Why now | First bounded action |
|---|---|---|---|
| 1 | `petersen-coloring` | Problem 11 of arXiv:2608.10028v4 (a cyclically 5-edge-connected counterexample) and a bounded Petersen defect on that class are high value and still unclaimed: nothing public after v4 (2026-09-30). The charge calculus and SAT/DRAT toolchain are built. The 52-vertex group is fast, so the window is time-limited. | EXP-015 as already ordered in `petersen-coloring/RESUME.md` section 5: 6-poles cut from the cyclically 5-edge-connected snarks of order at most 28, sector matrices, closures; close PCC-F6 if no zero-trace element exists. |
| 2 | `tau-conjecture` | No tau-conjecture paper since 2019 [V]; no public census of integer roots of short straight-line programs [U]. EXP-014 showed the [-32,32] window decides 99.998% of the additive nine-gate space, so z_max(9) is one residual away. | TCB-039: close the |c| >= 396 residual (0.002% of the space) with a dedicated confinement argument or exact sweep; a closed residual settles the seven-root threshold at 10 and gives z_max(9) = 6. |
| 3 | `hoa-mnh` (open it) | Zhan's disproof (arXiv:2608.00957v3, 2026-08-14) has no follow-up and does not claim 56 is least [V]; his Questions 2 to 4 are open [V]. Radar score 14/18 at scouting; exact Hamiltonicity checks; no visible competitor. | Run the opening gate of the entry point section 5 on the 2026-09-02 dossier, then EXP-001: exhaustive maximal non-Hamiltonian graphs to order 12 with a certified least counterexample order or a verified range. |
| 4 | `bougard-joret` | Das-Gupta (arXiv:2608.18828) is still v1 and says nothing about n = alpha+k+1 or the triangle-free slice [V]; no follow-up [V]. Theorem-shaped targets with exact certificates. | BJB-014 (the endpoint of d^2+4d+1 <= f(2d+3,2,d+2) <= d^2+4d+2), then exact small-triple data toward a corrected conjecture in the second regime n > k*alpha, which Das-Gupta leave open [V]. |
| 5 | `jacobian-conjecture` (redirect) | The (72,108) planar frontier, our long-running target, is publicly claimed excluded by Helali (Zenodo 10.5281/zenodo.21479814, 2026-07-21, conditional on the GGHV reduction, review requested) [V] and by Guo (GitHub preprint, 2026-08-10, conditional) [V]. An independent exact check of that claim is decisive either way and is citable as verification. | Strategic review (methodology 13, boundary 1 and 4), then one experiment: an independent replay of the two Laurent/Newton systems of GGHV Proposition 4.3 with a different elimination route. Park the transverse Fitting atlas. |
| 6 | `boij-soderberg-realizability` (open after `hoa-mnh`) | No follow-up to the Rethlas paper (arXiv:2605.25259) in five months [V]; our d3 = 10 counterexamples to Erman-Sam Question 6.1 remain smaller than the published one [V]; the d3 <= 12 table is finite. Needs a Macaulay2 toolchain. | Open with the 2026-09-02 dossier; first confirm both d3 = 10 points fail over U(H) as well as over S (Question 6.1 asks for either ring). |
| 7 | `huneke-wiegand` (close out HW-F7) | HW-F7 is answered by this review: the gluing transfer of EXP-067 is Proposition 10 and Theorem 13 of García-Sánchez and Leamer (2012). What remains new is the explicit family and the exponent-set transfer. | Record HWB-094 as a corollary disposition with credit, then the mandatory strategic review; candidate next focus: their open question on gluing for ideals with more than two generators. |

Hold or redirect (assessment): `central-configurations` (n = 5 finiteness now claimed by several
groups; redirect to an independent replay of the Lean-certified claim or gate), `unsplittable-flow-cost`
(refresh the dossier before EXP-005; the field moved), `navier-stokes` (dormant after one citation
revision), `riemann-hypothesis` (paused by Felipe; one publication-correction item is open, see
section 3). Proposed rows not to open now: `hodge`, `bsd`, `p-vs-np`, `yang-mills-mass-gap`,
`centralizers`, `diophantine-2var`. Re-scope before any opening: `sphere-log-energy`, `hilbert-16`,
`linear-programming`.

## 2. Problem by problem

### Opened problems

**`petersen-coloring`** (last pass 2026-10-06). External: disproved (Putman arXiv:2608.10012; Goedgebeur,
Jooken, Máčajová, Mattiolo, Mazzuoccolo, Ulyanov arXiv:2608.10028, v4 2026-09-30) [V]. New since the
last pass: none on the conjecture; adjacent only, Mkrtchyan arXiv:2610.35794 (2026-10-26, a
complexity statement for H-coloring) [V]. Overlap with CAOS claims: none new; the audit-row overlap
with v3 and v4 is already recorded. OpenAI Math: none. Plan: unchanged, PCC-F6 stays active (rank 1).

**`tau-conjecture`** (last pass 2026-08-25). External: open; newest tau-conjecture item on arXiv is
arXiv:1905.00091 (2019) [V]. Overlap: none found [U]. OpenAI Math: family 108 (an Omega(n^3) border
determinantal bound for the permanent) is adjacent, not overlapping [V]. Plan: rank 2, TCB-039 first.

**`bougard-joret`** (last pass 2026-09-05). External: disproved at n = alpha+k by Das and Gupta,
arXiv:2608.18828v1 (2026-08-19), smallest counterexample (7,3,4), second regime n > k*alpha open [V].
New: none; arXiv:2609.15637 cites the large-order case for 2-connected graphs [V2]. Overlap: none for
f(alpha+k+1, alpha, k), T(d,d+1) or the f(2d+3,2,d+2) bracket [U]. Plan: rank 4.

**`jacobian-conjecture`** (last pass 2026-09-18). External: false for n >= 3 (Alpoge's map, announced
2026-07-19/20 on X; no arXiv paper by Alpoge [U]); JC(2) open [V2]; reproductions and formalizations
include an Isabelle AFP entry [V2] and van den Essen arXiv:2609.17795 [V]. New since the last pass:
de Bondt arXiv:2610.24889 (2026-10-17): counterexamples to HJC(15), VC(28), HVC(30) and, with the
degree-3 reduction, JC(12,3), HJC(18,3), VC(34,4), HVC(36,4), and a cubic-linear counterexample in
dimension 90, over the Gaussian integers [V]; Kanel-Belov and Fedorov arXiv:2610.33919 (2026-10-24):
JC(2) implies a generalized Dixmier statement DC_1', no DC_2 counterexample announced [V]. Overlaps:
our explicit 48-variable witnesses for the vanishing and symmetric conjectures (EXP-041, restated in
EXP-136) are superseded in dimension by de Bondt's VC(28) and HVC(30); our Mathieu SU(N) threshold
N >= 24 may be lowered through HJC(15) (to check, not claimed). Not previously recorded: Helali's
and Guo's conditional (72,108) exclusion claims (above), Long arXiv:2608.23777 (Poisson for two
canonical pairs) [V], Kanel-Belov and Fedorov, de Bondt. The Wilson preprint in our records is
arXiv:2607.23887, a claimed proof of the two-variable Gaussian moments conjecture, correctly cited in
EXP-136 [V]. OpenAI Math: none. Plan: rank 5 with a redirect.

**`huneke-wiegand`** (last pass 2026-09-24). External: disproved by Christensen, Gerko, Iyengar
(arXiv:2608.21666, 2026-08-21, a field-extension construction found with Codex) and by Son Pham
(arXiv:2609.07615, 2026-09-07, numerical semigroup of multiplicity 56; Huneke recomputed the data) [V];
Pham's paper mentions the CAOS minimality and family results and does not rely on them [V]. New: none
after 2026-09-24 [U]. Overlap, decisive for HW-F7: García-Sánchez and Leamer, arXiv:1211.4554v1
(2012-11-19), Proposition 10: for a gluing Gamma = a1 Gamma1 + a2 Gamma2 and a relative ideal A1 of
Gamma1, "A := a1A1 + a2Gamma2 is Huneke-Wiegand if and only if A1 is Huneke-Wiegand", and Theorem 13 for
gluings of a symmetric Gamma1 with N [V, re-checked]. With a1 = q, a2 = m and Gamma2 = N this is the
ideal (t^(qm), t^(q(m+s))) transfer of EXP-067, by a combinatorial proof. What EXP-067 adds: the
explicit family (multiplicity 24p, embedding dimension 11p, Frobenius number q(102p-1)-24p), the
transfer of every consecutive-shift exponent set, and the flat-base-change route. A ResearchGate
title "Huneke-Wiegand conjecture and change of rings" remains unread [V2]. OpenAI Math: none. Plan:
rank 7, close HW-F7 as a corollary disposition with credit.

**`central-configurations`** (last pass 2026-08-24). External: planar five-body finiteness for all
positive masses is now claimed by Tomar (arXiv:2610.13100, v1 2026-10-09, v2 2026-10-15, Lean 4
formalization and certificates at Zenodo 10.5281/zenodo.23202861) [V, re-checked], by Chen and Tong
(arXiv:2610.16107, v1 2026-10-12, v4 2026-10-29, exact, interval and ball arithmetic, no Lean)
[V, re-checked] and by Liu and Liu (arXiv:2610.28168, 2026-10-20) [V]; none refereed. An earlier
Zenodo record by Nagy (record 19203285, 2026-03-24) claims finiteness for every N; only its title and
dates were read, and it is unvetted [V for title and dates]. Tomar also
claims uniqueness of the strictly convex four-body configuration (arXiv:2609.35632, v2 2026-10-29)
[V]. No n = 6 result located [U]. Overlap: the value of our n = 5 tropical replication and of the
round-54 certified atlas of the doubly symmetric five-body cross is superseded if these claims hold.
OpenAI Math: none. Plan: hold; strategic review; candidate redirect to an independent replay of the
Tomar certificates and Lean proof, or gate the problem.

**`unsplittable-flow-cost`** (last pass 2026-07-25, the oldest). External: Goemans' cost conjecture
is false on Rybin's instance (announced 2026-07-22) [V2]; formalized in Isabelle/HOL as an AFP entry
[V]. New: Afrasyab arXiv:2609.17568 (realizations of independence systems by zero-cost choices,
odd-cycle thresholds, C5 value 79/120) [V]; Bérczi, Liu, Reis, Tarnawski arXiv:2608.13983
(2026-08-14) disprove a Morell-Skutella conjecture on weighted equitability (their numbering) [V];
arXiv:2610.16079 on cost-preserving rounding [V2, unread]. Overlap: 16/15 and the separation LP
optimum 2/7 are not stated in these sources [V]; the threshold method of arXiv:2609.17568 overlaps
partly in style. Our statement that Morell-Skutella Conjecture 1.4 falls must be checked against the
numbering in the 2022 paper and the Bérczi et al. result. Plan: hold; refresh the dossier before EXP-005.

**`navier-stokes`** (last pass 2026-09-18). External: the Clay problem is open; the OpenAI forced
blowup (2026-09-08) is unrefereed [V2]. New: Bastounis, Circelli, Hansen, arXiv:2610.08144
(2026-10-06): the Lean proof does not correspond to the natural-language blowup proof [V, re-checked];
Alpoge, Buckmaster, Coiculescu arXiv:2609.16470 (forced IPM blowup with smooth force) [V];
Cao-Chi-Nie arXiv:2609.10262 (density of blowup forces) [V]; Petrillo-Glimm arXiv:2609.23868 [V];
Cheskidov-Dai-Palasek arXiv:2609.26790 [V]. Overlap: our Lean audit checked the statements, which
remains consistent with a proof-correspondence gap; the manuscript must cite and scope against
arXiv:2610.08144. No source states our class ceiling [U]; the nearest quantitative value is the
hypodissipative threshold (22-8*sqrt(7))/9 of arXiv:2407.06776 [V2]. Plan: one citation and scope
revision (v0.09), the bounded comparison of that threshold with the class ceiling, then dormant.

**`riemann-hypothesis`** (last pass 2026-10-08; research paused by Felipe on 2026-10-04). External:
open. New: Wang arXiv:2609.24167 was withdrawn on 2026-10-06 ("New method is need to obtain good
improvement") [V, re-checked]; Wang arXiv:2609.07918 has a v2 of 2026-10-06 with onset 0.5501 [V];
arXiv:2609.33043 v2 (2026-10-07, distinct zeros, global) [V]; Liu arXiv:2610.26835 (zero-free half-plane
Re s > 0.874886647 for Hecke L-functions) [V]; Ye arXiv:2610.15989 (short strips, uses the
quasi-Riemann results) [V]; expert reception of the OpenAI quasi-Riemann claim reported by Quanta on
2026-10-19 [V2]. Overlap: none below our internal onset 0.5339 [V]; our records already position
the onset against Wang's short-interval theorem. Plan: no research restart; one correction review
is open (section 3).

### Proposed and scoped rows

| Row | External status 2026-10-30 | Assessment |
|---|---|---|
| `hoa-mnh` | Disproved for every order n >= 56 (Zhan, arXiv:2608.00957v3); least order open in [8,56]; Questions 2 to 4 open; no follow-up [V] | Open next (rank 3). |
| `boij-soderberg-realizability` | Questions 6.1 and 6.2 answered negatively (arXiv:2605.25259v2, 2026-05-28); no follow-up [V] | Open after `hoa-mnh` (rank 6). |
| `sphere-log-energy` | Smale 7 open [V2]; C_log bracketed in [-0.0568456, -0.0556053] [V]; OpenAI family 090 (2026-09-23) claims C_log equals the Brauchart-Hardin-Saff value, unrefereed [V]; Gariboldi-Gigante arXiv:2609.39825 [V] | Re-scope to the algorithmic side or to an independent interval check before opening. |
| `hilbert-16` | OpenAI family 143 (2026-09-24) claims a uniform bound on limit cycles per degree, no Lean for the headline, no expert reaction found [V]; companion: at most two limit cycles for quintic Liénard systems, with Lean [V] | Finiteness is no longer a target; only lower-bound certificates remain. |
| `linear-programming` | Smale 9 open; 2026 progress on circuit diameter (arXiv:2602.06958) and a two-nonzeros class (arXiv:2610.26073) [V] | Keep proposed. |
| `diophantine-2var` | Two unknowns open; undecidability over Z claimed for 10 unknowns (arXiv:2609.01594) [V] | Keep proposed; low value. |
| `bsd` | Open; OpenAI families 002 and 006 claim BSD for Selmer corank at most 1 and Goldfeld, unverified [V] | Do not open. |
| `p-vs-np` | Open [V2] | Do not open. |
| `hodge` | Open; OpenAI family 032 claims rational Hodge for CM abelian varieties, three related manuscripts withdrawn 2026-10-07 [V] | Do not open. |
| `yang-mills-mass-gap` | Open; an OpenAI existence claim (2026-10-26) without mass gap, artifacts withheld for a review panel [V2] | Do not open. |
| `centralizers` | C^1 settled; C^r for r >= 2 open; no 2026 result [U] | Do not open. |

## 3. Record actions this review triggers

| Problem | Action | Gate |
|---|---|---|
| `huneke-wiegand` | Amend the EXP-067 novelty statement: the ideal transfer is García-Sánchez and Leamer (2012) Proposition 10 and Theorem 13; record HWB-094 as a corollary disposition | Problem round |
| `riemann-hypothesis` | Correction review: `sharp-three-point-kernel` v0.01 transfers a global proportion through Wang's arXiv:2609.24167v1 framework, withdrawn on 2026-10-06; re-read the Wang arXiv:2609.07918v2 pair theorem used by the EXP-010 onset | Felipe's pause: a publication correction, not an experiment; needs his go |
| `jacobian-conjecture` | Record Helali, Guo, Long, de Bondt, Kanel-Belov and Fedorov; mark the 48-variable witnesses as superseded in dimension | Problem round |
| `central-configurations` | Record the three arXiv five-body claims, the unvetted Nagy Zenodo record and the convex four-body claim; strategic review | Problem round |
| `navier-stokes` | Cite and scope against arXiv:2610.08144 in v0.09 | Problem round |
| `unsplittable-flow-cost` | Refresh the literature dossier; check the Conjecture 1.4 numbering | Problem round |
| program | Status board and `portfolio.yaml` reconciled with the problem records (Riemann published, Bougard-Joret consolidating, Petersen exploring since 2026-10-06) | Done in this branch |

## 4. Non-claims

This review settles no mathematical question. External claims listed as claimed are unrefereed
unless stated. Ranks are a program decision about where to spend the next rounds, not a judgment of
mathematical importance.
