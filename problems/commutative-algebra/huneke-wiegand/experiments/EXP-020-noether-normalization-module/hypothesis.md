# EXP-020 - exact Noether-normalization module

Status: DECLARED before formal implementation or execution on 2026-08-12.

## Question and motivation

For `p>=4`, put `s=6p`, let `G_p=gr_(T_p)(R_p)`, and let

```text
F_p=k[x_p],  x_p=(t^(4s))^*.
```

EXP-017 makes `F_p` a Noether normalization of `G_p`; EXP-019 identifies the complete torsion but
not the full `F_p`-module. Does the exact conductor-power Apery table determine a uniform cyclic
decomposition and the resulting graded Betti data?

## Falsifiable prediction

The complete graded decomposition is predicted to be

```text
G_p isomorphic to
  (F_p/(x_p))^p
  direct-sum F_p
  direct-sum F_p(-1)^(10p-1)
  direct-sum F_p(-2)^(12p)
  direct-sum F_p(-3)^(2p-1)
  direct-sum F_p(-4).
```

Equivalently, the only torsion invariant is `p` copies of `F_p/(x_p)` generated in degree zero;
the free-shift vector in degrees zero through four is

```text
(1,10p-1,12p,2p-1,1).
```

The predicted minimal graded Betti numbers over `F_p` are

```text
beta_(0,0)=p+1,
beta_(0,1)=10p-1,
beta_(0,2)=12p,
beta_(0,3)=2p-1,
beta_(0,4)=1,
beta_(1,1)=p,
```

with all others zero. Consequently

```text
pd_(F_p)(G_p)=1,
reg_(F_p)(G_p)=4,
a(G_p)=3,
length(G_p/x_pG_p)=25p=e0(T_p)+I(G_p).
```

## Premise dependencies

- EXP-017 confirms the minimal reduction, reduction number four, and `e0=24p`, `e1=39p`.
- EXP-018 confirms the exact Hilbert numerator of `G_p`.
- EXP-019 confirms `H^0=k^p` in degree zero, annihilation by `x_p`, and the Cohen--Macaulay
  quotient numerator.

## Required proof and evidence

1. Prove that `G_p` is finite over `F_p` and that its `F_p`-torsion equals EXP-019's `H^0`.
2. Apply the graded principal-ideal-domain structure theorem, proving that the quotient is free
   and that its Hilbert numerator uniquely fixes the shifts.
3. Derive the minimal resolution, projective dimension, `F_p`-regularity, top local-cohomology
   degree, and minimal-reduction-section length.
4. Independently reconstruct the decomposition column by column from the Apery sets of
   `R_p,T_p,...,T_p^5` modulo `24p`.
5. Run two exact routes for `p=4,...,300`, beginning with a mandatory `p=4` smoke gate, followed
   by an independent selected-parameter and all-row hash audit.

## PASS, FAIL, and one-sidedness

- A computational PASS confirms that both exact finite reconstructions implement the predicted
  formulas on the declared range. It does not prove the infinite family without the symbolic
  graded-module argument.
- Any mismatch at `p=4` refutes this exact prediction and stops the campaign. A later mismatch
  also refutes the formula as stated and must be preserved.
- A symbolic proof plus both exact routes, all adversarial controls, and the independent audit
  proves the stated theorem for every `p>=4` from the confirmed premises.

## Invariant-first note

The Hilbert numerator and the exponent-one torsion are sufficient invariants: over `k[x_p]`, they
force the complete cyclic decomposition. No SAT, Groebner basis, or larger parameter sweep is
needed. The Apery route is retained as an independent reconstruction, not as the proof.

## Adversarial controls

- change one torsion summand from `F_p/(x_p)` to `F_p/(x_p^2)`;
- delete one degree-one free summand;
- change `beta_(1,1)` from `p` to `p-1`;
- change regularity from four to three;
- change `length(G_p/x_pG_p)` from `25p` to `25p-1`.

Every corruption must be rejected.

## Compute budget and verdict rule

- CPU only; exact integer and bitset arithmetic; no randomness;
- two minutes for the full campaign and one minute for the independent audit;
- no checkpoint is needed because each parameter is an independent row and the full run is
  expected to finish well below five minutes;
- hitting the budget yields `INCONCLUSIVE`, not a mathematical negative result;
- `CONFIRMED` requires the symbolic proof, both complete exact routes, all controls, stable
  hashes, and the independent audit.
