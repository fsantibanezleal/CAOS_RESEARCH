# EXP-035 - Verdict: CONFIRMED (2026-07-22). The corner is diagonal; the core is the staircase

Artifact: `artifacts/output-2026-07-22.txt`.

## Established results

1. **The corner operator is DIAGONAL [MV].** For B = x^i y^j (i, j >= 1) and any monomial:
   J(B^p, x^a y^b) = p (i b - j a) x^{ip+a-1} y^{jp+b-1}, exactly, on the grid
   i, j <= 3, p <= 3, a, b <= 4. One monomial in, one monomial out; the eigenvalue is the
   determinant (ib - ja) of the exponent pair against the corner direction.
2. **Its kernel is exactly the powers of B [MV].** J(B^p, G) = 0 iff (a, b) is parallel to
   (i, j): the classical functional-dependence statement, now as a diagonal spectrum.
3. **A pure corner cannot produce the constant [MV].** No monomial G makes J(B^p, G) carry
   a constant term (output exponents ip + a - 1, jp + b - 1 never both vanish for
   i, j >= 1). The Keller constant must therefore be manufactured along the STAIRCASE of
   Newton vertices running from the swallowed linear vertex (1, 0) up to the top corner.
4. **The staircase is where the coupling lives [MV data].** Certificates for swallowed
   samples are multi-row bands whose lattice extent tracks the staircase geometry (recorded
   per sample with the Newton points and the staircase vertices), not a single ray.
5. **Territory widened [MV].** Thirty monomial-corner samples (B in {xy, x^2y, xy^2,
   x^2y^2, x^3y}, p <= 2, three filler patterns): every completion window EMPTY.

## The reframe (why this matters)

The mixed corner was the suspected hard object; it is not. It is diagonal, with a clean
spectrum and an explicit kernel. What resists is the STAIRCASE: the chain of Newton vertices
that must carry the constant from the linear vertex to the corner. This converts the open
core from "understand mixed corners" into a concrete combinatorial transport problem on the
lower-left Newton boundary (the classical Moh staircase), which is the right object to build
the next calculus on (JCB-038).

## How could this be wrong?

- The diagonal formula is exact and general (proved by the displayed computation, verified
  on a grid); the staircase claim is a structural reading of certificate data, labeled as
  such, not a theorem.
- The scans remain bounded windows; they map, they do not prove.
