# EXP-038 verdict

Status: **INCONCLUSIVE** for the all-parameter claims; **both finite gates pass**.

The complete, exact, independently audited targets give

```text
e_11=8688-8586=102,
e_12=16822-16684=138.
```

These were declared before the corresponding blocks were computed.  Low-degree and canonical
residual orders agree over `GF(2)`, and `GF(3)` agrees with `GF(5)`.  Thus the corrected series

```text
(1+2x+x^2+x^3-x^6)/((1-x)^2(1-x^2)(1-x^3))
```

survives its first two out-of-sample tests.  The exact finite sequence through `p=12` is
`1,4,9,18,31,49,72,102,138`.

This does not confirm P1 or P2.  No explicit degree-six relation, translation law, or proof of the
order-seven recurrence has been obtained.  The remaining failure modes are a common basis-model
error, an accidental finite fit, later corrections, and torsion not detected by the two odd
primes.  The next experiment must inspect the connected/local block structure of the combined
signed core and attempt to extract a bounded relation template; another large coefficient alone
is secondary.

The result transfers from `A_p` to `C_p` at the tested targets by EXP-036's all-parameter absence
of the shifted cubic source.  It does not complete either lower strand or resolve the
Huneke-Wiegand conjecture.  Without an all-parameter structural theorem, manuscript v0.24 and a
new Zenodo version remain closed.
