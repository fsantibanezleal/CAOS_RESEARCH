# V11: the evaluation-matrix (coincidence) view

Exploration note, 2026-08-03 (round 9). The mathematical object behind
the EXP-008 SMT encoding, promoted to a standing view; calibration
honest throughout.

## The object

Fix a program of length $\tau$ computing $f$ and let $r_1 < \dots < r_z$
be distinct integer roots of $f$. Evaluating every program item at every
root gives the EVALUATION MATRIX $E \in \mathbb{Z}^{(\tau+3) \times z}$:
rows indexed by items ($-1$, $1$, $x$, then gates), columns by roots;
the $x$-row is $(r_1, \dots, r_z)$ with distinct entries; every gate row
is the entrywise sum/difference/product of two earlier rows; the last
row is $\mathbf{0}$.

The tau conjecture is EXACTLY: a matrix with this closure property and
$\le \tau$ generated rows has at most $(1+\tau)^{\kappa}$ columns. The
census, the SAT encoding, and the co-occurrence scans are all
computations over this one object (the encoding drops the polynomial
entirely and works with $E$; the $\times$-case scan works with the
supports of rows; the digit census reads $E$'s columns mod $p$).

## What the view buys

1. **A coefficient-free formulation.** Nothing in the matrix mentions
   coefficients or degree: the conjecture becomes a combinatorial
   statement about entrywise-algebra closures over $\mathbb{Z}$ reaching
   $\mathbf{0}$ on many distinct inputs. This is the form a
   proof-theoretic or Ramsey-flavored attack would want, and the form
   SAT/SMT natively decides at fixed size.
2. **Growth discipline along rows.** Down any column, values evolve by
   $+,-,\times$ from $(-1, 1, r)$: a walk in $\mathbb{Z}$ whose zero
   landing at step $\tau$ must happen SIMULTANEOUSLY in all $z$ columns.
   The stall theorems are the special case where the walk is an
   iteration; the plateaus measure the general price of simultaneity.
3. **A possible bridge, flagged [C]:** simultaneous coincidences
   $v(r_i) = \mp b(r_i)$ across many $i$ smell like the
   unit-equation/subspace-theorem world (few solutions to structured
   equations); a round-9 sweep found NO existing application of that
   machinery to SLP root bounds, and no obvious direct reduction (the
   values $v(r_i)$ are not S-units in general). Recorded as a
   speculative direction, not a claim; a serious attempt would need the
   values to live in a finitely generated multiplicative structure,
   which the model does not provide for free.

## Instrumentation consequences (cheap, queued)

- Store, for census records, the full evaluation matrix restricted to
  roots-of-record: its entry growth (max $|E|$ per gate row) is a new
  measurable (how large must intermediate values get to kill $z$
  columns at once?). Candidate lemma target: lower bounds on
  $\max |E_{j,i}|$ in terms of $z$ (a Mahler/height flavored
  inequality), which would convert the census's plateau phenomenon
  into a proved trade-off. Backlog row TCB-030.

## Honesty

Nothing here is a theorem beyond restatements; the view's value is that
it unifies the program's instruments around one object and names the
speculative analytic bridge without claiming it.
