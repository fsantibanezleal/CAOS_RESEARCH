# EXP-058 hypothesis: local endpoint source search

Declared: 2026-09-05, before computation. Exact arithmetic, CPU only.

## Question and predictions

EXP-057 proves that the displayed connecting class equals `-[eta_p]` in the
full original integral cokernel, with four explicitly labelled rows. The next
question is whether a small original-domain chain witnesses `M v = 2 eta_p`.

- P1: the deterministic inverse-incidence search below finds an **integral**
  source for `2 eta_p` at each training parameter `p=8,9,10`, within radius two
  and the stated caps. A rational source with denominators does not pass P1.
- P2: any retained integral witness satisfies its complete original boundary
  under a separately implemented differential. Changing a nonzero source
  coefficient by one is rejected whenever that column has nonzero boundary.

The radius is graph distance in the row-to-column-to-row incidence graph,
starting at the four target rows. At each round, enumerate every original
source incident to the frontier rows, deduplicate by its complete labelled
source, and include its **entire** boundary. Process labels deterministically.
There are no projected-away equations: all additional rows have right-hand
side zero. Prefer integer-unit pivots, then exact rational elimination, while
tracking source provenance. A nonintegral particular solution is inconclusive
about integer membership, not a proof of failure in the selected lattice.

## Premise and source preflight

Use the frozen EXP-057 `eta_formula`, EXP-054 full original multiplication and
its independent audit differential, and the EXP-036 offset definitions. Pin
their source SHA-256 hashes in the run manifest. No old HNF source is an input.
The original `p=11` HNF-source holdout remains unread.

For a K row `(E,b)`, add any nonzero generator `v` outside `E` and set `c=b-v`.
This gives a K source if `c` is high, or an S source if `v` is high and `c` low.
For a D row `(E,kind,b)`, both `v` and `c=b-v` must be low and their low product
must equal the queried kind and offset. The face sign is
`(-1)^(number of u in E with u<v)`. A coefficient may also occur in the
exterior; only repeated exterior variables are forbidden.

The invariant-first lens is sparse exact image membership, complementing the
uniform face calculus and relative-incidence/Morse lens. Two structural seed
families motivate the search: K sources adding missing second-low variables,
and S sources with coefficient `3p+t`, `t=0,1,2`. Their initial boundaries are
small, but C0 cancellation may open a parameter-length family. This is a
prediction to test, not a presumed finite-support theorem.

## One-sided interpretation and kill conditions

A certified witness establishes only `2[eta_p]=0` for that parameter. It does
not prove nonzero class, a uniform formula, a second class, or an upper bound.
Rational inconsistency excludes only the selected local source span. A source
for `2d eta_p` obtained by clearing denominators does not certify order two.
P1 can be refuted only if the prescribed local rational span excludes the
target; caps or a nonintegral section are INCONCLUSIVE. Stop at the first
refutation unless an explicitly recorded retained-claims continuation is used.

## Resource budget and outputs

One CPU process, 60 seconds total, 1 GiB private memory, maximum 1200 source
columns and 20000 nonzero incidence entries per parameter. Check the time and
size caps while generating and eliminating; flush a checkpoint after each
radius and parameter. Preserve the completed smaller neighborhood if a later
radius exceeds its cap. No HNF, Smith normal form, global basis enumeration,
larger parameter, or implicit budget extension.

Persist deterministic neighborhood counts, premise hashes, exact residual
classification, any integral witness with full labels, and independent audit
results. Test outputs use temporary directories. Before another compute round,
inspect whether a witness has a symbolic pattern or a local obstruction points
to a different proof strategy. Finite success alone is not a publication trigger.
