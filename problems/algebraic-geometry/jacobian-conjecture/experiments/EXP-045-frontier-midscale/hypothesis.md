# EXP-045 - Frontier mid-scale: divisibility, degree-32 exclusions, and the filter value test (routes N2 + M1)

- **Question.** JCB-040/043. Move from scoping to running: real window certificates on
  B = 16-flavored shapes at degree 32, plus the measured value of the imported
  similarity filter.
- **Motivation (derivation, declared).** (i) For E = x^m psi(z) with m >= 2, both partial
  derivatives are divisible by x^{m-1}, so J(E, Q) is divisible by x^{m-1} for EVERY Q:
  the pure GGV leading form R0^m alone can never be a Keller component (one line; worth
  recording as the trivial base of the frontier analysis). (ii) The window system's
  unknown count depends on the PARTNER window, not on deg P, so mid-scale sweeps on
  degree-32 shapes are cheap: P32 = x + R0(1)^2 (support (1,0), (2,0), ..., (8,24)) is a
  genuine swallowed-staircase sample of the B = 16 flavor at degree 32. (iii) The
  Abhyankar similarity filter (Q supported in the (deg Q / deg P)-scaled polygon
  N^0(P)) should cut window unknowns substantially; its measured reduction is JCB-043's
  declared value test.
- **Falsifiable predictions.**
  1. [MV] (Divisibility one-liner) J(x^m psi(z), Q) is divisible by x^{m-1} for generic
     symbolic psi and arbitrary Q monomials; hence pure R0^m (m >= 2) is excluded
     trivially at every degree.
  2. [MV] (Degree-32 exclusions) P32 = x + R0(1)^2 has EMPTY completion windows at
     N = 12, 16, 20: new machine certificates on B = 16-flavored territory at degree 32.
  3. [MV] (Filter correctness) The scaled-polygon filter, applied to a genuine
     automorphism pair from the library, keeps its actual partner (the filter never
     excludes a true completion on tested pairs).
  4. [MV/D] (Filter value) On P32 at the similarity-admissible partner degree 48, the
     filter cuts the window unknown count by a measured factor (predicted: at least 2x;
     exact number recorded); same count reported for the (48, 64) system.
- **Method.** sympy over QQ; window solves (dense linsolve is enough at these unknown
  counts); a small exact convex-hull + half-plane lattice filter. Caps 570 s per part.
- **Success criterion.** 1-3 verified, 4 measured: the frontier program has a running
  mid-scale instrument and a quantified filter; the (48, 64) full sweep becomes a
  scheduling decision, not a research risk.
- **Failure criterion.** A consistent window on P32 (escalate: candidate component);
  the filter excluding a true partner (filter unsound: fix the polygon convention
  before any use).

Declared 2026-07-22 before the run.
