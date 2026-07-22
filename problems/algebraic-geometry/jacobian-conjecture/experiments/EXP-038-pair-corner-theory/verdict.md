# EXP-038 - Verdict: CONFIRMED; the pair adds structure, not depth (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`.

## Findings

1. **Top dependence and the common base [MV].** All 7 library pairs with deg sum > 2 have
   J(P_top, Q_top) = 0, proportional top radicals (the common base form), and identically
   vanishing top-2 classes of J(P, Q). The classical similarity picture is machine-exact on
   the library.
2. **The matched-pair law [MV].** The second class of J(P, Q) for cornered pairs
   (P = alpha B^p + P_sub, Q = beta B^q + Q_sub, B = x^i y^j) is EXACTLY
   alpha p (i b - j a) q_{a,b} - beta q (i d - j c) p_{c,d} summed over outputs, with
   monomials matched by (a, b) = (c, d) + (q - p)(i, j) (4 grids, term-by-term). The
   diagonal picture (EXP-035) extends to the pair level in closed form: Q's subtop is
   determined by P's subtop up to corner kernels and unmatched-monomial kills.
3. **The depth answer (the JCB-039 question) [MV].** On 4 cornered swallowed samples, the
   first-inconsistent window depth is IDENTICAL with Q free and with Q's top constrained
   to the similarity shape (N = 3 in all cases): the pair constraint contributes NO
   obstruction power beyond what the free-Q window already sees. Its real value is
   efficiency: at equal window the constrained system drops from 7 unknowns to 3-4
   (roughly half) on these samples, and the reduction grows with the window.

## What this changes

- JCB-039 is answered: the single-component staircase transport (EXP-037) is the right
  primary frame; pair-level structure is an instrument optimization (smaller windows for
  the same certificates), not a second obstruction source. The corner calculus needs no
  pair-level case analysis.
- The matched-pair law is worth keeping: it halves window sizes for future wide scans
  (beyond-floor bidegrees), and it is the exact bookkeeping needed if the transport
  certificates are ever run on the partner side.

## How could this be wrong?

- Depth comparison used 4 samples and windows up to 8; a shape where the pair constraint
  binds earlier could exist. The theory reason to doubt that (the constant is manufactured
  below the top; EXP-035 part B) is recorded, not proved.
- The matched-pair law is proved for monomial bases B; linear-base tops (rotatable case)
  are already covered by rotate-descent (EXP-034).
