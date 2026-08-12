# EXP-017 - exact conductor reduction number and Hilbert data

Status: DECLARED before formal implementation or execution on 2026-08-12.

## Objects

For every integer `p>=4`, retain `s=6p`, the one-dimensional Gorenstein semigroup ring `R_p`,
the finite birational extension `E_p`, and its conductor `T_p=R_p:E_p` from EXP-013. Put

```text
Q_p = t^(4s) R_p subset T_p.
```

## Falsifiable hypothesis

`Q_p` is a minimal reduction of the `m_p`-primary ideal `T_p`, with exact reduction number four:

```text
T_p^2 != Q_p T_p,
T_p^3 != Q_p T_p^2,
T_p^4 != Q_p T_p^3,
T_p^5  = Q_p T_p^4.
```

The complete successive quotient lengths are predicted to be

```text
length(T_p/Q_p)                 = 23p-1,
length(T_p^2/Q_p T_p)           = 14p,
length(T_p^3/Q_p T_p^2)         = 2p,
length(T_p^4/Q_p T_p^3)         = 1,
length(T_p^(n+1)/Q_p T_p^n)     = 0  for every n>=4.
```

More strongly, the two new nonzero value-set differences are predicted to be

```text
v(T_p^3) minus v(Q_p T_p^2)
  = 12s + ([2p+1,3p-1] union [5p-1,6p-2]) union {17s-1},

v(T_p^4) minus v(Q_p T_p^3) = {17s-1}.
```

Consequently, the one-dimensional Hilbert-Samuel coefficients should be

```text
e_0(T_p)=24p,
e_1(T_p)=39p,
```

where the `e_1` identity must be derived directly from the exact eventual Hilbert function, not
asserted from a citation alone.

## Required proof and evidence

1. Derive exact value-block formulas for `T_p/Q_p`, `T_p^3/Q_pT_p^2`, and
   `T_p^4/Q_pT_p^3`; EXP-016 supplies the square layer only.
2. Prove `T_p^5=Q_pT_p^4` and induction for every later power.
3. Prove `Q_p` is a minimal reduction and that the two strict inequalities force reduction number
   exactly four.
4. Derive the eventual Hilbert function and both coefficients from finite colength counts.
5. Run two exact implementations for every `p=4,...,300`, with the `p=4` smoke gate before the
   campaign artifact is created.
6. Run an independently written audit at `p=4,5,17,73,151,300` and rehash all campaign rows.

## Adversarial controls

- delete the terminal value `17s-1` from the cubic or quartic defect;
- force false stabilization at power three or four;
- alter either affine interval in the cubic defect;
- perturb one claimed quotient length while preserving the others.

Every corruption must be rejected.

## Budget and verdict rule

- CPU only; exact integer/bitset arithmetic; no randomness;
- two minutes for the full campaign and one minute for the independent audit;
- `CONFIRMED` requires the symbolic proof, both complete exact routes, all controls, stable hashes,
  and the independent audit;
- a smoke mismatch preserves this declaration as `REFUTED` or triggers a separately numbered
  corrected hypothesis before any broad campaign.

