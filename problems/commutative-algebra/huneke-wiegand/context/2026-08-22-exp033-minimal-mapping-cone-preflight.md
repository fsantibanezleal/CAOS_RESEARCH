# EXP-033 preflight - minimal cubic mapping cone

Date: 2026-08-22. Scope: HWB-035 and the new mapping-cone gate.

## Redirect decision

The prior handoff proposed constructing comparison maps between resolutions of `D_p` and
`A_p=P_p/Q_p`. The stronger invariant-first route is to determine `reg(A_p)` before constructing
those maps. If `reg(A_p)=2`, ordinary grading separates every source shift of `D_p(-3)` from every
target shift of `A_p`, so all comparison maps are Tor-zero and the entire cubic mapping cone is
minimal. This dominates a matrix-by-matrix rank campaign.

The new viewpoint is the pullback

```text
A_p=C_p times_(D_p/f_pD_p) D_p,
```

whose high-variable kernel has Hilbert numerator `8p z+10p z^2`. The analogy is a Betti-splitting
or mapping-cone argument, but no external theorem is being imported to assert minimality: the
load-bearing proof is the family-specific intersection identity plus the regularity gap.

## Frozen premises

| premise | SHA-256 | use |
|---|---|---|
| EXP-023 `proof.md` | `4f24c8bacf3ea4a7691142b6fbb2a79b40a1c200ec5051df3c79c3dc45bed084` | `J_p=(Q_p,f_p)` |
| EXP-024 `proof.md` | `b7b654609cfca99e979b26741f7d2b6bbbfc0029d882c38e3c2932bfc9146088` | Hilbert series and extremal Betti anchors |
| EXP-026 `proof.md` | `765fa23534be9e534fd507dff0e447e967345e4d2a485f7da6fdf0383b04fb56` | `X_0` is regular on `C_p` |
| EXP-030 `proof.md` | `1822095a7d16207b7d04261b7a6645f7ca51b01f490ba9d212a84ab7ca5bc729` | complete colon and `f_p` regular on `D_p` |
| EXP-032 `proof.md` | `4dc37605c012b7f6a70ec5d383897c45a34e1dd5d5e4bb32a0582b7a6d651d1c` | complete Betti polynomial of `D_p` |
| EXP-032 `verdict.md` | `3a04956262708ebb09b14c8a1628194dd0c7a21ca6171247e518b8cc4b98d7cc` | exact scope boundary |

## Online primary-source sweep

The 2026-08-22 sweep checked the following primary research records:

- Dochtermann--Mohammadi, *Cellular resolutions from mapping cones*,
  `https://arxiv.org/abs/1311.4599`, for the general principle that adding a generator is resolved
  by a lifted mapping cone and that minimality is a property of the chosen comparison map;
- Bolognini, *Betti splitting via componentwise linear ideals*,
  `https://arxiv.org/abs/1410.6511`, for the Tor-vanishing/Betti-splitting viewpoint;
- Autry--Graves--Loucks--O'Neill--Ponomarenko--Yih,
  *Squarefree divisor complexes of certain numerical semigroup elements*,
  `https://arxiv.org/abs/1804.06632`, for the multigraded divisor-complex perspective; and
- Stamate, *Betti numbers for numerical semigroup rings*,
  `https://arxiv.org/abs/1801.00153`, for the numerical-semigroup Betti landscape.

These sources support the comparison vocabulary and alternative computational lenses. None
contains the family-specific pullback, kernel Hilbert series, regularity-two theorem, or formulas
declared in EXP-033. Novelty remains subject to a broader literature review if the theorem is
confirmed.

## Self-questioning and failure routes

1. Could `Q_p=(Q_p,f_p) intersect (Q_p:f_p)` fail? Yes in general; the proposed proof must use
   that `f_p` is a nonzerodivisor modulo its colon quotient.
2. Could the high-variable kernel have hidden `X_0`-torsion? Not if the EXP-026 regularity premise
   is used correctly, but the inclusion into `C_p` must be explicit.
3. Could `reg(A_p)<=2` still permit scalar cancellations? No: after the cubic shift, every source
   summand has row at least three, while every target summand has row at most two.
4. Could a minimal mapping cone still leave the full Betti table unknown? Yes. It determines all
   of `C_p` once `A_p` is known and immediately determines the regularity-three and
   regularity-four strands, but the two lower strands of `A_p` remain the next frontier.
5. If the regularity prediction fails, fall back to explicit offset-graded comparison ranks only
   on the first nonzero overlap; do not launch a raw full resolution.

## Manuscript decision before results

A confirmed complete minimal-cone theorem and two complete new Betti strands belong in the
existing main manuscript. The companion curvilinear paper is not the right destination, and a
third paper would be premature unless a general transferable theorem emerges.
