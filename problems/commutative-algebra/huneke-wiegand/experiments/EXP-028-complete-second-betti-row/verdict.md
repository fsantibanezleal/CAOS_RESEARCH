# EXP-028 verdict - CONFIRMED

Date: 2026-08-19. Backlog: HWB-035.

## Result

For every integer `p>=4` and every field,

```text
beta_(2,5)=p(2p-3),
beta_(2,6)=0.
```

The complete degree-five offset support is

```text
[3p+2,5p-2] union [6p+1,8p-3] union [9p,11p-4],
```

with the outer pair-sum profile `m_out` and middle plateau profile `m_mid` stated in
`hypothesis.md` and proved in `proof.md`. The integral first homology is free in degree five and
zero in degree six, so there is no characteristic exception.

Together with EXP-024 and EXP-027, the entire second Betti row is now known:

```text
beta_(2,3)=2p(500p^2-330p+31)/3,
beta_(2,4)=8p,
beta_(2,5)=p(2p-3),
beta_(2,6)=0,
beta_(2,j)=0 otherwise.
```

This completes one full interior homological row. It does not determine the full Betti table and
does not settle the Huneke--Wiegand conjecture or HWB-035 by itself.

## Evidence

- integral relative offset-Koszul derivation;
- all-parameter lexicographic matching and unit Smith normal form;
- 297-row closed-form campaign for `p=4,...,300`;
- complete degree-five signed-chain profiles for `p=4,5,6`;
- complete `p=4` degree-six profile over two unrelated prime fields;
- independent rational-rank and Smith-normal-form audit;
- arithmetic/Z3 endpoint certificate through `p=10000`;
- frozen premise hashes and adversarial mutation controls.

Canonical aggregate:

```text
45f08e6a15e321512629fa4b6ab07161ddcc766ddf56e1d9579175f3444ec32f
```

## Gate assessment

All declared gates pass. The result is theorem-sized and completes a full row, so it triggers a
main-manuscript revision to v0.15. A separate manuscript remains deferred: the object and method
continue EXP-027, and the remaining table is still open.
