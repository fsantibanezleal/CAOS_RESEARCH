# hoa-mnh history

## 2026-11-06 - opened

External status: Hoa's conjecture is disproved for every order n >= 56 (Zhan, arXiv:2608.00957v3, still v3); the
least counterexample order is open in [8, 56]; Zhan's Questions 2-4 are open; no follow-up on arXiv [V].
- Opened from the 2026-09-02 dossier and the 2026-10-30 portfolio review (rank 3).
- Primary sources re-fetched to the data root with SHA-256 (the dossier's copies were under a temp path that no
  longer exists).
- Plan: exact census of MNH graphs by order (EXP-001), then the gadget search through Bullock et al. Theorem 3.13.

## 2026-11-06 - EXP-001 confirmed: no counterexample through order 11; A185306(11) = 67

- Hypothesis frozen before computation (6252044e). Exhaustive: nauty geng over every connected graph of order
  3 to 11 (1,006,700,565 at order 11, equal to OEIS A001349), exact filter `mnh.c` (degree-sum prune, Hamilton
  paths by subset dynamic programming, every longest-cycle vertex set).
- MNH counts 1, 1, 3, 3, 7, 9, 18, 31 for n = 3..10 (A185306 reproduced) and **67 at n = 11** (new term).
- Hoa's conjecture holds for every MNH graph of order <= 11 and every longest cycle, so the least counterexample
  order is in [12, 56]. No witness for Zhan's Questions 2 or 3; f(n) = 1 for 4 <= n <= 11.
- Independent backtracking re-check (`verify.py`) of all 139 MNH graphs of orders 4 to 11: 0 disagreements.
- Order 12 not run: it extrapolates to about 29 hours, over the frozen 12-hour stop condition (HMB-005).

## 2026-11-06/07 - EXP-002 (order 12) and EXP-003 (gadgets) confirmed

- Problem 266 (Discrete Math. 164 (1997) 317-321) obtained and archived: posed by Hoa as a question; the
  attribution is settled (HMB-003, partial: Hoa 2005 not obtained). Zhan v3 HTML re-read: no new content.
- EXP-002 (hypothesis 1de9ac88): order 12 by the maximum-degree split (Goedgebeur-Neyt-Zamfirescu Corollary 12):
  K_1 join every graph on 11 vertices (1,018,997,864 = A000088(11); 114 MNH) and maximum degree <= 8 with the
  degree-sum-pruned generator (5,705,422,732 graphs; 37 MNH). **A185306(12) = 151**; Hoa's conjecture holds at
  order 12, so the least counterexample order is in [13, 56]. Split gate reproduces 31 and 67; independent
  re-check of all 151 graphs; 16 random case-B parts re-run after a WSL restart, counts identical.
- EXP-003 (hypothesis c25531a4): every gadget (X, x) from the MNH graphs of order <= 12 (2,796 gadgets) has only
  clique omitted sets on its longest middle paths, so no Zhan-type counterexample comes from them; any
  Zhan-type counterexample has order >= 32. Gate: the code recognises Zhan's own gadget (A_18, d = 2, omitted
  {16, 17}).
