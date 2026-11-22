# The formal proof of the Riemann hypothesis released on 2026-11-20: review, state of verification, and what stays open

Date: 2026-11-21 (readings between 08:00 and 12:00 UTC). Written by the coordinating session on Felipe's order of
2026-11-21 ("review last claim from Anthropic, that they solved Riemann hypothesis, read and research online in
max depth for all the new works on that problem, and verify if any space of research is open"). Evidence marks:
[P] read by this session on the primary source; [T] a third party's published check, read on its own page; [R] a
delegated research report of 2026-11-21 (coordination repository, `wip/caos-research/rh-claim-reception`,
`rh-literature-refresh`, `rh-open-space`, each accepted with its open items); [D] a derivation of this programme.
This dossier reports who has shown what. It does not itself establish that the hypothesis is proved, and the
programme's own theorems do not depend on it. Sections 1 to 9 are the reading of 2026-11-21; the dated readings of
the watch list follow in section 10 (first reading: 2026-11-22).

## 1. The claim, on its primary source

- [P] A four-page unsigned note, `https://alpo.ge/remark.pdf` (245,114 bytes, SHA-256
  `3fc97784b71ddd44ff8aa0a177e99622a1c61b13cfa843a0989ee4a7a0cfeb8d`), on the site of Levent Alpoge (Anthropic;
  Society of Fellows, Harvard). Its words: "I believe I have, working with Claude, discovered a proof of the Riemann
  Hypothesis. In fact, the method easily extends much further, resolving the so-called Generalized Riemann
  Hypothesis, and I expect, with more time, the Extended Riemann Hypothesis too. Claude and I have also formalized
  the arguments without assumptions." The only artifact is Lean code, `https://alpo.ge/lean.tar.gz.part01` to
  `part14`. There is no written proof: "It being obviously inappropriate to attempt to post some massive
  unreadable travesty [...], I decided to only present Lean"; a generated text had "250,000+ pages".
- [P] The mathematics, as the note sketches it: "This argument is a descendant of Stepanov's"; multiplicity over
  the integers is obtained by "chaining theta lifts", "for the von Mangoldt sum of length X, Claude's suggested
  length of chain of theta lifts [...] was sqrt(X)"; a timeline of twenty steps dated 2026-10-06 to 2026-11-16
  names a Stepanov determinant, positivity of Weil's functional through determinants, Gan-Gross-Prasad and Bessel
  periods, iterated theta lifts between totally definite unitary groups, a Bost slope inequality, an Iwasawa tower,
  a relative trace formula, Chowla-Selberg, a weakening of Vandiver, and "11/16/26: GRH". The author states that
  parts of this description paraphrase a summary he cannot yet vouch for and that he expects simplifications.
- [R] The same author with R. Furman posted arXiv:2608.13637 in August 2026 (at least two thirds of the zeros simple
  and on the line, unconditionally; argument found by Claude; the baseline of this programme). The November proof
  is a different method; no source links the two. No official statement of Anthropic, of the Clay Mathematics
  Institute or of the Lean FRO was found on 2026-11-21. On 2026-11-22 a joint statement of the Lean and Mathlib
  communities, endorsed by the Lean FRO and the Mathlib Initiative and dated 2026-11-21 13:55, was read (section
  10); there was still none of Anthropic or of the Clay Institute.

## 2. What is formally stated

- [P] `src/Main.lean` of the archive (read on the mirror `leanprover-community/riemann-hypothesis`, commit 23aebbb3)
  has five theorems: `riemannHypothesis : RiemannHypothesis`; the same written out; and three statements on
  Dirichlet L-functions: no zero with real part above 1/2 for every modulus and every character (except the pole of
  the trivial character), every zero in the open critical strip on the line, and the same for primitive characters
  (`src/Statements.lean`, 16 lines, imports only Mathlib). "GRH" in the code means Dirichlet L-functions only.
  Dedekind zeta functions, Hecke, Artin and automorphic L-functions are not covered.
- [P] Statement check by this session, on Mathlib at the pinned commit `0df444a360eaa60ab8c11dca51a86af692955474`
  (file `Mathlib/NumberTheory/LSeries/RiemannZeta.lean`, SHA-256 `db9f37f0...2a1a9`): `riemannZeta` is defined as
  `hurwitzZetaEven 0` (line 121); `differentiableAt_riemannZeta` (line 139) gives differentiability at every
  s other than 1; `zeta_eq_tsum_one_div_nat_cpow` (line 207) gives riemannZeta s = sum of 1/n^s for Re s > 1. A
  function analytic on the plane minus the point 1 that equals the Dirichlet series on Re s > 1 is the zeta
  function, by uniqueness of analytic continuation. `RiemannHypothesis` (line 185) says: every zero other than
  the points -2(n + 1) and other than s = 1 has real part 1/2. That is the Riemann hypothesis. For characters,
  `DirichletCharacter.LFunction` equals the L-series for Re s > 1 (`LFunction_eq_LSeries`, line 75 of
  `DirichletContinuation.lean`) and is differentiable away from the pole (line 92), so it is the Dirichlet
  L-function.
- [T] The same comparison was made by hand by the verifiers (verification notes of the mirror; an independent
  reader, ishaan2006) and mechanically: Comparator's statement matching and `con-leche --compare` find the five
  theorems of the archive equal to the five of a challenge file that imports only Mathlib.

## 3. What has been checked, by whom (as of 2026-11-21 08:33 UTC; the later state is in section 10)

Source for every line unless said: `https://math.mit.edu/~drew/grh/` (A. Sutherland, MIT; last updated 2026-11-20
22:05 UTC; unchanged at 08:33 UTC on the 21st) [T], and the verification notes of the mirror [T].

| Check | Result |
|---|---|
| All 175,187 modules compile (Lean v4.33.1, Mathlib tag v4.33.1) | pass, zero errors |
| `#print axioms` of the five theorems | `propext`, `Classical.choice`, `Quot.sound` only |
| Static scan of the 17,374,215 lines | no `axiom`, `sorry`, `native_decide`, `unsafe`, `implemented_by`, `opaque`; two tactics (`kexactB`, `kcopy`) assign terms without elaborator type checking, so the kernel is the only check of those proofs |
| `leanchecker` replay of every module | 175,187 of 175,187 |
| nanoda (independent kernel, Rust) on the full export (61,570,595,788 bytes, SHA-256 `5ea74b91...be244e`) | accepts |
| con-leche (independent kernel), plain and `--compare` against the challenge | accepts; the five theorems "justified by the solution" |
| lean4lean (third kernel design) on the compiled modules | 175,187 of 175,187 (five with a raised step limit) |
| A second, independent build (ishaan2006, 94 cores, 401 minutes) [R] | its export is byte-identical to the first |
| Lean default kernel and hardened kernel on the export; `lake comparator` end to end | still running; no verdict published |
| A sandboxed build with the protocol of the mirror | not reported |
| Any rejection, crash or discrepancy of a kernel | none found in any source read |

Limits recorded by the verifiers themselves [T]: the builds were not sandboxed; Lean v4.33.1 predates runtime fixes
of v4.34.1 (issues 15241 and 15289, which could in principle be turned into a proof of False in the official kernel
with constructed input), which is why the judging uses independent kernels; "a passing check shows that the formal
statements, as written in Lean against Mathlib's definitions, follow from the three standard axioms according to
the kernels used". The Lean Zulip thread could not be read without an account [R].

This session could not replay a kernel: the published route needs 50 to 100 GB of memory and this device has 47.7.
What it checked itself is Section 2 and Section 5.

## 4. The proof as third parties have mapped it

[R], from issues 3, 5 and 12 of the mirror, a reader's guide on Zenodo (10.5281/zenodo.24410057) and reader
repositories; all are unofficial readings, several made with AI assistance, none by the author.

- Chain: the Riemann hypothesis is deduced from the nonvanishing of every Dirichlet L-function to the right of 1/2;
  that from a one-sided bound of square-root quality for weighted sums over primes, on windows, through a window
  form of Landau's theorem; the bound from Arakelov geometry (families of Hermitian lattices indexed by a code, a
  slope inequality of Bost type, near-orthogonality of period maps, a Chebyshev-type count of prime powers compared
  with a Chowla-Selberg period), with arithmetic inputs proved inside the archive (Galois representations through
  theta lifts, bounds for Tate-Shafarevich groups of Tate twists).
- Weaknesses flagged, none of which is a kernel failure: two classical inputs are present in a weaker form than the
  published theorems they are named after; ten statements on the chain have no reference in the literature (they
  are the new mathematics a referee would read); one clause is satisfied for a degenerate reason and is not used
  downstream; many declarations are off the path of the final theorems; the semantics of the archive's own
  definitions of classical objects has not been audited by experts.
- Reception [R]: T. Tao (blog, 2026-11-20): "has generated an (enormous) Lean-only proof of the Generalized Riemann
  Hypothesis"; "I imagine the digestion process will take some time". A. Sutherland: "This is indeed an historic
  moment"; "There is much work to be done to understand the mathematical details of the proof". J. Maynard: "If
  this fully checks out, it is clearly a historic milestone in mathematics". A. Granville: "What he released is
  garbled". M. Radziwill: the note contains "nonsensical statements". B. Conrey: "I really did not see this coming
  at all". Nothing was found from the persons named in the note's acknowledgements other than Radziwill.

## 5. The last step, checked on paper by this programme

[D] `2026-11-21-windowed-landau-endgame.md`: with G(x) = sum over n <= x of Lambda(n)(x/n - 1) - x log x +
(1 + gamma) x, a bound G(x) <= Y^eta x^theta on windows [Y, Y^(1 + delta)] for arbitrarily large Y and every
eta > 0 implies that zeta has no zero to the right of theta; the same for positive combinations over Dirichlet
characters. The proof was written from the Lean statements (`Formalism.Gz`, `Deduction.landau_window`,
`Deduction.zeroFree_of_rpow_window`), not from the proof terms. It was read twice by a reviewer other than the
writer on 2026-11-21. The first reading found that the formal lemma asks less than the note assumed (a positive
residue only at real poles, `PoleData`), and that the note's proof of the explicit formula gave a false reason; the
second version proves the lemma under the formal hypothesis, and the second reading found it correct as written
(fifteen findings in all, applied; report `wip/caos-research/rh-windowed-landau-review-2026-11-21.md` of the
coordination repository). A proof read twice by one reviewer is not a refereed proof. The explicit formula gives the converse size:
under the hypothesis, |G(x) - log 2 pi| <= 0.0461915 sqrt(x) + 0.31/x^2. EXP-029 is the numerical control of the
normalization (PASS on 2026-11-21: the explicit formula agrees at 460 points, and up to 10^8 the sum stays within
0.0247 sqrt(x) of log 2 pi, with both signs). This is the one piece of the formal proof this programme has verified independently of a kernel;
it is the easy end, and all the depth is upstream of it.

[P] The link above it was read in the Lean source itself (`src/Formalism/GammaFactorNonvanishing/CritLine.lean`, 30
lines). `Formalism.VW.critLine` takes a zero s of a primitive L(chi, s) with 0 < Re s < 1/2, uses Mathlib's
functional equation (`IsPrimitive.completedLFunction_one_sub`) and the nonvanishing of the gamma factor to produce
a zero of L(chi^-1, 1 - s) with real part above 1/2, against the half-plane statement; `Formalism.VW.rh_of_every`
applies the half-plane statement to the character of modulus 1, whose L-function is the zeta function
(`LFunction_modOne_eq`), and concludes through `rh_of_right`. This is the classical deduction of the line from the
half-plane, written with Mathlib's lemmas; nothing in it depends on the archive's own definitions. So the chain
reads, from the top: the hypothesis, from the half-plane statement for every Dirichlet character (functional
equation; read); the half-plane statement, from a one-sided bound on windows (Landau's theorem on windows; proved
on paper in the note); the one-sided bound, from the arithmetic geometry of the archive (not read by this
programme).

## 6. Assessment

- The evidence that the five formal statements are theorems of Lean with Mathlib is strong and of a new kind:
  three independent kernel designs accept the proof, two independent builds give the same export, the statements
  are Mathlib's own, and no axiom beyond the standard three is used. What remains pending is confirmatory (the
  reference kernel on the export, the end-to-end Comparator run, a sandboxed build). Reading of 2026-11-22 (section
  10): the sandboxed build is done and its export is byte-identical; a joint statement of the Lean and Mathlib
  communities, endorsed by the Lean FRO and the Mathlib Initiative, certifies the statement and the proof of the
  Riemann hypothesis; the MIT page still lists its own Lean-kernel run on the export and the end-to-end Comparator
  run as running.
- What is absent is understanding. No written proof exists, the author says he has not mastered parts of the
  argument, the experts quoted reserve judgment on the mathematics, and the new statements of the chain have not
  been read by referees. The rules of the Clay Mathematics Institute require publication in a refereed outlet, two
  years, and general acceptance, and say nothing about formal proofs [R].
- For this programme the working position is: treat the Riemann hypothesis and the generalized hypothesis for
  Dirichlet L-functions as formally verified statements whose acceptance is in progress (since 2026-11-22: formal
  verification certified for the Riemann hypothesis by the joint statement of section 10, acceptance as mathematics
  still in progress); state every new result
  either unconditionally or explicitly "under the Riemann hypothesis" (which is correct mathematics whatever the
  outcome); never describe a result of this programme as part of, or progress toward, that proof.

## 7. What stays open, and where this programme can still prove something

From [R] `rh-open-space` (rows marked UNVERIFIED there are not used here):

- Not covered by the five theorems: every result "under GRH" that needs Dedekind, Hecke, Artin or automorphic
  L-functions (Artin's primitive root conjecture after Hooley, generators of class groups after Bach, effective
  Chebotarev, ranks of elliptic curves). The note itself says the extended hypothesis needs more time.
- Not implied by any form of the hypothesis: simplicity of all zeros; Montgomery's pair correlation conjecture and
  the GUE statistics; linear independence of the ordinates; the true order of zeta on the line and of S(t); the
  moment conjectures; Cramer's conjecture.
- Zeros of zeta under the hypothesis, best known: at least 19/27 simple (Bui and Heath-Brown, arXiv:1302.5018,
  under RH alone); at least 0.8477 distinct (Chirre, Goncalves and de Laat, arXiv:1810.08843); multiplicity at most
  (1/2 + o(1)) log t/log log t (Goldston and Gonek). These dominate, once the hypothesis is a theorem, every
  global unconditional proportion of 2026, including the 0.6725 and 0.8362 of the programme's baseline, the
  0.67353 and 0.83900 of Knausgard (arXiv:2610.08965, 2026-10-06) and the programme's own distinct-zero constants.
- Short intervals: no theorem was found, with or without the hypothesis, giving a positive proportion of simple
  zeros in (T, T + T^theta] for theta at or below 0.5501 (Wang, arXiv:2609.07918v2; before, Steuding, 0.552),
  except this programme's unconditional 0.534 (`short-interval-levinson` v0.02, unrefereed).
- [D, written out in the barrier note and reviewed on 2026-11-21; the first wording here, that the pair correlation
  method should not pass that point even under the hypothesis, said more than is proved] Pair correlation with test
  functions supported in the band does not pass that point; under the hypothesis a relaxation lowers the onset to
  about 0.5487 (a probe), and inputs beyond the band under the hypothesis for Dirichlet L-functions are unexamined on
  windows. The reason for the band: on a window of length H = T^theta the
  mean value theorem for Dirichlet polynomials controls lengths up to about H, so the form factor is available for
  |alpha| < theta only, and the resulting bound for the sum of the multiplicities carries information only for
  theta above about 0.55 (with the Fejer kernel of that band, simple zeros at least 2 - 1/theta - theta/3,
  positive exactly for theta > 3 - sqrt(6) = 0.5505; Wang's 0.5501 is the same barrier with the optimal kernel).
  Mollified discrete moments of zeta'(rho) (Conrey, Ghosh and Gonek; Bui and Heath-Brown) give a positive
  proportion for a mollifier of any positive length, so with the programme's short-window twisted moments
  (mollifier T^nu, nu < theta - 1/2; EXP-010, EXP-028) they are the natural route to every theta > 1/2 under the
  hypothesis. This is the research space the plan of 2026-11-21 opens (focus RH-F17).
  The computation is written out in `2026-11-21-pair-correlation-band-barrier.md`: on a band lambda the method
  gives simple zeros at least 2 - lambda/2 - cot(lambda/sqrt 2)/sqrt 2, which vanishes at 0.550194 and equals
  0.41908 at 3/4, the two numbers of Wang's theorem; the source preflight of the focus read Wang's formula and it
  is the same, term by term.
- [R, a target, not a theorem] `2026-11-21-short-window-discrete-moments-target.md`: the two mollified discrete
  moments give, for a mollifier of length T^nu, the proportion 1 - 1/(1 + nu)^3 (a closed form derived from the
  main terms of the two papers; 19/27 at nu = 1/2). If a window of length T^theta admits nu < theta - 1/2, the
  proportion of simple zeros in it is at least 1 - 8/(2 theta + 1)^3 for every theta in (1/2, 1]. The preflight
  found that the only step of the two papers without a short-window form under the Riemann hypothesis alone is the
  bound for characters of large conductor, and that under the hypothesis for Dirichlet L-functions that step is
  pointwise. So the target is stated under exactly the two statements of the formal proof. Its proof obligations
  are the units of line B of the plan. `2026-11-21-window-moments-by-subtraction.md` reduces it to three named
  inputs: the identities of the two papers are additive in the height, so every term of size T^(1/2) y passes by
  subtraction; what remains is the mean square of the mollified zeta and zeta' on the window (unconditional, of the
  kind the programme already uses), a pointwise bound for twisted coefficient sums under the two hypotheses, and
  the derivative of the main terms. The barrier note and the target note were read by a reviewer on 2026-11-21
  (one blocker, the overclaim above; five major and twelve minor findings, applied); the reduction note was read by
  the same reviewer the same day (six minor findings, applied; no blocker, no major).

## 8. New works since the last pass (2026-10-04), from [R] `rh-literature-refresh`

- Knausgard, arXiv:2610.08965 (2026-10-06): distinct zeros at least 1645064/1960733 = 0.83900..., simple and
  critical at least 0.67353..., Lean 4 proofs with three axioms that record search-program results. It supersedes
  as a record the 0.8371747... and 0.8373797... of `distinct-zero-gram` v0.01 (which stay true statements).
- Wang, arXiv:2609.24167: withdrawn by its author (confirmed); arXiv:2609.07918 v2 unchanged at onset 0.5501.
- Lamzouri, arXiv:2611.14486 (small gaps, 0.7892) and arXiv:2610.26841 (isolated zeros, 13/20); Cobeli and
  Zaharescu, arXiv:2610.23467 (simple or on the line, more than 8/9); Arias de Reyna, arXiv:2610.24612 (a human
  exposition of the 0.6725 theorem); Goulden, arXiv:2611.23332 (Gram's law for moving targets, threshold
  0.5339..., the same decimals as this programme's internal onset for a different statement: to be examined).
- The zero-free half-plane of OpenAI (2026-10-06, Re s > 7/8, unrefereed) and five preprints that refine or use it
  (Liu, arXiv:2610.12234 and 2610.26835; Xu and Sang, 2610.15291; Ji, 2611.16665; one more); a conditional and an
  unconditional bound for the de Bruijn-Newman constant.
- No arXiv paper presents or reviews the proof of 2026-11-20.

## 9. Sources kept

Copies with SHA-256 under the data root, `caos-research/riemann-hypothesis/claim-2026-11-20/`: `coordinator/` (the
note, the MIT page as text, the mirror's README, notes, issues 2, 3, 5, 12, the statement and main files, the Lean
files of the last step, the two Mathlib files at the pinned commit) and one folder per research report. Manifest:
`source-manifest-claim-20261121.json`.

## 10. Watch readings (backlog RH-055)

### Reading 1: 2026-11-22, sources fetched 03:49 to 03:52 UTC (machine clock, within a second of the MIT server's)

The four sources of the watch list, and the post that prompted the reading (sent by Felipe). Copies with SHA-256 under
the data root, `caos-research/riemann-hypothesis/claim-2026-11-20/watch-2026-11-22/` (`SHA256SUMS.txt`).

- [P] The joint statement "Lean verification of the Riemann Hypothesis" on the Lean community blog
  (`https://leanprover-community.github.io/blog/posts/riemann-hypothesis/`, dated 2026-11-21 13:55; page
  `f1bc87e6...9a35`, source `0742e573...eeea`), "by the Lean and Mathlib communities, endorsed by the Lean FRO and
  the Mathlib Initiative". Its words: "We have full confidence that Alpöge's proof of the Riemann Hypothesis is
  correct"; "We hereby certify that both the statement and the proof of the Riemann Hypothesis are correct. The
  four criteria in [the Xena post below] are all satisfied." Its reasons: the statement is Mathlib's
  `RiemannHypothesis`; "dozens of people have reported correct compilation of the codebase, reproducing the same
  raw proof export file"; a file that states the theorem and imports only Mathlib was compared with the proved
  theorem "using two independent tools (comparator and con-leche --compare)"; the export "has been checked by
  several proof checkers, including Lean's official kernel, the con-leche and con-ron checkers, and several
  independent checkers contributed by third parties and implemented in different programming languages"; "The
  checkers con-leche and con-ron come with a formal proof, relative to set theory, that they cannot accept a false
  proof"; the checks "ran on an inert export of the proof". It closes: "We look forward to all the activity in the
  mathematical community that will help explain the new ideas in this proof." It names the Riemann hypothesis only
  and says nothing of the three statements on Dirichlet L-functions, which the MIT page lists as checked by the
  same runs. Its "17 million lines" agrees with the static scan of section 3 (17,374,215).
- [P] The four criteria (Xena project, 2026-11-12, "...and the proof is checked in Lean", `f74a2a80...51ef1`):
  (1) the Lean statement matches the informal statement; (2) the code compiles; (3) the code proves the theorem as
  stated (`lake comparator`: the statement of a trusted file equals the one proved, with the standard axioms only);
  (4) the proof does not exploit a bug of Lean's kernel (several independent kernels; `lake comparator
  --paranoid`). The post adds that a Lean proof that passes all four says nothing on the correctness of a written
  proof that accompanies it.
- [T] The MIT page, "last updated 2026-11-22 03:50 UTC" (fetched 03:49:47; `c9f09ce1...d59d`). New since 2026-11-21 08:33: an
  independent `lake build Main` in a bubblewrap sandbox (no network, source read-only, archive downloaded afresh),
  on a separate machine, pass at 18:07 UTC on the 21st; the export made inside that sandbox is byte-identical to the
  published one (61,570,595,788 bytes); 175,186 of its 175,187 compiled files equal the first build's, the
  exception being one module whose output depends on a race in parallel elaboration (the name of a bound variable
  in an automatically generated equation lemma that is not in the export; Lean issue 15498, fixed in v4.36.0);
  Mathlib's files equal the official cache; con-leche built from master accepts the full export (1,468,418
  declarations, `--verified` mode); con-ron, its Rust port, accepts in `--compare` mode with all five theorems
  "justified by the solution"; the challenge export equals the one the mirror's CI publishes. A check that does not
  rest on Mathlib's definition of the zeta function: with an independent formalization of the criteria of Robin and
  of Lagarias (`kimihiro64/Robin1984`, commit `acab1a3`) the proof yields Robin's inequality for every n > 5040 and
  Lagarias's inequality for every n >= 1, statements on the divisor sum alone, accepted by con-leche, con-ron and
  nanoda (the Comparator run on that combined export still running). Still running at 03:50 UTC: "Lean default
  kernel and Lean paranoid kernel on the export" and "lake comparator (Lean v4.36.0) end to end", whose statement
  comparison and axiom check have passed and whose kernel stages are single-threaded on a 62 GB export.
- [T] The mirror `leanprover-community/riemann-hypothesis` (head `f1f6d654`, 2026-11-22 03:33 UTC; the address
  `Deicyde/riemann-hypothesis` now redirects to it). The Results section of its notes (`e6aef798...de45`) still
  reads "The build is in progress." Since the 21st, cleanup pull requests 8, 45 and 57 removed 10,724 of the
  175,187 files and edited 18 (the count of the notes; pull requests 60 and 65, merged after it on the 22nd, shorten
  proof terms in further modules); the five statements are unchanged; commit `40e56bab` is the archive as published,
  and every check above was run on the archive as published, not on the cleaned tree. The notes record that
  con-leche and con-ron as bundled with Lean v4.36.0 exit 2 on a mutual inductive block with a reflexive member
  (`PrincipalizationCertificate`), so the mirror's Comparator configuration names only Lean paranoid and nanoda;
  the MIT page reports that both checkers built from master accept.
- [P] arXiv (API, newest 60 abstracts with "Riemann hypothesis", and every listing of the author): no paper presents
  or reviews the proof; the author's newest listing is of 2026-09-15; the newest abstract in the listing is of
  2026-11-19. Read again on the 24th.
- [P] Anthropic (news page) and the Clay Mathematics Institute (news page, newest item 2026-09-11; the page of the
  problem unchanged): no statement on the claim. News reports found by a search say the same of Anthropic.
- Not read: the Lean Zulip thread the statement links (an account is needed; the public archive has no copy).

What the reading changes:

- The four criteria, for the statement as written against Mathlib, are now certified by a joint statement that the
  Lean FRO and the Mathlib Initiative endorse, not only reported by individual verifiers.
- An unreconciled detail: the joint statement says Lean's official kernel checked the export; the MIT page, updated
  later (03:50 UTC on the 22nd), still lists its own run of Lean's kernels on the export as running, and the run of Lean's kernel that
  has passed there is the replay module by module (`leanchecker`, 175,187 of 175,187) on the compiled files. The
  sources read do not say which run the statement means. It does not touch the verdicts of nanoda, con-leche and
  con-ron on the export.
- Of the confirmatory items of section 6, the sandboxed build is done; the Lean-kernel run on the export and the
  end-to-end Comparator run stay open.
- Still absent: a written proof, a referee, any statement by Anthropic or by the Clay Institute, and any reading of
  the new mathematics beyond those of section 4; the joint statement itself leaves the explanation to "the
  mathematical community". The end condition of the watch list (plan, line A, item 4) is not met.
- The rule of the plan stands: every result of this programme is stated unconditionally or "under the Riemann
  hypothesis", never "because the hypothesis was proved".

Next readings: 2026-11-24 and 2026-11-28, then weekly.

### Addendum to reading 1 (2026-11-22, later the same day): sources the reviews of 2026-11-21 and 2026-11-22 missed

Three sources were not found by the searches of the two readings and were read after Felipe's correction of
2026-11-22 (the programme had not explored the proof's own fields; `program/riemann-hypothesis/research-lines-2026-11-22.md`):

- [P] R. Zhang (IHES), "A preliminary note on Alpoge's proposed proof of the generalized Riemann hypothesis", 73 pages,
  dated 2026-11-21, `https://www.ihes.fr/~rzhang/files/GRH%20note.pdf` (SHA-256 `2cbd7e9b...2ad9`; copy under the data
  root, `caos-research/millennium-review-2026-11-22/rh-anatomy/`). The first reading of the mathematics by a
  mathematician: the author says he prompted an AI system to infer a readable proof from the Lean code, rewrote its
  output, cannot claim the text is faithful to the code, and that most of Sections 2 to 6 were written by AI. Its
  outline (nine steps, seven fields) is transcribed in Section 1 of the research-lines file. It states the exponent
  1/2 as the balance of two errors of sizes x/m and m in the number m of theta lifts, which is the "chain of length
  sqrt(X)" of the author's note.
- [N] A second proposed proof, human, of GRH for the Hecke L-functions of all unitary Hecke characters of every number
  field, by A. M. Masullo, announced on 2026-11-20 on R. Vakil's Math 216 site (cited by Zhang, footnote 1, as [Mas26]);
  reported in news as reviewed for months by B. Conrad, with problems reported since; not read on its primary source.
  If it holds, it covers what Section 7 lists as not covered by the formal proof.
- [P] A community reading blueprint, `https://github.com/chrisflav/riemann-blueprint` (461 statements in four chapters,
  each labelled published, modified from the literature, or new in the proof; made by static analysis of the source,
  without a build; its README lists its known limits).


## How could this be wrong?

- A defect shared by the kernels that accepted the proof, or a flaw in Mathlib's definitions of the functions
  involved, would not be seen by any check listed; the second is unlikely for definitions with the analytic
  continuation and the Dirichlet series both proved in the library, the first is what the pending runs and the
  different kernel designs address.
- Sections 4, 7 and 8 rest on delegated reports with open items; their statements are marked [R] and the rows
  those reports call UNVERIFIED were left out.
- The state of verification changes by the hour. The watch list of the plan fixes when it is read again.
- The joint statement of 2026-11-22 (section 10) certifies a formal object: that the statements written against
  Mathlib follow from the standard axioms according to the checkers named. It does not certify Mathlib's definitions
  beyond the expert vetting it cites, and it says nothing of a written argument, which does not exist.
