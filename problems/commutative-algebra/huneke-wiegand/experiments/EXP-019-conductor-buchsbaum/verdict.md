# EXP-019 - verdict

Status: **CONFIRMED** on 2026-08-12.

## Theorem

For every integer `p>=4`, the conductor tangent cone

```text
G_p=gr_(T_p)(R_p)
```

is Buchsbaum but not Cohen--Macaulay. With `M_p` its homogeneous maximal ideal and

```text
H_p={2p-1,4p-1} union [4p+1,5p-2],
```

its complete zeroth local cohomology is

```text
H^0_(M_p)(G_p)
 = span_k{t^(5s+h)+T_p : h in H_p}
 isomorphic to k^p,
```

concentrated in degree zero, and

```text
M_p H^0_(M_p)(G_p)=0.
```

Thus the Buchsbaum invariant is `I(G_p)=p`, which is unbounded in the family. The quotient by its
complete finite-length torsion is Cohen--Macaulay with Hilbert series

```text
(1+(10p-1)z+12p z^2+(2p-1)z^3+z^4)/(1-z).
```

## Why the theorem follows

- The homogeneous colon-saturation formula identifies degree-`n` torsion with classes whose
  values survive the stable threshold `4(n+1)s`.
- Exact conductor-power profiles leave precisely `5s+H_p` in degree zero and no class in any
  positive degree.
- Both parts of the homogeneous maximal ideal were checked. The degree-zero part `m_p/T_p` sends
  every torsion representative into `T_p`; the positive part sends it into `T_p^2`.
- The only missing value at or above `9s` is `13s-1`, and attaining it would require a ring value
  strictly between levels `7s` and `8s`, where the exact ring profile is empty.
- The one-dimensional local-cohomology criterion therefore proves Buchsbaumness; EXP-018 supplies
  depth zero and non-Cohen--Macaulayness.

## Exact evidence

- Mandatory `p=4` smoke gate: PASS before creation of the campaign artifact.
- Complete two-route campaign: `p=4,...,300`, 297 rows, PASS in 41.146260 seconds.
- Campaign aggregate:
  `854d7889d9d7b911b462e4d483e021210ae2873ae0ec0091ec30e8fb29d6dbf7`.
- Independent bounded-bitset reconstructions: `p=4,5,17,73,151,300`, PASS.
- Independent audit aggregate:
  `0b01853febc9e9754e28abcd099a7ae3a97f4cc0ab92f3a345ab2ae03cd3c68a`.
- `results.json` SHA-256:
  `d0754006ad1b3426d6288748dd01604cccdc24b0008ff1bff74c1643fbaa2c18`.
- `audit.json` SHA-256:
  `d8ffc3598f2fed67aa7dee22f0d90c1eed21ec91a8b49f5462dee5d86b90bbbc`.
- `ruff` and Python byte-compilation checks: PASS.

## Adversarial controls

The campaign rejects a unit torsion class, deletion of the first genuine class, injected
positive-degree torsion, replacement of `m_p/T_p` by a degree-zero ideal containing the unit, the
false invariant `p-1`, and a perturbed quotient numerator. The independent audit separately checks
the unit, length, positive-degree, degree-zero-action, and false non-Buchsbaum corruptions.

## Scope

This is an exact theorem about the conductor filtration in the explicit EXP-009 family. It does
not classify Buchsbaum tangent cones of arbitrary ideals or arbitrary numerical-semigroup rings.
The symbolic proof is load-bearing; the finite campaign is reproducibility evidence.
