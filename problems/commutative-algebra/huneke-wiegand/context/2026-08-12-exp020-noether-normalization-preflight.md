# EXP-020 preflight - Noether-normalization module anatomy

Date: 2026-08-12.

## Exploration result and path selection

EXP-019 determines the complete finite-length torsion of

```text
G_p=gr_(T_p)(R_p),
```

but it does not describe the complete graded module carried by the minimal reduction. A fresh
primary-source sweep found a more decisive next view than a generic comparison bound for the
Buchsbaum invariant. Cortadellas Benitez and Zarzuela decompose tangent cones over the polynomial
Noether normalization determined by a minimal reduction and recover graded Betti data from that
module structure:

- T. Cortadellas Benitez and S. Zarzuela Armengou, *Tangent cones of numerical semigroup rings*,
  arXiv:0906.0911, `https://arxiv.org/abs/0906.0911`.
- T. Cortadellas Benitez and S. Zarzuela Armengou, *On the structure of the fiber cone of ideals
  with analytic spread one*, Journal of Algebra 317 (2007), 759--785,
  `https://doi.org/10.1016/j.jalgebra.2007.02.044`.

The first paper is specific in its explicit Apery formulas to the maximal-ideal filtration of a
numerical semigroup ring. The present object is the conductor filtration, so those formulas will
not be imported verbatim. Only the general viewpoint is used: EXP-017 makes

```text
F_p=k[x_p],  x_p=(t^(4s))^*,
```

a polynomial Noether normalization of `G_p`; the graded structure theorem over the principal
ideal domain `F_p` can then be proved directly from the exact conductor-power Apery table.

The downloaded primary-source PDF is stored outside Git at
`E:/_Datos/caos-research/huneke-wiegand/sources/exp020/cortadellas-zarzuela-0906.0911.pdf`.
It has 179,401 bytes and SHA-256
`131acf343f480c4abf45b19ac4fcd8146e990233e0ec3fb37f2a92efe8b57767`.

## Premise audit

The proposed theorem depends only on already confirmed CAOS results:

1. EXP-017: `Q_p=t^(4s)R_p` is a minimal reduction of `T_p`, with reduction number four and
   `e0(T_p)=24p`.
2. EXP-018: the exact Hilbert numerator of `G_p` is
   `(p+1)+(9p-1)z+12pz^2+(2p-1)z^3+z^4`.
3. EXP-019: the `F_p`-torsion is `H^0=k^p` in degree zero, `x_p` kills it, and the quotient by it
   is Cohen--Macaulay with numerator
   `1+(10p-1)z+12pz^2+(2p-1)z^3+z^4`.

No unverified literature statement is needed for the family-specific decomposition. The graded
PID argument and the conductor-power Apery-column reconstruction will both be written in full.

## Invariant-first prediction

Since `G_p/H^0` is a finite torsion-free module over `F_p=k[x_p]`, it is graded free. Its Hilbert
numerator fixes every free shift. Since `H^0` is killed by `x_p` and concentrated in degree zero,
the predicted complete decomposition is

```text
G_p isomorphic to
  (F_p/(x_p))^p
  direct-sum F_p
  direct-sum F_p(-1)^(10p-1)
  direct-sum F_p(-2)^(12p)
  direct-sum F_p(-3)^(2p-1)
  direct-sum F_p(-4).
```

This predicts the minimal graded `F_p`-resolution

```text
0 -> F_p(-1)^p ->
     F_p^(p+1) direct-sum F_p(-1)^(10p-1) direct-sum F_p(-2)^(12p)
     direct-sum F_p(-3)^(2p-1) direct-sum F_p(-4)
   -> G_p -> 0,
```

where the first map is `x_p` on the `p` torsion generators. In particular,

```text
pd_(F_p)(G_p)=1,
reg_(F_p)(G_p)=4,
a(G_p)=3,
length(G_p/x_pG_p)=25p=e0(T_p)+I(G_p).
```

The final equality packages the entire Buchsbaum defect as the excess of a minimal-reduction
section over multiplicity. It also gives the exact proportionalities
`I(G_p)=e0(T_p)/24=e1(T_p)/39=length(R_p/T_p)-1` inside this family.

## Alternatives evaluated

- A general upper bound for `I(G_p)` in terms of `e0`, `e1`, or reduction number would give only
  an inequality here. The exact module structure recovers all of those data and is stronger.
- Rees-algebra local cohomology may reveal a second layer beyond `G_p`, but it requires a new
  source and premise pass. It remains a later path after the complete `F_p`-module is settled.
- Nearby Kunz-face classification remains broader and more expensive. It is not justified while
  the known family still yields a finite exact structural target.

## Validation and cost gate

EXP-020 will use two exact routes for every `p=4,...,300`:

1. reconstruct the full conductor-power Apery table modulo `24p`, split each column into its
   finite and infinite strings under multiplication by `x_p`, and count cyclic summands;
2. derive the torsion and free shifts independently from EXP-018/019 Hilbert numerators.

An independently written audit will reconstruct selected parameters, rehash every row, and reject
mutations of the torsion exponent, a free-shift count, the first Betti number, regularity, and the
minimal-reduction-section length. CPU only, exact integer arithmetic, two-minute campaign budget,
one-minute audit budget. The symbolic proof remains load-bearing.
