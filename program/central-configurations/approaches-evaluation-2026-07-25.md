# Approaches evaluation and reframings (2026-07-25)

Felipe's request: evaluate the most effective approaches and take other views of the
problem. Part 1 ranks what we have actually run, by measured cost and yield, with
the evidence cited by experiment. Part 2 proposes alternative views, each with its
first executable experiment and its distinct failure profile, so a stall in one lane
never stalls the program. New backlog rows: CCB-033..036.

## Part 1: measured ranking of the approaches we have run

| Approach | Measured cost | Yield | Status |
|---|---|---|---|
| Tropical prevariety + exact comet decision (the Jensen-Leykin route) | 2-6 min per valuation at n = 5; seconds at n = 4; 33 s to decide all comets exactly (EXP-003/004/007) | Full generic-finiteness certificates at n <= 5; two NEW working valuation families; every negative turned into proof | The best cost/yield ratio we have at n <= 5. At n = 6 it is blocked by TOOLING, not budget: gfan 0.7 fails in both arithmetic modes (three abort signatures characterized in EXP-005); gfan 0.8beta cleared the first barrier and is running now |
| msolve censuses at fixed masses | Under 1 s at n = 3 (EXP-006); both n = 4 torus routes exceeded the 1 h cap (EXP-009, route B rerunning) | Ground-truth calibration and cross-engine agreement; not itself a finiteness route | Excellent as the census engine; the n = 4 torus census is at or past its practical limit, which is consistent with Hampton-Moeckel never solving that system either: they BOUNDED it |
| Exact LP pointedness decision | 33 s for 1367 comets (EXP-007) | Converts every screening outcome into a certificate | Pure win; the lane default |
| Equation-variant engineering | Seconds to minutes (EXP-002/004/008) | The enrichment law; symmetric equations proved essential; Dziobek active but not decisive; e_IU inert | Decided; informs every future run (what to include, what to drop) |
| sympy exact stack | Saturates at qdim about 100 with ugly coefficients (measured in EXP-002) | The specification and verification layer; regression anchors | Keep as verifier, never as the engine |

Honest bottom line: at n <= 5 the tropical route dominates everything else we
tried. At n = 6 its bottleneck is one C++ program's internals, which is a fragile
place for a mathematics program to sit. That alone justifies opening a second,
independent route to generic n = 6.

## Part 2: other views of the problem

### V1. The incidence-dimension view (recognition lens; the strongest candidate)

Treat the MASSES AS UNKNOWNS and consider the incidence variety
V = {(m, r) : enriched equations} inside mass-space x torus. Generic finiteness for
a given n IS a dimension statement about V and its projection to mass space; this is
exactly how Moeckel proved generic finiteness for Dziobek configurations
(Trans. AMS 353, 2001) and the frame of his "New equations for central
configurations" (arXiv:1508.06593), and how Dias 2026 gets uniform Dziobek bounds.
Executable form with the engines we already validated: randomized linear-section
dimension probes. Cut V by k random rational hyperplanes and ask msolve for
dimension and points; the largest k leaving points determines dim V, each answer
certified at the specialization, and upper semicontinuity of fiber dimension turns a
certified finite fiber at a verified point into finiteness on a dense open set of
each dominating component. What makes this a genuinely different view: NO valuation
choice at all (the lottery that dominates the tropical route disappears), no
polyhedral combinatorics, and the cost concentrates in one algebraic computation
whose difficulty we can measure at n = 4 and n = 5 against known answers before
spending anything at n = 6. Distinct failure profile: Groebner degeneration instead
of fan explosion. CCB-033.

### V2. The witness-set view (numerical algebraic geometry)

Numerical irreducible decomposition of the n = 6 incidence variety: monodromy plus
trace tests give the dimension AND degree of every irreducible component, with
certification a posteriori (interval Krawczyk or alpha theory) of the witness
points, and our exact layer re-verifying anything verdict-bearing. This is the
modern standard for "what does this variety actually look like", it parallelizes
well on GPU-adjacent hardware, and it would tell us WHERE any positive-dimensional
component lives (which masses, which cluster structure) rather than just whether one
exists. Floats explore, exactness certifies: consistent with methodology/04. Cost:
new tooling (Julia + HomotopyContinuation.jl, both already vetted in our
certification dossier). Calibration first: reproduce the known component structure
at n = 4, 5. CCB-034.

### V3. The degeneracy-exclusion view (invariant lens, now properly gated)

A continuum of central configurations is a positive-dimensional critical set, so
every point on it is a DEGENERATE critical point. Contrapositive, made
computational: at any specific exceptional mass vector (an Albouy-Kaloshin codim-2
point, a Chang-Chen residual mass relation), proving that EVERY central
configuration is nondegenerate excludes a continuum THERE. That attacks the
all-masses question exactly where the generic routes are silent. The Sun-Xie-You
read (context/2026-07-25-degeneracy-dossier.md) supplies the correct full-space
formulation and the warning that reduced-subspace detectors provably miss
degeneracies; Moczurad-Zgliczynski supply the listing technology at fixed masses.
The novel step, unclaimed in the literature we have read: chaining a rigorous
fixed-mass listing with per-solution nondegeneracy certificates into a
continuum-exclusion statement at named exceptional masses. CCB-014 (re-scoped) +
CCB-035.

### V4. The symmetric-strata ladder (a nearer n = 6 frontier)

Generic finiteness is ALREADY published for a class of symmetric planar six-body
configurations (arXiv:1811.08681, which also handles the six-vortex analog). So the
n = 6 frontier is not monolithic: it is stratified by symmetry type, and some
strata are closed while the full space is open. Our machinery is well suited to
extending the closed list: a symmetry stratum has fewer independent variables (the
quotient system is smaller), the tropical computation on the reduced system is
n = 5-scale rather than n = 6-scale, and each newly closed stratum is a publishable
sharpening even while full n = 6 stays open. Requires first reading 1811.08681 to
map which strata are done. CCB-036.

### V5. Already minted, still live

The cluster-recursion reading of failure diagrams (CCB-016, at-infinity lens) and
the vortex/homogeneous-potential transfer (CCB-019) remain on the board; both are
gated on reads (Chang-Chen tables; the vortex finiteness paper) rather than on new
ideas.

## Recommendation (ordered, with the reasoning stated)

1. **Keep the tropical n = 6 attempts running** (they are cheap in attention now:
   detached, checkpointed, on the version that cleared the first barrier).
2. **Open V1 as the second lane to generic n = 6** with a calibration experiment at
   n = 4 and n = 5 against known answers (EXP-010 candidate). It reuses validated
   engines, has no valuation lottery, and its cost is measurable before commitment.
3. **Stage V2** behind a Julia tooling spike; adopt only if V1's engines saturate.
4. **Read-gate V4** (one paper) and then decide whether a symmetric-stratum
   extension is the right first NOVEL claim of the program, since it is the
   smallest closed-form step beyond the published frontier.
5. **Hold V3** until CCB-014's instrument exists; it is the only lane aimed at the
   all-masses question, which makes it strategically valuable but not urgent.

## Infrastructure note that this evaluation forced

Three long computations died because the WSL virtual machine idle-terminates when
the last console detaches. Fixed permanently: `.wslconfig` now sets
`vmIdleTimeout=-1` (plus explicit memory/processor grants), a keepalive process is
planted, and long runs are launched with `setsid` as session leaders. The gfan
0.8beta runner now also checkpoints (`--saveas`), so a future interruption resumes
instead of restarting.
