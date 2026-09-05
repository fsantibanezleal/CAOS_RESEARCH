# EXP-060 hypothesis: explicit uniform twice-endpoint source

Declared: 2026-09-05 before computation. Exact integers, CPU only.

## Frozen original source operator

For p>=8 put `L=[1,p] union [3p,4p-2]` and `h=8p-2`. Potentials f are integral,
indexed by `0<=u<=p-2`, `0<=r<=p-1`, and vanish for `r<=u`. Define P(f) as follows.

For `r<s`, `u<=r+s<=p+u-1`, include the S source

```text
[(L minus {p-r,p-s,3p+u}) union {6p,h}; p+u-r-s]
```

with weight `(-1)^(p+r+s+u)(f_u(s)-f_u(r))`.

For `u<v`, set R=u+v, F=f_u-f_v, and take
`max(0,R-p+2)<=r<=min(p-1,R)`. Include the S source

```text
[(L minus {p-r,3p+u,3p+v}) union {6p,h}; 3p+R-r]
```

with weight `(-1)^(p+r+u+v) beta_r`, where beta_r=F(r)-F(R+1) if R<=p-2,
and beta_r=F(r) otherwise. Omit zero weights and combine identical original labels.

Write e(r;u,v), u<v, for the K row missing `{p-r,3p+u,3p+v}`, with exterior
high `{6p}`, coefficient offset `11p-2+u+v-r`, and normalized weight
`(-1)^(p+r+u+v)`. Use only valid degree-two offsets. Let x_uv=e(u+v;u,v).

## Explicit interval potentials and final candidate

For j=1,2 let k=p-2-j and define F_j by

```text
f_0(r)= 1 for j+1<=r<=k,
f_j(r)=-1 for j+1<=r<=p-2,
f_k(r)=-1 for k+1<=r<=p-2,
all other values zero.
```

The three second indices 0,j,k are distinct for every p>=8.
Let delta_02 and delta_03 be unit potentials at (u,r)=(0,2),(0,3).
For a=2,3 let Q_a be the **positive unit** K source

```text
[(L minus {p-a,3p}) union {6p};8p-2-a].
```

The frozen candidate is

```text
V_p=P(F_2+2F_1-4delta_03-4delta_02)+4Q_3-4Q_2.
```

- P1: P(f) has zero complete D boundary for these potentials. The full K
  boundary consists only of the negative h face: alpha survives at coefficient
  offset 1 (C0), beta at offset 3p (diagonal C2); all 6p faces vanish.
- P2: `M P(F_j)=2x_0j` for j=1,2. Reflection-symmetric interval potentials
  cancel every C0 row, and their endpoint differences telescope to these two rows.
- P3: putting B=P(delta_03)-Q_3 and D=P(delta_02)+Q_2, the exact ORIGINAL
  identities are `M B=e(3;0,1)+x_02+e(3;0,2)` and `M D=x_01+e(2;0,1)`.
  Consequently `eta=x_02+2x_01-2 M B-2 M D` and **`M V_p=2eta_p` for every p>=8**.

An earlier paper-only proposal omitted delta_02/Q_2 and confused e(2;0,1) with
x_01=e(1;0,1). It was rejected during preflight, before declaration or computation.
Do not reintroduce that error or treat quotient equality as exact vector equality.

## Premises, interpretation and proof obligations

Pin this hypothesis, EXP-036's offset algebra, EXP-054's two original boundary
implementations, and EXP-057's eta formula. EXP-059's signed potential proof is
the structural premise, but its high variable is different: derive the shifted
admissibility and every face again. No HNF source, global basis, or old p=11
HNF-source holdout is an input.

PASS proves uniform **2-annihilation**, not uniform nonvanishing: the class of
eta, and hence of b_A+b_B, has order dividing two in the full integral cokernel.
It does not prove that this order is exactly two, a second independent class,
the complete quotient, or a recurrence. Explicit source witnesses and complete
independent boundary checks are mandatory; finite field ranks are insufficient.

The invariant-first lens is an explicit source equation. The complementary
lenses are potential reconstruction, signed interval reflection, and parity.
The proof must check all interval endpoints and the Q_a high faces
`14p-4` and `14p-5`, which vanish in H4 for p>=8. No hidden unit filler or
projected-away row is allowed.

## Declared campaign, budget and kill rules

Training/smoke: p=8 first, then p=9,...,20. Stress parameters: 25,32,50,64,100.
These 18 values are fixed before testing; no holdout claim is made for this
newly constructed source. The original p=11 HNF-source labels remain unread.

One CPU producer and one independent CPU audit, each capped at 60 seconds and
1 GiB private memory. Check budgets within generation and multiplication,
checkpoint and flush at each parameter. Use sparse potentials and combine
identical source terms before multiplication; no ambient triple/basis enumeration.
Stop on first exact failure, premise mismatch or resource cap. Preserve failures;
do not silently enlarge the budget or alter the hypothesis.

Verify P1/P2/P3 with complete independently encoded differentials. Include
coefficient/sign mutations, and confirm that the rejected missing-delta_02
proposal fails. Persist deterministic full labelled V sources, compact boundary
hashes/counts, proof, audit, verdict and permanent temporary-output tests.
Reassess manuscript creation and Zenodo only after the all-parameter proof and
independent full-boundary audit pass, preserving the nonvanishing boundary.
