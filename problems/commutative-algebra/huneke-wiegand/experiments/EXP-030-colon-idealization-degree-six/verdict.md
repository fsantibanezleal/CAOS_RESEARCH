# EXP-030 verdict - CONFIRMED

## Verdict

**CONFIRMED.** For every integer `p>=4` and every field, the cubic-colon quotient is the canonical
idealization of the `p`th Veronese rational normal curve ring, and

```text
beta_(3,6)(C_p)=8p(7p^2-12p+2)/3.
```

The complete multigraded profile is

```text
beta_(3,(6,b))=[t^(b-3p)](s_p(t)+h_p(t)q_p(t)),
```

with the coefficient polynomials defined in `proof.md`. Its support is

```text
[3p+4,29p-5] minus ([6p-3,6p+1] union [9p-3,9p]),
```

containing `26p-17` offsets. The corresponding integral relative homology is free abelian, so
there is no characteristic exception.

## What was proved

1. The complete colon is

   ```text
   Q_p:f_p=Q_p+(X_h:h in H_p),     |H_p|=8p.
   ```

2. On the `2p` low variables it is the canonical idealization
   `k[s,t]^(p) semidirect omega_(k[s,t]^(p))`, with Hilbert series
   `(1+(2p-2)z+z^2)/(1-z)^2`.
3. The colon's total-degree-three second Betti coefficient is
   `8p(7p^2-12p+2)/3` after the high-variable Koszul extension.
4. Integral relative matching proves that these shifted classes survive primitively and exhaust
   `H_2` in total degree six.

This determines one new third-row entry. It does not determine `beta_(3,7)`, the complete third
row, the full Betti table, or the full minimal resolution.

## Canonical campaign

- Formula and colon checks: all 297 parameters `p=4,...,300`.
- Complete degree-six profiles: `p=4,5,6`.
- Exact totals: `704,1560,2912`.
- Characteristic control: complete `p=4` agreement over `GF(2)` and `GF(1000003)`.
- Runtime: 389.510 seconds, inside the declared 900-second budget.
- Aggregate:
  `de439ff5cf0784b332fcf811b17217579221afca42510f755963c81ff8beaa4d`.

## Independent and symbolic validation

The independently encoded idealization Hilbert numerator reconstructs every offset coefficient and
matches all three canonical profiles exactly. Selected `p=4` complexes at offsets `16,21,37` were
rebuilt over `QQ`, including a zero gap and two nonzero boundaries. Audit aggregate:

```text
bf5034efc37ec23edbd60d87c1eca36d437a9f9fc1e9d38f59816d8a7d3a7a16
```

The symbolic certificate independently verifies coefficient positivity, the two exact support
holes, support count, totals, and divisibility. Symbolic aggregate:

```text
c519356b98ea0c76ec3d49d5f04e3512f711e601fa6491a8bf28dd337454968c
```

## Preserved invalid audit attempt

The first independent audit merged the two blocks `[6p,8p-2]` and `[8p,10p-2]`, incorrectly
inserting the forbidden generator `8p-1`. It therefore produced `8p+1` high variables and a false
`p=4` total of 724. The failure is preserved in
`artifacts/attempt-1-audit-encoding.json` as `INVALID_IMPLEMENTATION`; it is non-evidence. The
corrected implementation keeps the gap, reproduces the required `8p` variables, and passes from a
fresh read of the frozen canonical artifact.

## Adversarial controls

The routes reject:

- omission of the square-zero `BB` relations;
- an offset shift in the `AB` relation fibers;
- `8p-1` or `8p+1` high-variable counts;
- a perturbed idealization Hilbert numerator;
- a perturbed degree-six polynomial; and
- filling either of the two support holes.

## Evidence hashes

| file | SHA-256 |
|---|---|
| `run.py` | `9187cbc9c5d300933a2f5f56540cd511455d2aed44f57ee2ff64bbc4dce9cf29` |
| `audit.py` | `d25bd258eee3eb12b9c4fa69621c64deaac34371d418d3a88249a9fc457af56d` |
| `symbolic_certificate.py` | `a1a5a6c12329105c953f4fd48d3d0e52dc7bc61311b9b976c65695d807e457ea` |
| `artifacts/results.json` | `98ab7f2baaf5315bcdeb51b10555db302a26e90802d53581e3df00379d297ec0` |
| `artifacts/audit.json` | `3aa3393670432f39a455901e2a44d7787c7b5baa37a078e9f1f839a703fdbfa7` |
| `artifacts/symbolic-certificate.json` | `31dbd2b52e719f95369370aa8fe347c5f9c741d6c6c994efedb07b9102e72d23` |

## How could this be wrong?

The load-bearing deductive step is the integral relative normal form: its blockwise least-toggle
argument must exhaust every endpoint without allowing a transient tetrahedron boundary to enter a
declared idealization label. Complete profiles in two characteristics, independent full-profile
agreement, selected rational ranks, and the caught `8p-1` encoding defect strongly test that
boundary, but they are not a proof-assistant certificate. A flaw there could invalidate the
transfer from the proved colon coefficient to `beta_(3,6)`.

The canonical-idealization theorem itself depends only on the exact quadratic fibers, the domain
property of the Veronese ring, and torsion-freeness of its canonical module. It does not depend on
finite campaigns or solver soundness.

## Consequences and next path

- HWB-043 is done.
- The theorem triggers an in-place v0.17 update of the existing main manuscript and a Zenodo new
  version gate; no separate manuscript is yet justified.
- The strongest next mathematical path is the last possible third-row entry `beta_(3,7)`. The
  efficient route is now to determine the next strand of the canonical-idealization resolution and
  its comparison map, not to launch a raw full-resolution sweep.
