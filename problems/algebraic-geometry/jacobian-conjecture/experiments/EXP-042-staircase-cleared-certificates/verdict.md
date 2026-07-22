# EXP-042 - Verdict: CONFIRMED (prediction 2 refuted as declared, replaced by a cleaner law); THEOREM 5 in window form (2026-07-22)

Artifacts: `artifacts/output-AB-2026-07-22.txt`, `artifacts/output-CD-2026-07-22.txt`.

## Findings

1. **Cleared certificates across the grid [MV].** Every (u, v, d) grid point has a
   POLYNOMIAL covector with c^T M = 0 verified identically and a MONOMIAL pairing:
   -13860 a^7, -32 a^4, -630 a^4, -2730 a^7, -1155 a^3, -165 a^4 (b-free: exclude every
   b), -4620 a^7 b and -81 b^4 (the b factor vanishes only at b = 0, which is Theorem 1
   territory anyway). Combined with Theorem 1 at b = 0: **THEOREM 5 (window form): for
   every grid (u, v, d) and window N = 7, P = x + a x^u y^v + b x^d admits no Keller
   partner of degree <= 7, for ALL parameter values with a != 0.** Sound at every point
   (polynomial identities, no generic steps).
2. **Window law [MV; declared prediction 2 REFUTED, replaced].** The declared guess
   (same pairing form at every window) is false; the measured law is cleaner: at
   (2, 1, 2) the pairing at window N is -c_N a^N with c_N a positive integer
   (420, 1260, 13860, 180180, ... at N = 5..9): a nonzero monomial in a alone at EVERY
   window. Emptiness therefore holds at every certified window for all parameters; the
   growing exponent is the certificate absorbing more staircase depth per window,
   the analog of Theorem 1's chain products.
3. **The annihilation machinery transfers verbatim [MV].** J(m, P^k) = -k L(P^{k-1} m)
   holds on the family (pure Leibniz, P-agnostic), and the certificate pairing of a
   source vanishes exactly when the preimage fits the window (4/4 spot grid). Both
   closure ingredients of the Theorems 2-4 tail machinery are available for the
   staircase family.
4. **General tails [MV].** Multi-term above-weight tails: sampled windows all EMPTY;
   the cleared certificate extends to the 3-parameter family x + a x^2 y + b x^2 +
   c3 x^3 with monomial pairing -27720 a^7 c3^4.

## What remains for the all-degree THEOREM 5

The single missing piece is the closed form of the transport chain (the analog of
EXP-029's banded formula): a proof that the constant-class reduced equation is
(nonzero) * a^N at EVERY window, not just the certified ones. The structure evidence
(window law exponent = N; annihilation transfer) makes this the precise target of the
next JCB-038 step; until then Theorem 5 stands in window form with sound all-parameter
certificates.

## How could this be wrong?

- Window form only (declared); windows to 9 (and 7 on the grid).
- The two b-involving pairings rely on Theorem 1 for their b = 0 locus (stated).
