# EXP-048 - Verdict: CONFIRMED with prediction 3 refuted-as-declared; the HALF-PLANE mechanism found (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`.

## Findings

1. **The operator form [MV].** L((xy)^s) = s x^s y^{s-1} (1 + 2bx) identically: every
   odd-resonance source is X-HEAVY (rows with i - j in {1, 2}).
2. **Not an image [MV].** rank([M | L((xy)^5)]) = 52 > 51 = rank(M) at N = 9: the key
   identity's mechanism cannot apply (as derived; ker L = C[P] and (xy)^odd does not
   reduce).
3. **Prediction 3 REFUTED as declared; the truth is existential [MV].** The left-null
   space at N = 9 is 20-dimensional with TWO pairing-nonzero certificates; one kills
   the resonance, one does not. The corrected statement, measured at both resonances:
   THERE EXISTS a pairing-nonzero certificate that kills, and its support is entirely
   in the Y-HEAVY half-plane {i < j} (e.g. rows (1,2), (1,4), ..., (3,8) at N = 9),
   disjoint from every x-heavy source. At N = 11 both pairing-nonzero certificates
   kill.
4. **The mechanism, named: THE HALF-PLANE CERTIFICATE.** The transport constant-class
   chain (the Theorem-1 ray x^t y^{2t+1}-band) lives on the y-heavy side; when the
   y-heavy subsystem alone carries the inconsistency, its certificate extends by zeros
   and annihilates ALL x-heavy sources trivially, odd and even resonances alike. The
   remaining formalization (queued): the y-heavy subsystem is inconsistent for every
   proper-power-top family member (measured here; the class-ray structure makes it the
   natural conjecture), which would close Theorem 5's last case.

## What this changes

- The proper-power tower survives via half-plane certificates; Theorem 5's proper-power
  case stands [D] with the mechanism identified and machine-verified at the tested
  resonances. The frontier shapes (R0^m tops are proper powers) will need exactly this
  construction: the half-plane subsystem is the object to certify there.

## How could this be wrong?

- Two resonances tested; the half-plane inconsistency is measured, not yet derived.
- The half-plane cutoff choice ({i < j} here) may need shape-dependent tilting for
  general proper-power tops (the correct general statement is likely "the transport
  band's half-plane").
