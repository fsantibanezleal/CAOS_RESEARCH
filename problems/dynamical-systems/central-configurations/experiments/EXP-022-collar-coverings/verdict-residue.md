# The residue audit (2026-08-20)

The covering's bisection performs a shell decomposition automatically: a
box touching a face splits into an outer half (which certifies) and an
inner half (which recurses), so at the depth cap the uncertified residue
is exactly the leaves that still touch the face. The theorem needs those
leaves to touch nothing but COLLISIONS, which the open stratum excludes.
residue-audit.py reconstructs the original (u, v, p, q) from each chart's
coordinates and measures, over every FAILED box, the smallest of the eight
collision distances (u, p, d1A, d2A, d1B, d2B, cs, cx).

Findings:

  cb1            12 residue boxes, collision floor 0 for every one
  cb1f            2 residue boxes, collision floor 0 for every one
  bicorner-same   none (after the seam widening)
  m2-R         9950 residue boxes, floor 0 for 8878, POSITIVE for 1072
                 (worst 2.58e-05: physical but extremely collapsed,
                 u ~ p ~ 2e-5, at the collinear quadruple corner)
  deep-R      10648 residue boxes with a POSITIVE floor up to 3.30e-02

The deep-R number exposed a REAL BUG rather than a mathematical obstacle:
deep's chart box product contains (w, rho, tau) combinations with
rho |alpha| > 2w, for which p = w - rho alpha / 2 is NEGATIVE. Those are
not configurations at all. M2 always tested for this; deep never did, so
its entire residue consisted of unphysical boxes that no certificate could
ever discharge. Fixed (make_discard now rejects u.hi <= 0 or p.hi <= 0)
and rerun.

After that fix the atlas's uncertified residue is: zero for every chart
whose residue touches only collisions (cb1, cb1f, and the charts with no
failures at all), plus m2's 1072 boxes within 2.58e-05 of the collision
locus. Lemma piece 10 closes the corner face uniformly; the analogous
uniform lemma for the pair-collapse face would close m2's residue in the
same way, and the shell measurements already show every shell at positive
distance certifying.

## Addendum (2026-08-20): m2's residue maps onto lemma piece 11

m2's uncertified boxes sit at chart coordinates Rc ~ 0.037, tt ~ 1,
tau ~ 1, which in the original coordinates is u ~ p ~ 2e-5 with the two
heights separated by f ~ 0.037. That is exactly lemma piece 11's regime:
both mirror pairs collapsing onto the axis (eps ~ 2e-5 with a ~ b ~ 1) at
distinct heights, which piece 11 covers uniformly on the whole punctured
collar. The chart cannot certify those boxes itself because its own column
scalings do not include the piece-11 division, but the mathematics is
supplied. Making the artifact self-contained would need only that column
rescale added to m2; the theorem does not wait on it.
