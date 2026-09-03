# EXP-050 proof record - exact corrected representatives

Date: 2026-09-03. Status: **REFUTED overall**, with P1 confirmed finitely. CPU-only exact integer
and binary arithmetic.

## Exact construction

EXP-050 carries integer provenance through the canonical Bockstein reduction. Start with a binary
kernel combination `z` and its even boundary `Rz=2b`. Whenever quotient reduction removes an image
vector represented by a binary column combination `w`, perform the exact update

```text
b <- b-Rw,       y <- z-2w.
```

Whenever Bockstein basis reduction xors two parity vectors, add their integer representatives and
witnesses. Every operation preserves

```text
Ry=2b.
```

The final parity vector is one displayed EXP-048 chain `a`, so coefficientwise
`c=(b-a)/2` is integral. Direct sparse multiplication verifies all sixteen identities for both
completions and every `p=8,...,11`. In every case `c` is nonzero, as required by the independent
EXP-049 nonmembership result.

Reversed relation traversal with high pivots independently constructs rank-two exact Bockstein
bases. Reducing their parity classes modulo the primary image gives the same intrinsic subspace.

## Declared predictions

P1 passes finitely. The experiment stores exact sparse `b`, `c`, and `y` for all sixteen named
classes, with

```text
b=a+2c,       Ry=2b,       c != 0.
```

P2 is strongly refuted. At `p=8`, the four correction supports already have sizes
`27,26,45,44`, and their maximum absolute coefficients are `14,28,32,21`, not one. Across the
full range, the correction support sizes in formula order are

```text
58->59: (27,26), (36,35), (43,45), (54,48),
58->62: (45,44), (63,62), (81,81), (101,100).
```

The maximum absolute coefficients across the same records range from `13` to `71`. Thus the fixed
provenance section is an exact certificate source but not a simple semantic proof basis.

P3 is refuted. Only one of the four sorted support series is affine on the complete table:
`9p-45`. The other three fail the declared affine test, and the correction atom histograms are not
constant. In particular, the `58->62` first series follows `18p-99` through `p=10` but is `101`,
not `99`, at `p=11`. This is a basis effect, not a new claim about the intrinsic torsion.

## Independent audit

The separate auditor passes 152 of 152 checks. It verifies the frozen result and relative-matrix
hashes; reconstructs every exact representative, correction, and witness vector from sparse
storage; checks parity and `b=a+2c`; confirms every correction is nonzero; checks both exact route
ranks; and independently re-evaluates the declared P2/P3 failures.

The result SHA-256 is
`2dc8f85097171e24f4080ce25684127914d86661a6291bab69fb334c2c987983`, with internal artifact hash
`70ea38438f376858a5878100bed77407bc28f78f6ea3d847587b3158cc022b589`. The audit certificate has
internal hash `51c6a2c36bcdde9c1327178d09460ce93f131daba2f9fc08ec9ff9546b5aa5c4` and external SHA-256
`eb62ef3e0b7801c44856ad135748f067a3d16846a109788af6e292ac074d99fe`.

## What could make this wrong?

- The constructions are exact only for `p=8,...,11`. They are not all-parameter formulas.
- The chosen `b,c,y` depend on binary elimination and quotient-section conventions. Their large
  coefficients and irregular supports must not be interpreted as intrinsic complexity.
- The audit validates the stored primary witnesses and the independent high/reverse route status,
  but a uniform proof still needs formula-level signed incidence identities.
- Constructing two classes gives the finite lower bound. The uniform upper bound remains separate.

## Consequence and route change

The corrected-lift existence problem is solved finitely, but direct formula fitting of the
canonical provenance output is demoted. The more promising primal object is an unreduced
Bockstein lift: among all binary cycles whose divided boundaries span the two quotient classes,
select witnesses minimizing boundary support before forcing the canonical `alpha/beta` section.
This preserves exact order two while avoiding the large free-coordinate corrections created by
quotient normalization.

The dual lower-bound route remains strongest because EXP-049 already gives support-at-most-four
certificates. After a uniform lower bound, the upper bound should use a relative-Morse/free
complement rather than global Smith coordinates.

No manuscript or Zenodo update is triggered.
