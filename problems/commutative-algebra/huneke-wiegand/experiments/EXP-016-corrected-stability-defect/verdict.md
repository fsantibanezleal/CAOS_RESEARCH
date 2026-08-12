# EXP-016 verdict - corrected exact stability defect CONFIRMED

Run date: 2026-08-12. Exact integer and bitset arithmetic, CPU only.

## Result

For every integer `p>=4`, the common trace/conductor ideal from EXP-013 satisfies

```text
v(T_p^2)=(8s+C_p) union [9s,13s-2] union [13s,infinity).
```

The square retains the inherited gap `13s-1` and fills the later endpoint `17s-1`. For
`x=t^(4s)`, the complete quotient has the six residue blocks declared in the hypothesis, and

```text
length(T_p^2/xT_p)=14p.
```

Thus the conductor is quantitatively far from stable: its one-step stability defect grows
linearly and without bound.

## Symbolic proof

The proof in `proof.md` is load-bearing. Five exact low/high residue identities determine levels
8 through 12. The final identity excludes the EXP-015 false point `13s-1`; a separate endpoint
decomposition fills `17s-1`. Subtraction from the exact shift `xT_p` gives block sizes

```text
2p, p, 3p, 6p, 2p-1, 1,
```

whose sum is `14p`.

## Computational and adversarial record

- Both exact routes pass for all 297 parameters `p=4,...,300`.
- Every row retains `13s-1`, fills `17s-1`, and has defect length `14p`.
- A separate implementation rehashes all rows and reconstructs
  `p=4,5,17,73,151,300`.
- Campaign aggregate:
  `8c280bf1db017f678896d473461ae245b4fce57d680be94094b0884556d91853`.
- Audit aggregate:
  `ce4ded03761eb44cba766eafb46926c8ca83d0f7f49a26697afed5ed49905653`.
- `results.json` SHA-256:
  `fde2fcc7cb932dd30bfdf121d43baa28ac1817be118614e485499186f3e43313`.
- `audit.json` SHA-256:
  `a9fc4ab5eb2bd061fa98b27e80e89e381167198cb81fd8e72dd49571810d208b`.
- The EXP-015 false tail, deleted terminal endpoint, and altered `C_p` controls are rejected.

## Prediction ledger

- P1 PASS: the corrected exact square formula is proved.
- P2 PASS: `13s-1` is excluded and `17s-1` is included.
- P3 PASS: the complete defect blocks are proved.
- P4 PASS: the quotient length is exactly `14p`.
- P5 PASS: campaign, independent audit, and corruptions agree.

Verdict: **CONFIRMED**.

## Consequence and scope

EXP-016 strengthens the family anatomy and supplies the correct new material for a manuscript
revision. It must be presented together with EXP-014's source correction: colength balance is
general local duality, while the exact conductor square and its `14p` stability defect are the
family-specific theorem.

The result does not classify all stable trace ideals, all finite birational extensions, or the
Kunz face around the family.

## How could this be wrong?

The proof depends on the EXP-013 conductor blocks. The finite campaign cannot replace the interval
identities. The quotient length is a monomial value-set length over the residually rational
semigroup ring. The theorem has not been journal peer reviewed or formalized in a proof assistant.
