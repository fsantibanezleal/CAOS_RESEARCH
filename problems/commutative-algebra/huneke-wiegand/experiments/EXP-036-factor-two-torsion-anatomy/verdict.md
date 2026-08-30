# EXP-036 verdict - CONFIRMED with structural propagation unresolved

## Verdict

**CONFIRMED for P1 and the compact-core part of P2.  The six-variable projective-plane
recognition clause is rejected for the canonical reduction.  P3 is not established.**

EXP-036 proves that the characteristic-dependent EXP-035 cell is not an isolated `p=4`
phenomenon.  Exact complete-target calculations find characteristic dependence in seven of the
eight newly tested cells.  At `(5,3)` and `(6,3)` the kernel incidence matrix itself has a
mod-two rank defect.  At every tested `t=2` cell with `5<=p<=9`, the kernel cokernel has the same
dimension over `GF(2)` and `GF(3)`; the dependence is created entirely by the smaller
connecting-image rank over `GF(2)`.  The additional tested field `GF(1000003)` agrees with
`GF(3)`; no statement covering every odd characteristic is inferred.

For `t=2`, the exact characteristic-two excesses in `A_p` and `C_p` are

```text
p=4,5,6,7,8,9:  1,4,9,18,31,49.
```

The conjectural formulas `(p-3)^2` and `2p^2-17p+39` are both refuted by later exact cells.  No
infinite excess formula is claimed.

At `(4,2)`, 74 exact unit cancellations leave a `5` by `45` residual with only two entries,
both `-2`, and recover `Z^4 direct-sum Z/2Z`.  The active certificate uses seven low variables,
not the six predicted by the real-projective-plane analogy.  This preserves the compact
factor-two certificate while rejecting that recognition in the tested canonical reduction.

Independently of the finite pattern, EXP-036 proves for all integers `p>=4` and
`2<=t<=p-2` that the shifted cubic source diagonal is absent.  Therefore every computed `A_p`
value in this family is exactly the corresponding `C_p` value, and the same transfer holds for
any future exact family cell.

## Evidence

- Canonical exact-sum enumeration reproduces the frozen EXP-035 `(4,2)` bases and ranks.
- The complete `p<=6` triangle and targeted `(7,2)`, `(8,2)`, and `(9,2)` cells use exact sparse
  ranks over GF(2), GF(3), and GF(1000003).
- A separately written semigroup-basis, dynamic-sum, reverse-pivot route audits all eight cells
  through `(8,2)` with an additional GF(5) control.  Its `(9,2)` attempt is preserved as a
  47.5-GB resource stop and contributes no mathematical evidence.
- Exact unimodular cancellation and Smith form certify the compact `(4,2)` factor-two residual.
- The symbolic certificate proves the positive cubic gap `g(p,t)>=3(p-1)^2` and preserves both
  failed interpolation controls.

## Boundary and redirection

The Huneke-Wiegand conjecture was already disproved by the public Son Pham counterexample; this
experiment does not claim that discovery.  Within the CAOS extension programme, EXP-036 does not
complete either lower Betti strand and does not prove infinitely many characteristic-dependent
cells.  The strongest next path is to identify the mod-two homology of the connecting-image
quotient, especially the `t=2` diagonal.  Integral Smith calculations of kernel matrices alone
cannot see that mechanism.
