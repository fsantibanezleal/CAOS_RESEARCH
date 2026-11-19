# boij-soderberg-realizability history

## 2026-11-19 - opened

External status: Erman-Sam Questions 6.1 and 6.2 are answered negatively by the Rethlas paper (arXiv:2605.25259, still
v2 of 2026-05-28), with one primitive point each; no follow-up found in the external refresh of 2026-11-19 [V].
- Opened from the 2026-09-02 dossier and the portfolio review of 2026-11-19 (rank 1, decision 1; the 2026-10-30 order
  "open after hoa-mnh" is met).
- Thirteen arXiv sources and the two Rethlas raw outputs fetched to the data root with SHA-256 (the dossier's copies and
  its census scripts were under a temporary path that no longer exists).
- Toolchain checked: Macaulay2 1.22 in WSL; `pureBetti {0,4,9,10}` returns {1, 3, 8, 6}, `pureBetti {0,1,6,10}` returns
  {6, 8, 3, 1}, `pureAll {0,4,9,10}` returns (70, 70, 15).
- Plan: the realizability table of the 220 rays with d3 <= 12 (EXP-001: census, closures, random search), then U(H)
  toward the smallest counterexample to Question 6.1.
