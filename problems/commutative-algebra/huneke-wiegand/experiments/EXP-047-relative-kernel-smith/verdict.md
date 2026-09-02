# EXP-047 verdict

Status: **CONFIRMED FINITELY** for `p=8,...,11`; P1, P2, and P3 pass.

The exact row-inclusion kernel modules are

```text
Q_p(58,59) = Z^binom(p-2,2) direct-sum (Z/2Z)^2,
Q_p(58,62) = Z^(p^2-4p-3) direct-sum (Z/2Z)^2,
Q_p(56,58) = Z^f_p direct-sum (Z/2Z)^(p-7)
```

on the tested range, with `f_p=rows(R1)-(3p-7)`. Exact transformed-Hermite kernel bases and Smith
forms establish the primary result. An independent 202-check audit proves the rational-rank
ceilings and top determinantal divisors by 61-bit modular/Hadamard certificates and explicit
Bareiss minors, excluding odd torsion and factors divisible by four.

This upgrades the carrier lattice from Bockstein rank patterns to exact integral relative modules.
Both alternative completions contribute precisely the same two elementary factor-two classes,
despite different free ranks, and the threshold quotient contributes exactly `p-7` such classes.

The result remains finite and the HNF basis has not yet been converted into a uniform semantic
chain map. The next gate is a certificate-producing unimodular reduction to the predicted
`I direct-sum 2I` forms and a symbolic classification of its pivots. No manuscript or Zenodo
update is triggered yet.
