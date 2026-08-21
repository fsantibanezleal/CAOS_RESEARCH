# EXP-023: the (k=0, p=3) stratum, three mirror pairs

Declared 2026-08-20, before the covering runs.

## The object

Six bodies, reflection-symmetric, NOTHING on the axis:
pair A = (+-u1, v1) mass mA, pair B = (+-u2, v2) mass mB,
pair C = (+-u3, v3) mass mC. Shape space dimension 4 after translation
and scale, the same as the (2,2) stratum; mass vector has 3 entries.

## Derived and verified before any run (derive.py)

1. Under the mirror, distances are invariant and every triangle area
   flips sign, so L_{sigma i, sigma j} = -L_ij. Hence L12 = L34 = L56 = 0
   IDENTICALLY (each is its own mirror image), and the remaining fifteen
   equations collapse to SIX independent ones,
   {L13, L14, L15, L16, L35, L36}, over three masses: a 6 x 3 matrix.
   Verified exactly at three random shapes (all the claimed vanishings
   and anti-equalities are 0.0 to 40 digits).

2. GENERIC RANK IS 3 (20 of 20 random shapes). For a 6 x 3 matrix that is
   FULL rank, so the kernel is trivial and there are NO admissible masses
   at a generic shape. Central configurations of this stratum therefore
   live only on the rank <= 2 locus R_2: they are confined to a
   codimension-2 subvariety of the shape space. This is a sharper
   structure than the (2,2) stratum, where generic shapes do admit masses.

3. Instrument validation on a KNOWN central configuration: the regular
   hexagon (all six bodies on a circle) has rank exactly 2, and its
   one-dimensional kernel is the equal-mass ray (1, 1, 1), reproducing
   the classical regular-hexagon central configuration. The matrix
   construction is therefore correct on an independently known member.

## The count for this stratum

    r = 3 : kernel trivial, contributes NOTHING
    r = 2 : dim <= dim R_2 + 1 <= 2 + 1 = 3   needs dim R_2 <= 2
    r = 1 : dim <= dim R_1 + 2                needs dim R_1 <= 1
    r = 0 : dim <= dim R_0 + 3                needs R_0 empty

and the mass space has dimension 3, so dim I <= 3 gives generic finiteness
exactly as before. Three requirements, the same shape as the (2,2) chain,
and one fewer than that chain needed.

## Plan

Gauge v1 = 0 and u1 = 1, using the S3 symmetry that permutes the three
pairs (a genuine symmetry: it permutes rows and columns of the matrix) to
assume u1 is the largest, so u2, u3 in (0, 1]. Free parameters
(u2, u3, v2, v3), a 4-dimensional box. Certificates as before: rank 3
(here FULL rank, so no central configurations at all in that box) and, on
the rest, the trap certificate bounding dim R_2 <= 2. The singular faces
are pair collapses (u_i -> 0) and pair-pair merges, which are precisely
the two face types lemma pieces 11 and 12 already closed.

## Success criteria (declared)

Certify the bounded region with zero residual failures, or with residues
touching only collisions; then the outer region by inverted charts. Budget
12 h per covering, resumable, failures recorded. This experiment does NOT
claim the (2,2) theorem's statement and does not gate it.
