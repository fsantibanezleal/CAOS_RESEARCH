# EXP-045 - Verdict: CONFIRMED; the filter is a x19 multiplier and (48, 64) is now small (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`.

## Findings

1. **The divisibility one-liner [MV].** J(x^m psi(z), Q) is divisible by x^{m-1} for
   m >= 2 (symbolic psi, grid): the pure GGV leading form R0^m alone is never a Keller
   component, at any degree, trivially. The frontier content is entirely in the lower
   classes, as EXP-043 concluded.
2. **Degree-32 exclusions [MV].** P32 = x + R0(1)^2 (support (1,0), (2,0), (3,4), ...,
   (8,24): a genuine swallowed staircase of the B = 16 flavor at degree 32) has EMPTY
   completion windows at N = 12, 16, 20 (88, 150, 228 unknowns): new mid-scale machine
   certificates on frontier-flavored territory.
3. **Filter soundness on knowns [MV].** The similarity filter (partner supported in the
   (deg Q / deg P)-scaled polygon N^0(P)) keeps every true partner monomial on the
   tested library pairs.
4. **THE FILTER VALUE (JCB-043's declared test) [MV].** On P32 at admissible partner
   degree 48: 1222 unknowns drop to 65 (5.3 percent kept, x18.8). On the (48, 64) shape:
   2142 drop to 111 (5.2 percent). The filtered window preserves the emptiness verdict
   (N = 16 on P32: 33 unknowns, EMPTY). Prediction said "at least 2x"; the truth is
   nearly x19.

## What this changes

- The (48, 64) validation sweep (route N2) is no longer a compute project: with the
  similarity filter the full-window system has ~111 unknowns; combined with the
  classwise transport (largest block 13) it is a SMALL exact computation. Same for
  (72, 108) by scaling (5992 unknowns filter to a few hundred at most; to be measured
  when the shape data is transcribed).
- JCB-043's value test is passed decisively; the remaining M1 work is importing the
  FURTHER literature filters (GGHV lower-left chains, Makar-Limanov trapezoids) only if
  the similarity filter alone proves insufficient somewhere.

## How could this be wrong?

- The filter encodes similarity for the polygon WITH origin (vdE 10.2.1 convention,
  both degrees > 1); pairs with a degree-1 member are exempt (they are automorphisms
  anyway); soundness is verified on library pairs of degrees (2,2) and (4,4) only, and
  the convention question for exotic supports is flagged.
- P32 is a sampled shape (lambda_0 = 1, no extra lower terms); the systematic sweep over
  lower-class terms is the actual N2 run, now scheduled as small.
