# EXP-023 - one-cubic defining ideal

Status: DECLARED before implementation or execution on 2026-08-17.

## Question

Is the universal EXP-022 cubic the only nonquadratic minimal equation of the conductor special
fiber for every `p>=4`?

## Falsifiable predictions

With `J_p=ker(S_p->F(T_p))`, `K_p=(J_p)_2S_p`, and
`F_p=X_0^2X_(3p)-X_p^3`:

- P1: `J_p=(K_p,F_p)`.
- P2: the complete first Betti row is

```text
beta_(1,2)=50p^2-17p,
beta_(1,3)=1,
beta_(1,j)=0 for every j>=4.
```

- P3: the relation type is three and `mu(J_p)=50p^2-17p+1`.
- P4: `F(T_p)` is Cohen--Macaulay and non-Koszul for every `p>=4`.

## Evidence required

1. Reproduce EXP-022's `p=4,5,6` first Betti rows with the independent state graph.
2. Complete a bounded exact campaign with checkpointed, hashed rows and adversarial controls.
3. Prove the degree-three interval graphs have one component except the two components joined by
   `F_p` at total `3p`.
4. Prove degrees four and five contribute no new component.
5. Invoke the published degree-five source bound only after checking all hypotheses.

## Verdict rule

An extra cubic component, or any degree-four/five component, refutes P1/P2 and must be preserved.
A finite pass is not a theorem. `CONFIRMED` requires the symbolic component proof plus an
independent exact audit. Budget exhaustion is `INCONCLUSIVE`.

## Adversarial controls

- omit the edge joining the two `t=3p` components after adjoining `F_p`;
- introduce a false second cubic component;
- suppress a zero-state edge;
- perturb the quadratic count or total equation count by one;
- falsely mark the algebra Koszul despite the necessary cubic.

## Lenses

- factorization graph and primitive additive circuit;
- exact degreewise systematic exclusion;
- Artinian multiplication automaton;
- source-backed relation-degree completeness;
- adversarial component corruption.
