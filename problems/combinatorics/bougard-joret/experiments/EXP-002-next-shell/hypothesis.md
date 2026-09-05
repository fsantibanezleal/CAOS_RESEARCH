# EXP-002: the full first interior shell

Date: 2026-09-05. Status: PREFLIGHT, before computation. Owner: Bougard-Joret lane.

## Claim and scope [C before validation]

For every integer k >= 3 and 2 <= a <= k+1, with n = a+k+1,

    f(n,a,k) = ceil(n*k/2).

These are all admissible parameters on this shell under n >= 2a. The shell satisfies n <= ka. This is a restricted infinite family, not a solution of the full revised first regime or second regime. Known numerical overlaps: a=k+1 in Bougard-Joret; (n,a,k)=(6,2,3) on n=ka; a=k-1 in EXP-001 / preprint v0.01. Novelty is bounded by the primary-source review, not guaranteed priority.

## Frozen construction and proof obligations

- a=2: complement of the n-cycle. Proposed equality classification: complements of disjoint cycles of lengths at least five.
- a=k+1: K_(a,a) minus a perfect matching.
- a=k: residual matching of ceil(k/2) edges on k+1 vertices. Add independent S of size k; each vertex misses a different matching endpoint and meets every other residual vertex.
- a=k-1: use the nonstar path construction from EXP-001.
- Remaining a>=3 and d=k-a>=2: m=k+1, epsilon=n*k modulo 2. Start with the classical d-connected Harary graph on m vertices. If d is even, it is C_m^(d/2). If d is odd and m even, add an antipodal perfect matching to C_m^((d-1)/2). If d,m are odd, m=2q+1, add edges {i,i+q}, 0<=i<=q, to that cycle power; q is the unique vertex of degree d+1. Add a deterministic greedy complement matching until exactly a+epsilon distinct vertices have degree d+1, avoiding q in the last case. Minimum-degree matching bounds justify enough edges. Choose a of these higher-degree vertices; each is missed by a different member of independent S, and add all other cross edges.

Prove degree sum with parity, exact independence, connectivity after every cut of size <k, the matching bound, and Harary connectivity using two deleted cyclic gaps. Handle the two-surviving-residual-vertices case separately. For a=2, equality makes the complement 2-regular: triangles violate independence; 4-cycles violate connectivity; all cycles of length >=5 suffice.

## Exact finite validation [MV, never a universal proof]

CPU only; standard-library integer graph representations. Smoke grid k=3..6, full grid k=3..12, every a=2..k+1. Verify all degrees, edge count, independence by include/exclude recursion and connectivity by vertex-split max flow. For n<=16 also compare independent direct subset and exhaustive vertex-cut checks. Audit residual d-connectivity independently for the Harary cases. Store full edge lists and deterministic source hashes.

Adversarial controls: remove one edge incident to a degree-k vertex and require rejection; verify odd n*k gives exactly one degree-(k+1) vertex; test complements with a triangle or 4-cycle as rejected alpha=2 candidates. Compare alpha=2 equality characterization to complete order-six census already certified in EXP-001. An independent reviewer must audit the all-parameter proof separately from the finite checker.

Each computational stage has a five-minute budget with deterministic per-case checkpoints. Reaching the cap yields partial evidence, never PASS. PASS requires every declared case and control plus a complete written proof; FAIL/REVISE records the counterexample or gap append-only. No existing experiment verdict is rewritten.

## Sources and decision

Primary comparison: Bougard-Joret, Section 6, https://gjoret.be/papers/turan.pdf; Das-Gupta, Sections 3-4, https://arxiv.org/html/2608.18828v1. Classical construction credit: Harary (1962), https://doi.org/10.1073/pnas.48.7.1142; full text inaccessible during this refresh, so prove every required property here. The dated portfolio refresh records all 13 unstarted and seven active rows. The full shell ranks first for source completeness, symbolic feasibility, exact auditability and extension beyond the previous diagonal.
