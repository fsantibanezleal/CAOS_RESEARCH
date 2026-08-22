# EXP-033 hypothesis - the complete cubic mapping cone is minimal

Status at declaration: **ACTIVE, NO RESULT CLAIMED**.

## Question and motivation

Retain

```text
A_p=P_p/Q_p,
C_p=P_p/(Q_p,f_p),
D_p=P_p/(Q_p:f_p),
f_p=X_0^2X_(3p)-X_p^3,
```

for every integer `p>=4`. EXP-032 determines every rank and shift in the minimal resolution of
`D_p`, but the exact sequence

```text
0 -> D_p(-3) --f_p--> A_p -> C_p -> 0                         (1)
```

still appears to require the comparison-map ranks. The purpose of EXP-033 is to decide whether
those maps can carry scalar entries at all, before constructing any differential matrix.

## Falsifiable prediction

Put

```text
c=2p-2,      m=8p,      N=10p,
lambda_(c,a)=c*binom(c,a)-binom(c,a+1)-binom(c,a-1).
```

The prediction is

```text
depth(A_p)=1,       pd_(P_p)(A_p)=N-1,       reg_(P_p)(A_p)=2. (2)
```

Consequently every comparison map induced by multiplication by `f_p`,

```text
Tor_i^(P_p)(D_p(-3),k) -> Tor_i^(P_p)(A_p,k),                 (3)
```

is zero for ordinary-degree reasons, and the mapping cone of (1) is minimal over every field:

```text
B_(C_p)(x,z)=B_(A_p)(x,z)+x*z^3*B_(D_p)(x,z).                (4)
```

In particular, the two highest regularity strands of `C_p` are predicted completely:

```text
beta_(i,i+3)(C_p)
  =sum_(a=1)^(c-1) lambda_(c,a) binom(m,i-1-a),               (5)

beta_(i,i+4)(C_p)=binom(m,i-1-c),                             (6)
```

with every out-of-range binomial coefficient interpreted as zero. Formula (6) predicts support
exactly at `2p-1<=i<=10p-1`. It recovers the known terminal values `8p,1`, while (5) recovers the
EXP-028--EXP-031 degree-five, degree-six, and degree-seven anchors.

Any failure of the intersection identity below, a zero divisor `X_0` on the declared kernel, a
kernel Hilbert coefficient outside degrees one and two, `reg(A_p)>2`, a scalar comparison entry,
or disagreement with a frozen Betti anchor refutes the relevant prediction.

## Proposed invariant-first proof

Let

```text
L_p=Q_p:f_p=Q_p+(X_h:h>=6p),
T_p=P_p/(L_p,f_p)=D_p/f_pD_p,
K_p=ker(C_p -> T_p).
```

EXP-030 says that `f_p` is a nonzerodivisor on `D_p`. The proposed route is:

1. Prove the algebraic intersection

   ```text
   Q_p=(Q_p,f_p) intersect L_p.                               (7)
   ```

   The reverse inclusion must use regularity of `f_p` modulo `L_p`; a Hilbert-series equality is
   not accepted as a substitute.
2. Use (7) to obtain the exact pullback sequences

   ```text
   0 -> A_p -> C_p direct-sum D_p -> T_p -> 0,
   0 -> K_p -> A_p -> D_p -> 0.                              (8)
   ```
3. Compute from the frozen Hilbert series

   ```text
   H_(T_p)(z)
     =(1+(2p-1)z+2p z^2+(2p-1)z^3+z^4)/(1-z),
   H_(K_p)(z)=(8p z+10p z^2)/(1-z).                          (9)
   ```
4. EXP-026 makes `X_0` regular on `C_p`, hence on its nonzero submodule `K_p`. Therefore `K_p` is
   one-dimensional Cohen--Macaulay and `reg(K_p)=2`.
5. Since `D_p` is two-dimensional Cohen--Macaulay of regularity two, the second sequence in (8)
   forces `depth(A_p)=1` and `reg(A_p)<=2`. The Hilbert numerator/top Betti coefficient must force
   equality and `beta_(N-1,N+1)(A_p)=10p`.
6. EXP-032 places the shifts of `D_p(-3)` in rows three, four, and five, while (2) places every
   shift of `A_p` in rows at most two. Thus every entry in a lifted comparison map has positive
   degree, proving minimality and (4)--(6).

## Premise verdicts

- EXP-023: accepted for `J_p=(Q_p,f_p)` and the exact cubic.
- EXP-024: accepted for the Hilbert series, projective dimension, regularity, and extremal anchors
  of `C_p`.
- EXP-026: accepted for `X_0`-regularity on `C_p`.
- EXP-030: accepted for `L_p=Q_p:f_p`, the canonical idealization, and regularity of `f_p` on
  `D_p`.
- EXP-032: accepted for the complete Betti polynomial of `D_p`.

Every canonical route must freeze and verify the declared premise hashes before calculation. A
hash mismatch gives `INCONCLUSIVE_PREMISE`, not a mathematical failure.

## Validation routes

### Canonical route

- exact integer arithmetic, CPU only, no randomness and no solver;
- verify (9), the Hilbert series of `A_p`, projective dimension, the terminal coefficient, and
  formulas (5)--(6) for every `p=4,...,300`;
- check every previously proved overlapping value and extremal anchor;
- store complete predicted regularity-three and regularity-four strands for `p=4,5,6`;
- reject wrong shifts, a missing high variable, a filled generator gap, a nonminimal-cone sign,
  and a perturbed terminal rank.

### Independent route

Reconstruct `H_(T_p)` by multiplying `H_(D_p)` by `1-z^3`, obtain `H_(K_p)` by subtraction from
the EXP-024 series, and reconstruct (5)--(6) by literal polynomial multiplication of
`x*z^3*B_(D_p)`. This route must not import the canonical formula functions.

### Structural audit

Write and check the general intersection lemma used in (7), verify the two pullback kernels
directly, and enumerate the degree-one and stable degree-at-least-two offset bases of `K_p` from
the eleven-block definition for the finite audit parameters. Finite enumeration validates the
identification; the written intersection, regular-element, depth, and regularity arguments carry
the all-parameter theorem.

## PASS, FAIL, and one-sidedness

- **PASS** requires the frozen-premise gate, both exact implementations, every adversarial
  control, and a complete written proof of (7)--(6).
- **FAIL** requires a certified counterexample to one of the displayed identities or structural
  steps.
- Finite agreement is one-sided implementation evidence. It cannot establish an all-parameter
  regularity or minimality theorem.

## Budget and kill criterion

- Canonical and independent campaigns: 120 seconds each.
- Structural finite audit: 180 seconds.
- Stop a route as `INCONCLUSIVE_BUDGET` if it crosses its cap; do not optimize an unexpectedly
  large resolution calculation. No raw Gröbner basis or full minimal-resolution sweep is
  authorized in this experiment.

## Publication gate

If confirmed, (4)--(6) determine two complete previously unknown strands of `C_p` and remove the
comparison-map ambiguity from the cubic mapping cone. That crosses the in-place main-manuscript
update gate. A separate manuscript remains deferred unless the proof yields a transferable
minimal-cone criterion beyond this family.
