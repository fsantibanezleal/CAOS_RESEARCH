# EXP-046 - Verdict: CONFIRMED; THE TOWER LEMMA IS PROVED (primitive-top scope); THEOREM 5 IS UNCONDITIONAL there (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`, `artifacts/output-D-2026-07-22.txt`.

## The proof, assembled (each step machine-verified)

1. **Bookkeeping [MV].** Old columns have zero entries on the new rows (outputs of degree
   <= N + deg P - 2), so a window-N certificate extended by new-row entries stays
   left-null on the old columns automatically.
2. **The top block [MV].** The new-rows x new-columns block is the action of the
   TOTAL-DEGREE top form T of P; its kernel at degree N + 1 is exactly the span of the
   predicted resonances (at (2,1,2), the single B-power (x^2 y)^3 at degree 9).
3. **The key identity [MV + one-paragraph derivation].** Every resonance kappa is
   lambda (P - low)^k with low the sub-top tail of P; hence kappa - lambda P^k is
   supported in degree <= N (checked exactly in all three regimes d < u+v, d = u+v, and
   the B-power cases), and P^k is in ker L: so L(kappa) is the L-image of an IN-WINDOW
   polynomial (rank test confirms), which every left-null certificate annihilates.
4. **The extension, realized [MV].** Across the ACTIVE resonance step 8 -> 9 at
   (2,1,2), the window-9 certificate restricts to the window-8 one on all 52 common rows
   with the single ratio 2 and pairing ratio 2: the extension exists exactly as the
   derivation constructs it, and the pairing (hence inconsistency) is preserved.

**THE TOWER LEMMA.** For P = x + a x^u y^v + b x^d with T primitive (a monomial x^u y^v
with gcd(u, v) = 1) or d >= u + v (T = P - x or T = b x^d): window inconsistency with a
certificate at any base N >= deg P - 1 propagates to every larger window.

**THEOREM 5 (UNCONDITIONAL on that scope).** Combining the lemma with EXP-042's sound
base certificates: for those (u, v, d), P = x + a x^u y^v + b x^d is NEVER a Keller
component, at any partner degree, for every parameter value with a != 0. The first
all-degree exclusion of an above-weight (staircase) perturbation: staircase length 2
falls.

## The remaining proper-power scope

For T a proper power (e.g. u = v = 2: T = a (xy)^2), the kernel also contains odd powers
(xy)^s that do NOT reduce mod C[P]. Measured: the certificates kill them anyway (the odd
resonance (xy)^5 at N = 9 and the even (xy)^6 at N = 11 both pair to zero). Theorem 5
holds there at [D] pending the derivation of the odd-resonance kill (the working
hypothesis is class-support disjointness; queued as the lemma's last case).

## How could this be wrong?

- The kernel identification (step 2) uses the dependence classification of binary forms;
  machine-checked at tested degrees, classical in general.
- The extension argument needs SOME certificate at the base window; EXP-042 supplies
  cleared, all-parameter ones for the whole grid.
