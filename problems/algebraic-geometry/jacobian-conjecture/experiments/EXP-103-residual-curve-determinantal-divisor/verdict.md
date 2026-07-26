# EXP-103: Endpoint gate blocks the first determinantal-divisor proof

## Verdict

**INCONCLUSIVE**, with a strong exact next target.

The NTT backend successfully reconstructs complete maximal-minor polynomials
modulo \(998244353\), and all direct checks agree. However, only one of the
four declared row charts passes the characteristic-zero endpoint gate, so a
certified gcd cannot yet be formed from two eligible minors.

## Exact and modular findings

- The scaled polynomial matrix has shape \(289\) by \(125\), after deletion of
  the structural constant-\(Q\) zero column.
- EXP-102's exact determinant at \(u=1\) is reproduced.
- EXP-102's chart has assignment bounds \([1547,1646]\) but recovered modular
  support \([1628,1646]\). The 81-degree low-end cancellation is therefore not
  certified over characteristic zero by the assignment shortcut.
- An independently pivoted chart at \(u=2\) has assignment bounds and recovered
  support exactly \([777,903]\). This chart is endpoint-safe.
- The normalized EXP-102 and \(u=2\) chart polynomials have modular gcd \(1\).
  This is exploratory only because the first chart failed its endpoint gate.
- A reversed-order chart at \(u=-1\) repeats the same 81-degree cancellation:
  bounds \([1323,1422]\), recovered support \([1404,1422]\).

Artifact SHA256:
`1DF6079D51ADF46D33C39DCD30DAAC4A87C5128E6CEE1BA5FDEDBE556D0CB710`.

## Interpretation

The modular evidence says the residual curve is very likely covered, but it is
not a proof. The remaining issue is no longer a 125-minor Smith computation.
It is the exact vanishing of 81 low coefficients of one degree-at-most-99
quotient polynomial.

## Next experiment

EXP-104 will evaluate the EXP-102 determinant exactly at 100 integer values.
After division by the proved assignment monomial \(u^{1547}\), exact
interpolation determines the entire degree-at-most-99 quotient. If its first
81 coefficients vanish and coefficient 81 is nonzero, the exact valuation is
\(1628\). The already observed modular gcd-one calculation then becomes a
valid characteristic-zero certificate when recomputed with the endpoint-safe
\(u=2\) chart.

No claim about complete curve coverage, the other 49 coefficient directions,
the full \((72,108)\) family, or \(JC(2)\) is made here.
