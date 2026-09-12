# Independent audit of AxiomMath/ZetaZerosV2

Audit date: 2026-09-12. Scope: current public source, theorem statements, assumption boundary, proof architecture, numerical certificate, CI coverage, reproduction cost, and related multiplicity refinements. No local Lean build or comparator run was performed during this audit.

## Preserved artifacts and exact revision

- Public source: https://github.com/AxiomMath/ZetaZerosV2
- Sole commit: `4c73b317232173a5e6d4253702c9870ee66c2c7b`, authored 2026-09-08 16:04:09 +01:00, subject `Publication of Files`.
- Git archive: `source-snapshots/axiom-zeta-zeros-v2-4c73b3172321.zip`.
- Portable archive size: 140,709 bytes. SHA-256: `2746d137514e4435c9af154d05137384993e998805facbfe6f8e71be09f16e09`. The final git-archive packaging differs from the initial acquisition ZIP; the pinned source commit is identical.
- License: Apache-2.0, retained verbatim inside the archive. Individual Lean files credit Kenny Lau or Axiom Math. Preserve these notices when reusing code.
- 44 Lean source files, 9,293 lines, 451,010 bytes (including Challenge and Solution). The clone also contains one GitHub Actions workflow; normal `rg --files` hides `.github`, so `git ls-files` is the authoritative inventory.
- Toolchain `leanprover/lean4:v4.34.0-rc2`; Mathlib `v4.34.0-rc2`, pinned to `85e3a25e006c35636f0e53b0e9296caca2685bc0` in `lake-manifest.json`. The manifest pins all eight transitive packages as well.

## What its headline statements actually prove

Let theta=1/sqrt(2) and A=1/2+theta*cot(theta)=1.3274992963... . Then C0=2-A=0.6725007037..., C1=(3-A)/2=0.8362503518..., and C2=(5+2sqrt(2)-2A)/(3+2sqrt(2))=0.8876200082... .

`ZetaZeros/Main.lean:69`, `:108`, `:148`, `:242` give asymptotic lower bounds C0, C1, C1, C2 respectively for:

1. simple zeros on the critical line;
2. distinct zeros;
3. the average of the proportion of simple zeros and of on-line zeros;
4. zeros that are simple or on the critical line (inclusive or).

Every one of those zeta statements takes two arguments: `(hRvM : RiemannVonMangoldt) (hPC : PairCorrelation)`. This is explicitly stated in the README and source, not a hidden assumption. The formalization establishes the implication from two classical analytic theorems to the four bounds. In ordinary mathematics these analytic inputs are unconditional theorems; within this Lean development they are assumptions, not proved facts. Calling this repository an end-to-end assumption-free Lean proof would be inaccurate.

The exact assumptions are `ZetaZeros/Defs.lean:206-220`:

- Riemann--von Mangoldt is N(T)/[(T/(2pi))*log(T)] tending to 1, in epsilon form.
- PairCorrelation is the complex-valued weighted sum for all admissible even integrable test functions supported in [-1,1], normalized by the same scale, differing from f(0)+2 integral_0^1 alpha f(alpha) d alpha by at most C/sqrt(log T), eventually.
- `IsPairTestFunction`, at `Defs.lean:200-202`, asks for a global Lipschitz-at-zero bound |f(x)-f(0)| <= C|x|. It is stronger than the cited local condition, hence makes the universally quantified analytic assumption weaker. The concrete smooth kernels satisfy it.
- `pairWeight(z)=4/(4-z^2)` and `rescaledDiff=i(rho-rho')log T/(2pi)` at `Defs.lean:162-179`. Complex differences are intentional and crucial for an unconditional statement; replacing them with only ordinate differences is not an innocuous simplification.

Counting conventions matter (`Defs.lean:35-85`). N(T), onLineCount and simpleOrOnLineCount count with multiplicity; simpleOnLineCount, simpleZeroCount and distinctZeroCount count distinct points. All sets use positive ordinates 0<Im(rho)<=T and the open critical strip 0<Re(rho)<1. Multiplicity is Mathlib's analytic order, not an abstract auxiliary number.

Theorems are eventual/asymptotic. No explicit height T0 is given and no computation of low-lying zeros is a premise. The project does not prove RH or establish a 67.25% fraction separately in every finite height window.

## Trust boundary and comparator

`Comparator/comparator.json` names exactly 12 statements: four finite-set Hilbert propositions, four exact asymptotic statements, and four numerical corollaries. Permitted axioms are only `propext`, `Quot.sound`, `Classical.choice`; `enable_nanoda` is true.

Source search found no project `axiom` declaration, `admit`, `unsafe`, or `native_decide`; the 12 executable `sorry` occurrences are all in `Challenge/Basic.lean`, as intended. Challenge is a Mathlib-only trusted statement file and is deliberately absent from default build targets (`lakefile.toml:20-30`). `Solution/Basic.lean` delegates to the proved library statements. The comparator must verify the same elaborated statement definitions and allowed proof dependencies, rather than merely accept a file sharing a theorem name.

The only custom metaprogramming is the `zz_tag` string attribute in `ZetaZeros/Meta/Attr.lean`; it records correspondences to source-paper tags. It does not replace proof checking. `Defs.lean:17-27` explains why definitions are kept identical to Challenge, including auxiliary elaborated proof naming. `ZetaZeros/Hilbert/AlphaExpansion.lean:903-906` documents avoiding a private mangled name for a proof-audit helper. These are signs of attention to statement fidelity, but the local source scan is not a substitute for comparator execution.

The author reports local comparator verification in README. The official comparator currently needs Linux Landrun, a Lean-version-matched lean4export, and (for this configuration) NanoDa. Its documented trust assumptions include a trusted Challenge/dependency/config surface and a correctly functioning sandbox. See https://github.com/leanprover/comparator . A fresh isolated verification workspace is appropriate; do not silently replace the real sandbox by its testing shim and call that the same certificate.

## CI evidence and reproduction cost

Current-head run https://github.com/AxiomMath/ZetaZerosV2/actions/runs/34242947077 is successful, head `4c73b317...`, created 2026-09-08 15:09:36Z and updated 15:16:28Z. The checked-in `.github/workflows/lean.yml` performs checkout@v4 and lean-action@v1. The retrieved log shows:

- Default `lake build` succeeds, 3,641 jobs including Mathlib closure.
- Build starts 15:13:14Z and completes 15:15:30Z (about 136 seconds).
- `Hilbert.AlphaExpansion` takes 26 seconds; `Zeta.Kernel` and `Hilbert.Propositions` about 13 seconds each.
- There is no comparator command or Challenge/Solution build in that run. Therefore current-head CI supports compilation of the default mathematical library, not an independently replayed comparator certificate.
- Cache-save tar fails with a disk-write warning after build success. This does not invalidate the completed build, but success should not be represented as a clean cache-upload receipt.

Local environment inspection: Windows PATH has no lean/lake. WSL Ubuntu-24.04 has no lean, lake or elan on PATH and no ~/.elan/toolchains directory. WSL reports 25 GiB memory, around 24 GiB available, 7 GiB swap and 924 GiB free filesystem capacity. No installation or large build has been started. A planning allowance of 10-20 minutes for toolchain install, dependency/cache transfer and one library/Solution build is reasonable but unmeasured; the measured upstream project build itself was 2m16 after dependencies. Full comparator setup adds matched exporter, sandbox and NanoDa builds. GPU offers no advantage for this kernel verification workload.

## Proof map and what was really simplified

The repository follows Lamzouri's September 8 v2 argument, including its two additional conclusions. The generic finite proposition concerns any finite conjugation-invariant multiset, an even normalized real test function eta, and K=Fourier(eta^2). It proves positivity and bounds for the real part of sum m(z)m(s)K(z-s)^2; this is a square, not an absolute square taken term by term.

1. `Hilbert/Defs.lean`, `FIdentity.lean`, `Subspaces.lean`, `Basis.lean`, `AlphaExpansion.lean`: form even/odd combinations of exponentials in L2, use a conjugation-symmetric adapted orthonormal basis and separate three ranges U, V/U and W/V.
2. `AlphaExpansion.lean:918` proves total coefficient sum is total mass; `:2425` proves Bessel control of squared coefficients; `:2477-2545` identifies the nonnegative double integral with the complex pair sum; `:2583` establishes the original first-range lower bound; `:2668`, `:2790` perform the elementary scalar inequalities for simple-real and distinct counts.
3. `Hilbert/RefinedRange.lean:27-135` preserves simple/multiple nonreal categories, improving the U-range mass lower bound. Its intermediate proof actually establishes the full multiplicity masses before replacing them by m>=1 or m>=2.
4. `Hilbert/Propositions.lean:32` and `:134` prove the two further scalar estimates; `:267` and `:307` assemble them. The union proof fixes t=2+sqrt(2), whose quadratic identity cancels the multiple-nonreal contribution.
5. `Zeta/Finite.lean:38` proves finiteness of zero sets using Mathlib. `Zeta/OrderConj.lean` proves preservation of analytic multiplicity under conjugation and the functional-equation reflection; it credits adapted helper lemmas from AxiomMath/PrimeNumberTheoremAnd. Transfer files connect the actual zeta counts to the abstract finite support.
6. `MontgomeryTaylor/` evaluates the explicit cosine extremizer and its self-convolution. `Basic.lean:32` proves the functional equals A, rather than assuming that numerical integral.
7. `Zeta/Kernel.lean:354-437` proves the exact second-derivative correction removing pairWeight; `:489` transfers the unweighted sum to two weighted pair sums; `:574` makes the correction vanish asymptotically; `:950-994` uses smooth cutoff convergence to approach A.

This is a genuine replacement of the finite Weil-matrix route with an L2/Bessel argument, not a new numerical choice of the extremal test function. Pair-correlation and Montgomery--Taylor inputs remain the limiting analytic information.

## Exact numerical certificate and the precision opportunity

`Numeric/MontgomeryTaylor.lean:65-148` observes theta^2=1/2, so cos(theta) and sqrt(2)sin(theta) have rational alternating series. Five terms provide a cosine upper bound 0.7602447 and four terms a denominator lower bound 0.9187251. Rational arithmetic proves theta*cot(theta)<0.8275 and therefore A<1.3275. This gives strict eventual proportions above 0.6725 and 0.83625.

`Numeric/SimpleOrOnLine.lean:91-103` explicitly records why the coarse A estimate only yields C2>0.887619766..., sufficient for 0.8876 but not for 0.88762. The exact formula C2=0.8876200082... does exceed 0.88762. More Taylor terms and a sharper rational enclosure of sqrt(2) can certify the latter decimal. This is a useful formal-certification improvement; it is not a new analytic constant and must not be advertised as a new discovery about zeta zeros.

## Comparison with the current Anthropic formalization

The link on the Anthropic article formerly named `anthropics/zeta-23-lean` redirects to https://github.com/anthropics/formal-math . The zeta23 source is preserved in `source-snapshots/anthropic-zeta23-fbdc36bbf17d.zip`; current head is `fbdc36bbf17d20af3fd0447c6d1a8a02773c9844`, dated September 5, 2026. The zeta23 subproject has 326 Lean files and 5,483,343 bytes. Its toolchain is v4.33.0-rc2, not Axiom's v4.34.0-rc2.

Its current `zeta23/Challenge.lean:131-229` and `Solution.lean:52-140` have no external analytic hypotheses in the 17 headline statements. README claims, and the actual statement signatures support, an end-to-end proof including analytic inputs. It also treats primitive Dirichlet L-functions and has a separate XiPrime topic. This audit did not independently build that development.

Do not overread a green current-head badge: at HEAD the two September 5 Actions runs succeeded only in metadata/wrapper/readme jobs; `verify` and doc-build jobs were skipped because the commit only changed action configuration. `zeta23/AUDIT.md` contains historical successful kernel/comparator receipts but begins with earlier 27-statement counts while current README says 17 main plus 6 XiPrime statements. That is recorded historical evidence, not a fresh local run or an automatically current receipt.

Most relevant prior art for a multiplicity follow-up is already in the original source:

- `zeta23/Zeta23/ZeroSide/RankTraceMult.lean:351-386` defines k_c(m)=c^2-max(c-m,0)^2 and proves, for arbitrary c>0, a multiplicity-aware rank-trace inequality with one c^2 contribution per positive pair block.
- `ZeroSide/TightMult.lean:91-107` proves abstract equality for every c on orthogonal integer atoms of multiplicity <=c together with positive pair blocks. It warns that the c=2 certificate cannot distinguish double real points from shallow conjugate pairs using only those quantities.
- `PairCeiling/` contains a stronger method ceiling discussion, with an explicit `EnclOK` hypothesis for external integer enclosures. It is a conditional certificate for that method, not a proof that every possible approach is bounded by 68.18%.

## Independently checked multiplicity-defect envelope

The following agrees with a separate derivation by the Lamzouri-analysis agent, but is an elementary corollary of existing machinery, so novelty is not established.

Let N be total mass, n the number of simple real support points, r the number of multiple real support points, and b the number of nonreal conjugate pairs. Set d=r+b. Let Q be the real part of the squared-kernel pair sum. The intermediate first-range estimate in `Hilbert/RefinedRange.lean` gives S_U>=N-n; the middle trace is <=n, the last coefficients are <=0, and dim U<=d. Moreover N-n>=2d.

For every t>=1 apply a^2>=2ta-t^2 on U, a^2>=2a-1 in the middle, and a^2>=2a in the negative range. Summing and replacing S_U by N-n gives

    Q >= 2tN - (2t-1)n - t^2 d.

If d>0 choose t=(N-n)/d>=2 and obtain

    Q >= n + (N-n)^2/d.

If d=0 all support points are simple and real and no division is needed. Define the nonnegative defect

    Delta = N-n-2d
          = sum_{real, m>=2}(m-2) + 2 sum_{nonreal conjugate pairs}(m-1).

Writing x=N-n=2d+Delta gives Q-N>=x(x+Delta)/(x-Delta). Minimizing the right side at x=(1+sqrt(2))Delta yields

    Q-N >= (3+2sqrt(2)) Delta.

Thus if Q/N<=A, Delta/N<=(A-1)/(3+2sqrt(2)), about 0.05619. A nonreal multiplicity-at-least-m tail, counted with multiplicity, costs at most m/(m-1) times Delta for m>=2; hence its proportion is <=[m/(m-1)](A-1)/(3+2sqrt(2)). Real multiplicity-at-least-m mass for m>=3 is <=[m/(m-2)]Delta. The m=2 nonreal statement recovers the existing simple-or-real union bound.

There is also a direct prior-art route: in Anthropic's arbitrary-c inequality, k_c(1)=2c-1 for c>=1 and k_c(m)<=c^2 for all larger multiplicities. Bounding the r higher real atoms and b pair blocks this way gives exactly the same parametric inequality. Consequently a paper should present the defect statement, at most, as a newly recorded multiplicity corollary with explicit antecedents; it cannot honestly claim discovery of the generalized inequality or an improvement to C0.

The envelope is sharp for the relaxed block-coefficient data: first-range coefficients all t, middle coefficients all 1, last range zero. That abstract sharpness is not realizability by a configuration of actual zeta zeros; it should not be confused with an arithmetic obstruction.

## Follow-up sources requiring separate triage

A primary-source search found the following relevant claims beyond the user's links; they were reported to the main research agent for deeper review:

- Biao Wang, arXiv:2609.07918 (September 7), short-interval pair correlation and Lamzouri transfer.
- https://github.com/trmdy/zeta-simple-zeros-673137 advertises a 67.3137630699% interval-certified bound using a stability refinement and shifted blocks from `ainta/zeta-simple-zeros`.
- https://zenodo.org/records/21975237 advertises 79.62% using higher moments; this is a claim, not a validated SOTA result in this audit.
- https://zeta-record.vercel.app/ advertises a `teal-sea/zeta-lab` record and Palomar n-point certificates. Headline unconditional language needs to be checked against the actual formal assumptions and analytic moment identities.
- Axiom's predecessor repository https://github.com/AxiomMath/ZetaZeros has earlier two-result statements and a later removal of an assumption. It is distinct from the V2 snapshot and should not be silently substituted.

The main technical risks in evaluating such improvements are whether an arbitrary-window analytic interface is actually proved, whether higher correlation/moment formulas introduce unsupported inputs, whether off-line complex differences are preserved, and whether interval certificates establish the final analytic implication rather than only a finite numeric optimization.

## Audit conclusion

The V2 source is a compact, well-delimited formalization of Lamzouri's four-count argument. Default-library compilation is verified at the pinned public commit. The two classical analytic assumptions remain explicit, and comparator verification is author-reported rather than independently reproduced here. Exact constants, integer multiplicities, complex Fourier arguments and asymptotic quantifiers are all visible and coherent. The strongest inexpensive next work is a bounded fresh comparator reproduction, a fully attributed multiplicity-corollary derivation, and a careful audit of claimed numerical improvements before announcing novelty or publishing.
