# EXP-028 - Verdict: CONFIRMED (2026-07-21). The strategy shift holds: polygons explain the machine

Artifacts: `artifacts/output-{ABD,C}-2026-07-21.txt`.

## Established results

1. **The lattice sieve is exact [MV].** Mechanical enumeration (n <= 60): for P = x + a h^2
   the Abhyankar similarity condition admits partner degrees ONLY at multiples of
   m = deg P (18: {18, 36, 54}; 24: {24, 48}). Pure arithmetic, machine-checked.
2. **The decisive window is empty [MV].** (18, <= 36) CONTAINS the first admissible rung
   n = 36, and it is empty at every numeric sample: the divisible rungs die too (the edge
   calculus + descent intuition: a P^2-proportional top can always be subtracted, landing in
   the previously emptied window).
3. **THE CERTIFICATE [MV]: at (18, <= 36), NO Keller partner exists for ANY a != 0**
   (1156 equations, 700 unknowns, 457 left-null vectors, ONE pairing, gcd -576 a^3; 182 s).
4. **Obstruction anatomy [MV, recorded].** The certificate vector's support lies EXACTLY on
   the ray parallel to P's Newton-edge direction: for P = x + a (xy)^2 (edge direction
   (1,2)), the supported equation rows are x^k y^{2k}, k = 1..4, with weights
   (4a, -3) at window 6 and (64a^3, -48a^2, 40a, -35) at window 10. The single pairing IS a
   weighted edge residue; a closed-form functional is conjectured [C], not claimed.
5. **Sources verified (JCB-031 advanced).** Abhyankar's similarity theorem (early 1970s;
   Newton polygons of Jacobian pairs, J. Pure Appl. Algebra, 1991 line): for a Jacobian pair
   with both degrees > 1, the Newton polygons are similar TRIANGLES with ratio
   deg f : deg g centered at the origin. Moh 1983: JC(2) verified to degree 100 (via a
   computer search leaving six candidate shapes, all eliminated); a 2022 preprint raises the
   minimal-possible-counterexample degree from 100 to 108 (arXiv:2204.14178). So the
   verified floor is currently ~108, and "beyond-current-knowledge" starts above it.

## The derived all-degree statement [D, conditional]

Assembling 1-3 with Abhyankar similarity (primary-cited) and the descent mechanics
(EXP-022): **P = x + a h^2 (h = x^p y^q, p != q, a != 0) is NEVER a Keller component, at ANY
partner degree**: similarity forces m | n; at n = km the leading edge is P^k-proportional and
one subtraction lands in a smaller admissible window; induction bottoms out below m where no
admissible degree exists. Status [D]: the similarity theorem is cited (full-text hypotheses
pass queued), the edge-proportionality step is the remaining formalization gap, and the
machine has verified the shadow directly through degree 36.

## The strategy evaluation (what Felipe asked for)

- The window program's ceiling is real, and the polygon calculus is the successor: the
  obstruction anatomy (support on ONE edge ray) says each certificate is an edge residue.
  The next instrument (JCB-032) is that functional in CLOSED FORM: it would evaluate rungs
  beyond the ~108 floor (e.g. gcd 45 at bidegrees (90, 135)) at negligible cost, where a
  certified exclusion would be a statement nobody has verified in any form.

## How could this be wrong?

- The all-degree statement is conditional [D]: the exact hypotheses of the similarity
  theorem (behavior when a component is a coordinate; the N^0 convention including the
  origin) must be read from the primary text before [D] hardens; the windows themselves are
  unconditional [MV].
- The anatomy is two data points; the closed form is a conjecture until derived and proved.

## Consequences

- Wiki 04 gains the polygon-strategy section; JCB-030 pivots to the edge-residue functional
  (JCB-032); JCB-031 keeps the full-text pass (similarity hypotheses + Moh + the 108 paper).
