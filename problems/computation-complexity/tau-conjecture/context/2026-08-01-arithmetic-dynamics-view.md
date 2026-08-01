# The arithmetic-dynamics view (round-5 exploration; view V8)

Dated 2026-08-01. Exploration-cadence deliverable (methodology 11): a new
lens minted from the round-5 sweep, connecting our proved stall theorems to
mainstream arithmetic dynamics. Tags as usual; nothing here is a premise
until the named sources are read in full.

## The observation

Our two stall theorems (Chebyshev tower; monic stall, both [D] proved
2026-08-01) are statements about INTEGER PREPERIODIC-TYPE SETS of a fixed
polynomial map $h$: the escape bound gives a finite ball containing all
integer points with non-escaping forward orbit, and tower root sets are
preimage closures of the fixed/anti-fixed sets, which stabilize. This is
precisely the opening move of arithmetic dynamics (heights, Northcott
finiteness), where far stronger statements are the subject of a mature
research program:

- **Morton-Silverman uniform boundedness conjecture** [MV: multiply
  attested in the round-5 sweep; primary source TO FETCH]: the number of
  $K$-rational preperiodic points of a degree-$d$ morphism is bounded by a
  constant depending only on $d$, $\deg K$ (not on the map).
- **Doyle-Poonen and the dynatomic-curve line** (arXiv:1711.04233) [MV]:
  strong uniform boundedness for $z^d + c$ over function fields; over
  number fields, partial results via gonality of dynatomic curves.

## Why this matters for the tau program

1. Our monic stall theorem bounds each SINGLE map's tower yield by a
   constant $Z(h)$ that depends on $h$ (through the escape radius $R$,
   i.e. the coefficient sizes). The loophole left open (verdict of
   EXP-003, mechanisms wiki) is MULTI-map or parameterized-family towers:
   a putative refuter could vary $h$ with the depth. A Morton-Silverman-
   type UNIFORM bound over a family (e.g. all $x^2 + c$, $|c|$ up to the
   gate budget) would close the loophole for that family up to the cost
   of building $c$: uniform stall constants. This is a precise, checkable
   bridge: OUR question ("root yield per gate of constant-building") is a
   height-counting question in a parameterized dynamical family. [C]
2. The dictionary also runs the other way (already in the literature):
   Cheng 2003 derives torsion bounds on elliptic curves from an
   L-conjecture on SLP lengths, and the round-5 sweep surfaced the
   statement that a NUMBER-FIELD tau analogue implies uniform torsion
   boundedness [MV: to verify in Cheng 2003 when read]. So
   complexity-to-dynamics transfers are established practice; the
   dynamics-to-complexity direction (using height machinery to bound
   root-factory yields) appears underexploited: no hit in the sweep
   applies preperiodic uniform boundedness to tau-conjecture mechanism
   analysis. Candidate niche. [C]
3. **Adelic tau conjecture** (Phillipson-Rojas, arXiv:1011.4128) [V:
   abstract]: a local-field variant with explicit fewnomial-system
   constructions approaching upper bounds via tropical intersections; the
   natural home for our valuation-spectrum instrumentation (RL-2) if we
   extend the census to p-adic root counts. TO FETCH in full.

## Concrete next steps minted (become backlog rows)

- RL-9 (new): the parameterized-tower experiment: for the family
  $h_c = x^2 - c$, measure (exactly, small $c$) the tower yield
  $Z(h_c)$ vs $\tau(c)$: is $\sup_c Z(h_c) / (\text{gates to build } c)$
  bounded? The stall theorem gives $Z(h_c) \le \#[-M_c, M_c]$ with
  $M_c \sim c$: LINEAR in $c$, while $\tau(c) \sim \log c$: so
  parameterized towers COULD in principle beat linear rate if yields
  tracked $M_c$: measuring actual yields (they should be far below
  $M_c$: only perfect-square-related $c$ contribute factors) decides
  whether this loophole is real or empty. This is a decision-bearing,
  cheap, exact experiment: the strongest candidate for the next EXP
  after the depth-7 census.
- Read Doyle-Poonen + Morton-Silverman survey material before any claim
  imports; read Cheng 2003 for the reverse bridge.
