# 01 - Statement and history

## The objects

A **central configuration (CC)** for masses $m_1, \dots, m_n > 0$ is an arrangement
$x = (x_1, \dots, x_n)$, $x_i \in \mathbb{R}^d$, of the Newtonian $n$-body problem whose
gravitational accelerations all point at the center of mass $c$ with a common factor:

$$\lambda\,(x_i - c) = \sum_{j \ne i} \frac{m_j (x_j - x_i)}{r_{ij}^3}, \qquad i = 1, \dots, n,$$

$r_{ij} = |x_i - x_j|$. Equivalently $\nabla U(x) + \lambda M (x - c) = 0$ with
$U = \sum_{i<j} m_i m_j/r_{ij}$; contracting with $x - c$ gives $\lambda = U(x)/I(x) > 0$,
$I$ the moment of inertia about $c$ (with $\sum m_i x_i = 0$ and $\sum m_i = m$:
$I = \frac{1}{m}\sum_{i<j} m_i m_j r_{ij}^2$). Sources: Moeckel, Lectures on Central
Configurations (Def. 1, eqs. 8-10); Moczurad-Zgliczynski, CMDA 2019, eq. (2). Both PDFs
read 2026-07-23; transcription in `../context/2026-07-23-deep-research-dossier.md`.

Dynamical meaning (same sources): released from rest, a CC collapses homothetically
keeping its shape; in the plane, each CC rotated at angular velocity
$\omega = \sqrt{\lambda}$ is a **relative equilibrium** (a rigidly rotating periodic
solution), and each CC generates a family of homographic (elliptic) solutions. CCs also
organize the topology of the integral manifolds of the $n$-body problem.

## The problem

**Smale's 6th problem (1998).** For every $n$ and every choice of positive masses, is
the number of planar central configurations (equivalently relative equilibria), modulo
rotation, translation, scaling (and optionally reflection and relabeling), FINITE?
Listed as problem 6 of Smale's eighteen problems for the 21st century (S. Smale,
Mathematical problems for the next century, Math. Intelligencer 20 (1998) 7-15). The
question goes back to Chazy (1918) and Wintner (1941). [Citation chain verified via two
independent papers; the verbatim Intelligencer text is still flagged UNVERIFIED in
`../context/references.md` (backlog CCB-011).]

Why finiteness: the CC equations are algebraic, so infinitely many solutions would mean
a positive-dimensional continuum of steady shapes; Morse/topological counting programs
(Smale, Palmore, Pacella) presuppose isolated (or at least finitely many) critical
points; and bifurcation analysis of the counts as masses vary (Palmore's degeneracies,
Simo's numerics) needs the finite regime.

## The classical arc

- **Euler 1767**: the three collinear 3-body CCs (one per ordering).
- **Lagrange 1772**: the equilateral triangle is a CC for ALL masses; with orientation,
  2 classes; total 5 planar CCs for $n = 3$, every mass vector.
- **Moulton 1910**: for any $n$ and positive masses, exactly one normalized collinear CC
  per ordering: $n!/2$ collinear classes (proof in Moeckel's notes, Prop. 18).
- **Dziobek 1900**: the determinantal structure of configurations of dimension $n - 2$
  (planar noncollinear 4-body, spatial nonplanar 5-body), the wedge every modern
  finiteness proof uses.
- **Chazy 1918, Wintner 1941**: the finiteness question posed.
- **Smale 1998**: problem 6.

The modern results (2001-2026) are the ladder in [02-known-results-ladder.md](02-known-results-ladder.md).
