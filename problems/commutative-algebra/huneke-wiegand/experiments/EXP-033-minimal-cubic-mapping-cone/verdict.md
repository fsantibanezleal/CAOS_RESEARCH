# EXP-033 verdict - CONFIRMED

Date: 2026-08-22. Backlog: HWB-035.

## Decision

**CONFIRMED.** For every integer `p>=4` and every field, the quadratic quotient

```text
A_p=P_p/Q_p
```

has depth one, projective dimension `10p-1`, and regularity two. Therefore the complete cubic
mapping cone

```text
0 -> D_p(-3) -> A_p -> C_p -> 0
```

is minimal: every shifted source summand lies at least one degree above every possible target
summand. Equivalently,

```text
B_(C_p)(x,z)=B_(A_p)(x,z)+x z^3 B_(D_p)(x,z).
```

This is the relevant result sought by the round. It removes all comparison-map rank ambiguity and
determines the two highest regularity strands of `C_p`:

```text
beta_(i,i+3)
 =sum_(a=1)^(2p-3)
    [(2p-2)binom(2p-2,a)-binom(2p-2,a+1)-binom(2p-2,a-1)]
    binom(8p,i-1-a),

beta_(i,i+4)=binom(8p,i-2p+1).
```

The regularity-three strand is supported at `2<=i<=10p-2`; the regularity-four strand is supported
at `2p-1<=i<=10p-1`. Their total ranks are

```text
2^(8p)((2p-4)2^(2p-2)+2),       2^(8p),
```

respectively.

## Why it works

The complete colon satisfies `L_p=Q_p:f_p`, and EXP-030 makes `f_p` regular modulo `L_p`. This
forces

```text
Q_p=(Q_p,f_p) intersect L_p.
```

The resulting pullback gives `0 -> K_p -> A_p -> D_p -> 0`, where `K_p` is the high-variable
kernel of `C_p -> D_p/f_pD_p`. Exact Hilbert subtraction gives

```text
H_(K_p)(z)=(8p z+10p z^2)/(1-z).
```

The EXP-026 regular element `X_0` stays regular on this submodule, so `K_p` is one-dimensional
Cohen--Macaulay of regularity two. Since `D_p` is two-dimensional Cohen--Macaulay of regularity
two, the depth and regularity lemmas force `depth(A_p)=1` and `reg(A_p)<=2`; its terminal Hilbert
coefficient forces equality and `beta_(10p-1,10p+1)(A_p)=10p`.

EXP-032 puts the shifts of `D_p(-3)` in rows three through five, strictly above all shifts of
`A_p`. Hence every lifted comparison entry has positive degree and the cone is minimal.

## Gate record

| gate | result |
|---|---|
| declaration before implementation | PASS; declaration commit `908ee10` precedes implementation commit `a5fc321` |
| frozen premises | PASS; all six EXP-023/024/026/030/032 hashes match |
| canonical campaign | PASS for all 297 parameters in 15.159 seconds |
| independent coefficients | PASS; every regularity-three/four array hash and total matches |
| structural kernel audit | PASS at `p=4,...,25,50,100,300` |
| symbolic identities | PASS through `p=300` after generic simplification |
| prior Betti anchors | PASS; EXP-024 and EXP-028--031 overlaps all agree |
| adversarial controls | PASS; wrong shift, high-variable mutations, sign, terminal rank, section h-vector, and kernel interval are rejected |
| all-parameter proof | PASS; intersection, pullback, CM kernel, regularity gap, and graded minimality are deductive |

Aggregates:

```text
canonical    67bff9217c89f212916220e858ef5168abe2d64cdbd789488e0ce5f49204092a
independent  6593291efaf092333bc42972c2f05712a151efb46f3f52ed9d28afd329585a4c
symbolic     58ab24887c79c3c075fdefea1f38ff2e1c1ef539490f7f52359149ed2bb1a4c8
```

## Preserved budget stops

Three complete-formula implementations stopped at `p=102`, `p=209`, and `p=267` under the exact
120-second cap. They are preserved as `INCONCLUSIVE_BUDGET` and carry no theorem evidence. The
successive recurrence implementations reproduce all earlier row hashes; the final run completes
all 297 rows inside budget.

## Scope and next frontier

The Huneke--Wiegand conjecture was already disproved by Son Pham's public counterexample; EXP-033
does not claim that discovery or solve a broader classification. It proves a new structural
theorem for the CAOS infinite counterexample family.

The complete Betti table of `C_p` is still not known. After EXP-033, its only unresolved data are
the two lower strands inherited from `A_p=P_p/Q_p`. The strongest next route is the exact sequence
`0 -> K_p -> A_p -> D_p -> 0`: determine the comparison maps between the now explicit
regularity-two modules `K_p` and `D_p`, rather than returning to the cubic cone or launching a raw
full-resolution sweep.

## Publication decision

The trigger is crossed. A complete minimal-cone theorem plus two complete Betti strands materially
extends the main manuscript and should open an in-place v0.20/Zenodo-version gate. A separate
manuscript is still premature unless the next round produces a transferable resolution theorem
for the high-variable kernel or the full table.
