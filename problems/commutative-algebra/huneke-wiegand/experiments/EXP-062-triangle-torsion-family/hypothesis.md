# EXP-062: quadratically many independent integral two-torsion classes

Declared 2026-09-05 BEFORE computation, following independent paper review.
Execution gate: EXP-061's complete original-sector audit must pass first.

## Frozen all-parameter candidate

Work in the FULL original integer presentation M_p of EXP-054, p>=8, with
the signed e(r;u,v) and x_uv=e(u+v;u,v) notation of EXP-060. Put n=p-2 and

    T_p = {(i,j,k): 0<=i<j<k, i+j+k=n}.

For T=(i,j,k), choose x_T=x_ij. For distinct u,a,b with a<b and u+a+b=n,
let T_u(a,b) be the potential f_u(r)=1 on [u+a+1,u+b], zero elsewhere.
Use EXP-060's exact signed shifted source operator P, and define

    F_T=T_i(j,k)-T_j(i,k)-T_k(i,j),  W_T=P(F_T).

P1: every source is admissible and the complete INTEGER boundary is
`M W_T=2 x_T` for every p>=8 and T in T_p. This is the signed triangle
identity with arbitrary smallest index, not a new numerical extrapolation.

For each T define z^T_uv=1 exactly when the unordered multiset
{u,v,n-u-v} equals T; zero on invalid indices/diagonals. Define lambda_T
on K rows by EXP-061's reflection construction: e(S;u,v), e(S+1;u,v)
get z^T_uv, and a C0 row with r+s=p+u-1 gets
z^T_u,r-u + z^T_u,r-u-1. All other rows get zero, over F2.
Do NOT assume twelve nonzero rows for every triangle; adjacent endpoints
can cancel. Use the formula, preserve the exact support.

P2: lambda_T kills every original K boundary and every connecting image
of a COMPLETE D cycle. Reuse the proved source classification and complete
potential reconstruction of EXP-061, but verify each step needs only symmetry,
reflection, and pair sums <=p-2, not the special triangle {0,2,p-4}.
The large-high h=10p sector has possible exceptional sums S=1 and S=2;
the A row on {S,S+1}, with offset 2p-S-3>p, kills both. For S>=3 the
A-star makes each relevant coefficient zero. Include h=10p-3 and 10p-2.

P3: lambda_T(x_U)=delta_TU. A pair of indices uniquely completes to a
triangle of sum n, so distinct triangles have disjoint unordered edge sets.
The relative-cokernel argument forces all coefficients of an integral relation
among x_T to be even; P1 realizes every even relation. Hence the map

    (Z/2)^(q(p)) -> coker_Z(M_p),  basis_T -> [x_T]

is injective, where q(p)=|T_p|=floor(((p-2)^2+3)/12).
Prove the count from q(n)-q(n-6)=n-3 and initial counts n=0,...,5,
or by an equally complete elementary argument. Finite agreement with earlier
isolated ranks 3,4,5,7 is motivation, NOT an identification or upper bound.

The tracked eta is integrally congruent to x_02 by EXP-060's exact corrections
and its twice-x_01 source. It is the T={0,2,p-4} member, not an exact equality
of target vectors. This result gives quadratically unbounded two-torsion in
the full explicit presentation. It does not characterize the full cokernel,
its odd torsion/free rank, the isolated subpresentation, the relative completion
quotient, or the lower-strand recurrence. The family-to-presentation premise
is not rederived by this experiment.

## Declared tests, independent audit, and resources

Smoke p=8 first. Producer: all triangles at p=8,...,14; then first, middle
(index floor((q-1)/2)) and last lexicographic triangle at p=16,20,25,32,50,64,100.
Check every full original signed source boundary, the entire functional pairing
matrix for all triangles at p<=14, exact count formula at p=8,...,100, and
the eta quotient-transfer source identity at p=8,...,12. Preserve every
tested full labelled W source and every functional support in deterministic
compressed artifacts if needed. No old HNF source is an input.

Independent auditor: at p=8,...,12, reconstruct ALL triangles and functionals
without producer imports, independently enumerate every incident K source and
every original S source in every reachable high sector, then check each
lambda_T B lies in the full D row span using exact F2 certificates. Reuse
the frozen EXP-061 independent differential/elimination infrastructure only
as explicitly pinned machinery, not its hard-coded twelve-row functional.
Also reconstruct and check every declared producer W source by an independent
signed differential, and the full small-p pairing matrices. Check integer
source coefficient/sign changes, removal of a functional endpoint, and
duplicate/mirrored edge selections that produce a singular pairing matrix.

One CPU producer and one independent CPU auditor, EACH capped at 120 seconds
and 1 GiB private memory, with checks within generation/elimination and
checkpoints after each parameter. Stop on first mismatch or cap. Preserve
partial/failure artifacts; do not silently enlarge the campaign or budget.
Do not assemble a dense global ambient matrix or compute HNF/SNF.
Permanent tests must use temporary outputs. Pin source and hypothesis hashes,
independently review the all-parameter proof, and distinguish this lower-bound
theorem from any complete quotient claim in verdicts and the new manuscript.
