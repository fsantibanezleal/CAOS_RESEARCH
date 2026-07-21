# EXP-028 - The strategy shift: from windows to the polygon argument (all degrees)

- **Question.** Can the window-by-window certificate program be replaced by an ALL-DEGREE
  structural argument for pure slices? The route: the classical Newton-polygon similarity
  theory for Jacobian pairs (Abhyankar line; van den Essen Ch. 10) says a partner's polygon
  must be similar to P's with ratio n/m; for P = x + a h^2 (h = x^p y^q, p != q) the scaled
  vertices (n/m)(1,0) and (n/m)(2p,2q) must be lattice points, which fails for almost all n.
  If the argument holds, P = x + a h^2 is NEVER a Keller component at ANY partner degree:
  an all-degree statement the windows can only approximate.
- **Motivation (the strategy evaluation Felipe asked for).** Window certificates have a
  structural ceiling (fixed N per run) and their single-pairing phenomenon (every window,
  25 to 700 unknowns, yields exactly ONE obstruction) suggests one canonical obstruction
  exists. The polygon calculus is the candidate closed form of that obstruction. This
  experiment (a) mechanizes the lattice-similarity necessary condition, (b) tests its
  sharpest prediction against the machine, and (c) extracts the certificate vectors' support
  structure as data toward identifying the obstruction functional.
- **Falsifiable predictions.**
  1. [MV] (The lattice sieve) Mechanically enumerating n <= 60 for m = 18 (h = x^4 y^5):
     the similarity condition admits lattice vertices ONLY when 18 | n; for m = 24
     (h = x^5 y^7), only when 24 | n. (Pure arithmetic, machine-enumerated.)
  2. [MV] (The decisive window) The (18, <= 36) completion window, which CONTAINS the first
     admissible rung n = 36, is nevertheless EMPTY (numeric a samples): divisible-rung tops
     Q_top proportional to (P_top)^2 still fail to complete. This is the prediction that
     separates "the sieve explains the data" from "something deeper blocks everything".
  3. [MV] (Certificate) The (18, <= 36) exclusion certifies for ALL a != 0 (pure a-power
     pairing gcd), extending EXP-026's window past the first divisible rung.
  4. [MV] (Obstruction anatomy) The certificate vectors at (4, <= 6) and (4, <= 10) have
     structured support: the weighted rows concentrate on a small set of equation degrees
     (recorded as data; a closed-form functional is conjectured [C], not claimed).
  5. [C, gated on primary sources] The similarity theorem's exact statement and hypotheses
     (does it apply when one component may be a coordinate?) are fetched from the
     Newton-polygon literature; until verified, the all-degree conclusion stays labeled [C]
     with the windows as its machine-verified shadow.
- **Method.** sympy: lattice enumeration (exact rationals); the certificate instrument
  unchanged (caps 570 s); certificate-vector extraction with support statistics; a targeted
  primary-source fetch for the similarity theorem and Moh's coverage claim (JCB-031).
- **Success criterion.** 1-2 verified (3 certified or capped honestly; 4 recorded); 5
  resolved to a precise citation or an explicit UNVERIFIED flag.
- **Failure criterion.** Prediction 2 fails, i.e. the divisible rung IS consistent: then a
  completion exists at (18, 36), the all-degree conjecture dies, and the completion goes to
  the checker immediately (a potential coordinate, or far more).

Declared 2026-07-21 before the run.
