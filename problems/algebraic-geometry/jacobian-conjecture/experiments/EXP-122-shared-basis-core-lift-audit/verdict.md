# EXP-122 - Verdict: no free lift, but one sparse direction ladder

Verdict: **confirmed exact activity audit; free-lift prediction refuted**.

## Result

The accepted exact run completed in 45.15 seconds. It reconstructed all 24
EXP-112 cyclic-core directions on the EXP-121 shared row basis and reproduced:

- the complete 302-by-125 augmented system;
- the identical \(L/Q\) shared row basis;
- the exact rational-anchor determinant at \((A,B,d)=(1,0,1)\); and
- the size-26 cyclic block of the fixed-\(d\), \(A/B\) graph.

There are 21 restored directions outside
\[
T_B=\{(0,1),(0,5),(1,0)\}.
\]
Their exact classification is:

| property | count |
|---|---:|
| determinant-inert on the one-parameter anchor line | 0 |
| support internal to the existing 26-block | 13 |
| enlarges the fixed-\(d\) cyclic SCC beyond 26 | 16 |
| nonzero first or pairwise mixed determinant coefficient | 21 |

The counts overlap: eight directions both act internally and enlarge the SCC.
The mutually exclusive primary labels are 13
`active_in_existing_26_block` and eight `scc_increasing`. No restored
direction is acyclic/off-block relative to the fixed-\(d\) graph.

Prediction 1 passed. Prediction 2 was refuted. Predictions 3 and 4 passed.

## Refutation of the free lift

For every restored direction \(D_i\), let
\[
K_i=M_\ast^{-1}D_i,\qquad
M_\ast=M(A=1,B=0,d=1).
\]
The run computed \(\det(I+tK_i)\) exactly from the cyclic diagonal blocks and
then checked it against direct exact 125-by-125 determinant ratios at
\(t=1\) and \(t=-1/2\).

All 21 factors are nonconstant. Therefore no restored core direction gives
\[
\det(M_\ast+tD_i)=\det(M_\ast)
\]
on its complete anchor line. The hoped-for trivial extension of the EXP-121
basis is unavailable.

This is a basis-local statement. It does not rule out a higher-dimensional
cover assembled from several row bases.

## The new structural pattern

The eight directions
\[
(2,j),\qquad 2\leq j\leq9,
\]
form one coherent class:

1. none has an edge internal to the existing 26-block;
2. each nevertheless enlarges the cyclic SCC;
3. each has a linear one-parameter determinant factor at the anchor.

Their factors are:

| direction | \(\det(I+tK_i)\) | enlarged SCC |
|---|---|---:|
| \((2,2)\) | \(1-3t/68\) | 36 |
| \((2,3)\) | \(1+6t/17\) | 36 |
| \((2,4)\) | \(1+3t/68\) | 36 |
| \((2,5)\) | \(1-31t/272\) | 36 |
| \((2,6)\) | \(1-3t/68\) | 36 |
| \((2,7)\) | \(1-3t/544\) | 36 |
| \((2,8)\) | \(1+3t/68\) | 35 |
| \((2,9)\) | \(1+3t/544\) | 34 |

Thus graph enlargement and determinant complexity separate sharply: adding
up to ten vertices to the cyclic block still contributes only a linear
factor on the anchor line.

Direction \((2,9)\) is the strongest next target. It has:

- the smallest selected direction rank, 53;
- the smallest normalized support, 1319 nonzero entries;
- the smallest enlarged SCC, 34;
- the linear line factor \(1+3t/544\); and
- nonzero mixed coefficients with every \(T_B\) direction:
  \[
  c_{(2,9),(0,1)}=\frac{303}{544},\quad
  c_{(2,9),(0,5)}=\frac{5}{544},\quad
  c_{(2,9),(1,0)}=\frac{15}{272}.
  \]

This direction was determinant-inert on the pinned \(T_A\) chart in EXP-114
but is immediately active on the EXP-121 shared chart. That complementarity
supports a multi-chart constructible cover rather than a search for one
universal basis.

## What this proves

- The EXP-121 shared basis has no trivial one-direction free lift among the
  other 21 cyclic-core parameters.
- Every restored direction is visible to the determinant by first order or
  pairwise mixed order at the rational anchor.
- The eight \(x\)-degree-two directions form an exact sparse ladder with
  linear anchor-line factors.
- \((2,9)\) is the smallest justified four-parameter symbolic-neighborhood
  target.

## What this does not prove

- No four-parameter restriction has been covered.
- Anchor-local derivatives do not prove nonvanishing on a symbolic
  neighborhood or on any residual component.
- The EXP-121 basis need not remain useful on the new exceptional divisor
  \(1+3t/544=0\).
- The result does not close the 24-parameter core, the full 51-parameter
  family, \((72,108)\), the planar degree floor, or \(JC(2)\).

## Adversarial validation

- The exact anchor determinant matches EXP-121 byte-for-byte as an integer.
- The active direction labels match the EXP-112 24-direction prefix exactly.
- The size-26 regression uses precisely the EXP-121 fixed-\(d\) \(A/B\)
  graph. Attempt 001 incorrectly included the \(d\)-tangent, stopped at the
  assertion, and is preserved under `artifacts/attempts/`.
- Every one-parameter factor was independently evaluated through the original
  selected matrix at two nonzero rational values.
- All 72 trace pairings were recomputed in both orders and agreed exactly.
- The accepted artifact has SHA-256
  `8FFF9A859845E0E7E359BABA72CDD3A1A1D60301634546E564ED585AD05E7A8F`.

## How could this be wrong?

- The classification is local to the EXP-121 shared basis and rational
  anchor. A different chart can reverse which directions appear simple, as
  the EXP-114 comparison already demonstrates.
- Pairwise trace tensors detect only terms through mixed degree two. They do
  not describe the full four-variable determinant.
- SCC size is a support invariant. It does not prevent algebraic cancellation,
  which is why all determinant statements were computed separately and
  exactly.
- Completeness remains relative to the canonical EXP-071 coefficient pool.

## Strategy consequence

Declare EXP-123 on the four-parameter restriction
\[
\{(0,1),(0,5),(1,0),(2,9)\}.
\]
Compute the shared-basis determinant exactly after normalizing \(d=1\), using
the 34-block rather than the full matrix. Test whether the new parameter enters
affinely over \(\mathbb Q[A,B]\). If it does, eliminate it directly against
the already closed \(T_B\) chart cover and isolate only the coefficient-zero
exceptional stratum. If it does not, stop before a generic Groebner
calculation and use specialization recursion on the lowest-degree coefficient
in the new parameter.

The complete EXP-118 through EXP-121 \(T_B\) cover remains the regression
control. It must not be recomputed as an unstructured four-variable problem.
