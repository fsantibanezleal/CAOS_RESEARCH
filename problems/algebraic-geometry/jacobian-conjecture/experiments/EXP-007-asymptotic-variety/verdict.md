# EXP-007 - Verdict: CONFIRMED (2026-07-20)

Output: `artifacts/output-2026-07-20.txt`. All five predictions verified exactly.

## Established results (ours, exact)

1. **Escape = multiple fiber root (family theorem).** In the potential form,
   W'(w) = k^2 p(w) - BC identically, and the reconstruction scale is s = -W'(w)/m. Hence a
   fiber root fails to reconstruct (preimage escapes to infinity) precisely when it is a
   MULTIPLE root of the fiber polynomial W. Sheets merge exactly at infinity, never at finite
   points: the discriminant locus of W is the non-properness locus over C != 0. Verified for
   the announced F and the P3 instance.
2. **The asymptotic variety of F, explicitly:**
   A(F) = {C = 0} union {27 A^2 C^2 - 18 A B C + 16 A + B^3 C - B^2 = 0}
   (the discriminant surface; disc_w(W) = -16 C^2 (27 A^2 C^2 - 18 A B C + 16 A + B^3 C - B^2)).
3. **A concrete escape, end to end.** The target (0, 1, 1) lies on the discriminant surface
   (built by imposing s(1/2) = 0); its EXACT fiber is the single point (2, -1/2, 9/8): two of
   the three sheets escaped, and the surviving point is the one the reconstruction predicts.
4. **The plane C = 0 is asymptotic with a flat-sheet remainder.** Over generic (A, B, 0) the
   exact fiber is exactly one point, (0, B, A - 4B^2), on the flat sheet x = 0; both curved
   sheets escape. Verified at two rational targets.
5. **Collisions are generic, not asymptotic.** The EXP-004 collision target (-16, -16, 1) has
   D = 36864 != 0 and a full 3-point rational fiber; both engineered collision points are in it
   (third point: (1/24, -28, -10656)).

## Adversarial validation record

- The discriminant characterization is proved as a polynomial identity (route 1), then
  stress-tested on targets ON and OFF the locus with independent Groebner fiber computations
  (route 4): predictions in both directions (deficient vs full fiber) confirmed.

## How could this be wrong?

- "A(F) = discriminant locus" is established over C != 0 via the reconstruction bijection
  between simple fiber roots and finite preimages; targets where the correspondence could
  degenerate other than by multiplicity (leading coefficient of W in w) do not exist here since
  the leading coefficient is the nonzero constant k^2 phi_{d+1}.
- Dimension/irreducibility statements about the surface were not asserted, only computed
  membership and fiber counts.

## Consequences

- JC-P2 core done: the geometry of the failure is now a named, explicit surface; Kraus's
  "ramification at infinity" is, for this family, the discriminant of a univariate polynomial.
- The surface (a low-degree affine surface in (A, B, C)) is an ideal web-app visualization
  artifact (real slice + escape animation), queued with M3.
