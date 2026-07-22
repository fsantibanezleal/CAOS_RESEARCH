# EXP-043 - First contact with the live frontier: the GGV B = 16 shape and the (72, 108) scoping

- **Question.** JCB-040. The recalibrated frontier (EXP-040) is GGV's B = 16 normal form
  (J. Algebra 471 (2017): directions {(4,-1), (-2,1), (-1,-1), (0,-1)};
  l_{4,-1}(P) = lambda_P R0^m with R0 = x (x y^4 - lambda_0)^3;
  l_{-2,1}(P) = lambda_P R1^{4m} with R1 = y (x y^2 - lambda_1)) and the lone surviving
  pair (72, 108). Can our instruments engage these shapes, and what does a full attack
  cost?
- **Motivation (derivation, declared).** For an x^m-anchored edge E = x^m phi(z),
  z = x^k y^l, the chain rule gives the MULTIPLICATION formula
  J(E, x^alpha y^beta) = x^{m+alpha-1} y^{beta-1} [beta m phi(z) + (beta k - alpha l) z phi'(z)],
  generalizing Theorem 3's operator (the case m = 1). R0^m has exactly this shape
  (x^m psi(z), z = x y^4, psi = (z - lambda_0)^{3m}). Consequences to test: (i) for
  m >= 2 no polynomial monomial reaches the constant from the R0^m edge (output needs
  alpha = 1 - m < 0): the constant must travel the lower boundary, i.e. the B = 16
  problem IS a staircase-transport problem; (ii) the pure m = 1 shape has x as a
  Newton-polygon vertex (support (1,0), (2,4), (3,8), (4,12), no pure x^d), so THEOREM 4
  excludes it as a Keller component outright; swallowed variants (with x^d fillers) fall
  into EXP-037 territory.
- **Falsifiable predictions.**
  1. [MV] (Structure) R0 is (4,-1)-homogeneous of weight 4 with collinear x-anchored
     support; R1 is (-2,1)-homogeneous of weight 1; R0^m and R0^n are Jacobian-dependent.
  2. [MV] (The x^m edge operator) The multiplication formula holds identically in
     symbolic edge coefficients on a grid of (m, k, l) and (alpha, beta).
  3. [MV] (Constant unreachable for m >= 2) On the grid, J(R0^m, x^alpha y^beta) has a
     nonzero constant term only when m = 1, alpha = 0, beta = 1 (where it is
     -lambda_0^3 times a nonzero integer): for m >= 2 the top edge cannot make the
     constant: the B = 16 core is a staircase transport.
  4. [MV] (Our theorems bite) The pure m = 1 sample P = R0/(-lambda_0^3) (normalized
     linear part, lambda_0 = 1) has an EMPTY completion window (Theorem 4 replication);
     swallowed variants (plus x^2 or x^3 fillers) also have EMPTY windows (EXP-037
     territory extended to the B = 16 shape).
  5. [D] (Scoping) Exact per-class block-size histograms of the transport decomposition
     for the (48, 64) attack (grading (4,-1)) and the (72, 108) attack (leading
     direction from GGHV's ((8,28),(3,2)) data): the largest diagonal block stays in the
     low hundreds, so the classwise attack is compute-feasible; numbers recorded.
- **Method.** sympy over QQ with symbolic lambda; window solves at N = 8 on degree-16
  shapes (window system rows grow with deg P: keep N modest); combinatorial block
  counts. Caps 570 s per part.
- **Success criterion.** 1-4 verified; 5 tabulated: JCB-040 gets its instrument map and
  cost estimate; the B = 16 core is formally identified as staircase transport.
- **Failure criterion.** The multiplication formula fails (derivation wrong); a
  consistent window on the B = 16 samples (candidate component: escalate immediately).

Declared 2026-07-22 before the run.
