# EXP-107: First three-parameter graded chart lift

## Question

After adding \(v=\varepsilon_{(0,7)}\), do finitely many graded maximal minors
cover the full \((u,v)\)-surface above the EXP-101 residual curve?

## Invariant coordinates and bounds

EXP-106 gives \(w_v=8\) in its stored convention, so \(v\) transforms with
weight \(1\). Set

\[
z=u^9,\qquad y=v/u.
\]

The new scaled matrix term is \(u^8yA_v\). Assignment bounds show \(z\)-width
14 for both existing charts. The \(y\)-degrees are bounded by the modular
direction ranks 53 and 41.

## Pilot

1. Reconstruct the first two determinant polynomials over
   \(\mathbb F_{998244353}[z,y]\) on 16-by-64 NTT grids.
2. Verify their restrictions at \(y=0\) are the exact EXP-105 polynomials.
3. Factor and compute their common-zero ideal. Coprimality alone is not enough
   in two variables.
4. If the ideal is nonempty, select new point-local row charts on each
   residual component and iterate, with a four-chart stop condition.
5. Repeat any unit-ideal decision at a second prime and lift a compact exact
   certificate before making a characteristic-zero claim.

## Decision boundary

A modular unit ideal is a pilot result until endpoint preservation and exact
lifting are supplied. A nonempty modular residual is an explicit next chart
locus, not evidence for a counterexample.

Declared 2026-07-26 after EXP-106 and before implementation.
