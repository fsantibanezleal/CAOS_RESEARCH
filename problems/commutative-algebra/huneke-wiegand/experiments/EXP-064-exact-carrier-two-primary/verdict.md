# EXP-064 verdict

Status: **CONFIRMED FINITELY** for `p=8,9,10,11`; P1--P3 pass.

Exact modular-Hadamard certificates determine the rational ranks of all 16
carrier matrices. In every case the rational/mod-two rank gap equals the first
integral Bockstein rank, proving that every even Smith factor has 2-adic
valuation exactly one. The complete 2-primary types are

```text
mask 56: 0, 0, 0, (Z/2)^1
mask 58: (Z/2)^1, (Z/2)^2, (Z/2)^3, (Z/2)^5
mask 59: (Z/2)^3, (Z/2)^4, (Z/2)^5, (Z/2)^7
mask 62: (Z/2)^3, (Z/2)^4, (Z/2)^5, (Z/2)^7.
```

Combining this exponent-two theorem with EXP-062's twice-class sources and
EXP-063's literal coordinates upgrades the comparison to an exact integral
finite result. In mask 58 the endpoint triangles `(0,1,p-3)` and
`(0,2,p-4)` vanish integrally; all remaining triangle images form the complete
2-primary subgroup. All triangles generate the complete 2-primary subgroup in
masks 59 and 62. Mask 56 kills all triangle images through `p=10`; at `p=11`,
`(2,3,4)` is its sole nonzero triangle image and generator.

The independent audit verifies 1,100 prime/rank pairs, 16 minimally sufficient
Hadamard prefixes, 16 entry-mutation controls, two exponent controls and 16
triangle consequences. This closes the exact finite integral comparison gate.

The uniform comparison remains open: the integral vanishings currently follow
from finite exponent certificates rather than explicit all-parameter sources.
No complementary full-cokernel upper bound or recurrence follows. The result
is substantial but finite and does not trigger a manuscript or Zenodo revision.
