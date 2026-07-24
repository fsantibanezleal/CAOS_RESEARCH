# Method dossier: the Hampton-Moeckel finiteness certificate (and the Hampton-Jensen tropical variant)

Date: 2026-07-23. Purpose: transcribe, at implementation level, the machine-assisted
method that proved Smale 6 for n = 4 (Hampton-Moeckel, Invent. Math. 163 (2006) 289-312)
and its tropical refinement used for the spatial 5-body case (Hampton-Jensen, Cel. Mech.
Dyn. Astron. 109 (2011) 321-332). Primary basis for this transcription: the Hampton-Jensen
PDF (read in full front matter during this pass), which states verbatim that "Our proof
strategy will be the same as that of Hampton and Moeckel (2006)", replacing BKK language
by tropical language; plus Moeckel's Lectures on Central Configurations (PDF read).
The Inventiones PDF itself is not yet in our hands: every statement attributed to HM06
below is tagged [HM-via-HJ11] or [HM-via-notes] accordingly, and the direct read is a
backlog item (CCB-002).

## 1. The equations (exact polynomial forms, ready to implement)

Variables: mutual distances $r_{ij}$, $1 \le i < j \le n$ (so $\binom{n}{2}$ variables),
masses $m_i$ as parameters. Set $S_{ij} = r_{ij}^{-3} + \Lambda$; the homogeneity of the
CC equations lets one fix $\Lambda = -1$ without loss of generality (this fixes scale)
[V: HJ11 Section 3].

**Symmetric Albouy-Chenciner equations** (the core system; originally from
Albouy-Chenciner 1998, "Le probleme des n corps et les distances mutuelles",
Invent. Math. 131 (1998) 151-184 [Vs: cited in HJ11 and Moeckel notes]):

$$f_{ij} = \sum_{k=1}^{n} m_k \left[ S_{ik}\,(r_{jk}^2 - r_{ik}^2 - r_{ij}^2) + S_{jk}\,(r_{ik}^2 - r_{jk}^2 - r_{ij}^2) \right] = 0$$

for $1 \le i < j \le n$; polynomial after multiplying through by $\prod r^3$ (clearing
the $r^{-3}$ in the $S$). [V: HJ11 eq. (3), PDF read.] Denote the set $\mathcal{F}$.

**Asymmetric (Roberts) AC equations**: a more restrictive valid set observed by Roberts
(HJ11 cite "Roberts 2009" [U: which Roberts paper exactly]):

$$g_{ij} = \sum_{k=1}^{n} m_k\, S_{ik}\,(r_{jk}^2 - r_{ik}^2 - r_{ij}^2) = 0,$$

for ordered pairs $i \ne j$ ($n(n-1)$ equations; $f_{ij} = g_{ij} + g_{ji}$). Both sets
were kept in HJ11 to refine the tropical computation. [V: HJ11 eq. (4).]

**Dziobek equations** (valid on the Dziobek stratum, dim = n - 2; Dziobek 1900):

$$h_{ijkl} = (r_{ij}^{-3} - 1)(r_{kl}^{-3} - 1) - (r_{ik}^{-3} - 1)(r_{jl}^{-3} - 1) = 0$$

for distinct $i, j, k, l$ (clear denominators to get polynomials; for n = 5 this is 15
equations, 5 independent). [V: HJ11 eq. (5).]

**Cayley-Menger realizability**: for n points to embed in $\mathbb{R}^d$ the
Cayley-Menger matrix conditions apply; for 5 points in $\mathbb{R}^3$ the single equation
is $e_{CM} = \det \begin{pmatrix} 0 & 1 & \cdots \\ 1 & 0 & r_{ij}^2 \\ \vdots & & \end{pmatrix} = 0$
(the 6x6 bordered determinant). For 4 points in the plane the analogous 5x5 bordered
determinant vanishes. [V: HJ11 eq. (6) for the spatial case; the planar 4-body use is
[HM-via-HJ11].]

**Energy-inertia redundancy** (kept for symmetry): $e_{IU} = U - M I = 0$ with
$I = \frac{1}{M}\sum_{i<j} m_i m_j r_{ij}^2$, $M = \sum m_i$, $U = \sum_{i<j} m_i m_j r_{ij}^{-1}$;
a consequence of the AC equations under $\Lambda = -1$. [V: HJ11 eq. (7).]

HJ11's full spatial 5-body ideal: $I_s = \langle \mathcal{F}, \mathcal{G}, \mathcal{H}, e_{CM}, e_{IU} \rangle$,
42 polynomial equations in the 10 variables $r_{ij}$ (plus mass parameters). [V: HJ11
Section 3 end.]

For the PLANAR 4-BODY problem (the HM06 setting): 6 variables $r_{ij}$; the system is
$\mathcal{F}$ (6 symmetric AC equations) together with the planarity Cayley-Menger
$e_{CM}^{(4, planar)} = 0$; the asymmetric set and Dziobek equations are available as
refinements. [HM-via-HJ11; exact equation inventory used by HM06 to be confirmed at
CCB-002.]

## 2. The finiteness logic

1. Normalized CCs avoid collisions and infinity (Shub 1970 compactness), so in the
   distance-variable torus $(\mathbb{C}^*)^{\binom{n}{2}}$ the physically admissible
   solutions sit inside the variety $V(I)$ of the (cleared) system, and an INFINITE
   family of CCs would force a positive-dimensional irreducible component of $V(I)$
   meeting the positive real cone. [V: logic restated in HJ11 Section 2 and Moeckel
   notes; Shub via MZ19 refs.]
2. **HM06 (BKK form)**: if $V(I)$ had a positive-dimensional component in the torus,
   then along it some monomial ordering degenerates: there exists a nonzero weight
   vector $\omega$ (a Puiseux valuation profile) such that the initial system
   $\mathrm{in}_\omega(I)$ has a toric solution. HM06's Proposition 2 characterizes this
   via Puiseux series. The certificate: enumerate all candidate $\omega$ from the Newton
   polytopes (the BKK/polyhedral data), and for each one show by exact computation that
   the initial system has no solution in the torus (the "no solution at infinity in
   direction omega" step). With all directions excluded, the variety is finite in the
   torus, and BKK also yields the upper bound (8472) on the number of isolated
   solutions. Everything runs in exact integer/symbolic arithmetic. [HM-via-HJ11:
   "where they use the theory of Bernstein, Khovanskii, and Kushnirenko we will use the
   language of tropical geometry ... (Hampton and Moeckel, 2006, Proposition 2) falls
   out of the general theory"; bound 8472 via Moeckel notes; the exact enumeration HM06
   used and the derivation of 8472 and 32: read at CCB-002.]
3. **HJ11 (tropical form)**: the modern restatement. The tropical variety
   $T(I) = \{\omega : \mathrm{in}_\omega(I) \text{ contains no monomial}\}$ is, by
   Bieri-Groves, the support of a pure d-dimensional fan where d = dim V(I). To prove
   dim = 0 it suffices to show $T(I) \cap \{\omega \in \mathbb{R}^n : \sum_i \omega_i \ge 0\} = \{0\}$
   (scaling was already fixed by $\Lambda = -1$; the halfspace restriction encodes it;
   the fundamental theorem of tropical geometry / Speyer-Sturmfels connects this to the
   Puiseux statement = HM06 Prop. 2). Pipeline:
   a. Compute the tropical PREVARIETY $\bigcap_i T(\langle f_i \rangle)$ of the
      generating set with Gfan (finite polyhedral computation; overapproximates T(I)).
      HJ11: 576 rays (26 types up to symmetry), f-vector (1, 576, 1620, 1420, 450);
      44 cases survive the halfspace + symmetry reduction.
   b. For each surviving ray/cone, take a relative-interior $\omega$, form the initial
      forms of ALL generators, saturate by $\prod r_{ij} \cdot \prod m_i$, and show by
      exact Groebner computation (Singular/Sage) that the saturated initial ideal is
      $\langle 1 \rangle$, OR that its mass-eliminant forces a sum of masses to vanish
      (impossible for positive masses).
   c. The rays that survive with nonzero mass solutions yield the EXCEPTIONAL mass
      conditions (HJ11 Table 1; two "troublesome rays" 270 and 275 needed bespoke exact
      elimination, including a factorization $Q = (m_1^3 - m_4^3)^2(m_2^3 - m_3^3)^2 \cdot (\ldots)$-type
      identity forcing $m_1 = m_4$, $m_2 = m_3$ on the real positive locus).
   [V: HJ11 Sections 2, 4, 5, PDF read; Table 1 transcribed in part (rays 59, 72, 210,
   270, 275, ... with their exceptional polynomials).]
4. **Where infiniteness would hide**: masses on the exceptional conditions (AK12's
   codim-2 subvariety for planar n = 5; HJ11's Table 1 for spatial; Chang-Chen's 24
   residual diagram cases for planar n = 6). Every modern partial result has this
   "except an explicit subvariety" shape; closing a case means excluding a diagram/ray
   at its exceptional masses (what MZ 2601.01165 did for several 5-body cases).

## 3. Implementation notes for OUR pipeline (exact, Python, repo .venv)

- sympy over QQ suffices for: building $\mathcal{F}, \mathcal{G}, \mathcal{H}, e_{CM}, e_{IU}$
  exactly (cleared denominators); Groebner bases over QQ and QQ(m) for small systems;
  resultants; saturation via added inverse variables ($t \cdot \prod r_{ij} - 1$).
- Newton polytopes: supports are small integer vectors; affine hulls and vertex sets
  computable with Fraction linear algebra; mixed volumes for the BKK rung need a real
  polyhedral instrument (staged; exact; consider the Minkowski-sum lattice-point route
  or a port of the standard mixed-subdivision algorithm; external Gfan as wrapped
  fallback with recorded binaries + hashes).
- The initial-form exclusion step (3b) is pure Groebner over QQ with parameters, exactly
  the machinery the jacobian program exercises daily (including modfrac: rational
  reconstruction of mod-p Groebner runs for speed, then exact re-verification).
- Krawczyk/interval certification (for fixed-mass listings a la MZ19): implement exact
  rational interval arithmetic over sympy Rationals (slow but certificate-grade), or
  mpmath with directed rounding documented; every float exploration is followed by
  exact/certified re-checks on the candidate set (methodology/04).
- Normalization: fix $\Lambda = -1$ (scale); quotient labels by the symmetric group
  action when comparing counts; report the invariant $J = U I^{1/2}/M^{5/2}$ per
  solution for cross-paper matching.

## 4. Calibration targets with known answers (for the opening experiments)

| Target | Known answer | Source |
|---|---|---|
| n = 3 AC system, symbolic masses | equilateral $r_{12} = r_{13} = r_{23} = 1$ (with $\Lambda = -1$); collinear stratum reduces per ordering to Euler's quintic with exactly one positive root per ordering (3 collinear classes); total labeled distance-space count 4 | Euler/Lagrange/Moulton [V: Moeckel notes]; the quintic's exact coefficients are DERIVED by machine, then compared to the literature form at verdict time |
| n = 3 equal masses, classes mod permutation + reflection | 2 | MZ19 appendix [V] |
| n = 4 equal masses, classes mod permutation + reflection | 4 (square; equilateral triangle + center; isosceles/concave family representative; collinear) | MZ19 appendix [V]; shape identification [U] until computed |
| n = 4 equal masses, rotation-only classes | 50 (Simo 1978, numerical) | MZ19 intro [V] |
| n = 4 planar, all positive masses | finite, count in [32, 8472] | HM06 [Vs] |
| n = 5 spatial prevariety | f-vector (1, 576, 1620, 1420, 450), 44 cases, Table 1 exceptional conditions | HJ11 [V] |
| n = 5, 6, 7 planar equal masses | 5, 9, 14 classes | MZ19 [V] |

## 5. Direct-read backlog produced by this dossier

- CCB-002: obtain and read HM06 (Inventiones PDF): exact equation set, Prop. 2 statement,
  the enumeration structure, where 32 and 8472 come from; upgrade every [HM-via-*] tag.
- CCB-003: obtain AK12 PDF (Annals): the zw-diagram machinery (also the basis of
  Chang-Chen), the explicit codim-2 exceptional variety for n = 5.
- CCB-004: Chang-Chen (I) JSC 2024 + (II) SIADS 2025: transcribe the 24 residual
  diagrams and their mass relations exactly.
- CCB-005: HJ11 supplementary Sage worksheet (www.d.umn.edu/~mhampton/FiveBodySpatial.sws):
  fetch, archive, and diff against our reproduction.
- CCB-006: Roberts 1999 PDF: the continuum construction and exact masses.
