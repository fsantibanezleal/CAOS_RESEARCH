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

## 2026-11-19 - literature pass absorbed; EXP-001 and EXP-002 frozen

- Literature pass (four lanes, twelve items re-read by skeptics; [context note](../context/2026-11-19-literature-pass.md)):
  16 primitive points of the dossier's undecided list are realized by printed sources or by scaling (Macaulay2
  documentation outputs over ZZ/101; Soderberg's extremely compressed level modules); c_d = 2 on (0,4,9,10) and
  (0,1,6,10); over U(H) the Kostant modules L(p,q) of sp_4 realize eleven primitive points in characteristic 0;
  Boocher-Huang-Wolf (arXiv:2512.24320, December 2025) describe the rays with B1 = 2, of which (0,6,20,21) is the second.
  Four claimed items did not survive the skeptics (Pieri candidates, a purity reading of relatively compressed
  algebras, a tool limitation, a lane's reading of the gcd restriction).
- Derived by hand, before any machine run: U(H)/U(H)(x^2, y^2) has Hilbert function (1,2,2,2,1) and the pure resolution
  (1,2,2,1) of type (0,2,6,8) when 6 is invertible (written in the EXP-002 hypothesis).
- EXP-001 (the table over S) and EXP-002 (the three rays left open over U(H), the family U/U(x^e, y^e), calibration and
  duality) frozen before computation.

