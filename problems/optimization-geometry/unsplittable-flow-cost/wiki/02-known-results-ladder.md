# 02 - The known-results ladder

Transcribed from `../context/2026-07-24-literature-status-dossier.md`, which holds the
per-claim verification tags and the source hashes. Nothing here is recalled from memory.

## The four statements people mean

| Label | Bounds on $f^{\mathcal{P}}(a)$ | Cost clause | Acyclic required |
|---|---|---|---|
| DGG theorem (1999) | $\le x(a) + d_{\max}$ | no | no |
| Goemans Conj 1.2 | $\le x(a) + d_{\max}$ | $c^T f^{\mathcal{P}} \le c^T x$ | no (WLOG yes) |
| Conj 1.3 (Morell-Skutella 2022 Conj 1); FALSE, Bérczi et al. 2026 Thm 17 | $x(a) - d_{\max} \le \cdot \le x(a) + d_{\max}$ | no | yes |
| Conj 1.4 (Morell-Skutella 2022 Conj 2); FALSE | $x(a) - d_{\max} \le \cdot \le x(a) + d_{\max}$ | $c^T f^{\mathcal{P}} \le c^T x$ | yes |
| Conj 1.5 | $x(a) - 2d_{\max} \le \cdot \le x(a) + 2d_{\max}$ | $c^T f^{\mathcal{P}} \le c^T x$ | yes |

Labels follow arXiv:2510.21287, so that our record and the literature can be compared line
by line. [VERIFIED] Morell and Skutella's own paper (Math. Program. 192 (2022)) numbers the
two-sided conjectures 1 (no cost) and 2 (with cost); 1.3 and 1.4 are STVZ25's labels, tagged
"[MS22]" there. [VERIFIED 2026-11-07]

Implications, all elementary and re-derived by us: Conj 1.4 implies Conj 1.3 (drop the
cost clause) and Conj 1.4 implies Conj 1.2 (drop the lower bounds; Goemans is acyclic
without loss of generality, by cancelling flow on cycles and deleting zero-flow arcs).
STVZ25 Theorem 1.6 adds the non-trivial implication: Conj 1.3 implies Conj 1.5. [VERIFIED
for Thm 1.6; [D] for the elementary ones] Since 2026-08-14 Conj 1.3 is known to be false
(Bérczi, Liu, Reis, Tarnawski, arXiv:2608.13983, Theorem 17: for every k >= 4 a single-source
DAG with max demand 8k where every unsplittable flow deviates by at least 9k - 3 =
(9/8 - 3/(8k)) d_max on some arc), so Theorem 1.6 no longer gives a route to Conj 1.5, which
stays open. [VERIFIED 2026-11-07]

## What is proved

| Result | Hypothesis | Guarantee | Source |
|---|---|---|---|
| Dinitz-Garg-Goemans | any instance | congestion-good, poly time | Combinatorica 19(1) 1999 |
| Skutella 2002 | demands all multiples of one another | Conj 1.2 in full | reported in STVZ25 and MSW25 |
| Lenstra-style | source plus two layers | Conj 1.2 | reported in TVZ24 |
| Morell-Skutella 2022 | any instance | the lower bound $f \ge x - d_{\max}$ alone | reported in TVZ24 |
| Morell-Skutella 2022 | demands all multiples of one another | Conj 1.4, hence 1.3 | reported in STVZ25 |
| Traub, Vargas Koch, Zenklusen | PLANAR, single source | Conj 1.5 (cost-good at $2 d_{\max}$), and Conj 1.3 | arXiv:2308.02651; Math. Prog. 2026 |
| Majthoub Almoghrabi, Skutella, Warode | SERIES-PARALLEL digraphs, general multiflows | Conj 1.4, hence Conj 1.2, in convex-combination form with STRICT deviation $< d_{\max}$ | arXiv:2412.05182v2; IPCO 2025 |
| Swamy, Traub, Vargas Koch, Zenklusen | acyclic | Conj 1.3 implies Conj 1.5 | arXiv:2510.21287 Thm 1.6 |
| same | weighted ring loading | cost guarantee at $\frac{13}{5} d_{\max}$ | arXiv:2510.21287 Thm 1.7 |

## What the 2026 counterexample changes

Conj 1.2 and Conj 1.4 move to FALSE, together with the convex-combination form; every
other row above stands, and each of the four rows that could conceivably have conflicted
with the counterexample was tested against it directly and found consistent (EXP-002,
tests C1-C9). [MV]

The class picture that results is unusually sharp:

- SERIES-PARALLEL (equivalently, $K_4$-minor-free): conjecture TRUE, with strict deviation.
- The first structure past that boundary, a $K_4$ subdivision: conjecture FALSE, witnessed
  by a 7-vertex instance.
- PLANAR: cost-good rounding possible at $2 d_{\max}$ (proved), impossible at $d_{\max}$
  (the counterexample is planar). The true planar constant lies strictly between.
- GENERAL: no finite constant is known at all, and whether $O(d_{\max})$ suffices is the
  open breakthrough target.

## What remains genuinely open

1. Does a cost-good routing always exist with violation $O(d_{\max})$? No finite constant
   is known outside planar graphs. This is the question the primary literature names as the
   breakthrough target, and a counterexample to the constant 1 does not touch it.
2. What is the exact frontier constant $\alpha^\*$, in general and for planar graphs?
   Known: $\alpha^\* \ge 16/15$ [MV, EXP-002], $\alpha^\*_{\text{planar}} \le 2$ [VERIFIED,
   TVZ24].
3. Conj 1.3 (Morell-Skutella 2022 Conjecture 1), the cost-free two-sided statement: settled
   false by Bérczi et al. 2026 (Theorem 17). The open questions it leaves are the right
   two-sided constant (Bérczi et al. ask for 2 d_max) and Conj 1.5 by another route.
4. How small can a counterexample be? Nothing is published on minimality.
