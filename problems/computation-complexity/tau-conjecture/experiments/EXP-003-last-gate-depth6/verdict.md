# EXP-003 verdict: census CONFIRMED, $z_{\max}(6) = 5$; our prediction 2 REFUTED

Run 2026-08-01, `run.py` (tclib tests green incl. the new tower checks;
smoke over the depth-4 frontier reproduced EXP-002 exactly: 11,377 new
polys, $z_{\max}(5)=4$, 10 records; then full), repo venv Python 3.13.0,
CPU only, deterministic; scan 295 s, witness reconstruction to 1005 s
total (budget 60 min). Raw output: `artifacts/scan6.json`.

## Results (exact, depth 6 decision-complete via the last-gate lemma)

| $\tau$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $z_{\max}$ | 1 | 2 | 3 | 3 | 4 | **5** |

- 778,087 depth-5 states scanned completely; 134,494 new polynomials at
  depth 6 (z histogram: 50,224 rootless; 59,674 with 1; 20,081 with 2;
  4,316 with 3; 195 with 4; **4 with 5**).
- Prediction 1 CONFIRMED (new-poly count on the order of $10^5$).
- **Prediction 2 REFUTED**: $z_{\max}(6) = 5$, not 4. The minimal $\tau$
  with 5 distinct integer roots is exactly 6 (lower bound from the
  depth-5 census, upper bound by witness).

## The mechanism we missed (recorded in full)

All four records are one polynomial family: $\pm x^{1,2} \cdot
\big(x^2 - (x^2-2)^2\big) = \mp x^{1,2}(x^2-1)(x^2-4)$, root set
$\{0, \pm 1, \pm 2\}$, 2-adic spectra $\{0,1\}$. Witness (replay-verified):
$-2$; $x^2$; $x^2-2$; $(x^2-2)^2$; $x^2 - (x^2-2)^2$; $\times\, x$:
six gates. The move our prediction ignored: MULTIPLYING BY THE INPUT $x$
costs one gate and adjoins the root 0 to any record avoiding it: the
depth-5 records with roots $\{\pm1,\pm2\}$ were one such. The
Chebyshev-tower route to the same root set ($G_2$) costs 7; the census
found the 6-gate shortcut by pairing the $k=1$ DOS split with the free
root at 0 instead of climbing the tower.

Corrected structural picture: the stable core $P = \{0, \pm1, \pm2\}$ of
the $x^2-2$ preimage tree is reachable at $\tau = 6$; the tower lemma
(context note) still says no SINGLE-INNER-MAP tower beats $|P| = 5$ at
ANY depth, so beating 5 roots requires leaving that mechanism class
entirely (shifted/multi-map factories: exactly what depth 7+ will probe).

## Method note (the last-gate lemma held up)

$z_{\max}(6)$ was decided WITHOUT storing the depth-6 frontier (estimated
~20M states): the scan kept memory at the depth-5 frontier plus a
~150k-poly dictionary and ran in 5 minutes. The smoke gate also caught a
real accounting artifact before the run (results equal to the free inputs
were initially counted as new polynomials: 11,380 vs 11,377; fixed by
seeding the known-set with the inputs; z-values unaffected). Both facts
go to the method's credit ledger: the gate did its job.

## Adversarial validation record

- Internal regression gate: frontier rebuild reproduced state counts
  9/98/1462/29506/778087.
- Witness replay: three of the four records reconstructed as explicit
  6-gate programs; tuple-exact replay; all roots verified by exact
  evaluation; counts certified by the divisor argument.
- Independent cross-check this round: tclib vs sympy on 284 polynomials
  (all of $\tau \le 3$ plus every stored record), zero mismatches
  (`scripts/check_sympy_crosscheck.py`).

## How could this be wrong?

The last-gate lemma's normalization step (an optimal length-$(d{+}1)$
program WLOG has normalized prefix) reuses the EXP-001 lemmas; the new
step is the prefix argument, written in the hypothesis. The residual risk
is shared code paths (enumerator and witness DFS both use tclib), now
partially hedged by the sympy cross-check on records. The refuted prediction is a
judgment error, not a tooling error: the census machinery itself passed
every gate.

## Consequences for the strategy

- Growth data $1,2,3,3,4,5$: records track $z = \tau - 1$ from $\tau = 3$
  onward. Minted question: is $z_{\max}(\tau) = \tau - 1$ the exact law in
  this range, i.e. does depth 7 give 6? The multiply-by-$x$ move plus
  shifted DOS blocks suggests YES as a construction target; the scan of
  the depth-6 frontier is beyond the current naive method (frontier not
  stored) so depth 7 NEEDS the TCB-005 canonicalization or a compiled
  backend: now the concrete blocker.
- The anatomy ledger gains the "free root at the origin" move; the dual
  view $T(S)$ records $T(\{0,\pm1,\pm2\}) = 6$ and
  $T(\{\pm1,\pm2\}) = 5$.
