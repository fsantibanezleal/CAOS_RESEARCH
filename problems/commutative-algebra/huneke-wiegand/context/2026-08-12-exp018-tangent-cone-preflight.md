# EXP-018 preflight - conductor tangent cone

Date: 2026-08-12.

## Why this path is next

EXP-017 determines the complete reduction sequence of the conductor `T_p` with respect to
`Q_p=t^(4s)R_p`, but reduction number and Hilbert coefficients do not decide the depth of the
associated graded ring

```text
G_p=gr_(T_p)(R_p)=direct_sum_(n>=0) T_p^n/T_p^(n+1).
```

Valabrega--Valla's original criterion says, in this one-dimensional Cohen--Macaulay setting, that
the initial form of the regular reduction generator is regular on `G_p` exactly when

```text
Q_p intersect T_p^(n+1) = Q_p T_p^n
```

for every `n>=0`. See P. Valabrega and G. Valla, *Form rings and regular sequences*, Nagoya
Mathematical Journal 72 (1978), 93--101,
`https://doi.org/10.1017/S0027763000018225`. The criterion supplies the structural gate only; it
does not compute any intersection for this family.

## Scouting boundary

A disposable exact-value calculation at `p=4,5,6,17` found a nonzero intersection defect only at
`Q_p intersect T_p^2`, with observed lengths `4,5,6,17`. It suggested the level-nine residue block

```text
{2p-1,4p-1} union [4p+1,5p-2].
```

This calculation is discovery scouting only. It is not a committed artifact and is not evidence
for EXP-018. The experiment below is declared before its formal implementation, campaign, audit,
or symbolic proof.

## Hypothesis selected

Predict that the complete Valabrega--Valla module is concentrated in its first tested degree:

```text
(Q_p intersect T_p^2)/(Q_pT_p) has length p,
Q_p intersect T_p^(n+1) = Q_pT_p^n for n=0 and every n>=2.
```

Consequently `G_p` should have depth zero and fail to be Cohen--Macaulay for every `p>=4`, even
though its Hilbert numerator has only positive coefficients. Computing that numerator exactly is
part of the experiment, because it records why Hilbert-series positivity alone misses the defect.

The competing paths are lower priority:

- extending the parameter sweep beyond `p=300` cannot decide a graded-depth theorem;
- nearby-face SAT has no comparably sharp finite target;
- another immutable manuscript version is premature until the structural result is proved,
  audited, and assessed against the existing v0.07 claims.
