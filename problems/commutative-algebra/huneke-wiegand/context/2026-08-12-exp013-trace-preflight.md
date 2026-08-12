# EXP-013 trace and conductor preflight

Date: 2026-08-12. This preflight was completed before EXP-013 implementation or execution.

## Exact question

Let `R_p=k[[Gamma_p]]`, let `J_p=(1,t^s)` with `s=6p`, and put
`E_p=End_(R_p)(J_p)=k[[Lambda_p]]`. Determine, for every integer `p>=4`,

```text
tr_(R_p)(J_p),   tr_(R_p)(E_p),   and   R_p:E_p.
```

The equality alone is not an open discriminator here. Since `R_p` is one-dimensional Gorenstein,
its maximal Cohen-Macaulay ideals are reflexive; Lindo-Maitra-Zhang Corollary 5.6 therefore predicts
`tr_R(J_p)=tr_R(E_p)`. The new decision-bearing question is the exact common ideal and its defect.

## Source-complete gate

The relevant theorem and surrounding proof in H. Lindo, S. Maitra, and W. Zhang, *Trace does not
preserve reflexivity*, arXiv:2509.12576v1 and its 2026 version of record, were checked directly.
Corollary 5.6 states the trace/endomorphism criterion for a reflexive ideal in a reduced
one-dimensional Cohen-Macaulay local ring. The archived PDF has SHA-256
`9060c45e4d53b0617c7ad95d77f2b9c3df6662451643890dc6858d012fe5bbcf`.

This changes the route: an experiment merely asking whether the two traces agree would recompute
a consequence already forced by the hypotheses. EXP-013 instead asks for a uniform valuation
formula and an exact colength, neither supplied by that criterion.

## Hand derivation before code

Write the EXP-009 blocks as `A_p`, `B_p`, and `C_p`, and the EXP-011 extra block as

```text
Q_p=[p+1,2p-2] union {2p,4p}.
```

The reflection of `Q_p` across `s-1` is

```text
H_p=(s-1)-Q_p={2p-1,4p-1} union [4p+1,5p-2].
```

The predicted common value ideal is

```text
T_p = (4s+A_p)
      union (5s+([0,s-1] without H_p))
      union (6s+B_p)
      union (8s+C_p)
      union [9s,infinity).
```

Because `[0,s-1] without H_p=A_p union B_p`, its only difference from `Gamma_p` is the zero value
and the `p` values `5s+H_p`. Hence `length(R_p/T_p)=p+1`.

For `W_p=R_p:J_p`, valuation arithmetic gives `tr_R(J_p)=J_p W_p=W_p union (s+W_p)`.
For `R_p:E_p`, every positive `Gamma_p` value automatically handles the isolated top overring
value; the only new obstruction comes from `7s+Q_p`. At level five it excludes exactly the
reflected block `H_p`. This predicts `R_p:E_p=T_p`. Since the conductor is an `E_p`-ideal,
`tr_R(E_p)=E_p(R_p:E_p)=R_p:E_p`.

## Novelty-risk and scope

Fresh exact-formula searches found no primary record matching this family formula. This is only a
novelty-risk check, not proof of novelty. The proposed result classifies these three ideals for the
explicit CAOS family; it does not classify trace ideals of arbitrary rigid modules or solve the
remaining Huneke-Wiegand variants.

## Route decision

The strongest route remains symbolic block arithmetic, followed by two independent finite
reconstructions and adversarial mutations. Nearby-face SAT remains inactive because it is less
direct and cannot prove the all-parameter trace formula.
