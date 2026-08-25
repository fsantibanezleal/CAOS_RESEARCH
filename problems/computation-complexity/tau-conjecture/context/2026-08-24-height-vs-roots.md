# TCB-030 instrumentation: minimal HEIGHT against root count

Measurement note, 2026-08-24. Instrument proposed by the V11
evaluation-matrix view: does making many columns vanish at once force
large magnitudes? Height (max |coefficient|) is the cheap proxy, and the
census records answer it directly.

## Data (min over the witnesses our census stores)

    z (distinct integer roots) :  2   3   4   5    6
    minimal height             :  1   1   2   4   15

Sources: depths 1-5 from a fresh census pass; z = 5 from the complete set
of 67 five-rooters with tau <= 7 (EXP-007); z = 6 from the 50 stored
8-gate six-rooters (EXP-006).

Cross-check by hand for z = 6: the monic product over the record root set
{-2,-1,0,1,2,3} expands to
x^6 - 3x^5 - 5x^4 + 15x^3 + 4x^2 - 12x, height 15, matching the measured
minimum; the symmetric alternative (x^2-1)(x^2-4)(x^2-9) has height 49,
so the record set is also the cheaper one in height, not only in gates.

## Reading (honest scope)

- The trend 1, 1, 2, 4, 15 is monotone and accelerating, which is the
  qualitative statement the V11 note wanted to test: root count and
  coefficient magnitude trade off against each other.
- SCOPE: this is the minimum over the witnesses in our census (tau <= 8),
  not a proof about all polynomials with z integer roots. For z <= 6 the
  hand check above suggests the census minimum coincides with the true
  minimum, but that is verified only for the specific sets examined.
- The quantity "smallest height of an integer polynomial with z distinct
  integer roots" has a classical flavour (integer Chebyshev / small-height
  problems); we have not identified a source, so no attribution is made.
- What it does NOT give: a lower bound on tau. A tau-gate program can
  produce height up to a tower in tau, so height alone cannot bound gates
  from below. The interesting direction would be a bound on the height
  reachable with FEW BUILT CONSTANTS, which is the census's actual
  friction and is not captured by height alone. Recorded as the honest
  limitation of this instrument.
