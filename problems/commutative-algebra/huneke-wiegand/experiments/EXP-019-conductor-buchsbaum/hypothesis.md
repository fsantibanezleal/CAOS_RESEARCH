# EXP-019 - conductor tangent cone is Buchsbaum

Status: DECLARED before formal implementation or execution on 2026-08-12.

## Objects

For every integer `p>=4`, retain `s=6p`, the ring `R_p`, its maximal ideal `m_p`, conductor ideal
`T_p`, and tangent cone

```text
G_p=gr_(T_p)(R_p),
M_p=(m_p/T_p) direct-sum G_(p,+).
```

Put `H_p={2p-1,4p-1} union [4p+1,5p-2]`.

## Falsifiable hypothesis

The complete zeroth local cohomology is predicted to be

```text
H^0_(M_p)(G_p)
  = span_k{t^(5s+h)+T_p : h in H_p}
  isomorphic to k^p,
```

concentrated in degree zero. Its annihilator contains the full homogeneous maximal ideal:

```text
M_p H^0_(M_p)(G_p)=0.
```

Consequently `G_p` is Buchsbaum but not Cohen--Macaulay, and its one-dimensional Buchsbaum
invariant is

```text
I(G_p)=length(H^0_(M_p)(G_p))=p.
```

The Cohen--Macaulay quotient `G_p/H^0_(M_p)(G_p)` is predicted to have Hilbert series

```text
(1+(10p-1)z+12p z^2+(2p-1)z^3+z^4)/(1-z).
```

## Required proof and evidence

1. Prove the general homogeneous colon-saturation description
   `H^0_n=union_k ((T^(n+k+1):T^k) intersect T^n)/T^(n+1)` in this filtration.
2. Use the exact stabilized tails `v(T^k)=[4ks,infinity)` for `k>=4` to reduce saturation to the
   threshold `v>=4(n+1)s`.
3. Compare the threshold with every exact power profile and prove that only degree zero survives,
   with value set `5s+H_p` and length `p`.
4. Check both parts of the homogeneous maximal ideal: `(m_p/T_p)` kills the torsion in degree zero,
   and `G_(p,+)` kills it into `T_p^2`.
5. Apply the one-dimensional local-cohomology criterion to prove Buchsbaumness and compute the
   invariant and Cohen--Macaulay quotient series.
6. Run two exact implementations for every `p=4,...,300`, starting with a mandatory `p=4` smoke
   gate, and an independently written audit at `p=4,5,17,73,151,300` that rehashes every row.

## Adversarial controls

- insert the unit class into degree-zero torsion;
- delete the first predicted torsion class;
- inject a false positive-degree torsion class;
- omit the `(m_p/T_p)` part of the annihilator test;
- perturb the Buchsbaum invariant from `p` to `p-1`;
- perturb the Cohen--Macaulay quotient numerator.

Every corruption must be rejected.

## Budget and verdict rule

- CPU only; exact integer/bitset arithmetic; no randomness;
- two minutes for the full campaign and one minute for the independent audit;
- `CONFIRMED` requires the symbolic proof, two complete exact routes, all controls, stable hashes,
  and the independent audit;
- a `p=4` mismatch preserves this declaration as `REFUTED` or triggers a separately numbered
  corrected hypothesis before any broad campaign.
