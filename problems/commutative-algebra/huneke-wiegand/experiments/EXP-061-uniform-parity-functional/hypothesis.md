# EXP-061: a twelve-row relative parity functional

Declared 2026-09-05 BEFORE computation. Exact arithmetic over F2; p>=8.

## Frozen functional

Use the full original S/K -> D/K presentation of EXP-054, the four-row eta
of EXP-057, and the normalized e(r;u,v) notation of EXP-060. Put k=p-4.
For distinct second indices u,v define z_uv=1 exactly when the unordered
multiset {u,v,p-2-u-v} equals {0,2,k}; set invalid indices and diagonals to zero.
This is symmetric and obeys z_uv=z_u,p-2-u-v.

The F2 functional lambda_K is zero on every row except the following twelve
K rows, all with exterior high set {6p}, where its value is one:

- Six C2 rows: e(S;u,v) and e(S+1;u,v), S=u+v, for
  (u,v)=(0,2),(0,k),(2,k). Their offsets are 11p-2 and 11p-3.
- Six C0 rows, with offset 8p-1 and omitted lows {p-r,p-s,3p+u}:
  (r,s;u)=(2,p-3;0),(3,p-4;0),(2,p-1;2),(3,p-2;2),
  (p-4,p-1;k),(p-3,p-2;k).

Equivalently the C0 value when r+s=p+u-1 is
d_u(r)=z_u,r-u+z_u,r-u-1. Reflection makes this symmetric in r,s;
at a reflected fixed point d_u(r)=0. The twelve rows must be distinct and valid
for every p>=8. Signs are immaterial only in this F2 experiment.

## Predictions and full proof obligations

P1: lambda_K(eta)=1 and lambda_K annihilates every original K-source boundary.
Prove exhaustiveness by number of high exterior variables and the missing-low
types AA, AB, BB. It is not enough to check a truncated local matrix.

P2: lambda_K annihilates the K boundary of EVERY S source chain whose full
D boundary vanishes. The D differential preserves the exterior-high set.
The ONLY potentially visible sectors have high set {6p,h}, with
h in [7p-1,8p-2] union {10p-3,10p-2,10p}. Prove this reachability list.
The h=10p-3 sector was caught during paper-only independent preflight and
is explicitly included; no computational result preceded this declaration.

For h=8p-d, 2<=d<=p+1, reconstruct the COMPLETE D kernel by potentials:

    alpha(r,s;u)=f_u(r)+f_u(s)
    u+d-2 <= r+s <= p+u+d-3, r<s,
    f_u(r)=0 for r<u+d-2; f_u(0)=0.

For u<v, S=u+v, F=f_u+f_v, the beta range is
max(0,S+d-p)<=r<=min(p-1,S+d-2), and

    beta(r;u,v)=F(r)+F(S+d-1) if S<=p-d, else F(r).

Out-of-range potential values are zero. At d=2, f_u(u) is FREE for u>=1:
do not confuse this complete kernel with EXP-060's restricted construction.
Prove completeness by the A-vertex-zero and B-star equations, with all
endpoints treated. Both C0 and C2 pairings equal
sum_{u<v} z_uv (F(S)+F(S+1)), hence cancel. Treat d=2, 3<=d<=p,
and d=p+1 separately, including the fixed reflected point.

For h=10p-3 or 10p-2, the first-low ABB sources have r>=S+1 or r>=S,
respectively; alpha_0 is absent and the A-star equations force all relevant
coefficients to zero. At h=10p the same star argument works for S>=3;
the remaining visible S=2 case is killed by the A row on endpoints {2,3}.
All other source families have zero relevant A contribution. Prove these
claims from the original differential, not by extrapolated rank tables.

P3: if eta=M(s,t) over F2, its zero D boundary forces s into the full D
kernel, so P1/P2 contradict lambda_K(eta)=1. Thus eta is nonzero in the
full mod-two cokernel. Combined with the independently proved EXP-060
identity M V=2eta, its integral class has EXACT order two for every p>=8.
EXP-057 transfers this conclusion to the class of b_A+b_B (up to sign).
This does not prove a second independent class, the full quotient, or its
recurrence, and does not resolve the original Huneke-Wiegand conjecture anew.

## Declared finite audits, resources, and rejection controls

First p=8, then 9,10,11,12. For these five parameters independently enumerate
every original source incident to the twelve functional rows (inverse incidence
is exhaustive), all S sources in EACH reachable high sector, and their full D
rows. Verify lambda_K K=0 and lambda_K B restricted to ker(D)=0 by exact F2
elimination, using NO producer potential formula for this audit. Preserve
sector dimensions/ranks and exact dual or kernel certificates and incidence
hashes; no non-incident source needs enumeration because its pairing is zero.

Separately check the complete potential parametrization against exact D kernels
at p=8,9, and the declared unit-potential boundary identities at p=8,...,16,
25,32,50,64,100 (all basis elements for p<=12, frozen valid endpoint/midpoint
samples for larger p). Pin all formulas and sampling in source BEFORE execution.
No old p=11 HNF-source labels are an input; this is not an untouched holdout.

One CPU producer and one independently encoded CPU auditor, EACH capped at
120 seconds and 1 GiB private memory; check budget inside enumeration/elimination
and checkpoint after each parameter. Stop on first mismatch or resource cap;
preserve a partial result without silently increasing the budget. If necessary,
reduce only a separately declared follow-up campaign, never rewrite this one.
No dense global ambient matrix or integer HNF/SNF computation.

Include removal of the odd eta-pairing row, a support-index mutation, an omitted
reachable high-sector diagnostic, and a candidate functional that passes a
proper local subset but fails an added original source. Keep failures explicit.
Independent proof review plus original-differential audits, not finite agreement,
are the grounds for a uniform verdict and any unpublished manuscript upgrade.
