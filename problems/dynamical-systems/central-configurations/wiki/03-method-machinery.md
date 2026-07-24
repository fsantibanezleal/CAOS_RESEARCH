# 03 - Method machinery: the Albouy-Chenciner system and the exclusion certificates

Transcribed from `../context/2026-07-23-hampton-moeckel-method-dossier.md` (built from
the Hampton-Jensen 2011 PDF, read in full front matter; HM06 statements are tagged
[HM-via-HJ11] until the Inventiones PDF is read, backlog CCB-002).

## The polynomial system (mutual distances)

Variables $r_{ij}$; $S_{ij} = r_{ij}^{-3} + \Lambda$ with $\Lambda = -1$ fixed (scale
normalization; $S_{ii} = 0$). After clearing denominators everything is polynomial:

- **Symmetric Albouy-Chenciner** (Albouy-Chenciner 1998; the core):
  $$f_{ij} = \sum_{k=1}^{n} m_k \left[ S_{ik}(r_{jk}^2 - r_{ik}^2 - r_{ij}^2) + S_{jk}(r_{ik}^2 - r_{jk}^2 - r_{ij}^2) \right] = 0.$$
- **Asymmetric (Roberts)**: $g_{ij} = \sum_k m_k S_{ik}(r_{jk}^2 - r_{ik}^2 - r_{ij}^2) = 0$,
  with $f_{ij} = g_{ij} + g_{ji}$ (a strictly finer valid set).
- **Dziobek** (dimension $n-2$ stratum):
  $h_{ijkl} = (r_{ij}^{-3} - 1)(r_{kl}^{-3} - 1) - (r_{ik}^{-3} - 1)(r_{jl}^{-3} - 1) = 0$.
- **Cayley-Menger**: the bordered determinant $e_{CM} = 0$ enforces realizability in the
  target dimension (planar for 4 points: the 5x5 determinant; spatial for 5 points: 6x6).
- **Energy-inertia**: $e_{IU} = U - M I = 0$ (redundant, kept for symmetry).

## The finiteness logic (HM06 / HJ11)

1. Shub compactness: solutions stay in the torus (all $r_{ij} \ne 0, \infty$ after
   normalization). An infinite CC family forces a positive-dimensional component of the
   variety $V(I)$ in $(\mathbb{C}^*)^{\binom{n}{2}}$.
2. A positive-dimensional component in the torus forces a nonzero weight vector $\omega$
   (a Puiseux valuation profile; HM06 Prop. 2, equivalently the fundamental theorem of
   tropical geometry) in the tropical variety $T(I)$, with $\sum_i \omega_i \ge 0$ after
   the scale normalization.
3. **Certificate**: compute all candidate directions (HM06: from Newton polytopes / BKK;
   HJ11: the tropical prevariety via Gfan; for their 42-equation spatial 5-body system
   the prevariety has f-vector (1, 576, 1620, 1420, 450), reduced to 44 cases by symmetry
   and the halfspace condition), then kill each direction by exact computation: the
   initial-form ideal, saturated by $\prod r_{ij} \prod m_i$, is shown to contain 1, or
   to force a positive-mass-impossible condition (a sum of masses vanishing).
4. Directions that survive yield EXPLICIT exceptional mass conditions (AK12's codim-2
   subvariety at $n = 5$; HJ11's Table 1 spatially; Chang-Chen's 24 residual diagram
   cases at $n = 6$). BKK also yields the count bound (8472 for $n = 4$).

## Certification stack (for fixed-mass listings and numerics)

- Krawczyk operator + interval arithmetic (Moczurad-Zgliczynski's instrument: a priori
  compact search region, exclusion tests, Krawczyk existence + local uniqueness).
- Smale's alpha theory: alphaCertified (Hauenstein-Sottile, ACM TOMS 2012, exact
  rational arithmetic); interval certification in HomotopyContinuation.jl
  (Breiding-Rose-Timme, arXiv:2011.05000); certified tracking arXiv:2402.07053.
- Cross-paper matching invariant: $J = U I^{1/2} / M^{5/2}$ (MZ19 eq. 66).

Our implementations: EXP-001 builds the exact system; the mixed-volume and prevariety
instruments are staged (backlog CCB-007, CCB-008).
