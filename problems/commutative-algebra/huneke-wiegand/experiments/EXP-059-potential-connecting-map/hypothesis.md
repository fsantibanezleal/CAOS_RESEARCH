# EXP-059 hypothesis: a uniform potential basis and sparse connecting map

Declared: 2026-09-05 before numerical evaluation. Exact integers, CPU only.

## Structural prediction

Fix `p>=8`, `L=[1,p] union [3p,4p-2]`, and the two exterior high variables
`{6p,8p-4}`. Consider all original S sources in the current multidegree whose
exterior high set is exactly this pair. Denote their D boundary by `d_D`.
Index first-low variables as `p-r`, `0<=r<=p-1`, and second-low variables as
`3p+u`, `0<=u<=p-2`.

Choose arbitrary integral potentials `f_u(r)`, required to vanish for `r<=u+1`.
For `r<s`, define `alpha_u(r,s)=f_u(s)-f_u(r)`. Include the original S column

```text
[(L minus {p-r,p-s,3p+u}) union {6p,8p-4}; p+2+u-r-s]
```

with weight `(-1)^(p+r+s+u) alpha_u(r,s)`, whenever
`u+2<=r+s<=p+u+1`.

For `u<v`, put `R=u+v`, `F=f_u-f_v`, and let
`max(0,R-p+4)<=r<=min(p-1,R+2)`. Define

```text
beta_r(u,v) = F(r)-F(R+3) if R<=p-4,
              F(r)       if R>=p-3.
```

Include the S column

```text
[(L minus {p-r,3p+u,3p+v}) union {6p,8p-4}; 3p+2+u+v-r]
```

with weight `(-1)^(p+r+u+v) beta_r(u,v)`. Zero weights are omitted.

- P1: these chains are exactly `ker_Z(d_D)` in this specified fixed-high
  sector, with unit-potential basis `f_u(r)=1` for `u+2<=r<=p-1`. Its rank is
  `binom(p-1,2)`. The proof must include exhaustion of original sources,
  complete signed A/B equations, reconstruction, and uniqueness over Z.
- P2: each unit-potential chain has coefficients of absolute value one and
  support at most `3p-5`. Its full original boundary has ZERO D component and
  at most seven K rows: at most one C0 and at most six C2 rows.
- P3: the complete boundary is obtained by retaining only the negative
  `8p-4` face, and only when an alpha coefficient-offset equals 3 or a beta
  coefficient-offset is `3p`, `3p+1`, or `3p+2`. Every `6p` face vanishes.
  Independently encoded full differentials and coefficient mutations must
  confirm the frozen formulas.

## Premise and distinguishing-invariant preflight

Use EXP-036's original offset algebra and EXP-054's independently encoded
original differentials. Pin their hashes and this declaration. EXP-057 owns
the four-row endpoint target; EXP-058's exact local dual excludes its
radius-two source span at p=8. No old HNF source or p=11 source holdout is read.

The new lens is a complete potential parametrization before elimination:
A equations through first endpoint 0 determine alpha; B equations through
the same endpoint determine beta. In the second-low-only sector, a unit
star minor gives injectivity. This is an integral reconstruction claim, not
an inference from equal ranks. The paired lenses are signed complements,
relative homology, and the sparse connecting-image map.

PASS supplies a generic original D-cycle basis and an explicit sparse
connecting map for ONE fixed-high sector. It does not show that this sector
controls the entire presentation, that eta is nonzero, that `2eta` is in the
image, that the quotient has a second class, or any full torsion upper bound.
These remain separate gates. A sign or endpoint failure refutes the stated
formula; do not repair the declaration silently.

## Budget, campaign, and independent evidence

One CPU process per producer/audit, each at most 60 seconds and 1 GiB private
memory. Check and flush after every parameter, and check budget within chain
generation. No HNF, Smith form, full basis of M, or unbounded parameter sweep.

Check every unit potential at p=8,...,16 (525 chains). At p=17,...,100 check
the four frozen pairs `(0,2)`, `(0,p-1)`, `(1,3)`, `(p-3,p-1)` (336 chains).
The total is 861 distinct chains; this stress range does not replace P1's
uniform proof. Audit the complete original boundaries independently and
recover each potential from its distinguished alpha coordinate. Include
wrong-sign and coefficient-mutation controls. Preserve the first failing
case and stop on disagreement, premise mismatch, or a resource cap.

Persist compact deterministic counts/hashes, source generation and boundary
formulas, signed proof, independent audit, tests, and a verdict. Test writes
must use temporary paths. After validation, evaluate whether the seven-row
connecting map can produce a uniform `2eta` source or dual. Do not increase
the local-search radius by default. Reassess publication only against the
existing stronger theorem gate, not merely this new presentation size.
