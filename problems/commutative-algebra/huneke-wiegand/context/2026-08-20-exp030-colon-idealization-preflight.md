# EXP-030 preflight - cubic-colon idealization and degree-six third strand

Date: 2026-08-20. Scope: HWB-035 and HWB-043.

## Question and premise audit

EXP-029 determines the linear part of the cubic colon

```text
(Q_p:f_p)_1=span{X_a:a in E_(p,1), a>=6p}
```

and uses its second Koszul wedges to prove the complete degree-five third-syzygy profile. The next
entry is `beta_(3,6)`. In the mapping cone for

```text
0 -> P_p/(Q_p:f_p)(-3) -> P_p/Q_p -> C_p -> 0,
```

its first new colon term is `beta_(2,3)(P_p/(Q_p:f_p))`. Computing that quotient before computing
the full relative complex is therefore the invariant-first route.

Premises are frozen as follows.

| premise | supporting record | status |
|---|---|---|
| `J_p=(Q_p,f_p)` with one cubic `f_p=X_0^2X_(3p)-X_p^3` | EXP-023 | confirmed |
| `E_(p,1)` has the eleven displayed blocks and `|E_(p,1)|=10p` | EXP-021/023 | confirmed |
| the linear colon is exactly the `8p` variables of offset at least `6p` | EXP-027 | confirmed |
| relative squarefree-divisor homology computes the multigraded Betti entries | EXP-027 | confirmed |
| the complete degree-five third strand is the shifted high-variable pair basis | EXP-029 | confirmed |
| no cancellation removes the predicted degree-six colon term | new EXP-030 hypothesis | unproved |

## Source-complete and novelty sweep

The full sources already retained for EXP-029 were rechecked before selecting the route:

- `https://arxiv.org/abs/1801.00153`, numerical-semigroup Betti numbers and the characteristic
  boundary of squarefree-divisor homology;
- `https://arxiv.org/abs/1804.06632`, explicit squarefree-divisor complexes;
- `https://arxiv.org/abs/math/0501179`, integral algebraic discrete Morse cancellation;
- `https://arxiv.org/abs/1909.12820`, toric splitting and recursive Betti reconstruction;
- `https://arxiv.org/abs/1407.5702`, Betti-poset recognition for monomial resolutions; and
- `https://arxiv.org/abs/2605.27035`, the recent family-wide KW-semigroup Betti computation via
  Apéry posets and determinantal recognition.

A fresh 2026-08-20 primary-source search also checked recent work on mapping cones, semigroup
Betti numbers, fiber-cone resolutions, and algebraic discrete Morse theory. No source found in the
sweep computes this nonreduced conductor-fiber family, its cubic colon, or `beta_(3,6)`. The KW
paper is methodologically relevant because it recognizes a whole-family resolution from a
classical model, but its semigroups and determinantal ring are different. It cannot support the
present formula.

## Invariant-first derivation

Let

```text
L_p=[0,p] union [3p,4p-2],
A_i=X_i                 (0<=i<=p),
B_j=X_(3p+j)            (0<=j<=p-2).
```

After the `8p` high variables are killed, equal-offset quadratic moves predict the ideal generated
by

```text
A_i A_j-A_k A_l     when i+j=k+l,
A_i B_j-A_k B_l     when i+j=k+l,
B_i B_j             for all i,j.
```

This is the defining ideal of the square-zero algebra

```text
k[s,t]^(p) semidirect omega_(k[s,t]^(p)),
A_i -> s^(p-i)t^i,
B_j -> epsilon s^(p-2-j)t^j,
epsilon^2=0.
```

The degree-`d` pieces have dimensions `dp+1` and `dp-1`, respectively. The predicted colon
quotient therefore has

```text
H(z)=(1+(2p-2)z+z^2)/(1-z)^2.
```

It is a two-dimensional graded Gorenstein canonical idealization. With `c=2p-2`, the Hilbert
numerator and the absence of cubic generators give

```text
beta_1,2 over the 2p low variables = c(c+1)/2-1 = p(2p-3),
beta_2,3 over the 2p low variables = c(c-2)(c+2)/3
                                      = 8p(p-1)(p-2)/3.
```

Tensoring with the Koszul complex on the `8p` killed high variables predicts

```text
beta_(2,3)(P_p/(Q_p:f_p))
  = 8p*p(2p-3) + 8p(p-1)(p-2)/3
  = 8p(7p^2-12p+2)/3.
```

EXP-030 tests whether the shifted mapping-cone classes are complete and primitive in relative
`H_2` at total degree six. This exact value is a prediction, not a result.

## Path ranking

1. **Colon recognition plus relative `H_2` (selected).** Prove the idealization presentation,
   derive its linear strand, and test completeness by integral relative homology.
2. **Direct relative-chain matching (adversarial route).** Reconstruct every total-degree-six
   offset for small parameters without importing the colon rank calculation.
3. **Whole third-row or full-resolution computation (demoted).** It spends far more memory and
   still cannot prove an all-parameter formula.
4. **Initial-ideal Betti table (bound only).** EXP-029 already shows the available grevlex ideal is
   neither stable nor strongly stable; degeneration cannot certify equality here.
5. **Hilbert-numerator cancellation (insufficient alone).** Internal degree six contains several
   unknown homological entries, so its alternating coefficient cannot isolate `beta_(3,6)`.

## P1-P6 and experiment gates

- **P1 source-complete:** the retained primary sources and fresh sweep do not settle the family.
- **P2 smoke:** `p=4` must emit per-offset progress and a checkpoint before any extension.
- **P3 premises:** every established dependency is tied to EXP-021/023/027/029 above.
- **P4 one-sidedness:** colon agreement alone proves only the colon theorem and a candidate
  mapping-cone contribution. Exact `beta_(3,6)` requires the independent relative-homology gate.
- **P5 invariant-first:** the canonical idealization and its Hilbert series replace a blind raw
  resolution sweep.
- **P6 budget:** smoke budget 120 seconds; canonical small campaign budget 900 seconds; checkpoint
  after every parameter and offset. A budget hit is `INCONCLUSIVE_BUDGET`, not evidence.

Success requires the exact colon presentation, Hilbert series and Betti coefficient; complete
`p=4,5,6` degree-six profiles matching the formula; agreement at `p=4` in two characteristics;
and an integral unit-pivot or Smith argument excluding torsion. Failure of any equality refutes the
corresponding prediction and is preserved before any amended experiment.

## Exploration moment and publication boundary

The new viewpoint is recognition, not enumeration: the cubic colon should be a polynomial
extension of the canonical idealization of a rational normal curve. This would explain the
otherwise opaque factor `8p(7p^2-12p+2)/3` and may expose the colon's complete Betti table.

No manuscript update is triggered by declaration or finite agreement. A proved idealization
theorem plus a characteristic-independent `beta_(3,6)` formula belongs in the existing main
manuscript. A separate manuscript remains deferred unless the idealization determines a
substantial part of the remaining resolution as a distinct theorem.
